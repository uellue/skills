---
name: sync
description: Bring a project and its upstream in step - fetch the repository and read the issue tracker, mark ledger rows whose issues or pull requests closed, route the ledger's inbox notes to an issue, a comment, a ledger row or the bin, and list what waits to go out (unpushed commits, drafts, replies owed), each posted only on the person's yes; git and gh run with the person's support, by the agent only where authorised, each command shown and explained. Only when the user types /kaizen:sync.
disable-model-invocation: true
---

# Sync

Text id `0024885b`: first run `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/version.py sync 0024885b` as it stands and pass on what it prints, if anything (it is silent when all is well; if it fails, carry on).

The project's backlog lives upstream (its issue tracker and pull requests); the ledger holds how the work is done, and its notes section is the inbox for ideas dropped during work until they find their place. A sync moves things across that border in both directions, with `git` and the tracker's CLI (`gh` for GitHub, `glab` for GitLab), the person supported rather than replaced: reading is the agent's to do; anything that changes something (a rebase, a push, a post) is proposed with its command and explained where it may be unfamiliar, and the agent runs it only where the person has authorised that, otherwise the person runs it. Nothing leaves the machine without the person's yes.

Use plain words with the person: explain a term of this plugin the first time you use it with them, as `${CLAUDE_PLUGIN_ROOT}/references/words.md` does; keep a message to about fifteen lines, one step or question at a time; number a message's items from 1 in one sequence that never restarts within it, so the person can answer by number.

## Steps

1. **The setting.** Read the "Issue tracker" section of the project's instruction file (`CLAUDE.md` or `AGENTS.md`): where issues live, when to read them, how often to post, whose yes counts. Without one, ask those questions once and offer to record the answers there (`${CLAUDE_PLUGIN_ROOT}/references/changelog.md`, 0.6.0, has the section to fill in); a project with no tracker syncs only its repository.
2. **In.** `git fetch` and say what moved: the default branch, the branches of open pull requests, the current branch against its upstream (behind, ahead, diverged; a rebase or merge is offered with its commands, never done unasked). From the tracker: issues and pull requests opened, closed or merged since the last sync (the ledger's notes say when that was). For each ledger row or note that links one that closed, propose the status ("done in pull request 9"); name open questions in the project's records that a closed issue made stale; name issues and pull requests from others that have waited more than two days for an answer.
3. **The inbox.** For each note in the ledger's notes section that is not yet routed, propose one destination, numbered: a new issue (title and body as a draft), a comment on an existing one (which, and the draft), a ledger row (a proposal about how the work is done), or dropped. Notes that belong to the debrief (how the session went) stay for it. One yes may take the list.
4. **Out.** List what waits to go upstream: unpushed commits and branches, drafts in `.claude/drafts/` (kept out of git like `.claude/debriefs/`), the replies owed from step 2, the issues and comments from step 3. Each draft is split into a part for people and a part for agents. On the person's yes, and where they authorised the agent to post, post it with the tracker's CLI and show the link; otherwise give the person the command or the text and the place, and help them through it. A commit that fixes an issue says `Closes #n`, a part of one `Refs #n`.
5. **Record.** In the ledger: each routed note keeps only its link ("→ #18", "→ row 12", "dropped"); statuses from step 2; one line in the notes with the date of this sync, so the next one knows where to start. Commit on the current working branch with the person's agreement.

## Rules

- Never post, push, close, label, rebase or force anything without the person's yes for that item; reading is free.
- Issues stay in the tracker: never copy an issue's text into the ledger; link it and say in one line what it is about.
- Say which layer each finding is about: the project's work (the tracker) or the work with the agent (the ledger).
- At the end, one line into the project's ledger: what in this skill did not fit. If the file is new, announce it first (playbook, Rules).
