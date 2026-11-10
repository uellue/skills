# skills

A place to keep and share my AI agent skills, as a Claude Code plugin marketplace.

## Install

```bash
claude plugin marketplace add uellue/skills
claude plugin install kaizen@uellue --scope user
```

Or inside a session: `/plugin marketplace add uellue/skills`, then `/plugin install kaizen@uellue`.
To follow updates, turn on auto-update for the `uellue` marketplace under `/plugin` → Marketplaces. After an update, the first kaizen skill you run in a project says once, when the project's records are from an older version, that `/kaizen:update` shows what changed and brings the project up to date on a branch, asking before each change.

## First steps

In a Claude Code session in your project:

```text
/kaizen:playbook      which step of the work this is, and which skill fits now
/kaizen:hallway-test  a tool that already works, before others use it: a fresh first user tries it
/kaizen:debrief       after a stretch of work: how it went (it lists the sessions and asks before reading)
/kaizen:update        after the plugin was updated: what changed, and the project brought up to date
/kaizen:sync          the project and its upstream in step: tracker read, notes routed, what waits to go out
```

`/kaizen:update` and `/kaizen:sync` start only when you type them: asking in words ("let's sync") does not start them, by design, since they change your instructions or talk to your upstream. Not sure where you are? Start with `/kaizen:playbook`; it offers two further skills, requirements and walk-through, when they fit. The words the skills use are explained in [Words you will see](plugins/kaizen/references/words.md).

## Plugins

- **kaizen**: continuous improvement of how we work with agents (Toyota's word for improving the processes themselves). Five skills along the life of a project, one for its updates and one to keep it in step with its upstream, sharing documents in the project's `design/` directory (`stakeholders.md`, `requirements.md`, `walkthroughs/`, `examples.md`, `changes/`, `hallway/`, `kaizen.md`):
  - `/kaizen:playbook`: which moment a session is in and which skill fits: stakeholders, requirements, walk-throughs, the project's own specification method, build, hallway test, debrief; which shared documents are missing and which skill writes them.
  - `/kaizen:requirements`: interview the person who needs a solution in short rounds of the questions that are currently unblocked, and write a demand and requirements specification along a demand and requirements form written at ER-C (by the author; not an institute requirement), every item marked answered, record, assumed, unknown or deferred; reconstruct the requirements of a tool that grew from playing around, from its history and transcripts; check an existing document for what it skips; need before solution, numbers as numbers, prior art before "nothing exists"; a hand-over check that lists everything still unconfirmed. Section 1.4 writes the project's stakeholder record.
  - `/kaizen:walkthrough`: put on the shoes of a stakeholder from the record (never an assumed one) and walk through a process step by step, against the running system where there is one, to find the questions, gaps and acceptance examples nobody wrote down; a measured walk hands the process to a fresh agent under injected faults. Bundles a requirements questionnaire adapted from the same demand and requirements form; the two-hat interview and the "simulated stakeholders are lower confidence" rule are borrowed from Feature Forge (jeffallan) and melodic-software's requirements-elicitation skills.
  - `/kaizen:field-test`: a person tries the tool for real (real data, a real machine, an issue from real use) while the agent follows along through channels both checked first, and they talk about it as it happens: the frame asked, the setting walked through, safety limits written before any command on a shared machine, a runbook of one command per line read together, the run graded and its findings filed by layer.
  - `/kaizen:hallway-test`: a fresh sub-agent that sees only the requirements and the user documentation (with no requirements yet, the README alone) builds test cases, writes its expectations to a file before running, asks questions and reports bugs, surprises and gaps; by eye too, through a bundled xterm screenshot driver (needs xvfb, xterm, xdotool, imagemagick); as a diagnosis under injected faults; as an impatient user who only skims the README for commands and then follows the program's hints, where every break of that chain is a finding; on a README or an agent instruction file as an evaluation with a key written before the run and a grader who does not know which version it grades. The CLI usability checklist is adapted from the MIT-licensed cli-ux-tester skill by Alister Lewis-Bowen.
  - `/kaizen:update`: after the plugin was updated, bring a project up to date: what changed for projects since the version its records are from (`references/changelog.md`), the standing instructions merged line by line with the project's adaptations kept, new settings such as the issue tracker asked once, everything the project chose on purpose named and kept until you confirm, on a branch, ending with the version applied. Only you start it; the other skills say once per new version when a project is behind.
  - `/kaizen:sync`: bring the project and its upstream in step: fetch and read the issue tracker, mark ledger rows whose issues closed, route the notes you dropped into the ledger (an issue, a comment, a ledger row, or the bin), list what waits to go out (unpushed commits, drafts you asked for) and where your answer is needed, each posted only on your yes; the agent helps you through `git` and `gh`, shows and explains every command, and runs one itself only where you authorised it. Only you start it.
  - `/kaizen:debrief`: debrief a session, a stretch of work or several sessions at once on how the collaboration went, not on what it produced: cited moments, coaching for the person writing the prompts, proposals with a destination, a usage check with tokens counted once per API message, and the plugin's own skills checked for where they were used and where they would have helped. The report is private (`.claude/debriefs/`); only what is actionable goes into the repository's ledger (`design/kaizen.md` by default, committed; it asks whether the repository is or may become public, and then holds no details of other projects), and what you said about working with the plugin, liked or not, into `design/feedback.md`, cleaned (the verbatim words stay private). Scripts: `transcript.py` (locate, render, export sessions wherever the harness or a checkout keeps them) and `usage.py`. Structure adapted, with thanks, from the MIT-licensed `debrief` skill by Wavez and the `retrospective` plugin by florianbuetow.

**Works alongside other skills.** [Matt Pocock's skills](https://github.com/mattpocock/skills) (MIT) are a complete lifecycle of their own; several complement this plugin: `/mattpocock-skills:grill-me` (or `/mattpocock-skills:grill-with-docs` in a repository) when you have no clear idea yet, leading into `/kaizen:requirements`; `/mattpocock-skills:domain-modeling` for a glossary; `/mattpocock-skills:to-questionnaire` for questions to a stakeholder who is not in the room; `/mattpocock-skills:retro` for the agent's environment beside `/kaizen:debrief`; `/mattpocock-skills:handoff` before logging off. These are the names when installed as their Claude Code plugin; skills copied into `.claude/skills/` drop the prefix (`/grill-me`). The playbook keeps the full mapping. [OpenSpec](https://github.com/Fission-AI/OpenSpec) (MIT) fits the specification step between the kaizen skills before and after it. The playbook checks which of them are present, maps their steps onto its lifecycle and says what to know before installing them; the plugin works without either.

The two flows, in short (details and the full mapping: `/kaizen:playbook`):

```text
kaizen alone
  idea ─► /kaizen:requirements, /kaizen:walkthrough, design/examples.md (IDs)
       ─► decision record (design/changes/) ─► build
       ─► /kaizen:hallway-test ─► pull request ─► merge ─► /kaizen:debrief

with OpenSpec and/or Matt Pocock's skills (each optional, never installed unasked)
  idea ─► /mattpocock-skills:grill-me or /mattpocock-skills:grill-with-docs
          (discovery, when there is no idea yet)
       ─► /kaizen:requirements, /kaizen:walkthrough, design/examples.md (IDs)
       ─► specification, one of:
            OpenSpec /opsx:propose (the decision record goes into its design.md,
              each must-example becomes an OpenSpec scenario citing its ID)
            /mattpocock-skills:to-spec, then /mattpocock-skills:to-tickets
       ─► build (with OpenSpec: /opsx:apply)
       ─► /kaizen:hallway-test ─► pull request and its review
       ─► with OpenSpec: /opsx:archive on the branch, as the last commit before the merge
       ─► merge ─► /kaizen:debrief, beside /mattpocock-skills:retro
```

Where to archive is our recommendation; OpenSpec says only "archive when done". Archiving on the branch after the review lets the code and the updated specs reach the main branch in one merge, and changes asked for in the review still go into the open change, not into the archive.

The plugin's own stakeholders, requirements, testing plan and kaizen ledger are in `design/`.

## Working with agents: lessons learned

From debriefs of real sessions (a crawler, a dev-VM tool, a Nextcloud upgrade, autumn 2026). The skills above codify most of the process; this keeps what does not map to a skill yet. Two parts: what you do, and what you paste for the agent.

### What you do

Starting an agent session is onboarding a new employee that knows only the repository. So: write decisions, backlog and conventions into the repository, not into chat; and lead it like this.

1. **Say the outcome, not the solution**, with the boundary, model and effort in one message. Keep your own solution idea back; it tests whether the requirement was clear.
2. **Slash commands on their own line** (`/model`, `/effort`), then read the model line back. Typed inside a message they do nothing.
3. **Decide in numbered replies with a priority**; ask for options with counter-arguments, not for decisions.
4. **Label examples** ("this is one case of ..."), and generalise your own corrections.
   Phrase a request as a question when you want pushback; the agent's standing instructions say to answer with a verdict and the argument against before acting.
5. **Ask the behaviour question early**: "what changes for the user?", "does the test check the outcome the user cares about?"
6. **Judge behaviour, not text**: try it, hallway-test it, screenshot it, run it against the real back-end. Measure when the agent has an opinion about itself.
7. **Decide or delegate what you would leave hanging**; constraints (reviewer, MR shape, remote, account) before the work, not after.
8. **Say when you are away**, and what to do meanwhile.
9. **Challenge one lean per review**; give documents others build on thirty seconds: the unconfirmed items and two quotes.
10. **Don't polish in advance; fix unwanted outcomes when you have a concrete example**, with its test. Security and safety are the exception: think them through before.
11. **Prefer a check to a sentence**: a hook, a lint rule or a template field holds; a rule in a file is the fallback.
12. **Debrief after each release**: while the final acceptance tests run, note thoughts for the debrief; push and merge; then debrief, best in a new session (the session that did the work tends to confirm itself; it may run the debrief if it says so). Its proposals go into the next release, so there is never "one more thing before the push".
13. **Be clear and deliberate with words.** Muddy words in the prompt make muddy concepts, winding paths and muddy outcomes. When a term turns out to carry two meanings, settle it once in a glossary (`/mattpocock-skills:domain-modeling` does it with you, and fits well into a debrief); the agent then reads your words in the glossary's sense and says so when it is unsure.

### What you paste for the agent

Standing instructions, for `AGENTS.md` or `CLAUDE.md`. Merge, don't append: read each line against the project's existing instructions and requirements, keep the stricter rule, and point general rules at the project's own commands and documents. Keep the first line: it names the version the block is from, so that after an update the skills can tell the project is behind and `/kaizen:update` can show what changed.

```text
Kaizen standing instructions, version 0.6.0-dev.2: /kaizen:update brings them up to date with a newer plugin.
- Number every item and question you put to the person in one sequence across your messages: a new message continues from the last number used and never restarts at 1 while earlier numbered items are open; an open item restated keeps its number; no item without a number, no jumps. Write each as a bullet with its number in bold (`- **7** …`), never as a markdown numbered list (`7. …`): a display renumbers such a list from its first number. Restart only when nothing is open and nothing is still to come back from work in the background.
- Keep changes tight: no speculative generality, no abstraction without a second concrete user.
- Follow established formats, patterns and tools; before writing a mechanism a library implements, search for the library; before defining a term, look for the field's established vocabulary (a community glossary or ontology) and ask which one the project uses; ask before adding a new dependency, with its current release looked up, not recalled, and flag it in the hand-over.
- A pull request or release description starts from the branch's log and diff, grouped by area, so that nothing is left out; the size of a change is not its importance, and the agent can rarely judge which changes matter to which readers: ask the person, or leave the summary on top to them.
- Every mechanism, option or output detail names its source: a requirement, scenario, decision, or the person's request (record a request where the project keeps its requirements). Without any source, leave it out and suggest it as a next step.
- Earlier notes and brainstorming are options to evaluate, not requirements.
- When a request names a specific case, say whether you read it as the whole ask or as an example of a rule, or ask.
- When a word in a request is ambiguous or differs from the project's glossary, push back softly: say which reading you take, in the glossary's terms ("I read X as …"), and offer a glossary entry where none fits.
- A request phrased as a question ("should we ...?", "could X be a good place?", "we can proceed now?") is a question: answer it first with a verdict and the strongest argument against. Act only if the verdict is yes and the step is cheap to undo; otherwise wait for the person.
- Report evidence: the command run and its output, the screenshot, the diff of a re-recorded expectation. Report "clean" only from the command the commit or CI runs; give the number of skipped tests, and say where the local environment differs from CI's (user, groups, packages, switches that make a missing prerequisite fail).
- Before a long stretch without check-ins, or any loop of expensive test runs or many agents, give the estimated cost and agree a ceiling with the person (default $20 at list price); enforce it with a tool where one exists, and stop with a quarter of it left, never at the limit. Tests stay the feedback loop throughout, spent where much work remains: while iterating, run them in descending order of how likely the change affects them, one run per case while it is written; the less likely rest and repeated runs for statistics belong to the final acceptance tests.
- A change beyond a few hundred lines, or code that changes files or data on its own (a rewrite script, a migration, a hook), gets a review by an agent that did not write it before it is handed over.
- At every hand-over that follows accepted leans, list each one: implemented as agreed, or deviated and why; and show where the person's remarks went (what they said, what it became), without judgment.
- Do not build for cases nobody has hit; when an unwanted outcome appears, fix it with its concrete example and a test. Security and safety are the exception: think them through before building.
- Use absolute paths and self-contained shell commands; edit files with the Edit tool, not with inline replacement scripts.
- Never delete through a shell variable that could be empty or unset, in commands you run and in code you write (`"${var:?}"`, above all where the variable starts a path); quote variables, and prefer not creating what you would have to delete. Existing code is checked line by line and otherwise left as it is.
- A vulnerability found while testing is reported first and stops the plan; the fix path is the proposed next step.
- Anything that leaves the repository or a session for people and agents at once (issues, merge requests, upstream comments, hand-over notes, reports) is split: a short part for people first (what is wrong or decided, what to do, one example or the list of actions), then the part for agents (context, specifics, commands, what was verified), as a separate block, section or file, marked as reviewed by a person or attached unreviewed. Committed documentation counts as reviewed by its commit and is not restructured unasked.
- Offer a debrief (`/kaizen:debrief`) in one line, once, at each of these moments: a pull request merged, a release, the end of a day or a stretch of work, the first use of a kaizen skill in the project; and, once per stretch, while a run of several minutes goes on (above all the final acceptance tests), an invitation to note thoughts for it. Not at other times: an offer at every turn is noise.
```

When a project also uses Matt Pocock's skills, for `AGENTS.md` or `CLAUDE.md`:

```text
- When routing work with /mattpocock-skills:ask-matt, also place the kaizen moments in its flow: the stakeholder record and /kaizen:requirements after the grilling, /kaizen:walkthrough and design/examples.md before /mattpocock-skills:to-spec, /kaizen:hallway-test before the pull request, /kaizen:debrief on its schedule. See /kaizen:playbook.
```

Unblocking a round of questions:

```text
Go with your leans on all of these; most important is <the priority>. Details we can fix later. List what you decided.
```

Before stepping away:

```text
I am away for about <time>. Take your lean where you have one, keep going, and list every decision you took and every question you could not answer when I am back.
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

## For developers of this plugin: tests cost money

Testing a plugin means running agents: every eval case, self-test and hallway test is a full Claude session, and its judges are more. That is expensive, and it draws on your plan's usage. In one long stretch on 2026-11-10, 325 eval runs cost about $97 at list price and hit the session limit, which held up other work. This seems to be a general issue of plugin development, not one of this plugin: behaviour can only be tested by running it, and an agent left to iterate on its own will rerun tests generously. What helps here: agree a budget before a long stretch (the standing instructions above), run the evals through `plugins/kaizen/evals/run.py`, which refuses a run that could pass three quarters of the budget, and keep the full, repeated runs for the final acceptance test. The evals README (`plugins/kaizen/evals/README.md`) gives the measured cost per run of each suite.

## Licence

MIT, see `LICENSE`.
