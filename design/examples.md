# Acceptance examples

One line each: ID, situation and observable outcome, priority, source. Requirements, walk-throughs, decision records, tests and tester briefs cite the IDs; nobody keeps a copy.

- **E1** (must; requirements S3): when a walk-through is invoked and the stakeholder record has no matching persona, then the skill shows the known personas and asks, offering to add one, before walking.
- **E2** (must; requirements 2.5): when `usage.py` runs on a session, then its output tokens equal the sum over distinct API message ids.
- **E3** (must; requirements S4): when a hallway test ends, then its record exists under `design/hallway/` and names, per defect, what would have caught it.
- **E4** (must; requirements S5, 2.9): when a transcript is exported into a directory git would track, then the export is refused and nothing is written.
- **E5** (must; requirements S5): when a session contains messages the person typed while a turn ran, then the rendering shows them as `USER (queued mid-turn)` and the usage counts them, and harness text is never labelled or counted as the person's.
- **E6** (should; requirements S1): when the requirements interview starts on a topic with an existing record, then its first round is drafted from the record and asks only the frontier questions the record does not settle.

From the walk-throughs of 2026-11-05 (`design/walkthroughs/colleague-first-debrief.md`, `design/walkthroughs/maintainer-check-before-release.md`), run by an agent without a person: simulated and unconfirmed by the principal; priorities are the agent's proposal.

- **E7** (should; walk colleague-first-debrief step 3; unconfirmed): when a colleague reads the README only as headings and command blocks (`skim.py README.md`), then the view shows, after the install commands, the command that starts a first debrief.
- **E8** (must; walk colleague-first-debrief steps 4, 5; unconfirmed): when `/kaizen:debrief` is invoked in a fresh session without naming a stretch, then it does not debrief the session it runs in; it shows the project's earlier sessions in a form the person can recognise and says which it will take, or asks.
- **E9** (must; walk colleague-first-debrief step 7; unconfirmed): when the private report's destination would be tracked by git in the person's repository, then the person is told before anything is written, and the coaching is not written where `git add -A` picks it up without their say.
- **E10** (should; walk colleague-first-debrief step 6; unconfirmed): when a debrief would read more than one session, then it states the sessions, their sizes and its expected cost before reading, and waits for the person.
- **E11** (should; walk colleague-first-debrief step 4; unconfirmed): when a bundled script runs on a Python older than it supports, then it stops with one line naming the required version, not a traceback.
- **E12** (must; walk maintainer-check-before-release step 3; unconfirmed): when a skill or reference names a `${CLAUDE_PLUGIN_ROOT}/...` file that does not exist, then `./check.sh` fails and names the file and the path.
- **E13** (should; walk maintainer-check-before-release step 3; unconfirmed): when `./check.sh` runs, then it lists every example in `design/examples.md` that no test or fixture cites.
- **E14** (should; walk maintainer-check-before-release step 4; unconfirmed): when the requirements skill is run against the scripted-principal fixture (testing.md, fixture 3), then the blind grade lists per key item found or not, with the plugin commit and the model, beside the previous run of the same fixture.
- **E15** (should; walk maintainer-check-before-release steps 5, 6; unconfirmed): when a benchmark run is finished, then its result file names the plugin commit, the model, whether the grader was blind, the conditions run and the output tokens, and sits beside the earlier results.
- **E16** (must; walk maintainer-check-before-release step 2; unconfirmed): when the maintainer tries a changed skill by hand in a session, then the session runs the checkout's version and the maintainer can see which version ran.
