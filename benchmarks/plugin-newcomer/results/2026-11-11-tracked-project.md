# Run 2026-11-11: scenario tracked-project, commit `c717975` (0.6.0-dev.3, before the release review's fixes), Opus, about 4 minutes

Pre-test of stage A before the 0.6.0 acceptance; one run (the default since 2026-11-11, ledger 216). Usage: 25,303 output tokens, 27 tool calls. Graded by a fresh Sonnet agent that changed no skill, from the report, the key and the claims the main session checked: update step 5 writes no date for the first look; "about fifteen lines" against one item per line in update step 3; `version.py` writes `.git/info/kaizen-update-noticed` without any text saying so; `record.sh --help` gave only the usage line; field-test step 5 named no path for a participant's brief; neither the field-test skill nor its brief asked the participant's consent to where findings go. All confirmed; findings 2, 6, 7 and 8 are design judgements, not checked.

| Key | This run | Runs 3, 4 (2026-11-09) |
|---|---|---|
| N2 version line silent | held | not graded |
| N7 ledger announced | held (M1 item 4, M5) | not graded |
| N24 terms explained | partly ("debrief" glossed; "lean" not; "owner" in two senses) | not graded |
| N25 plain words in files | not held ("principal", "small path", "decision record's safety row", "text id", "evidence folder") | not graded |
| N27 numbering | held (1 to 41 across M1 to M8, bold labels, no restart) | held, held |
| N28 length | partly (M3 17 lines, the update's list) | held, partly |
| N32 instructions update | partly (line by line, adaptations kept; the `ask-matt` line not named) | held, held |
| N33 tracker setting | held | held, held |
| N34 issues stay on GitHub | held | held, held |
| N35 nothing posted, Closes/Refs | held | held, held |
| N36 waiting reporter | held (#16, #17 named, no draft) | held, held |
| N37 feedback from the tracker | partly ("claudism" entry, no account; pull request 15's remark not taken) | not reached, not reached |
| N38 field-test brief | partly (through the skill now; consent inferred, not asked) | partly, partly |
| N39 layer per finding | not reported (findings labelled by skill) | held, partly |
| N40 records when needed | held | partly, partly |
| N41 branch and pull request | partly (branch; no description offered) | held, held |
| N42 no perceived regression | held ("kept on purpose", recorded) | held, held |
| N43 the update skill | held | held, held |
| N1, N6, N8 to N10, N29 to N31 | not reached or not reported | not graded |

Compared with runs 3 and 4: N37 and N40 better; the field test now runs through its skill. N28 partly again from the same cause (the update's list), N32 and N41 down a step, N39 not reported.

Findings not in the key, all fixed before the acceptance except where a ledger row says otherwise: the participant's consent to where findings go (field-test brief, "Where things go"); a remote participant whose recording arrives only afterwards (row 301); no path for the brief (field-test step 5); the update's first look undated (update step 5); "closed since the project's version" undefined without a version (update step 5); `version.py --project` trusts the version line once present (row 301); the notice file not mentioned (row 301); `record.sh --help` (done).

Setup misfit named by the tester: its own inline Python edit of the ledger against the standing "Edit tool" rule.
