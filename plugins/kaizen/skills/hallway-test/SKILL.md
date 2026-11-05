---
name: hallway-test
description: Run a hallway usability test of a tool, document, instruction file or diagnosis process with a fresh sub-agent that sees only the requirements and user-facing documentation, writes expectations before running, and reports bugs, surprises and gaps; optionally judging a real terminal by eye through screenshots. Use it whenever the user wants a tool, command, CLI, notebook workflow, README, page or agent instruction file tried out by a critical first user, asks for a play test, usability test, "let someone try this", "test it as a new user", wants output checked in a real terminal rather than by parsing text, wants to know whether a user who skims the README and follows the program's hints gets there, or wants to measure how well a fresh agent copes with an instruction file or a fault.
---

# Hallway test

The name comes from grabbing a person in the hallway and watching them use the product. Here the person is a sub-agent that has not seen the implementation, the specs or the conversation that produced the code, so it cannot un-know what the author knows. It reads the requirements and the user-facing documentation, decides what should happen, tries it, and reports where reality differs. It regularly finds defects that the test suite has enshrined and that every scenario missed.

The test is the third moment for a persona and a process that the `walkthrough` skill imagined before the thing existed: the tester executes the same walk with fresh eyes, and the comparison of imagined and observed is the validation of the specification. Take the persona from the project's stakeholder record (`design/stakeholders.md`) and the coverage from the walk-through's steps and acceptance examples when they exist.

Modes, often combined:

- **Behaviour**: the tester builds test inputs, writes its expectation for each before running, runs the tool, compares, classifies.
- **By eye**: for output meant for people, the tester drives the tool in a real terminal and judges screenshots, which catches what text parsing never sees: output scrolled off, noise drowning the signal, lines wrapping, a pager hiding diagnostics. The bundled driver `${CLAUDE_PLUGIN_ROOT}/scripts/xterm-shots.py` starts an xterm under a virtual X server, sends keys and takes screenshots; it needs `xvfb`, `xterm`, `xdotool` and `imagemagick` (ImageMagick's `import`) installed, which a devcontainer or VM can carry.
- **Diagnosis**: the process under test is finding out what is wrong. The main session injects faults that look real into a running system; the tester gets the symptom, the persona and the user-facing documents only, and its investigation log, verdict, time and tokens are the measurement. Brief in `${CLAUDE_PLUGIN_ROOT}/references/diagnosis-brief.md`.
- **Hint-following (the impatient user)**: a first user who does not read. They skim the README for a command that looks like what they want, run it, and then follow only what the program prints, the way a good compiler or git leads you on. The tester sees the README only through `${CLAUDE_PLUGIN_ROOT}/scripts/skim.py` (headings and command blocks), because an agent told to be lazy still reads everything it is given: the laziness is enforced by what it can see. Every time the output gives no next step and the tester has to go back to the documents, the chain breaks; each break is a finding whose fix belongs in the program's output, with the text it should have printed. Measured: commands to the goal, breaks, minutes. Check the transcript afterwards: a `Read` of a documentation file that the brief did not allow invalidates the run. Brief in `${CLAUDE_PLUGIN_ROOT}/references/impatient-brief.md`. The other modes test whether the tool does the right thing; this one tests whether a person who reads nothing gets there.
- **Documents and instruction files**: the subject is a README, a guide or an agent instruction file (`AGENTS.md`, `CLAUDE.md`). For a README, the tester follows it from a clean checkout and reports where it stops. For an instruction file, the test is an evaluation: variants of the file in separate worktrees × typical tasks × one fresh, cheap agent per cell, an answer key written before the runs, a blind grader that did not write the variants, and the usage per cell; it decides layout questions by measurement instead of argument.

A borrowed checklist, with thanks: the eleven CLI usability criteria of the MIT-licensed cli-ux-tester skill by ali5ter, in `${CLAUDE_PLUGIN_ROOT}/references/cli-ux-checklist.md`, as an extra pass for command-line tools.

## Before launching

Settle these with the user; they become the tester's brief:

1. **The persona**, from the stakeholder record; offer to add one if the first user of this thing is not in it.
2. **What the tester may read.** Only what a first user would have: the requirements, the user documentation, the command's help. Name the files or directories; forbid the rest explicitly (source, tests, specs, design notes, git history). The point of the test is the fresh view; every extra document weakens it. If no requirements document exists, say so to the user before the test; a tester that has to invent the requirement tests its own invention.
3. **The tool and how to run it.** The command line or entry point, where test inputs may be created (a scratch directory, never the repository), what may be installed, what must not be touched (a read-only data mount is read-only).
4. **The coverage to insist on.** The acceptance examples by ID from `design/examples.md`, the walk-through's steps, the requirements' scenarios, the last test's gaps, plus "add experiments of your own". Each mandatory case names the example ID it serves, so that the tester asserts the outcome the user cares about and not the mechanism the author expects. Tell the tester to spend at least half its effort outside the list: the worst defects tend to lie outside every scenario. For by-eye tests: the scenarios, the terminal size, the keys to press.
5. **Who answers questions.** The tester asks the main session when the requirements do not say what should happen; the main session answers from the design and records what it could not answer confidently as TODO items for the owner.
6. **Where the record goes** and the summary length.

## The brief

Spawn a general-purpose sub-agent in the background with a brief built from the template in `${CLAUDE_PLUGIN_ROOT}/references/tester-brief.md`: the persona, the strict reading rules, the command reference as a user would get it, the method (create, write the expectation down first, run, compare, classify as matches / bug / surprising but defensible / gap / question), the mandatory coverage, the instruction to ask, and the report structure. For by-eye tests, use `${CLAUDE_PLUGIN_ROOT}/references/visual-brief.md`, which describes the driver and insists that the tester judges only screenshots; for diagnosis, `${CLAUDE_PLUGIN_ROOT}/references/diagnosis-brief.md`; for hint-following, `${CLAUDE_PLUGIN_ROOT}/references/impatient-brief.md`.

Two mechanics that the first uses taught:

- **Expectations are a file, written first.** The tester writes `expectations.md` in its scratch directory before its first run and reports its timestamp; the main session checks the order. A transcript with no expectation text and the first command in the first minute means the comparison is worthless.
- **The report comes back as the tester's final message.** Harness rules may forbid a sub-agent from writing report files; the main session writes the record from the message, with the screenshot file names, so that nothing is lost when the tester cannot write.

Model: a cheaper model is enough for the by-eye tester, which looks and reports, and for the eval cells of an instruction-file test; the behaviour and diagnosis testers benefit from the session's model, since they reason about what should happen.

## While it runs

Answer the tester's questions from the design, with the reasoning, and tell it when a question exposed a bug (then fix the bug in the normal way, with its test, and tell the tester the tool has changed). Keep a running list of what you could not answer with confidence; those go to the owner as decisions, not as your guesses.

## After

1. Read the report. Verify each bug claim against the code before accepting it; a tester with no source access describes symptoms, and the cause may differ. Get its cost from `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/usage.py agent-<its id>`.
2. Write the record to `design/hallway/<date>.md`: what held up, what was fixed with its test and spec scenario, the answers given, a TODO list for the owner with your lean per item, and for every defect "what would have caught this". Propose committing it on the working branch (commit it there if the person has asked you to commit): it becomes a source that requirements and specs cite, and a record that stays uncommitted can be lost while documents still cite it. The tester's long report is for agents; the human part is the summary at the top.
3. For every defect, add what would have caught it: a test, a rule, a check. A defect without that answer is only half fixed.
4. When the owner has decided the leans, the hand-over lists each accepted lean: implemented as agreed, or deviated and why.
5. Keep the experiment reproducible: the brief, the answer key or expectations, the answers given, the usage, and a small script that re-runs any experiment, saved together next to the record or in a named directory, with relative paths. This applies to every measurement, not only to hallway tests; an instruction-file eval whose prompts were not saved cannot be repeated.
6. If a walk-through preceded the test, add the comparison to it: per step, imagined versus observed.
7. With OpenSpec, the test runs after apply and before archive (the playbook's hand-off).

## Rules

- The tester never modifies the repository, never reads what it was forbidden, and says in the report what it was given, including anything the harness attached that it did not ask for.
- Expectations are written before running, or the comparison means nothing.
- A finding is a moment: the exact command, what was expected, what was observed, the relevant stderr lines or the screenshot file name.
- Do not fix during the test what the tester reported as a question; decide first whether it is a bug or a design choice, then fix with its test.
- A finding that is a vulnerability (data readable by the wrong user, a credential exposed, an unsafe default) is reported to the user first and the plan stops there; the fix path is the proposed next step, not an item further down the list.
- At the end, one line into the project's `design/kaizen.md`: what in this skill did not fit.
