# Benchmark: tags and search for a shared notes tool

A small, fixed change request on a toy command-line tool, taken through the kaizen skills alone, OpenSpec alone, and both together. It makes visible how a change to the skills changes what the processes find and miss, so that a change can be compared with the last run instead of judged by feel. It is not a known-good test: the key records what runs have found, not the right answers, and real-world use, seen through the debriefs, is authoritative. First run: 2026-11-05 (`baseline.md`).

## Contents

- `project/`: the input. `notes.py` (a 35-line notes CLI with a JSON file), `README.md` with the group leader's request, `CLAUDE.md`. Never edited by a run; each run works on a copy.
- `conditions.md`: the brief for each condition (A: kaizen alone, B: OpenSpec alone, C: both), with placeholders for paths.
- `key.md`: reference findings (K1 to K10) and process measures, written from the first run; extended when a later run finds something real that the key lacks.
- `baseline.md`: the results of the first run against the key.

## Running it

1. For each condition, copy `project/` to a fresh directory outside this repository and `git init` it.
2. Start one fresh agent per condition with the brief from `conditions.md`, the placeholders filled in. Use the same model for all conditions and note it; the baseline used Opus 5.5. Conditions B and C need the OpenSpec CLI; note its version (baseline: 1.16.0).
3. Each agent returns its report as its final message. Save the reports and the usage of each agent (`python3 plugins/kaizen/scripts/usage.py agent-<id>`) outside the repository.
4. Compare each report with `key.md` with an agent that did not run any condition and does not know which skill version was used: for each key item, found or not, at which stage (requirements, walk-through, specification, implementation, hallway test, only in the agent's own critique afterwards), and any finding that is wrong.
5. Write the result as `results/<date>.md` in the format of `baseline.md`, with the plugin's commit and what changed since the last run. Compare with the baseline in the ledger, `design/kaizen.md`.

Cost of one full run (three conditions, implementation and hallway test where the brief asks for it): about 380 k sub-agent tokens and ten minutes.

## Limits

One toy, one request, one run per condition: differences of one or two key items are noise. The agent plays the principal, so everything a real person would contribute (priorities, what "old notes" means to them) is simulated. Use it to see regressions and gross effects of a change, not to rank processes or to certify a skill; when a run and real use disagree, real use wins and the key is corrected.
