---
name: walkthrough
description: Put on the shoes of a stakeholder and walk through a process step by step to find the requirements, questions and acceptance examples nobody has written down. Use it during requirements gathering or design, before a change is specified, whenever the user says "walk through", "from the perspective of", "what would an operator / scientist / new colleague do", "how would X use this", or asks how a new repository, deployment, onboarding or workflow would go for someone; also before a play test, to decide what to test, and after one, to compare what was imagined with what happened. Where OpenSpec is also installed, use this skill rather than /opsx:explore before a proposal.
---

# Stakeholder walk-through

Text id `3fb92223`: first run `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/version.py walkthrough <this text id>` and pass on what it prints, if anything (it is silent when all is well; if it fails, carry on).

Requirements that nobody wrote down surface when someone who is not the author tries to do the thing: the operator installing the service, the scientist searching for their data, the colleague setting up a repository, the maintainer reading a log at three in the morning. A walk-through does that on paper, with a named persona and a concrete process, before the change is specified. Its output is not a design: it is questions for the owner, gaps, and acceptance examples that the specs and tests can use.

The walk-through is one of three moments for the same persona and process: the walk-through imagines it before anything exists and produces the use scenarios (section 2.1 of the requirements) and the acceptance examples; the `hallway-test` skill executes it with fresh eyes once something exists; comparing the two, what was expected to go wrong against what did, validates the specification and the implementation. The `playbook` skill in this plugin says when each fires.

Two borrowed habits, with thanks: interview from two hats, the product hat (user value, goals, success) and the developer hat (feasibility, security, edge cases), as the MIT-licensed Feature Forge skill by jeffallan does; and mark what a simulated stakeholder "said" as lower confidence than what a real one said, as melodic-software's requirements-elicitation skills do.

## Inputs

Settle these with the user before walking, and write them at the top of the output.

1. **The persona. This blocks: do not walk in a persona nobody confirmed.** Read the project's stakeholder record (`design/stakeholders.md`). Show the personas it has, ask which one to take, and offer to add a new one or correct an existing one: this is the moment to learn from the people who know the project. If no record exists, ask who the stakeholders are and create it with what the user says, one entry per persona: who they are, what they want from this process, what they know and do not know, what they have on their machine, what they would never read, and whether the entry comes from an interview or is simulated. Prefer a real person's role at the institute over an archetype. With no person available, follow the playbook's "Working without a person": the persona is recorded as simulated and the walk is marked as resting on it.
2. **The process.** The thing they are trying to do, from their first step to the moment they consider it done. Examples: install the crawler on a server; find last week's measurement in the index; add a new file format as an external collection; start a new repository for development with agents; read the crawl log after a night run; diagnose a search result that looks wrong.
3. **What exists.** The documents, code, commands and pages the persona would meet, so that the walk tests reality and not a plan; read them as the persona would, in the order they would find them, skipping what they would skip. Where the system runs (a test deployment, a VM, a stack that can be started), walk against the running system and do what the persona would do, instead of reading about it: the live step finds what the document hides.

When the user invokes this skill together with `requirements`, do the demand sections (1.1 to 1.4) first, then the walk-throughs as the use scenarios of 2.1, then the remaining sections; each walk's questionnaire footer lists the questions the record does not answer yet, which the interview then asks.

## Before the walk: the questionnaire

Read `${CLAUDE_PLUGIN_ROOT}/references/requirements-questions.md`, a requirements questionnaire adapted from a demand and requirements form written at ER-C. Check which of its questions the project's record already answers and note the ones it skips; the skipped ones often decide the walk (who operates this after the project? what happens when it is wrong and nobody notices?). The walk-through itself produces the questionnaire's section 2.1, the use scenarios; the rest is filled from the conversation with the real stakeholder, and a question without an answer is a finding.

## The walk

Take the process one step at a time, in the persona's shoes. For every step, write down:

- **What they do**, concretely: the command typed, the page opened, the file read, the person asked.
- **What they need to know** at that moment, and whether what exists tells them.
- **What goes wrong** here in practice: the silent failure, the misleading message, the choice with no default, the step that needs rights they do not have, the wait with no feedback.
- **The question they would ask** the owner if they could, in their words.

Then switch hats twice over the whole walk: with the product hat, ask what the persona wanted and whether the process delivers it, what "done" looks like for them, what they would complain about; with the developer hat, ask what is infeasible, insecure, slow at scale, or fragile in the order of steps.

Where the walk reaches a point the documents do not cover, do not invent the answer: record it as a question, and if you had to assume something to continue, say so and mark the rest of the walk as resting on that assumption.

Go up a level when a step reveals something general (five whys): a confusing message is one step; "the tool never says what it will do before doing it" is a requirement.

**A measured walk.** When the process can be carried out by an agent (a diagnosis, a setup, a search), run it instead of imagining it, against a simulator or in a dry run when it drives hardware: give a fresh sub-agent only the persona, the process and the user-facing documents, with the template `${CLAUDE_PLUGIN_ROOT}/references/diagnosis-brief.md` when the process is finding out what is wrong, and inject the faults the walk is about. Record what it did, the calls, the time and the tokens (`python3 ${CLAUDE_PLUGIN_ROOT}/scripts/usage.py agent-<its id>`), and put the result in the walk as a measurement, not an assumption. An injected fault must look like a real one: an artefact the system never produces (a timestamp with microseconds, a file name with a test marker) is a tell that invalidates the measurement.

## Output

Write the walk-through to `design/walkthroughs/<persona>-<process>.md` and give a short summary in the reply. Its acceptance examples go to `design/examples.md` with the next free IDs, a priority and the step they came from; the walk lists only the IDs. A small change gets a step table of at most about 300 words. Template:

```markdown
# Walk-through: <persona> <does process>

Persona: <who, goal, knowledge, environment; the entry in the stakeholder record>. Confidence: <simulated | based on interviews with ... | answered by the owner on <date>>.
What exists: <documents, code, commands read; the running system used>.

## Steps
1. **<step>.** Does: <...>. Needs to know: <...>. Goes wrong: <...>. Would ask: "<...>".

## Product hat
<what they wanted, what "done" is for them, what they would complain about>

## Developer hat
<infeasible, insecure, slow, fragile>

## Questions for the owner
- <question, in the persona's words, with the step it came from>

## Answers from the owner (<who>, <date>)
<each question with its answer, or "deferred to <stage>, owner <who>">

## Gaps
- <requirement, behaviour or document that does not exist; the step that needs it>

## Acceptance examples
- E<n> (added to design/examples.md): when <concrete situation>, then <observable outcome>. From step <k>.

## Questionnaire
<the sections of the requirements questionnaire the record does not answer, each with the question in one line>
```

## After the walk

- **Put the questions to a real stakeholder when one is available.** If a person in that role is in the room or reachable, list the open questions for them before anything else is relayed; their answers go into "Answers from the owner" and the confidence line changes from simulated to answered. A question the owner defers is recorded with the stage it is deferred to and who owns it, in the walk and in the requirements' open questions; a deferred question that lives only in chat is lost. If the stakeholder is not in the room, offer to turn the questions into a document to send (Matt Pocock's `to-questionnaire` skill does this, where it is installed).
- **Update the stakeholder record** with what the walk taught about the persona.
- **Hand the steps and the acceptance examples to the hallway test** as its coverage list when the thing exists or is built; after that test, add a line per step: imagined versus observed.

## Rules

- Say which parts are simulated. A walk-through by an agent finds the gaps a careful colleague would find; it does not know what the real persona values.
- Stay in the shoes. If you know how the system works, the persona does not; write what they see, not what you know.
- Concrete over general. "The operator runs `modama-crawler crawl` and sees nothing for two hours" is a finding; "feedback could be improved" is not.
- Questions, gaps and examples are the deliverable. Do not design the fix here; the owner decides what becomes a requirement, and the decisions go into the decision record (the playbook's "what we decided" moment).
- A number in the walk has a source (the owner, a measurement, a document); the agent's own estimate is marked as one.
- At the end, one line into the project's `design/kaizen.md`: what in this skill did not fit. If the file is new, announce it first (playbook, Rules).
