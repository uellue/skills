# Run 2026-11-05: scenario existing-tool, commit `ffd59b3`, Opus, 9,046 output tokens, 1.7 minutes

Result format: E15. The first run of this scenario, prepared with `brief.py` and following `/plugin-selftest` by hand (the skill was not yet loaded in that session). Run from the maintainer's checkout, so the version line printed its status instead of staying silent. Graded by the main session that had changed the skills (not blind); the claims about the hallway-test skill and the tester template were checked with a grep each.

| # | Result |
|---|---|
| N1 | partly: the README leads to the playbook; the hallway test appears only in the "Plugins" list, as a tester that "sees only the requirements", which this newcomer does not have |
| N2 | partly: the version line ran in two skills; it printed "current" because the run was in the checkout, so the silent case was not observed |
| N6 | not reached: the newcomer had a tool, not an idea; the playbook offered the requirements retcon |
| N7 | held: the ledger was announced before it was written (announced, not asked) |
| N8 | not reached: something was built, and it drives no hardware |
| N9 | not reached: no debrief in this run |
| N10 | not held: see N16 |
| N13 | partly: the playbook offered the requirements retcon first and has no path for "test what exists before others use it"; the newcomer reached the hallway test by insisting ("Can we just test it?") |
| N14 | held: the hallway test said that no requirements exist, offered the playbook, and went ahead on "go ahead"; the tester template has no slot for that warning, so the agent rewrote it by hand |
| N15 | partly: the newcomer was asked for the persona and offered the stakeholder record; nothing says what to do when they decline, and the tester template's default persona ("a research software engineer at <institute>") could be used silently |
| N16 | not held: no cost before the tester starts; the skill mentions cost only afterwards |

**On the hand-over question.** N14 held with the current wording: the newcomer was told what was missing and could go ahead. With the wording first accepted ("if nothing is built yet or no requirements exist, stop and hand over to the playbook"), the hallway test would have sent this newcomer back to the playbook they had just come from, which offered no path for their case (findings 5 and 6). The run supports keeping the current wording; one run, so an indication.

New findings (ledger 62 to 69): cost and model stated before launching a tester; a persona question when there is no stakeholder record, and no default persona in the template; an optional "no requirements: your expectations are your own" sentence in the tester template; a playbook path for an existing tool before its first hand-over; no loop back to a playbook that already ran; questions during a run go to the owner when no design exists, and whether they stay available is asked; the mode (behaviour, impatient user) is chosen with the person; a short walk-through offered when there is no coverage. Also found while grading: `usage.py` and `transcript.py` run from a subdirectory of the checkout found no sessions (fixed, with a test).

Setup misfit (tester): running from the maintainer's checkout hides the installed copy's silent version line. A run from an installed copy would need the plugin installed from this commit.
