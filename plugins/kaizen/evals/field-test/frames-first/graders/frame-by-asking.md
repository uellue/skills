---
type: llm
focus: last_message
---

The person wants to try their tool "tally" for real for the first time, on a shared analysis machine.

PASS if the reply asks the person about the frame of the test (at least three of: what exactly is under test, who takes part, where it runs, what they want to learn, whether it is one shot on real work or repeated from a fixed state) before giving any step-by-step commands, and does not assume that a plugin is the subject or that the state will be reset between runs.
FAIL if the reply goes straight to a list of commands or a runbook, or assumes a reset, a master copy or a plugin under test without asking.
