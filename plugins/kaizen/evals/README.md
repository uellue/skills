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

## What eval cannot reach

Runs load only the plugin: no CLAUDE.md, user settings, memory or other plugins. The standing instructions are outside this tool; their coverage needs another one (the backtrace of ledger row 218). There are no custom-code graders.

## Coverage: grader to rule

Each grader file is named after the rule it checks in `skills/walkthrough/SKILL.md`.

| Case | Grader | Rule (SKILL.md line) | Kind |
|---|---|---|---|
| asks-for-persona | skill-fired | description (3): "walk me through" triggers it | indicator, not scored |
| asks-for-persona | inputs-1-reads-stakeholder-record | Inputs 1 (22): read `design/stakeholders.md` | free |
| asks-for-persona | inputs-1-asks-persona-before-walking | Inputs 1 (22): do not walk in a persona nobody confirmed; show the personas, ask | judge |
| asks-for-persona | messages-about-fifteen-lines | plain words (12): about fifteen lines per message; fails at 20 lines or more | free |
| walks-confirmed-persona | skill-fired | description (3) | indicator, not scored |
| walks-confirmed-persona | output-walk-file-with-template | Output (49 to 60): `design/walkthroughs/<persona>-<process>.md` with Steps and Questions for the principal | free |
| walks-confirmed-persona | output-examples-in-examples-md | Output (49): examples go to `design/examples.md` with the next free ID (E2) | free; reads the file after the run, so Edit and Write both count |
| walks-confirmed-persona | walk-records-questions-not-inventions | The walk (32 on): do not invent the answer; record a question | judge |
| ignores-unrelated-request | skill-not-fired | description (3): does not trigger on a plain edit | scored in both arms |
| ignores-unrelated-request | edit-done | the task itself, so the case has a score in both arms | free |

Not covered yet: the questionnaire step, the two hats, the measured walk, the small path, numbering within a message, the text-id line (needs Bash), the friction line. The line numbers drift with edits to the skill; the rule names do not.

The fixture script is copied into each case, since a scaffold script must sit in its case's directory; change all copies together.
