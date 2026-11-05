---
name: playbook
description: Which kaizen skill fits now, and what the shared documents are. The lifecycle from stakeholders to requirements, walk-throughs, the decision record, the build, the hallway test and the debrief, with the moment each skill fires, the documents they share, a small-change path, and how to work alongside OpenSpec. Use it at the start of a project or a larger change, when the user asks how to approach product or feature development with agents, "what should we do next", "which skill applies", or when a session is about to specify, build or hand over something and no stakeholder record or requirements exist yet.
---

# Playbook

The other skills in this plugin are moments in one process. This skill says which moment a session is in, what document that moment reads and writes, and what to do when the document is missing. It does not replace the skills; it points at them, and at the gap when none fits.

All shared documents live in the project's `design/` directory. "The ledger" is always the project's own `design/kaizen.md`.

## The lifecycle

| Moment | Skill | Reads | Writes | Fires when |
|---|---|---|---|---|
| Who is this for | `requirements` (section 1.4) | the conversation, the record | `design/stakeholders.md`: one entry per persona (role, goal, knowledge, environment, what they never read, interviewed or simulated) | a project or change starts; a new kind of user appears; a walk-through or test needs a persona that is not on record |
| What is needed | `requirements` | stakeholders, the record, prior art | `design/requirements.md` (ER-C form numbering, markers per item, open questions with owner and stage) | the start of a project or a larger change; "what do we actually need"; a tool that grew from playing around needs its record reconstructed; an existing document to check; an open question or a vague idea on one topic that needs fleshing out |
| How it would go | `walkthrough` | stakeholders, requirements, what exists, the running system | `design/walkthroughs/<persona>-<process>.md` (steps, two hats, questions, gaps, answers from the owner); acceptance examples appended to `design/examples.md` | before a change is specified; requirements 2.1; before a hallway test, to decide what to test |
| What we decided | this skill, with `references/change-record.md` | requirements, walk-throughs, examples | `design/changes/<name>.md`: interface, decisions with who decided and whether reversible, must / should / won't with a size budget, the examples it must satisfy, the questions that block the build. With OpenSpec, the same content goes into the change's `design.md` and scenarios instead (see below) | after the walk-throughs, before the build; whenever an implementer would otherwise invent decisions |
| Build | the project's instructions | the decision record | code, tests citing example IDs, docs | every sub-agent brief names the example IDs each assertion serves |
| Does it hold up | `hallway-test` | stakeholders, requirements, user documentation, the examples | `design/hallway/<date>.md`, committed; imagined versus observed added to the walk-through | something exists that a first user could try; before a merge request; with OpenSpec, after apply and before archive |
| How did we work | `debrief` | the transcripts, the ledger, the memory, the instruction files | `.claude/debriefs/<date>.md` (private, full); `design/kaizen.md` (proposals with decisions, earlier recommendations, skill friction, notes) | on a schedule (end of a day, end of a stretch); after a skill was used for the first time; when the person says "note for the debrief" (then the note goes to the ledger at once) |

**Acceptance examples have one home**, `design/examples.md`: one line each, with an ID (`E1`, `E2`, …), the concrete situation and observable outcome, a priority (must / should), and the walk step or requirement it came from. Walk-throughs and the requirements interview append to it; decision records, scenarios, tests and tester briefs cite the IDs; nobody keeps a copy. Before a hand-over, list every example with no scenario or test.

## Size the process to the change

The trials of 2026-11-05 wrote 34 KB of records for a 4 KB tool. Choose the path:

- **Small change** (one command, one behaviour, a few hours): a need note of five lines in the decision record (whose need, what the request names, what the need behind it is); one walk-through as a step table of at most about 300 words, against the running system; the examples; the decision record; the hallway test. No full requirements form, no OpenSpec specs or tasks.
- **Larger change or a new project:** the full table above.
- **A single open question or idea:** the requirements interview or a walk-through on that topic only, and its answer into the existing documents.

Do what the moment needs and leave the rest: fix unwanted outcomes when there is a concrete example, rather than specifying every detail in advance. Security and safety are the exception: think them through before building.

## Working without a person

When no principal is available (an agent-only run, a trial, an evaluation), the skills may simulate one, and then:

- Write the simulated principal's persona into the stakeholder record first, marked simulated, before the interview starts.
- A simulated principal may answer questions, marked `[assumed]`; it may not confirm personas, accept leans or unblock the build. Those wait for a person and are listed at hand-over.
- The decision record says on which assumptions the build may start.

## Alongside OpenSpec

The plugin covers what comes before a specification (stakeholders, requirements, walk-throughs, examples) and after it (hallway test, debrief); OpenSpec ([github.com/Fission-AI/OpenSpec](https://github.com/Fission-AI/OpenSpec), MIT, `npm install -g @fission-ai/openspec`) structures the specification itself: proposal, spec deltas, design, tasks, structural validation, archive, and the rule not to touch code while planning. A comparison on 2026-11-05 found the content in the kaizen steps, the structure in OpenSpec, and the links between them in the project's own `config.yaml` rules; the hallway test found the worst defects after `openspec validate --strict` had passed, because validation checks structure, not content.

At the start of a session:

1. Check whether OpenSpec is in use (an `openspec/` directory) or installed (`openspec --version`).
2. If neither, and the change is larger than small, mention it once as an option, with the facts the person needs to decide: a third-party dependency (Node.js package, single maintainer), telemetry on by default (`export OPENSPEC_TELEMETRY=0` to turn it off). Do not install it unasked; the plugin works without it, with the decision record in `design/changes/`.
3. If it is in use, offer the rules in `${CLAUDE_PLUGIN_ROOT}/references/openspec-config.yaml` for the project's `openspec/config.yaml` (merge with what is there; the generated file is empty).

The hand-off, in both directions:

- **Before `/opsx:propose`:** the stakeholder record, the walk-throughs and `design/examples.md` exist for the change, or the proposal says why not. The proposal names the persona, says whether the requested solution is the whole need, and lists the premises nobody confirmed.
- **Into the change:** the decision record's content goes into OpenSpec's `design.md`; each must-example becomes a scenario that cites its ID; an example without a scenario is listed in the proposal. Requirements stay in `design/requirements.md`; OpenSpec's specs are the behaviour contract, not the place for new requirements.
- **After apply, before archive:** the hallway test, with the scenarios as part of its coverage and at least half its effort outside them. `validate` and `verify` do not replace it. The debrief flags a change archived without a hallway test, and scenarios without an example ID.
- **Deferrals:** OpenSpec asks to settle questions that change the approach before proposing; the plugin records deferrals with stage and owner. Both hold: a question that changes the approach blocks the proposal; one that does not is deferred in the requirements and named in the proposal.
- **Exploring:** where both are installed, use the `requirements` interview and `walkthrough` to clarify a need, not `/opsx:explore`, which writes into `specs/`.

## When a session starts

1. Look for the documents in the table. For each one that is missing and that this session's work would need, say so and offer the skill that writes it; do not write it unasked.
2. Choose the path by size, and say which.
3. If the person brings a request that names a case or a solution, ask whether it is the whole need or an example (the `requirements` habit), and whether a persona on record is the one asking.
4. If the session will hand something over (a document, a change, a merge request), plan the hallway test and the debrief as part of the work, not after it.

## Which skill would have supported this

At every point where the session finds a defect, a misunderstanding, a gap in a document or a question nobody can answer, ask which moment in the table should have caught it, and write the answer into the ledger's notes. That question, asked at the moment and not at the debrief, is what makes the next debrief short.

## Rules

- A missing document is a finding, not a reason to assume its content.
- The person decides which moment the session is in and which path; this skill proposes.
- At the end of any skill's run, one line into the ledger: what in the skill did not fit.
