---
type: llm
focus: trace
---

PASS if the agent invoked the hallway-test skill (a Skill tool call naming hallway-test), or if, without starting another skill, its reply offers both a hallway-test and a walkthrough and asks the person which one fits.
FAIL if it invoked the walkthrough skill without offering hallway-test, or answered from its own reading without either skill or the question.
