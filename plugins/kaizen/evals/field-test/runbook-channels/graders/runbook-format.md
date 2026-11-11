---
type: llm
focus: last_message
---

Look at the runbook the agent gave, in its reply or in a file it wrote (for example under design/field-tests/).

PASS if the runbook is written in fenced code blocks (not a Markdown table), sets the values that vary (paths, host names) as shell variables first, then gives one command per line, each with a short `#` comment or note of what it does, and the reply invites the person to read and adjust it before running anything.
FAIL if there is no runbook, if its commands sit in a table, if it is one long script or a multi-line block to paste and run without notes, or if commands come without saying what each does. (Field-test run of 2026-11-10: a runbook as a table was unreadable as raw text and could not be copied out as a script.)
