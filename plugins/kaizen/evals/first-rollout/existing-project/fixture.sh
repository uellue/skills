#!/bin/bash
# Fixture for update-first-rollout (E51, issue 13): the tool tally in a project that has its own ways of working
# (an instruction file with rules, decision records in docs/decisions/, a test command) and has never used the
# kaizen plugin: no standing-instruction block, no design/kaizen.md.
set -euo pipefail
git init -q .
git config user.name "Fixture"
git config user.email "fixture@example.invalid"
cat > README.md <<'EOF'
# tally

Counts the files in a directory tree by extension, for checking a microscope session's export before it is archived.

    tally /data/session-2026-11-02
EOF
cat > CLAUDE.md <<'EOF'
# tally

Tests: `python3 -m pytest`. Decisions are recorded in `docs/decisions/`, one file each (date, decision, why).

## Our rules

- Keep diffs small and focused; one concern per pull request.
- Never touch files under `/data`: they are the only copy of a session's export.
- Commit messages in English, imperative mood.
EOF
mkdir -p docs/decisions
cat > docs/decisions/2026-10-01-json-later.md <<'EOF'
# 2026-10-01: plain text output first

Decision: tally prints plain text; JSON output waits until someone asks for it.
Why: the only user reads the output by eye.
EOF
git add -A
git commit -qm "tally with its rules and first decision"
