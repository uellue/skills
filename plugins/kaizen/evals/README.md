# Eval suite of the kaizen plugin

First experiment of ledger row 214 (`design/requirements.md`, topic 204, decision 1): a coverage table for one skill, `walkthrough`, with `claude plugin eval`. Documentation: https://code.claude.com/docs/en/plugin-evals.md and `claude plugin eval --help` (Claude Code 2.1.269 or later; checked with 2.1.319).

## Run

This is the one place that says how to run the suites. From the repository root; each command writes its results and its log into a new folder under `plugins/kaizen/evals/results/` (ignored by git), so an agent can read them without copying output:

    # the trigger table (triggers/): one arm, since no kaizen skill can start without the plugin
    out=plugins/kaizen/evals/results/$(date +%Y%m%d-%H%M%S)-triggers; mkdir -p "$out"
    PATH="/usr/bin:$PATH" claude plugin eval plugins/kaizen --tag trigger --scaffold --ablation none --no-publish -j 3 --max-cost-usd 15 --output-dir "$out" 2>&1 | tee "$out/run.log"

    # the walkthrough comparison (walkthrough/): three runs per case, with and without the plugin
    out=plugins/kaizen/evals/results/$(date +%Y%m%d-%H%M%S)-walkthrough; mkdir -p "$out"
    PATH="/usr/bin:$PATH" claude plugin eval plugins/kaizen --case 'walkthrough-*' --scaffold --allow-tools Write Edit --no-publish -j 3 --max-cost-usd 6 --output-dir "$out" 2>&1 | tee "$out/run.log"

    # the update notice (update/): Bash for the start-up line
    out=plugins/kaizen/evals/results/$(date +%Y%m%d-%H%M%S)-update; mkdir -p "$out"
    PATH="/usr/bin:$PATH" claude plugin eval plugins/kaizen --case 'update-*' --scaffold --allow-tools Bash --runs 1 --ablation none --no-publish -j 2 --max-cost-usd 2 --output-dir "$out" 2>&1 | tee "$out/run.log"

    # the sync reproducer (sync/): Bash for git, Write and Edit to see whether drafts are written; a sonnet judge
    out=plugins/kaizen/evals/results/$(date +%Y%m%d-%H%M%S)-sync; mkdir -p "$out"
    PATH="/usr/bin:$PATH" claude plugin eval plugins/kaizen --case 'sync-*' --scaffold --allow-tools Bash Write Edit --runs 5 --ablation none --no-publish -j 5 --max-cost-usd 4 --judge-model sonnet --output-dir "$out" 2>&1 | tee "$out/run.log"

    # the debrief reproducer (debrief/): a debrief of an exported session, Bash for the scripts
    out=plugins/kaizen/evals/results/$(date +%Y%m%d-%H%M%S)-debrief; mkdir -p "$out"
    PATH="/usr/bin:$PATH" claude plugin eval plugins/kaizen --case 'debrief-*' --scaffold --allow-tools Bash Write Edit --runs 8 --ablation none --no-publish -j 4 --max-cost-usd 8 --judge-model sonnet --output-dir "$out" 2>&1 | tee "$out/run.log"

    # an older plugin version, e.g. the one a field test ran (run 8: 1f231b7): a worktree, the cases copied in
    #   git worktree add --detach <scratch>/kaizen-old 1f231b7; cp -a plugins/kaizen/evals/sync <scratch>/kaizen-old/plugins/kaizen/evals/
    #   then run the command from <scratch>/kaizen-old

    # one case, while writing or fixing its graders: one run, no comparison; add --keep-temp to look into a failure
    out=plugins/kaizen/evals/results/$(date +%Y%m%d-%H%M%S)-<case>; mkdir -p "$out"
    PATH="/usr/bin:$PATH" claude plugin eval plugins/kaizen --case <case> --scaffold --allow-tools Write Edit --runs 1 --ablation none --no-publish --max-cost-usd 2 --output-dir "$out" 2>&1 | tee "$out/run.log"

- A full run takes several minutes: the time to note thoughts for the debrief ("note for the debrief: …"). When it is the final acceptance test of a release, the debrief follows the push and the merge, and its proposals go into the next release (ledger 230).
- Cost ceilings are about 1.5 times the last full run ($10.01 for the triggers, $3.02 for the comparison). A ceiling never stops a run in progress, only the start of the next one, so it guards against a runaway (a skill looping to its turn limit), not against a normal run that costs a little more.
- `--keep-temp` keeps each run's sandbox with its full trace; it is sealed and needs `chmod` to read. The results file already holds the trace a judge saw, so keep it for one case whose failure the results do not explain.
- `--scaffold` runs each case's `fixture.sh` (a tiny tool `tally` with a stakeholder record); without it the workspace is empty and most graders fail.
- `--allow-tools Write Edit` is needed by `walks-confirmed-persona` (writes the walk) and `ignores-unrelated-request` (edits a file); runs never ask for permission.
- `--no-publish`: by default the HTML report is published to claude.ai; keep it local until we decide otherwise.
- `--model` pins the agent's model (for a Fable against Opus comparison); `--judge-model` the `llm` graders' judge (default haiku).
- Each results folder holds `aggregate-result.json` (every grader's verdict, the judge's votes and the trace it saw), `report.html` and `run.log`.

First run (2026-11-07, one run per case, no baseline, default model, judge haiku): $0.59 and 113 s for the three cases ($0.14, $0.08, $0.36). The full comparison (three runs, two arms) is about six times that, roughly $3.50 by that figure; the cost is a list-price estimate, not plan usage. That run's one failure was the grader: the agent wrote E2 to E8 into `design/examples.md`, but not with Edit, so the grader now reads the file.

First comparison (2026-11-07, three runs per arm, 18 runs, 676 s, $3.02): every with-arm run scored 1.00; without the plugin, asks-for-persona 0.33 (it walked at once, in a long message), walks-confirmed-persona 0.33 (no walk-through file, no examples), ignores-unrelated-request 1.00 by design. Every grader gave the same verdict in all three runs of an arm. Two graders passed in both arms, so their rules are what Claude does anyway in that situation: reading the stakeholder record, and recording questions instead of inventing answers. The with-arm never failed, so the suite does not yet find a weakness of the skill; that needs harder situations (no stakeholder record, a vague answer, the small path).

## What eval cannot reach

Runs load only the plugin: no CLAUDE.md, user settings, memory or other plugins.

The sandbox keeps the caller's PATH but hides the home directory (checked 2026-11-09 with the probe below and `--keep-temp`). Where the first `python3` on PATH lives under the home directory (miniforge, conda, pyenv, a virtual environment), it starts and cannot find its standard library: "Fatal Python error: Failed to import encodings module". Then no skill's start-up line (`scripts/version.py`) runs, silently, since the skills say "if it fails, carry on". So every command above runs with the system's Python first: prefix it with `PATH="/usr/bin:$PATH"`. The case `probe-python-in-sandbox` (`probes/`) tests the sandbox itself, not a skill: it prints PATH, HOME and each `python3` with whether it finds its library, and passes when `/usr/bin/python3` does; run it on a new machine or a new Claude Code version, with `--keep-temp` to read its output in the trace (the report shows only the prompt).

Rerun with the prefix (2026-11-09, so that the start-up lines run for the first time in an eval): the trigger table 16 of 16 at 1.00 ($8.58, 433 s), the walkthrough comparison unchanged (with the plugin 1.00 in all three cases, without 0.33, 1.00, 0.33; $3.04, 237 s); the earlier results stand.

The cases in `update/` (ledger 280) check the notice the start-up line prints when a project's records are older: one names `/kaizen:update`, one stays silent; both pass with the PATH prefix (2026-11-09, one run each, $0.30) and failed for the instrument without it. The standing instructions are outside this tool; their coverage needs another one (the backtrace of ledger row 218). There are no custom-code graders.

## Coverage: grader to rule

Each grader file is named after the rule it checks in `skills/walkthrough/SKILL.md`.

| Case | Grader | Rule (SKILL.md line) | Kind |
|---|---|---|---|
| asks-for-persona | skill-fired | description (3): "walk me through" triggers it | indicator in a run with baseline; scored with `--ablation none` |
| asks-for-persona | inputs-1-reads-stakeholder-record | Inputs 1 (22): read `design/stakeholders.md` | free |
| asks-for-persona | inputs-1-asks-persona-before-walking | Inputs 1 (22): do not walk in a persona nobody confirmed; show the personas, ask | judge |
| asks-for-persona | messages-about-fifteen-lines | plain words (12): about fifteen lines per message; fails at 21 lines or more (20 line breaks) | free |
| walks-confirmed-persona | skill-fired | description (3) | indicator in a run with baseline; scored with `--ablation none` |
| walks-confirmed-persona | output-walk-file-with-template | Output (49 to 60): `design/walkthroughs/<persona>-<process>.md` with Steps and Questions for the principal | free |
| walks-confirmed-persona | output-examples-in-examples-md | Output (49): examples go to `design/examples.md` with the next free ID (E2) | free; reads the file after the run, so Edit and Write both count |
| walks-confirmed-persona | walk-records-questions-not-inventions | The walk (32 on): do not invent the answer; record a question | judge |
| ignores-unrelated-request | skill-not-fired | description (3): does not trigger on a plain edit | scored in both arms |
| ignores-unrelated-request | edit-done | the task itself, so the case has a score in both arms | free |

Not covered yet: the questionnaire step, the two hats, the measured walk, the small path, numbering within a message, the text-id line (needs Bash), the friction line. The line numbers drift with edits to the skill; the rule names do not.

## Triggers: which prompt starts which skill

`triggers/` (ledger 223): 16 short prompts on the same fixture, each checked for which kaizen skill starts, if any; the expected skill and the expected effect, written before the first run, are in each case's `description`. Two cases depend on the project's state (principal, 2026-11-07): early in design, "what would a new colleague run into" should start the walk-through; nearly done with a persona, the hallway test; offering both and asking is also right, so a judge grades those two. "What should we do next" is tested only in a defined situation, since in general the answer depends on the session: just after a merge, a debrief is offered, by the debrief itself or by the playbook (principal, 2026-11-07), also judged. New prompts come from real use. Run them with the trigger command under "Run".

First run (2026-11-07, 48 runs, 650 s, $10.01, more than the $5 to $8 estimated: the skills ran on for up to 12 turns): 14 of 16 cases passed 3 of 3, as expected. `after-merge-offers-debrief` passed 2 of 3 (expected 1 of 3): the playbook started every time and offered the debrief in two. `state-nearly-done` passed 0 of 3 (expected 2 of 3): the walk-through started every time, never the hallway test, and it never asked; nothing in the hallway test's description says "nearly done, smoothing out rough edges".

Expected effects of ledger 224 and the description changes (written before the rerun, 2026-11-07): the playbook says to offer the debrief first when a piece of work has just ended, so `after-merge-offers-debrief` passes 3 of 3 (medium-high); the hallway test's description now names the state, so `state-nearly-done` passes at least 2 of 3 (medium); the trimmed hallway-test and debrief descriptions still start their skills in their cases, 3 of 3 each (medium-high); the other cases unchanged.

Rerun at 0.5.3 (2026-11-07, 48 runs, 437 s, $8.57, no run errors): 16 of 16 cases passed 3 of 3; every expected effect held. `after-merge-offers-debrief`: the playbook started and offered the debrief in all three runs; `state-nearly-done`: the hallway test started in all three.

The fixture script is copied into each case, since a scaffold script must sit in its case's directory; `tests/test_evals.py` fails when the copies differ.

## Sync: reproducers from field-test run 8

`sync/answers-not-drafts` (ledger 291; field-test run 8, 2026-11-10): the owner types `/kaizen:sync` on devvm one day after the update (the fixture of the self-test's `tracked-sync`, embedded in `fixture.sh`), with issue 16 from another person unanswered, and drops an idea in passing ("a glossary"). Expected, in the principal's words: no drafted replies to people on the tracker unless asked, "point out where an answer from me is needed"; the dropped idea lands in the ledger's inbox at once. Written first and run against the plugin as installed in run 8 (commit `1f231b7`, a worktree with this folder copied in), where it must fail:

With the graders as they stand (five runs each, sonnet judge, results `20261110-082239-sync-run8` and `20261110-082242-sync-dev2`):

| Grader | run-8 version | 0.6.0-dev.2 |
|---|---|---|
| no-reply-drafts (judge) | failed 3 of 5 | passed 5 of 5 |
| idea-in-inbox (the ledger file) | failed 4 of 5 | passed 5 of 5 |
| no-drafts-written, -edit, -bash (nothing written to `.claude/drafts/`) | passed 5 of 5 | passed 5 of 5 |

How the graders got there, since each change was checked on both versions: the first fixture lacked "who runs commands" in the tracker setting, so the sync stopped at that question in all runs and never reached the drafts (results `075053`); the setting was added, as devvm's had it in run 8. A judge of the first reply's plain words failed both versions in every run, so it measured the judge and was dropped. The drafts judge then failed the run-8 version 11 of 11, but in 2 of those the reply only repeated the project's setting ("drafts go to `.claude/drafts/` first"), and once it failed 0.6.0-dev.2 for offering the body of a new issue the owner would open; the grader now says that neither counts, which lets 2 of 5 run-8 runs pass. Earlier drafts of 0.6.0-dev.2 passed only 2 of 3, by routing an inbox note as "a comment on #16", which answers a person too; the inbox step now names that case.

No drafts were written in either version: the run-8 version offered them, which is what the person objected to; the guards stay, the Bash one matching only writes (`>` or `tee` into the folder), since the sync may check that git ignores it. Not reproducible in one turn, so not in this suite: the restart of numbering across messages (a prompt has to state the open numbers, and stating them prevents the restart: the run-8 version continued at 5 in 6 of 6), and the plain words of the "Out" list, which the sync reaches only after an answer. Both are measured on real sessions instead: `transcript.py messages <session>` (ledger 209) lists each reply's numbers and length, and found 12 restarts in run 8's update and sync session.

## Debrief: reproducers from field-test run 8

`debrief/routes-inbox` (field-test run 8, regrade of 2026-11-10): a debrief of one session exported into the checkout (`transcript.py locate` finds `.claude/transcripts/`, so the sandbox's hidden home does not matter), with the person away ("put your questions at the end", which the skill allows). The ledger's inbox holds a project idea never routed; in the session the person said "Note for upstream plugin: …". Expected: the debrief proposes a destination for the note, and offers the upstream issue as a numbered question. In run 8 both failed.

| Grader | run-8 version (8 runs) | 0.6.0-dev.2 (8 runs) |
|---|---|---|
| routes-inbox-note (judge, sonnet) | failed 1 of 8 | passed 8 of 8 |
| offers-upstream-issue (judge, sonnet) | failed 3 of 8 | passed 8 of 8 |

The reproducer is weak: the run-8 version fails it only sometimes, while in the real run 8, a long session with many open items, both failed. A small fixture is easier than real work; the field test remains the stronger check (principal, 2026-11-10: "that's an issue to keep an eye on").
