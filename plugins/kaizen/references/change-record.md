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
Each row a question an implementer would otherwise answer alone: names, semantics (substring or word, exact or fuzzy), constants (timeouts, limits), compatibility with old data and old clients. "Decided by": the person (answered) or the author (assumed). Security and safety decisions are never left to "assumed" without saying so at hand-over. When the change acts on hardware, one row per safety stop: what the software refuses or does on its own (a move outside the envelope, a lost connection), and who agreed; and one required row "develop against what": the simulator, a dry-run mode, or the real instrument with the owner's agreement, recorded as answered with the owner's name and the date; a principal who is not the owner cannot accept it as an assumption. With no simulator, building or faking one is planned work with its own must-examples, among them "it enforces the instrument's limits" and "its output is labelled as simulated wherever it is kept, never presented as a real result". The limits come from the owner or the vendor's documentation, never from the author; until they are on record, the limits example is blocked and says so. This row is the one place for these rules; the playbook, the walk-through and the hallway test point here.

## 4. Scope
Must: <example IDs from design/examples.md>. Should: <IDs>. Won't (this change): <IDs or items>.
Size budget: <for example "notes.py stays under 120 lines; no new dependency">.

## 5. Blocking questions
The questions that must be answered before the build starts, with who answers. If the build starts anyway, on which assumptions, and what changes if they turn out wrong.
```

Where the project keeps ADRs (`docs/adr/`, for example from Matt Pocock's `domain-modeling` skill), a decision that is hard to reverse, surprising without context and the result of a real trade-off also gets an ADR that links back here; all other decisions stay in this record only.

Hand-over of the built change: each must-example has a test that cites its ID; each accepted lean is listed as implemented as agreed or deviated and why; the hallway test record is linked.
