# Eval suite of the kaizen plugin

First experiment of ledger row 214 (`design/requirements.md`, topic 204, decision 1): a coverage table for one skill, `walkthrough`, with `claude plugin eval`. Documentation: https://code.claude.com/docs/en/plugin-evals.md and `claude plugin eval --help` (Claude Code 2.1.269 or later; checked with 2.1.319).

## Run

From `plugins/kaizen/`:

    # graders first: one run per case, no baseline, local report, a cost ceiling
    claude plugin eval . --scaffold --allow-tools Write Edit --runs 1 --ablation none --no-publish --max-cost-usd 3
    # one case
    claude plugin eval . --case walkthrough-asks-for-persona --scaffold --runs 1 --ablation none --no-publish
    # the comparison: three runs per case, with and without the plugin
    claude plugin eval . --scaffold --allow-tools Write Edit --no-publish --max-cost-usd 10

- `--scaffold` runs each case's `fixture.sh` (a tiny tool `tally` with a stakeholder record); without it the workspace is empty and most graders fail.
- `--allow-tools Write Edit` is needed by `walks-confirmed-persona` (writes the walk) and `ignores-unrelated-request` (edits a file); runs never ask for permission.
- `--no-publish`: by default the HTML report is published to claude.ai; keep it local until we decide otherwise.
- `--model` pins the agent's model (for a Fable against Opus comparison); `--judge-model` the `llm` graders' judge (default haiku).
- Results go to `evals/results/<timestamp>/` (ignored by git): `aggregate-result.json` and `report.html`.

First run (2026-11-07, one run per case, no baseline, default model, judge haiku): $0.59 and 113 s for the three cases ($0.14, $0.08, $0.36). The full comparison (three runs, two arms) is about six times that, roughly $3.50 by that figure; the cost is a list-price estimate, not plan usage. That run's one failure was the grader: the agent wrote E2 to E8 into `design/examples.md`, but not with Edit, so the grader now reads the file.

First comparison (2026-11-07, three runs per arm, 18 runs, 676 s, $3.02): every with-arm run scored 1.00; without the plugin, asks-for-persona 0.33 (it walked at once, in a long message), walks-confirmed-persona 0.33 (no walk-through file, no examples), ignores-unrelated-request 1.00 by design. Every grader gave the same verdict in all three runs of an arm. Two graders passed in both arms, so their rules are what Claude does anyway in that situation: reading the stakeholder record, and recording questions instead of inventing answers. The with-arm never failed, so the suite does not yet find a weakness of the skill; that needs harder situations (no stakeholder record, a vague answer, the small path).

## What eval cannot reach

Runs load only the plugin: no CLAUDE.md, user settings, memory or other plugins. The standing instructions are outside this tool; their coverage needs another one (the backtrace of ledger row 218). There are no custom-code graders.

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

`triggers/` (ledger 223): 16 short prompts on the same fixture, each checked for which kaizen skill starts, if any; the expected skill and the expected effect, written before the first run, are in each case's `description`. Two cases depend on the project's state (principal, 2026-11-07): early in design, "what would a new colleague run into" should start the walk-through; nearly done with a persona, the hallway test; offering both and asking is also right, so a judge grades those two. "What should we do next" is tested only in a defined situation (just after a merge), since in general the answer depends on the session. New prompts come from real use. A skill cannot start without the plugin, so run them with one arm:

    claude plugin eval . --tag trigger --scaffold --ablation none --no-publish --max-cost-usd 10

The fixture script is copied into each case, since a scaffold script must sit in its case's directory; `tests/test_evals.py` fails when the copies differ.
