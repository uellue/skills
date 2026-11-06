# Alongside OpenSpec and Matt Pocock's skills

Read when the playbook's step 4 finds one of them present, or when a moment would benefit from one. The plugin works without either and installs neither unasked.

## OpenSpec

The plugin covers what comes before a specification (stakeholders, requirements, walk-throughs, examples) and after it (hallway test, debrief). OpenSpec (github.com/Fission-AI/OpenSpec, MIT, `npm install -g @fission-ai/openspec`) structures the specification itself (proposal, spec deltas, design, tasks, validation, archive, no code while planning); its `validate` checks structure, not content, and the hallway test finds whether a user can do the thing.

- **Not in use and not installed:** for a change larger than small, mention it once as an option with what the person needs to decide (checked 2026-11-05: a third-party Node.js package with one maintainer on the npm registry; its README says telemetry is on unless `OPENSPEC_TELEMETRY=0` is set). Do not install it unasked; without it, the decision record in `design/changes/` does its job.
- **In use:** offer the rules in `${CLAUDE_PLUGIN_ROOT}/references/openspec-config.yaml` for the project's `openspec/config.yaml` (merge with what is there; `openspec init` writes one with comments only).
- **Before `/opsx:propose`:** the stakeholder record, the walk-throughs and `design/examples.md` exist for the change, or the proposal says why not. The proposal names the persona, says whether the requested solution is the whole need, and lists the premises nobody confirmed.
- **Into the change:** the decision record's content goes into OpenSpec's `design.md` instead of `design/changes/`; each must-example becomes an OpenSpec scenario that cites its ID. Requirements stay in `design/requirements.md`; OpenSpec's specs are the behaviour contract, not the place for new requirements.
- **After apply, before archive:** the hallway test, with the OpenSpec scenarios as part of its coverage and at least half its effort outside them. Archive on the branch after the review approves, as the last commit before the merge.
- **Deferrals:** a question that changes the approach blocks the proposal; one that does not is deferred in the requirements with stage and owner and named in the proposal.
- **Exploring:** where both are installed, clarify a need with `requirements` and `walkthrough`, not `/opsx:explore`, which writes into `specs/`.

## Matt Pocock's skills

Matt Pocock's MIT-licensed skills (github.com/mattpocock/skills) are a complete lifecycle of their own, with a router (`ask-matt`), a specification path (`to-spec`, `to-tickets`), review and retrospective. Their Claude Code plugin installs all of them at once (27 skills in version 1.3.2, checked 2026-11-05), and eleven of them start on their own (`code-review` among them shares its name with Claude Code's built-in command); [skills.sh](https://skills.sh/mattpocock/skills) copies single skills instead. When they are not present and a moment below would benefit, mention them once with that information.

| Moment | Kaizen | Theirs, when present |
|---|---|---|
| From nothing to an idea | none | `grill-me`, or `grill-with-docs` in a repository; its result is the record `requirements` starts from |
| Vocabulary | none | `domain-modeling` keeps `GLOSSARY.md` at the repository root; kaizen documents use its terms and do not redefine them |
| Questions for a real stakeholder | the walk-through lists them | `to-questionnaire` turns them into a document to send or fill in together |
| What we decided | the decision record in `design/changes/` | an ADR in `docs/adr/` only for a decision that is hard to reverse, surprising without context and the result of a real trade-off (their criteria); it links to the decision record |
| Specification | OpenSpec, or the decision record | `to-spec` and `to-tickets` as another option (they need his `setup-matt-pocock-skills` run once for the issue tracker); specs and tickets cite the example IDs |
| Retrospective | `debrief`: the collaboration, coaching for the person, the history across debriefs | `retro`: the agent's environment (checks, navigation, steering files); invoked by the person only, as a message of its own, or run by the debrief through an independent sub-agent; the two complement each other |
| Before logging off | the debrief's notes, the hand-over | `handoff` writes the state for the next session |

When `ask-matt` routes the work, place the kaizen moments in its flow: stakeholders and the requirements interview after the grilling, walk-throughs and `design/examples.md` before `to-spec`, the hallway test before the pull request, the debrief on its schedule. `to-spec` synthesises the conversation without an interview, and ask-matt keeps grilling, spec and tickets in one context window: the kaizen steps in between fill that window, so tell `to-spec` to read `design/requirements.md`, `design/examples.md` and the decision record, or compact at that boundary as ask-matt advises. Their documents stay where their skills put them (`GLOSSARY.md`, `docs/adr/`, `docs/agents/`, `.scratch/`); the kaizen documents stay in `design/`.
