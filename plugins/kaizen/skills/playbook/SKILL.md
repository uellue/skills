---
name: playbook
description: Which kaizen skill fits now, and what the shared documents are. The lifecycle from a first idea to stakeholders, requirements, walk-throughs, the decision record, the build, the hallway test and the debrief, with the moment each skill fires, the documents they share, a small path for small changes, working without a person, and how to work alongside OpenSpec and Matt Pocock's skills. Use it at the start of a project or a larger change, when the user asks how to approach product or feature development with agents, "what should we do next", "which skill applies", when routing work with ask-matt or another skill router (to place the kaizen moments in that flow), or when a session is about to specify, build or hand over something and no stakeholder record or requirements exist yet.
---

# Playbook

Text id `11c7874a`: first run `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/version.py playbook 11c7874a` as it stands and pass on what it prints, if anything (it is silent when all is well; if it fails, carry on).

The other skills are moments in one process; this skill says which moment a session is in, what that moment reads and writes, and what to do when a document is missing. It proposes; the person decides.

All shared documents live in the project's `design/` directory, or where step 3 placed them; "the ledger" is always the project's own `kaizen.md` there.

Use plain words with the person: explain a term of this plugin the first time you use it with them, as `${CLAUDE_PLUGIN_ROOT}/references/words.md` does; keep a message to about fifteen lines, one step or question at a time; number items as bold labels (`- **7**`, never `7.`), one sequence across messages, never restarting while any is open.

## When a session starts

Each step that asks something is its own message (steps 5 and 7 may share one; the path of step 2 is a message of its own, without step 3's questions); wait for the answer before the next.

1. **What it reaches.** Unless the request or the repository already answers it, ask one thing first: what the tool, or the tool to be, writes or changes (files next to its inputs, a server, an instrument's state) and what makes a change take effect (a push, a merge, a deploy, a restart, a command to the instrument) and where it then appears (a public site and its address, a shared server). A tool that writes into the directory it reads from reaches its users' data and gets the second round below. Before the agent runs a tool that writes on data, ask whether the data are the originals and whether another copy exists.
   Only if that reaches something real it could damage or that could cause harm (an instrument or other hardware; production, valuable or irreplaceable data; a service or website that is live, public or in use; messages to real people), a second round in a message of its own, with no lean of yours on the owner, the limits or who may authorise:
   - who owns it (if nobody knows, the group leader or the facility usually knows; when the answer is that the person publishes to the site or service on their own authority, they are its owner for this, as the decision record says, and whoever they name instead is the owner otherwise; when the answer names both, ask whether that person must approve this change);
   - what it could damage, and who may authorise what the tool does to it (when the person does not know, name the kinds as prompts, which is not a lean: a collision, the sample, the beam, venting; data overwritten; a page broken in public);
   - whether a stand-in exists (a simulator, a copy, a staging service, a local preview, a dry-run mode) and, for a simulator, whether it enforces the real thing's limits and labels its output as simulated (the decision record's safety row); if none, offer the cheapest one now (a copy of the data, a local preview; for an instrument, ask the vendor or the facility about a simulation or offline mode).
   An unknown answer blocks the step that reaches the real thing (the push, the deploy, the command to the instrument) until the owner answers; say so now, in those words. The safe work meanwhile is the stand-in (building one may start; its limits wait for the owner or the vendor's documentation, as the decision record says) and reading documents and code; connecting to the real thing counts as the real thing, even for a read-only query. When a push or a merge makes the change take effect, that merge is the release: work on a branch and try the change on the stand-in first. The session goes on.
2. **The path.** Unless the request or the repository already says it, ask who needs this and what they would do differently with it; if the person cannot say, discovery comes first (the lifecycle's first row). Then choose the path by size (below) and say which, in plain words: each step as what it does for the person ("a short list of who will use it", "a first user tries it"), the plugin's name in parentheses at most.
3. **The documents.** For each one the path needs and that is missing, say so and offer the skill that writes it; write nothing unasked. Before creating `design/` in a project that has none, ask, and ask whether committed files become public (a public repository, a site deployed from a branch) unless step 1 already told you. If they do and the person names no other place, lean towards a private repository of its own beside this one (for a public repository, the only choice), or `design/` excluded from deployment where the host allows it; record the choice; the ledger goes there too. A sibling repository gets a pointer in the project (a note under `.claude/`, listed in `.git/info/exclude`); once it is chosen, ask where it is pushed, since a repository on one disk only is one failure from gone. For every file written into `design/`, say whether it will be committed. A repository with no instruction file for agents is offered the block in `${CLAUDE_PLUGIN_ROOT}/references/standing-instructions.md`, once, with one line on what it asks of the agent; where committed files become public, as an uncommitted file listed in `.git/info/exclude`.
4. **Companion tools.** Check whether OpenSpec (an `openspec/` directory, or `openspec --version`) or Matt Pocock's skills (`claude plugin list`, a read-only command, shows `mattpocock-skills`; or copies under `.claude/skills/` or `~/.claude/skills/`) are present. Read `${CLAUDE_PLUGIN_ROOT}/references/companions.md` where one is, and for a change larger than small, to mention the absent ones once as options. The plugin works without either and installs neither unasked.
5. **Case or rule.** If the request names a case or a solution, ask whether it is the whole need or an example, and, if a stakeholder record exists, which persona on it is asking.
6. **The end.** If the session will hand something over (a document, a change, a merge request), plan the hallway test and the debrief as part of the work, not after it. If a piece of work has just ended (a merge, a release), offer its debrief first, before the next thing.
7. **Words.** Whenever a word carries two meanings or a request reads two ways, say which reading you take, in the project's glossary terms if it has one ("I read X as …"), and offer to settle the word: with Matt Pocock's `domain-modeling` where installed (it keeps `GLOSSARY.md`), otherwise by recording the agreed term where the project keeps its vocabulary. Before defining a term, look for one that exists: the project's glossary, and the field's own vocabulary (a community glossary or ontology); ask the person which they use, naming one you know of only when they have none (for electron microscopy, for example, the EM Glossary of the Helmholtz Metadata Collaboration), and adopt its term. Muddy words make muddy concepts and winding paths.

## The lifecycle

| Moment | Skill | Writes | Fires when |
|---|---|---|---|
| From nothing to an idea | optional: `/mattpocock-skills:grill-me` or `grill-with-docs` (`/grill-me` for a copied skill; see `companions.md`), invoked by name only | notes the requirements interview starts from; with `grill-with-docs`, the glossary and ADRs | the person cannot yet name who needs it and what they would do differently; otherwise `requirements` |
| Who is this for | `requirements` (section 1.4) | `design/stakeholders.md`: one entry per persona (role, goal, knowledge, environment, what they never read; interviewed, described by <who>, or simulated) | a project or change starts; a new kind of user appears; a walk-through or test needs a persona not on record |
| What is needed | `requirements` | `design/requirements.md` (form sections as a checklist, markers per item, open questions with owner and stage) | a loose idea needs tightening; a project or larger change starts; a tool that grew from playing around needs its record reconstructed; an existing document to check; one open question to flesh out |
| How it would go | `walkthrough` | `design/walkthroughs/<persona>-<process>.md`; acceptance examples appended to `design/examples.md` | before a change is specified; requirements 2.1; before a hallway test, to decide what to test |
| What we decided | the agent drafts it from `${CLAUDE_PLUGIN_ROOT}/references/decision-record.md` and asks the person each decision it cannot take from the record | `design/changes/<name>.md`: need, interface, decisions with who decided and whether reversible, must / should / won't with a size budget, blocking questions | after the walk-throughs, before the build; whenever an implementer would otherwise invent decisions; done when every must-example is cited and every blocking question is answered or named as an assumption the person accepted |
| Build | the project's own instructions | code, tests citing example IDs, docs | every sub-agent brief names the example IDs each assertion serves; anything it could damage as the decision record's safety row says |
| Does it hold up | `hallway-test` | `design/hallway/<date>.md`; imagined versus observed added to the walk-through | something exists that a first user could try; before a merge request |
| Does it hold up for real | `field-test` | `design/field-tests/<scenario>-runbook.md`; evidence in `.claude/field-tests/` (private) | a person tries it for real (real data, a real machine, an issue from real use), the session following along |
| How did we work | `debrief` | `.claude/debriefs/<date>.md` (private); the ledger | on a schedule (a day, a stretch, a skill's first use); after each release, in a fresh session, after the push and merge, with notes taken while the final acceptance tests ran; its proposals go into the next release; when the work is ready to push or a debrief's proposals are applied, suggest ending the session with the prompt for the next one; "note for the debrief" goes to the ledger at once |

**Acceptance examples have one home**, `design/examples.md`: one line each, with an ID (`E1`, `E2`, …), the concrete situation and observable outcome, a priority (must / should), and the walk step or requirement it came from. Walk-throughs and the requirements interview append to it; decision records, scenarios, tests and tester briefs cite the IDs; nobody keeps a copy. Before a hand-over, list every example with no scenario or test.

## Size the process to the change

- **Small change** (one command, one behaviour, a few hours): a need note of five lines (whose need, what the request names, the need behind it), written first into `design/changes/<name>.md`, which the decision record later grows around; a stakeholder record of one or two entries, which the walk-through writes as its first step; one walk-through as a step table of at most about 300 words with its examples and one line of open questions, without the template's other sections, against the running system and through the existing parts the change touches (a stand-in where it could damage something); the examples; the decision record; the hallway test. No full requirements form, no OpenSpec specs or tasks.
- **An existing tool before its first hand-over** (it works for its author; others start using it soon): the hallway test now, with the person as the source of the persona; a reconstruction of the requirements afterwards, from its findings.
- **Larger change or a new project:** the full table.
- **A single open question or idea:** the requirements interview or a walk-through on that topic only, its answer into the existing documents.

Fix unwanted outcomes when there is a concrete example, rather than specifying every detail in advance. Security and safety are the exception: think them through before building.

## Working without a person

With no principal available (an agent-only run, a trial), the skills may simulate one:

- The simulated principal's persona goes into the stakeholder record first, marked simulated.
- A simulated principal may answer questions, marked `[assumed]`; it may not confirm personas, accept leans or unblock the build. Those wait for a person and are listed at hand-over.
- The decision record says on which assumptions the build may start.

## Which skill would have supported this

At every point where the session finds a defect, a misunderstanding, a gap in a document or a question nobody can answer, ask which moment in the table should have caught it, and write the answer into the ledger's notes.

## Rules

- A missing document is a finding, not a reason to assume its content.
- At the end, one line into the project's ledger: what in this skill did not fit. If it does not exist yet, say first where it will go (`design/kaizen.md`, or where step 3 placed `design/`) and whether it will be committed, and start it from `${CLAUDE_PLUGIN_ROOT}/references/ledger.md`, which says what to ask first.
