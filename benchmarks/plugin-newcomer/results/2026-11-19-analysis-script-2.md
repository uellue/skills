# Run 2026-11-19 (2): scenario analysis-script, commit `cc180fe` (0.6.1-dev.2 with the fixes of ledger 315), Opus, about 3 minutes

Usage of the tester (`usage.py agent-ae86f2b90946d327f`): Output tokens, claude-opus-5-5 17,514 . Rerun after the fixes of ledger 315 (`cc180fe`); the tester's report was read by the main session from its transcript, and claims it makes about the plugin's text were checked before grading.

Graded by a fresh Sonnet agent that changed no skill, from the report, the key and the main session's checked claims.

Usage of the tester: not given to the grader. Third run of this scenario (previous: today's first run on `a26ddc9`, before the fixes of ledger 315). As in the first run, the tester stopped before starting the behaviour tester.

The tester's "agent messages" M1 to M10 are its own composition in the agent's role, with the full text left out of the report and quotes shortened. N24, N27 and N28 are therefore graded from a simulation and are weaker evidence than a transcript. N16, N20 and the plan items are graded from the messages and the tester's reading of the skills, not from a tester run.

Only two claims in this report were checked by the main session: the ledger template order (finding 8) and the HOME isolation of the rerun briefs. The other claims are marked "unchecked".

| # | Result |
|---|---|
| N1 | held, with a different path from before. The README sends the newcomer to `/kaizen:update` ("once in each project"), whose hand-over names `/kaizen:playbook`. Whether the debrief is labelled for after a stretch of work is not reported. |
| N2 | held: "Every version line was silent", and `version.py --project` reported the first rollout, as expected. The tester does not say which text the session ran. |
| N6 | partly: the playbook chose "an existing tool before its first hand-over" without hesitation. Whether the other skills point to that test is not reported. |
| N7 | held: M3 says "The ledger goes to design/kaizen.md and will be committed. Committing CLAUDE.md and design/kaizen.md on the new branch kaizen-rollout. OK?" Both files were committed only after the yes. |
| N8 | held: "Before anything runs on them I copy data/ to <path>, outside the project" (M6). The data are real, so no "simulated" label applies. |
| N9 | not reached: no debrief was run. |
| N10 | held: M7 announces the hallway test and the requirements afterwards. M10 gives the cost before the start ("Start?"). |
| N16 | held: M10, "My guess … about 15 minutes (about 50 k output tokens). Nothing in your project or in data/ is touched. Start?" It gives no money figure and no ceiling (finding 4). |
| N17 | held: M5, "Who owns the spectra in data/ …? What could it damage there …? Is there a stand-in …? Are the files in data/ the original measurements, and is there another copy?" The tester says the playbook asked these on the repo's own evidence, and the tester did not volunteer the answers. |
| N18 | held: the existing-tool path, with the hallway test now and the requirements afterwards. The full form was not offered. |
| N19 | held: M8 items 17 and 18, "How would you notice a wrong result …?" and "a spectrum whose right answer you know?", both before the run. |
| N20 | partly: the copy was announced and made (M6), and M10 says data/ is not touched. The brief text that gives the tester only the copy was read (hallway item 3) but is not quoted. The tester run did not happen. Finding 1 says nothing enforces this beyond the instruction. |
| N24 | partly, better than before. Ledger, hallway test and the lean (M2: "the answer I suggest; a plain 'yes' takes it") are explained at first use. Not explained: "output tokens" (M10), "behaviour" as a mode and "command-line usability pass" (M9). |
| N25 | not held: the tester lists about 10 hard words in the README (upstream, `Ledger:` trailer, closing keyword, inbox/route, two-hat interview, measured walk, injected faults, hint-following, blind grader, must-example). It lists about 6 in the skills (principal, small path, need note, safety row, "second round", retcon). It names three concepts with two names (inbox / "Notes for the next debrief", hint-following / "the impatient user", ledger / `kaizen.md`), and "record" is overloaded. |
| N27 | held: items 1 to 26 run in one sequence through M1 to M10, with no restarts and bold-number bullets. |
| N28 | held: lines per message are M1 11, M2 8, M3 3, M4 6, M5 6, M6 3, M7 5, M8 11, M9 12, M10 3. All are 15 or fewer. |
| N29 | not reached: no push or release came out of it. |
| N30 | not reached: no debrief. |
| N31 | not reached: no debrief. |
| N53 | held: M1 asks "Does anything happen when you commit or push here …?" (item 4) and "Is the repository public, or may it become public …?" (item 5), before anything is written. The tester answered "private, may become public with the paper" (made up). Whether the block and ledger stay out of a published tree was not tested, because the repo is private. Take-effect and public are asked in the same message. |
| N54 | held: M2 item 6 asks "CLAUDE.md or AGENTS.md?" with the lean CLAUDE.md, before creating one. |
| N55 | held: M4, "Next step: type /kaizen:playbook". It makes no debrief offer and no message-length question, and items 1 to 9 contain none. Finding 7 reports the debrief offer at the playbook's first use and at the hallway test's first use. Neither offer appears in the quoted messages. |

## Comparison with the previous run (`a26ddc9`)

| # | Change |
|---|---|
| N28 | better: partly (msg I about 17 lines), now held (longest message 12 lines). |
| N24 | better, still partly: "lean" is now explained and fewer terms are left over. "output tokens", "behaviour" and "command-line usability pass" remain. |
| N20 | worse in grading basis only: held, now partly. The previous run quoted the brief item. This run did not, and the ledger 315 fixes do not touch it. |
| N1 | changed path: First steps used to start at the playbook, now the README goes through update. Both lead to the playbook. |
| N53, N54, N55 | new, all held. |
| N2, N6, N7, N8, N9, N10, N16, N17, N18, N19, N25, N27, N29 to N31 | same. |

No item got worse in substance.

Ledger 315, items (a) to (f):

| Item | State | Evidence |
|---|---|---|
| (a) | holds | M1 items 4 and 5 ask about push and public before any write. The exclusion of a published tree was not exercised on this private repo. |
| (b) | holds | M2 item 6, "CLAUDE.md or AGENTS.md", with the lean, before creating the file. This closes the former finding 1 ("first rollout assumes an instruction file exists"). |
| (c) | holds | M4 names `/kaizen:playbook` as the next step. |
| (d) | holds at the rollout, with a caveat | M4 contains no debrief offer. Finding 7 says the offer now moves to the playbook's first use, where nothing has happened yet, and comes again at the hallway test's first use (unchecked). |
| (e) | holds | No question about the messages' length in items 1 to 9. |
| (f) | holds | No report of the host's `~/.claude/CLAUDE.md`. The main session confirms that the rerun briefs ran every plugin script with HOME set to an empty folder. |

## Setup misfit (tester)

The project is described as "the only copy", but `data/` is committed in git with no remote. A second copy therefore already sits on the same disk. The newcomer's answer "No copy; those are the originals" is at odds with that. The tester answered the question as asked and does not claim a skill failed because of it.

The previous run's misfit (the host's `~/.claude/CLAUDE.md` being read) is gone (f).

## New findings (candidates for key items)

Ranked by support. Everything is unchecked unless stated.

1. **Original data are protected only by an instruction.**
   - Hallway item 3 says to give the tester only a copy and not the original's path. The tester runs as the same user, `data/` stays writable, and the project path can be found. Nothing checks `data/` afterwards.
   - The tester notes that README lesson 11 says "prefer a check to a sentence".
   - Proposed fix: make `data/` read-only for the run and compare checksums afterwards.
   - Key item: N20 extended with a check that the original is unchanged after the run.
2. **The backup can land on the same disk, and git without a remote is not a backup.**
   - Neither hallway item 3 nor the decision record says where the copy goes, or that `git ls-files data/` should be checked. The skill's exemption is "data in git with a remote".
   - This is the setup misfit seen as a skill gap.
   - Key item: the copy is outside the project, preferably on another disk or share; git without a remote does not count as a second copy.
3. **"Who owns it" is ambiguous for a tool that will run on other people's data.** Playbook step 1, second round: the author's spectra or the future users'? Hallway item 5 comes back to the users' data only later.
4. **The cost has no money figure and no ceiling.**
   - Hallway item 9 gives minutes, with tokens in brackets. The standing instructions ask for a ceiling (default $20 at list price).
   - "Output tokens" is never explained to the person.
   - This is the same as the previous run's finding 3 and recurs.
5. **The first message of the hallway test holds five questions, against the rule of "one step or question at a time".** The five are who is first, how a wrong result would show, which cases matter most, who answers during the run, and where the record goes. M8 shows this.
6. **The take-effect answer is not recorded.**
   - Update asks "what makes a change take effect" and the playbook asks it again unless the repo answers it.
   - Only `Public:` goes into the ledger, so a new session asks again.
   - Proposed fix: record it beside `Public:`.
7. **The debrief offer is only moved.** After the first rollout it comes at the playbook's first use, and again at the hallway test's first use. Key item: N29 or N55 extended so the offer waits for the end of a stretch of work.
8. **The ledger's section order puts `## Skill friction` in the middle of the template.** The simulated agent appended its friction lines under "Notes for the next debrief". The main session confirmed the order (Proposals, Skill friction, Notes for the next debrief).

What worked: the README leads straight to update. The rollout chains into the playbook, and the playbook picks the existing-tool path. Version lines were silent. Data questions, the copy and the known-answer question came before anything ran. Message length and numbering now meet the key.
