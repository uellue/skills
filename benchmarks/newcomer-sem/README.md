# Self-test: a newcomer with an instrument project, from the README

A fresh agent plays a new colleague who wants an agent to operate a scanning electron microscope, and that colleague's agent. It starts at this repository's README with no requirements and no code, follows the plugin as instructed, invents short answers for the colleague, and abbreviates real work ("that's what I would have done now: ..."). It shows, cheaply, whether the plugin's path holds from the first command to the debrief, and whether the skills raise what an instrument project needs without being told. Like `notes-tags`, it makes changes visible; it is not a known-good test, and real use, seen through the debriefs, is authoritative. First run: 2026-11-05 at `8480733` (`results/2026-11-05.md`, record `design/hallway/2026-11-05.md`).

## Contents

- `brief.md`: the tester's brief, with placeholders for paths and the model.
- `key.md`: what a run is checked against (N1 to N10), written from the first run.
- `results/<date>.md`: one file per run.

## Running it

1. Note the commit under test: `git rev-parse --short HEAD`. Run `/reload-plugins` (or start a new session) so the session runs the skills on disk, and check one skill's version line.
2. Start one fresh agent in the background with `brief.md`, the placeholders filled in: `<REPO>` this checkout, `<SCRATCH>` a new empty directory outside the repository, `<MODEL>` (first run: Opus). About 80 k tokens and three minutes.
3. The agent returns its report as its final message. Check its claims about the skill texts yourself (a grep each), then compare it with `key.md`: for each item, held, not held, or not reached, and any finding that is wrong. A grader that did not change the skills is better; for a quick rerun the main session may grade, and says so.
4. Write `results/<date>.md` with the commit, the model, the cost (`python3 plugins/kaizen/scripts/usage.py agent-<id>`), the key items, and new findings; add the findings that change a skill to the ledger. Extend the key when a run finds something real that it lacks.

## Limits

One persona, one domain, one run: a difference of one or two key items is noise. The tester plays both the person and the agent and invents the person's answers, so everything a real colleague would contribute is simulated. The brief forbids the tester from volunteering the risks the key asks about (N3 to N5), so that the run shows whether a skill asks; a tester that slips is visible in its path, and the run then says nothing about those items.
