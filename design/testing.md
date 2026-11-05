# Testing the skills

Status 2026-11-05: `./check.sh` runs the script tests on synthetic transcripts, the pre-push hook's tests and a lint of the skill texts, and reports which examples no test covers, from the pre-commit hook and CI; one benchmark exists (below). The skills' behaviour is not yet tested automatically. The question from the principal was whether skills can have unit tests at all. They can be tested the way the first week tested everything else: a fresh agent, a pre-written key, a blind grader, and a measurement.

## What a test of a skill looks like

A skill is a procedure an agent follows; its test is a run of that procedure by a fresh agent on a fixture, graded against reference findings written before the run; the result shows how a change in the skill changes the output, it does not prove the skill right. Three fixtures cover the plugin:

1. **Debrief.** Two or three small transcripts (rendered or JSONL) with planted moments: a blocking question that waited an hour, a slash command typed inside a message, a decision deferred and dropped, a "clean" reported from the wrong command, a hallway record never committed. Key: the findings a good debrief must contain, with the L-markers. Grader: did the report cite each planted moment, and did it invent any? `usage.py` has its own check: the output tokens of a fixture equal the sum over distinct message ids (a fixture with three lines per message, written by hand).
2. **Hallway test.** A toy command-line tool (a hundred lines) with planted defects: an option order that contradicts its help, a silent failure on a missing input, an error on stderr with exit 0, output that scrolls off in forty rows. Key: the defects. Grader: found or not; expectations file written before the first run (check the timestamps); report returned as the final message.
3. **Requirements and walk-through.** A scripted principal (a sub-agent given a persona and a set of facts it may reveal when asked, with one need hidden behind a solution and one number it only gives when pressed). Key: the need behind the solution, the number, the deferred item recorded with stage and owner, the handover list of unconfirmed items. For the walk-through: the fixture's stakeholder record lacks the persona; the key says the skill must ask before walking.

Order of building (principal, 2026-11-05): the debrief's fixture first, as the most frequent use; then the scripted principal; then the toy CLI.

The first fixture exists: `benchmarks/notes-tags/` (a toy notes CLI and a change request, taken through the kaizen skills alone, OpenSpec alone and both; a reference key and the baseline of 2026-11-05). Like every fixture here, it shows how a change in the skills changes the output; it does not certify them. Real-world use, through the debriefs and the ledger, is authoritative.

Each run is graded blind by an agent that did not run the skill, as in the instruction-file eval of 2026-11-04; the usage per run is recorded so that a change in a skill's cost is visible.

## The harness's own mechanism

Claude Code has a plugin evaluation command (`claude plugin eval`: eval suites per plugin with a JSON report, a sandbox, usable in CI). Its exact format was not checked when this plan was written; the maintainer checks it before building the fixtures, and uses it if it fits, so that the suite runs in CI on every change to a skill. Until then the fixtures live under `benchmarks/` in this repository and are run by hand with a sub-agent per fixture.

## What is not tested this way

Whether a skill helps a real project: that is the debrief's job, through the ledger's skill-friction lines and the "used, by hand, missed" table.
