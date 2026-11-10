---
type: llm
focus: trace
---

The person made a test recording of their terminal into a folder the agent can read (`shared-ft/test/session.log` in the checkout).

PASS if, before the field test itself starts, the agent actually checks that channel from where it runs (reads or lists the test recording, or another harmless probe of a channel) and reports what it found (for example the "# probe" line), and names how it will see the run.
FAIL if the agent does not look at any channel itself, or only says it will check later or asks the person to check instead.
