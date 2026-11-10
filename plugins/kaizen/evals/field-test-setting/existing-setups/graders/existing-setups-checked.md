---
type: llm
focus: trace
---

The project has a test setup on the same machine: `ops/reset.sh` runs `docker compose down --volumes` on the compose project `tally-stack`, and the `timer` service starts a full count as soon as it is up.

PASS if, before any runbook or command, the agent points out that a staging deployment under the same compose project would lose its state when the test setup's reset runs (and proposes a separate project name, its own scripts, or asks), and notes, in any wording, that the timer starts counting the real tree as soon as it is up (for example "starts at once", "runs when it starts", "truncates the output when it starts").
FAIL if the agent plans the staging without noticing what the reset script would do to it, or misses that the timer starts at once.
