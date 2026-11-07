---
type: llm
focus: trace
---

PASS if the agent invoked the debrief skill (a Skill tool call naming debrief), or if its reply proposes a debrief (a retrospective on how the work went) of the work just merged, alone or among other next steps.
FAIL if it moves on to the next piece of work, or lists next steps, without offering a debrief.
