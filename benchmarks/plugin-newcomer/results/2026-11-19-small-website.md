# Run 2026-11-19: scenario small-website, commit `a26ddc9` (0.6.1-dev.2), Opus, about 2 minutes

Usage of the tester (`usage.py agent-a62d4d112dbf1450a`): Output tokens, claude-opus-5-5 17,044 . The tester's report was read by the main session from its transcript; claims it makes about the plugin's text were checked by the main session before grading.

Graded by a fresh Sonnet agent that changed no skill, from the report, the key and the main session's checked claims.

The result format follows E15 and the previous run. The report gives no output-token count. It records ten quoted agent messages (M1 to M10) and a path of 12 steps. The tester made up the answers marked "[made up]". Items about what a skill asks count only where the tester did not volunteer the answer.

| # | Result |
|---|---|
| N1 | partly: the README's "First steps" lead to `/kaizen:playbook`, but the tester's path started with `/kaizen:update` ("README: `/kaizen:update` once per project. I had expected `/kaizen:playbook` first"). The main session confirmed that update is now under Install and not in First steps. The label on the debrief is not reported; M4 says only "A debrief (`/kaizen:debrief`) is possible after this first use". |
| N2 | held: "Version lines were silent four times"; `version.py update` "printed nothing (correct)". The `--project` line about the copy in `~/.claude/CLAUDE.md` is the update notice and a setup artefact (see the misfit below), not a skill's version line. |
| N6 | not reached: the small path was taken, no discovery question. |
| N7 | held: M1 says where and what before any write: "a file `design/kaizen.md`, the "ledger" ... Everything goes on a new branch, `kaizen-rollout`; nothing is written before you agree". M3 adds "committed on the branch". |
| N8 | not reached: nothing was built and no tester was spawned. The mode plan itself is graded under N22. |
| N9 | not reached: no debrief. |
| N10 | held: M10 states the cost before the start and ends with "Start?". M7 sizes the process before it starts: "This is a small change ... No full requirements document." |
| N16 | held: M10 says "Cost: a guess, about 10 minutes (about 30 k output tokens). Start?" It is called a guess, which the hallway-test text for a web page requires. |
| N17 | held: the agent asked, and the tester did not volunteer the answers. M5: "What makes a change to the site take effect, and where does it then appear?" M6: "Who owns the site and its address? ... Is there a local preview or staging copy? If not, the cheapest stand-in is a local preview". The previous run's caveat is gone. One gap: update step 4 did not ask how a change goes live. |
| N18 | held: M7 gives a five-line note, one visitor's walk-through, decisions, build and a fresh agent's try, "No full requirements document". |
| N21 | held: M6 says "Until the owner answers, pushing to `main` is blocked; work happens on a branch and in the preview." Step 7 of the report says the same, with the answer "I don't know". |
| N22 | held: M10 says "the tester cannot see the rendered page", so the plan is a behaviour test of the generator plus the person checking the local preview. |
| N24 | partly: M1 glosses "ledger" only as "a list of what to improve in how we work". "Stand-in" is explained only by example (M6). "Lean" (M2, M4, M8) and "pull request" in M4, with no remote, are not explained. Each concept kept one name in the quoted messages. |
| N25 | not held: the tester lists about eleven words in the plugin's files that a newcomer cannot know ("trailer", "closing keyword", "upstream", "Text id", "need note", "safety row", "measured walk", "eval", "Feature Forge", "two-hat", and others). It also names three names for one concept ("inbox" = "Notes for the next debrief" = "notes section") and "record" for four different things. |
| N27 | held: the items run 1 to 15 in one sequence across M1 to M10, with no restart in a message. |
| N28 | held: the lengths are 7, 4, 5, 5, 2, 6, 8, 5, 3 and 4 lines, none over fifteen. M7 and M6 are the longest at 8 and 6. |
| N29 | not reached: no push, merge or release. M4's offer of a debrief "after this first use" is the first-use offer; no invitation to note thoughts is reported. |
| N30 | not reached: no debrief. |
| N31 | not reached: no debrief. M3 did ask "Is the length of my messages fine?", but that is the update's own question, not the first debrief's. |

## Comparison with 2026-11-06

- N1: worse in the path, held to partly. The newcomer was sent to `/kaizen:update` first by the README and expected the playbook. The previous run held.
- N7: better, not reported to held. The ledger is announced with its place and the branch before it is written.
- N17: better, held with a caveat to held. The previous run needed the agent to infer "live" from a README line. Now playbook step 1 asks directly what makes a change take effect, and the owner and stand-in follow.
- N10, N16, N18, N21, N22: same, held. In N10 and N16 the cost is now a guess for a web page, where the previous run used measured figures.
- N2: same, held.
- N6, N8, N9: same, not reached.
- N24, N25, N27 to N31 are new in the key since the last run and have no earlier result. N27 and N28 held. N25 was not held. N24 held partly.

## Setup misfit named by the tester

`version.py --project` read the tester host's real `~/.claude/CLAUDE.md` and printed "a copy in your ~/.claude/CLAUDE.md", which a real newcomer would not have. The main session confirmed it for this run and for existing-tool and sem-instrument too; `brief.py` does not isolate HOME. This run's answer to M1's first question ("Didn't know I had that. Its own.") is therefore made up. The previous run's misfit, that the hidden fact depended on the simulated agent's inference, is gone. The walk-through question "who uses / maintains / owns / reads" brought out the readers without leading.

## New findings the key lacks (candidates for key items)

Confirmed by the main session:

- **Order of update and playbook (report finding 1, the main one).** `/kaizen:update` writes `CLAUDE.md` and `design/kaizen.md` into a repository whose committed files are the public site. It asks only whether the repository is or may become public. `ledger.md` line 3 says the ledger goes "never into a tree whose committed files are published". Playbook step 3, which handles that, runs two skills later. Candidate key item for small-website: the deploy question, and whether committed files are published, come before the first write of the rollout. Report fix: ask playbook step 1 and the step 3 question in update's first rollout, before anything is written.
- **No instruction file (finding 2).** Update step 3 speaks only of "the project's existing instruction file". It does not say what to do when there is none, and it does not point to playbook step 3. This is the review finding L8 that was declined earlier; it is now hit by two runs. Candidate key item for all scenarios with no instruction file: update names where a missing file is created.
- **No look at a rendered page (finding 5).** The hallway-test text says "A rendered web page cannot be judged by eye yet". This is honest and N22 holds, but the page's layout stays untested. The report proposes a headless-browser driver, a new dependency to be asked about first.

Not checked by the main session, so listed as observations only:

- **Two meanings of "public" (finding 3).** The ledger's `Public:` question means the repository; for a site the repository can be private while its contents are public. The tester's "may become" answer was honest but misleading.
- **No build-step question (finding 7).** Nothing asks whether the host runs a build step, or whether the output is committed. This decides the design.
- **Indefinite block (finding 6).** With the owner "I don't know", the push is blocked indefinitely. The rule for publishing on one's own authority exists, but the agent's M6 question did not offer it.
- **Overlap of update and playbook (finding 4).** The playbook's lean (a separate repository for `design/`, M8) undoes what update had just committed.

Not counted: finding 8, that the README's hook section comes before First steps. It is NOT CONFIRMED, because the hook paragraph is at README:49, under "## Plugins", after "## First steps" (README:22).

Process notes: the tester ran `ls skills/`, slightly past the reading rules, and its expectations file predates its first command (mtime 13:46:51.419 against `date -Is` 13:46:51). The hallway-test step was planned but not reached.
