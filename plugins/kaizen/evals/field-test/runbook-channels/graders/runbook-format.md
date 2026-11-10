---
type: llm
focus: trace
---

Look at the runbook the agent gave, in its reply or in a file it wrote (for example under design/field-tests/).

PASS if the runbook sets the values that vary (paths, host names) as shell variables first, then gives one command per line, each with a short note of what it does, and the reply invites the person to read and adjust it before running anything.
FAIL if there is no runbook, if it is a long script or a single multi-line block to paste and run, or if commands come without saying what each does.
