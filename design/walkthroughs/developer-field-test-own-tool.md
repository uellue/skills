# Walk-through: a developer field-tests their own tool with the field-test skill

Persona: "A developer field-testing their own tool" (`design/stakeholders.md`): takes a tool that has been cooking in simulation to its first real use on a shared test machine ("bare metal", other things on it; production later for some users), develops in a devvm VM with an agent, reaches the tool's services through forwarded ports, wants the project's work done first and reports plugin findings upstream on the side; empowered on the test machine. Confidence: answered by the principal, 2026-11-10, for the frame below; the steps are walked on paper by the agent (simulated) and rest on a field-test skill that does not exist yet (ledger 283).
What exists: the field-test requirements topic (`design/requirements.md`), the devvm walk-through and its runbook, brief, `record.sh`, `brief-lessons.md`, `grade-brief.md`, the ledger notes of 2026-11-09 and 2026-11-10 on field tests, the decision record's safety row (`plugins/kaizen/references/decision-record.md`). Not read, on purpose: the other project itself, so that the skill meets it fresh (principal: run the test "pristine", no information leaks from here).

Layers (read back to the principal and confirmed): L1 this repository, the plugin maintainer, subject the field-test skill; L3 the other project in its devvm VM, the developer with their agent, the plugin brought up to date there; L4 the test machine where the developer's tool runs bare metal, reached through forwarded ports. The field-test skill serves any project's field test of its own subject, not only kaizen on kaizen.

## Steps

1. **Start.** Does: in the devvm session, after `/kaizen:update`, says "I want to field-test <the tool> on the test machine" or types the skill's command. Needs to know: that a field test is a person trying the subject in their environment while the agent reads along, and how it differs from a hallway test (agents only). Goes wrong: the hallway test starts instead; the older copy of the plugin has no such skill until the update. Would ask: "Is this the hallway test with a human, or something else?"
2. **The frame.** Does: answers what is under test (their tool, not the plugin), who takes part (themself, colleagues, later users), where it runs, what they want to learn, one shot or repeated. Needs to know: why the skill asks this, and that "one shot on real work" is fine. Goes wrong: the skill assumes the kaizen-on-kaizen setting (a plugin under test, a reset, a master copy); asks about a persona when the developer is the user. Would ask: "Why would I reset? I want my work."
3. **Fitting it to the scenario.** Does: walks through the run with the agent (the walk-through skill), settles open points (the requirements skill, one topic). Needs to know: that every field test needs some individual work, and that these skills are how it is done. Goes wrong: the skill writes a generic runbook without walking; or walks for an hour when the setting is simple. Would ask: "How much of this do we need for a one-shot test?"
4. **Safety on a shared machine.** Does: states what the tool may touch (paths, ports, data, other users' processes), how a run is stopped, what must never happen, who agreed. Needs to know: that nothing runs on the test machine before this is written down. Goes wrong: the agent proposes commands on the machine before limits exist; a forwarded port is reachable from the network; a recording catches credentials; a crawler walks outside its allowed tree. Would ask: "Where do we write the limits, and who has to sign?"
5. **Channels.** Does: agrees with the agent how data travels: a view of the session (a recording written as it goes), the forwarded ports, log files, shared folders. Needs to know: which the agent can actually read from its VM. Goes wrong: the recording lands where the VM cannot see it; the port answers from the host but not from the VM; the agent learns this mid-run. Would ask: "Can you see it? Check now, before I start."
6. **The runbook.** Does: reads the steps with the agent: variables first, then one command per line, each explained; adjusts them. Needs to know: where runbook and evidence live in the project (tracked or private). Goes wrong: a long script handed over as "run this"; multi-line pastes break in the terminal. Would ask: "Why this command? What does it change?"
7. **The run.** Does: real work on the tool, over hours, partly in the background; notes as `#` lines, a notes file or "note for the debrief". Needs to know: when the agent looks at the live view and when it speaks up. Goes wrong: the agent interrupts work or stays silent through a skipped step; reading the live view costs tokens with nobody asking. Would ask: "Are you watching? Did I miss a step?"
8. **Wind-down and evidence.** Does: ends the recording, exports the sessions, packs one archive, looks through it for anything private. Needs to know: what is in the evidence and where it goes. Goes wrong: an export refused because git would track it; a session not exported; credentials in the recording. Would ask: "Is all of it there? What must I remove?"
9. **Process and act.** Does: the agent grades the run against the project's requirements with a grading brief; findings go by layer: the tool's to the project's tracker, the plugin's upstream (a draft for the person to send), the method's to the field-test notes. The next run is offered once these are acted on. Needs to know: which findings are "works as designed". Goes wrong: a finding about the plugin filed in the project's tracker, or the reverse; the next run starts before anything changed. Would ask: "What do I do with the plugin findings?"

## Product hat
The developer wants the tool working on the test machine and the work kept; "done" is a run that taught them something, with findings filed where they belong and nothing harmed on the shared machine. They would complain about ceremony that a one-shot test does not need, about being asked to act a role, and about an agent that did not notice a skipped step it could see.

## Developer hat
Bare metal on a shared machine is the risk: the limits must exist before the first command, and the skill must never run anything there itself without a yes. Recordings and exports can hold secrets. Forwarded ports can expose services beyond the VM. Watching a long run live is a token cost and an interruption risk. The skill must stay general: each scenario's specifics come from walking it with the person, not from the skill's text.

## Questions for the principal
1. Is the skill started only by the person (`/kaizen:field-test`), or may the agent start it when someone says "field test"? (step 1)
2. Must the safety limits be written and agreed before any runbook, as a gate, for every setting outside an isolated VM? (step 4)
3. When does the agent look at the live view during a long run: when the person asks, at each step of the runbook, or on a schedule? (step 7)
4. During the run, may the agent speak up unasked when it sees a skipped step or a risk, or only when asked? (step 7)
5. Where do a project's runbook, brief and evidence live: tracked in the project (`design/field-tests/`) or private (`.claude/`)? (steps 6, 8)
6. May the agent in the VM run commands on the test machine (through a port or ssh), or only read? (steps 4, 5)
7. Plugin findings from another project: a drafted issue for the plugin's repository, sent by the person? (step 9)

## Answers from the principal (2026-11-10)
- Frame: the subject is the developer's own tool; one shot, no reset ("my main concern is getting work done in that project"); the agent gets a view of the session and forwarded ports, and the skill finds the appropriate channels for data exchange; the skill works without any input from this repository and stays general ("not hand-crafted"); it adapts to each scenario with the walk-through and requirements skills; it takes care of safety, since the test runs bare metal on a shared machine; the principal is empowered on that machine.
- Questions 1 to 7: open.

## Gaps
- No field-test skill (step 1); the hallway test's description says nothing about a person.
- The general parts exist only as devvm files in this repository (`record.sh`, `brief-lessons.md`, `grade-brief.md`): an installed plugin does not carry them (steps 5 to 9).
- No safety step for a subject outside a VM (step 4).
- No check of the exchange channels before a run (step 5).
- No rule for how the agent watches a long run (step 7).
- No place in a project for a field test's records (step 6).

## Acceptance examples
- E43, E44, E45, E46, E47, E48 (added to `design/examples.md`).

## Questionnaire
Not filled from this walk: 2.5 (how a wrong result of the tool is noticed during the run), 2.6 (how long a run lasts, how much the live view costs), 2.10 (what is removed from the test machine afterwards); for the developer's own requirements, the skill asks them in the real run.
