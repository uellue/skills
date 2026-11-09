# Walk-through: the plugin maintainer runs a field test of kaizen 0.6.0-dev.1 in devvm

Confidence after the answers: answered by the principal, 2026-11-09; the runbook is `design/field-tests/devvm-runbook.md`.

Persona: the plugin maintainer (stakeholder record), outer role; the same person plays the manager in devvm, inner role (variant 1). Variant 1 runs exactly as variant 2 would, where a colleague plays the inner role, so that the handovers are tested. Confidence: confirmed by the principal, 2026-11-09 (the persona, the process, the layers, the reset).
What exists: branch `field-tests-269` pushed at `fe7586f` (kaizen 0.6.0-dev.1: `/kaizen:update`, `/kaizen:sync`, the notice); `transcript.py locate <dir>` reads another project's sessions; `benchmarks/plugin-newcomer/` (self-test scenarios `tracked-project`, `tracked-sync`, keys N32 to N50); the research notes on field tests; devvm at github.com/modama-rdm/devvm (checkout `~/src/devvm`). Walked on paper; nothing run.

Layers (principal, 2026-11-09):
- **L1**, this repository and session: kaizen on kaizen; the maintainer prepares, analyses, improves the plugin.
- **L2**, the kaizen plugin at 0.6.0-dev.1: the subject under test.
- **L3**, devvm and its Claude Code session: outer, the maintainer as a tester of 0.6.0-dev.1; inner, the manager developing devvm (update the plugin, sync, work on the tracker's issues), guided by the plugin.
- **L4**, what devvm creates (VMs, an agent inside them) and devvm's own infrastructure: managed by the inner role in L3; outside this walk.
The reset belongs to L1 only (kaizen on kaizen); normal plugin use never rewinds a project.

## Steps
1. **L2, install the branch.** Does: `claude plugin marketplace remove uellue`, `claude plugin marketplace add uellue/skills#field-tests-269`, `claude plugin install kaizen@uellue --scope user`, `claude plugin list`. Needs to know: removing the marketplace uninstalls kaizen from every project of this user; only a changed version string reaches an install. Goes wrong: user scope means every other project's sessions get 0.6.0-dev.1 too; a later fix here reaches devvm only with a new version (dev.2). Would ask: "Do I test at user scope, or can devvm alone get the branch?"
2. **L1, record the start state.** Does: write down devvm's commit, the plugin version, and a copy of `~/.claude/CLAUDE.md` (the update may offer to change it, step 3 of the skill). Needs to know: what a retry must start from. Goes wrong: a rewind of the devvm checkout leaves `.git/info/kaizen-update-noticed` (the notice stays silent next time), ignored drafts and debriefs, and the agent's memory for that path; posts and pushes upstream cannot be rewound at all. Would ask: "What exactly is 'the same state' upstream, on GitHub?"
3. **L1 to L3, the handover brief.** Does: a short written brief, the same a colleague would get (variant 2): what to try (the update, a sync, work on the issues), what to record, what not to do, how to hand back, and the closing question "did we do OK?". Needs to know: the brief must not say how to test devvm (the plugin must guide that). Goes wrong: in variant 1 the maintainer knows everything, so a thin brief passes unnoticed. Would ask: "Is the brief good enough for a colleague who was not here?"
4. **L3, recording.** Does: the devvm Claude Code session is the main record (its transcript); optionally the terminal under `script` (the method's own test); notes in the moment about the plugin, kept apart from devvm's own ledger. Needs to know: where notes about L2 go, so that "note for the debrief" in devvm stays devvm's. Goes wrong: an L2 note lands in devvm's ledger, and the layers mix. Would ask: "Where do I write a note about the plugin while I work on devvm?"
5. **L3, the run (inner role; not walked).** The plugin guides: the update, the sync, the issues. The maintainer only checks that it starts from the brief.
6. **L3 to L1, handing back.** Does: name the session (its id or the clone's path), the recording and notes, what was posted or pushed upstream (links), and the answer to "did we do OK?". Needs to know: what L1 needs to analyse without copy and paste. Goes wrong: the session ran in a VM (L4) or on another machine, so its transcript is not under this host's `~/.claude/projects/`. Would ask: "Where did my devvm session run?"
7. **L1, analysis.** Does: `transcript.py locate <devvm clone>`, `export` into this repository's ignored `.claude/transcripts/`, readers as in the debrief; grade against N32 to N50 and the field-test topic; the inner role's remarks as feedback entries; fixes; the version raised to 0.6.0-dev.2; push. Needs to know: which findings are about L2 (the plugin), which about devvm (they go to devvm's tracker, by the inner role), which about the field-test method. Goes wrong: an L3 finding fixed here as if it were the plugin's.
8. **L1, reset and retry (kaizen on kaizen only).** Does: update the install (`claude plugin marketplace update uellue`, `claude plugin update kaizen@uellue`), a fresh clone of devvm at the recorded commit in a new path, the global instruction file restored from step 2's copy, the run's VMs destroyed by the inner role (L4). Needs to know: what the previous run left behind and where. Goes wrong: a rewound checkout in the same path carries memory, notice file and drafts into the next run; upstream posts stay. Would ask: "Fresh clone per run, or rewind?"
9. **Variant 2, a colleague as the inner role.** The same brief, the same return path; the colleague keeps devvm's improvements, no reset; their material travels by the field-test transport (an issue in a private repository). Goes wrong: a brief that worked for the maintainer leans on what only the maintainer knew. The maintainer may also end the churn by turning the last run into variant 2: no reset, devvm keeps its changes (principal, 2026-11-09); so a run must be able to become the kept one after the fact, which a fresh clone in its own path allows (its branch is pushed or merged instead of discarded).

## Product hat
The maintainer wants to see whether a change to the plugin had the intended effect, run after run, and to judge the handovers as a colleague would meet them. Done: a runbook that starts from a recorded state, a run whose inputs and outputs reach L1 whole and labelled by layer, and a reset that leaves nothing behind. They would complain about a retry that is not from the same state, and about having to copy a session by hand.

## Developer hat
Upstream is not resettable: posts, issues, comments and pushes to the public tracker stay. User scope spreads the branch to all projects. The noticed-file, memory and ignored files survive a `git reset`. A session inside a VM keeps its transcript in the VM. Deleting a run's clone is a deletion through a path: only through a checked, non-empty variable, or by hand.

## Questions for the principal
- Upstream during churn runs: drafts only, a private fork as the tracker, or real posts that improve devvm and stay? (step 2)
- Where do notes about the plugin go while working on devvm? (step 4)
- Where does the devvm session run: on the host, or inside a devvm VM? (step 6)
- Reset by a fresh clone per run in a new path, or by rewinding `~/src/devvm`? (step 8)
- The global `~/.claude/CLAUDE.md`: copy and restore, or decline the update's offer to change it during test runs? (step 2)
- User scope for the branch, accepted for all projects during the test? (step 1)

## Answers from the principal (2026-11-09)
- Upstream: churn runs keep drafts only; the last run, once it becomes variant 2, posts for real ("Perfect, good point!").
- Notes about the plugin: a plain file outside devvm, so that they survive the reset.
- Where the session runs: inside the devvm VM `devvm-snapshots` (L4 hosts the L3 session); from there it spawns testing VMs as needed. So the session's transcript lives in that VM's home, and must be exported into the shared checkout (ignored by git) or copied out before a reset.
- Reset: devvm's own snapshot and reset for the VM's state (the plugin install, the agent's memory, the VM's `~/.claude/CLAUDE.md`, transcripts unless copied out first); the git tree comes from the host and is reset separately (a fresh clone per run). Some of these questions should also be asked of the inner role in L3: a follow-up check in the transcript is whether the plugin walked the inner role cleanly through setting up, its environment, what to run where, how information flows, and the roles. devvm may want to reset an inner layer of its own too (a fresh Debian VM with nothing set up and missing dependencies, rerun from the same state after devvm improves): devvm's matter, and a pattern for the field-test skill.
- The global instruction file: the one that counts is the VM's, covered by the snapshot; the host's is untouched ("good catch").
- User scope: install the branch at user scope inside `devvm-snapshots` only; the host and other projects keep the released version. The principal's question, how to test a development version in a branch without a release to everyone, answered from the documentation facts in the requirements topic (round 5): a branch reaches nobody who does not add it; one marketplace per name, so the tester's machine loses the released install while testing, which a VM avoids.

## Gaps
- No field-test skill yet (ledger 283): the brief and the return path are written by hand (steps 3, 6).
- No reset procedure, and it must not be in the plugin: it belongs to this repository's field-test material (step 8).
- The start-up notice cannot be reset by git: its file is in `.git/info/` (step 2).

## Acceptance examples
- E38, E39, E40, E41 (added to `design/examples.md`).

## Questionnaire
2.4 operating conditions (host or VM, step 6); 2.5 what a failed run leaves behind (step 8); 2.7 who operates the field-test material later (variant 2's colleague, step 9); 2.9 personal data in a colleague's transcript (variant 2).
