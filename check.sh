#!/bin/sh
# The repository's one check: script tests on synthetic transcripts and the lint of the skill texts.
# Run before calling anything ready; the pre-commit hook and CI run exactly this.
cd "$(dirname "$0")" || exit 1
exec python3 -m unittest discover -s tests "$@"
