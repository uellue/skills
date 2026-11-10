# Changes for projects

What `/kaizen:update` brings into a project, newest first: what a project adopts, changes or keeps when the plugin moves past the version its records are from. Changes inside the skills that need nothing from the project are not listed; the skills apply them on their own. The standing instructions are compared line by line with the project's copy, so their wording is not repeated here.

## 0.6.0

- **Numbering across messages** (new in 0.6.0-dev.2, first line of the block after the version line). Items and questions are numbered in one sequence across the agent's messages, never restarting while any is open, no item without a number, no jumps. From field-test run 8, where restarts across messages kept recurring.
- **A budget for long stretches** (new in 0.6.0-dev.2, before the review line). Before a long stretch without check-ins, or a loop of expensive test runs or many agents, the agent gives the estimated cost and agrees a ceiling (default $20 at list price), stops with a quarter left, and runs the likely-affected tests while iterating, the rest at acceptance. From 2026-11-10, when eval runs hit the person's session limit.
- **Ledger and inbox** (changed in 0.6.0-dev.2). The issue-tracker section below now says the ledger's notes section is the inbox for ideas about the project too; a project at 0.6.0-dev.1 has the older sentence "holds only what concerns working with the plugin and the agent" and replaces it.
- **Replies to people** (changed in 0.6.0-dev.2). The same section no longer has the agent draft replies to people on the tracker: it points out where the person's answer is needed, and drafts only when asked. A project at 0.6.0-dev.1 has "Post only replies … drafts first" and is offered the new wording. From field-test run 8: "Let's not create noise on the issue tracker. I can follow up with human users."
- **Version line.** The standing-instruction block starts with "Kaizen standing instructions, version …"; a project that has the block adds the line, first inside whatever section holds the block, so that the skills can tell when the project is behind. A project without the block has no version line, and its ledger alone tells the skills it is behind.
- **Issue tracker.** Where a project's issues and pull requests live (GitHub, GitLab, a mail list, none) is a setting in its instruction file, asked once: the tracker and repository, when the agent reads it (at the start of work on an issue, before a pull request, in the debrief), and who may post. The section the update writes, filled in with the answers:

  ```text
  ## Issue tracker
  Issues and pull requests: <tracker, repository>. They are the backlog of the work; design/kaizen.md (the ledger) holds what concerns working with the plugin and the agent, with a link where an issue touches that, and in its notes section (the inbox) any idea dropped during work, about the project too, until /kaizen:sync or the debrief routes it. Read the tracker <when>. Post nothing (comments, replies, labels, closing) and draft no replies to people unless <the person who decides> asks; point out where their answer is needed instead. Commands that change something (push, rebase, posts) are run by <the person, with the agent's help / the agent after a yes>; a draft they ask for goes to .claude/drafts/ (kept out of git), split into a part for people and a part for agents. A fix says "Closes #n", a part of an issue "Refs #n".
  ```
- **Sync and inbox.** `/kaizen:sync` reads the tracker from then on, marks ledger rows whose issues closed, and routes the ledger's notes (now an inbox for any idea dropped during work) to an issue, a comment, a ledger row or the bin; the update only takes the first look.
- **Unanswered reporters.** The first time the update reads the tracker, it names issues and pull requests from others that have had no answer for more than two days, as places where the person's answer is needed; it drafts a reply only when asked (0.6.0-dev.2; dev.1 offered a draft).

## 0.5.5

- **Ledger header.** `design/kaizen.md` carries two lines under its title: `Public: <yes / no / may become>, asked <date>` (whether the repository is or may become public: then the ledger holds no details of other projects and no security findings) and `Message size: <comfortable / shorter / longer> ("<the person's words>"), asked <date>`. The update asks both questions rather than guessing.
- **Feedback entries.** What people say about working with the agent and the plugin, liked or not, goes verbatim into `.claude/debriefs/feedback-raw.md` (private) and cleaned into `design/feedback.md` (one line per entry). Created when the first entry comes, not by the update.
- **Private folder.** `.claude/debriefs/` holds private reports; it must be ignored by git on every branch (`/.claude/debriefs/` in `.git/info/exclude`, or in `.gitignore`).

## Before 0.5.5

Projects from these versions have the standing instructions without a version line, and so do projects from 0.5.5: a block without one takes the sections of 0.5.5 and 0.6.0, and the comparison line by line covers its wording. Records were the same as in 0.5.5 except for what that section lists.
