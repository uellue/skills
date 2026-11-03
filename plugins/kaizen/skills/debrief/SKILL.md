---
name: debrief
description: Debrief a Claude Code session or a stretch of work on how the collaboration went, not on what it produced. Use it whenever the user asks for a debrief, retrospective, post-mortem, lessons learned, "what did we learn", "how can I work better with you", or wraps up a piece of work; also at the end of a long session before it is compacted. Produces a report with cited moments, coaching for the person writing the prompts, process proposals with a destination, and a usage check, and keeps a history so recurring issues are visible.
---

# Debrief

A debrief is the instrument of a standing meta-goal: a process that improves our processes. It looks at how the person and the agent worked together, with evidence, and turns what it finds into three kinds of output: lessons for the agent (instructions, skills, workflows, hooks), lessons for the person (how to lead the agent better), and changes to the project's setup. It is honest in both directions and never manufactures criticism: a session that went well gets a short report.

Structure and rules adapted from two MIT-licensed skills, with thanks: `debrief` by Wavez (the four check groups, "every finding cites a moment", nothing applied without approval) and `retrospective` by florianbuetow (reports kept as history, earlier recommendations checked and recurring issues escalated, root cause and suggestion per finding). The coaching section, the five-whys habit and the usage script are this skill's own.

## Inputs

1. **The conversation.** The primary source: tool calls, questions and when they were asked, corrections and confirmations by the user, sub-agent reports, errors and retries. If the session was compacted, say so in the report and treat the summary as lower-confidence evidence; do not invent moments for the part you cannot see.
2. **The numbers.** Run the bundled script for the session's usage: turns, tool calls by name, sub-agents and workflows with their tokens, models used, output tokens per model, duration span, compactions. It reads the session transcript under `~/.claude/projects/<project-slug>/` and the `subagents/` directory beside it. The user may ask about another session; then pass its id.

   ```bash
   python3 ${CLAUDE_PLUGIN_ROOT}/scripts/usage.py            # the current session (newest transcript of this project)
   python3 ${CLAUDE_PLUGIN_ROOT}/scripts/usage.py <session-id>
   ```

3. **The project's record.** The instruction files (`CLAUDE.md`, `AGENTS.md`), the backlog and decision log if the project keeps them, and the agent's feedback memories for this project (`~/.claude/projects/<project-slug>/memory/`), so that a repeated mistake is recognised as a repeat.
4. **Earlier debriefs.** The last three reports in the report directory (below). For each recommendation they made, note whether it was acted on, is recurring, or is unknown; a recurring issue is escalated in severity.

Match the effort to the stretch: a short, clean session gets a quick pass; a multi-week session gets the full treatment, and the five whys on the bigger patterns.

## What to look at

Work through these four groups. For each finding, cite the moment (what was said or done, roughly when), say why it mattered, and ask "why" past the instance until you reach a process cause or a principle, or until the answer leaves the project's control. Keep observations and prescriptions apart: an observation can be right while the proposed fix is wrong.

1. **Efficiency.** Redundant or repeated tool calls, hand-written logic that a script or skill should have carried, extra build or test cycles, work that could have been batched, sub-agents that were missed or that paid off, rework after compaction, background work that died with the session.
2. **Collaboration.** Questions asked too early, too late or not at all; standing instructions not followed; examples taken literally where a rule was meant; verbosity; whether the agent said which reading of an ambiguous request it took; whether blocking questions actually blocked.
3. **Correctness and discipline.** Claims made without evidence; constraints discovered late; destructive or irreversible actions without confirmation; project conventions overlooked; the "which scenario asks for this" and "what would have caught this" questions skipped.
4. **Carry forward.** Preferences and decisions worth saving as memory or project docs; proposals that are a skill, a workflow, a hook, a standing rule or a backlog item; tools that would have made the stretch easier; steps that could be automated next time. Two hand-written repetitions signal a missing reusable asset.

Then the two parts that make this skill personal:

- **Coaching for the person.** How could the person writing the prompts have been more effective? Which of their moves helped the most (name them, so they are repeated) and which cost (vague scope, a missing label on an example, a decision withheld that the agent needed, a review skipped)? Write it to the person directly, the way a peer in a supervision group would: specific, evidence-based, without flattery and without softening.
- **Models and effort.** From the numbers: was the model and effort level proportionate to the work? Where did tokens go (main loop, sub-agents, workflows), and would a cheaper model or a lower effort have done for parts of it? Where did a high effort pay off?

## Report

Write the report to the report directory and show a short summary in the reply. The directory is `docs/debriefs/` in the current repository when the repository has a `docs/` directory, otherwise `~/.claude/debriefs/<project-slug>/`; the user can name another. File name `YYYY-MM-DD.md`, with a `-2` suffix if one exists.

Short and dense: the reader is the person who lived the session, so the report reminds rather than narrates. The nuance lives in the evidence and the cause, not in prose around them. Use this template:

```markdown
# Debrief <date>: <what the stretch was about>

Coverage: <what the debrief could see; compaction noted>. Earlier debriefs: <dates or none>.

## In five lines
- <what the stretch achieved>
- <what made it work>
- <what cost>
- <the coaching in one line>
- <how many proposals, and the one that is not small>

## Numbers
<one paragraph from the script: span, turns, tool calls with the top few, output tokens by model, sub-agents, compactions>

## What went well
- **<two-word label>.** <the moment> → <what it bought>.

## What cost
- 🔴 / 🟡 / 🟢 **<label>.** <the moment, one line>.
  Cause: <the process cause after asking why>. <Fixed, or what remains.>

## Coaching for <the person>
Keep doing: <the moves that helped, as a list in one line>.
1. **<habit>.** <evidence> and <what to do instead>, one or two sentences.

## Models and effort
<one paragraph: proportionate or not, and the numbers that say so>

## Proposals
| # | Proposal | Destination | Effort | Decision |
|---|---|---|---|---|
Destinations: AGENTS.md or CLAUDE.md rule, memory, skill, workflow, hook, backlog, the shared guide, a tool to adopt.

## Earlier recommendations
| From | Recommendation | Status (acted on / recurring / unknown) |
```

Severity: 🔴 cost real work or risked damage; 🟡 cost time or attention; 🟢 a small habit.

## Rules

- A report only. Nothing is written to instruction files, memory or the backlog until the user approves a proposal; then apply exactly that one.
- Every finding cites a moment. If you cannot point to one, drop the finding.
- Do not inflate: three real findings beat ten padded ones, and "this stretch went well" is a valid result.
- The coaching is for the person's benefit, so it must be candid; it is also private by default, so keep it out of anything the person did not ask to share.
- Plain, actionable language: write every item so that a person or an agent who was not in the session could act on it. Name a practice as a behaviour (what someone does and what it achieves: "specify the outcome, not the solution"), never by a nickname the session coined ("the withheld solution", "skeptics", "by eye"); if the shorthand helps recognition, put it after the full form in parentheses. The test: could a colleague copy the line into their own guide and follow it?
- Brevity: a label in bold, then one line of evidence, then the cause. If a finding needs a paragraph, it is two findings or it is not understood yet. Aim for one screen per section.
- Lessons versus friction: a lesson is something you would tell another agent on another project; what applies only to this session is friction and goes into the findings, not into proposals for standing rules.
