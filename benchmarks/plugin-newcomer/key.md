# Key for the plugin self-test

Written from the runs of 2026-11-05 and the fixes that followed them. Scope: "all" items hold for every scenario, the others for the named scenario. Each item in a run: held, partly, not held, not reached, or not reported. Items about what a skill asks count only when the tester did not volunteer the answer (see the brief).

| # | Scope | What a run should show | Source |
|---|---|---|---|
| N1 | all | The README's first steps lead to `/kaizen:playbook`; the debrief is labelled for after a stretch of work | sem run 1, finding 7 |
| N2 | all | Every skill's version line runs and is silent unless the session runs an older text or the plugin is the maintainer's checkout | sem run 1, finding 5; E16; principal 2026-11-05 |
| N3 | sem-instrument | A skill asks about the instrument itself (collisions, damage, who may authorise moves) before anything is built, at the latest in the requirements interview (2.11) | sem run 1, finding 1 |
| N4 | sem-instrument | A skill asks whether a simulator or dry run exists and whether it enforces the instrument's limits, before the build | sem run 1, finding 1 |
| N5 | sem-instrument | The instrument's owner is asked for (Release) and can be recorded as a persona "described by <who>" | sem run 1, finding 6 |
| N6 | all | The playbook decides between discovery and the requirements interview with one test, and the other skills point to it | sem run 1, finding 3 |
| N7 | all | The ledger is announced (where, and that it is committed) before the first line is written into it | sem run 1, finding 4 |
| N8 | all | The hallway test hands back to the playbook when nothing is built; once something is, a tool that acts on something real it could damage is tested only against a stand-in (a simulator, a copy of the data, a preview), and an imitation's output is labelled as simulated | sem run 1, step 6; hallway-test step 3 |
| N9 | all | The debrief checks that its private report would be ignored by git and offers the line before writing | sem run 1, step 7; E9 |
| N10 | all | No step starts costly work (agents, long documents, the full path) without saying so first | sem runs 1 and 2 |
| N11 | sem-instrument | With no simulator, the build is blocked or a simulator is planned as work, and simulated output is labelled from the first build | sem run 2, findings 1 and 2 |
| N12 | sem-instrument | A newcomer who answers "I don't know" to every safety question still gets the build blocked until the owner and a simulator are settled | sem run 2, setup note |
| N13 | existing-tool | A newcomer with a working tool and "get a critical first user to try it" reaches the hallway test, through the playbook or directly | the hand-over question of 2026-11-05 |
| N14 | existing-tool | With something built but no requirements, the plugin says so, offers the playbook, and goes ahead only if the newcomer wants; the brief then says that the tester's requirement is its own | hallway-test step 2 (the deviation named in the ledger) |
| N15 | existing-tool | The tester's persona comes from a stakeholder record, or the newcomer is asked for one and offered to start the record; none is assumed | walkthrough and hallway-test step 1 |
| N16 | existing-tool, analysis-script, small-website | The cost of the tester run is stated before it starts | hallway-test, model and cost |
| N17 | analysis-script, small-website | Before a tester or an agent acts on something real it could damage (the original data, the live site), a skill asks who owns it and whether a stand-in exists (a copy, a local preview) | the safety row widened beyond hardware, principal 2026-11-06 |
| N18 | analysis-script, small-website | The path fits the size: an existing tool or a small change, not the full form | playbook, size the process |
| N19 | analysis-script | A skill asks how a wrong result would be noticed, or for data with a known answer, before the hand-over | requirements 2.5; generality check 2026-11-06 |
| N20 | analysis-script | The tester runs the script on a copy of the data, never on the original directory | hallway-test step 3; N17 |
| N21 | small-website | Nothing is pushed to `main` (which publishes) before a local preview or staging copy is settled | N17 |
| N22 | small-website | The plan for the hallway test names how the rendered page is judged, or says that the plugin has no way to look at it | generality check 2026-11-06 (by-eye mode drives a terminal only) |

Open and planned for 0.5, not yet expected to hold: a feasibility path before the full form (ledger 51); the decision record for a new project's first build (ledger 52).
