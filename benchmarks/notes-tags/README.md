# Benchmark: tags and search for a shared notes tool

A small, fixed change request on a toy command-line tool, taken through the kaizen skills alone, OpenSpec alone, and both together. It makes visible how a change to the skills changes what the processes find and miss, so that a change can be compared with the last run instead of judged by feel. It is not a known-good test: the key records what runs have found, not the right answers, and real-world use, seen through the debriefs, is authoritative. First run: 2026-11-05 (`baseline.md`).

## Contents

- `project/`: the input. `notes.py` (a 35-line notes CLI with a JSON file), `README.md` with the group leader's request, `CLAUDE.md`. Never edited by a run; each run works on a copy.
- `conditions.md`: the brief for each condition (A: kaizen alone, B: OpenSpec alone, C: both), with placeholders for paths.
- `key.md`: reference findings (K1 to K10) and process measures, written from the first run; extended when a later run finds something real that the key lacks.
- `baseline.md`: the results of the first run against the key.

## Running it

1. For each condition, copy `project/` to a fresh directory outside this repository and `git init` it. Start the agents from a session whose working directory is outside this repository too.
2. The version under test is the `plugins/kaizen/` directory of this checkout at a named commit, read as files: `<PLUGIN>` in the briefs, and `${CLAUDE_PLUGIN_ROOT}` in the skills means the same directory. An installed kaizen plugin may also be visible to the agents; the briefs say not to invoke it.
3. Start one fresh agent per condition with the brief from `conditions.md`, the placeholders filled in, including `<MODEL>`: all condition agents and every agent they start run on it (the baseline left nested agents free, see `baseline.md`). Conditions B and C need the OpenSpec CLI; note its version (baseline: 1.16.0).
4. Each agent returns its report as its final message. Save the reports outside the repository, and the cost: output tokens from `python3 plugins/kaizen/scripts/usage.py agent-<id>` for each condition agent plus its nested agents (their `.meta.json` names the parent agent).
5. Compare each report with `key.md` with an agent that did not run any condition and does not know which skill version was used: for each key item, found or not, at which stage (requirements, walk-through, specification, implementation, hallway test, only in the agent's own critique afterwards), and any finding that is wrong.
6. Write the result as `results/<date>.md` in the format of `baseline.md`, with the plugin's commit and what changed since the last run, compare it with `baseline.md` and the previous results, and note the outcome in the ledger, `design/kaizen.md`.

Cost of the baseline run: about 130 k output tokens across the three conditions and their nested agents, and ten minutes.

## Limits

One toy, one request, one run per condition: differences of one or two key items are noise. The agent plays the principal, so everything a real person would contribute (priorities, what "old notes" means to them) is simulated. Use it to see regressions and gross effects of a change, not to rank processes or to certify a skill; when a run and real use disagree, real use wins and the key is corrected.
