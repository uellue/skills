# Run 2026-11-19: scenario tracked-project, commit `a26ddc9` (0.6.1-dev.2), Opus, about 4 minutes

Usage of the tester (`usage.py agent-aa759e8109fb19980`): Output tokens, claude-opus-5-5 21,987 . The tester's report was read by the main session from its transcript; claims it makes about the plugin's text were checked by the main session before grading.

Graded by a fresh Sonnet agent that changed no skill, from the report, the key and the main session's checked claims.

Acceptance of 0.6.1-dev.2, one run. The report is the Opus tester's own composition: it quotes the agent's messages M0 to M9, and the agent's replies were made up by the tester. Claims the main session checked and found "NOT a leak" or "by design" are not counted as findings.

The run stopped in field-test step 4 to 5. The tester wrote the brief and a runbook stub. It did not do the walk-through, the channel probe, the run or the grading.

## Grades

| Key | Grade | Evidence |
|---|---|---|
| N1 | not reported | The tester read the README but says nothing on whether its first steps lead to the playbook. |
| N2 | held | "The startup version line was silent." `version.py --project` named the old block. The `field-test` call was silent after the update, by design (checked). |
| N6 | not reported | No discovery or requirements-interview decision came up. |
| N7 | held | M1 item 3: "A ledger, design/kaizen.md: a short file about how we work with the agent (not devvm's backlog)". M7 says "new, committed". Both come before anything is written. |
| N8 | not reached | No hallway test. |
| N9 | not reached | No debrief. |
| N10 | partly | Nothing costly was started. The planned walk-through is "a few minutes, no cost stated", and it was not run. |
| N24 | held | The tester says "none left unexplained (ledger, field test and channel probe are explained on first use)". Terms such as "N7" and "hallway report" in M1 and M2 are devvm's own. Not independently checked. |
| N25 | not held | The tester lists "lean", "text id", "small path", "two hats", "principal", "the start", "trailer", "inbox" and "Notes for the next debrief". It also lists "owner" in two senses, which words.md flags. |
| N27 | held | Items 1 to 39 in one sequence. "No message restarts its numbering." |
| N28 | held | The messages run 2, 14, 6, 10, 10, 6, 12, 8, 13 and 9 lines. The longest is 14. |
| N29 | not reached | No push or release. |
| N30 | not reached | No debrief. |
| N31 | not reached | No debrief. |
| N32 | partly | M3 and M4 name the pull request description (10), ambiguous words (12), the debrief offer (15), the review rule (18), the hand-over rule (19) and the dependency lookup (17). The adaptations are kept (CI commands, N7, spec.md). The `ask-matt` line is not named. CLAUDE.md was changed after an "agree". |
| N33 | held | M5 item 23: "I take it from requirements.md (#n) that issues and pull requests are on GitHub. When should I read them?" It asks about reading, posting and public status, and records them in CLAUDE.md under "## Issue tracker". |
| N34 | held | One ledger row, for #16's unclear agent-written README text, with link and one line. #17 gets none. Closed #8 maps to spec.md question 3. "The rest stays in the tracker." |
| N35 | held | M5 item 24: "I'd post nothing unless you ask". `Refs #n` / `Closes #n` is named in M3 item 11. No draft was made, so the people/agents split was not exercised. |
| N36 | held | M6 items 27 and 28 name #16 and #17 as unanswered since 5 and 7 November. "I draft no reply unless you ask." |
| N37 | partly | `design/feedback.md` was created with one line citing #16, no account. #16's praise of the guidance after `./install.sh` was read only in step 5, after step 2 looked for liked wording. The tester kept the devvm-praise remark out (finding 3). PR 15's remark was not reached; no pull requests are open. |
| N38 | partly | The brief and runbook stub were written. M8 item 34 names the layers. M9 items 37 to 39 give the notes channel and ask for the colleague's yes. The tester praises the brief's consent and closing questions. The zsh line may not survive `record.sh` (finding 9), and the participant's own agent and the private repository for the raw recording are not reported. |
| N39 | not reported | The tester ranks findings as gap, bug and so on, but the report does not tie each to the plugin, devvm or the method. |
| N40 | held | M5 item 25 asks `Public:`. M2 item 6 keeps open questions in spec.md and the ledger takes only how we work with the agent. |
| N41 | partly | Branch `kaizen-0.6.1` was created. The pull request text and the plugin version in it were not asked: "I was not asked about the pull request text, which left the PR 'not asked'". |
| N42 | partly | M2 names the hallway report and spec.md open questions as kept on purpose. The guidance after `./install.sh` that the colleague liked is not named before anything would change it (finding 3). |
| N43 | partly | The request came in words, and update has `disable-model-invocation`. The tester assumed M0 "type it on its own line" and the newcomer typing it [made up]. The skill was followed from its file, not started. Recording the applied version is not reported. |
| N51 | partly | M9 item 38: "that yes is theirs", plus item 39 on the committed brief being public. This was asked of the owner, not of the participant, and no filing happened. |
| N52 | not held | M9 item 36 asks "How does it reach us?". No dry run was planned. Finding 10 says it is unclear how `record.sh` reaches a remote laptop. Not yet expected to hold (ledger 301). |

## Comparison with 2026-11-11 (2), 0.6.0

| Key | Now | Before | Change |
|---|---|---|---|
| N2, N7, N33 to N36, N40 | held | held | same |
| N10 | partly | partly | same |
| N24 | held | partly | better (tester's own count of unexplained words; "lean" and "debrief" no longer reached the messages) |
| N25 | not held | not held | same |
| N27 | held | held | same |
| N28 | held (14) | held (14) | same |
| N31 | not reached | partly | not comparable: the run stopped before the debrief |
| N32 | partly | partly | same (`ask-matt` still not named) |
| N37 | partly | partly | same |
| N38 | partly | partly | same |
| N39 | not reported | held, thinly | worse |
| N41 | partly | held | worse: the pull request text was not asked |
| N42 | partly | held | worse: the install.sh praise is read too late to be named |
| N43 | partly | held | worse in form: the tester only assumed the route; before, the newcomer typed it |
| N51, N52 | partly, not held | not in the previous grading | new items |

The N41 to N43 drops may also come from the run being cut short at field-test step 4 to 5, not only from changes in the skills.

## Setup misfit named by the tester

The request in words cannot reach a skill marked `disable-model-invocation`, so update step 1 had to be assumed. This is the open row 302. The old project copy has no line naming `/kaizen:update`, and the README says that asking in words does not start it. The tester ran with the host's real `~/.claude/CLAUDE.md` visible (the main session confirms `version.py --project` reads it, for three other scenarios). This is not reported for this run.

## New findings (candidates for key items)

Confirmed by the main session:
- **Changelog "Before 0.5.5" contradicts update step 1.** The changelog says a block without a version line "takes the sections of 0.5.5 and 0.6.0". The skill says "every section", and a 0.6.1 section now exists. This is a candidate for a wording fix, and the key could check that the applied sections include 0.6.1.
- **Feedback-entry wording is unclear.** The changelog says feedback entries are "created when the first entry comes". Update step 4 says "other records (feedback entries ...) wait". Step 5 says a remark "becomes a feedback entry". The main session finds no contradiction on a careful reading, but the tester read it as one. It could be reworded.

Unchecked, candidates only:
- **Order of steps (tester finding 3).** Update step 2 looks for wording someone said they liked, but #16's praise is read only in step 5. The skill also does not say whether praise of the project, not the agent, becomes a feedback entry. This bears on N37 and N42.
- **One issue with many points (finding 5).** The skill does not say whether #16's six points become one ledger row or several. The tester made one row.
- **Field-test step 3, whose yes counts (finding 8).** "The person may change or waive any of this for their own machine" assumes the owner is the participant. Here the laptop is the colleague's.
- **Brief template and `record.sh` (finding 9, likely bug).** The brief says "`setopt interactivecomments` first in zsh". `record.sh` starts a new shell, so the option may be lost. The skill says only variables carry over.
- **Remote participant (finding 10, second half).** How `record.sh` reaches a remote laptop, and how step 7 ("each session ... exported") applies, is unclear. This ties to N52 and ledger 301.
- **Pull request text not asked (path item 6).** Update step 6 lacks the pull request question, which leaves N41 "not asked". Related to a single commit `b093a42` for update and field-test together, which deviates from step 6.
- **Who may post (finding 12).** Update step 4 asks "who may post", but devvm's requirements already say "The owner pushes and merges from the host". The tester stated it as a lean instead of asking. This is arguably good behaviour.

Dropped:
- `version.py field-test` silent after the update: by design (checked).
- `record.sh --help` showing `~/field-test` with the host's home expanded: the tester host's HOME, not a leak, and a different place from `.claude/field-tests/` by design (checked).
- The three messages for the line-by-line comparison (finding 11): defensible.

Worked well, per the tester: update's "kept on purpose" step, the line-by-line comparison that keeps the project's adaptations, "draft only when asked", the brief's consent and closing questions, and the silent version line.
