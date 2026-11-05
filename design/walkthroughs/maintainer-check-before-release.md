# Walk-through: the plugin maintainer changes a skill and checks it before releasing

Persona: "The plugin maintainer" in `design/stakeholders.md`: whoever changes the skills (today the manager); knows the skill texts and the scripts; has this repository, its design record and the debriefs; wants "a way to test a skill before shipping it". Process: tighten the requirements interview (`plugins/kaizen/skills/requirements/SKILL.md`), then find out whether the plugin still works before releasing it.
Confidence: the persona entry is interviewed (the manager, 2026-11-05); the choice of persona and process for this walk was made by the calling agent and is not confirmed by the principal (no person available; playbook, "Working without a person"). The steps are simulated.
What exists (2026-11-05, branch `kaizen-0.4`, unpushed): `design/testing.md`; `design/requirements.md` 2.2, 2.7, 2.10; `design/examples.md` E1 to E6; `benchmarks/notes-tags/` (README, conditions, key, baseline); the check, being written while this walk ran and treated as planned: at the start neither `./check.sh` nor `tests/` existed; by the end `./check.sh` (runs `python3 -m unittest discover -s tests`, said to run from the pre-commit hook and CI), `tests/test_scripts.py` (tests marked E2, E4, E5) and `tests/test_lint.py` (frontmatter, body budget, dates as checked facts, plugin paths exist, bare reference names exist, stale strings, table rows match headers, versions and names) existed; their names and `check.sh` were read, nothing was run; the skill texts and references; `~/.claude/plugins/installed_plugins.json` (kaizen 0.3.0 installed from the marketplace on this machine). This walk is the intended source of `design/testing.md`.

## Steps

1. **Change the skill.** Does: edits `requirements/SKILL.md`, for example makes the frontier rule stricter or shortens the habits list. Needs to know: which examples and requirements the passage serves, so that a change can be checked against them. Goes wrong: the skill text cites no example IDs; the link from passage to E6 (frontier from the record) or S1 exists only in the maintainer's head. Would ask: "Which examples does this paragraph exist for?"
2. **Try it by hand.** Does: opens a session and types `/kaizen:requirements` on a small topic. Needs to know: which version runs. Goes wrong: the session loads the installed plugin, 0.3.0 from the marketplace cache, not the edited checkout. (Checked by the main session afterwards: the plugin registry does list 0.3.0, but the debrief session of 2026-11-05 loaded the skills from the checkout, with 0.4 text and the repository as base directory; how a session picks one or the other is not documented and was not verified. The need stands: the maintainer must be able to see which version ran.) Nothing in the repository says how to run the checkout's version in a session; the benchmark avoids the problem by having agents read the skills as files and telling them not to invoke the installed plugin (benchmark README, step 2). A maintainer who forgets gets a confident "works" from the old text. Would ask: "Am I testing my change or the release from last week?"
3. **Run the check.** Does: `./check.sh` (planned). Needs to know: what a green check means. What such a check can tell, from what exists:
   - The scripts still do what defects taught them: `tests/test_scripts.py` covers token counting once per message (E2), queued mid-turn messages and harness labels (E5), export refused into tracked directories (E4), option order, closed pipes, the skim view. Deterministic, seconds, no tokens.
   - The skill texts are well-formed: frontmatter; a body within a word budget; every `${CLAUDE_PLUGIN_ROOT}/...` path exists (checked by hand at the start of this walk: all 13 resolve); names of references exist; known stale strings are absent; tables are consistent; versions and names agree. A contradiction of the kind condition C found (briefs said `REPORT.md`, the skill said "final message") is caught only once it is written down as a stale string the lint knows; the next new contradiction is not.
   What it cannot tell: whether an agent following the tightened interview asks better questions, asks fewer, or stops asking; whether a changed description still fires the skill at the right moments; whether a passage that the budget allows is one an agent follows. Goes wrong: green looks like "works". The script tests cite E2, E4 and E5 (when first seen they named defects only; IDs were added during the walk); E1, E3 and E6, the examples about skill behaviour, have no test, and the check does not list uncovered examples. Would ask: "Green. Does that mean the interview still works?"
4. **Look for the behavioural test.** Does: opens `design/testing.md`. Needs to know: which fixture exercises the interview. Goes wrong: the fixture that would (number 3: a scripted principal who hides a need behind a solution and gives a number only when pressed) is described, not built. Status line: "nothing runs automatically yet". The harness's `claude plugin eval` is named but its format unchecked (requirements 2.2, unknown). Would ask: "So what do I run for the interview today?"
5. **Run the benchmark instead.** Does: follows `benchmarks/notes-tags/README.md`. Needs to know: which conditions a change to one skill needs, what it costs, how to read the difference. Goes wrong: the README runs three conditions; B and C need the OpenSpec CLI (a third-party Node package); nothing says that a change to the interview needs only A, or A and C. Cost of the baseline: about 130 k output tokens and ten minutes for the three conditions, plus a blind grader (the README's figure). The key items that touch the interview are K1 (need behind tags) and K5 (what the group drive is); but the agent plays the principal itself, so an interview that stops asking can still "find" K1 and K5 by its own reasoning; the benchmark measures the outcome of the whole chain, not the interview. Its own limit: "differences of one or two key items are noise", out of ten. Would ask: "If K5 disappears, is that my change or the dice?"
6. **Compare with the last run.** Does: looks for earlier results. Needs to know: the result of the last version. Goes wrong: there is no `results/` directory yet; the only comparison is `baseline.md`, taken at commit `40bf5c7`, before proposals 22 to 35 and the review fixes, and graded by the orchestrator, not blind. The next run changes both the plugin (many changes at once) and the grader (blind), so its difference from the baseline cannot be attributed to the interview change. Would ask: "What am I comparing against?"
7. **Decide to release.** Does: merges to `main` and bumps `plugin.json` (now 0.4.0). Needs to know: what "release" is and its checklist. Goes wrong: no document says what a release is (merge, tag, version bump), how colleagues receive it (auto-update is opt-in, README), or what is checked first. Requirements 2.10 says "each release is checked against the current Claude Code behaviour (sub-agent write rules, transcript format)"; there is no procedure or check for it. The release decision is the principal's (requirements, Release). Would ask: "What is the list I go through before I merge?"
8. **After the release.** Does: waits for use. Needs to know: whether the change hurt anyone. Goes wrong: real use is authoritative (testing.md, benchmark README), but every skill run writes its friction line into the ledger of the project where it ran; the maintainer sees only their own projects. A colleague's friction never reaches this repository unless someone files an issue. Would ask: "How would I hear that the interview now annoys people?"

## Product hat
The maintainer wanted a fast yes or no before releasing, and a slower signal of whether the behaviour got better or worse. "Done": a cheap check that catches broken references, broken scripts and text contradictions on every change, plus a behavioural run per skill that is cheap enough to do for each change to that skill and comparable with the last run. They would complain about: testing the installed version by mistake (2), a green check mistaken for a working skill (3), a 130 k-token benchmark whose result is within noise (5, 6), no list for releasing (7), silence from other people's projects (8).

## Developer hat
- Three layers, three costs: the check (seconds, deterministic, structural); per-skill fixtures with a key and a blind grader (minutes, tens of thousands of tokens, noisy, comparative); real use through debriefs (weeks, authoritative, slow). Only the first can block a release mechanically; the second gives a trend over runs, not a verdict.
- One run per condition is noise at ten key items; deciding on a change needs either several runs (cost multiplies) or key items specific to the changed skill.
- A fixture where the same agent plays principal and interviewer cannot test whether the interview asks; a separate scripted principal with withheld facts can.
- Model drift: a run on a new model version changes results without any skill change; each result must name the model and the plugin commit.
- `claude plugin eval` might run fixtures in CI; until checked, nothing behavioural runs automatically.
- Running the checkout's skills in a session (instead of the installed release) is a precondition for any hand test, and it is not documented.

## Questions for the owner
- What is a release of this plugin, and what must be green before it? (Step 7.)
- How should a session run the checkout's skills instead of the installed ones, and should the check refuse to run, or warn, when the installed version differs? (Step 2.)
- Is a behavioural run required for each change to a skill, or only before a release, and what token budget per run is acceptable? (Steps 4, 5.)
- Which fixture comes first: the scripted principal (interview, walk-through), the planted-moment transcripts (debrief), or the toy CLI with planted defects (hallway test)? (Step 4.)
- Should `./check.sh` list the examples in `design/examples.md` that no test or fixture cites, as the playbook asks before every hand-over? (Step 3.)
- How should friction from colleagues' projects reach this repository? (Step 8.)
- Is the next benchmark run a new baseline (blind grader, current commit) rather than a comparison with `baseline.md`? (Step 6.)

## Answers from the owner
None: no person was available during this run. All questions are open.

## Gaps
- No documented way to run the checkout's skills in a session (step 2).
- No mapping from skill passages to example IDs (step 1). E1, E3 and E6 have no test or fixture, and nothing lists uncovered examples (step 3).
- Fixture 3 (scripted principal) does not exist (step 4).
- No per-skill selection of benchmark conditions, no `results/`, no comparable baseline for the current commit (steps 5, 6).
- No release definition or checklist; the "checked against current Claude Code behaviour" requirement has no procedure (step 7).
- No channel from other projects' ledgers to the maintainer (step 8).

## Acceptance examples
E12, E13, E14, E15, E16 (added to `design/examples.md`, unconfirmed).

## What `design/testing.md` can take from this walk
- The check (`./check.sh`): structural and deterministic; tells the maintainer the scripts and the texts are intact (E12, E13); cannot tell whether a skill still works.
- Per-skill fixtures with a key, a separate scripted principal where a person is needed, a blind grader, the model and commit recorded; comparative, noisy; tell a trend over runs (E14, E15).
- The benchmark: an end-to-end run of the whole chain on one change request; shows gross regressions and what each process stage contributes; too coarse and too costly to judge one paragraph of one skill.
- Real use through debriefs: authoritative, slow, and today reaches the maintainer only from their own projects.
- Precondition for all hand tests: the checkout's version is the one running (E16).

## Questionnaire
- 2.5 Reliability: how is a skill that got worse noticed, and by whom, if not by the maintainer's own use?
- 2.6 Performance: budget in tokens and minutes for a check before a release.
- 2.7 Testing and service: what the release is, who signs it off (record: the principal), what must pass.
- 2.10 Lifetime: how the "checked against current Claude Code behaviour" requirement is carried out per release.
