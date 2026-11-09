# Runs 2026-11-09 (1 and 2): scenario tracked-sync, commit `2512ddc` (0.6.0-dev.1, the first `/kaizen:sync`), Opus, about 2.5 minutes each

Graded by the main session, not independent (it wrote the skill and the key). Claims checked: `sync/SKILL.md` step 2 said "links one that closed" (present; settled by the fix to "settles"); step 4 named no ignore check for `.claude/drafts/` (present); step 5 had no form for a link before posting (present); the changelog's tracker template had no slot for who runs changing commands (present); `words.md` had no "inbox" or "sync" (grep: none). Setup misfit, both runs: the fixture has no `kaizen-0.6.0` branch and no remote, and the tracker's dates (2026-11-10) lie after the system date; both runs simulated the fetch and dated their work 11-10.

| Key | Run 1 | Run 2 |
|---|---|---|
| N27 numbering | held | held |
| N28 length | partly (M1 17 lines) | partly (M2 17 lines) |
| N44 setting read, not asked again | held (asked only the missing point: who runs changing commands) | held (same) |
| N45 fetch reported, rebase offered not run | held | held |
| N46 #17 reported, nothing added; spec question 3 named; #16 waiting | held (no "done" status, rightly: nothing #17 settles) | held (same; a "decided" line proposed for question 3) |
| N47 four notes, one destination each | held (issue, comment on 16, "→ row 1", debrief) | held (same) |
| N48 links only, sync date recorded | held (interim "draft, number follows") | held (same) |
| N49 nothing posted or pushed without a yes; drafts split; push left to the maintainer | held | held |
| N50 runs as `/kaizen:sync` | held | held (the agent first said to type it: asking in words does not start it) |

Both runs agree on every key item. Findings, fixed after the runs (both unless named): the setting lacked who runs changing commands; "links" marked notes done that a closed issue only mentions; a first sync had no start and stale questions depended on the window; a never-pushed branch has no upstream (run 2); no interim link before a draft is posted; no ignore check for `.claude/drafts/`; no "already there" destination for duplicate notes; the inbox's two names; step 2 needs two messages; whether the agents' part of a draft goes public (run 2); the README did not say that the person types `/kaizen:sync` themselves (run 2).
