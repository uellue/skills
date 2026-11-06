---
name: debrief
description: Debrief a Claude Code session, a stretch of work or several sessions at once on how the collaboration went, not on what it produced. Use it whenever the user asks for a debrief, retrospective, post-mortem, lessons learned, "what did we learn", "how can I work better with you", "kaizen", or wraps up a piece of work; on a schedule, at the end of a working day or a stretch; after a skill of this plugin was used for the first time; and whenever the user says "note for the debrief" (then the note goes to the ledger at once). Produces a private report with cited moments, coaching for the person writing the prompts, process proposals with a destination, and a usage check, and keeps a ledger in the repository so recurring issues and skill friction are visible.
---

# Debrief

Text id `1f10c921`: first run `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/version.py debrief 1f10c921` as it stands and pass on what it prints, if anything (it is silent when all is well; if it fails, carry on).

A debrief is the instrument of a standing meta-goal: a process that improves our processes. It looks at how the person and the agent worked together, with evidence, and turns what it finds into three kinds of output: lessons for the agent (instructions, skills, workflows, hooks), lessons for the person (how to lead the agent better), and changes to the project's setup. It is honest in both directions and never manufactures criticism: a session that went well gets a short report.

Structure and rules adapted from two MIT-licensed skills, with thanks: `debrief` by Wavez (the four check groups, "every finding cites a moment", nothing applied without approval) and `retrospective` by florianbuetow (reports kept as history, earlier recommendations checked and recurring issues escalated, root cause and suggestion per finding). The coaching section, the five-whys habit, the usage script and the ledger are this skill's own.

## When

Ends do not announce themselves (a compaction, a reboot, a refused turn), so the debrief runs on a schedule the person chooses (the end of a day, the end of a stretch, after the first use of a new skill), not "before the end". Several first uses in one session make one debrief, not one each. Three cheap habits feed it between runs; the first capture into a new ledger first says where it goes:

- **"Note for the debrief."** When the person or the agent says it, write the note into the ledger's notes section at once, with the moment, and carry on. Sorting is the debrief's job; capture must cost nothing.
- **Skill friction.** At the end of every run of a skill of this plugin, one line into the ledger: what in the skill did not fit the situation.
- **Offered, not decided.** When the agent offers steps and the person neither picks nor drops them, the open offer goes into the ledger's notes before the topic changes; the debrief asks whether it was dropped on purpose.

## Inputs

1. **The transcripts.** The primary source. Find them with the bundled script, which also looks where worktrees, VMs and checkouts keep them.

   ```bash
   python3 ${CLAUDE_PLUGIN_ROOT}/scripts/transcript.py locate            # every session of this project: span, size, first message
   python3 ${CLAUDE_PLUGIN_ROOT}/scripts/transcript.py render <id>       # readable text with L<n> markers, for reading in slices
   python3 ${CLAUDE_PLUGIN_ROOT}/scripts/transcript.py export <id>       # copy a session into <repo>/.claude/transcripts/<id>/ (refused unless git ignores it)
   ```

   **Which sessions.** When the person names none:
   - In a fresh session (the newest session's first message is this debrief's own invocation), never take that session. Propose the sessions since the last debrief in the ledger (no ledger yet: those of the last seven days), each with its date, size and first message; say which you will take and wait for a yes.
   - In the session that did the work (wrapping up, or after a skill's first use), the stretch is this session so far; say so, and offer a fresh session for a less anchored read.

   Before reading more than one session, state the sessions, their sizes, the readers' model and the token estimate (see "Several sessions at once"), and wait; for one session, state its size and go on.

   Read the rendering, not the raw JSONL: grepping one's own transcript for patterns has ended sessions. If the session was compacted, say so in the report and treat the summary as lower-confidence evidence; do not invent moments for the part you cannot see. Messages the person queued while a turn ran appear as "USER (queued mid-turn)"; they are easy to miss in the raw file and often carry decisions. Text the harness put in the person's place (skill texts, sub-agent reports, notifications, command output) is labelled HARNESS: it is not the person's, and never evidence for coaching.
2. **The numbers.** The usage script: user messages, API messages, tool calls by name, output and input tokens per model counted once per API message, sub-agents with their tokens, span, compactions.

   ```bash
   python3 ${CLAUDE_PLUGIN_ROOT}/scripts/usage.py <id>       # each chosen session; without an id, the newest (often the one you run in)
   python3 ${CLAUDE_PLUGIN_ROOT}/scripts/usage.py agent-<id>    # a sub-agent
   ```
3. **The project's record.** The instruction files (`CLAUDE.md`, `AGENTS.md`), the backlog and decision log if the project keeps them, the stakeholder and requirements records in `design/`, and the agent's feedback memories for this project (`~/.claude/projects/<slug>/memory/`), so that a repeated mistake is recognised as a repeat. Memory is per checkout path: say in the report which memory the session actually had, because a worktree or a VM often had none.
4. **The ledger and earlier reports.** `design/kaizen.md` (below) and the last three reports in `.claude/debriefs/`. For each earlier proposal, note whether it was acted on, is recurring, or is unknown; a recurring issue is escalated in severity. Adoption is not habit: a proposal marked done last time can still recur, and the finding then is that the destination was a sentence where a check (a hook, a lint rule, a template field) was possible.

Match the effort to the stretch: a short, clean session gets a quick pass; a multi-week session gets the full treatment, and the five whys on the bigger patterns.

**Several sessions at once.** When the debrief covers more than one session (a week, three repositories, the first uses of a skill), render each session and give one reader agent per session the brief in `${CLAUDE_PLUGIN_ROOT}/references/reader-brief.md`, with the session's paths and numbers filled in; the readers report with cited moments, and the main session synthesises. Verify yourself any claim a reader makes about an instrument (a script, a count, a skill's text) before it goes into the report; a reader's claim is a lead, not a finding. Budget about 200 k tokens per reader for a day-long session, and set each reader's model explicitly, because sub-agents otherwise inherit the main loop's model: a model below the top one is enough for reading and citing (Opus, as of the model line-up checked 2026-11-05); use the top model only when the person asks for it.

## What to look at

Work through these four groups. For each finding, cite the moment (what was said or done, roughly when), say why it mattered, and ask "why" past the instance until you reach a process cause or a principle, or until the answer leaves the project's control. Keep observations and prescriptions apart: an observation can be right while the proposed fix is wrong.

1. **Efficiency.** Redundant or repeated tool calls, hand-written logic that a script or skill should have carried, extra build or test cycles, work that could have been batched, sub-agents that were missed or that paid off, rework after compaction, background work that died with the session, questions that blocked while the person was away.
2. **Collaboration.** Questions asked too early, too late or not at all; standing instructions not followed; examples taken literally where a rule was meant; verbosity; whether the agent said which reading of an ambiguous request it took; whether blocking questions actually blocked; decisions the person withheld and what they cost; constraints that arrived after the work; a real stakeholder present and unused.
3. **Correctness and discipline.**
   - Claims without evidence; constraints discovered late; destructive or irreversible actions without confirmation; project conventions overlooked.
   - "Clean" reported from a different command than the commit or CI runs; a change beyond a few hundred lines without an independent reader.
   - A vulnerability found and not put first.
   - Documents handed over with stale markers or unverified quotes.
   - A change merged or archived without a hallway test; tests and scenarios that cite no example ID; decisions an implementer invented because no decision record existed.
   - The questions "which scenario asks for this" and "what would have caught this" skipped.
4. **Carry forward.** Preferences and decisions worth saving as memory or project docs; proposals that are a skill, a workflow, a hook, a standing rule or a backlog item; tools that would have made the stretch easier; steps that could be automated next time; instruments built by hand (an eval, a brief, a probe) that should be kept. Two hand-written repetitions signal a missing reusable asset.

Then the two parts that make this skill personal:

- **Coaching for the person.** How could the person writing the prompts have been more effective? Which of their moves helped the most (name them, so they are repeated) and which cost (vague scope, a missing label on an example, a decision withheld that the agent needed, a review skipped, a slash command typed inside a message that never ran)? Write it to the person directly, the way a peer in a supervision group would: specific, evidence-based, without flattery and without softening.
- **Models and effort.** From the numbers: was the model and effort level proportionate to the work? Where did tokens go (main loop, sub-agents, workflows, context), and would a cheaper model or a lower effort have done for parts of it? Where did a high effort pay off? Check that the model the person asked for is the one in the transcript.

Matt Pocock's `retro` covers the agent's environment (checks, navigation, steering files, tool economy); cite its findings, and add the collaboration, the coaching and the history. Only the person can invoke it, as a message of its own (a slash command inside another command's arguments never runs); otherwise give its `SKILL.md` and the rendered transcript to an independent sub-agent that has not seen your findings. Compare the two reads: agreement strengthens a finding; say what each missed.

And, for this plugin's own improvement (kaizen on kaizen): which of its skills were used, how they ran, where one would have helped and was not used, and what no skill covers. Look for missed skills from the tools the playbook pairs with it too (OpenSpec, Matt Pocock's skills), installed or not: name one only where it would have changed a cited moment, and say what installing it would take. Those findings become proposals with the destination "kaizen plugin". In the plugin's own repository they become issues or merge requests with the maintainer's say. In anyone else's project nothing is sent on their behalf, since their ledger may be private: suggest politely that, if they would like to help improve the plugin, they open an issue at github.com/uellue/skills with a text you draft for them to copy, or send it to the maintainer privately.

## Output

Two documents, in the repository that was debriefed:

- **The report**, private: `.claude/debriefs/YYYY-MM-DD.md` (with a `-2` suffix if one exists). It is a subjective snapshot with the coaching in it, so it stays out of version control: before writing anything, run `git -C "$(git rev-parse --show-toplevel)" check-ignore -q .claude/debriefs/x.md` (exit 0: ignored; outside a git repository, ask where to write); if git would track it, offer the line `/.claude/debriefs/` for `.gitignore` (or `.git/info/exclude`, which is not shared) and write nothing until the person agrees. The user can name another place.
- **The ledger**, in the repository: `design/kaizen.md` (create `design/` if the project has none, after telling the person where the ledger goes and that it is meant to be committed). If the repository is public or may become so, the ledger carries no details of other projects (those go to their own backlogs; the ledger says "transferred") and no security findings, secrets or credentials, not even as to-dos. Generalising an entry later does not remove it from git history: if one slipped in, say so before the branch is pushed, so the person can decide whether to rewrite the unpushed history. Only what is actionable leaves the session: the proposals table with their destinations and decisions, the status of earlier recommendations, the skill-friction lines, and the unsorted notes for the next debrief. Create it from `${CLAUDE_PLUGIN_ROOT}/references/ledger.md` if no skill has yet; on later ones, append the proposals under the date and update the statuses.

Show a short summary in the reply: the five lines and the proposals that are not small.

The report is short and dense: the reader is the person who lived the session, so it reminds rather than narrates. The nuance lives in the evidence and the cause, not in prose around them. Template:

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
Destinations: AGENTS.md or CLAUDE.md rule, a hook or lint check, memory, skill, workflow, backlog, the shared guide, a tool to adopt, the kaizen plugin (as above: an issue the person opens, or a private message to the maintainer).

## Earlier recommendations
| From | Recommendation | Status (acted on / recurring / unknown) |
```

Ledger template: `${CLAUDE_PLUGIN_ROOT}/references/ledger.md`.

Severity: 🔴 cost real work or risked damage; 🟡 cost time or attention; 🟢 a small habit. A recurring finding goes up one level.

## Rules

- A report and a ledger entry only. Nothing is written to instruction files, memory, hooks or the backlog until the user approves a proposal; then apply exactly that one and record the decision in the ledger.
- Every finding cites a moment. If you cannot point to one, drop the finding.
- Do not inflate: three real findings beat ten padded ones, and "this stretch went well" is a valid result.
- The coaching is for the person's benefit, so it must be candid; it is also private by default, so keep it out of anything the person did not ask to share, and never put it in the ledger.
- Plain, actionable language: write every item so that a person or an agent who was not in the session could act on it. Name a practice as a behaviour (what someone does and what it achieves: "specify the outcome, not the solution"), never by a nickname the session coined; if the shorthand helps recognition, put it after the full form in parentheses. The test: could a colleague copy the line into their own guide and follow it?
- Brevity: a label in bold, then one line of evidence, then the cause. If a finding needs a paragraph, it is two findings or it is not understood yet. Aim for one screen per section.
- Lessons versus friction: a lesson is something you would tell another agent on another project; what applies only to this session is friction and goes into the findings, not into proposals for standing rules.
- Prefer a check to a sentence: when a proposal can be a hook, a lint rule, a template field or a script, that is its destination; a rule in an instruction file is the fallback.
