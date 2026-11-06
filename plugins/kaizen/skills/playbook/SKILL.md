---
name: playbook
description: Which kaizen skill fits now, and what the shared documents are. The lifecycle from a first idea to stakeholders, requirements, walk-throughs, the decision record, the build, the hallway test and the debrief, with the moment each skill fires, the documents they share, a small-change path, working without a person, and how to work alongside OpenSpec and Matt Pocock's skills. Use it at the start of a project or a larger change, when the user asks how to approach product or feature development with agents, "what should we do next", "which skill applies", when routing work with ask-matt or another skill router (to place the kaizen moments in that flow), or when a session is about to specify, build or hand over something and no stakeholder record or requirements exist yet.
---

# Playbook

Text id `b5298646`: first run `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/version.py playbook b5298646` as it stands and pass on what it prints, if anything (it is silent when all is well; if it fails, carry on).

The other skills in this plugin are moments in one process. This skill says which moment a session is in, what document that moment reads and writes, and what to do when the document is missing. It proposes; the person decides which moment the session is in and which path to take.

All shared documents live in the project's `design/` directory. "The ledger" is always the project's own `design/kaizen.md`.

## When a session starts

1. Unless the repository already answers it, ask what the tool writes or changes (next to its inputs, on a server) and what makes a change take effect (a push, a deploy, a restart). A tool that writes into its inputs' directories always gets the next question, for the data it will meet in its users' hands too. If that reaches something real it could damage or that could cause harm (an instrument or other hardware; production, valuable or irreplaceable data; a service or website that is live, public or in use; messages to real people: the decision record's safety row), ask who owns it and whether a stand-in exists (a simulator, a copy, a staging service, a dry-run mode). An unknown answer is an open question that blocks work on the real thing; the session goes on.
2. Choose the path by size (below) and say which.
3. Look for the documents in the table below. For each one that is missing and that the chosen path needs, say so and offer the skill that writes it; do not write it unasked. Before creating `design/` in a project that has none, ask, and ask whether committed files become public (a public repository, a site deployed from a branch); the person may name another place, outside the published tree.
4. Check which complementary tools are present, and follow the sections below: OpenSpec (an `openspec/` directory, or `openspec --version`); Matt Pocock's skills (`claude plugin list` shows `mattpocock-skills`, or copies under `.claude/skills/` or `~/.claude/skills/`; most of his skills are invoked by name only and do not appear in the list of skills an agent sees; his documents are a further sign: `GLOSSARY.md` at the root, `docs/adr/`, `docs/agents/`).
5. If the request names a case or a solution, ask whether it is the whole need or an example, and whether a persona on record is the one asking.
6. If the session will hand something over (a document, a change, a merge request), plan the hallway test and the debrief as part of the work, not after it.

## The lifecycle

| Moment | Skill | Writes | Fires when |
|---|---|---|---|
| From nothing to an idea | optional: `grill-me` or `grill-with-docs` from Matt Pocock's MIT-licensed skills (github.com/mattpocock/skills); invoked by name only: type `/mattpocock-skills:grill-me` (plugin) or `/grill-me` (copied skill) | notes the requirements interview starts from; with `grill-with-docs`, the glossary and ADRs | the person cannot yet name who needs it and what they would do differently; otherwise go to `requirements` (`grill-me` wraps the `grilling` skill) |
| Who is this for | `requirements` (section 1.4) | `design/stakeholders.md`: one entry per persona (role, goal, knowledge, environment, what they never read; interviewed, described by <who>, or simulated) | a project or change starts; a new kind of user appears; a walk-through or test needs a persona not on record |
| What is needed | `requirements` | `design/requirements.md` (form sections as a checklist, markers per item, open questions with owner and stage) | a loose idea needs tightening; a project or larger change starts; a tool that grew from playing around needs its record reconstructed; an existing document to check; one open question or vague idea needs fleshing out |
| How it would go | `walkthrough` | `design/walkthroughs/<persona>-<process>.md`; acceptance examples appended to `design/examples.md` | before a change is specified; requirements 2.1; before a hallway test, to decide what to test |
| What we decided | the agent, with the person, from `${CLAUDE_PLUGIN_ROOT}/references/change-record.md` | `design/changes/<name>.md`: need, interface, decisions with who decided and whether reversible, must / should / won't with a size budget, blocking questions | after the walk-throughs, before the build; whenever an implementer would otherwise invent decisions. The agent drafts it and asks the person for each decision it cannot take from the record; it is done when every must-example is cited and every blocking question is answered or named as an assumption the person accepted |
| Build | the project's own instructions | code, tests citing example IDs, docs | every sub-agent brief names the example IDs each assertion serves; anything it could damage as the decision record's safety row says (`${CLAUDE_PLUGIN_ROOT}/references/change-record.md`) |
| Does it hold up | `hallway-test` | `design/hallway/<date>.md`; imagined versus observed added to the walk-through | something exists that a first user could try; before a merge request |
| How did we work | `debrief` | `.claude/debriefs/<date>.md` (private); `design/kaizen.md` (ledger) | on a schedule (end of a day or a stretch); after a skill's first use; at least once per release: wind the working session down, debrief in a fresh session, apply what belongs in the release, then push; "note for the debrief" goes to the ledger at once |

**Acceptance examples have one home**, `design/examples.md`: one line each, with an ID (`E1`, `E2`, …), the concrete situation and observable outcome, a priority (must / should), and the walk step or requirement it came from. Walk-throughs and the requirements interview append to it; decision records, scenarios, tests and tester briefs cite the IDs; nobody keeps a copy. Before a hand-over, list every example with no scenario or test.

## Size the process to the change

Records can easily outweigh the change they describe. Choose the path:

- **Small change** (one command, one behaviour, a few hours): a need note of five lines at the top of the decision record (whose need, what the request names, what the need behind it is); a stakeholder record of one or two entries, since the walk-through needs a confirmed persona; one walk-through as a step table of at most about 300 words, against the running system (a stand-in where it could damage something); the examples; the decision record; the hallway test. No full requirements form, no OpenSpec specs or tasks.
- **An existing tool before its first hand-over** (it works for its author; others start using it soon): the hallway test now, with the person as the source of the persona; a reconstruction of the requirements afterwards, from its findings.
- **Larger change or a new project:** the full table.
- **A single open question or idea:** the requirements interview or a walk-through on that topic only, its answer into the existing documents.

Fix unwanted outcomes when there is a concrete example, rather than specifying every detail in advance. Security and safety are the exception: think them through before building.

## Working without a person

When no principal is available (an agent-only run, a trial, an evaluation), the skills may simulate one, and then:

- The simulated principal's persona is written into the stakeholder record first, marked simulated, before the interview starts.
- A simulated principal may answer questions, marked `[assumed]`; it may not confirm personas, accept leans or unblock the build. Those wait for a person and are listed at hand-over.
- The decision record says on which assumptions the build may start.

## Alongside OpenSpec

The plugin covers what comes before a specification (stakeholders, requirements, walk-throughs, examples) and after it (hallway test, debrief). OpenSpec (github.com/Fission-AI/OpenSpec, MIT, `npm install -g @fission-ai/openspec`) structures the specification itself: proposal, spec deltas, design, tasks, structural validation, archive, and the rule not to touch code while planning. Its `validate` checks structure, not content; the hallway test is what finds whether a user can do the thing.

- **Not in use and not installed:** for a change larger than small, mention it once as an option with what the person needs to decide (checked 2026-11-05: a third-party Node.js package with one maintainer on the npm registry; its README says telemetry is on unless `OPENSPEC_TELEMETRY=0` is set). Do not install it unasked; without it, the decision record in `design/changes/` does its job.
- **In use:** offer the rules in `${CLAUDE_PLUGIN_ROOT}/references/openspec-config.yaml` for the project's `openspec/config.yaml` (merge with what is there; `openspec init` writes one with comments only).
- **Before `/opsx:propose`:** the stakeholder record, the walk-throughs and `design/examples.md` exist for the change, or the proposal says why not. The proposal names the persona, says whether the requested solution is the whole need, and lists the premises nobody confirmed.
- **Into the change:** the decision record's content goes into OpenSpec's `design.md` instead of `design/changes/`; each must-example becomes a scenario that cites its ID. Requirements stay in `design/requirements.md`; OpenSpec's specs are the behaviour contract, not the place for new requirements.
- **After apply, before archive:** the hallway test, with the scenarios as part of its coverage and at least half its effort outside them.
- **Deferrals:** a question that changes the approach blocks the proposal; one that does not is deferred in the requirements with stage and owner and named in the proposal.
- **Exploring:** where both are installed, clarify a need with `requirements` and `walkthrough`, not `/opsx:explore`, which writes into `specs/`.

## Alongside Matt Pocock's skills

Matt Pocock's MIT-licensed skills (github.com/mattpocock/skills) are a complete lifecycle of their own, with a router (`ask-matt`), a specification path (`to-spec`, `to-tickets`), review and retrospective. They complement the plugin and the plugin does not depend on them. Their Claude Code plugin installs all of them at once (27 skills in version 1.3.2, checked 2026-11-05), and eleven of them start on their own (among them `grilling`, `domain-modeling`, `tdd`, `prototype` and `code-review`, which shares its name with Claude Code's built-in command); [skills.sh](https://skills.sh/mattpocock/skills) copies single skills instead. When they are not present and a moment below would benefit, mention them once with that information; do not install them unasked.

| Moment | Kaizen | Theirs, when present |
|---|---|---|
| From nothing to an idea | none | `grill-me`, or `grill-with-docs` in a repository; its result is the record `requirements` starts from |
| Vocabulary | none | `domain-modeling` keeps `GLOSSARY.md` at the repository root; kaizen documents use its terms and do not redefine them |
| Questions for a real stakeholder | the walk-through lists them | `to-questionnaire` turns them into a document to send or fill in together |
| What we decided | the decision record in `design/changes/` | an ADR in `docs/adr/` only for a decision that is hard to reverse, surprising without context and the result of a real trade-off (their criteria); it links to the decision record |
| Specification | OpenSpec, or the decision record | `to-spec` and `to-tickets` as another option (they need his `setup-matt-pocock-skills` run once for the issue tracker); the same rule applies: specs and tickets cite the example IDs |
| Retrospective | `debrief`: the collaboration, coaching for the person, the history across debriefs | `retro`: the agent's environment (checks, navigation, steering files); invoked by the person only, as a message of its own, or run by the debrief through an independent sub-agent; the two complement each other |
| Before logging off | the debrief's notes, the hand-over | `handoff` writes the state for the next session |

When `ask-matt` routes the work, place the kaizen moments in its flow: stakeholders and the requirements interview after the grilling, walk-throughs and `design/examples.md` before `to-spec`, the hallway test before the pull request, the debrief on its schedule. `to-spec` synthesises the conversation without an interview, and ask-matt keeps grilling, spec and tickets in one context window: the kaizen steps in between fill that window, so tell `to-spec` to read `design/requirements.md`, `design/examples.md` and the decision record, or compact at that boundary as ask-matt advises. Their documents stay where their skills put them (`GLOSSARY.md`, `docs/adr/`, `docs/agents/`, `.scratch/`); the kaizen documents stay in `design/`.

## Which skill would have supported this

At every point where the session finds a defect, a misunderstanding, a gap in a document or a question nobody can answer, ask which moment in the table should have caught it, and write the answer into the ledger's notes. Asked at the moment and not at the debrief, it makes the next debrief short.

## Rules

- A missing document is a finding, not a reason to assume its content.
- At the end, one line into the project's `design/kaizen.md`: what in this skill did not fit. If the file does not exist yet, say first where it will go and that it is meant to be committed, and start it from `${CLAUDE_PLUGIN_ROOT}/references/ledger.md`.
