# Standing instructions for agents

The block a project pastes into its `AGENTS.md` or `CLAUDE.md`. The same text stands in the plugin's README ("What you paste for the agent"); the repository's check keeps the two identical. Merge, don't append: read each line against the project's existing instructions and requirements, keep the stricter rule, and point general rules at the project's own commands and documents.

```text
- Keep changes tight: no speculative generality, no abstraction without a second concrete user.
- Follow established formats, patterns and tools; before writing a mechanism a library implements, search for the library; before defining a term, look for the field's established vocabulary (a community glossary or ontology) and ask which one the project uses; ask before adding a new dependency, with its current release looked up, not recalled, and flag it in the hand-over.
- A pull request or release description starts from the branch's log and diff, grouped by area, so that nothing is left out; the size of a change is not its importance, and the agent can rarely judge which changes matter to which readers: ask the person, or leave the summary on top to them.
- Every mechanism, option or output detail names its source: a requirement, scenario, decision, or the person's request (record a request where the project keeps its requirements). Without any source, leave it out and suggest it as a next step.
- Earlier notes and brainstorming are options to evaluate, not requirements.
- When a request names a specific case, say whether you read it as the whole ask or as an example of a rule, or ask.
- When a word in a request is ambiguous or differs from the project's glossary, push back softly: say which reading you take, in the glossary's terms ("I read X as …"), and offer a glossary entry where none fits.
- A request phrased as a question ("should we ...?", "could X be a good place?", "we can proceed now?") is a question: answer it first with a verdict and the strongest argument against. Act only if the verdict is yes and the step is cheap to undo; otherwise wait for the person.
- Report evidence: the command run and its output, the screenshot, the diff of a re-recorded expectation. Report "clean" only from the command the commit or CI runs; give the number of skipped tests, and say where the local environment differs from CI's (user, groups, packages, switches that make a missing prerequisite fail).
- A change beyond a few hundred lines gets a review by an agent that did not write it before it is handed over.
- At every hand-over that follows accepted leans, list each one: implemented as agreed, or deviated and why.
- Do not build for cases nobody has hit; when an unwanted outcome appears, fix it with its concrete example and a test. Security and safety are the exception: think them through before building.
- Use absolute paths and self-contained shell commands; edit files with the Edit tool, not with inline replacement scripts.
- Never delete through a shell variable that could be empty or unset, in commands you run and in code you write (`"${var:?}"`, above all where the variable starts a path); quote variables, and prefer not creating what you would have to delete. Existing code is checked line by line and otherwise left as it is.
- A vulnerability found while testing is reported first and stops the plan; the fix path is the proposed next step.
- Anything that leaves the repository or a session for people and agents at once (issues, merge requests, upstream comments, hand-over notes, reports) is split: a short part for people first (what is wrong or decided, what to do, one example or the list of actions), then the part for agents (context, specifics, commands, what was verified), as a separate block, section or file, marked as reviewed by a person or attached unreviewed. Committed documentation counts as reviewed by its commit and is not restructured unasked.
```
