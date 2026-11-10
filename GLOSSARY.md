# kaizen

The vocabulary of the kaizen plugin and of its development in this repository, where the plugin is also used on itself. The skills and the README speak to their users in these words. A term from another tool carries its namespace ("OpenSpec scenario", "Matt Pocock's `retro`") wherever the local meaning would be read otherwise. The plugin explains the words its users meet in `plugins/kaizen/references/words.md`, in plain words; that list must agree with this file.

## Language

### People

**Principal**:
The person who decides for a project and reviews its work; often also the agents' manager.
_Avoid_: user, boss, owner

**Stakeholder**:
Anyone with a stake in the tool: its users, its maintainer, the owner of what it touches, the readers of what it produces.
_Avoid_: user (for the whole set), party

**Persona**:
A described stakeholder whose position a walk-through or a hallway test takes, with how much of the description was confirmed by the people it describes.
_Avoid_: user story, role

**Manager**:
A person who leads coding agents, the way a line manager leads a team; the persona the plugin is mainly written for.
_Avoid_: operator, lead

**Maintainer**:
Whoever changes the plugin's skills, scripts and references.
_Avoid_: developer, author

**Owner**:
The person who may authorise work on a real thing and who sets its limits.
_Avoid_: admin, responsible

### Records

**Ledger**:
The project's committed list of proposals with their decisions, skill friction and notes for the next debrief.
_Avoid_: backlog, log, kaizen file (as its name: "backlog" is the project's own list of work, such as its issues; `words.md` may say "the backlog for how the work is done" to explain the ledger to a newcomer)

**Proposal**:
A numbered change in the ledger, with a destination, an effort and a decision.
_Avoid_: recommendation, suggestion, action item

**Finding**:
An observation that cites a moment and names its cause; a finding can be right while the proposal drawn from it is wrong.
_Avoid_: issue, problem, bug (unless it is one)

**Lean**:
The agent's preferred answer to an open question or decision, stated alongside it so that "yes" accepts it; an accepted lean is a decision.
_Avoid_: recommendation, recommended answer, default, suggestion

**Open offer**:
Steps the agent offered that the principal neither took nor dropped.
_Avoid_: pending item

**Revisit**:
A record item kept for a later look, always with its trigger ("revisit when the suite covers a second skill"); without a trigger it is never looked at again.
_Avoid_: Wiedervorlage, bring forward, BF, tickler, "later" without a trigger

**Skill friction**:
One line, written at the end of a skill's run, on what in the skill did not fit the situation.
_Avoid_: bug report, feedback (that is what people say, below)

**Feedback entry**:
What a person said about working with the plugin, positive or negative, kept as a primary source for goals: verbatim and private in `.claude/debriefs/feedback-raw.md`, cleaned in `design/feedback.md` with its effect (a ledger row, a rule, a test, or none yet).
_Avoid_: complaint, praise, user voice

**Acceptance example**:
A concrete situation and its observable outcome, with an ID, a priority and the walk step or requirement it came from.
_Avoid_: test case, scenario, user story

**Use scenario**:
A step-by-step account of who does what with the software, in section 2.1 of the requirements; the walk-throughs supply them.
_Avoid_: scenario (unqualified), use case

**OpenSpec scenario**:
A case in an OpenSpec specification; in a project that uses OpenSpec, each must-example becomes one and cites its ID.
_Avoid_: scenario (unqualified), spec scenario

**Decision record**:
The short record of what was decided for a change: interface, decisions with who decided, must / should / won't with a size budget, blocking questions.
_Avoid_: change record, spec, design doc, ADR

**Need note**:
The first five lines of a decision record: whose need, what the request names, the need behind it; on the small path it is written first and the record grows around it.
_Avoid_: problem statement, intro

**Small path**:
The process sized for a small change: the need note, one or two personas, one walk-through as a step table, the examples, the decision record, the hallway test; no full requirements form.
_Avoid_: small-change path, lite mode, fast track

### Testing and review

**Hallway test**:
A first-user trial: a fresh agent that sees only what a first user would see tries a subject and reports what broke or surprised it.
_Avoid_: play test, usability test, user test

**Field test**:
A real person, the participant, tries a subject for real in their own environment (real data, a real machine, an issue from real use), and the agent reads what happened: live, through channels both checked before the run, talking about it as it happens (the field-test skill, 2026-11-10), or afterwards from what they send back (a recording, notes in the moment, a report they approved); a brief gives the start and the method when the participant is someone else; inside it, the usability-testing terms task scenario, think-aloud, moderated and unmoderated apply (requirements, topic ledger 269).
_Avoid_: human trial (it reads as a clinical trial), human-in-the-loop test, user test, human hallway test

**Subject**:
What a hallway test, a walk-through, a review or a debrief judges: a tool, a document, a process, or the plugin itself.
_Avoid_: target, system under test, the thing (it reads as the real thing)

**Self-test scenario**:
A project a persona brings into a self-test; it is input, never the subject.
_Avoid_: scenario (unqualified), use case, example project

**Self-test**:
A hallway test whose subject is the kaizen plugin itself, with a self-test scenario as input, graded against the key.
_Avoid_: hallway test of the plugin, quick tests, smoke test

**Key**:
The list of key items a skill test is graded against, written before the runs it grades.
_Avoid_: rubric, expectations

**Pre-commit check**:
What runs without an agent before every commit and in CI: unit tests of the scripts and the git hooks, lint of the skill texts, references and manifests, and a report of the acceptance examples no test cites.
_Avoid_: check (unqualified), quick tests, CI, unit tests

**Skill test**:
A run of a skill by a fresh agent on a fixture, graded against a key written before the run; it shows whether a change to the skill made it better or worse. A self-test is a skill test of the whole plugin.
_Avoid_: behaviour test (that is the hallway test's behaviour mode), eval, benchmark

**Eval suite**:
The skill tests that `claude plugin eval` runs: its own term, kept for its files and commands (`plugins/kaizen/evals/`). Each case is a prompt, a fixture and graders; it runs with the plugin (the with-arm) and without it (the without-arm, the baseline).
_Avoid_: eval (unqualified, for a skill test in general)

**Grader**:
One check of an eval case, named after the rule of the skill it checks; free (a pattern, a tool call, a file) or judged by a model against PASS and FAIL conditions.
_Avoid_: assertion, key item (that is the self-test's key)

**Rule ablation**:
A skill test run on a copy of the plugin with one rule removed, its expected effect written down before the run (`benchmarks/rule-ablation/`); it shows whether, and how, that rule acts in a situation.
_Avoid_: leave-one-out (unqualified)

**Fixture**:
The prepared input of a skill test: a transcript with planted moments, a tool with planted defects, a scripted principal with withheld facts, a self-test scenario.
_Avoid_: behaviour fixture, test data

**Coverage (of a skill)**:
Which rules of the installed texts (skills, references, standing instructions) a skill test or a session exercised, and in which situations: the rule fired, held or was broken, or did not apply. Like code coverage, with the parameter space (the situations a rule meets) counted, not only whether it ran.
_Avoid_: usage (that is whether a skill was invoked at all)

**Expected effect**:
What a change to a skill text should move, named before the next skill test: a key item or an observable behaviour. The test marks it confirmed, not confirmed, or side effect elsewhere.
_Avoid_: prediction (unqualified), hypothesis

**Kept improvement**:
A change to a skill that a later skill test or real use confirmed and that was not reverted; counted per activity (review, real use, self-test) against the tokens it cost.
_Avoid_: fix (unqualified), finding

**Behaviour mode**:
The hallway test's mode in which the tester builds inputs, writes its expectation for each, runs the subject and compares; the other modes are by eye, diagnosis, hint-following and documents.
_Avoid_: behaviour test (unqualified)

**Independent review**:
A review by an agent that wrote none of the change, briefed with the diff and the record, ending in a verdict.
_Avoid_: code review (unqualified), second opinion

**Walk-through**:
A step-by-step pass through a process in a persona's shoes, imagined or against the running system, that yields questions and acceptance examples.
_Avoid_: walkthrough test, simulation

**Debrief**:
A review of how a person and agents worked together over a stretch, with cited moments, coaching and proposals.
_Avoid_: retro, retrospective, post-mortem

### Safety

**Real thing**:
Anything a tool could damage or that could cause harm: an instrument, production or irreplaceable data, a live service, messages to real people.
_Avoid_: production, prod, hardware (too narrow)

**Stand-in**:
What work runs against instead of the real thing: a simulator, a copy of the data, a preview or staging service, a dry run.
_Avoid_: mock, fake, sandbox

### The plugin on itself

**Kaizen on kaizen**:
Using the plugin's own moments (requirements, walk-throughs, hallway tests, debriefs) to improve the plugin.
_Avoid_: dogfooding, self-improvement

**Level**:
Where a step sits when the plugin is used on itself: the plugin as subject, the self-test scenario as input, or one of the plugin's skills as a step inside that scenario.
_Avoid_: recursion, meta

**Text id**:
A short fingerprint of a skill's text, which tells a session that it runs an older text than the one on disk.
_Avoid_: version, hash

### Updates

**Standing instructions**:
The block of rules for the agent that a project copies into its `CLAUDE.md` or `AGENTS.md`, merged with its own rules; its first line is the version line.
_Avoid_: working rules (a project's own heading for it), the paste block

**Version line**:
The first line of the standing instructions, naming the plugin version they are from; the record of which version a project last applied.
_Avoid_: version stamp, header

**Update** (of a project):
Bringing a project's records up to the installed plugin with `/kaizen:update`, after the plugin itself was updated (`claude plugin update`); the two are different steps.
_Avoid_: upgrade, migration (for the skill's work)

**Sync**:
`/kaizen:sync`: bringing a project and its upstream in step in both directions (the tracker read and the ledger updated; the inbox routed; what waits to go out posted on a yes).
_Avoid_: pull, refresh

**Inbox**:
The ledger's notes section in its role of holding ideas dropped during work until a sync or a debrief routes each to its place, leaving only the link.
_Avoid_: slush pile, scratchpad

**Changes for projects**:
`references/changelog.md`: per plugin version, what a project adopts, changes or keeps; not the plugin's own history.
_Avoid_: release notes
