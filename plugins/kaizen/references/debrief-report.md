# Debrief report (template)

The private report in `.claude/debriefs/<date>.md`. Short and dense: the reader lived the session, so it reminds rather than narrates; the nuance lives in the evidence and the cause. Severity: 🔴 cost real work or risked damage; 🟡 cost time or attention; 🟢 a small habit. A recurring finding goes up one level.

```markdown
# Debrief <date>: <what the stretch was about>

Coverage: <sessions read, how; compaction noted; what the renderer or readers could not see>. Earlier debriefs: <dates or none>.

## In five lines
- <what the stretch achieved>
- <what made it work>
- <what cost>
- <the coaching in one line>
- <how many proposals, and the one that is not small>

## Numbers
<one paragraph from the script: span, messages, tool calls with the top few, output tokens by model counted once per message, sub-agents, compactions>

## What went well
- **<two-word label>.** <the moment> → <what it bought>.

## What cost
- 🔴 / 🟡 / 🟢 **<label>.** <the moment, one line>.
  Cause: <the process cause after asking why>. <Fixed, or what remains.>

## The plugin's skills
<used, done by hand, missed, gaps; one table or a few lines>

## The process-improvement process
<where the lessons of this stretch went, and which earlier ones were applied or violated>

## Coaching for <the person>
Keep doing: <the moves that helped, as a list in one line>.
1. **<habit>.** <evidence> and <what to do instead>, one or two sentences.

## Models and effort
<one paragraph: proportionate or not, and the numbers that say so>

## Proposals
| # | Proposal | Destination | Effort | Decision |
|---|---|---|---|---|
Destinations: an AGENTS.md or CLAUDE.md rule, a hook or lint check, memory, skill, workflow, backlog, the shared guide, a tool to adopt, the kaizen plugin.

## Earlier proposals
| From | Proposal | Status (acted on / recurring / unknown) |
```
