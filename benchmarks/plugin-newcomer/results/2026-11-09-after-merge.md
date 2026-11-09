# Run 2026-11-09: scenario after-merge, commit `e9f7853`, Opus, 3.3 minutes, 18.7 k output tokens

Result format: E15. Graded together with `2026-11-09-after-merge-2.md` by a separate Sonnet agent that changed none of the skills, from both reports, the key, the scenario, the previous pair's results, the expected effects of 245 to 251 and the main session's checked claims (9, all confirmed by grep or by inspecting the scratch projects). Rerun after 245 to 251; two runs on one commit (ledger 216).

| # | Result |
|---|---|
| N1 | partly: the playbook link not reported |
| N2 | held: version lines silent |
| N6 | not reached |
| N7 | held: M3 names `design/kaizen.md`; M8 announces the new `design/feedback.md` as committed |
| N8 | not reported |
| N9 | held: M7, check-ignore exit 1, the exclude line offered before any write |
| N10 | held: M2, cost before the run, "Start it?" |
| N24 | not held: "persona", "must-cases", "leans", "ledger" with only its file name, "stretch", ".git/info/exclude" |
| N25 | not held: "stretch", "principal", "need note", "small path", "record" for three documents, "brief" against "instructions" |
| N27 | held |
| N28 | held: the final reply in two messages of 14 and 6 lines |
| N29 | held: M3 invites once; M4, M5 after the merge (offered twice, see findings) |
| N30 | held: the coaching in full, each remark traced; M8 offers the paraphrase; verbatim only in the private file |

Expected effects: 245, 246, 247, 248, 249, 250, 251 held. Compared with the previous pair: 242 and 243 now held. Noise against run 2: N24 (not held / partly), N28 (held / partly), 247 (held / partly). Findings: ledger 252 to 258.

Setup misfit the tester named: the fixes given on `main` standing for `hallway-tally`, so it created the branch and simulated the merge as a fast-forward; it appended one ledger line with sed (its slip, not the plugin's).
