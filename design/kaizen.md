# Kaizen ledger

What leaves a debrief: proposals with decisions, the fate of earlier ones, what did not fit in the plugin's skills, and notes for the next debrief. The full reports are private, in `.claude/debriefs/` (not under version control). The debrief of 2026-11-03 was about the data-management-system project and lives in that repository (`docs/debriefs/2026-11-03.md`); its recommendations are tracked there.

## Proposals

### 2026-11-05 (debrief of the plugin's first week: seven sessions in devvm, data-management-system and its devvm worktree)

Destination "plugin" means this repository; "other repos" means the projects' own backlogs or instruction files, to be transferred by the manager.

| # | Proposal | Destination | Effort | Decision / status |
|---|---|---|---|---|
| 1 | `usage.py`: count tokens once per API message id, report API messages not lines, per-sub-agent rows, verified against a known session | plugin | small | done in 0.4 |
| 2 | `transcript.py`: locate transcripts wherever they are, render them with L-markers and queued mid-turn messages, export a session into `.claude/transcripts/`; no ad-hoc JSONL grepping | plugin | small | done in 0.4 |
| 3 | Debrief skill: transcripts beyond `~/.claude/projects`; multi-session mode with one reader per session and a bundled reader brief; readers' claims about instruments verified by the main session | plugin | medium | done in 0.4 |
| 4 | Debrief on a schedule, not before an end; "note for the debrief" captured into this ledger at once; report private in `.claude/debriefs/`, ledger in `design/`; debriefs go to the repository that was debriefed | plugin | small | done in 0.4 (principal's decision 2026-11-05) |
| 5 | Hallway test: report as the tester's final message, expectations file before the first run, record committed by default, accepted lean versus shipped, diagnosis brief, documents and instruction files as subjects, experiment bookkeeping, vulnerability first | plugin | medium | done in 0.4 |
| 6 | Walk-through: persona from the stakeholder record and never assumed, offer to add or correct one; combination with requirements; the running system as "what exists"; measured walk with injected faults; confidence updated after the owner answers; a real stakeholder present gets the questions first | plugin | small | done in 0.4 |
| 7 | Requirements: "from the record" mode (facts gathered first, reconstruction) with `[record]`; markers per item; several sections per round, pre-filled; deferrals with stage and owner; figures in the agent's prose need a source; quotes from sub-agents verified; handover check listing everything unconfirmed; 1.4 writes the stakeholder record | plugin | small | done in 0.4 |
| 8 | A stakeholder record per project, shared by requirements, walk-through and hallway test | plugin (skills); projects (`design/stakeholders.md`) | small | done in 0.4 for the skills; this repository's own record written |
| 9 | A playbook skill: the lifecycle, when each skill fires, the shared documents, "which skill would have supported this" asked at the moment | plugin | small | done in 0.4 |
| 10 | Kaizen on kaizen: every skill run ends with one friction line into the ledger; plugin proposals become issues or merge requests on this repository with the manager's say | plugin | small | done in 0.4 (the line in every skill); issues: pending the manager |
| 11 | The plugin's own design record: stakeholders, requirements, testing plan | plugin | medium | done in 0.4; requirements from the record, to be confirmed by the principal |
| 12 | Tests for the skills: fixtures with planted defects, a pre-written key, a blind grader; check `claude plugin eval` | plugin | medium | planned, `design/testing.md`; owner the maintainer |
| 13 | Output that leaves a project: a short part for humans, details for agents, marked as endorsed by a human (a design document they reviewed) or attached without endorsement (an agent's analysis on an upstream issue) | README standing instructions; projects' `AGENTS.md` | small | done in 0.4 as a standing instruction (principal, 2026-11-05: the README's own operator/agent split is an instance); to transfer to the projects |
| 14 | A hook that runs the project's pre-commit check before `git commit`; "clean" only from that command (recurring in four sessions) | other repos (hook) | small | to transfer |
| 15 | A diff-size check that asks for an independent review past the threshold (skipped four times) | other repos (hook or rule with a command) | small | to transfer |
| 16 | Sub-agent briefs name the scenario or acceptance example each assertion serves | other repos (`AGENTS.md`); plugin (tester brief, done) | small | plugin part done; to transfer |
| 17 | Bash discipline: absolute paths and self-contained commands; Read and Edit instead of inline replacement scripts (three sessions with a clobber or a miss) | other repos (memory, `AGENTS.md`) | small | to transfer |
| 18 | Name any deviation from a lean the person accepted, at hand-over | other repos (`AGENTS.md`); plugin (hallway-test after-step, done) | small | plugin part done; to transfer |
| 19 | Lessons that travel: seed standing lessons into every checkout's memory (devvm provisioning) or keep them in the repository | devvm `setup-dev`; guide | medium | open; owner the manager |
| 20 | Standing answer for absence in the guide: "away for N; take the recommended option, list the rest" | guide | small | to transfer |
| 21 | Close the open items of the week in the projects concerned (a credential to rotate, an uncommitted test record, stale markers, two open decisions) | other repos (backlogs) | small | transferred |
| 30 | A request phrased as a question is a question: verdict and strongest counter-argument first, act only if yes and cheap to undo (principal, 2026-11-05: questions were taken as instructions three times in this session: the README section, the standing instruction, the OpenSpec recommendation) | README standing instructions; projects' `AGENTS.md` | small | done in 0.4; to transfer |

### 2026-11-05 (comparison of the kaizen skills with OpenSpec: alone, OpenSpec alone, both)

| # | Proposal | Destination | Effort | Decision / status |
|---|---|---|---|---|
| 22 | A "decide" moment after the walk-throughs and a short change record of its own (interface, decision table with who decided and whether reversible, must/should/won't with a size budget, questions that block the build), mapped one-to-one onto OpenSpec's design and scenarios when a project uses it | plugin (playbook, new template) | medium | done in 0.4 |
| 23 | Acceptance examples in one place with IDs, concrete data, priority and the walk step they came from; walks append to it, tests and hallway briefs cite the IDs; a coverage check lists examples with no scenario or test; add the section to the requirements template | plugin (requirements, walkthrough, hallway-test) | small | done in 0.4 |
| 24 | A small-change path in the playbook: a short need note, one walk as a step table, the decision record, the hallway test; the full form and OpenSpec's specs and tasks only for larger changes | plugin (playbook) | small | done in 0.4 |
| 25 | A ready-made OpenSpec `config.yaml` (context and rules: the proposal names the persona, says whether the requested solution is the whole need, lists unconfirmed premises; each scenario cites its example ID or says "(assumed)"; the last task group is a hallway test) offered by the playbook when `openspec/` exists; hallway test after apply and before archive; the debrief flags "archived without a hallway test" | plugin (references, playbook, debrief) | small | done in 0.4 |
| 26 | Running without a person: what a simulated principal may confirm and what waits for a human; the simulated principal's persona comes first, before the interview | plugin (requirements, walkthrough, playbook) | small | done in 0.4 |
| 27 | One canonical location, `design/`, in all skills; "the ledger" means the project's own `design/kaizen.md`; the handover check gains "may the build start, on which assumptions" | plugin | small | done in 0.4 |
| 28 | Tester brief: name the input formats the tester invented and how long it waited before calling something permanent; ask "your caller" instead of `to: "main"` | plugin (references) | small | done in 0.4 |
| 29 | Narrow the kaizen skills' trigger descriptions against `openspec-explore`; suggest not installing `openspec-explore` where kaizen is installed | plugin; guide | small | done in 0.4 |

Done the same day: the tester brief templates told testers to write `REPORT.md` while the skill said "final message" (introduced in 0.4, found by condition C); fixed in `ca62d8c`, with "half the effort outside the coverage list".

Independent review of the branch (2026-11-05, one Opus agent that did not write it, triggered by the standing instruction on changes beyond a few hundred lines): 24 findings, four high, all in `transcript.py` and verified by the main session: rendering crashed on messages the person queued mid-turn (the case the script was written for), an option before the ID selected another session, harness text was counted and labelled as the person's, and exports could land where git tracks them. All fixed and tested the same day, with the medium and low findings on consistency, locations, duplicated text and the plugin's own record; one finding (internal details in this public repository) waits for the principal.

| # | Proposal | Destination | Effort | Decision / status |
|---|---|---|---|---|
| 31 | A ledger in a public repository carries no details of other projects (transferred to their backlogs) and no security findings or secrets, not even as to-dos (review finding 17: two entries named internal details of other projects) | plugin (debrief) | small | done in 0.4 |
| 32 | Discovery before the interview: an optional free interview such as `grill-me` (Matt Pocock) leads into `requirements`; the interview asks in rounds of unblocked questions with recommended answers (adapted from `grilling`); the form's section order is a checklist, not an order | plugin (playbook, requirements) | small | done in 0.4 |

## Earlier recommendations

The 2026-11-03 debrief (data-management-system) made seven proposals and five coaching points; their status after the week, as seen in the seven sessions: proposals 1, 3, 5, 6 acted on; 2 and 4 recurring in four sessions each (escalated, proposals 14 and 15 above); 7 done but its table row never closed. Coaching 1, 3, 5 acted on; 2 and 4 partly. Details in that repository's debrief history.

## Skill friction

- 2026-11-03, hallway-test (devvm): the by-eye tester refused to write `REPORT.md` under a harness rule; screenshots were dropped when the main session rebuilt the report. Fixed in 0.4 (report as final message).
- 2026-11-03, hallway-test (devvm): expectations-before-running could not be checked afterwards; the tester's transcript has no text and the first command ran in the first minute. Fixed in 0.4 (expectations file, timestamp).
- 2026-11-03, hallway-test (devvm): no requirements document existed; the tester invented a one-line requirement. Fixed in 0.4 (say so before the test).
- 2026-11-04, requirements (Nextcloud upgrade): the facts were gathered before the interview; the agent improvised a `[record]` marker and pre-filled drafts. Fixed in 0.4 (mode "the record").
- 2026-11-04, requirements (Nextcloud upgrade): 2.9 was never asked; the handover had no list of unconfirmed items; the person did not review the text, so 32 record items counted as confirmed downstream. Fixed in 0.4 (handover check).
- 2026-11-04, requirements + walkthrough (crawler chain): the two skills say nothing about being used together; the agent merged them into one plan that worked. Fixed in 0.4.
- 2026-11-04, walkthrough (crawler chain): "what exists" meant documents; running the stack was the agent's idea and the main source. Fixed in 0.4.
- 2026-11-04, walkthrough (crawler chain): a real admin was present and the walks' questions were not put to them; the confidence line stayed "simulated" after the owner answered. Fixed in 0.4.
- 2026-11-04, walkthrough (crawler chain): walk C (a fresh agent diagnosing injected faults) had no template; the injected datestamp had microseconds the crawler never writes. Fixed in 0.4 (diagnosis brief, "faults must look real").
- 2026-11-04, requirements by hand (devvm retcon): the reconstruction skipped 2.5 and 2.10, which bit within a day; quotes from a sub-agent were committed unchecked. Fixed in 0.4 (reconstruction mode names the sections a retcon skips; quotes verified).
- 2026-11-05, walkthrough (relayed from a colleague): personas were assumed without asking. Fixed in 0.4 (blocking step, stakeholder record).
- 2026-11-05, debrief (this plugin): transcripts were not under `~/.claude/projects`; `usage.py` over-counted 2 to 5 times; no renderer; the renderer written ad hoc dropped queued mid-turn messages; no multi-session mode. Fixed in 0.4.
- 2026-11-05, debrief (this plugin): the report was first written into the debriefed project's `docs/debriefs/`, which the principal found awkward (a subjective snapshot in the repository) and in the wrong repository (the debrief was about this plugin). Fixed in 0.4 (private report, ledger, repository that was debriefed).
- 2026-11-05, requirements (this plugin's own handover check): the unconfirmed items were first asked for by number only ("items 1 to 8"); the principal could not review them until they were quoted in full. Fixed in 0.4 (quote every item in the message).

## Notes for the next debrief

- 2026-11-05, principal: the probing interview helped to clarify their own thoughts; deferring questions as "currently open" or "for a later stage" should be encouraged. (Taken into the requirements skill.)
- 2026-11-05, principal: requirements, walk-through and hallway test intersect in the stakeholders; keep a separate stakeholder document: their desired experiences are requirements, their role is taken in a walk-through, the hallway test assumes their position. (Taken into the skills and the playbook.)
- 2026-11-05, principal: is the walk-through a method of requirements gathering or a thing of its own? An imagined walk-through and what happens in a hallway test would be interesting to compare; a walk-through also validates specs and implementation, which is what the hallway test does. (Pipeline stated in both skills; the merge question deferred, see `requirements.md` 2.2.)
- 2026-11-05, principal: retconning design documents worked very well in devvm: start by playing around, then use the evidence to formalise the product documents; they onboard new contributors, humans and agents, and prevent drift. (Reconstruction mode in the requirements skill.)
- 2026-11-05, principal: the intersection with OpenSpec was interesting; should they keep being used together? The impact of OpenSpec on the process cannot be judged, a lot happened behind the scenes. (Measurement proposed in the playbook: findings that cite a scenario; coverage from scenarios.)
- 2026-11-05, principal: humans and bots communicate in all directions now; humans need a clear, short executive summary, bots benefit from all the context. Two distinct cases: details endorsed by humans (the design documents made with the skills, where not reading them and focusing on outcomes was found good in the earlier debrief) and details attached without endorsement (an agent's analysis posted on an upstream issue). (Proposal 13.)
- 2026-11-05, principal: kaizen on kaizen means using personas, requirements, walk-throughs and the debrief on the plugin itself, and keeping design documents to test the skills against; whether skills can have unit tests is a new question. (`design/` of this repository; `testing.md`.)
- 2026-11-05, principal: a colleague found `grilling` good for discovery (from nothing to something specific) and the requirements skill good for tightening a loose idea; one leads into the other. (Proposal 32.)
- 2026-11-05, principal: the order of the demand and requirements form does not matter (the principal wrote it at ER-C; ER-C does not require it); the plugin gives it a second life as a checklist, from the insight that the tools and processes that keep large organisations on track also help with agents. (Proposal 32.)
- 2026-11-05, principal: requests phrased as questions mean the principal is unsure and wants pushback; three were taken as instructions in this session. (Proposal 30.)
- 2026-11-05, principal: the trial material becomes a benchmark for future development; its results are not known-good, they make visible how changes in the input influence the output; real-world testing is authoritative. (`benchmarks/notes-tags/`.)
