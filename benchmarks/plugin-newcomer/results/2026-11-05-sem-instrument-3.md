# Run 2026-11-05 (3): scenario sem-instrument, commit `ec3b4b9`, Opus, 11,845 output tokens, 2.2 minutes

Result format: E15. The first run with the current brief: the plugin named as the subject, the scenario as input, the tester reading an untracked copy of the README and the plugin (so the version line behaves as in an installed copy). Graded by the main session that had changed the skills (not blind); the report's claims about the plugin's text were checked with a grep each (one quote was located in the playbook, not in `change-record.md` as the tester said; the finding stands).

| # | Result |
|---|---|
| N1 | held |
| N2 | held: silent in all three skills |
| N3 | held: 2.11 asked about collisions, damage and who authorises, without the tester volunteering it; no recommended answer was given |
| N4 | held: the playbook asked about a simulator at session start (step 6), 2.3 again with "does it enforce the limits" |
| N5 | held: the playbook asked for the owner at session start; Release again |
| N6 | held: the one test routed to the requirements interview |
| N7 | not reported |
| N8 | not reached: nothing built |
| N9 | not reached |
| N10 | not held: the full path (every section, walk-throughs, decision record) starts without a cost or time estimate; the prior-art sub-agent too |
| N11 | partly: with no simulator, building one is planned work with the right must-examples; but its "enforces the limits" example depends on limits nobody knows yet, and that is not flagged |
| N12 | partly: "I don't know" to every safety question is recorded as open, but the real instrument is only softly blocked: the decision record allows "the real instrument with the owner's agreement", and nothing stops the principal from accepting that as an assumption |

Compared with run 2 (`376c18a`): N2 now held (the copy is silent); N4 and N5 now asked at session start, not only in the interview; N11 and N12 reached for the first time, both partly. N10 still not held.

New findings (ledger 70 to 74): the real instrument only after the owner's recorded agreement, never as an assumption; the simulator's limits come from the owner or the vendor and its limit example stays blocked until they are on record; playbook step 6 asks the person (not "name"), comes first, and records an unknown as a question that blocks real-instrument work; the owner's questions can be sent at once, in parallel with the interview; the measured walk-through's fallback when neither simulator nor dry run exists. Also: no cost for the full path (with ledger 59, planned for 0.5).

Setup misfit (tester): with no code, the build and the hallway test are only read about, never run.
