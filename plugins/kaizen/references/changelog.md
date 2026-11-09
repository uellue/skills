# Changes for projects

What `/kaizen:update` brings into a project, newest first: what a project adopts, changes or keeps when the plugin moves past the version its records are from. Changes inside the skills that need nothing from the project are not listed; the skills apply them on their own. The standing instructions are compared line by line with the project's copy, so their wording is not repeated here.

## 0.6.0

- **Version line.** The standing-instruction block starts with "Kaizen standing instructions, version …"; a project that has the block adds the line, first inside whatever section holds the block, so that the skills can tell when the project is behind. A project without the block has no version line, and its ledger alone tells the skills it is behind.
- **Issue tracker.** Where a project's issues and pull requests live (GitHub, GitLab, a mail list, none) is a setting in its instruction file, asked once: the tracker and repository, when the agent reads it (at the start of work on an issue, before a pull request, in the debrief), and who may post. The section the update writes, filled in with the answers:

  ```text
  ## Issue tracker
  Issues and pull requests: <tracker, repository>. They are the backlog of the work; design/kaizen.md (the ledger) holds only what concerns working with the plugin and the agent, with a link where an issue touches that. Read the tracker <when>. Post <how often: e.g. only replies the person asked for>, nothing (comments, replies, labels, closing) without the yes of <the person who decides>; drafts first, in .claude/drafts/ (kept out of git), split into a part for people and a part for agents. A fix says "Closes #n", a part of an issue "Refs #n".
  ```
- **Unanswered reporters.** The first time the update reads the tracker, it names issues and pull requests from others that have had no answer for more than two days and offers a short reply as a draft.

## 0.5.5

- **Ledger header.** `design/kaizen.md` carries two lines under its title: `Public: <yes / no / may become>, asked <date>` (whether the repository is or may become public: then the ledger holds no details of other projects and no security findings) and `Message size: <comfortable / shorter / longer> ("<the person's words>"), asked <date>`. The update asks both questions rather than guessing.
- **Feedback entries.** What people say about working with the agent and the plugin, liked or not, goes verbatim into `.claude/debriefs/feedback-raw.md` (private) and cleaned into `design/feedback.md` (one line per entry). Created when the first entry comes, not by the update.
- **Private folder.** `.claude/debriefs/` holds private reports; it must be ignored by git on every branch (`/.claude/debriefs/` in `.git/info/exclude`, or in `.gitignore`).

## Before 0.5.5

Projects from these versions have the standing instructions without a version line, and so do projects from 0.5.5: a block without one takes the sections of 0.5.5 and 0.6.0, and the comparison line by line covers its wording. Records were the same as in 0.5.5 except for what that section lists.
