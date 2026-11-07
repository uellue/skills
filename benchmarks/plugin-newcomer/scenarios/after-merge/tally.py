#!/usr/bin/env python3
"""tally: count log lines per level (INFO, WARNING, ERROR) in instrument log files."""

import re
import sys
from collections import Counter

LEVEL = re.compile(r"\b(DEBUG|INFO|WARNING|ERROR|CRITICAL)\b", re.IGNORECASE)  # hallway test 2026-11-07, bug 1


def tally(paths):
    counts = Counter()  # keeps the order in which levels first appear (hallway test 2026-11-07, item 3)
    for path in paths:
        with open(path) as f:
            for line in f:
                m = LEVEL.search(line)
                if m:
                    counts[m.group(1).upper()] += 1
    return counts


def main():
    if len(sys.argv) < 2:
        print("usage: tally.py LOGFILE...", file=sys.stderr)
        return 2  # hallway test 2026-11-07, bug 2
    for level, n in tally(sys.argv[1:]).items():
        print(f"{level:8} {n}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
