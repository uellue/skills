---
type: llm
focus: last_message
---

The person runs tally on the analysis machine over ssh from their own terminal, while the agent follows along from a VM.

PASS if the reply names how the agent will see what happens (for example a recording of the person's terminal written to a place the agent can read, log files, a forwarded port) and either checks each channel with a harmless probe from where the agent runs and reports the result, or gives the person such a probe to run first, before the field test itself starts.
FAIL if the reply assumes the agent can see the session or the files without saying how, or leaves checking the channels until the run.
