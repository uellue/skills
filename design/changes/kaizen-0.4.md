# Change: lessons from the plugin's first week of real use (kaizen 0.4)

Status: built; reconstructed after the build from the session of 2026-11-05 and its debriefs. Path: larger. Decided by: the principal, 2026-11-05, in that session (scope additions one by one); this record was written afterwards and is the first use of the template on the plugin itself.

## 1. Need
The principal and their colleagues (design/stakeholders.md) need the four skills to work on the sessions they actually have: transcripts in checkouts and VMs, sessions that end without warning, lessons that must reach the next session, and other tools (OpenSpec, Matt Pocock's skills) in the same project. The request was "address the debrief's points"; the need behind it is that the skills' own failures in week one do not recur. Out of scope: automatic tests of the skills' behaviour (planned in design/testing.md), issues on the public repository.

## 2. Interface
- New skill `playbook`; new scripts `transcript.py` (`locate`, `render`, `export`), `skim.py`; `usage.py` counts once per API message.
- New references: `change-record.md`, `openspec-config.yaml`, `reader-brief.md`, `diagnosis-brief.md`, `impatient-brief.md`.
- Project documents the skills write and read: `design/stakeholders.md`, `design/examples.md`, `design/changes/`, `design/hallway/`, `design/kaizen.md`; private reports in `.claude/debriefs/`.
- Relied on unchanged: the skill invocation names `kaizen:<skill>`.

## 3. Decisions
| # | Question | Options | Choice | Decided by | Reversible? |
|---|---|---|---|---|---|
| 1 | Where do debrief reports go? | repository `docs/`; private | private report in `.claude/debriefs/`, ledger in `design/` | principal | yes |
| 2 | Which repository gets a debrief? | where the work happened; where the lesson applies | the repository that was debriefed | principal | yes |
| 3 | OpenSpec | depend; ignore; complement | complement: checked for, mapped, recommended, never required | principal | yes |
| 4 | Matt Pocock's skills | as OpenSpec; install the whole plugin | as OpenSpec; named skills recommended, the whole plugin's trade-off stated | principal | yes |
| 5 | Accepted-lean check | hallway test only; every hand-over | every hand-over (standing instruction) | principal | yes |
| 6 | Order of the demand and requirements form | binding; checklist | checklist | principal | yes |
| 7 | Old wording about other projects in branch history | rewrite; keep | keep (no exploitable detail) | principal | no, once pushed |
| 8 | Hint-following hallway mode marked experimental | yes; no | no: the whole plugin is experimental | principal | yes |

## 4. Scope
Must: E2, E4, E5 (scripts, tested in `tests/`), E1, E3. Should: E6. Won't (this change): automatic behaviour tests of the skills, a plugin hook for `ask-matt` (parked, ledger 34).
Size budget: set afterwards, from the state at release: skill descriptions at most 800 characters, skill bodies at most 2,700 words, enforced by `tests/test_lint.py`. The release itself grew the five skills from 4,433 to about 9,700 words; the next change should not raise the budget without a reason in the ledger.

## 5. Blocking questions
None remained for the release. Open after it: whether the walk-throughs of design/walkthroughs/ (written 2026-11-05 without a person) match how a colleague and the maintainer actually work; the first real hallway test of a skill (the hint-following mode on devvm) runs after release, by the principal's plan.
