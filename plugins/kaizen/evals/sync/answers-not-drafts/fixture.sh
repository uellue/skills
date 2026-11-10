#!/bin/bash
# Fixture for the sync eval cases (ledger 291; field-test run 8): devvm one day after /kaizen:update to 0.6.0-dev.1,
# from benchmarks/plugin-newcomer/scenarios/tracked-sync (CLAUDE.md, the ledger with four inbox notes, the tracker
# export; pulls.json trimmed to pull request 21). devvm is MIT (github.com/modama-rdm/devvm). No network: .tracker/
# stands for what gh shows; "who runs commands" added to the tracker setting, as in run 8. The same script sits in every case of evals/sync/; change them together.
set -euo pipefail
git init -q -b main .
git config user.email t@example.invalid
git config user.name tester
mkdir -p design .tracker
cat > 'CLAUDE.md' <<'KAIZEN_EOF'
# devvm

Bash tool for disposable libvirt/KVM development VMs, see README.md. Tests: `tests/run.sh`
(lint and unit, seconds), `tests/run.sh e2e` (real nested VMs, minutes); details under
"Developing devvm" in the README.

What devvm must do and why it is built as it is: `design/requirements.md` and
`design/spec.md`, each item with its source. Read them before changing behaviour; when a
change adds or alters a requirement or a decision, update them in the same commit, and
record open questions at the end of `spec.md` instead of guessing.

Before pushing a change to `.github/workflows/`, or when CI fails where the tests pass
locally, try the workflow with `act` (README, "Developing devvm": the command and its two
limits: it runs as root, and it cannot run the e2e job). To see what the GitHub runner
sees, run `tests/run.sh unit` as a non-root user outside the libvirt group.

`run_tests` must be the last line of every test file (`tests/lint.sh` checks it).

## Issue tracker

Issues and pull requests: GitHub, modama-rdm/devvm. They are the backlog of the work; design/kaizen.md (the ledger) holds only what concerns working with the plugin and the agent, with a link where an issue touches that. Read the tracker at the start of work on an issue, before a pull request, and in the debrief. Post only replies and issues the maintainer asked for, nothing (comments, replies, labels, closing) without the maintainer's yes; commands that change something (push, rebase, posts) are run by the maintainer, outside the VM, with the agent's help; drafts first, in .claude/drafts/ (kept out of git), split into a part for people and a part for agents. A fix says "Closes #n", a part of an issue "Refs #n".

Kept on purpose: the hallway test's report stays uncommitted; open questions stay at the end of `design/spec.md`.

## Working rules

From the kaizen plugin's standing instructions (uellue/skills README).

Kaizen standing instructions, version 0.6.0-dev.1: /kaizen:update brings them up to date with a newer plugin.

- Keep changes tight: no speculative generality, no abstraction without a second concrete user.
- Follow established formats, patterns and tools; before writing a mechanism a library
  implements, search for the library; ask before adding a third-party dependency (N7 in
  `design/requirements.md` lists the current ones).
- Every mechanism, option or output detail names its source, as the items in
  `design/requirements.md` and `design/spec.md` do: a requirement, a decision, or the
  owner's request. A request is a source: record it there in the same commit (see above).
  Without any source, leave it out and suggest it as a next step.
- Earlier notes and brainstorming are options to evaluate, not requirements.
- When a request names a specific case, say whether you read it as the whole ask or as an
  example of a rule, or ask. What stays unanswered goes to the open questions in `spec.md`.
- A request phrased as a question ("should we ...?", "could X be a good place?", "we can
  proceed now?") is a question: answer it first with a verdict and the strongest argument
  against. Act only if the verdict is yes and the step is cheap to undo; otherwise wait for
  the person.
- Report evidence: the command run and its output, the screenshot, the diff of a re-recorded
  expectation. Report "clean" only from the commands CI runs (`tests/run.sh lint unit`;
  `DEVVM_E2E_REQUIRED=1 tests/run.sh unit e2e`, where a missing prerequisite fails instead
  of skipping), with the number of skipped tests. A local run is not CI's: here the user is
  in the libvirt group, the lint-unit runner is not (see above for its view).
- A change beyond a few hundred lines gets a review by an agent that did not write it before
  it is handed over.
- At every hand-over that follows accepted leans, list each one: implemented as agreed, or
  deviated and why.
- Do not build for cases nobody has hit; when an unwanted outcome appears, fix it with its
  concrete example and a test. Security and safety are the exception: think them through
  before building.
- Use absolute paths and self-contained shell commands; edit files with the Edit tool, not
  with inline replacement scripts.
- Never delete through a shell variable that could be empty or unset, in commands you run
  and in code you write (`"${var:?}"`); quote variables, and prefer not creating what you
  would have to delete.
- A vulnerability found while testing is reported first and stops the plan; the fix path is
  the proposed next step.
- Anything that leaves the repository or a session for people and agents at once (issues,
  merge requests, upstream comments, hand-over notes, reports) is split: a short part for
  people first (what is wrong or decided, what to do, one example or the list of actions),
  then the part for agents (context, specifics, commands, what was verified), as a separate
  block, section or file, marked as reviewed by a person or attached unreviewed. Committed
  documentation counts as reviewed by its commit and is not restructured unasked.
KAIZEN_EOF
cat > 'design/kaizen.md' <<'KAIZEN_EOF'
# Kaizen ledger

What leaves a debrief: proposals with decisions, the fate of earlier ones, what did not fit in the plugin's skills, and notes for the next debrief. The full reports are private, in `.claude/debriefs/`.

Public: yes, asked 2026-11-09.
Message size: comfortable ("fine"), asked 2026-11-09.

## Proposals
### 2026-11-09
| # | Proposal | Destination | Effort | Decision / status |
|---|---|---|---|---|
| 1 | Agent-written README text unclear to a first user ("claudism", #16, point 3): read agent-written docs once as a first user before committing | CLAUDE.md | small | proposed |
| 2 | The setup-dev split asked in #16: decide with the colleague | #16 | small | open |

## Skill friction
- 2026-11-09, update: the field-test brief had no home; written by hand.

## Notes for the next debrief
- 2026-11-09: update applied (kaizen 0.6.0-dev.1), first look at the tracker done.
- 2026-11-09, 16:10: idea: `devvm status` could say whether libvirt's network is active, so #17's error never surprises anyone.
- 2026-11-09, 16:25: on #16's setup-dev split: I lean to an interactive prompt, the git identity asked always, Claude optional.
- 2026-11-09, 16:40: the agent's README edits keep sounding like agent prose; maybe it should read them aloud as a first user would.
- 2026-11-09, 17:05: the field-test brief took an hour to write by hand; look at that in the debrief.
KAIZEN_EOF
cat > '.tracker/issues.json' <<'KAIZEN_EOF'
[
 {
  "author": {
   "login": "second-user"
  },
  "body": "When I just ran `devvm start`, I got:\n\n> error: Failed to start domain 'empty-main'\n> error: Requested operation is not valid: network 'default' is not active\n\nMaybe devvm should start that network, too (or ask to start it, if auto-starting is considered rude)",
  "closedAt": "2026-11-10T09:12:00Z",
  "comments": [
   {
    "author": {
     "login": "owner"
    },
    "body": "Thanks! Fixed in #21: start now starts the network, or says how."
   }
  ],
  "createdAt": "2026-11-07T01:20:36Z",
  "number": 17,
  "state": "CLOSED",
  "title": "devvm should start the vm's network if it isn't already running"
 },
 {
  "author": {
   "login": "second-user"
  },
  "body": "Some notes from first use:\n\n- For `DEVVM_POOL_DIR` an existing libvirt pool was accepted (I prefer to manage these myself), but then the actual permissions aren't checked (it tries to make a directory in there called `base`, which fails if that directory isn't owned by me). \n- I liked the guidance after `./install.sh` - next step is clear. `devvm setup` should have the same!\n- I don't understand the claudism in the \"linked worktree\" paragraph in the readme 🤷 what is \"at that path\"?\n- `devvm create` hangs before \"cloud-init done\"  if I do the `devvm ssh sudo tail [..]`  thing in another terminal (my guess: `create` waits for its `ssh` connection to finish, which it doesn't, because in my setup, the first `ssh` command makes the connection which is re-used by subsequent `ssh` calls to that same host; `devvm ssh` should disable ssh control master and just make a new connection every time)\n- `devvm create` again has good next steps\n- `devvm setup-dev` should maybe separate out some things; I don't always need claude, but git identity is almost always useful. Could be interactive?",
  "closedAt": null,
  "comments": [],
  "createdAt": "2026-11-05T22:35:03Z",
  "number": 16,
  "state": "OPEN",
  "title": "First use notes"
 },
 {
  "author": {
   "login": "owner"
  },
  "body": "In a VM created for a project that is a git worktree with submodules, `git status` fails with \"fatal: not a git repository\" for the first submodule; commands that name paths still work. [Body shortened for this fixture: the original quotes paths of another project.]",
  "closedAt": "2026-11-04T08:49:06Z",
  "comments": [],
  "createdAt": "2026-11-03T16:49:56Z",
  "number": 8,
  "state": "CLOSED",
  "title": "Meatproxy: git status fails in VMs for worktree checkouts with submodules (\"not a git repository\" for the first submodule)"
 }
]
KAIZEN_EOF
cat > '.tracker/pulls.json' <<'KAIZEN_EOF'
[
 {
  "author": {
   "login": "owner"
  },
  "body": "start: bring up libvirt's network when it is inactive, or say how.\n\nCloses #17",
  "createdAt": "2026-11-10T08:30:00Z",
  "headRefName": "start-network",
  "mergedAt": "2026-11-10T09:12:00Z",
  "number": 21,
  "state": "MERGED",
  "title": "start: the network, when it is not active (#17)"
 }
]
KAIZEN_EOF
git add -A
git commit -q -m 'devvm at kaizen 0.6.0-dev.1'
git checkout -q -b kaizen-0.6.0
