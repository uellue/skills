---
name: plugin-selftest
description: Self-test of the kaizen plugin in this repository - a fresh agent meets the plugin from its README as a newcomer with a scenario project, and the run is graded against benchmarks/plugin-newcomer/key.md. Only when the maintainer types /plugin-selftest.
argument-hint: "[scenario: sem-instrument | existing-tool | ...] [model]"
disable-model-invocation: true
---

# Plugin self-test

The subject is always the kaizen plugin in this checkout. The scenario (`benchmarks/plugin-newcomer/scenarios/<name>.md`, with an optional project folder of the same name) is only the input the newcomer brings; when the run reaches one of the plugin's skills, including `kaizen:hallway-test`, that is a step to observe, never a test of the scenario's project. Do not invoke `kaizen:hallway-test` for this; this procedure is the hallway test of the plugin, and its results file stands in for the hallway record (`design/hallway/`).

Run every command from the repository root (`cd "$(git rev-parse --show-toplevel)"`).

1. **Scenario and model.** Take them from the arguments; without a scenario, list `benchmarks/plugin-newcomer/scenarios/*.md` with their first line and ask. Model: the argument, else Opus. Name the commit under test and say whether the plugin has uncommitted changes.
2. **Prepare.** `python3 benchmarks/plugin-newcomer/brief.py <scenario>` creates the scratch project and prints the filled brief; the scratch directory is in its first line.
3. **Run.** Start one fresh general-purpose agent in the background, on the chosen model, with the printed brief (without the header line) as its whole prompt. Tell the maintainer the cost to expect: about 15 k output tokens and three minutes per run so far. Answer its questions, if any, from the plugin's documents; what you cannot answer goes to the maintainer.
4. **Check.** For every claim the report makes about the plugin's text or scripts, check it yourself (a grep or a run each); a claim you cannot confirm is marked so.
5. **Grade.** Against `benchmarks/plugin-newcomer/key.md`: the items for all scenarios and those for this scenario, each held, partly, not held, not reached or not reported. Write `benchmarks/plugin-newcomer/results/<date>-<scenario>.md` (add `-2`, `-3` for further runs that day): commit, scenario, model, output tokens (`python3 plugins/kaizen/scripts/usage.py agent-<id>`), "graded by the main session, not blind", the table, the comparison with the previous run of the same scenario, the setup misfit the tester named.
6. **Hand over.** New findings go into `design/kaizen.md` as proposals with a lean each, not applied; a finding that the key lacks becomes a key item when the maintainer agrees. Summarise for the maintainer in a few lines: what held, what did not, what changed since the last run, the decisions waiting. Commit the result when the maintainer has asked for commits.
