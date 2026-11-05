# skills

A place to keep and share my AI agent skills, as a Claude Code plugin marketplace.

## Install

```bash
claude plugin marketplace add uellue/skills
claude plugin install kaizen@uellue --scope user
```

Or inside a session: `/plugin marketplace add uellue/skills`, then `/plugin install kaizen@uellue`.
To follow updates, turn on auto-update for the `uellue` marketplace under `/plugin` → Marketplaces.

## Plugins

- **kaizen**: continuous improvement of how we work with agents (Toyota's word for improving the processes themselves). Five skills along the life of a project, sharing a few documents in the project's `design/` directory (`stakeholders.md`, `requirements.md`, `walkthroughs/`, `kaizen.md`):
  - `/kaizen:playbook`: which moment a session is in and which skill fits: stakeholders, requirements, walk-throughs, the project's own specification method, build, hallway test, debrief; which shared documents are missing and which skill writes them.
  - `/kaizen:requirements`: interview the person who needs a solution, a few sections at a time, and write a demand and requirements specification in the structure of ER-C's form, every item marked answered, record, assumed, unknown or deferred; reconstruct the requirements of a tool that grew from playing around, from its history and transcripts; check an existing document for what it skips; need before solution, numbers as numbers, prior art before "nothing exists"; a handover check that lists everything still unconfirmed. Section 1.4 writes the project's stakeholder record.
  - `/kaizen:walkthrough`: put on the shoes of a stakeholder from the record (never an assumed one) and walk through a process step by step, against the running system where there is one, to find the questions, gaps and acceptance examples nobody wrote down; a measured walk hands the process to a fresh agent under injected faults. Bundles a requirements questionnaire adapted from ER-C's demand and requirements form; the two-hat interview and the "simulated stakeholders are lower confidence" rule are borrowed from Feature Forge (jeffallan) and melodic-software's requirements-elicitation skills.
  - `/kaizen:hallway-test`: a fresh sub-agent that sees only the requirements and the user documentation builds test cases, writes its expectations to a file before running, asks questions and reports bugs, surprises and gaps; by eye too, through a bundled xterm screenshot driver (needs xvfb, xterm, xdotool, imagemagick); as a diagnosis under injected faults; on a README or an agent instruction file as an evaluation with a pre-written key and a blind grader. The CLI usability checklist is adapted from the MIT-licensed cli-ux-tester skill by Alister Lewis-Bowen.
  - `/kaizen:debrief`: debrief a session, a stretch of work or several sessions at once on how the collaboration went, not on what it produced: cited moments, coaching for the person writing the prompts, proposals with a destination, a usage check with tokens counted once per API message, and the plugin's own skills checked for where they were used and where they would have helped. The report is private (`.claude/debriefs/`); only what is actionable goes into the repository's ledger (`design/kaizen.md`). Scripts: `transcript.py` (locate, render, export sessions wherever the harness or a checkout keeps them) and `usage.py`. Structure adapted, with thanks, from the MIT-licensed `debrief` skill by Wavez and the `retrospective` plugin by florianbuetow.

The plugin's own stakeholders, requirements, testing plan and kaizen ledger are in `design/`.

## Working with agents: lessons learned

Collected from debriefs of real sessions (a crawler, a dev-VM tool, a Nextcloud upgrade, autumn 2026). The skills above codify most of the process; this section keeps what does not map to a skill yet. Written for colleagues at ER-C starting with Claude Code or Codex; each item is a behaviour, with the reason.

**The picture.** Starting an agent session is onboarding a new employee: it knows nothing but the repository and its instructions. Everything that keeps a human organisation coherent works for agents for the same reasons: a written record of decisions, a backlog, conventions, a reviewer who did not write the code, a retrospective.

**Leading the agent**

- State principles once and trust them: "keep changes tight, no speculative generality", "follow established formats and tools, invent only with a reason", "earlier notes are options, not requirements". They shape hundreds of small decisions you never see.
- Specify the outcome, not the solution. "I want to see the diagnostics next to each entry when I pipe into `less`" produced a better answer than dictating one would have, and tested whether the requirement was clear.
- Put outcome, boundary, model and effort in one message: what should work at the end, where the work may happen, which model at which effort. Send slash commands (`/model`, `/effort`) on their own line and read the model line back; typed inside a message they do nothing.
- Ask for options with counter-arguments, not for decisions; then decide with numbered replies and a priority ("go with your leans; most important is a break-through, details later"). One such message unblocks a whole afternoon.
- Label examples. A case named without "this is an example of ..." is sometimes taken literally and becomes a special case. Generalise your own corrections the same way.
- Ask the behaviour question, once and early: "Is the test checking the right outcome for the user?", "What changes for the user?" One such question has exposed a systemic flaw that a review would have missed.
- Order work by what validates what: run the tests against the known-good version before trusting them on the new one.
- Decide or delegate what you would otherwise leave hanging. A deferred decision that lives only in chat costs round trips or is lost; say "you decide, tell me" or park it in the backlog under your name.
- Constraints before, not after: who will review, in what shape, over which remote, with which account. Each one learned after the first attempt costs a redo.
- Say when you will be away and what to do meanwhile: "away an hour; take the recommended option, list the rest". A blocking question in your absence blocks until you return.
- When a real stakeholder is in the room, give the agent five minutes to list its open questions for them before relaying their wish.

**Judging the work**

- Judge behaviour by trying it, not by reviewing generated text: play tests, oracle commands, screenshots of a real terminal, the real back-end instead of a stub. A test that passed while the documented command failed teaches more than a rule.
- Measure instead of argue when the agent has an opinion about its own effectiveness: fresh agents, an answer key written before the runs, a blind grader. The agent's prior has been refuted this way.
- Challenge one recommendation per review; accepting all leans in a line is defensible, but disagreement is where you add the most.
- Documents others build on get thirty seconds: "which items still say pending, assumed or taken from the record?" and two quotes spot-checked.
- Expect evidence: the command run and its output, the screenshot, the diff of a re-recorded expectation; "clean" only from the command the commit or CI actually runs.

**What costs, and the fix**

- Work launched in a session dies with the session; context compaction loses detail; what lives in files survives. Before logging off: what is running and does it survive, where do results land, who answers the tester's questions, what is committed, what does the next session need.
- The agent's defaults are the manager's pet peeves: reinvented libraries, polish without a requirement, generality with one user. Standing instructions in `AGENTS.md`, a review by an agent that did not write the code, and "which scenario asks for this?" at commit time.
- A rule in a file is not a habit; a check is. Where a lesson can be a hook, a lint rule or a template field, put it there; the instruction file is the fallback.
- Agent memory is per user and per checkout path; a worktree or a VM starts empty. Team knowledge goes into the repository: instruction files, decision log, backlog, the `design/` documents.
- Output that leaves the project is read by people and by their agents. A short part for humans (what is wrong or decided, what to do, one example), then the details for agents; mark whether a human endorsed the details or only attached them.

## Licence

MIT, see `LICENSE`.
