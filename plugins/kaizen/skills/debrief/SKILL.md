---
name: debrief
description: Debrief a Claude Code session, a stretch of work or several sessions at once on how the collaboration went, not on what it produced. Use it whenever the user asks for a debrief, retrospective, post-mortem, lessons learned, "what did we learn", "how can I work better with you", "kaizen", or wraps up a piece of work; after a merge or a release; on a schedule, at the end of a day or a stretch; after a skill of this plugin was used for the first time; and whenever the user says "note for the debrief" (then the note goes to the ledger at once). Produces a private report with cited moments, coaching for the person writing the prompts, process proposals with a destination, and a usage check, and keeps a ledger in the repository so recurring issues and skill friction are visible.
---

# Debrief

Text id `021e6c22`: first run `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/version.py debrief 021e6c22` as it stands and pass on what it prints, if anything (it is silent when all is well; if it fails, carry on).

A debrief is the instrument of a standing meta-goal: a process that improves our processes. It looks at how the person and the agent worked together, with evidence, and turns what it finds into lessons for the agent (instructions, skills, workflows, hooks), lessons for the person (how to lead the agent better) and changes to the project's setup. (Structure adapted, with thanks, from two MIT-licensed skills, `debrief` by Wavez and `retrospective` by florianbuetow; the coaching, the five whys, the usage script and the ledger are this skill's own.)

Use plain words with the person: explain a term of this plugin the first time you use it with them, as `${CLAUDE_PLUGIN_ROOT}/references/words.md` does; keep a message to about fifteen lines, one step or question at a time; number a message's items from 1 in one sequence that never restarts within it, so the person can answer by number.

## When

Ends do not announce themselves (a compaction, a reboot), so the debrief runs on a schedule the person chooses (a day, a stretch, a new skill's first use), not "before the end". A release is debriefed after its push and merge, not before: its proposals go into the next release, so the work ships. Several first uses in one session make one debrief. Three cheap habits feed it between runs; the first capture into a new ledger first says where it goes:

- **"Note for the debrief."** When the person or the agent says it, write the note into the ledger's notes section at once, with the moment, and carry on. Sorting is the debrief's job; capture must cost nothing. Once per stretch, while a run of several minutes goes on (the final acceptance tests, a reviewer, the debrief's own readers), invite the person to note thoughts; not for a short wait, not again after a no, not without a person.
- **Skill friction.** At the end of every run of a skill of this plugin, one line into the ledger: what in the skill did not fit the situation.
- **Offered, not decided.** An offer the person neither took nor dropped goes into the ledger's notes before the topic changes; the debrief asks whether it was dropped on purpose.

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

   Before reading several sessions, state them, their sizes, the readers' model and the cost, and wait; for one session, state the cost and go on. The cost in minutes first, a guess called one, tokens in brackets.

   Read the rendering, not the raw JSONL: grepping one's own transcript for patterns has ended sessions. If the session was compacted, say so; the rendering usually still shows the earlier part, so read it there, and use the summary as lower-confidence evidence only where that part is missing; never invent moments. Messages the person queued while a turn ran appear as "USER (queued mid-turn)" and often carry decisions. Text the harness put in the person's place (skill texts, sub-agent reports, notifications, command output) is labelled HARNESS: it is not the person's, and never evidence for coaching.
2. **The numbers.** The usage script: messages, tool calls by name, tokens per model, sub-agents, span, compactions.

   ```bash
   python3 ${CLAUDE_PLUGIN_ROOT}/scripts/usage.py <id>       # each chosen session; without an id, the newest (often the one you run in)
   python3 ${CLAUDE_PLUGIN_ROOT}/scripts/usage.py agent-<id>    # a sub-agent
   ```
3. **The project's record.** The instruction files (`CLAUDE.md`, `AGENTS.md`), the backlog and decision log if the project keeps them, the stakeholder and requirements records in `design/`, and the agent's feedback memories for this project (`~/.claude/projects/<slug>/memory/`), so that a repeated mistake is recognised as a repeat. Say which memory the session had: it is per checkout path, and a worktree or a VM often has none.
4. **The ledger and earlier reports.** `design/kaizen.md` (below) and the last three reports in `.claude/debriefs/`. For each earlier proposal, note whether it was acted on, is recurring, or is unknown; a recurring issue is escalated in severity. Adoption is not habit: a proposal marked done last time can still recur, and the finding then is that the destination was a sentence where a check (a hook, a lint rule, a template field) was possible.
5. **The person.** Before writing findings, ask in one message what went well for them, where they felt friction, and where the agent seemed to lose track (of the scope, a decision, which level is under test when a tool tests itself), citing a moment you suspect; where they already said it, quote them and ask only what to add. The agent is often blind to its own confusion; the answers are evidence, marked as theirs. If they are away, the questions end the report. Note their remarks with an emotional lean, positive or negative: they become feedback entries (Output). Ask too whether the messages' length suited them, and offer longer or shorter: always in the first debrief; later when they asked for an adjustment since, or when the ledger's `Message size:` line is more than three days old; note the answer there.

Match the effort to the stretch: a quick pass for a short, clean session; the full treatment and the five whys for a long one.

**Several sessions at once.** For more than one session (a week, three repositories), give one reader agent per rendered session the brief in `${CLAUDE_PLUGIN_ROOT}/references/reader-brief.md`, filled in; the readers report with cited moments, and the main session synthesises. A reader's claim about an instrument (a script, a count, a skill's text) is a lead: verify it before it goes into the report. Budget about 200 k tokens per reader for a day-long session and set each reader's model explicitly (sub-agents inherit the main loop's); a model below the top one is enough (Opus, checked 2026-11-05).

## What to look at

Work through these five groups. For each finding, cite the moment (what was said or done, roughly when), say why it mattered, and ask "why" past the instance until you reach a process cause or a principle, or until the answer leaves the project's control. Keep observations and prescriptions apart: an observation can be right while the proposed fix is wrong.

1. **Efficiency.** Redundant or repeated tool calls, hand-written logic that a script or skill should have carried, extra build or test cycles, sub-agents that were missed or that paid off, rework after compaction, background work that died with the session.
2. **Collaboration.** Questions asked too early, too late or not at all; standing instructions not followed; examples taken literally where a rule was meant; verbosity; whether blocking questions actually blocked; decisions the person withheld and what they cost; constraints that arrived after the work; a real stakeholder present and unused.
3. **Correctness and discipline.**
   - Claims without evidence; constraints discovered late; destructive or irreversible actions without confirmation; project conventions overlooked.
   - "Clean" reported from a different command than the commit or CI runs; a change beyond a few hundred lines without an independent reader.
   - A vulnerability found and not put first.
   - Documents handed over with stale markers or unverified quotes.
   - A change merged or archived without a hallway test; tests and OpenSpec scenarios that cite no example ID; decisions an implementer invented because no decision record existed.
   - The questions "which scenario asks for this" and "what would have caught this" skipped.
4. **Carry forward.** Preferences and decisions worth saving as memory or project docs; proposals that are a skill, a workflow, a hook, a standing rule or a backlog item; tools or automation that would have made the stretch easier; instruments built by hand (an eval, a brief, a probe) that should be kept. Two hand-written repetitions signal a missing reusable asset.
5. **Language**, always, in the chat and in the work: a term used in two senses, a request read two ways and whether the agent said which reading it took, a word the project's glossary avoids, one concept named differently in code and documents. Settle each with the person, with Matt Pocock's `domain-modeling` where installed (it keeps `GLOSSARY.md`), otherwise by agreeing the term and recording it where the project keeps its vocabulary.

Then the two parts that make this skill personal:

- **Coaching for the person.** Which of their moves helped the most (name them, so they are repeated) and which cost (vague scope, muddy words, an unlabelled example, a decision withheld, a review skipped)? Write it to the person directly, the way a peer in a supervision group would: specific, evidence-based, without flattery and without softening. Every item cites a moment, as a finding does, and fits it (no "say so at once" where they did). When a cause lies in a skill, the finding goes to the skill, not into the coaching.
- **Models and effort.** From the numbers: was the model and effort level proportionate to the work? Where did tokens go (main loop, sub-agents, workflows, context), and would a cheaper model or a lower effort have done for parts of it? Where did a high effort pay off? Check that the model the person asked for is the one in the transcript.

Matt Pocock's `retro` covers the agent's environment. Only the person can invoke it; otherwise give its `SKILL.md` and the rendered transcript to an independent sub-agent that has not seen your findings. Compare the two reads: agreement strengthens a finding; say what each missed.

And, for this plugin's own improvement (kaizen on kaizen): which of its skills were used, how they ran, where one would have helped and was not used, and what no skill covers. Look for missed skills from the tools the playbook pairs with it too (OpenSpec, Matt Pocock's skills), installed or not: name one only where it would have changed a cited moment, and say what installing it would take. In the plugin's own repository they become proposals with the maintainer's say; elsewhere nothing is sent on anyone's behalf, but offer a drafted issue for github.com/uellue/skills or a private message to the maintainer, with the feedback entries about the plugin on the person's yes.

## Output

Three documents, in the repository that was debriefed; when the default branch is checked out, the committed ones go on a working branch, which needs its own merge request unless the person carries them into the next one:

- **The report**, private: `.claude/debriefs/YYYY-MM-DD.md` (with a `-2` suffix if one exists), from the template in `${CLAUDE_PLUGIN_ROOT}/references/debrief-report.md`, read before writing. It is a subjective snapshot with the coaching in it, so it stays out of version control: before writing anything, run `git -C "$(git rev-parse --show-toplevel)" check-ignore -q .claude/debriefs/x.md` (exit 0: ignored; outside a git repository, ask where to write); if git would track it, offer the line `/.claude/debriefs/` for `.git/info/exclude`, which protects every branch at once (`.gitignore` on a working branch leaves `main` open until the merge; offer both), and write nothing until the person agrees. The user can name another place.
- **The ledger**: `design/kaizen.md`, or where the playbook's step 3 placed `design/`; say where and whether it is committed before creating it. Unless its header says, ask once whether the repository is public or may become so, and note the answer there. If so, the ledger carries no details of other projects (they go to their own backlogs; the ledger says "transferred") and no security findings, secrets or credentials, not even as to-dos. If one slipped in, say so before the push: git history keeps it. Only what is actionable leaves the session. Start it from `${CLAUDE_PLUGIN_ROOT}/references/ledger.md`; later, append the proposals under the date and update the statuses.
- **The feedback entries**: the remarks noted at input 5, verbatim with their source in `.claude/debriefs/feedback-raw.md` (private), cleaned in `design/feedback.md` (no ids, names or private projects; a paraphrase offered where they might not want the original public), from `${CLAUDE_PLUGIN_ROOT}/references/feedback.md`; announced like the ledger. A decision ("yes to all") is not a feedback entry.

Reply in two messages: first the five lines and where the person's remarks went (what they said, what it became); then the coaching in full (the person may not be able to open the report), the proposals that are not small, and the branch with its merge request.

## Rules

- A report and a ledger entry only. Nothing is written to instruction files, memory, hooks or the backlog until the user approves a proposal; then apply exactly that one and record the decision in the ledger.
- Every finding cites a moment. If you cannot point to one, drop the finding.
- Do not inflate: three real findings beat ten padded ones, and "this stretch went well" is a valid result.
- The coaching is for the person's benefit, so it must be candid; it is also private by default, so keep it out of anything the person did not ask to share, and never put it in the ledger.
- Plain, actionable language: write every item so that a person or an agent who was not in the session could act on it. Name a practice as a behaviour ("specify the outcome, not the solution"), never by a nickname the session coined; a helpful shorthand goes after the full form, in parentheses. The test: could a colleague copy the line into their own guide and follow it?
- Brevity: a label in bold, then one line of evidence, then the cause. If a finding needs a paragraph, it is two findings or it is not understood yet. Aim for one screen per section.
- Lessons versus friction: a lesson is something you would tell another agent on another project; what applies only to this session is friction and goes into the findings, not into proposals for standing rules.
- Prefer a check to a sentence: when a proposal can be a hook, a lint rule, a template field or a script, that is its destination; a rule in an instruction file is the fallback.
