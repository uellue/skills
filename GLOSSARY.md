# kaizen

The vocabulary of the kaizen plugin and of its development in this repository, where the plugin is also used on itself. The skills and the README speak to their users in these words. A term from another tool carries its namespace ("OpenSpec scenario", "Matt Pocock's `retro`") wherever the local meaning would be read otherwise. The plugin explains the words its users meet in `plugins/kaizen/references/words.md`, in plain words; that list must agree with this file.

## Language

### People

**Principal**:
The person who decides for a project and reviews its work; often also the agents' manager.
_Avoid_: user, boss, owner

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
_Avoid_: backlog, log, kaizen file

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

**Skill friction**:
One line, written at the end of a skill's run, on what in the skill did not fit the situation.
_Avoid_: bug report, feedback

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

### Testing and review

**Hallway test**:
A first-user trial: a fresh agent that sees only what a first user would see tries a subject and reports what broke or surprised it.
_Avoid_: play test, usability test, user test

**Subject**:
What a hallway test, a review or a debrief judges.
_Avoid_: target, system under test

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

**Fixture**:
The prepared input of a skill test: a transcript with planted moments, a tool with planted defects, a scripted principal with withheld facts, a self-test scenario.
_Avoid_: behaviour fixture, test data

**Behaviour mode**:
The hallway test's mode in which the tester builds inputs, writes its expectation for each, runs the subject and compares; the other modes are by eye, diagnosis and hint-following.
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
