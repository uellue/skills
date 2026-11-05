# Coding standards

For the reviewer of a change to this repository. Only judgement calls are here; anything mechanical is a test in `tests/` (run by `./check.sh`), and a rule that could be one belongs there instead.

1. **One meaning in one place.** A rule, a location or a hand-off is stated once, in the skill or reference that owns it; the others point to it. Two copies drift: the tester briefs once told testers to write a report file the skill had abolished, and the OpenSpec hand-off appeared five times.
2. **A skill is self-contained under the plugin root.** A skill may point to `references/` and `scripts/` of its plugin, never to the repository's README or `design/`, which an installed plugin does not carry.
3. **Skill bodies hold procedure, not history.** Why a rule exists belongs in the ledger or the commit message; a skill says what to do. A fact that can go stale carries the date it was checked.
4. **Every rule in a skill can be traced to a requirement or an observed failure.** Text that no requirement in `design/requirements.md` and no ledger entry asks for is a candidate for deletion; skill text loads on every run.
5. **Instruments are tested on the case they were written for.** A script change comes with a test in `tests/` that fails without it.
6. **Public by default.** Nothing about other projects, people's internal disagreements or security findings; generalise, and say so before a push if earlier commits carry the specific wording.
