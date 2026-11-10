---
type: llm
focus: last_message
---

Field-test run of 2026-11-10: the question whether to try the tool once on real work or repeatedly from a reset state reached the person as a label ("One shot or repeatable"), which they called jargon.

PASS if the reply, where it asks whether the test is done once or repeated, asks in plain words a person understands without the plugin's vocabulary (for example "try it once as part of your real work, keeping everything, or run it several times from the same starting point, reset in between?"), or does not ask it yet.
FAIL if it asks with a label such as "one shot or repeatable", "one shot on real work or repeated from a fixed state", "variant 1 or 2", without saying in plain words what each means.
