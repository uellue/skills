# Self-test: the plugin as a newcomer meets it

**Under test: the kaizen plugin**, from its README through whatever its skills lead to. A fresh agent plays a newcomer and that newcomer's agent, invents short answers to what the plugin asks (and volunteers nothing), and abbreviates real work ("that's what I would have done now: ..."). **The scenario is not under test**: it is the project the newcomer brings, the way a build tool is tried on a sample project; when the run reaches one of the plugin's skills, including its hallway test, that is a step to observe. Like `notes-tags`, this makes changes visible; it is not a known-good test, and real use, seen through the debriefs, is authoritative.

## Running it

In a Claude Code session in this repository: `/plugin-selftest <scenario> [model]` (the project skill in `.claude/skills/plugin-selftest/`; if a session started before that folder existed does not offer it, run `/reload-skills` or start a new session: Claude Code documentation, code.claude.com/docs/en/skills, "Edit a skill during a session", checked 2026-11-05). It prepares the run with `brief.py`, starts the tester, checks its claims, grades it against `key.md` and writes `results/`.

By hand: `python3 benchmarks/plugin-newcomer/brief.py <scenario>` prints the filled brief and creates a scratch project; give the brief to one fresh agent; grade its report against `key.md` as the skill describes. The tester reads an untracked copy of the README and the plugin that `brief.py` makes in the scratch directory, so it sees the version line as an installed plugin shows it and cannot touch this repository.

## Contents

- `brief.md`: the brief, with the scenario as a placeholder; `brief.py` fills it.
- `scenarios/<name>.md`: who the newcomer is, what exists, what they must never volunteer, what to note in particular; `scenarios/<name>/`, if present, is copied into the scratch project.
  - `sem-instrument`: a new colleague who wants an agent to operate a scanning electron microscope; nothing exists yet.
  - `existing-tool`: a scientist with a small working CLI (`tally`) and no requirements, told to get a critical first user to try it.
- `key.md`: what a run is checked against, per scenario (N1 to N16).
- `results/<date>-<scenario>.md`: one file per run.

A new scenario is a new file in `scenarios/` and, when the plugin should handle it in a particular way, new key items with that scope. About 15 k output tokens and three minutes per run so far.

## Limits

One persona and one run per scenario: a difference of one or two key items is noise. The tester plays both the newcomer and the agent and invents the newcomer's answers, so everything a real person would contribute is simulated, and a tester that answers too readily hides what the plugin would do with "I don't know". The tester reads the skill files rather than invoking the installed plugin, so loading and trigger behaviour are not tested.
