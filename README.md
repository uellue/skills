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

From debriefs of real sessions (a crawler, a dev-VM tool, a Nextcloud upgrade, autumn 2026). The skills above codify most of the process; this keeps what does not map to a skill yet. Two parts: what you do, and what you paste for the agent.

### What you do

Starting an agent session is onboarding a new employee that knows only the repository. So: write decisions, backlog and conventions into the repository, not into chat; and lead it like this.

1. **Say the outcome, not the solution**, with the boundary, model and effort in one message. Keep your own solution idea back; it tests whether the requirement was clear.
2. **Slash commands on their own line** (`/model`, `/effort`), then read the model line back. Typed inside a message they do nothing.
3. **Decide in numbered replies with a priority**; ask for options with counter-arguments, not for decisions.
4. **Label examples** ("this is one case of ..."), and generalise your own corrections.
5. **Ask the behaviour question early**: "what changes for the user?", "does the test check the outcome the user cares about?"
6. **Judge behaviour, not text**: try it, play-test it, screenshot it, run it against the real back-end. Measure when the agent has an opinion about itself.
7. **Decide or delegate what you would leave hanging**; constraints (reviewer, MR shape, remote, account) before the work, not after.
8. **Say when you are away**, and what to do meanwhile.
9. **Challenge one recommendation per review**; give documents others build on thirty seconds: the unconfirmed items and two quotes.
10. **Don't polish in advance; fix unwanted outcomes when you have a concrete example**, with its test. Security and safety are the exception: think them through before.
11. **Prefer a check to a sentence**: a hook, a lint rule or a template field holds; a rule in a file is the fallback.

### What you paste for the agent

Standing instructions, for `AGENTS.md` or `CLAUDE.md`:

```text
- Keep changes tight: no speculative generality, no abstraction without a second concrete user.
- Follow established formats, patterns and tools; before writing a mechanism a library implements, search for the library; flag every new dependency.
- Every mechanism, option or output detail names the requirement, scenario or decision that asks for it; without one, leave it out and suggest it as a next step.
- Earlier notes and brainstorming are options to evaluate, not requirements.
- When a request names a specific case, say whether you read it as the whole ask or as an example of a rule, or ask.
- Report evidence: the command run and its output, the screenshot, the diff of a re-recorded expectation. Report "clean" only from the command the commit or CI runs.
- A change beyond a few hundred lines gets a review by an agent that did not write it before it is handed over.
- At every hand-over that follows accepted leans, list each one: implemented as agreed, or deviated and why.
- Do not build for cases nobody has hit; when an unwanted outcome appears, fix it with its concrete example and a test. Security and safety are the exception: think them through before building.
- Use absolute paths and self-contained shell commands; edit files with the Edit tool, not with inline replacement scripts.
- A vulnerability found while testing is reported first and stops the plan; the fix path is the proposed next step.
- Anything written for people and agents at once is split: a short part for people first (what is wrong or decided, what to do, one example or the list of actions), then the part for agents (context, specifics, commands, what was verified), as a separate block, section or file, marked as reviewed by a person or attached unreviewed. This applies to issues and merge requests, hand-over notes, guides, reports and documentation alike.
```

Unblocking a round of questions:

```text
Go with your leans on all of these; most important is <the priority>. Details we can fix later. List what you decided.
```

Before stepping away:

```text
I am away for about <time>. Take the recommended option where you have one, keep going, and list every decision you took and every question you could not answer when I am back.
```

Before ending a session:

```text
Before we stop: what is running, and does it survive the session? Where do the results land, and is anything only in the scratchpad or /tmp? What is committed, what is not? What does the next session need to know that it cannot read from the repository?
```

When a sub-agent brief is written:

```text
For every assertion or check in the brief, name the scenario or acceptance example it serves. Assert the outcome the user cares about, not the mechanism you expect. Report what the test proves and what it does not.
```

When a document is handed over:

```text
List every item that is still marked pending, assumed, taken from the record or unknown, and every quote or figure you took from a sub-agent and did not check against the source.
```

## Licence

MIT, see `LICENSE`.
