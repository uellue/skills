# Run 2026-11-19: scenario analysis-script, commit `a26ddc9` (0.6.1-dev.2), Opus, about 4 minutes

Usage of the tester (`usage.py agent-a393930755e66649a`): Output tokens, claude-opus-5-5 23,023 . The tester's report was read by the main session from its transcript; claims it makes about the plugin's text were checked by the main session before grading.

Graded by a fresh Sonnet agent that changed no skill, from the report, the key and the main session's checked claims.

Result format: E15. Second run of this scenario (previous: 2026-11-06, commit `d14e602`). The tester stopped before starting the behaviour tester and described step 11 as what it would have done. N16, N20 and the plan items are therefore graded from the agent's messages, not from a tester run. Claims in the report that the main session did not check are marked "unchecked". The one claim marked NOT CONFIRMED belongs to the small-website run and is not used here.

| # | Result |
|---|---|
| N1 | partly: the README's "First steps" block starts at `/kaizen:playbook` (confirmed, though it leaves out update, see finding 2). Whether the debrief is labelled for after a stretch of work is not reported. |
| N2 | held: playbook and hallway-test "version line silent"; for update the version line "printed nothing (rc 0)". `version.py --project` printed its first-rollout report, which is expected. |
| N6 | partly: the playbook chose the existing-tool path at once (msg G, "this is an existing tool before its first hand-over"). Whether the other skills point to the same test is not reported. |
| N7 | held: msg A names the ledger, `design/kaizen.md`. Msg D says "I will now write two files on branch `kaizen-rollout`, both committed with your yes: ... `design/kaizen.md`: the ledger". Nothing is written before the yes. |
| N8 | held: the data are a copy (msg F: "I won't run anything on them. The cheapest stand-in is a copy"). The tester gets the copy only. The data are real, not an imitation, so no "simulated" label is needed. |
| N9 | not reached: no debrief was run. |
| N10 | held: msg G announces the hallway test and the requirements afterwards before anything starts. Msg J states time and tokens before the tester starts. |
| N16 | held: msg J, "Estimate: about 15 minutes (about 45 k output tokens), from a measured behaviour test of a small command-line tool; yours is similar, so this is close but still a guess." There is no dollar figure and no ceiling, see finding 3. |
| N17 | held: msg E, "Are the files in `data/` your original measurements, and does another copy exist?" and "Who owns these data, and who may decide what a tool does to them?". The agent asked these from the skill's step 1 and the decision record's safety row, not on its own judgment. "Until 7 is answered, I run nothing on `data/`." |
| N18 | held: the existing-tool path, with a hallway test now and requirements afterwards. The full form was not offered. |
| N19 | held: msg H, "How would you notice a wrong result: a plot, a known peak position, a comparison?" and "Do you have one spectrum where you know the right answer?". Both come before the tester. Msg I item 19 has the tester build its own known-answer spectra. |
| N20 | held: msg I item 17, "a copy of the spectra in its own scratch folder; never the path of `data/` or your copy". The copy is made through a question first (msg F). |
| N24 | partly: "ledger", "debrief" and "hallway test" are explained at first use (msg A). "lean" (msg A, though words.md defines it), "branch", "remote", "persona", "scratch folder", "behaviour" mode, "eleven-point command-line checklist", "Must-case" (coined in the session; the plugin says must-example), "Sonnet" and "output tokens" are not. "Hallway test" and "a first user tries it" appear side by side. |
| N25 | not held: the tester lists about 10 hard words in the README (for example "ledger rows", "`Ledger:` trailer", "`Refs #<n>`", "OpenSpec", "list price") and about 5 in the skills ("principal", "safety row", "need note", "inbox", "stand-in"). It also finds concepts with two or more names: inbox = "Notes for the next debrief" = the ledger's notes section; acceptance example = must-example = mandatory case = scenario; principal = person = owner. |
| N27 | held: items 1 to 23 run through msgs A to J in one sequence. There are no restarts and every question is a bold-number bullet. |
| N28 | partly: of the ten messages, nine are 15 lines or fewer (A 15, B 8, C 6, D 9, E 9, F 4, G 9, H 11, J 3). Msg I with seven leans runs about 17 lines. |
| N29 | not reached: no push or release came out of the hand-over. The debrief offer in msg D comes straight after the four-message rollout (finding 4). The run of several minutes does not invite notes for the debrief; msg H item 15 is about the tester's questions. |
| N30 | not reached: no debrief. |
| N31 | not reached: no debrief. The update itself already asks the question (msg C item 5, "Shorter or longer messages than these?") and records "messages: this length" in the ledger. |

## Comparison with 2026-11-06

| # | Change |
|---|---|
| N7 | better: not reported, now held (the ledger is announced with where and "committed with your yes"). |
| N10 | better: partly, now held. |
| N17 | better: the caveat is gone. Step 1 and the decision record's safety row now carry the question. |
| N19 | better: not held, now held. The hallway test asks about a wrong result and a known answer (items 13 and 14). |
| N20 | better: partly, now held. Item 17 names the copy and withholds the originals' path. |
| N6 | better: not reached, now partly. |
| N1 | graded on a different basis (earlier the hallway-test line, now the First steps block), so the two results are not comparable. |
| N2, N8, N16, N18 | same (held). |
| N9 | same (not reached). |

N24 to N31 were not graded in the previous run, so there is no comparison. No item got worse.

## Setup misfit (tester)

`version.py --project` printed "a copy in your ~/.claude/CLAUDE.md", read from the host user's file. A real newcomer would not have one, so the tester skipped the question the skill attaches to it. The main session confirmed this in three more runs: `brief.py` does not isolate HOME. The previous run's misfit (synthetic spectra labelled in their header) was not named this time.

## New findings (candidates for key items)

Ranked by support.

1. **First rollout assumes an instruction file exists.**
   - Confirmed by the main session: `update/SKILL.md`'s first-rollout paragraph speaks only of "the project's existing instruction file" (review finding L8, declined then, now hit by two runs).
   - Here the agent asked about `CLAUDE.md` or `AGENTS.md` (msg B item 2) and so coped. The text does not say to.
   - Key item: with no instruction file, the update asks `CLAUDE.md` or `AGENTS.md` and creates it after a yes.
2. **Two entry points roll out differently.**
   - Confirmed: README "First steps" leaves out `/kaizen:update`, and playbook step 3 suggests it only for "a project that has its own instruction file but neither ...".
   - Following First steps in a project like this one skips the rollout.
   - Key item: the README's first steps reach the rollout, or the playbook suggests update whenever no ledger exists.
3. **Cost without money or ceiling.**
   - Unchecked as a whole. The main session confirmed only that hallway-test item 9 compares the cost "against their limit, if they gave one".
   - The standing instructions ask to "agree a ceiling (default $20 at list price)". The newcomer got minutes and tokens and no ceiling.
   - Key item: N16 extended to the ceiling, or the standing instruction says minutes are enough for a single test.
4. **Debrief offered too early.**
   - The standing instruction "offer a debrief ... at a kaizen skill's first use in the project" produced the offer in msg D after a four-message rollout.
   - That the update skill does not exempt it is unchecked.
   - Key item: N29 extended so that update's first use does not trigger the offer.
5. **Question order in the rollout.** Unchecked. Update asks "whether the messages' length suits" before any messages have been read (msg C item 5). Playbook step 3 asks again about public commits without reading the ledger's `Public:` line.
6. **Leans block over the limit.** Seven leans ran to about 17 lines. The skill moves only "the record's place and the ledger" out. Unchecked: whether the skill's internal labels ("item 3", "step 2") leak into the numbering.
7. **Playbook round 2 fits facilities better than own data.** Unchecked. Its questions (owner, who may authorise, a simulator) read oddly for a student's own spectra. Fix proposed by the tester: put "originals / other copy" first in the bullets.
8. **Wrong result only asked inside the hallway test.** Nothing before it asks, and on "I don't know" the tester builds synthetic inputs. The tester calls this defensible on the existing-tool path. N19 holds, so this is not a miss.
9. **Question left unasked.** Not asked: what the colleagues would do differently with the tool.

What worked and is already in the key: the data questions before any run, the copy and backup proposed, the original's path withheld, the existing-tool path chosen at once, silent version lines (N2, N8, N17, N18, N20).
