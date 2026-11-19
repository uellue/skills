# Run 2026-11-19: scenario existing-tool, commit `a26ddc9` (0.6.1-dev.2), Opus, about 3 minutes

Usage of the tester (`usage.py agent-a461d3110edfe77e3`): Output tokens, claude-opus-5-5 17,508 . The tester's report was read by the main session from its transcript; claims it makes about the plugin's text were checked by the main session before grading.

Graded by a fresh Sonnet agent that changed no skill, from the report, the key and the main session's checked claims.

Acceptance of 0.6.1-dev.2, one run. The Opus tester stopped at the hand-over to the real tester (after message 4, "Start?"). Items about what the tester's own run shows were therefore not reached, and N14's "the brief then says" is judged from message 1 and the plugin's text. The previous result is `2026-11-11-existing-tool.md` (0.6.0). Ceiling for the selftest stretch: $50 (principal, item 47).

## Grades

| Key | This run | Previous (2026-11-11) | Evidence from the report |
|---|---|---|---|
| N1 | partly | partly | The README's "First steps" line ("a tool that already works, before others use it: a fresh first user tries it") matches the request. The first steps list the skills from `/kaizen:playbook`, and `/kaizen:update` sits under Install (checked claim, analysis-script run). The debrief label is not reported. |
| N2 | held | held | "The start-up version line printed nothing and exited 0." |
| N6 | not reported | not listed | The tester read the playbook, but the report says nothing about its discovery-versus-interview test. |
| N7 | held | held | Message 3, item 13: "design/kaizen.md, a short 'ledger' ... Committed too, marked 'not public'. Fine?" This comes before any line is written. |
| N8 | partly | partly | Nothing is handed back to the playbook, and the tool reads only. The copy-and-scratch rule held ("runs a copy of tally.py in a scratch folder ... with copies of logs/"). Labelling of constructed logs as simulated is not reported. |
| N9 | not reached | not listed | No debrief in this run. |
| N10 | held | held | The cost comes before any start: message 4 ends "Start?". |
| N13 | held | held | The README line led straight to `/kaizen:hallway-test` ("the description matches"). |
| N14 | partly | partly | Message 1: "There are no written requirements, so the tester's expectations come from the README alone; where it has to invent one, it is testing its own invention." The tester notes it was "Not asked ... any offer of the playbook". Item 7's "playbook not yet run" gives the agent nothing to go on. |
| N15 | held | held | Message 2, item 6: persona "as you described them ... marked 'described by you, not interviewed'". The agent asked first (item 1) and offered to start `design/stakeholders.md`. |
| N16 | held | held | Item 14: "about 46 k output tokens ... on Opus it is a guess, around 15 to 20 minutes. Start?" There is no money figure and no ceiling (see findings). |
| N23 | held | held | Message 1 opens "I read 'test' as a hallway test ... Not automated tests of the code; say if you meant those." |
| N24 | partly | partly | Unexplained on first use: "persona", "scratch folder", "output tokens", "Opus/Sonnet", "branch", "leans", "brief", "behaviour test". "Ledger" and "debrief" are explained. |
| N25 | not held | not held | The tester lists trailer, `Ledger:` trailer, eval, judges, OpenSpec, principal, need note, stand-in and others. words.md misses trailer, eval and OpenSpec. It also lists concepts with two names (tester, sub-agent, fresh agent, first user; walkthrough, walk-through; ledger, `kaizen.md`, inbox; person, principal). |
| N27 | held | held | Items 1 to 14 run in one sequence over four messages. The "Message 2" block of leans is numbered 6 to 11, with no restart. |
| N28 | held | partly (M2 20 lines) | Messages of 9, 10, 4 and 3 lines. |
| N29 | not reached | not listed | The run stopped before the long run. Message 4 has no invitation to note thoughts for the debrief, but the run had not started. |
| N30, N31 | not reached | not listed | No debrief in this run. |

## Comparison with 2026-11-11

- Better: N28 (partly to held). The block of leans is down from 20 to 10 lines, and every message is 15 lines or fewer.
- Same: N1, N8, N14, N24 (all partly), N25 (not held), and N2, N7, N10, N13, N15, N16, N23, N27 (all held).
- Worse: none.
- N6, N9, N29, N30 and N31 were not listed in the previous result, so there is nothing to compare. All five were not reached or not reported here.
- The cost in "minutes" with a Sonnet-only measurement (row 302) is unchanged. It still gives no money figure and no ceiling.

## Setup misfit

`version.py --project` read the host's real `~/.claude/CLAUDE.md`. It reported "a copy in your ~/.claude/CLAUDE.md", which a real newcomer would not have. The main session checked this: `brief.py` does not isolate HOME, and the same misfit hit three runs. Also, the tester made up answers 1, 4 and 5 ("[made up]"), which is allowed by the brief.

## New findings the key lacks

Findings 1 to 3 rest on claims the main session checked. 4 and 5 are the tester's own and unchecked.

- **1** Candidate item (existing-tool): skipping `/kaizen:update` goes unnoticed. In a project with neither standing instructions nor a ledger, `version.py hallway-test` is silent. The session then runs without the $20 ceiling and the rule on ambiguous words. The update skill's first-rollout paragraph speaks only of "the project's existing instruction file" (checked, review finding L8, now hit by two runs).
- **2** Candidate item (existing-tool, N16 widened): the cost is stated in money against a ceiling, and a ceiling is asked for when none is on record. Item 9 says "against their limit, if they gave one" (checked), but nothing asks for that limit. The figure was measured only on Sonnet (unchecked).
- **3** Candidate item: a one-off test's footprint is proportionate. The tester counts a branch, a stakeholder record, a brief, the record, a re-run script and a new ledger for a 25-line read-only tool. The ledger was announced (N7 held), and ledger.md line 3 holds ("never into a tree whose committed files are published"). The open question is whether to ask before starting a ledger that will hold one friction line.
- **4** Availability is asked before the duration is known. The first message asks "who answers during the run", and the duration comes only in item 9 (unchecked).
- **5** Two overlapping question lists in hallway-test "Before launching": a general ordering rule and a first-message list for an existing tool. Item 7 also sends the agent into another skill mid-flow ("the playbook's step 3") (unchecked).
- **6** Setup: `brief.py` should isolate HOME so that `version.py --project` sees a clean host (checked).
