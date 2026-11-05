# skills

Marketplace of one plugin, `plugins/kaizen/`: skills in `skills/*/SKILL.md`, templates and briefs in `references/`, scripts in `scripts/`. What the plugin must do and for whom: `design/` (stakeholders, requirements, examples with IDs, testing plan, the kaizen ledger). Rerunnable comparison: `benchmarks/`.

- Check: `./check.sh` (script tests on synthetic transcripts, lint of the skill texts; the pre-commit hook and CI run the same). Say "ready" only with its output; a change to a script gets a test in `tests/`.
- Claims about Claude Code's behaviour (plugin and skill format, transcript layout, skill visibility, hooks, `claude plugin eval`) are checked with the `claude-code-guide` agent or the CLI's `--help` before they go into a skill, and the source is named.
- A change beyond a few hundred lines gets a review by an agent that did not write it, briefed with the diff, `design/requirements.md` and `CODING_STANDARDS.md`, before it is called ready.
- This repository is public: no details of other projects, no security findings, no transcripts. Private material goes to `.claude/debriefs/` (ignored).
