# Run 2026-11-19 (3): scenario existing-tool, commit `ff5c1c0` (the fixes of ledger 316), Opus, about 2 minutes

Confirming run for ledger 316, graded by the main session, not independent, and only on N56 and 316 (a) to (c); the full grading of this scenario is in `2026-11-19-existing-tool-2.md`. Usage of the tester (`usage.py agent-aa60d7c94742e4e87`): Output tokens, claude-opus-5-5 14,108 .

The tester's report follows unchanged.

## Self-test report: scenario existing-tool, commit ff5c1c0

**Files read.** In this order:
- `/tmp/kaizen-selftest-existing-tool-c_90t7iy/kaizen/README.md`
- `plugins/kaizen/skills/update/SKILL.md`
- `plugins/kaizen/skills/hallway-test/SKILL.md`
- `references/words.md`
- `references/tester-brief.md`
- `references/cli-ux-checklist.md`
- `references/ledger.md`
- the first 40 lines of `references/wording-review.md`
- project files: `README.md`, `tally.py`, `ls logs/`

I also listed the names in `skills/`, which the README lists anyway.

Scripts run: `version.py hallway-test a0ed1877` printed nothing (exit 0). `version.py --project` printed "first rollout". Two runs of the tool itself: `tally.py --help` ends in a FileNotFoundError traceback, and running it with no arguments prints the usage line with exit 0.

**Timing.** `expectations.md` has mtime 14:08:25.97. The first command (`date -Is`) ran at 14:08:28. The file came first.

### Path
- **1** I read the README and described the install, without running it. The README's bold "**Then, once in each project**: `/kaizen:update`" conflicts with what the newcomer actually wants (a test now). I chose the scenario: the first request went in directly, and the update was left to the skill's own suggestion.
- **2** "Can you test it before my colleagues use it?" led to `/kaizen:hallway-test`: the skill description matches the newcomer's wording almost exactly. The version line was silent, which is correct.
- **3** Message 1: the reading of "test", the no-requirements line, and five questions. The answers:
  - Who uses it: "my two colleagues, a bit of Python, they know the logs" [made up].
  - How a wrong result would show: "I don't know, I'd compare with grep" [made up].
  - Which cases matter: "I don't know".
  - Available during the run: "here for an hour" [made up].
  - Update and visibility: "skip the update; design/ is fine; not public" [made up].
- **4** Message 2 (leans 6–11) and message 3 (leans 12–13, the record and the ledger): the newcomer answered "yes" [made up].
- **5** Message 4 (model, cost, duration): "yes" [made up].
- **6** Files written:
  - branch `hallway-test-tally`
  - `project/design/stakeholders.md` (one entry, fields that were not asked marked unknown)
  - `project/design/hallway/2026-11-19-brief.md`
- **7** Hand-over point. That's what I would have done now: copy the README, `tally.py` and `logs/` into scratch, then start a background behaviour tester with the brief. Per the skill's measured figure that is about 14 min (46 k output tokens); the record would go to `design/hallway/2026-11-19.md` and a friction line into a new `design/kaizen.md`.
- Not asked: what "test" meant to the newcomer (the agent stated its reading and offered a correction, as intended).

### Findings, ranked
- **1 Gap.** Cost is stated only in minutes and tokens. The skill (item 9) says "Give the cost in minutes … output tokens only in brackets". The standing instructions use "$20 at list price", and the README's developer section uses dollars ("$97"). A newcomer with no budget set cannot connect minutes to money or to their plan. Fix: one line on what the minutes mean against a plan limit, or a money figure where one is known.
- **2 Question / gap.** The measured model differs from the recommended one. The measurement is "14 minutes (46 k) … (Sonnet)", while the advice is "behaviour … testers benefit from the session's model". On Opus, the only figure the skill gives turns into a guess. Fix: give one measured figure per recommended model, or recommend the model that was measured.
- **3 Gap.** The skill never says how to detect "neither standing instructions nor a ledger" (item 7). I ran `version.py --project`, which only the update skill names. Fix: name that command in item 7.
- **4 Surprising but defensible.** The README sends a newcomer to `/kaizen:update` before anything else. For "test my tool before Monday" that is a detour; the hallway-test suggestion ("once") handles it better. Fix: the README could say "or start with the skill you need; it will suggest the rollout".
- **5 Gap.** "Which cases matter most" got "I don't know". Item 5 says to offer a short walk-through (`/kaizen:walkthrough`) when no coverage is named. My leans only offered it in one clause, and the first-message list does not mention the offer, so it is easy to miss.
- **6 Surprising.** A new ledger appears as a side effect. The Rules' end line ("one line into the project's ledger … A new ledger starts from…") creates `design/kaizen.md` in a project that asked for none. That file is aimed at improving the plugin and is opaque to a newcomer. The skill does force it into its own message, which helps.
- **7 Question.** The skill numbers its own steps 1–9 and cites them ("(item 3)", "(item 9)"). The agent's numbering across messages then runs 1–14, so "item 9" means different things in the two places. An agent could mix them up.
- **8 Defensible.** Item 3 says "A tool that only reads and prints needs none of the rest", but copying the data into scratch sits in that skipped rest, while item 2 also asks for the copy. This is resolvable, but read literally it contradicts.
- **9 Worked.** Things noticed in the code stayed out of the brief, as the skill requires: `--help` gives a traceback, the usage message exits 0, and the docstring says three levels where the regex matches five. They are kept for the record.

Checked against the scenario's "note in particular":
- The agent states its reading of "test" first: yes, required and given as an example.
- The plugin leads to the hallway test: yes, through the skill description.
- Built but no requirements: it goes ahead, says so, and promises `/kaizen:requirements` afterwards.
- "Tests its own invention" is said, both in the skill and in the brief template.
- The persona comes from the newcomer's answer, marked "not on record".
- Cost is stated before the start, but not in money.
- Hand-over point: after the explicit yes to message 4.

### The agent's messages, word for word
**Message 1** (about 13 lines; no restart):
> I read "test" as a hallway test: a fresh agent tries `tally` as a first user would, with only your README, and reports what breaks or surprises it; not automated tests of the code. Say so if you meant those.
> There are no written requirements, so the tester checks against your README; where it has to invent a requirement, it tests its own invention, and its report marks those.
> - **1** Who uses `tally` first, and what do they already know (Python, these instrument logs)?
> - **2** How would you notice a wrong count? Is there a log whose counts you know?
> - **3** Which cases matter most: kinds of logs, sizes, levels?
> - **4** During the run the tester may ask questions the README does not answer. Will you be around to answer, or should it collect them for afterwards?
> - **5** Where should the test's record go? I'd create `design/hallway/` on a new branch. The plugin suggests running `/kaizen:update` once first (you type it): it adds its standing instructions, a short block of rules for me, to a CLAUDE.md. Is the repository public, or may it become so?

**Message 2** (about 15 lines; continues the numbering):
> Thanks. My leans, the answers I'd pick; one "yes" takes them all, or name a number to change:
> - **6** Persona: a colleague from your group who knows a little Python and these logs and has only the README; your description, not yet on record.
> - **7** Start a stakeholder record, `design/stakeholders.md`, with that one entry (role, knowledge; the rest marked unknown).
> - **8** The tester reads only the README and runs copies of `tally.py` and `logs/` in a scratch folder outside the project; it is told not to open the script, which is the source.
> - **9** Mode: behaviour test (it writes logs with counts it knows, predicts, runs, compares), plus a pass over an eleven-point checklist for command-line tools (help, error messages, exit codes).
> - **10** Coverage, as you named none: logs with known counts, including hard ones (a level word inside a message, lower case, an empty or missing file), plus its own experiments. `tally` only reads the logs, never writes them (from the code). A short walk-through of a colleague's first steps could come first; my lean: not now.
> - **11** The tester's questions come to you through me while you are here.

**Message 3** (4 lines):
> - **12** Record: `design/hallway/2026-11-19.md` with the brief beside it, on a new branch `hallway-test-tally`; I commit only when you say so.
> - **13** At the end I add one line to a new `design/kaizen.md`, the plugin's ledger of what did not fit, committed with the record (not public, as you said).

**Message 4** (5 lines):
> - **14** Before I start it: the tester runs on this session's model (Opus), in the background. A behaviour test of a small command-line tool took about 14 minutes (46 k output tokens) when measured, on a cheaper model (Sonnet); for `tally` that is a guess of 10 to 15 minutes. While it runs you can note anything for a later review as "note for the debrief: …". Start?

### Words the newcomer would not know
- **(a) In the agent's messages:**
  - "standing instructions" is explained only loosely.
  - "ledger" is explained, but only after first use in the same line.
  - "behaviour test" is explained in brackets.
  - "debrief" is not explained.
  - "output tokens" is not explained.
  - "Opus/Sonnet" are not explained.
  - "on record" is not explained.
  - Two names: "hallway test" and "tester"/"fresh agent" are used for the same thing; "record" means both the test record and the stakeholder record.
- **(b) In the plugin's files:**
  - Undefined at the point of use: "principal", "small path", "need note", "decision record's safety row", "OpenSpec", "trailer", "upstream".
  - "leans" appears in the README before `words.md` is reached.
  - "skill friction" and "acceptance example IDs" are undefined in the hallway skill.
  - Two names: "inbox" = "Notes for the next debrief" (`words.md` admits it); "principal" / "person" / "owner"; "hallway test" / "play test"; "persona" / "first user"; "behaviour" mode vs "behaviour test".

### What worked well
- The skill description catches the newcomer's exact phrasing.
- Stating the reading of "test" before acting is mandatory and comes with a model sentence.
- The no-requirements case is handled without blocking, with the "own invention" caveat in both the skill and the brief template.
- The persona path is clear when there is no stakeholder record.
- The rule against putting code knowledge in the brief stops the author's view leaking to the tester.
- The silent version check works.
- The message-size rule keeps the agent's messages short.

**Setup misfit:** the scenario's first request skips the README's bold "`/kaizen:update` once in each project" step, so the rollout path went untested here.
