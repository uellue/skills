---
name: playbook
description: Which kaizen skill fits now, and what the shared documents are. The lifecycle from stakeholders to requirements, walk-throughs, specification, build, hallway test and debrief, with the moment each skill fires and the documents they share. Use it at the start of a project or a larger change, when the user asks how to approach product or feature development with agents, "what should we do next", "which skill applies", or when a session is about to specify, build or hand over something and no stakeholder record or requirements exist yet.
---

# Playbook

The four other skills in this plugin are moments in one process. This skill says which moment a session is in, what document that moment reads and writes, and what to do when the document is missing. It does not replace the skills; it points at them, and at the gap when none fits.

## The lifecycle

| Moment | Skill | Reads | Writes | Fires when |
|---|---|---|---|---|
| Who is this for | `requirements` (section 1.4) | the conversation, the record | `design/stakeholders.md`: one entry per persona (role, goal, knowledge, environment, what they never read, interviewed or simulated) | a project or change starts; a new kind of user appears; a walk-through or test needs a persona that is not on record |
| What is needed | `requirements` | stakeholders, the record, prior art | `design/requirements.md` (ER-C form numbering, markers per item, open questions with owner and stage) | the start of a project or a larger change; "what do we actually need"; a tool that grew from playing around needs its record reconstructed; an existing document to check for what it skips |
| How it would go | `walkthrough` | stakeholders, requirements, what exists, the running system | `design/walkthroughs/<persona>-<process>.md`: steps, two hats, questions, gaps, acceptance examples, answers from the owner | before a change is specified; requirements 2.1; before a hallway test, to decide what to test; when a document is about to be written for a reader who has not been imagined yet |
| What will be built | the project's specification method (OpenSpec, a spec file, an issue with acceptance examples) | requirements, walk-throughs | the spec, with the acceptance examples as scenarios and "what changes for the user" stated | after the walk-throughs, before the build |
| Build | the project's instructions | the spec | code, tests, docs | every sub-agent brief names the scenario or acceptance example each assertion serves |
| Does it hold up | `hallway-test` | stakeholders, requirements, user documentation, the walk-through's coverage | `design/hallway/<date>.md` or `design/playtest.md`, committed; expectations before running; imagined versus observed added to the walk-through | something exists that a first user could try: a command, a README, an instruction file, a diagnosis; before a merge request; after a fix that changes what the user sees |
| How did we work | `debrief` | the transcripts, the ledger, the memory, the instruction files | `.claude/debriefs/<date>.md` (private, full); `design/kaizen.md` (ledger: proposals with decisions, earlier recommendations, skill friction, notes) | on a schedule (end of a day, end of a stretch), not at an end nobody sees coming; after a skill was used for the first time; when the person says "note for the debrief" (then the note goes to the ledger at once) |

The specification method is the project's own; this plugin sits before it (stakeholders, requirements, walk-throughs) and after it (hallway test, debrief). Where OpenSpec is used, the walk-throughs' acceptance examples become its scenarios and the hallway test takes the scenarios as its coverage list; whether the spec made the build better is measured, not assumed: in the review, count the findings that cite a scenario, and in the hallway test, count the scenarios that held.

## When a session starts

1. Look for the documents in the table. For each one that is missing and that this session's work would need, say so and offer the skill that writes it; do not write it unasked.
2. If the person brings a request that names a case, ask whether it is the whole need or an example (the `requirements` habit), and whether a persona on record is the one asking.
3. If the session will hand something over (a document, a change, a merge request), plan the hallway test and the debrief as part of the work, not after it.

## Which skill would have supported this

At every point where the session finds a defect, a misunderstanding, a gap in a document or a question nobody can answer, ask which moment in the table should have caught it, and write the answer into the ledger's notes. That question, asked at the moment and not at the debrief, is what makes the next debrief short.

## Rules

- A missing document is a finding, not a reason to assume its content.
- The person decides which moment the session is in; this skill proposes.
- At the end of any skill's run, one line into the ledger: what in the skill did not fit.
