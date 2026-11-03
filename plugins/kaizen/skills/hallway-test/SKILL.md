---
name: hallway-test
description: Run a hallway usability test of a tool with a fresh sub-agent that sees only the requirements and user-facing documentation, builds its own test cases, writes expectations before running, asks questions, and reports bugs, surprises and gaps; optionally judging a real terminal by eye through screenshots. Use it whenever the user wants a tool, command, CLI, notebook workflow or page tried out by a critical first user, asks for a play test, usability test, "let someone try this", "test it as a new user", or wants output checked in a real terminal rather than by parsing text.
---

# Hallway test

The name comes from grabbing a person in the hallway and watching them use the product. Here the person is a sub-agent that has not seen the implementation, the specs or the conversation that produced the code, so it cannot un-know what the author knows. It reads the requirements and the user-facing documentation, decides what should happen, tries it, and reports where reality differs. In the modama crawler this found twenty experiments' worth of behaviour in an afternoon, including defects the test suite had enshrined.

Two modes, often combined:

- **Behaviour**: the tester builds test inputs, writes its expectation for each before running, runs the tool, compares, classifies.
- **By eye**: for output meant for people, the tester drives the tool in a real terminal and judges screenshots, which catches what text parsing never sees: output scrolled off, noise drowning the signal, lines wrapping, a pager hiding diagnostics. The bundled driver `${CLAUDE_PLUGIN_ROOT}/scripts/xterm-shots.py` starts an xterm under a virtual X server, sends keys and takes screenshots; it needs `xvfb`, `xterm`, `xdotool` and `imagemagick` (ImageMagick's `import`) installed, which a devcontainer can carry.

A borrowed checklist, with thanks: the eleven CLI usability criteria of the MIT-licensed cli-ux-tester skill by ali5ter, in `${CLAUDE_PLUGIN_ROOT}/references/cli-ux-checklist.md`, as an extra pass for command-line tools.

## Before launching

Settle these with the user; they become the tester's brief:

1. **What the tester may read.** Only what a first user would have: the requirements, the user documentation, the command's help. Name the files or directories; forbid the rest explicitly (source, tests, specs, design notes, git history). The point of the test is the fresh view; every extra document weakens it.
2. **The tool and how to run it.** The command line or entry point, where test inputs may be created (a scratch directory, never the repository), what may be installed, what must not be touched (a read-only data mount is read-only).
3. **The coverage to insist on.** A list of cases the tester must cover, from the requirements and from the last play test's gaps, plus "add experiments of your own". For by-eye tests: the scenarios, the terminal size, the keys to press.
4. **Who answers questions.** The tester asks the main session when the requirements do not say what should happen; the main session answers from the design and records what it could not answer confidently as TODO items for the owner.
5. **The report location** and the summary length.

## The brief

Spawn a general-purpose sub-agent in the background with a brief built from the template in `${CLAUDE_PLUGIN_ROOT}/references/tester-brief.md`: the persona ("a research software engineer trying this for the first time, as a critical early user"), the strict reading rules, the command reference as a user would get it, the method (create, write the expectation down first, run, compare, classify as matches / bug / surprising but defensible / gap / question), the mandatory coverage, the instruction to ask, and the report structure. For by-eye tests, use the brief in `${CLAUDE_PLUGIN_ROOT}/references/visual-brief.md`, which describes the driver and insists that the tester judges only screenshots.

Model: a cheaper model is enough for the by-eye tester, which looks and reports; the behaviour tester benefits from the session's model, since it reasons about what should happen.

## While it runs

Answer the tester's questions from the design, with the reasoning, and tell it when a question exposed a bug (then fix the bug in the normal way, with its test, and tell the tester the tool has changed). Keep a running list of what you could not answer with confidence; those go to the owner as decisions, not as your guesses.

## After

1. Read the report. Verify each bug claim against the code before accepting it; a tester with no source access describes symptoms, and the cause may differ.
2. Write the persistent record where the project keeps design notes (for example `design/playtest.md`): what held up, what was fixed with its test and spec scenario, the answers given, and a TODO list for the owner with your lean per item.
3. For every defect, answer "what would have caught this" and add that: a test, a rule, a check. A defect without that answer is only half fixed.
4. Keep the tester's trees and screenshots reproducible: a small script that re-runs any experiment, saved next to the report or in the scratch directory, with the path named in the record.

## Rules

- The tester never modifies the repository, never reads what it was forbidden, and says in the report what it was given, including anything the harness attached that it did not ask for.
- Expectations are written before running, or the comparison means nothing.
- A finding is a moment: the exact command, what was expected, what was observed, the relevant stderr lines or the screenshot file name.
- Do not fix during the test what the tester reported as a question; decide first whether it is a bug or a design choice, then fix with its test.
