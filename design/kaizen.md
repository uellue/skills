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
| 5 | Hallway test: report as the tester's final message, expectations file before the first run, record proposed for commit on the working branch, accepted lean versus shipped, diagnosis brief, documents and instruction files as subjects, experiment bookkeeping, vulnerability first | plugin | medium | done in 0.4 |
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
| 21 | Close the open items of the week in the projects concerned | other repos (backlogs) | small | transferred |
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

Independent review of the branch (2026-11-05, one Opus agent that did not write it, triggered by the standing instruction on changes beyond a few hundred lines): 24 findings, four high, all in `transcript.py` and verified by the main session: rendering crashed on messages the person queued mid-turn (the case the script was written for), an option before the ID selected another session, harness text was counted and labelled as the person's, and exports could land where git tracks them. All fixed and tested the same day, with the medium and low findings on consistency, locations, duplicated text and the plugin's own record; one finding (internal details in this public repository) was decided by the principal: generalised in the files, history kept.

| # | Proposal | Destination | Effort | Decision / status |
|---|---|---|---|---|
| 31 | A ledger in a public repository carries no details of other projects (transferred to their backlogs) and no security findings or secrets, not even as to-dos (review finding 17: two entries named internal details of other projects) | plugin (debrief) | small | done in 0.4 |
| 32 | Discovery before the interview: an optional free interview such as `grill-me` (Matt Pocock) leads into `requirements`; the interview asks in rounds of unblocked questions with recommended answers (adapted from `grilling`); the form's section order is a checklist, not an order | plugin (playbook, requirements) | small | done in 0.4 |
| 33 | Matt Pocock's skills as a complement like OpenSpec: the playbook checks for them, maps their steps onto its lifecycle (discovery, glossary, questionnaire, ADRs, spec path, retro, handoff), names the trade-off of installing the whole plugin; requirements, walkthrough, debrief and the decision record point to the matching skill; the README carries the paste-in line for projects that route with ask-matt | plugin; README | small | done in 0.4 |
| 34 | A hook in the plugin that adds the kaizen moments to the context when `/ask-matt` is typed; only if the paste-in line and the playbook's trigger description prove insufficient; plugin hooks to be verified first | plugin (hook) | small | parked |
| 35 | A hint-following mode for the hallway test: a first user who skims the README for commands and then follows only the program's output; the skim view (`scripts/skim.py`) enforces the laziness, every return to the documents is a break whose fix belongs in the program's output; a brief template (from a colleague's remark that the tester is too smart and not lazy enough, and that devvm's chain of hints broke off) | plugin (hallway-test, script, brief) | small | done in 0.4; first real use: devvm |

### 2026-11-05 (debrief of the 0.4 development session, with Matt Pocock's `retro` run alongside by an independent sub-agent)

| # | Proposal | Destination | Effort | Decision / status |
|---|---|---|---|---|
| 36 | Test suite for the scripts and skill texts (stdlib `unittest`): synthetic transcript fixtures (list-shaped queued prompt, several lines per message id, sub-agent metadata, rendered transcript inside a result, option before the id, export into a tracked folder); lint for frontmatter, referenced paths, dates in skill bodies, stale strings, table columns, description and body budgets; one check command | plugin (0.4) | small | done in 0.4 (`tests/`, `./check.sh`; 10 of the first 13 script tests fail on the pre-review scripts; the count grows with the suite) |
| 37 | Pre-commit hook running the check (CI if the repository gets Actions); "ready to push" quotes its output | plugin repository | small | done in 0.4 (`.githooks/pre-commit`, enabled with `core.hooksPath`; `.github/workflows/check.yml`) |
| 38 | Short `CLAUDE.md` for this repository: pointers, the check command, claims about Claude Code verified with `claude-code-guide` or `--help` and cited, the review threshold | plugin repository (0.4) | small | done in 0.4 |
| 39 | `CODING_STANDARDS.md` for the reviewer, judgement calls only: one meaning in one place; skills self-contained under the plugin root; procedure, not history | plugin repository | small | done in 0.4 |
| 40 | `transcript.py render` indents result bodies so that text inside a result cannot pass for a header | plugin (0.4) | small | done in 0.4 |
| 41 | `retro` is user-invoked: the person types it as its own command, or its skill text goes to an independent sub-agent and the two reads are compared; no slash command inside another command's arguments | plugin (0.4: debrief, playbook) | small | done in 0.4 (debrief, playbook) |
| 42 | Multi-session readers get an explicit model (sub-agents inherit the main loop's); Opus by default | plugin (0.4: debrief) | small | done in 0.4 (debrief) |
| 43 | The plugin's next change through its own moments: decision record with a size budget, the two walk-throughs (a colleague's first debrief; the maintainer changes a skill), a first hallway test in real use; steps the agent offers go to the ledger | plugin backlog (0.5) | medium | partly done in 0.4: decision record `design/changes/kaizen-0.4.md` (after the fact, with the size budget now enforced by the lint); walk-throughs `design/walkthroughs/` (without a person; their questions answered in the requirements round of 2026-11-05); open offers captured by the debrief; the first hallway test in real use follows the release |
| 44 | Standing instructions at user level on the maintainer's host, so that they reach every checkout (partial answer to 19) | maintainer's configuration | small | done (the maintainer's `~/.claude/CLAUDE.md`, a copy of the README block; keeping the two in step is by hand). The README block gained "never delete through a shell variable that could be empty", from the `rm -rf` through unguarded variables that the safety check stopped in the 0.4 session |
| 45 | Pre-push hook checking outgoing commits against a local, uncommitted denylist | plugin repository | small | done in 0.4 (`.githooks/pre-push`; the denylist in `.git/info/denylist` starts empty) |

Third independent review (2026-11-05, the commits after `99eeff3`, about 725 lines, one Opus agent with the diff and the design record only): ready after fixes; 13 findings, all addressed the same hour. The pre-push hook let commit message bodies and invalid patterns through and refused removals of already-public lines (all reproduced; fixed, with tests); the debrief's session choice contradicted its own numbers step and had no rule for a first debrief or an in-session debrief; requirements answered in the round were not yet in the skill (feedback from other projects) or not built (E16, now marked so); the design record was stale after the round; the coverage report counted IDs in its own test's fixture text. Not changed: `actions/checkout` stays pinned by tag (its commit SHA was not verified here), and the pre-commit hook checks the working tree, not the index (documented in the hook).

Status changes from this debrief: 15 and 17 recurred in this repository too (escalated, 37, 38, 44); 30 held for the rest of the session after adoption; 2 and 3 used for real and held, gaps in 40–42.

### 2026-11-05 (hallway test of the plugin from the README: a new colleague with an SEM project, `design/hallway/2026-11-05.md`)

| # | Proposal | Destination | Effort | Decision / status |
|---|---|---|---|---|
| 46 | Hardware safety from the start: questionnaire 2.11 names the instrument and who authorises moves, 2.3 asks for a simulator that enforces the limits, Release names the instrument's owner; the playbook's build step, the measured walk and the decision record point to the hallway test's hardware rule | plugin (0.4) | small | done in 0.4 |
| 47 | One test for discovery versus the requirements interview (can the person name who needs it and what they would do differently?), in the playbook; `grill-me` wraps `grilling` | plugin (0.4) | small | done in 0.4 |
| 48 | Every skill's ledger line announces the ledger the first time | plugin (0.4) | small | done in 0.4 |
| 49 | `version.py --stamp` refuses outside a git checkout; the version line says what to compare | plugin (0.4) | small | done in 0.4, with a test |
| 50 | A persona "described by <who>"; README: the debrief comes after a stretch of work | plugin (0.4) | small | done in 0.4 |
| 51 | A feasibility path: "can an agent do this at all?" as a five-line need note and a throwaway prototype against a simulator, before the full form | plugin backlog (0.5) | small | proposed |
| 52 | The decision record says that a new project's first build counts as a change | plugin backlog (0.5) | small | proposed |
| 53 | Keep this test as a rerunnable self-test of the plugin (`benchmarks/plugin-newcomer/`), with a brief that forbids the tester from volunteering the risk under test | plugin | small | done in 0.4 (principal, 2026-11-05); then (principal: "I'd like easy tooling to test and re-test the plugin itself") the levels named in the brief (the plugin under test, the scenario only input), scenarios as files (`sem-instrument`, `existing-tool`), `brief.py`, and the project skill `/plugin-selftest`; the hallway-test skill says that a plugin or process is tested with a scenario that is not the subject |

Fourth independent review (2026-11-05, the commits after `849cd7e`, about 417 lines, one Opus agent with the diff and the design record): ready after fixes, no high findings. Fixed the same hour, each with a test that fails on the old code: a quoted "Text id" ahead of the real line hid a stale id; an edit without `--stamp` printed a new id labelled "current text", so `/reload-plugins` would loop; any enclosing git repository passed as the maintainer's checkout; `--stamp` stopped half-way on a malformed id; the pre-push hook ignored file names (now added files only). Also: a failing version line no longer blocks a skill; the ledger rule and the discovery test are pointers to the playbook instead of copies; the record and the first result corrected. **Deviation from an accepted lean:** the hallway test's hand-over (`cf6f9c6`, accepted as "if nothing is built yet or no requirements exist, stop") now stops only when nothing is built; with something built and no requirements it says so, offers the playbook and goes ahead if the person wants, because the accepted wording refused most real tools. Open for the principal: whether every skill run should show the version line to the person, or only on a mismatch or in a checkout (one tool call per run either way).

### 2026-11-05 (self-test rerun at `d30ceac`, `benchmarks/plugin-newcomer/results/2026-11-05-sem-instrument-2.md`)

Applied as leaned (principal, 2026-11-05).

| # | Proposal | Destination | Effort | Decision / status |
|---|---|---|---|---|
| 54 | Hardware with no simulator: the decision record gets a required row "develop against what"; building or faking a simulator is planned work with its own must-examples, among them "it enforces the instrument's limits" | plugin (change-record, playbook) | small | done in 0.4 (principal, 2026-11-05: "go with your leans") |
| 55 | Labelling simulated output in the build step, the decision record's hardware sentence and questionnaire 2.3, not only in the hallway test | plugin | small | done in 0.4 (principal, 2026-11-05: "go with your leans") |
| 56 | No recommended answer for safety limits, authorisation and the owner (2.11, Release), or mark accepted recommendations there as `[assumed]` | plugin (requirements) | small | done in 0.4 (principal, 2026-11-05: "go with your leans") |
| 57 | A shared ledger template in `references/`, named by every skill's ledger line | plugin | small | done in 0.4 (principal, 2026-11-05: "go with your leans") |
| 58 | One session-start line in the playbook: work that acts on hardware names the owner and whether a simulator exists before planning | plugin (playbook) | small | done in 0.4 (principal, 2026-11-05: "go with your leans") |
| 59 | A cost note for the full path, and a feasibility spike between requirements and the decision record (with ledger 51) | plugin backlog (0.5) | small | planned for 0.5 (principal, 2026-11-05: "go with your leans") |
| 60 | `version.py <skill> <expected id>` prints "current" or "older text: run /reload-plugins", so the person reads a verdict, not two ids | plugin | small | done in 0.4: the script gives the verdict and is silent unless it matters (principal, 2026-11-05: only where it could be relevant) |
| 61 | Smaller: one debrief per session for several first uses; the exact invocation of `grill-me`; the requirements handover lists questions for an absent owner as a deliverable to send | plugin | small | done in 0.4 (principal, 2026-11-05: "go with your leans") |

The hallway test's hand-over deviation (stop only when nothing is built) was measured in the existing-tool scenario (N14 held) and kept by the principal, 2026-11-05.

### 2026-11-05 (self-test, scenario existing-tool, `benchmarks/plugin-newcomer/results/2026-11-05-existing-tool.md`)

The run supports keeping the hallway test's current hand-over (stop only when nothing is built): with something built and no requirements, the newcomer was told and could go ahead; the wording first accepted would have looped back to the playbook. Decision (principal, 2026-11-05, "go with your leans"): the current hand-over stays. The proposals below were applied as leaned.

| # | Proposal | Destination | Effort | Decision / status |
|---|---|---|---|---|
| 62 | hallway-test, before launching: state the model, the expected cost and the duration, and wait | plugin (hallway-test) | small | done in 0.4 (principal, 2026-11-05: "go with your leans") |
| 63 | No stakeholder record: one question ("who uses it first, what do they already know?"), marked "not on record" in the brief; the tester template loses its default persona | plugin (hallway-test, tester-brief) | small | done in 0.4 (principal, 2026-11-05: "go with your leans") |
| 64 | The tester template gets an optional sentence: "no requirements exist; your expectations are your own, mark them as such" | plugin (tester-brief) | small | done in 0.4 (principal, 2026-11-05: "go with your leans") |
| 65 | A playbook path "existing tool, before its first hand-over": the hallway test now, a requirements retcon afterwards from its findings; the README's first steps name the hallway test for a working tool | plugin (playbook, README) | small | done in 0.4 (principal, 2026-11-05: "go with your leans") |
| 66 | No loop: the hallway test offers the playbook only if it has not run in this session | plugin (hallway-test) | small | done in 0.4 (principal, 2026-11-05: "go with your leans") |
| 67 | Questions during a run: with no design, the owner answers; ask whether they stay available or collect the questions for afterwards | plugin (hallway-test) | small | done in 0.4 (principal, 2026-11-05: "go with your leans") |
| 68 | The mode is chosen with the person (behaviour, impatient user, by eye, ...), with a recommendation | plugin (hallway-test) | small | done in 0.4 (principal, 2026-11-05: "go with your leans") |
| 69 | A short walk-through offered when the person cannot name the coverage; the debrief offered at the end of a first use | plugin (hallway-test) | small | done in 0.4 (principal, 2026-11-05: "go with your leans") |

Fixed while grading: `usage.py` and `transcript.py` run from a subdirectory of the checkout found no sessions; they now also look under the checkout's root (test added).

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
- 2026-11-05, debrief 0.4 (first real use): `locate`, `render` and `usage` worked on the first call; rendered text inside a tool result looks like a real header (40); readers inherited the top model (42); `retro` cannot be called by an agent and the suggested prompt nested it in the debrief's arguments (41).
- 2026-11-05, walkthrough (two walks of the plugin by a sub-agent, no person, no edits allowed outside its files): the closing duties (friction line, stakeholder-record update, persona confirmation) assume the walker may write and a person is there; no variant for a read-only caller without a person; the template has no place to say that "what exists" changed during the walk (the check appeared mid-walk); a measured walk was impossible because the process installs a plugin and reads transcripts.
- 2026-11-05, requirements (handover check, by hand): confirm-items mixed with open questions in one message; the questions were answered, the items were not.

- 2026-11-05, requirements (round on the walk-throughs' open questions): two recommendations used terms the principal did not know ("checkout or installed version", "behaviour fixture") and cost a round each; the skill asks for the person's words in the answers but has no rule to put the questions in the person's words, with an example of what a term means.
- 2026-11-05, hallway-test (dry run for a new colleague who wants an agent to operate a scanning electron microscope; made-up answers, nothing launched): with nothing built and no requirements, the skill only says "say so" and does not hand over to the playbook, so a newcomer pointed at it starts at the wrong moment; "what must not be touched" covers a read-only mount but not hardware: an instrument needs "simulator or dry run only unless the owner says otherwise" and a check that the simulator enforces the instrument's limits.
- 2026-11-05, hallway-test (second dry run, same colleague, through the whole lifecycle): the session ran the skill text from before `cf6f9c6`, because edits reach a running session only with `/reload-plugins`, and nothing showed which version ran (E16 observed live; fixed in 0.4: each skill carries a text id kept current by the check and starts by comparing it with `version.py`); a simulator-backed test should say that simulator output is labelled as such and never presented as a real measurement. (In the hallway-test skill since 0.4.)
- 2026-11-05, hallway-test (sub-agent as a new colleague with an SEM project, from the README, made-up answers): the setup cannot show whether the plugin raises a risk by itself when the tester supplies the answer itself; a brief for a "does the process raise X" question should forbid the tester from volunteering X and count whether a skill asked. Record: `design/hallway/2026-11-05.md`.

## Notes for the next debrief

- 2026-11-05, walk-throughs of the plugin (`design/walkthroughs/`; answered the same day in the requirements round): 13 open questions for the principal, among them which sessions a debrief takes when none is named, whether it may write into a colleague's repository before the private report is ignored there, its expected cost, the minimum Python (the scripts need 3.10), what must be green before a release, and how a session runs the checkout's skills rather than the installed ones.

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
- 2026-11-05, colleague (relayed by the principal): the hallway tester is potentially too smart (reading comprehension, attention span, context window) and not lazy enough. Real first users read the README TL;DR-style, copy the first command that looks right, and then follow the program's hints, as git and the Rust compiler make easy; in devvm the chain worked in places, broke off elsewhere, and having to read the README was annoying. (Proposal 35.)
