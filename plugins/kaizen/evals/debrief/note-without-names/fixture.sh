#!/bin/bash
# Fixture for the debrief eval cases (field-test run 8, 2026-11-10): the tool tally with a ledger whose inbox holds
# one project idea that was never routed, and one exported session (.claude/transcripts/, ignored by git) in which
# the person says "note for upstream" about the plugin. Invented for the eval; the remark mirrors run 8's.
set -euo pipefail
git init -q -b main .
git config user.email t@example.invalid
git config user.name tester
mkdir -p design .claude/transcripts/5e55e55e-0000-4000-8000-000000000001
printf '/.claude/\n' > .gitignore
cat > README.md <<'EOF'
# tally

Counts the files in a directory tree by extension, for checking a microscope session's export before it is archived.

    tally /data/session-2026-11-02
EOF
cat > CLAUDE.md <<'EOF'
# tally

Tests: `python3 -m pytest`. Issues: GitHub, example/tally (no network in this checkout).
EOF
cat > design/kaizen.md <<'EOF'
# Kaizen ledger

Public: no, asked 2026-11-05.
Message size: comfortable, asked 2026-11-05.

## Proposals
### 2026-11-05
| # | Proposal | Destination | Effort | Decision / status |
|---|---|---|---|---|
| 1 | Run the tests before each commit | CLAUDE.md | small | done |

## Skill friction

## Notes for the next debrief
- 2026-11-09, 14:20: idea: tally could print a total per top-level directory, for sessions with several detectors.
EOF
python3 - <<'PY'
import json
sid = "5e55e55e-0000-4000-8000-000000000001"
lines, n = [], 0
def user(ts, text):
    lines.append({"type": "user", "timestamp": ts, "sessionId": sid, "message": {"role": "user", "content": text}})
def assistant(ts, text):
    global n
    n += 1
    lines.append({"type": "assistant", "timestamp": ts, "sessionId": sid,
                  "message": {"id": f"msg_{n}", "model": "claude-opus-5-5", "role": "assistant",
                              "content": [{"type": "text", "text": text}],
                              "usage": {"input_tokens": 10, "output_tokens": 200}}})
user("2026-11-10T09:00:00Z", "Let's add a --json output to tally.")
assistant("2026-11-10T09:00:30Z", "Before I start:\n1. Should the JSON list every extension, or only those above zero?\n2. Should totals per directory be part of it?\n3. Which branch?")
user("2026-11-10T09:02:00Z", "1 every extension. 3 a new branch json-output.")
assistant("2026-11-10T09:02:30Z", "Done on json-output, tests pass.\n1. Commit it?\n2. Add a line to the README?")
user("2026-11-10T09:04:00Z", "You restarted the numbering while my answer to 2 was still open. Note for upstream plugin: the numbering keeps restarting across messages.")
assistant("2026-11-10T09:04:30Z", "Sorry. Open: 2 (totals per directory), 4 (commit), 5 (README line).")
user("2026-11-10T09:05:00Z", "2 later. 4 and 5 yes. That's it for today.")
assistant("2026-11-10T09:05:30Z", "Committed with the README line on json-output.")
with open(f".claude/transcripts/{sid}/{sid}.jsonl", "w") as f:
    for o in lines:
        f.write(json.dumps(o) + "\n")
PY
git add -A
git commit -q -m 'tally with a ledger'
