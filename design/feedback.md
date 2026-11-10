# Feedback

What people said about working with the plugin, positive and negative, as the primary source for goals (ledger 238). One entry per line, so that `grep negative`, `grep hallway-test` or `grep "effect: none"` finds candidates for new work:

`- <date> | positive or negative | <area> | <what was said, cleaned> | effect: <what it became: a ledger row, a rule, a test; or none yet>`

Entries here are cleaned: no session ids, no names, no private projects, nothing caustic or personal; paraphrased where the words would be. The raw, verbatim remarks with their sources stay private, in `.claude/debriefs/feedback-raw.md` (ignored by git). Before an entry moves here, the person is offered a softened or paraphrased version whenever someone might not want the original public. When a ledger row acts on an entry, its effect is updated in the same commit.

## Entries

- 2026-11-05 | positive | requirements | The detailed, probing interview helped clarify my own thoughts; deferring questions as "open" or "for a later stage" was great and should be encouraged | effect: the requirements skill's rounds and its open and deferred markers
- 2026-11-05 | positive | requirements | The step-by-step interview style | effect: the requirements skill's rounds
- 2026-11-05 | positive | process | Reconstructing design documents from "just playing around" worked very well | effect: "retcon" in the requirements skill
- 2026-11-05 | positive | README | "Much better like this!": the lessons split into what the person does and what they paste for the agent | effect: the README's two parts; the standing instruction on a part for people and a part for agents (row 13)
- 2026-11-05 | negative | walkthrough | A colleague: the walk-through assumed personas without asking | effect: the persona gate; eval case asks-for-persona; the rule ablation showed which sentence holds it (214, 215)
- 2026-11-05 | negative | hallway-test | A colleague: the tester is too smart and not lazy enough; real first users skim the README and follow the program's hints | effect: the hint-following mode; the advice to run a cheaper tester
- 2026-11-05 | negative | debrief | The place for debrief results was awkward: rambling is fine in the session, but only actionable items should leave it | effect: private reports in `.claude/debriefs/`, the ledger for what is actionable
- 2026-11-05 | negative | collaboration | Statements written as questions were sometimes taken as decisions | effect: the standing instruction that a question is a question; a hook proposed (213)
- 2026-11-05 | negative | collaboration | "The numbers tell me nothing": items referred to by number without showing them | effect: none yet
- 2026-11-05 | negative | process | Skills building skills feels "meta"; the levels blur when the plugin tests itself | effect: `/plugin-selftest`; the glossary's *subject*
- 2026-11-06 | positive | pull requests | Drafting the pull request description together worked well; the summary on top is the manager's to write | effect: the standing instruction to start from log and diff and leave the summary to the person
- 2026-11-06 | positive | glossary | Settling the vocabulary was great to clarify what we talk about; muddy words in, muddy outcomes out | effect: `GLOSSARY.md`; the debrief's language group; README item 13
- 2026-11-06 | positive | glossary | Pushing back softly on muddy words ("I read X as …"): "You already do that, which is great" | effect: the standing instruction on ambiguous words
- 2026-11-06 | negative | debrief | The debrief missed the agent's struggle with the levels of self-testing; it should ask the person, since the agent may be blind to it | effect: the debrief asks the person before writing findings
- 2026-11-06 | negative | self-test | Unclear which skills a self-test used and what they covered | effect: topic 204; the eval suites and the coverage table (214)
- 2026-11-06 | negative | messages | The outputs are too long, I have to scroll | effect: the fifteen-line rule, key item N28 (185, 186); still recurring (209)
- 2026-11-06 | negative | messages | Numbered lists restarted within one message, and later across relayed messages | effect: one numbering per message, key item N27; across messages: a note, not yet tested
- 2026-11-07 | positive | self-test | Trying the newest version after the self-tests showed how far it had come | effect: none needed
- 2026-11-07 | positive | safety | Asking whether the agent could damage anything where it runs now was a very good idea, and so was offering the operator manual as context | effect: kept as "keep offering the ideas" in row 208, not built
- 2026-11-07 | negative | safety | On a toy instrument the skills came on strong about safety: they mixed up this session with later use elsewhere, did not take the manager's word, and asked for a written note an agent cannot verify | effect: row 208, not built
- 2026-11-07 | negative | skill development | Changing a skill felt like guesswork, without a backtrace, debugger or coverage | effect: topic 204: eval suites, rule ablation (214, 215); backtrace (218) not built
- 2026-11-07 | negative | skill development | Developing a skill and testing it at the same time was hard; wanted a notebook-like loop | effect: row 203, not built
- 2026-11-07 | negative | design documents | The documents grow fast and feel like sprawl | effect: the archive; rows 205 to 207, 217
- 2026-11-07 | negative | git | Keeping cited commits in step across rebase merges | effect: `rehash.py` and the `Ledger:` trailer (220)
- 2026-11-07 | negative | release | "We keep forgetting to bump the plugin version" | effect: the pre-push hook (222)
- 2026-11-07 | positive | skills | "Good impulse, I see the skills are working as intended" | effect: none needed
- 2026-11-07 | positive | requirements | The read-back of understanding in the agent's own words | effect: none yet; a candidate for a test
- 2026-11-07 | positive | debrief | Offering the debrief right after a merge makes more sense than moving on to the next thing | effect: row 224; trigger case after-merge
- 2026-11-07 | positive | debrief | Offering to note thoughts while a long run goes on: "a nice bridge" | effect: row 225, built in 0.5.4
- 2026-11-07 | positive | plugin development | The work on tooling for plugins was insightful; with the plugin, work starts to "flow" | effect: row 226
- 2026-11-07 | positive | ledger | The ledger keeps both the person and the agent on track through complex work and side quests, like a notebook | effect: row 10 (no issues for its rows)
- 2026-11-07 | positive | process | A revisit always with its trigger: good project-management practice | effect: the glossary's *revisit*
- 2026-11-07 | negative | debrief | The coaching did not reach the reply; it stayed in a file the person could not open | effect: row 238
- 2026-11-07 | positive | collaboration | Showing where the person's input went, as cause and effect without judgment, is very effective | effect: row 238; the standing instruction on hand-overs
- 2026-11-07 | positive | collaboration | A summary that shows what the person said and what it became keeps them feeling in control while so much of the work is beyond their view and bandwidth | effect: the hand-over rule (238), first used in that summary; scenario after-merge checks it
- 2026-11-09 | positive | collaboration | The hand-over's length and level of detail fit a terminal; the recap of what the person said and what it became is very helpful, keep doing it | effect: kept as the hand-over form (238); no change
- 2026-11-09 | positive | collaboration | Dropping random thoughts at any time and having them followed up at the right moment works very well | effect: row 268 (tips for new users)
- 2026-11-09 | positive | collaboration | The guidance from generic ideas and wishes to specific, actionable items is much liked | effect: none yet; kept
- 2026-11-09 | positive | ledger | A focused, version-controlled structure of requirements, action items and ideas in the repository, rather than message logs, keeps large and complex work on track and makes sure things are followed up | effect: none yet; kept
- 2026-11-09 | negative | hallway-test | Field tests with people in another environment have no guidance yet; copy and paste between the participant and the session is not always possible or sufficient | effect: row 269, research report `design/research/human-trials.md`
- 2026-11-09 | positive | process | Things keep improving; the person's input visibly shapes the experience, and it gets better and better | effect: none needed
- 2026-11-09 | positive | debrief | Losing track happens; what matters is that both notice and act, and the debrief catches it. Best it does not happen, then the agent corrects itself, then the agent notices and the person helps, then the person notices; the only fail is when it persists long enough to cause friction that better messages or introspection would have prevented | effect: row 277
- 2026-11-09 | negative | field test | A brief that told the participant to follow the plugin and how to answer imposed a personality change; people come with their own persona and agenda and need only the start and the method | effect: the devvm brief rewritten; the requirements topic field tests; for the field-test skill (283); worked examples `design/field-tests/brief-lessons.md`, E42
- 2026-11-09 | positive | field test | The most valuable information comes when real people follow their nose and go off script; scripts and scenarios belong to the automated hallway tests | effect: `design/field-tests/brief-lessons.md`, E42, the requirements topic field tests
- 2026-11-09 | positive | collaboration | Agents are a phenomenal help with git and gh; a colleague no longer wants to rebase without the agent | effect: row 291 (the sync supports the person with git and gh, shows and explains each command, and runs one itself only where authorised: "not exactly on my behalf, but with your support and help")
- 2026-11-09 | negative | process | The project's files churn so much that the person stopped reading many of them; agents judge cause and effect in skills better; the person's role is to change what the process converges to, not to move its state by hand, since agents may move it back at once | effect: row 289 (an audit skill)
- 2026-11-09 | positive | requirements | Suggesting the requirements skill for a set of open questions on one topic was exactly right | effect: none needed; kept
- 2026-11-09 | positive | debrief | A colleague uses the skills without adding anything to the repository yet, and likes that the debriefs stay under `.claude/`, kept but not tracked | effect: row 294 (a scenario for using kaizen without tracked files)
- 2026-11-10 | positive | field test | Variables first, then a series of plain commands, works; helper scripts must stay simple and understandable, and the steps are inspected and adjusted together with the person rather than handed over as "run this"; much of the field test's detail came from that | effect: ledger note for 283 (the field-test skill)
- 2026-11-10 | positive | field test | Observing real-world use of the object under test, and talking about it live while it happens, was very helpful for development | effect: ledger note for 283 (the live view is part of the method)
- 2026-11-10 | negative | testing | Problems believed fixed (the numbering) came back in the first real field test; real tests are needed and the self-test's cases need improving | effect: ledger note; row 209 escalated (measure numbering and length on real transcripts)
- 2026-11-10 | positive | field test | Having the agent check the person's steps through a complex procedure as they happen, and help fix the setting when it breaks (the VM clone), was very helpful | effect: ledger note for 283
- 2026-11-10 | positive | collaboration | The agent reading back its understanding of the layers and personas before a walk-through made sure both had them right | effect: kept; the field-test walk-through starts with it
- 2026-11-10 | positive | field test | A role-play of a planned field test, with the person playing themself and the agent in role, went well and did what the person had in mind; out-of-role notes were well marked, the layers always clear | effect: rows 295, 296; the method noted in the quick debrief
- 2026-11-10 | negative | testing | Repeated plugin eval runs overran the cost and hit the person's session limit, which slowed down their work on another project | effect: ledger note; proposals for an eval budget
- 2026-11-10 | positive | skills | Reading the skills after many self-modification loops, the person found them clean and sane, "a stable, sensible attractor", although the method could be called mucking with it until it passes tests | effect: none needed; kept
- 2026-11-10 | negative | field test | The field-test skill's frame question reached the person as a label ("One shot or repeatable"), which is jargon; it needs to be asked in clear language | effect: the skill's step 1 now gives the question in plain words
- 2026-11-10 | positive | field test | The field-test skill's open questions led the person to a good idea of their own (a quick test on a subtree before the whole tree) without imposing anything or narrowing their thoughts: open questions gather real-world ideas and keep the scope wide | effect: a win to keep; the frame's questions stay open, without proposing the answer
- 2026-11-10 | positive | collaboration | Leans with a rationale let the person move fast, are right most of the time, and stay open enough to capture their thoughts in the right places; nothing to shift now ("if it ain't broke, don't fix it") | effect: none; the balance of leans and open questions stays as it is
- 2026-11-10 | positive | field test | The person loves running a field test of their own tool with the agent's help (the first use of the field-test skill in another project) | effect: none needed; kept
