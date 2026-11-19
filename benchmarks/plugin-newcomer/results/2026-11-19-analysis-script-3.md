# Run 2026-11-19 (3): scenario analysis-script, commit `ff5c1c0` (the fixes of ledger 316), Opus, about 2 minutes

Confirming run for ledger 316, graded by the main session, not independent, and only on N57 and 316 (a) to (c); the full grading of this scenario is in `2026-11-19-analysis-script-2.md`. Usage of the tester (`usage.py agent-a589c745d624ba69a`): Output tokens, claude-opus-5-5 17,459 .

The tester's report follows unchanged.

**Self-test of the kaizen plugin, scenario analysis-script (commit ff5c1c0)**

## What I read
- README.md
- skills/update/SKILL.md, skills/playbook/SKILL.md and skills/hallway-test/SKILL.md
- references/words.md, standing-instructions.md (head and block), ledger.md, tester-brief.md, and the safety row of decision-record.md (grep)
- The project's README.md, fitpeaks.py and the head of data/sample_a.csv. I also ran `ls skills/`, which goes slightly past the reading rules; the README names those skills anyway.
- Scripts run: `version.py update efa6c3e9`, `--project`, `playbook 1291422e`, `hallway-test a0ed1877` (all silent, rc=0). One stray call of mine, `version.py hallway-test x`, printed the stale-text warning as designed.

**Timing:** expectations.md was written before my first command, which ran at `date -Is` 2026-11-19T14:08:28+01:00. That time stands for the file's.

## The path
- **1** README: install (described, not run), then `/kaizen:update`.
- **2** update, first rollout: what the plugin adds; asked whether anything takes effect on push → "No, just my laptop" [made up]; public? → "No" [made up]; create CLAUDE.md? → "Yes"; issue tracker → "None" [made up].
- **3** update: whole block offered as one change, plus the ledger, on branch `kaizen-rollout` → "Yes". Commit 8f93189.
- **4** update hand-over: offered a PR description → "No"; next step `/kaizen:playbook`.
- **5** playbook step 1: originals? copy? → "Originals, only copy". This was asked before anything ran. Good.
- **6** playbook second round (owner, who may authorise, stand-in) → "Me for mine, each colleague for theirs" [made up]; "Me" [made up]; "No copy, make one" [made up]. The backup went to /tmp/kaizen-selftest-analysis-script-7wa6xjm5/backup-data with SHA256SUMS. Where the copy should go was not asked by any skill; the agent asked on its own.
- **7** playbook step 2: who uses it → "Two colleagues from my group, on their own spectra". Path chosen: existing tool before its first hand-over, so the hallway test now and the requirements reconstructed afterwards.
- **8** playbook step 7: "width" read as sigma → "Yes, sigma" [made up].
- **9** hallway-test first message: first user → "Don't know which; both know Python a little" [made up]; wrong fit → "I don't know"; hard spectra → "Overlapping ones" [made up]; questions collected for afterwards [made up]; place for the record → "Fine".
- **10** hallway leans accepted with one yes. Written: design/stakeholders.md and design/hallway/2026-11-19-brief.md, commit 328e83b.
- **11** Cost stated: about 14 min (46 k tokens, Sonnet), marked as a guess → that's what I would have done now: spawn a Sonnet behaviour tester with that brief, about 14 min and 46 k output tokens; it would produce design/hallway/2026-11-19.md.

Asked as the scenario wanted: how a wrong result would be noticed, and data with a known answer (hallway item 4). The originals question came before any run (playbook step 1).

## Findings, ranked
- **A — gap: about 25 numbered questions before any test.** Over update, playbook and hallway-test (10 messages, items 1–25), the newcomer answered about 25 numbered items before a tester could start. Expected: a few questions. Fix: for the "existing tool before hand-over" path, merge the playbook's step 1 and second round into hallway-test's first message, and skip the owner round when the person says the data are their own.
- **B — gap: the block is accepted unread.** update, step 3 of the first rollout: "offer the whole block as one change". A newcomer cannot judge 17 dense rules and accepts them blind. Fix: show 3 or 4 rules that change what they will notice (numbered questions, cost before agent runs), and link the rest.
- **C — surprising but defensible: the originals question is in four places.** It appears in playbook step 1, hallway items 3 and 5, and decision-record ("propose a backup before anything else"). Only hallway item 3 has a "unless already known" escape; nothing tells the agent not to ask again after the playbook asked. Fix: one line, "asked once per session; reuse the answer."
- **D — gap: where the backup copy goes is not asked.** hallway item 3 says "on another disk or share where there is one, announced with its path", but no question asks the person where that is. Fix: add "where is another disk or share?" to the questions only the person can answer.
- **E — question: units of cost.** Hallway item 9 gives minutes and tokens; the standing instructions give a ceiling "$20 at list price". A newcomer on a plan cannot relate either one to the other. Fix: one sentence translating the measured run into dollars or plan usage.
- **F — question: does the companion check apply?** Playbook step 4: "for a change larger than small, recommend the absent ones". It is unclear whether "existing tool before first hand-over" counts as larger than small. I skipped it.
- **G — surprising but defensible: PR offer with no remote.** update step 6 offers a PR description in a repository with no remote or tracker. Fix: offer it only when a remote exists.
- **H — gap: no place for the brief before the run.** Hallway "After 4" says the brief is saved next to the record, but nothing says where it goes before the run. I chose design/hallway/<date>-brief.md.
- **I — gap: the template line `Message size:` has no "not asked yet" form.** update says this question waits for the first debrief.
- **Good:** "git counts only with a remote elsewhere" stopped the agent from treating the committed data/ as a backup. Hallway item 5 makes writing next to inputs a mandatory case. The original's path is withheld from the tester, which works in scratch on a copy; data/ is made read-only and checked against checksums.

## The agent's messages, word for word
**M1** (11 lines, numbering no restart):
"This sets up the kaizen plugin in your project for the first time (a first rollout). What it adds:
- standing instructions: a short block of rules for me, kept in your project's CLAUDE.md
- a ledger, design/kaizen.md: a short list of what did not fit in how we work, read at the next debrief (a look back at how we worked together)
- skills for the next steps; /kaizen:playbook says which one fits now
Everything goes on a new branch, since you are on main; nothing is written before you agree.
- **1** Does committing or pushing here make anything happen (a website, a copy your group pulls from)?
- **2** Is the repository public, or may it become public?
- **3** There is no CLAUDE.md or AGENTS.md yet. Shall I create CLAUDE.md for the block? (AGENTS.md if agents other than Claude Code work here.)
- **4** Do you track issues for this script anywhere (GitHub, GitLab, none)?"

**M2** (4 lines):
"Nothing in the project conflicts with the block: there was no instruction file and no earlier choices to keep.
- **5** I would create CLAUDE.md with one section, "Kaizen standing instructions": 17 rules for me, for example numbering my questions like this, stating the cost before long agent runs, and asking before adding a dependency. And design/kaizen.md, the ledger, with "Public: no". Both committed on a new branch, kaizen-rollout. Yes?"

**M3** (6 lines):
"Done, on branch kaizen-rollout, one commit:
- CLAUDE.md: the standing instructions, version 0.6.1-dev.2
- design/kaizen.md: the ledger, Public: no; no issue tracker, so nothing to sync from
Taken: the whole block (you said yes to item 5). Kept: nothing existed to keep. Waiting: nothing.
- **6** Shall I write a pull request description? (No tracker or remote, so probably not needed.)
Next: type /kaizen:playbook; it says which step your work is at."

**M4** (3 lines):
"Your README says the script writes `<name>_peaks.csv` next to each spectrum, so it writes into the folder holding the data, also for your colleagues.
- **7** Is `data/` the original measurements, and is there another copy anywhere (git counts only if it is pushed somewhere)?"

**M5** (7 lines):
"Then the script can damage data that cannot be replaced: if a spectrum file ever ended in `_peaks`, or a name clashed, a result would overwrite it. Three questions, and no lean of mine on them:
- **8** Who owns these measurements, and the data your colleagues will run it on?
- **9** Who may agree that the script, or an agent testing it, runs on them? If you're unsure: think of data overwritten.
- **10** Is there a copy to work on instead? If not, I suggest making one now, outside the project, before anything runs.
Until the owner answers, nothing runs on the originals; reading the code and documents is fine meanwhile."

**M6** (1 line): "- **11** Who will use the script, and what will they do with the table it writes?"

**M7** (8 lines):
"Your script works for you and others start next month, so I suggest the short path for an existing tool before its first hand-over:
- first, a fresh agent tries the script as one of your colleagues would, with only the README, and reports what breaks or surprises it (a hallway test, /kaizen:hallway-test)
- then we write down what the script must do, from what that test found (/kaizen:requirements)
- at the end, a look back at how we worked (/kaizen:debrief)
No requirements, no tests and no list of users exist yet; the hallway test will offer a short user list.
- **12** Shall I start the hallway test? It asks you a few questions first and states its cost before it runs.
- **13** You said widths; the table's column is `sigma` (the Gaussian's standard deviation), not the full width at half maximum. I read "width" as sigma; is that what your colleagues expect?"

**M8** (7 lines):
"I read 'try it before others use it' as a hallway test: a fresh agent tries the script as a first user and reports what breaks; not automated tests.
There are no written requirements: the tester judges against your README only, and says where it had to guess.
- **14** Which of your two colleagues starts first, and what do they already know (Python, the command line, peak fitting)?
- **15** How would you notice a wrong fit? Is there a spectrum whose peak positions you know?
- **16** Which spectra are hard: overlapping peaks, noise, a sloping background?
- **17** During the run, will you answer the tester's questions, or shall I collect them for afterwards?
- **18** The test record goes to design/hallway/2026-11-19.md, committed on the branch kaizen-rollout. Fine?"

**M9** (9 lines):
"My leans; one yes takes all:
- **19** Persona: a group colleague who knows a little Python and has only the README; I add them as the one entry of a new user list, design/stakeholders.md (committed), marked described by you, the other fields unknown.
- **20** The tester gets: the README, a copy of fitpeaks.py to run but not to open, and a copy of your two spectra, in a scratch folder outside the project. It never gets the path of data/.
- **21** During the run data/ is made read-only and checked afterwards against checksums taken now; a change is a finding.
- **22** Since nobody knows a correct answer, the tester builds spectra with known peaks, overlapping and noisy ones among them.
- **23** Must-cases: the script writes next to its inputs (a result file overwriting an input), a folder with an existing `_peaks.csv`, an empty or malformed file. Plus experiments of its own.
- **24** Mode: behaviour (does it do what the README says), plus a pass over the command line's usability."

**M10** (2 lines):
"- **25** The tester runs on Sonnet; a behaviour test of a small command-line tool took about 14 minutes (46 k output tokens) when measured; for this script that is a guess of 10 to 15 minutes. Start?"

## Words a newcomer would not know
**(a) In the agent's messages:**
- "branch"
- "lean" (M5 and M9; never explained)
- "persona" (M9)
- "scratch folder"
- "must-cases"
- "checksums"
- "output tokens"
- "Sonnet"
- "pull request description"

Two names in list (a): "user list" vs "stakeholder record". The agent avoided the plugin's term but did not name the file's role consistently.

**(b) In the plugin's files:**
- marketplace
- upstream
- trailer (`Ledger:`)
- ER-C
- principal
- owner
- stand-in
- safety row
- must-example
- OpenSpec
- grill-me
- tokens counted once per API message

Two names in list (b):
- "inbox" = "Notes for the next debrief"
- "ledger" = `kaizen.md`
- "hallway test" = "play test"
- "requirements" = "demand and requirements specification"
- tester / persona / first user, used near-interchangeably in hallway-test

words.md explains most of these, but the README links it only once.

## What worked well
- The script's version lines were silent throughout.
- The first rollout asked about publication and created nothing unasked.
- The playbook's "existing tool before its first hand-over" path fit exactly.
- The data protection in the hallway test is concrete: copy, path withheld, read-only, checksums.
- Hallway item 4 asks how a wrong result would show and asks for known answers, falling back to synthetic spectra.
- The cost was stated before the start, with an honest "guess".

## Setup that did not fit
One line: the scenario's "never volunteer: who the other users are" collides with hallway's first question. The newcomer had to answer it briefly with a made-up answer, which shaped the persona.
