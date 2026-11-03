---
name: walkthrough
description: Put on the shoes of a stakeholder and walk through a process step by step to find the requirements, questions and acceptance examples nobody has written down. Use it during requirements gathering or design, before a change is specified, whenever the user says "walk through", "from the perspective of", "what would an operator / scientist / new colleague do", "how would X use this", or asks how a new repository, deployment, onboarding or workflow would go for someone; also before a play test, to decide what to test.
---

# Stakeholder walk-through

Requirements that nobody wrote down surface when someone who is not the author tries to do the thing: the operator installing the service, the scientist searching for their data, the colleague setting up a repository, the maintainer reading a log at three in the morning. A walk-through does that on paper, with a named persona and a concrete process, before the change is specified. Its output is not a design: it is questions for the owner, gaps, and acceptance examples that the specs and tests can use.

Two borrowed habits, with thanks: interview from two hats, the product hat (user value, goals, success) and the developer hat (feasibility, security, edge cases), as the MIT-licensed Feature Forge skill by jeffallan does; and mark what a simulated stakeholder "said" as lower confidence than what a real one said, as melodic-software's requirements-elicitation skills do.

## Inputs

Settle these with the user before walking, and write them at the top of the output:

1. **The persona.** Who they are, what they want from this process, what they know and do not know, what they have on their machine, and what they would never read. Prefer a real person's role at the institute over an archetype; prefer a real person's answers over your guesses when you can ask.
2. **The process.** The thing they are trying to do, from their first step to the moment they consider it done. Examples: install the crawler on a server; find last week's measurement in the index; add a new file format as an external collection; start a new repository for development with agents; read the crawl log after a night run.
3. **What exists.** The documents, code, commands and pages the persona would meet, so that the walk tests reality and not a plan. Read them as the persona would: in the order they would find them, skipping what they would skip.

## The walk

Take the process one step at a time, in the persona's shoes. For every step, write down:

- **What they do**, concretely: the command typed, the page opened, the file read, the person asked.
- **What they need to know** at that moment, and whether what exists tells them.
- **What goes wrong** here in practice: the silent failure, the misleading message, the choice with no default, the step that needs rights they do not have, the wait with no feedback.
- **The question they would ask** the owner if they could, in their words.

Then switch hats twice over the whole walk: with the product hat, ask what the persona wanted and whether the process delivers it, what "done" looks like for them, what they would complain about; with the developer hat, ask what is infeasible, insecure, slow at scale, or fragile in the order of steps.

Where the walk reaches a point the documents do not cover, do not invent the answer: record it as a question, and if you had to assume something to continue, say so and mark the rest of the walk as resting on that assumption.

Go up a level when a step reveals something general (five whys): a confusing message is one step; "the tool never says what it will do before doing it" is a requirement.

## Output

Write the walk-through to the project's design notes if it has them (for example `design/walkthroughs/<persona>-<process>.md`), otherwise `docs/walkthroughs/`, and give a short summary in the reply. Template:

```markdown
# Walk-through: <persona> <does process>

Persona: <who, goal, knowledge, environment>. Confidence: <simulated | based on interviews with ...>.
What exists: <documents, code, commands read>.

## Steps
1. **<step>.** Does: <...>. Needs to know: <...>. Goes wrong: <...>. Would ask: "<...>".

## Product hat
<what they wanted, what "done" is for them, what they would complain about>

## Developer hat
<infeasible, insecure, slow, fragile>

## Questions for the owner
- <question, in the persona's words, with the step it came from>

## Gaps
- <requirement, behaviour or document that does not exist; the step that needs it>

## Acceptance examples
- When <concrete situation>, then <observable outcome>.   (ready for a spec scenario or a test)
```

## Rules

- Say which parts are simulated. A walk-through by an agent finds the gaps a careful colleague would find; it does not know what the real persona values. Hand the questions to a real stakeholder where one exists, and update the confidence line.
- Stay in the shoes. If you know how the system works, the persona does not; write what they see, not what you know.
- Concrete over general. "The operator runs `modama-crawler crawl` and sees nothing for two hours" is a finding; "feedback could be improved" is not.
- Questions, gaps and examples are the deliverable. Do not design the fix here; the owner decides what becomes a requirement.
- Consider a fresh pair of eyes: for a tool that exists, a sub-agent given only the persona, the process and the user-facing documents, with the instruction to run the tool, finds what the author cannot un-know. That is the `hallway-test` skill in this plugin; use it when the walk-through turns into "let's try it".
