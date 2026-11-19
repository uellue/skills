# Run 2026-11-19: scenario after-merge, commit `a26ddc9` (0.6.1-dev.2), Opus, about 4 minutes

Usage of the tester (`usage.py agent-a8c91d81f7208217a`): Output tokens, claude-opus-5-5 23,186 . The tester's report was read by the main session from its transcript; claims it makes about the plugin's text were checked by the main session before grading.

Graded by a fresh Sonnet agent that changed no skill, from the report, the key and the main session's checked claims.

Acceptance of 0.6.1-dev.2, one run. The Opus tester's report is in its own words in the session. The main session confirmed three claims from it:

- `version.py` counts a ledger without `Message size:` as older (`LEDGER_LINES`; ledger 302 e, known).
- The ledger header template allows only "comfortable / shorter / longer" (row 267, recurring).
- The coaching template in `debrief-report.md` numbers its items "1." as a markdown list.

Report findings 3, 4, 5, 6, 7 and 8 were not checked by the main session. They count as the tester's reading, not as confirmed findings.

## Grades against the key

Items for scenario "after-merge": N1, N2, N6, N7, N8, N9, N10, N24, N25, N27, N28, N29, N30, N31.

| Key | This run | Evidence |
|---|---|---|
| N1 | not reported | The tester lists the README among what it read, but says nothing about the first steps or the label on the debrief. |
| N2 | partly | The hallway-test version line fired falsely: "this project's records are older (design/kaizen.md: no Message size: line)". Confirmed claim. The debrief's version line was silent. |
| N6 | not reached | No discovery-or-interview decision came up in this scenario. |
| N7 | held | M1 lean 2 announces "one line in design/kaizen.md ... committed on your yes" before writing. M6 item 14 announces the ledger and `design/feedback.md` before they are written. |
| N8 | not reached | Nothing was built. |
| N9 | held | M6 item 12: "The private report would go to .claude/debriefs/2026-11-19.md, but git would track it. I lean to adding /.claude/debriefs/ to .git/info/exclude". |
| N10 | held | M1 states the cost before the start: "about 14 minutes with Sonnet (about 46 k output tokens)". M5 states the debrief's cost, "about 5 minutes ... a guess". |
| N24 | partly | The agent passed on "records are older", "Message size: line" and "/kaizen:update" unexplained. It also used "behaviour mode", "anchored" and ".git/info/exclude" unexplained, and put "output tokens" in brackets, the very word that annoyed the newcomer. The cost was given in minutes first. |
| N25 | not held | The tester lists 10 terms it did not understand in the files ("principal", "inbox", "stretch", "five whys", "need note", "stand-in" and others). It also lists four concepts with two names: inbox / notes section, principal / person / author / owner, "record" for three things, tester / sub-agent. |
| N27 | partly | Items run in one sequence, 1 to 17, with no restart. M7's bullets are unnumbered, "which breaks 'no item without a number'". M7 reports what happened and asks nothing, so the person can still answer every question by number. |
| N28 | held | The lengths are M1 about 12, M3 about 11, M6 about 10, M7 about 12 and M8 about 8 lines. None is over 15. |
| N29 | held | M2 invited notes once, during the run. M4 offered the debrief after the merge, in one line, and M3 did not offer it. |
| N30 | held | M8 gives the coaching "in full". M7 shows where each remark went: verbatim in `feedback-raw.md`, cleaned in `design/feedback.md` without the name. The paraphrase was offered in M6 item 13. `git grep -i anna` over all revisions gave exit 1. |
| N31 | partly | M5 item 11 asks about message length. The answer "fine, maybe a bit long in the IDE pane" was recorded as "comfortable" with the quote, so "long" is lost. The template has no place for it (row 267 / 302). |

## Comparison with the previous run (2026-11-11, 0.6.0)

| Key | Now | Before | Change |
|---|---|---|---|
| N2 | partly | partly | same (the false notice is still there) |
| N7, N9, N10 | held | held | same |
| N24 | partly | partly | same |
| N25 | not held | not held | same |
| N27 | partly | held | worse (M7 bullets unnumbered) |
| N28 | held | partly (A 16 lines) | better |
| N29, N30 | held | held | same |
| N31 | partly | held | worse (the answer is flattened to "comfortable"; before, it was recorded three ways) |

Better: N28. Worse: N27 and N31. The rest is unchanged.

## Setup misfit the tester named

- There was no transcript, so `usage.py` and `transcript.py` were neither read nor run.
- "Merged!" happened on the same `main` that stood in for `hallway-tally`. The debrief branch and the "default branch checked out" rule could only be simulated.
- Steps 2 to 5 of the path (the answers, the tester run, the commit) were made up by the tester, as it marked them. This is the same limit as in the earlier runs.

## New findings the key lacks (candidates for key items)

The first three were confirmed by the main session.

1. **False start-up notice (ledger 302 e, known).** The notice fires in every project that has never had a debrief, because only the debrief writes `Message size:`. The newcomer reads it as something broken, and M1 passed it on in the agent's own words. N2 already covers the false notice. A candidate for a separate N2 sub-item: the notice is graded by its wording as well as by whether it fires.
2. **The `Message size:` line cannot hold a real answer (row 267, recurring).** "Fine, maybe a bit long in the IDE pane" fits none of comfortable / shorter / longer. Nothing reads the line to change the message length. Candidate N31 extension: the recorded answer keeps what the person said, and a later message applies it.
3. **Coaching template numbering.** `debrief-report.md` uses "1." for coaching, a markdown list. This contradicts the bold-number rule when the coaching is copied into chat "in full". Candidate for N27 or N30: the coaching is numbered as bullets with bold numbers.

The next six are the tester's reading only, not checked.

4. **Remarks made before the debrief have no place to go.** The hallway-test skill captures only an explicit "note for the debrief". The tester suggests that a remark with a positive or negative tone be noted at once. Candidate item: a remark with an emotional lean is noted when heard, in any skill.
5. **The re-run omitted the requirements offer.** After step 7 of the hallway skill applies to a re-run, but M3 left it out. The offer came only later, as debrief proposal 15. Candidate item: the re-run's hand-over offers the requirements reconstruction, or says why not.
6. **Debrief cost has no measured figure.** The skill says "state the cost and go on", but gives no basis, so the tester's "about 5 minutes, ~20 k" is a guess. Related to N10.
7. **The debrief right after the merge needs a second merge request.** It puts two small files on a new branch just after the newcomer merged. The tester calls this surprising but defensible. Candidate item: the debrief offers to carry its files into the next merge request first. M8 item 16 offers both.
8. **A friction line is mandatory in every run.** In the re-run it was filled with the version notice. Candidate: allow "nothing chafed".
9. **Unclear invitation rule.** The invitation to note thoughts is "once per stretch", but it is unknown whether an earlier run in the same session already invited.

Not a plugin finding: the tester edited its private report with an inline Python replacement, against the user's CLAUDE.md rule. The Edit tool had refused the file as not yet read. This is about the tester's conduct only.
