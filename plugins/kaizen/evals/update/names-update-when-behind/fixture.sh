#!/bin/bash
# Fixture for the update eval cases (ledger 280, E33): a small tool whose CLAUDE.md carries the kaizen standing
# instructions. VERSION_LINE is empty here (a copy from before 0.6, no version line); silent-when-current sets
# a version far in the future. The same script sits in both cases of evals/update/; change both together.
set -euo pipefail
VERSION_LINE=""
git init -q .
cat > README.md <<'EOF'
# tally

Counts the files in a directory tree by extension, for checking a microscope session's export before it is archived.

    tally /data/session-2026-11-02
EOF
{
  printf '# tally\n\nTests: `python3 -m pytest`.\n\n## Working rules\n\n'
  [ -n "$VERSION_LINE" ] && printf '%s\n' "$VERSION_LINE"
  cat <<'EOF'
- Keep changes tight: no speculative generality, no abstraction without a second concrete user.
- A request phrased as a question is a question: answer it first with a verdict and the strongest argument against.
EOF
} > CLAUDE.md
