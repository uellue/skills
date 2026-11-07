#!/bin/sh
# The repository's one check: script tests on synthetic transcripts and the lint of the skill texts.
# Run before calling anything ready; the pre-commit hook and CI run exactly this.
# Afterwards it lists the acceptance examples that no test covers and the glossary words to avoid in
# added lines (information, not failures).
cd "$(dirname "$0")" || exit 1
python3 -m unittest discover -s tests "$@" || exit 1
python3 tests/coverage.py
python3 tests/avoid_words.py
