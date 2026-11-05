# Walk-through: the colleague starting with agents installs kaizen and runs their first debrief

Persona: "The colleague starting with agents" in `design/stakeholders.md`: an ER-C research software engineer or scientist who has used Claude Code for a few sessions on their own project; knows their science and code, not the agent's conventions, memory locations or plugin mechanics; has a fresh checkout and possibly Codex instead of Claude Code; reads the README only for headings and commands to copy, then follows the program's output. Goal of this process: a debrief report and a ledger in their project, i.e. "how am I doing with the agent, and what should I change".
Confidence: simulated. The persona entry itself is simulated (stakeholder record). The choice of this persona for this process was made by the calling agent, not confirmed by the principal; this run had no person available (playbook, "Working without a person"), so the whole walk rests on that unconfirmed choice. Nothing below was said by a real colleague.
What exists (read 2026-11-05 on branch `kaizen-0.4`, unpushed): `README.md`; its skim view (`python3 plugins/kaizen/scripts/skim.py README.md`); `plugins/kaizen/skills/debrief/SKILL.md`; `transcript.py --help` and `transcript.py locate`, `usage.py --help` and `usage.py` without arguments, run on this repository; `plugins/kaizen/.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`; the scripts' imports and annotations. Not run: the install itself and a debrief (both change state; a debrief would read transcript content). The marketplace currently installs 0.3.0 (`~/.claude/plugins/installed_plugins.json` on this machine), so a colleague installing today gets 0.3.0, not what is walked here.

## Steps

1. **Find the plugin.** Does: follows a colleague's link to the GitHub repository, opens `README.md`, skims. Needs to know: what this gives them, in one line, and what to type. Goes wrong: the first line is "A place to keep and share my AI agent skills"; the one-line purpose of kaizen sits in a bullet under "Plugins", which the skim view drops. Would ask: "Is this the thing that tells me how I am doing with Claude, or something for the author?"
2. **Install.** Does: copies the two commands under "Install" (`claude plugin marketplace add uellue/skills`, `claude plugin install kaizen@uellue --scope user`). Needs to know: whether a running session must be restarted to see the skills; that the plugin is Claude Code only. Goes wrong: if they use Codex (stakeholder record: possible), nothing tells them at the install step that none of this applies; the Codex note is in requirements 2.8, not the README. Whether installing needs GitHub access from their machine (VM, devcontainer, institute network) is not said. Would ask: "Do I need to restart Claude? I use Codex mostly, does this work there?"
3. **Find the command.** Does: looks for the command that runs a debrief. Needs to know: `/kaizen:debrief`. Goes wrong: in the skim view (headings and command blocks only, which is how this persona reads and how the hallway test's hint-following mode enforces it) the README shows the install block and then eight paste-in text blocks under "Working with agents"; `/kaizen:debrief` appears only in prose. The chain of hints breaks right after install, unless the install command itself prints the skills (not verified: install not run). Would ask: "OK, installed. Now what do I type?"
4. **Start the debrief.** Does: opens a new Claude Code session in their project and types `/kaizen:debrief` (or "debrief me"). Needs to know: which sessions will be looked at. Goes wrong: the skill's inputs say "the transcripts" without saying which ones by default, and `usage.py` without arguments reports "the current session (newest transcript of this project)". Run here, it reported the session that ran it (this walk-through, `8ccc3714`), not the work before it. In a fresh session that is the debrief session itself. Whether the agent then asks, picks the previous session or debriefs itself depends on the agent, not on the skill. Would ask: "Is it looking at what I did yesterday, or at this conversation?"
5. **Choose the sessions.** Does: if asked, looks at `transcript.py locate` output. Needs to know: which of the listed sessions was "the one where I fought with the build". Goes wrong: `locate` lists id, time span, size, message counts and path: no topic, first prompt or branch. Choosing by timestamp works for a person who remembers when; it does not for a week of sessions. Would ask: "Which of these is the one about the plotting script?"
6. **Wait for it.** Does: lets it run. Needs to know: how long and what it costs (the stakeholder record says this persona wants to know "what it costs"). Goes wrong: nothing in the README or the skill tells the person the cost before it starts. The figures in the record: one debrief of seven sessions took about 1.5 M tokens of readers and an hour (requirements 2.6); the skill budgets about 200 k tokens per reader for a day-long session. A colleague debriefing "my last week" would set off the multi-session mode without a number in front of them. Would ask: "Is this going to eat my budget for the month?"
7. **Privacy of what is written.** Does: nothing; the agent writes `.claude/debriefs/<date>.md` (with coaching) and `design/kaizen.md`. Needs to know: that the coaching file is private and must not be committed; that `design/` is created in their repository; what the ledger will contain. Goes wrong: in this repository `.gitignore` excludes `.claude/debriefs/`; in theirs nothing does. The skill says "check that ... is ignored, and say so if it is not", then writes anyway; a colleague who commits with `git add -A` (common among people new to git hygiene, an assumption) commits candid coaching about themselves into a group repository. The skill also creates `design/` without asking, in a project that may keep its docs elsewhere. Would ask: "Who else can see this? Why is there a new design folder in my repo?"
8. **Read the report.** Does: opens the report. Needs to know: what "ledger", "kaizen", "L-markers", "destination", the severity dots mean; that "debrief on the collaboration, not on what it produced" means no code review. Goes wrong: citations like `L1234` point into a rendering they never saw; a person expecting a code review is surprised by coaching addressed to them, written "without softening". Would ask: "What is L1234? And why is it criticising how I write prompts, I wanted to know if my code is ok."
9. **Act on proposals.** Does: reads the proposals table. Needs to know: how to approve one (reply in the session) and that nothing was applied yet. Goes wrong: if the session has ended, the approval path is gone; the ledger lists the proposals but the skill does not say how a later session picks up "apply proposal 3". Would ask: "I closed the window. How do I say yes to number 3 now?"
10. **Done.** For them: a report they understood, one or two habits to change, and the confidence that nothing private went public. The second debrief should show whether they changed anything (earlier recommendations table); whether this persona ever runs a second one is unknown.

Developer-side check run alongside step 4: `transcript.py` and `usage.py` use `str | None` in function annotations without `from __future__ import annotations`, so they need Python 3.10 or newer (read from the code, not run on an older Python). Neither the README nor the skill says so; on a system Python 3.9 the scripts would stop with a traceback before printing anything.

## Product hat
They wanted "am I using this well, and what should I do differently", cheaply, privately. "Done" is a short report they understand without knowing the plugin's vocabulary, with two or three concrete habits. They would complain about: having to read the README after all (step 3), not knowing what it costs (6), a debrief of the wrong session (4), coaching that lands in git (7), jargon (8). The README's strongest part for them, the lessons and paste-in blocks, is reachable in the skim view; the plugin's own entry point is not.

## Developer hat
- Session choice defaults to "newest", which in the typical flow (new session, then `/kaizen:debrief`) is the debrief itself (steps 4, 5).
- Writes into the person's repository before asking (7); a private file next to a tracked tree relies on an ignore rule that only this repository has.
- Transcripts contain whatever was pasted, credentials included (requirements 2.9); the report quotes moments from them; quoted secrets would land in a file that may be committed (7). The skill's privacy rules cover the ledger, not the report's quotes.
- Python version floor undocumented (step 4 note).
- What a colleague installs today is 0.3.0; this walk is of 0.4 on an unpushed branch, so any hallway test of it must install from the branch or read the files.

## Questions for the owner
- Is the colleague the intended first user of the debrief, or is it for the manager first and colleagues later? (Steps 1, 8; requirements 1.4 orders the audience.)
- When `/kaizen:debrief` runs in a fresh session with no stretch named, which sessions should it take? (Step 4.)
- Should the debrief write anything into a colleague's repository before the person has seen where it goes and whether the private report is ignored by git? (Step 7.)
- Should a debrief state its expected cost before reading, and what is an acceptable cost for a colleague's weekly debrief? (Step 6.)
- What is the minimum Python and the supported environments (Codex users, institute network without GitHub)? (Steps 2, 4.)
- Should the README's skim view carry the first command to run after install? (Step 3.)

## Answers from the owner
None: no person was available during this run. All questions are open; confidence stays simulated.

## Gaps
- No README entry point for the skimming user: the command after install is not in a heading or a code block (step 3).
- No default or rule for which sessions a debrief covers when none is named (step 4).
- `locate` offers no way to recognise a session by topic (step 5).
- No cost statement before a debrief starts; no figure for a single-session debrief of a colleague (step 6; requirements 1.3 lists this figure as unknown).
- No rule that the debrief stops or asks when the private report would be tracked by git; the ignore lines exist only in this repository (step 7).
- No glossary of the report's vocabulary for a first-time reader (step 8).
- No documented way to apply a proposal from a later session (step 9).
- No stated Python floor or Claude Code-only note at install (steps 2, 4).

## Acceptance examples
E7, E8, E9, E10, E11 (added to `design/examples.md`, unconfirmed).

## Questionnaire
- 1.3 Benefits: what does a debrief buy a colleague who is not the author, in time per week? (Already listed as unknown in the record.)
- 1.4 Users: is the colleague in the audience for 0.4, or later? How many colleagues, how often?
- 2.4 Operating conditions: which Python, OS, network (GitHub reachable?) do colleagues' machines have?
- 2.6 Performance: acceptable cost and duration for a colleague's single-session and weekly debrief.
- 2.7 Installation and service: how a colleague gets help when a skill misbehaves; how their skill-friction lines reach the maintainer.
- 2.9 Jurisdictions: coaching and quoted transcript content in a repository shared with a group; personal data of others in a transcript.
