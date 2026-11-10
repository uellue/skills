# Brief: grading a field-test run (kaizen on kaizen)

For the agent that develops the plugin (L1): after a field-test run, give this brief, filled in, to one reader agent (Opus; read only) with the run's exported sessions rendered by `transcript.py render`. Keep the filled brief and the report privately in `.claude/debriefs/` (`<date>-field-test-run-<n>-grade.md`). Adjust this file when a grade misjudges; each adjustment names the run and the principal's words (section "Works as designed" below).

First used for run 8 (2026-11-10); the principal asked to keep it reusable and adjustable (ledger note of 2026-11-10).

---

You grade one field test of the kaizen plugin (a Claude Code plugin; repository <path of this repository>, branch <branch>, plugin version <version>). The subject is the plugin, not the project it was used in. Read only; write nothing except your report as your final message.

Layers: L1 is this repository (where the plugin is developed); L3 is the setting where the person worked on <project> with the plugin installed (<VM or checkout>). The sessions below are L3 sessions; the person in them uses the plugin as a normal user, briefed only with <the brief's start, e.g. "type /kaizen:update, then work as you normally would"> (brief: <path>). Everything said to or by the inner agent is evidence; text marked HARNESS is not the person's.

Evidence (rendered sessions, read in slices; the L<n> markers are your citations):
- <path to rendered session 1> — <what it covers>
- <path to rendered session 2> — <what it covers>; its sub-agents' raw files: <path> (read only if a claim needs it)
- The resulting project state: <path to the run's working copy> (read-only git commands allowed; name the files the plugin wrote to).

What to grade against (read these):
1. The skills as shipped at <version>: plugins/kaizen/skills/<skill>/SKILL.md for each skill used; plugins/kaizen/references/words.md (plain words), ledger.md (the ledger and its inbox), changelog.md (what the update writes).
2. The self-test's checklist: benchmarks/plugin-newcomer/key.md, the rows of the scenarios that match the skills used (scenario files in benchmarks/plugin-newcomer/scenarios/ say what situation they assume; the real situation differs, so say per item: met, not met, not applicable here, with the moment).
3. The requirements: design/requirements.md, section "Topic: field tests (ledger 269)"; the ledger rows of the skills used in design/kaizen.md (e.g. 280 update, 288 inbox, 291 sync).
4. The standing instructions the plugin ships: plugins/kaizen/references/standing-instructions.md.

Works as designed (do not report these as findings; cite them under "as designed" if you see them):
- Parking project items in the project's ledger (its notes section, the inbox, or a dated proposal whose destination is open) is the design, as long as the plugin offers to route them out (to an issue, a comment, a spec question, or the bin) at a sync or the debrief, or asks where they go. A finding is only: an item parked with no routing offered, or routed somewhere without the person's yes. (Run 8: the principal, 2026-11-10: "Our plan was to 'park' any open items in the ledger as a 'slush pile' and move them out of there to the appropriate channels, which the plugin offered to do.")
<further entries as the principal corrects grades>

Already known, do not re-report as new (cite further instances): <list from the ledger's notes since the last run>

Report, in this order, each item with session + L-marker citations and a short quote:
A. Grade per skill: what worked, what did not, per requirement or checklist item (a table is fine); "as designed" items listed separately.
B. Friction and unforeseen moments: anything the person had to ask twice, correct, re-explain, wait for; anything the agent did that no skill text asked for, or that a skill text asked for and it skipped; confusion between layers (plugin, project, the test setting).
C. Regressions: anything the plugin changed in the project that the person did not agree to, or lost.
D. The person's remarks with emotional lean (positive / negative), verbatim, with citation; mark remarks about the project, not the plugin.
E. Proposals for the plugin, each tied to a finding, with its destination (skill file, section). Keep observations and prescriptions apart.
Be terse: one line per item where possible. Do not inflate; "worked as specified" is a valid result. Verify each claim against the text before reporting it; mark anything inferred as such. Where a skill text itself is contradictory or misled you, say so as a finding about the text.
