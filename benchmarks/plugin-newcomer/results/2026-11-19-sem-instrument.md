# Run 2026-11-19: scenario sem-instrument, commit `a26ddc9` (0.6.1-dev.2), Opus, about 3 minutes

Usage of the tester (`usage.py agent-ae058a076338ff305`): Output tokens, claude-opus-5-5 18,521 . The tester's report was read by the main session from its transcript; claims it makes about the plugin's text were checked by the main session before grading.

Graded by a fresh Sonnet agent that changed no skill, from the report, the key and the main session's checked claims.

Result format: E15. The tester wrote its expectations before its first command (13:46:51). Findings marked "unchecked" were not among the claims the main session verified. They are candidates only.

## Grades

| # | Result |
|---|---|
| N1 | partly: the tester followed the README's "Then, once in each project" to `/kaizen:update` first and called the playbook "the real first step". It reached the playbook only through "Not sure where you are?". The update hand-over named no next step. Checked: the README's First steps no longer list `/kaizen:update`. |
| N2 | held: "The version line was silent" in update, playbook and requirements (rc=0, no output). |
| N3 | held: M4, at playbook step 1 before requirements: "What could it damage, and who may authorise what the agent does to it? ... a stage collision with the pole piece or detectors, the sample, the beam, venting the chamber." No lean was given. |
| N4 | held: M4 item 10: "Is there a stand-in: a simulator, an offline or dry-run mode? If a simulator: does it enforce the instrument's limits, and does it label its output as simulated?" |
| N5 | partly: the owner was asked at step 1 (M4 item 8, "Who owns the SEM?"). The run stopped at requirements round 1, so Release and recording the owner as a persona "described by <who>" were not reached. |
| N6 | held: the tester could name who needs it ("me and the microscopists"), so the playbook went to the requirements interview (M5 item 11, then `/kaizen:requirements`). |
| N7 | held: M2 item 6: "The ledger goes to design/kaizen.md and will be committed. OK?" It was announced before the file was written. Finding 2 (below) is about where the ledger goes, not about the announcement. |
| N8 | not reached: nothing built. |
| N9 | not reached: no debrief. |
| N10 | not held: "Cost before code: never stated". The full path (M6) and the requirements rounds carry no cost figure. This is unchanged and known (ledger 59). |
| N11 | held: M4: "every command to the real SEM is blocked, read-only queries included. Safe meanwhile: building a stand-in, reading documentation." Simulated output labelling is asked in item 10. Whether the build itself labels it was not reached. |
| N12 | held: the tester answered "I don't know" to items 8, 9 and 10. M5: "commands to the SEM stay blocked until the owner answers", and the agent offered to write the questions for the group leader. M9 lists 8, 9 and 10 as "Still open, waiting for the owner". |
| N24 | partly: "stand-in", "ledger" and "walk-throughs" are explained on first use. "My lean" appears in M1 and is explained only in M9. "Pole piece" (M4) is unexplained. M6 uses "hallway test" and "debrief" with short glosses only. |
| N25 | not held: the tester lists unexplained words in the README ("ER-C", "upstream", "trailer", "Ledger: rows", "spec deltas") and in the skills ("frontier", "retcon", "Lastenheft/Pflichtenheft", "ADR", "must-example", "small path"). Four concepts have two names: decision record / design/changes; inbox / Notes for the next debrief; principal / person who needs the solution; stand-in / simulator, dry run. |
| N26 | held: M8 item 15 asked "Does the project or institute use a glossary or ontology for electron-microscopy terms?" at playbook step 7, before any term was defined. The tester called this a good point. |
| N27 | held: items 1 to 19 run in one sequence over M1 to M9, and every item is a bold bullet. M9 restated the open 8, 9 and 10 under their numbers. |
| N28 | held: the quoted messages are 10, 7, 4, 10, 3, 6, 5, 3 and 7 lines long. |
| N29 | not reached: no push or release. |
| N30 | not reached: no debrief. |
| N31 | not reached: no debrief. Update itself asked about message length (M2 item 5) before any message had been seen (finding 4, unchecked). |

## Comparison with the previous run (2026-11-06, `9be3979`)

- Changed:
  - N1 went from held to partly. The README now sends a newcomer to `/kaizen:update` first, which does nothing for the SEM goal.
  - N5 went from held to partly, but the cause is the run, not the plugin. The earlier run reached Release; this one stopped at round 1.
- Same: N2, N3, N4, N6, N7, N11 and N12 held in both runs. N10 was not held in both. N8 and N9 were not reached in both.
- Not comparable: the previous result graded only N1 to N12. N24 to N31 (N26 for this scenario) are graded here for the first time. N26, N27 and N28 held. N24 held partly, and N25 was not held.
- The previous run's new findings, ledger 95 and 96, were not re-tested in this report. One of them is where the blocking question is recorded before `design/` exists. The tester wrote a `design/` directory only after the update, and recorded the block nowhere.

## Setup misfit named by the tester

`version.py --project` read the tester host's real `~/.claude/CLAUDE.md`. Every run therefore reported "a copy in your ~/.claude/CLAUDE.md", and a real newcomer would not see that line. The main session confirmed it: `brief.py` does not isolate HOME. Item 1 of M1 (the "its own copy" question) is therefore an artefact of the host, and the tester's answer "its own copy" was made up. The earlier misfit (no code, so no hallway test or debrief) recurs: N8, N9 and N29 to N31 are not reached.

## New findings, candidates for key items

1. Update has no case for a project without an instruction file (checked: update/SKILL.md speaks only of "the project's existing instruction file"; this is the review finding L8, declined earlier and now hit by two runs). The tester created CLAUDE.md on its own. Candidate key item for all scenarios: for a repository with no instruction file, update says where the block goes (as a new file) before writing it. Related: the update hand-over names no next step, so the playbook is not reached from there (feeds N1).
2. The ledger placement ignores the answer to "Public" (partly checked). ledger.md line 3 says the ledger goes "never into a tree whose committed files are published", which holds. But update step 4 committed `design/kaizen.md` after the answer "may become public". The tester says update does not apply playbook step 3 and that neither text covers "may become". Candidate key item: with an answer of "may become public", the ledger goes where the playbook step 3 places it, or the plugin says what "may become" means. The playbook also asks "public" again without reading the ledger's `Public:` line (unchecked).
3. Playbook step 1, "say so now, in those words" (checked: the wording is in the file): it is unclear whose words. A wording question; no key item needed.
4. Update asks, on a first rollout, whether message length suits the person (M2 item 5) before any message has been seen (unchecked). Candidate to move into N31 (the first debrief asks).
5. The README's hook section talks about ledger rows, the `Ledger:` trailer and `Refs #<n>` before the ledger is explained, and a newcomer stalls there (unchecked). The main session's NOT CONFIRMED claim concerned the order of README sections in another run (small-website, finding 8), not this stall. Candidate for N25.
6. Cost of the full path (an extension of N10, known as ledger 59): the tester suggests a rough minutes or tokens figure per step in playbook step 2.
7. The output "a copy in your ~/.claude/CLAUDE.md" is opaque to a newcomer (the tester's finding 5). Partly an artefact of the setup misfit above.

