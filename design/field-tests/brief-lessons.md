# Writing a brief for a person in a field test: worked examples

From the principal's edits of `devvm-brief.md`, 2026-11-09 (commits `18e81bf` to `bdaa59e`), for the field-test skill (ledger 283). The rule they show, in the principal's words: don't inject disturbances into the test case; counter what might be a disturbance caused by the person knowing it is a test, running it with instrumentation and so on. Better than asking someone to take a role is finding someone who has it naturally. The most valuable information comes when real people follow their nose and go off script; specific scripts and scenarios are for the automated hallway tests.

So a brief gives the starting point and the method (how to record, how to note, what must not leave the machine, how to hand back), and nothing about how to behave, what to try, or how to answer.

## The edits

| Before (the agent's draft) | After (the principal) | Why |
|---|---|---|
| Three numbered steps: start with any skill or `/kaizen:update` and "follow it"; then `/kaizen:sync`; then work on the open issues "with the plugin guiding you" | "type `/kaizen:update`. From there on, work as you normally would." | The rest must flow from the plugin; a script of steps tests the script, not the plugin |
| "You decide everything the plugin asks; answer as yourself." | (removed) | People come with their own persona and agenda; telling them how to answer is a personality change |
| "Do not look up how the plugin works; if you would have to, that is a finding." | (removed) | An instruction about behaviour, injected by the test; a person who looks something up is data |
| Notes: "one line to the notes file … outside devvm" | Three ways, whichever is at hand: a `#` comment at a shell prompt (it lands in the recording), the notes file from a second terminal or the editor, or the plugin's own features ("note for the debrief", `/kaizen:debrief`) | Counters the instrumentation: noting must cost nothing and use what the person would use anyway; the plugin's own notes are feedback too |
| "Notes about devvm itself go wherever the plugin tells you, as usual." | "Notes about devvm itself go wherever you see fit. Please follow your normal procedures there." | The plugin may guide, but the person decides; no role word ("as the manager") either: it reads as a job title to a colleague, and "maintainer" belongs to the outer role |
| "Tell the plugin you are done, and let it hand over as it would." | "Wind the session down as you normally would." | How a session ends is the person's habit, and the plugin's hand-over is under test, not to be prompted |

Added on the principal's suggestion (same day), both countering the setting rather than steering the person:

| Added | Why |
|---|---|
| "Also note what you do that the recording does not see, such as reading the README in a browser, asking a colleague, or looking something up elsewhere." | The instruments have gaps; a note closes them without changing what the person does |
| "Be frank: the raw reaction is what helps, swearing and sighs included; nothing you write here is held against anyone." | People who know they are tested tend to be polite; the raw information and the emotional cues are what the debrief needs (feedback entries keep the words verbatim and private) |

## What stays in a brief

- The start: one command or one situation.
- The method: the recording (started for them, see `record.sh`), the ways to note, the hand-back.
- What must not leave the machine in a churn run (nothing upstream), as a rule of the setting, not as a script for reacting to the plugin.
- The closing question: did we do OK, was anything uncomfortable or unclear.
