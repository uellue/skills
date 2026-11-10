---
type: llm
focus: trace
---

Field-test run of 2026-11-10: the channel probe was asked for only in the chat, not in the runbook, so the person, following the runbook, never did it.

PASS if, when the agent writes a runbook (in its reply or a file), every step it asks the person to do (in particular the check that the agent can see the recording, the "probe") is a step of that runbook, and the reply refers to the runbook's steps rather than adding steps outside it. Also PASS if no runbook is written yet.
FAIL if the reply asks the person to do something for the test (a probe, a check, a command) that the runbook it wrote does not contain.
