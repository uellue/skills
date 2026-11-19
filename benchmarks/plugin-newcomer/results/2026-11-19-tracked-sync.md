# Run 2026-11-19: scenario tracked-sync, commit `a26ddc9` (0.6.1-dev.2), Opus, about 2 minutes

Usage of the tester (`usage.py agent-a8e6398dbf84fc1eb`): Output tokens, claude-opus-5-5 11,329 . The tester's report was read by the main session from its transcript; claims it makes about the plugin's text were checked by the main session before grading.

Graded by a fresh Sonnet agent that changed no skill, from the report, the key and the main session's checked claims. The main session confirmed every claim about `sync/SKILL.md` that the report makes: step 5 "→ draft", step 3 "only when the person asks", step 2 "update's first look", "two messages" and `disable-model-invocation`.

## Grades

| Key | Grade | Evidence |
|---|---|---|
| N1 | not reached | The tester read the README only for the sync paragraph and never followed First steps. |
| N2 | partly | M2 opens "kaizen 0.6.1-dev.2 is installed; this project's records are older (CLAUDE.md: standing instructions from 0.6.0-dev.1): /kaizen:update brings them up to date". This is correct for the fixture, whose copy is older. It is not silent, as in the previous run. |
| N6 | not reached | The playbook was not used. |
| N7 | not reached | The ledger already existed. The agent wrote into it only in step 5, and the report does not say that it announced where the ledger is or that it is committed. |
| N8 | not reached | Nothing was built or tested. |
| N9 | not reached | No debrief report was written. Only an offer was made. |
| N10 | held | Nothing costly was started. The five-message length of a sync was not announced (finding 7, minor). |
| N24 | partly | M3 used "ledger" before M4 explained it, and "first look" was never explained. This is the same weakness as before (previously "lean"). |
| N25 | not held | The tester lists "routes" (explained only by its examples), "the update's first look", "inbox" against "Notes for the next debrief", and "maintainer" against "the person" or "principal". It also lists a "Kept on purpose" README paragraph with no counterpart in the skill. |
| N27 | held | The numbers run 1 to 10 across M2 to M5, with no restart, and M5 refers back with "after **2**". One point is open: M6 asks "Commit these on that branch or a separate one?" without a number. |
| N28 | held | The tester reports the lengths of the quoted messages as 4, 6, 14, 9, 11 and 5 lines, all at or under 15. |
| N29 | partly | M6 offers a debrief once, "Want a debrief of yesterday's stretch? `/kaizen:debrief`". The push is still pending, so placement after the push is not tested. No invitation to note thoughts was reported. |
| N30, N31 | not reached | No debrief was run. |
| N44 | held | M2: "Your CLAUDE.md already says where issues live (GitHub, modama-rdm/devvm) and that nothing is posted without your yes; I'll keep to that." Only the missing push and rebase point was asked. |
| N45 | held | M3: "`origin/main` moves to the merge of pull request 21. Your branch `kaizen-0.6.0` was never pushed: 2 commits ahead of `origin/main`, and at least 1 behind", with `git rebase origin/main` offered and not run. The fixture has no such branch or remote, so this was simulated (see the setup misfit). |
| N46 | held | M3 reports #17 as closed by pull request 21 and adds nothing to the ledger for it. It names open question 3 as stale ("#8 was fixed by #9 … the question looks stale"). It names #16 as unanswered, with the item "**4** #16 … has no answer yet", and M5 ends "Where your answer is needed: **4** (#16)". The agent did not volunteer a reply draft. |
| N47 | held | M4 gives each of the four notes one destination: 16:10 a new issue, 16:25 ledger row 2 ("A comment on #16 only if you want one"), 16:40 already row 1, 17:05 kept for the debrief. The place where the maintainer's answer is needed is named in M3 and M5. Drafts were written only for the items the scenario's answers picked (issue and comment). |
| N48 | held | M6: "the three routed notes now hold only their links, the 17:05 note stays, plus one line '2026-11-19: synced'". |
| N49 | held | Nothing was posted or pushed. M5 states "two drafts, each with a part for people first and a part for agents", and shows `git push -u origin kaizen-0.6.0`. The split is shown here, not just implied. |
| N50 | held | M1: "It starts only when you type it yourself", and the newcomer typed `/kaizen:sync`. |

N3 to N5, N11 to N23, N26 and N32 to N43, N51, N52 belong to other scenarios and are not graded.

## Comparison with 2026-11-11 (0.6.0)

- N28: better, from partly (about 17 lines in M2) to held (all messages at 15 lines or fewer).
- N47: better, from partly to held. The setup-dev lean now goes with ledger row 2, and the place for the maintainer's answer on #16 is named twice.
- N49: better. The people/agents split is now stated in M5, not just implied.
- N27: same, held (1 to 17 before, 1 to 10 now). New point: the question in M6 has no number.
- N2: same, partly. Same cause: the project really is behind.
- N24: same, partly. A different word is unexplained ("ledger" and "first look" instead of "lean").
- N25: same, not held, with the same kind of words.
- N44 to N46, N48 and N50: same, held.
- N29 to N31 and the other debrief items: not graded before or now.

## Setup misfit

The fixture is on `main`, with no `kaizen-0.6.0` branch, no unpushed commits and no remote. The rebase, the push and "what each unpushed commit holds" (step 4) were only simulated, and the tester's finding 6 could not be tested. This is the same misfit as in the previous run and is still unfixed. The misfit about `version.py --project` reading the host's `~/.claude/CLAUDE.md` is not reported for this scenario, because M2 named the project's own `CLAUDE.md`.

## New findings the key lacks (candidates)

Layer for all: the plugin (sync skill).

- **Dangling link after routing (tester finding 1, confirmed against step 5).** A routed note keeps only "→ draft `.claude/drafts/<file>`". The folder is git-ignored but the ledger is committed. The note's content leaves the committed record, other clones get a dead link, and the idea is lost if the draft is deleted before posting.
  - Candidate item: a routed note that points to an unposted draft keeps a one-line gist until it is posted.
- **Two paths edit one section (finding 4).** Step 1 offers to record "who runs push" in `CLAUDE.md`, while the version line says `/kaizen:update` should rewrite that section. The skill does not say which one wins. In the run the newcomer deferred it ("leave that for the update").
  - Candidate item: when the project's records are older, the sync defers recording to the update, or says so.
- **First sync without a start line (finding 5).** Step 2 starts from the update's first look. This worked only because the ledger had that line. The skill says nothing for a ledger without it.
  - Candidate item: a first sync works from a ledger that has no first-look line.
- **Unnumbered question at the end (new, from M6).** "Commit these on that branch or a separate one?" has no bold number, although the key's N27 and the standing instruction require every item to be numbered. N27 is graded held, but the key could say that closing questions count too.
- **Terms used before they are explained (from the tester's list).** "Ledger" appears before M4 explains it, and "first look" is never explained. This is already covered by N24, and the sync skill's wording is a place to fix it.
- **Finding 2 (comment on someone else's issue) is not a gap in practice.** The agent offered the comment on #16 itself in M4 ("only if you want one"), so the wording worked. Keep it as a note, not a key item.
- **Finding 3 ("let's sync" in words does not start the skill).** This is by design (`disable-model-invocation`, README sentence). The agent handled it with M1 and cost one extra round trip. Not a key item.
- **Finding 7 (five or more messages, no up-front hint).** This is minor, and N10 is graded held because nothing costly started.
