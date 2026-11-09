# Words you will see

The kaizen skills use a few words of their own. When an agent uses one with you for the first time, it should say what it means; this list is the short version.

- **Lean**: the agent's preferred answer to an open question, given with the question so that "yes" accepts it. A lean you accept becomes a decision.
- **Principal**: you, as the person who decides for the project and reviews the work.
- **Owner**: whoever may authorise work on something real (an instrument, a live site, irreplaceable data) and sets its limits; often not the principal. A project may use "owner" for its maintainer; then say which you mean.
- **Standing instructions**: the short block of rules for the agent that a project copies into its `CLAUDE.md` or `AGENTS.md`; its first line names the plugin version it is from, so that `/kaizen:update` can show what changed since.
- **Persona**: a described user (who they are, what they want, what they know), whose shoes a walk-through or a hallway test steps into.
- **Stakeholder**: anyone with a stake in the tool: its users, whoever maintains it, whoever owns what it touches, whoever reads what it produces.
- **Stakeholder record**: the file listing the personas (`design/stakeholders.md`), and whether each was described by the people it describes or imagined.
- **Acceptance example**: one concrete situation and what should then be observable, with an ID such as E7, so that tests can cite it; a must-example is one that has to hold.
- **Decision record**: a short file per change with what was decided, by whom, what is in and out, and what still blocks the build. Its safety row says what may touch something real, and on whose agreement. Its need note is its first five lines: whose need, what was asked for, the need behind it.
- **Small path**: the short version of the process for a small change: the need note, one or two personas, one walk-through as a step table, the examples, the decision record, the hallway test; no full requirements document.
- **Walk-through**: going through a task step by step in a persona's shoes, to find the questions nobody has answered yet.
- **Hallway test**: a fresh agent that has seen only what a first user would see tries your tool and reports what broke or surprised it. That agent is the tester, a sub-agent the session starts; its brief is the instruction it gets; it works in a scratch directory, a throwaway folder outside your project. Its modes: behaviour (does it do what it should), by eye (how the output looks), diagnosis (can someone find what is wrong), hint-following (a user who only skims and follows the program's messages), and a documents mode for a README or an instruction file.
- **Output tokens**: the unit in which the agent's work is counted against your plan or budget; a short README test takes about 15 k, a behaviour test of a small tool about 45 k. The hallway test states its cost in minutes first, tokens in brackets.
- **Stand-in**: what is used instead of something real that could be damaged: a simulator, a copy of the data, a local preview, a dry run.
- **Hand-over**: the moment work passes to someone else: a merge request, a release, a tool given to colleagues.
- **Ledger**: the backlog for how the work is done, not for the work itself: a short file (`design/kaizen.md`) of numbered proposals with their decisions, kept apart from the project's own backlog (its issues or task list). Each skill adds one line to it about what did not fit, so that rough edges surface at your next debrief.
- **Two hats, five whys**: interview habits the skills use: asking once as the person who needs the tool and once as the one who builds it; and asking "why" past the first answer until the cause is reached.
- **Debrief**: a look back at how you and the agents worked together, with proposals to work better next time.
- **Feedback entry**: something you said about working with the plugin, liked or not, kept as a source of goals: word for word in a private file, cleaned up (no names, no private projects) in `design/feedback.md`.
