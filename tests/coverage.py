#!/usr/bin/env python3
"""Report the acceptance examples in design/examples.md that no test, fixture or hallway record cites.

Information, not a failure: an example without a test is a known gap, listed so that it stays visible.
A citation is the example's ID as a word ("E12") in tests/, benchmarks/ or design/hallway/.
"""

import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]


def main():
    examples = re.findall(r"^- \*\*(E\d+)\*\* \(([a-z]+)", (REPO / "design" / "examples.md").read_text(), re.M)
    cited = set()
    for d in ("tests", "benchmarks", "design/hallway"):
        for f in (REPO / d).rglob("*"):
            if f.is_file() and f.resolve() != Path(__file__).resolve() and f.suffix in (".py", ".md", ".sh", ".txt", ".yaml"):
                cited |= set(re.findall(r"\bE\d+\b", f.read_text(errors="replace")))
    missing = [f"{e} ({prio})" for e, prio in examples if e not in cited]
    covered = len(examples) - len(missing)
    print(f"examples covered by a test or fixture: {covered} of {len(examples)}")
    if missing:
        print("not covered: " + ", ".join(missing))


if __name__ == "__main__":
    main()
