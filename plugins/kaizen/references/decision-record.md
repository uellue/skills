# Decision record for a change (template)

What the walk-throughs and the requirements leave open and an implementer would otherwise invent. One file per change, `design/changes/<name>.md`, named after the need, not the solution. With OpenSpec, the same content goes into the change's `design.md` (sections 2 to 5) and its scenarios (section 4); this file is then not written.

```markdown
# Change: <the need, in a few words>

Status: <draft | decided | built | tested>. Path: <small | larger>. Decided by: <person, date | assumed, waits for <person>>.

## 1. Need
Whose need (persona from design/stakeholders.md), what the request named, what the need behind it is, in five lines at most. What is out of scope.

## 2. Interface
The commands, options, inputs and outputs as a user meets them; data and file formats that change; errors and exit statuses; what goes to stdout and stderr. Only what this change touches; existing behaviour it relies on is stated in one line each, so it is not changed by accident.

## 3. Decisions
| # | Question | Options | Choice | Decided by | Reversible? |
|---|---|---|---|---|---|
Each row a question an implementer would otherwise answer alone: names, semantics (substring or word, exact or fuzzy), constants (timeouts, limits), compatibility with old data and old clients. "Decided by": the person (answered) or the author (assumed). Security and safety decisions are never left to "assumed" without saying so at hand-over. When the change acts on something real it could damage or that could cause harm (an instrument or other hardware; production, valuable or irreplaceable data; a service or website that is live, public or in use; messages to real people), one row per safety stop: what the software refuses or does on its own (a move outside the instrument's safe range, a write to the original data, a lost connection), where it is enforced (in code outside any agent that operates the thing, never by the model's judgement alone), and who agreed; one row for which actions need a person's confirmation and which may run unattended; and one required row "develop against what": a stand-in (a simulator, a copy of the data, a staging service, a local preview, a dry-run mode), on which work may start without the owner, or the real thing, which needs the owner's agreement recorded as answered with the owner's name and the date; a principal who is not the owner cannot accept that as an assumption, while a principal who already publishes or operates there on their own authority is its owner for this purpose, recorded as such. With no stand-in, building one is planned work and the first buildable item, with its own must-examples, among them "it enforces the real thing's limits" (the instrument's safe range of motion and dose, the data's permissions) and "its output is labelled as simulated wherever it is kept, never presented as a real result". The limits come from the owner or the vendor's documentation, never from the author; until they are on record, the limits example is blocked and says so, and the simulator's limits are placeholders marked blocked. These two examples are for a simulator, which imitates the real thing. A local preview that serves the same files needs no "simulated" label; its one example is "it serves the same paths as the real site" (the base path, the files served). Results on an exact copy of data are real and need neither. When the original data turns out to be the only copy, propose a backup before anything else. This row is the one place for these rules and the list of what counts; the playbook (which quotes the list), the questionnaire, the walk-through and the hallway test point here.

## 4. Scope
Must: <example IDs from design/examples.md>. Should: <IDs>. Won't (this change): <IDs or items>.
Size budget: <for example "notes.py stays under 120 lines; no new dependency">.

## 5. Blocking questions
The questions that must be answered before the build starts, with who answers. If the build starts anyway, on which assumptions, and what changes if they turn out wrong.
```

Where the project keeps ADRs (`docs/adr/`, for example from Matt Pocock's `domain-modeling` skill), a decision that is hard to reverse, surprising without context and the result of a real trade-off also gets an ADR that links back here; all other decisions stay in this record only.

Hand-over of the built change: each must-example has a test that cites its ID; each accepted lean is listed as implemented as agreed or deviated and why; the hallway test record is linked.
