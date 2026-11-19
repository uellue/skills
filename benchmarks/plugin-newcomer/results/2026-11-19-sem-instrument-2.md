# Run 2026-11-19 (2): scenario sem-instrument, commit `cc180fe` (0.6.1-dev.2 with the fixes of ledger 315), Opus, about 3 minutes

Usage of the tester (`usage.py agent-abae119ac1b424b76`): Output tokens, claude-opus-5-5 16,326 . Rerun after the fixes of ledger 315 (`cc180fe`); the tester's report was read by the main session from its transcript, and claims it makes about the plugin's text were checked before grading.

Usage of the tester: not given in the report; the main session adds it from `usage.py` if wanted. The tester's report was read by the main session; claims it makes about the plugin's text were checked by the main session before grading, and only those count as findings below.

Graded by a fresh Sonnet agent that changed no skill, from the report, the key and the main session's checked claims.

Result format: E15. The tester wrote its expectations before its first command (13:59:03). Findings marked "unchecked" were not among the claims the main session verified. They are candidates only. All answers to the plugin's questions in the run were made up by the tester, except the vocabulary question.

## Grades

| # | Result |
|---|---|
| N1 | held: the tester typed `/kaizen:update` from the README's "Then, once in each project", and the update hand-over ended "Next: type /kaizen:playbook. It says which step of the work you are at and which skill fits." The playbook was reached from there. Remaining: "First steps" still omits update (finding 4 below, unchecked in this run; the main session confirmed the same omission in the analysis-script run). |
| N2 | held: "`version.py update efa6c3e9`, `playbook 1291422e` and `requirements f920fe4b` were all silent (rc=0)". |
| N3 | held: M4 at playbook step 1, before requirements: "- **7** What could the agent damage, and who may authorise which actions? Kinds to think of: a stage collision, the sample, the beam, venting the chamber." "I give no lean on these". |
| N4 | held: M4 "- **8** Is there a stand-in: a simulator, an offline or dry-run mode from the vendor? If it is a simulator: does it enforce the real microscope's limits, and does it label its output as simulated?" |
| N5 | partly: the owner was asked at step 1 ("- **6** Who owns the SEM, i.e. who may authorise work on it and sets its limits?"). The run stopped at requirements round 1, so Release and recording the owner as a persona "described by <who>" were not reached. M9 does keep "the instrument's owner stays question 6" apart from "who signs off", which is a good sign. |
| N6 | held: the request named the need, so the playbook went to "- **10** Who needs this, and what would they do differently with it?" and then chose the full path and offered the requirements interview (M6 item 11). |
| N7 | held: M2 "I would then start the ledger at design/kaizen.md, committed (the repository is private)... Both go on the branch kaizen-rollout", and M1 "nothing is written before you agree"; the file was written after the "yes". |
| N8 | not reached: nothing built. |
| N9 | not reached: no debrief. |
| N10 | not held: finding 1, "no cost or length is stated for the path before the first line of code"; the tester estimates 20 to 40 exchanges and the plugin says none. Same as before, known (ledger 59). |
| N11 | held: M4 "Until the owner has answered, nothing reaches the real microscope, not even a read-only query. Safe meanwhile: reading documents and building or getting a stand-in." Labelling of simulated output is asked in item 8; the build itself was not reached. |
| N12 | held: the tester answered "I don't know" to the owner and damage questions; the stand-in question was blocked on the same footing. M4 states the block in plain words and M4b offers messages to the facility manager and the vendor ("later", sent to the inbox). |
| N24 | partly: "stand-in", "owner", "ledger" and "walk-throughs" are explained on first use. "lean" is used in M4 ("I give no lean on these") and explained only in M9 ("with my lean, so that 'yes' accepts it"). "decision record" (M7) and "telemetry" (M7) are unexplained. M5b names the hallway test and the debrief with short glosses only. |
| N25 | not held: the tester lists unexplained words in the plugin's files: ER-C, principal, frontier, ledger trailer, `Refs #`, upstream, retcon, Lastenheft/Pflichtenheft, two hats, five whys, the cost of `--scope user`. Two names for one thing: standing instructions / the block / "What you paste for the agent"; inbox / "Notes for the next debrief"; person / principal. |
| N26 | held: M8 "- **15** Does your field or institute use a vocabulary for microscope terms (a community glossary or ontology) that we should use?" at playbook step 7, before any term was defined; the answer was volunteered by the tester ("EM Glossary"), and the requirements skill does not ask again. |
| N27 | held: items 1 to 20 run in one sequence over M1 to M9 (M1 1-3, M2 4, M3 5, M4 6-8, M4b 9, M5 10, M6 11, M7 12-13, M8 14-15, M9 16-20), every item a bold bullet, no restart. |
| N28 | held: the reported lengths are 13, 5, 6, 11, 2, 1, 3, 3, 4, 3 and 8 lines; none above fifteen. |
| N29 | not reached: no push or release. |
| N30 | not reached: no debrief. |
| N31 | not reached: no debrief. The first rollout no longer asks about message length (see N55); M3 says "Waiting: how long my messages should be, asked at the first debrief." |
| N53 | held for the asking, the exclusion untested: M1 "- **1** Does anything happen when a change is committed or pushed here (a deploy, a site), and will committed files be public, now or later?" came before anything was written. The tester answered "Nothing deploys; institute GitLab, private", so the case where the block and the ledger stay out of a published tree was not exercised. |
| N54 | held: M1 "- **2** There is no instruction file yet. Shall I create CLAUDE.md (for Claude Code), or AGENTS.md (if other agents will work here too)?" asked before creating one. |
| N55 | held: M3 ends "Next: type /kaizen:playbook." It offers a merge request description (item 5) but no debrief, and asks nothing about message length (it names the question as deferred to the first debrief). |

## Comparison with the previous run (2026-11-19, `a26ddc9`, before the fixes of ledger 315)

Ledger 315 (a) to (f):

- **(a) held** (asking part): the first rollout now asks what a commit triggers and whether files become public, before writing. Before, the "Public" answer came after or beside the ledger placement and update committed `design/kaizen.md` on "may become public". Untested here: the exclusion from a published tree, since the answer was private. The main session's check of ledger.md line 3 ("never into a tree whose committed files are published") stands.
- **(b) held**: the first rollout asks CLAUDE.md or AGENTS.md (M1 item 2). Before, the tester "created CLAUDE.md on its own" (finding 1, review finding L8).
- **(c) held**: the update hand-over names `/kaizen:playbook`. Before, it named no next step.
- **(d) held**: no debrief is offered in the rollout hand-over.
- **(e) held**: no message-length question in update. Before: "- **5**" in M2 asked it before any message had been seen.
- **(f) held**: the run reported no "a copy in your ~/.claude/CLAUDE.md" line (`--project` printed "no standing instructions and no ledger yet: first rollout"). The main session confirms the rerun briefs ran every plugin script with HOME set to an empty folder. The M1 question about "its own copy" is gone.

Per item:

- Better: N1 (partly, held), because the update hand-over now leads on to the playbook.
- Unchanged, held: N2, N3, N4, N6, N7, N11, N12, N26, N27, N28.
- Unchanged, partly: N5 (the run stops at round 1 again), N24.
- Unchanged, not held: N10, N25.
- Not reached in both: N8, N9, N29, N30, N31.
- New items N53 to N55: all held (N53 the asking only).
- Worse: none.

## Setup misfit named by the tester

The scratch repository has no commit, so `main` is unborn. update's branch rule ("a new one when the project is on its default branch") could not be followed as written: `kaizen-rollout` became the only branch. In addition, the tester edited the ledger with an inline script, which the standing instructions forbid. The HOME misfit of the earlier run is fixed (f). Nothing was built, so N8, N9 and N29 to N31 stay unreachable in this scenario, as before.

## New findings, candidates for key items

None of these was among the claims the main session checked, so all are candidates ("unchecked") unless marked.

1. Update in a repository with no commit (tester finding 2, unchecked): "a new one when the project is on its default branch" assumes a base commit; `main` does not exist afterwards. M3 told the person ("merge the branch or rename it to main"), so the outcome was handled by the agent, but the skill says nothing. Related to, but not the same as, the checked point that update step 6 has no case for an all-uncommitted rollout. Candidate: one line for repositories with no commit.
2. The build block is said but not recorded (tester finding 3, unchecked): playbook step 1 says "say so now, in those words" (checked: the wording is there, and it is unclear whose words), but names no file to record the block in before requirements; the tester put it into the ledger inbox. Candidate: name the destination.
3. The standing instructions are accepted unseen (tester finding 7, unchecked): M2 asks "Take the whole block?" for 19 rules without showing them; the README section is named, but not summarised. Candidate: a three-line summary in the offer.
4. Two first commands (tester finding 4, unchecked here; the omission of update from "First steps" is checked in the analysis-script run): README says to run update once per project, "First steps" starts at the playbook. Partly eased by N1 now holding.
5. "Public?" appears in three places (tester finding 6, unchecked): update's first-rollout bullet, update step 4, and ledger.md ("asking once"). A literal agent may ask twice. M1 asked once in this run.
6. One question, two subjects (tester finding 5, unchecked): update asks what makes a change take effect (about the repository), playbook step 1 asks the same words about the tool and the instrument. A newcomer may answer twice or the wrong one.
7. Debrief offers before any work (tester finding 8, unchecked): the standing instruction "at a kaizen skill's first use in the project" plus update's "the next skill's first use does" means offers after the playbook and after requirements with no work done. The rollout hand-over itself is clean (N55).
8. Cost of the full path (tester finding 1): an extension of N10, known as ledger 59. Candidate: a figure of rounds or minutes in playbook step 2.
9. Commit subject versus the hook (tester finding 9, untested): the tester's commit subject began "Ledger:", which may trigger the hook's warning about a `Ledger:` line git does not read as a trailer. A test of the hook would settle it.
10. Wording: "lean" is used in M4 before it is explained in M9 (feeds N24); the README hook section's terms (`Ledger:` trailer, `Refs #`) stall a newcomer (feeds N25). Not confirmed by the main session: no claim about README section order in this run.

Not counted: nothing from this report is marked NOT CONFIRMED by the main session. The NOT CONFIRMED claim of the small-website run (README hook section before First steps) concerns another run.

