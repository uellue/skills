#!/usr/bin/env python3
"""Run the plugin's eval suites within a stretch's budget (principal, 2026-11-10: 325 runs, $96.74 in one day hit the
session limit; "Standing instructions didn't work too well regarding budget").

    run.py --new-stretch [BUDGET]           start a stretch with a budget in dollars at list price (default 20)
    run.py --status                         what the stretch has spent
    run.py LABEL <claude plugin eval args>  one eval run: needs --max-cost-usd; refused when the stretch's spend
                                            plus that ceiling would pass three quarters of the budget (the reserve)

A run writes into results/<date>-<time>-LABEL with its run.log; the system's Python comes first on PATH (the eval
sandbox hides the home directory, see README). The spend counts each run's measured cost, or its ceiling when a run
left no result. A ceiling does not stop a run in progress, which is why the stretch stops with a quarter left.
"""

import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent
PLUGIN = HERE.parent
RESULTS = Path(os.environ.get("KAIZEN_EVAL_RESULTS") or HERE / "results")
CLAUDE = os.environ.get("KAIZEN_EVAL_CLAUDE") or "claude"
STRETCH = RESULTS / ".stretch.json"
DEFAULT_BUDGET = 20.0
RESERVE = 0.25


def load():
    try:
        return json.loads(STRETCH.read_text())
    except (OSError, ValueError):
        return None


def spent(s) -> float:
    total = 0.0
    for r in s["runs"]:
        try:
            total += float(json.loads((Path(r["dir"]) / "aggregate-result.json").read_text())["costUsd"] or 0)
        except (OSError, ValueError, KeyError, TypeError):
            total += r["ceiling"]  # no result: count what it was allowed to spend
    return total


def status(s):
    used, limit = spent(s), s["budget"] * (1 - RESERVE)
    print(f"stretch since {s['start']}: spent ${used:.2f} of ${s['budget']:.2f}; runs stop at ${limit:.2f}, {len(s['runs'])} runs")


def main(argv):
    if argv[:1] == ["--new-stretch"]:
        budget = float(argv[1]) if len(argv) > 1 else DEFAULT_BUDGET
        RESULTS.mkdir(parents=True, exist_ok=True)
        s = {"start": datetime.now().isoformat(timespec="seconds"), "budget": budget, "runs": []}
        STRETCH.write_text(json.dumps(s, indent=1))
        print(f"new stretch: budget ${budget:.2f}; runs stop at ${budget * (1 - RESERVE):.2f}, a quarter kept in reserve")
        return 0
    s = load()
    if s is None:
        print("no stretch yet: agree the budget with the person, then run.py --new-stretch [BUDGET]", file=sys.stderr)
        return 2
    if argv[:1] == ["--status"]:
        status(s)
        return 0
    if not argv or argv[0].startswith("-"):
        print(__doc__, file=sys.stderr)
        return 2
    label, args = argv[0], argv[1:]
    if "--output-dir" in args:
        print("run.py sets --output-dir itself (results/<date>-<label>)", file=sys.stderr)
        return 2
    if "--max-cost-usd" not in args:
        print("give --max-cost-usd: the most this run may cost, at list price", file=sys.stderr)
        return 2
    ceiling = float(args[args.index("--max-cost-usd") + 1])
    used, limit = spent(s), s["budget"] * (1 - RESERVE)
    if used + ceiling > limit:
        print(f"refused: spent ${used:.2f}, this run may cost up to ${ceiling:.2f}, the stretch stops at ${limit:.2f} "
              f"(budget ${s['budget']:.2f}). Ask the person before going on.", file=sys.stderr)
        return 3
    out = RESULTS / f"{datetime.now():%Y%m%d-%H%M%S}-{label}"
    out.mkdir(parents=True)
    s["runs"].append({"dir": str(out), "label": label, "ceiling": ceiling})
    STRETCH.write_text(json.dumps(s, indent=1))
    env = {**os.environ, "PATH": "/usr/bin:" + os.environ.get("PATH", "")}
    with open(out / "run.log", "w") as log:
        p = subprocess.run([CLAUDE, "plugin", "eval", str(PLUGIN), *args, "--output-dir", str(out)],
                           env=env, stdout=log, stderr=subprocess.STDOUT)
    text = (out / "run.log").read_text()
    if "CASE" in text:  # the summary table at the end of the log
        print("CASE" + text.split("CASE", 1)[1][:2000])
    print(out)
    status(s)
    return p.returncode


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
