#!/bin/bash
# Fixture for the walkthrough eval cases: a tiny tool with a README, a stakeholder record with two personas
# and one acceptance example. The same script sits in every case of evals/walkthrough/ (a scaffold
# script must be in its case's directory); change all copies together.
set -euo pipefail
mkdir -p design tally
cat > README.md <<'EOF'
# tally

Counts the files in a directory tree by extension, for checking a microscope session's export before it is archived.

## Install

    pip install -e .

## Use

    tally /data/session-2026-11-02

Prints one line per extension with the number of files and their total size.
EOF
cat > pyproject.toml <<'EOF'
[project]
name = "tally"
version = "0.1.0"
requires-python = ">=3.10"
[project.scripts]
tally = "tally.cli:main"
EOF
cat > tally/__init__.py <<'EOF'
EOF
cat > tally/cli.py <<'EOF'
import collections
import pathlib
import sys


def parse_args(argv):
    if len(argv) != 1:
        sys.exit("usage: tally <directory>")
    return pathlib.Path(argv[0])


def main(argv=None):
    root = parse_args(sys.argv[1:] if argv is None else argv)
    counts = collections.Counter()
    sizes = collections.Counter()
    for path in root.rglob("*"):
        if path.is_file():
            counts[path.suffix] += 1
            sizes[path.suffix] += path.stat().st_size
    for suffix, n in sorted(counts.items()):
        print(f"{suffix or '(none)'}\t{n}\t{sizes[suffix]}")
EOF
cat > design/stakeholders.md <<'EOF'
# Stakeholders of tally

## The new PhD student

Who: starts in the group this month; exports their first sessions from the microscope PC.
Wants: to know the export is complete before the raw data is deleted from the acquisition PC.
Knows: Python from their studies; not the group's servers or the archive.
Has: a laptop with Python 3.12; an account on the analysis server.
Never reads: anything beyond the README's first screen.
Confidence: simulated.

## The facility operator

Who: runs the microscope and the transfer of data to the archive.
Wants: a check they can run on every session without thinking about it.
Knows: the archive and the acquisition PC well; little Python.
Has: the acquisition PC (Windows, no admin rights), the analysis server.
Never reads: code.
Confidence: simulated.
EOF
cat > design/examples.md <<'EOF'
# Acceptance examples

- E1 (must): when `tally` runs on an empty directory, then it prints nothing and exits 0.
EOF
git init -q
git add -A
git -c user.name=fixture -c user.email=fixture@example.invalid commit -q -m "tally 0.1.0"
