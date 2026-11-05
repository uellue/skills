# Condition briefs

One fresh agent per condition, each on its own copy of `project/`. Placeholders: `<PLUGIN>` is the kaizen plugin directory (`plugins/kaizen/` of this repository), `<OPENSPEC>` the OpenSpec CLI, `<WORK>` the condition's working copy. The baseline briefs also pointed to evidence of real use in other projects; that is left out here so that runs are comparable across machines.

## Common part (all conditions)

You are one of three reviewers in a comparison. Each reviewer takes the same small project and the same change request through a different process, then reviews critically. The question behind the comparison: what each process contributes, what it lacks, and what would make it better. Be critical, not polite.

The project is in `<WORK>` (a git repository: `notes.py`, `README.md` with the change request, `CLAUDE.md`). Work only there. There is no principal to interview: play the group leader yourself and mark every answer you give as simulated.

Return your report as your final message (at most 2,000 words, dense, citing file and line or the artefact): what you did with the artefacts and their sizes; what the process contributed that a plain "implement this" session would not have; what it lacked; defects and friction in the process's instructions; cost per stage; your recommendation and the three changes with the best value.

## A: kaizen alone

Read `<PLUGIN>/skills/playbook/SKILL.md` first, then the other skills and `<PLUGIN>/references/`. Take the change request from request to a state where an implementer could start, following the skills as written; implement the change and run a hallway test if time allows. Do not use OpenSpec. Note every point where a skill's instruction was unclear, missing, wrong for the situation or too long, and where you had to invent a step; and whether an implementer could work from your artefacts.

## B: OpenSpec alone

Run `<OPENSPEC> init --tools claude` in `<WORK>`, read what it generated and follow its workflow as written (proposal, specs, design, tasks, validate; apply and archive if you implement). Do not use the kaizen skills during the trial; read `<PLUGIN>/skills/*/SKILL.md` afterwards to say what OpenSpec lacks that they cover, and the reverse. Note where OpenSpec pushed you to a solution before the need was clear, where a stakeholder's view or an acceptance example was missing and nothing asked for it, and what it did well.

## C: both

Follow the playbook (`<PLUGIN>/skills/playbook/SKILL.md`): kaizen before the specification (stakeholders, requirements, walk-through, examples), OpenSpec for the change (`<OPENSPEC> init --tools claude`, the playbook's `config.yaml` rules, proposal, specs, design, tasks, validate), kaizen after it (hallway test). Implement and test if time allows. Note every point where the hand-off between them was unclear, duplicated or contradictory, and where the combination was clearly better than either alone.
