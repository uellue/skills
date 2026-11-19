# Run 2026-11-19: scenario old-block-published (fixed from a varied seed), commit `9dc61a6` (the fixes of ledger 317), Opus, about 3 minutes

Confirming run for ledger 317, graded by the main session, not independent, on its key items only: N58 held: message 1 item 5 asks before design/ is created whether committed files become public, although an old kaizen block exists. The full grading of the varied run this scenario came from is in `2026-11-19-varied-*.md`. Usage of the tester (`usage.py agent-adbadd4a8049a7d73`): Output tokens, claude-opus-5-5 15,767 .

The tester's report follows unchanged.

**Self-test report: scenario old-block-published, commit 9dc61a6**

**What I read**
- Plugin: `kaizen/README.md`, `skills/hallway-test/SKILL.md`, `skills/playbook/SKILL.md` (the hallway test points to its step 3), `skills/update/SKILL.md` (the version notice points to it), and the references `words.md`, `tester-brief.md`, `ledger.md`, `decision-record.md` (safety row only, via grep) and the first 20 lines of `cli-ux-checklist.md`.
- Scripts run: `version.py hallway-test 88d82b56` twice, `version.py --help` and `version.py --project`.
- Scenario project: `CLAUDE.md`, `DEPLOY.md`, `README.md`, `tally.py`, `logs/*.log` (head only).
- Timing: I wrote expectations.md before my first command, which ran `date -Is` and printed 2026-11-19T14:23:34+01:00.

**Path**
- **1** README: the newcomer skips the "once in each project: `/kaizen:update`" step. Their request ("Can someone try it before my colleagues use it?") matches the description of `/kaizen:hallway-test`, so the agent loads that skill.
- **2** Start-up `version.py hallway-test 88d82b56`: it was not silent. It printed the "records are older … /kaizen:update" line and wrote `.git/info/kaizen-update-noticed`. On the second run it was silent.
- **3** Message 1 (verdict, reading of the request, no-requirements line, questions 1–5). Answers, all [made up] except where noted:
  - 1: "two colleagues from the group, they know the shell"
  - 2: "don't know"
  - 3: "you decide" (from the scenario's habit)
  - 4: "afterwards"
  - 5: "private" (allowed by the scenario when asked)
- **4** Message 2, the leans (items 6–10): "yes" [made up].
- **5** Message 3, record and ledger (items 11–12): "ok" [made up].
- **6** Message 4, model, cost and start (item 13): "yes" [made up].
- **7** Written in the project on the new branch `hallway-test-tally`, uncommitted: `design/stakeholders.md` (one entry) and `design/kaizen.md` (ledger with one friction line).
- **8** That's what I would have done now: spawn the behaviour tester from `tester-brief.md` with the CLI checklist pass, then write `design/hallway/2026-11-19.md`. Cost as stated in item 13: about 15 minutes, roughly 45 k output tokens, a guess for Opus.
- Not asked: a money ceiling. Also not asked by the skill: what makes a change take effect. The agent found DEPLOY.md on its own initiative.

**Findings, ranked**
1. **Gap: an old block with no ledger is not treated as a first rollout.**
   - Moment: `version.py --project` printed `CLAUDE.md: standing instructions from before 0.6 (no version line)` rather than "first rollout". The update skill runs its first-rollout branch only "when the script says so (no standing instructions and no ledger yet)".
   - Expected: a project that has never used the plugin gets the rollout questions (what makes a change take effect, whether committed files become public).
   - Observed: `/kaizen:update` would take the plain update path. That path skips the deploy question and creates the ledger in step 4. Harmless here, because only `docs/` is published, but not in general.
   - Fix: treat "no ledger" (or no version line and no ledger) as a first rollout for the where-files-go questions.
2. **Gap: hallway-test never looks at what publishes the repository.**
   - Moment: item 7 says "ask … whether committed files become public".
   - The newcomer's honest answer, "private", says nothing about DEPLOY.md publishing `docs/` on every push. Only the agent's own initiative caught it.
   - Fix: borrow the playbook's step 1, i.e. read deploy/CI files, or ask what a push publishes.
3. **Bug (wording): the version notice speaks of records the project never had.**
   - Quote: "this project's records are older (CLAUDE.md: standing instructions from before 0.6 (no version line)) … Said once for 0.6.1-dev.2."
   - The newcomer has no plugin records, "records" is not explained, and "Said once for" reads as internal.
   - Fix: "CLAUDE.md holds an older copy of kaizen's standing instructions; `/kaizen:update` compares it with the current one and asks before each change."
4. **Surprising but defensible: the first message is 20 lines, against the skill's target of about 15.**
   - Four mandates stack up: the version notice to pass on, the project CLAUDE.md's "verdict and strongest argument against" for a request phrased as a question, the reading line plus the no-requirements line, and five questions.
   - Fix: let the version notice go last, and let the reading serve as the verdict.
5. **Question: two rules each claim the first line.** The project's CLAUDE.md says to answer a question with a verdict first. The skill says "the first message is the reading of the request". I combined them (verdict, then reading). The skill could say which comes first.
6. **Surprising but defensible: the cost is given only in minutes and tokens.**
   - The standing instructions' default ceiling ($20 at list price) is never mentioned, and the newcomer was not asked for a limit.
   - The only measured figure is for Sonnet, so the Opus figure is a guess, which the skill does say.
7. **Question: the only copy of the repository.** The repository has no remote. The skill treats data well: tally only reads, so per item 3 nothing more is needed, and copies go to scratch. But the record is "committed" into the only copy, and "an uncommitted record can be lost" applies to the whole repository just as much. Fix: ask where the repository is pushed, as the playbook already does for a sibling repository.
8. **Surprising but defensible: `version.py` writes `.git/info/kaizen-update-noticed` without announcing it.** The file is not committed and `--help` documents it.

**The agent's messages, word for word**

Message 1 (20 lines at 100 characters; numbering does not restart):
> kaizen 0.6.1-dev.2 is installed; this project's records are older (CLAUDE.md: standing instructions from before 0.6 (no version line)): /kaizen:update brings them up to date, asking before each change. Said once for 0.6.1-dev.2.
>
> Yes, a fresh agent can try `tally` the way your colleagues would, with only the README, and report what breaks. The strongest argument against: nothing is written down about what tally must do, so the tester can only check it against its own reading of the README.
>
> I read "try it" as a hallway test: a fresh agent (the tester) uses the tool as a first user would and reports bugs and surprises; not automated tests. There are no written requirements, so the README is its only guide.
>
> Before I set it up:
> - **1** Who will use it first, and what do they already know (shell, Python, these logs)?
> - **2** How would you notice a wrong count? Is there a log whose correct counts you know?
> - **3** Which cases matter most to you?
> - **4** Will you answer the tester's questions while it runs (about 15 minutes), or should it collect them for afterwards?
> - **5** The test's notes would go into a new folder `design/` in this repository, on a branch. Is the repository public, or could committed files become public?

Message 2 (12 lines; numbering does not restart):
> My suggestions for the test; one "yes" takes them all, or name the numbers to change:
> - **6** The tester plays one of your colleagues: uses the terminal, has only the README. Not written down anywhere yet; I would start a one-entry list of users, `design/stakeholders.md` (committed on the branch).
> - **7** It may read README.md and what `python3 tally.py` prints; it runs a copy of tally.py and is told not to open it, since the file is also the source. Nothing else from the repository.
> - **8** tally only reads logs, so your files are not at risk; the tester still works on copies of `logs/*.log` in a throwaway folder outside the repository.
> - **9** It builds logs with known counts, including hard ones (lower-case `error`, a level word inside a message, an empty file, a missing file), runs a check of the command-line usability, and adds experiments of its own.
> - **10** Its questions are collected and answered by you afterwards.

Message 3 (5 lines; numbering does not restart):
> Where things go, on a new branch `hallway-test-tally`, nothing pushed:
> - **11** The test's record: `design/hallway/2026-11-19.md`, committed on the branch when you say so. `design/` is not under `docs/`, so per DEPLOY.md a push to `main` would not publish it.
> - **12** A short log of how the plugin's steps fitted this project, the ledger, `design/kaizen.md` (committed, marked "Public: no"), with one line from this test.

Message 4 (3 lines; numbering does not restart):
> - **13** The test runs on this session's model (Opus) in the background: about 15 minutes (roughly 45 k output tokens). That figure was measured once for a small tool on Sonnet, so for Opus it is a guess. Start?

**Words the newcomer would not understand**

(a) In the agent's messages:
- From the passed-on version notice, unexplained: "records", "standing instructions", `/kaizen:update`.
- Also: "output tokens", "Opus/Sonnet" (light) and "branch" (fine for this audience).
- Two names: "the ledger" vs "a short log of how the plugin's steps fitted".

(b) In the plugin files:
- README: "ledger", "upstream", "route the notes" / "inbox", "`Ledger:` trailer", "accepted leans", "principal", "acceptance examples", "need note", "small path", "safety row", "stand-in", "by eye", "hint-following", "two-hat interview", "Feature Forge". words.md covers many of these, but the README uses several before its link to words.md.
- Skills: "text id", "first rollout", "scratch".
- Two names:
  - "standing instructions" / "the block" / "the plugin's rules"
  - "records", which means the instruction file plus the ledger in version.py, the hallway record, and the stakeholder record
  - "tester" / "sub-agent"
  - "principal" / "person" / "owner"
  - "hallway test" / "play test"

**What worked well for a newcomer**
- The skill matched the newcomer's wording directly.
- The reading line and the no-requirements line made the scope clear.
- Item 3 correctly lets a read-only tool skip the data-safety ritual while still using copies.
- The leans were accepted with one "yes".
- The version notice is said once only.
- Nothing was written before asking.
- The ledger template asks "Public:" only once.

**Setup**
What in this test's setup did not fit: the scenario's two-line `CLAUDE.md` barely resembles an older kaizen block, yet `version.py` recognised it, so it is unclear whether detection is meant to be that loose.
