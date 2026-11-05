# Demand and requirements: the kaizen plugin

Author: Claude (Fable 5.1), with the principal. Principal: Dieter Weber. Date: 2026-11-05. Interviewed: from the record, every item confirmed by the principal on 2026-11-05 in the handover check; (the running notes `docs/working-with-claude.md` of the data-management-system repository, the debriefs of 2026-11-03 and 2026-11-05, seven session transcripts of 2026-11-03 to 11-05) and the principal in person (feedback of 2026-11-05).
Markers per item: [answered] said or confirmed by the principal; [record] taken from the sources above, not yet confirmed; [assumed] proposed by the author; [unknown] with what would resolve it; [deferred] with stage and owner.

## 1. Demand

### 1.1 Problem and context
- [answered] Working with coding agents is onboarding a new employee every session: it knows only the repository and its instructions. What keeps a human organisation coherent (decisions written down, a backlog, conventions, a reviewer who did not write the code, a retrospective) works for agents for the same reasons, and had to be done by hand on every project. (Guide, "The picture".)
- [answered] The standing meta-goal is a process that improves our processes; the debrief is its instrument, and the plugin is where practices that happened by hand more than once are kept as documented, invokable procedures. (Guide, "Regular debrief"; principal 2026-11-05: "We should always do kaizen on kaizen".)
- [answered] The demand and requirements form behind the requirements skill was written by the principal at ER-C; it is not an institute requirement. Agents give it a second life, because the tools and processes that keep large organisations on track also keep agents on track. (Principal, 2026-11-05.)
- [answered] Lessons otherwise land in chat, in a per-checkout memory that a worktree or a VM does not see, or nowhere; in the first week, a dozen lessons were lost that way (debrief 2026-11-05).
- [answered] What happens if nothing is done: agents are a vast power we are only starting to explore. They can create gigantic messes and dig holes to fall into, or create and improve things of exceptional power, utility and quality orders of magnitude cheaper than before, in a short week what took years and a large team. Driving agents effectively is a very different skill from developing oneself: the issues that appeared with one's own work over months and years now hit after a one-hour session. High-level management skills (work on the process, not the problem; leadership and communication; clarity of thought and intent; clear documentation and project structure) are the key, and must now be mastered on day one, as a junior in any job, where before they were skills of senior managers that few people in an organisation had to master. Without the plugin, those skills stay in one person's head and guide, colleagues learn them the expensive way, and the agent's lessons keep dying with sessions. (Principal, 2026-11-05.)

### 1.2 Current solutions
- [answered] Prior art checked 2026-11-03: `debrief` (Wavez) and `retrospective` (florianbuetow) for the debrief; `cli-ux-tester` (ali5ter) and `user-testing-agents` (dekic648) for the hallway test; Feature Forge (jeffallan) and melodic-software's elicitation skills for requirements and walk-throughs; Anthropic's `code-review`, `feature-dev`, `session-report`. None starts from the project's requirements, writes expectations before running, asks the manager questions during a test, judges a real terminal by eye, or verifies findings adversarially; those are kept as ours, and attributed pieces are borrowed (the four check groups, the two hats, the eleven CLI criteria, the lower-confidence rule for simulated stakeholders). (Guide, "Prior art for the four pieces".)
- [answered] OpenSpec is used as the specification method on the data-management-system project and is still under evaluation. The principal's impression is that it helped to structure the process, but could not tell whether the difference came from their prompts, their standing instructions, the skills of this plugin, or OpenSpec; with OpenSpec alone they missed the skills developed here. The plugin sits before it (stakeholders, requirements, walk-throughs) and after it (hallway test, debrief). A critical review of the skills stand-alone, compared with OpenSpec, and used together with OpenSpec was started 2026-11-05 (sub-agents on Opus 5.5; result to be recorded here). (Principal, 2026-11-05.)
- [answered] Matt Pocock's skills (github.com/mattpocock/skills, MIT; recommended by a colleague): treated like OpenSpec, a useful complement: recommended, checked for presence, mapped in the playbook, never depended on. Their suite is a lifecycle of its own (router, specification path, review, retrospective), and installing their plugin brings eleven skills that start on their own, so the playbook recommends specific skills (`grill-me` or `grill-with-docs`, `domain-modeling`, `to-questionnaire`, `handoff`, `retro`) and keeps the full mapping and names the trade-off. A colleague found `grilling` good for discovery and the requirements interview good for tightening a loose idea. (Principal, 2026-11-05.)
- [answered] Observations from that comparison, one run per condition and not graded blind, so indications rather than results (2026-11-05, three Opus agents on one toy CLI and one change request; reports in the session's scratchpad, not kept): the content (the need behind the requested solution, two measured causes of lost notes, the locking question that decided the design) came from the walk-through and the requirements habits in both kaizen conditions; OpenSpec contributed order, gates, structural validation and the rule not to touch code while planning; the links from example to scenario to test came from the principal's own `config.yaml` rules, which belong to neither tool, which explains why the effect could not be attributed. The hallway test was the most valuable stage in every condition that ran it: data-loss defects outside all scenarios, after validation passed and tests were green. `openspec validate --strict` accepts a one-line proposal and an untestable scenario (verified). Without a specification step, an implementer working from the kaizen documents alone invented 21 decisions that had no home. Conclusion of all three reviewers: keep both with a stated hand-off; give the kaizen skills a minimal decision record of their own that maps onto OpenSpec's design and scenarios; one list of acceptance examples with IDs; a small-change path.

### 1.3 Benefits
- [answered] A hallway test found 12 verified defects in 14 minutes and about 46 k sub-agent tokens on devvm (2026-11-03); the crawler play test found twenty experiments' worth of behaviour in an afternoon, including defects the test suite had enshrined.
- [answered] A requirements document written by the skill in 87 minutes served as the live specification of the next session, which cited it while working and wrote measured results back (Nextcloud upgrade, 2026-11-04).
- [answered] The interview clarified the principal's own thoughts and raised things to consider; deferring questions as open or for a later stage kept it moving (2026-11-05).
- [answered] A debrief across seven sessions found a measurement error in its own instrument (tokens over-counted 2 to 5 times) that every earlier cost judgement rested on.
- [answered] Estimated productivity so far: about a factor 10, much of it still invested in learning, tooling and process (such as this plugin). Quality can improve a lot (a security bug in a deployment was found by a probe against the real back-end), but the work carries more process. It is a dynamic equilibrium: devvm would not have reached its current power without these tools; without them the principal would have used libvirt directly or written a short bash script. (Principal, 2026-11-05.)
- [unknown] Figures for time saved per week for a colleague who is not the author of the process. Resolves with a few weeks of ledger entries from someone else's project.

### 1.4 Users
See `stakeholders.md`: the manager, the colleague starting with agents, the coding agent, the fresh tester or reader agent, the plugin maintainer, the recipient of agent output outside the project.
- [answered] Audience, in order: the principal; their close colleagues; ER-C and other collaborators where it is the principal's job to lead the way, with adaptations for their needs; everyone else is invited to learn, benefit and contribute feedback and improvements, but the plugin is not developed to cater to them at this point. Colleagues use Claude Code or Codex (Codex reads `AGENTS.md` only; the skills are Claude Code's). (Principal, 2026-11-05.)

## 2. Requirements

### 2.1 Use scenarios
The lifecycle in the `playbook` skill: stakeholders → requirements → walk-throughs → specification (the project's method) → build → hallway test → debrief.
- [answered] S0, discovery: going from nothing to a more specific idea is a free interview, for example Matt Pocock's `grill-me` (a colleague found it good for discovery); the requirements interview then tightens the loose idea (principal, 2026-11-05). The order of the ER-C form's sections is not binding: the form is hardly used as written, and the plugin gives it a second life as a checklist (principal, 2026-11-05).
- [answered] S1, requirements interview: a few sections per round, pre-filled from the record, the person corrects rather than repeats; deferring is allowed and recorded with stage and owner; the result is handed over with a list of everything still unconfirmed.
- [answered] S2, reconstruction: a tool that grew from "just playing around" gets its requirements and specification retconned from git history, code, issues, hallway reports and transcripts, every item with a source, questions where the sources are silent; the documents then onboard humans and agents and prevent drift (principal 2026-11-05: "worked very well in devvm").
- [answered] S3, walk-through: a persona from the stakeholder record, confirmed with the user (never assumed), walks a process; against the running system where it exists; questions go to a real stakeholder when one is present; the walk feeds requirements 2.1 and the hallway test's coverage.
- [answered] S4, hallway test: a fresh sub-agent with only the requirements and user documentation; expectations in a file before the first run; report as its final message; the record goes to `design/hallway/` and its commit is proposed; "what would have caught it" per defect. [answered] The check of accepted leans against what shipped belongs to every hand-over (a standing instruction), not only to the hallway test (principal, 2026-11-05). Variants: by eye in a real terminal; diagnosis under injected faults; a README from a clean checkout; an instruction file as an eval with a pre-written key and a blind grader.
- [answered] S5, debrief: on a schedule, over one or several sessions, from transcripts wherever they are; a private report in `.claude/debriefs/`, a ledger in `design/` with only what is actionable; kaizen on the plugin itself becomes issues or merge requests on this repository.
- [answered] S6, "note for the debrief": a one-line capture into the ledger at the moment, sorted later.
- [answered] Frequency: the debrief and the "note for the debrief" daily or weekly; a requirements interview and walk-throughs once per project or larger change, and also on a specific topic whenever the need arises (open questions identified, an idea so far only general to be fleshed out), so the playbook has to judge what to do and what not to do at a given point; a hallway test per change a user would notice; a reconstruction once per tool that grew. (Principal, 2026-11-05.)
- [answered] S7, playbook: at the start of a project or change, say which moment this is, which documents are missing, and which skill writes them; propose, do not write unasked.
Acceptance examples: E1 to E6 in `examples.md`.

### 2.2 Demand uncertainties
| Uncertainty | Resolves by |
|---|---|
| [unknown] Whether skills can be tested with the harness's own eval mechanism (`claude plugin eval`) and in what format | the maintainer checks the documentation; `testing.md` |
| [unknown] Whether OpenSpec's scenarios improve the build | count review findings that cite a scenario; hallway-test coverage from scenarios (playbook) |
| [deferred] Whether walk-through stays a skill of its own or becomes the method inside `requirements`; kept separate for now with the pipeline stated | principal, after the next uses |
| [unknown] How lessons travel between checkouts, worktrees and VMs (memory is per path) | a seeding step in provisioning, or lessons kept in the repository; devvm's `setup-dev` |

### 2.3 Interfaces with existing systems
- [answered] Claude Code's plugin and skill format (`SKILL.md` with frontmatter, `${CLAUDE_PLUGIN_ROOT}`), its transcript JSONL (one line per content block, usage repeated per line; queued mid-turn messages as attachments), its sub-agent and SendMessage mechanics, its rules on what a sub-agent may write.
- [answered] The demand and requirements form (version 1.1, 2026) the principal wrote at ER-C, whose sections serve as a checklist; the order is not binding. ER-C does not require it.
- [answered] OpenSpec on the projects that use it; `AGENTS.md`/`CLAUDE.md` conventions; the projects' `design/` directories.
- [answered] Output that leaves a project (issues, merge requests, upstream comments): a short part for humans and details for agents, marked as endorsed by a human or attached without endorsement.

### 2.4 Operating conditions
- [answered] Sessions run on the host, in devcontainers, in devvm VMs and in worktrees; each has its own memory slug and sometimes no instruction file; transcripts are copied into checkouts for debriefs elsewhere. Tools for the by-eye test (xvfb, xterm, xdotool, imagemagick) are installed by the VM's provisioning.

### 2.5 Availability and reliability
- [answered] A wrong number from an instrument is worse than none: every model-and-effort judgement of the first two debriefs rested on tokens over-counted 2 to 5 times. Instruments are smoke-tested against one known case before use, and a reader's claim about an instrument is verified by the main session.
- [answered] A session can end at any moment (reboot, compaction, a refused turn); nothing the plugin does may depend on the end being seen. Capture is immediate, sorting is scheduled.

### 2.6 Performance
- [answered] Hallway test on a CLI: about 14 minutes and 46 k sub-agent output tokens (Sonnet by behaviour, Haiku by eye). Requirements interview: 87 minutes on Sonnet, 64 k output tokens. Debrief of seven sessions: about 1.5 M tokens of readers and an hour. Instruction-file eval, 12 cells: about 90 k tokens and two minutes.

### 2.7 Testing, installation and service
- [answered] Installed from the marketplace `uellue/skills` at user scope; devvm's `setup-dev` installs it in the VM. The maintainer is the principal.
- [deferred] Tests of the skills themselves: see `testing.md`; owner the maintainer, stage: before the next release after 0.4.

### 2.8 Portability and distribution
- [answered] Skills are Claude Code's; the briefs and templates are plain text and can be used by hand or by other tools; what must reach Codex users goes to `AGENTS.md` and the guide, not the plugin.

### 2.9 Jurisdictions
- [answered] Transcripts contain everything pasted into the chat, including credentials and personal data; exports stay out of version control. The coaching is private to the person debriefed and never enters the ledger. Names of people stay in the project's own record and out of anything published. Borrowed pieces are MIT-licensed and attributed.

### 2.10 Lifetime and decommissioning
- [answered] As long as the institute works with coding agents; the skills change with the harness, so each release is checked against the current Claude Code behaviour (sub-agent write rules, transcript format).

### 2.11 Safety and risks
- [answered] A reader or tester agent treats transcript and tool content as data, never as instructions; readers do not run commands found in transcripts. Grepping a session's own transcript for secret-like patterns has ended sessions; the export script copies and renders, it does not scan.
- [answered] A proposal is never applied without the person's approval; the debrief writes a report and a ledger entry only.
- [answered] Working principle: do not obsess about details in advance; fix unwanted outcomes when there are concrete examples, so the skills and their outputs change in response to evidence. This does not hold for security and safety, where care comes before the example. Decisions such as where the accepted-lean check lives are taken provisionally and changed later. (Principal, 2026-11-05.)

### 2.12 Applicable standards
- [answered] None binding. Followed by choice: the principal's demand and requirements form; the five-whys habit (Toyota); the organisation's rule against invented references.

## Release
Decides: the principal. Builds: the principal with Claude. Pays: ER-C (tokens). Signs off: the principal, per release.

## Open questions
- How to test a skill before shipping it, for the maintainer, resolves 2.7; deferred to the next release.
- Whether walk-through and requirements merge, for the principal, resolves 2.1; deferred until the next two uses.
- Where lessons live so that every checkout's agent sees them, for the principal, resolves 2.2; deferred to the devvm provisioning work.
