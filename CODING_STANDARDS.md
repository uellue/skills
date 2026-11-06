# Coding standards

For the reviewer of a change to this repository. Only judgement calls are here; anything mechanical is a test in `tests/` (run by `./check.sh`), and a rule that could be one belongs there instead.

1. **One meaning in one place.** A rule, a location or a hand-off is stated once, in the skill or reference that owns it; the others point to it. Two copies drift: the tester briefs once told testers to write a report file the skill had abolished, and the OpenSpec hand-off appeared five times.
2. **A skill is self-contained under the plugin root.** A skill may point to `references/` and `scripts/` of its plugin, never to the repository's README or `design/`, which an installed plugin does not carry.
3. **Skill bodies hold procedure, not history.** Why a rule exists belongs in the ledger or the commit message; a skill says what to do. A fact that can go stale carries the date it was checked.
4. **Every rule in a skill can be traced to a requirement or an observed failure.** Text that no requirement in `design/requirements.md` and no ledger entry asks for is a candidate for deletion; skill text loads on every run.
5. **Instruments are tested on the case they were written for.** A script change comes with a test in `tests/` that fails without it.
6. **Public by default.** Nothing about other projects, people's internal disagreements or security findings; generalise, and say so before a push if earlier commits carry the specific wording.

## The review brief

The independent review (see `CLAUDE.md`) gets this brief, filled in, as its whole prompt; it was written by hand for six reviews of 0.4 before it was kept here.

> You review a change to the kaizen plugin in `<repository>`, a public repository; you did not write it. Change no file; report only. The change: `git diff <last reviewed commit> HEAD`. Read the diff, then the files it touches. Judge it against `design/requirements.md` (what the plugin must do), this file (judgement calls) and the ledger rows it claims to implement (`design/kaizen.md`, <row numbers>). Run `./check.sh`. Reproduce every claim about a script in a scratch directory outside the repository before you report it. Report each finding with its severity (high, medium, low), the file and line, and how to reproduce it or the text that shows it; end with a verdict: ready, ready after fixes, or not ready.

Where Matt Pocock's skills are installed, `/mattpocock-skills:code-review` adds a second read along its standards and spec axes; give it `design/requirements.md` as the spec, since it looks for one in `docs/` and `specs/`. It reads the diff only and runs nothing, so it does not replace the brief above.
