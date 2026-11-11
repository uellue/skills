#!/bin/bash
# Fixture for the numbering cases (principal 2026-11-10, item 56): a small tool whose CLAUDE.md carries the kaizen
# numbering line, copied from references/standing-instructions.md; tests/test_evals.py does not check the copy.
set -euo pipefail
git init -q -b main .
cat > README.md <<'EOF'
# tally

Counts the files in a directory tree by extension. Tests: `python3 -m pytest` after `pip install -e .[test]`.
EOF
cat > CLAUDE.md <<'EOF'
# tally

## Working rules
- Number every item and question you put to the person in one sequence across your messages, each as a bullet with its number in bold (`- **7** …`), never as a markdown numbered list (`7. …`), which a display renumbers. An open item restated keeps its number; no item without a number, no jumps; restart at 1 only when nothing is open and nothing is still to come back from work in the background.
EOF
