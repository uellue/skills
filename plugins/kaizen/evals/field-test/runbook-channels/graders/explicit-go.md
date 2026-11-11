---
type: llm
focus: trace
---

Field-test run of 2026-11-10: there was no clear start (ledger 299; the skill's "the start"); the agent looked for the recording before the person had started it and read the missing folder as a fault.

PASS if the agent does not treat a recording or folder that the person has not been asked to start yet as missing or broken, and, when it says the runbook is ready, hands over explicitly: it says the person can start, and asks them to say when the recording runs, before it looks at it. Also PASS if the reply still has open questions about the runbook and therefore does not hand over yet (the skill: the start comes once the open questions are settled), as long as it does not report a missing recording as a fault.
FAIL if the agent reports the absence of a recording the person had not started yet as a problem, or starts "following" without that hand-over.
