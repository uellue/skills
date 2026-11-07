---
type: llm
focus: trace
---

PASS if the agent invoked the walkthrough skill (a Skill tool call naming walkthrough), or if, without starting another skill, its reply offers both a walkthrough and a hallway-test and asks the person which one fits.
FAIL if it invoked the hallway-test skill without offering walkthrough, or answered from its own reading without either skill or the question.
