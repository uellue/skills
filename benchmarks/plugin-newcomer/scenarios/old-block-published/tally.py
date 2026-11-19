#!/usr/bin/env python3
"""tally: count log lines per level (INFO, WARNING, ERROR) in instrument log files."""

import re
import sys
from collections import Counter

LEVEL = re.compile(r"\b(DEBUG|INFO|WARNING|ERROR|CRITICAL)\b")


def tally(paths):
    counts = Counter()
    for path in paths:
        with open(path) as f:
            for line in f:
                m = LEVEL.search(line)
                if m:
                    counts[m.group(1)] += 1
    return counts


def main():
    if len(sys.argv) < 2:
        print("usage: tally.py LOGFILE...")
        return
    for level, n in sorted(tally(sys.argv[1:]).items()):
        print(f"{level:8} {n}")


if __name__ == "__main__":
    main()
