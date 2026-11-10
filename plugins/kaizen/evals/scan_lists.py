#!/usr/bin/env python3
"""List the eval runs whose final reply uses markdown numbered-list syntax (principal, 2026-11-10: a display
renumbers such a list from its first number, so answers by number went to the wrong items; the standing
instructions ask for bold labels, "- **7** ...").

    scan_lists.py [RESULT_FOLDER ...]   default: every folder under results/

Reads only what the runs already wrote, so it costs nothing. A reply counts when a numbered item stands outside a
code block; one with gaps ("17. 18. 35.") is shown renumbered. A list the person asked for is also reported: the
reader judges those (rare; an LLM triage only if they turn up often).
"""

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "scripts"))
from transcript import numbers  # noqa: E402  the same parser as `transcript.py messages`


def final_reply(run: dict) -> str:
    """The run's last reply: from its trace when it still exists, else from a grader's evidence that is not a trace."""
    trace = run.get("tracePath")
    if trace and Path(trace).is_file():
        last = ""
        for line in open(trace):
            try:
                o = json.loads(line)
            except ValueError:
                continue
            if o.get("type") == "assistant":
                for b in (o.get("message") or {}).get("content") or []:
                    if isinstance(b, dict) and b.get("type") == "text":
                        last = b["text"]
        if last:
            return last
    for g in run.get("graders", []):
        ev = g.get("evidence")
        if isinstance(ev, str) and ev.strip() and not ev.lstrip().startswith(("{", "[")):
            return ev
    return ""


def scan(folder: Path, out=sys.stdout):
    try:
        data = json.loads((folder / "aggregate-result.json").read_text())
    except (OSError, ValueError):
        return 0, 0
    total = hits = 0
    for case in data.get("cases", []):
        name = "/".join(Path(case.get("dir", "?")).parts[-2:])
        for arm, runs in (case.get("arms") or {}).items():
            for i, run in enumerate(runs, 1):
                text = final_reply(run)
                if not text:
                    continue
                total += 1
                kinds = []
                nums = numbers(text, kinds)
                listed = [n for n, k in zip(nums, kinds) if k == "list"]
                if listed:
                    hits += 1
                    gaps = any(b != a + 1 for a, b in zip(listed, listed[1:]))
                    note = "gaps: shown renumbered" if gaps else "no gaps"
                    print(f"{folder.name}  {name}  {arm} run {i}: numbers {','.join(map(str, listed))} ({note})", file=out)
    return total, hits


def main(argv):
    folders = [Path(a) for a in argv] or sorted(p for p in (HERE / "results").iterdir() if p.is_dir())
    total = hits = 0
    for f in folders:
        t, h = scan(f)
        total, hits = total + t, hits + h
    print(f"{hits} of {total} replies in list syntax")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
