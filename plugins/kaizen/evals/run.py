#!/usr/bin/env python3
"""Run the plugin's eval suites within a stretch's budget (principal, 2026-11-10: 325 runs, $96.74 in one day hit the
session limit; "Standing instructions didn't work too well regarding budget").

    run.py --new-stretch [BUDGET] [--force]   start a stretch with a budget in dollars at list price (default 20);
                                              refused while the current stretch has spend, unless --force (it is kept)
    run.py --status                           what the stretch has spent
    run.py LABEL [--plugin PATH] <claude plugin eval args>
                                              one eval run: needs --max-cost-usd; refused when the stretch's spend
                                              plus that ceiling would pass three quarters of the budget (the reserve);
                                              --plugin runs another copy, e.g. an older version, in the same stretch;
                                              one run, plugin arm only, unless --runs or --ablation say otherwise

A run writes into results/<date>-<time>-LABEL with its run.log; the system's Python comes first on PATH (the eval
sandbox hides the home directory, see README). The spend counts each run's measured cost, or its ceiling while it
runs or when it left no result. A ceiling does not stop a run in progress, which is why the stretch stops with a
quarter left. The stretch file is locked while a run is checked and recorded, so parallel runs share one budget.
"""

import fcntl
import json
import math
import os
import re
import subprocess
import sys
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent
PLUGIN = HERE.parent
RESULTS = Path(os.environ.get("KAIZEN_EVAL_RESULTS") or HERE / "results")
CLAUDE = os.environ.get("KAIZEN_EVAL_CLAUDE") or "claude"
STRETCH = RESULTS / ".stretch.json"
DEFAULT_BUDGET = 20.0
RESERVE = 0.25


class Corrupt(Exception):
    pass


@contextmanager
def locked():
    RESULTS.mkdir(parents=True, exist_ok=True)
    with open(RESULTS / ".stretch.lock", "w") as f:
        fcntl.flock(f, fcntl.LOCK_EX)
        yield


def load():
    """The current stretch, None when there is none; Corrupt when the file cannot be read as one."""
    if not STRETCH.exists():
        return None
    try:
        s = json.loads(STRETCH.read_text())
        float(s["budget"]), s["start"], list(s["runs"])
        return s
    except (OSError, ValueError, KeyError, TypeError) as e:
        raise Corrupt(f"{STRETCH} is corrupt ({e}); look at it before starting a new stretch") from e


def save(s):
    """Write the stretch whole: a reader outside the lock sees the old file or the new one, never half of it."""
    tmp = STRETCH.with_name(f"{STRETCH.name}.{os.getpid()}.tmp")
    tmp.write_text(json.dumps(s, indent=1))
    os.replace(tmp, STRETCH)


def spent(s) -> float:
    total = 0.0
    for r in s["runs"]:
        try:
            total += float(json.loads((Path(r["dir"]) / "aggregate-result.json").read_text())["costUsd"] or 0)
        except (OSError, ValueError, KeyError, TypeError):
            total += r["ceiling"]  # still running, or no result: count what it may spend
    return total


def status(s):
    used, limit = spent(s), s["budget"] * (1 - RESERVE)
    print(f"stretch since {s['start']}: spent ${used:.2f} of ${s['budget']:.2f}; runs stop at ${limit:.2f}, {len(s['runs'])} runs")


def amount(text) -> float:
    """A positive, finite amount of dollars, or ValueError."""
    v = float(text)
    if not math.isfinite(v) or v <= 0:
        raise ValueError(text)
    return v


def new_stretch(argv) -> int:
    force = "--force" in argv
    rest = [a for a in argv if a != "--force"]
    try:
        budget = amount(rest[0]) if rest else DEFAULT_BUDGET
    except ValueError:
        print(f"the budget must be a positive amount of dollars, not {rest[0]!r}", file=sys.stderr)
        return 2
    with locked():
        try:
            old = load()
        except Corrupt:
            old = None if force else "corrupt"
            if old:
                print(f"{STRETCH} is corrupt; look at it, then --new-stretch --force", file=sys.stderr)
                return 2
        if old and old["runs"] and not force:
            print(f"refused: the current stretch (since {old['start']}) has spent ${spent(old):.2f} of "
                  f"${old['budget']:.2f}. A new budget is the person's decision: --new-stretch {budget:g} --force",
                  file=sys.stderr)
            return 3
        if STRETCH.exists():
            STRETCH.rename(RESULTS / f".stretch-{datetime.now():%Y%m%d-%H%M%S}.json")  # kept, not overwritten
        s = {"start": datetime.now().isoformat(timespec="seconds"), "budget": budget, "runs": []}
        save(s)
    print(f"new stretch: budget ${budget:.2f}; runs stop at ${budget * (1 - RESERVE):.2f}, a quarter kept in reserve")
    return 0


def main(argv):
    if argv[:1] == ["--new-stretch"]:
        return new_stretch(argv[1:])
    try:
        s = load()
    except Corrupt as e:
        print(e, file=sys.stderr)
        return 2
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
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]*", label) or ".." in label:
        print(f"a label is a plain name (letters, digits, '.', '_', '-'), not {label!r}", file=sys.stderr)
        return 2
    if args.count("--case") > 1:
        print("give one --case glob (claude plugin eval keeps only the last); run each suite on its own", file=sys.stderr)
        return 2
    # principal 2026-11-11: one run with the plugin is the default; repeats and the baseline arm only when asked
    for flag, default in (("--runs", "1"), ("--ablation", "none")):
        if flag not in args:
            args = [*args, flag, default]
    if "--output-dir" in args:
        print("run.py sets --output-dir itself (results/<date>-<label>)", file=sys.stderr)
        return 2
    plugin = PLUGIN
    if "--plugin" in args:
        i = args.index("--plugin")
        plugin = Path(args[i + 1]).resolve() if i + 1 < len(args) else None
        args = args[:i] + args[i + 2:]
        if plugin is None or not plugin.is_dir():
            print("--plugin needs the folder of a plugin", file=sys.stderr)
            return 2
    try:
        ceiling = amount(args[args.index("--max-cost-usd") + 1])
    except (ValueError, IndexError):
        print("give --max-cost-usd with a positive amount: the most this run may cost, at list price", file=sys.stderr)
        return 2
    with locked():
        s = load()
        used, limit = spent(s), s["budget"] * (1 - RESERVE)
        if used + ceiling > limit:
            print(f"refused: spent ${used:.2f}, this run may cost up to ${ceiling:.2f}, the stretch stops at "
                  f"${limit:.2f} (budget ${s['budget']:.2f}). Ask the person before going on.", file=sys.stderr)
            return 3
        out = RESULTS / f"{datetime.now():%Y%m%d-%H%M%S}-{label}"
        out.mkdir(parents=True, exist_ok=True)
        s["runs"].append({"dir": str(out), "label": label, "ceiling": ceiling})
        save(s)
    env = {**os.environ, "PATH": "/usr/bin:" + os.environ.get("PATH", "")}
    try:
        with open(out / "run.log", "w") as log:
            p = subprocess.run([CLAUDE, "plugin", "eval", str(plugin), *args, "--output-dir", str(out)],
                               env=env, stdout=log, stderr=subprocess.STDOUT)
        code = p.returncode
    except OSError as e:
        print(f"could not start {CLAUDE}: {e}; the run counts at its ceiling", file=sys.stderr)
        code = 1
    text = (out / "run.log").read_text()
    if "CASE" in text:  # the summary table at the end of the log
        print("CASE" + text.split("CASE", 1)[1][:2000])
    print(out)
    sys.path.insert(0, str(HERE))
    from scan_lists import scan  # replies in markdown numbered-list syntax, which a display renumbers

    total, hits = scan(out)
    print(f"{hits} of {total} replies in list syntax")
    status(load())
    return code


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
