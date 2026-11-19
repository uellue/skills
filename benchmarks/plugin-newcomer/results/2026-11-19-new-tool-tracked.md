# Run 2026-11-19: scenario new-tool-tracked (fixed from a varied seed), commit `9dc61a6` (the fixes of ledger 317), Opus, about 3 minutes

Confirming run for ledger 317, graded by the main session, not independent, on its key items only: N59 held: the block goes into the existing CLAUDE.md beside the project's rules (overlaps named and kept), the ledger stays out of the published docs/; N60 held: the playbook read the tracker (#3) before asking who needs the tool. The full grading of the varied run this scenario came from is in `2026-11-19-varied-*.md`. Usage of the tester (`usage.py agent-a8c11f993e9a7b43f`): Output tokens, claude-opus-5-5 15,726 .

The tester's report follows unchanged.

## Read, and timing
I read the README, `skills/playbook/SKILL.md`, `skills/update/SKILL.md`, `skills/requirements/SKILL.md` (lines 1–40, up to where the real interview would start), and from `references/` the files `words.md`, `companions.md` (first 80 lines), `standing-instructions.md` and `ledger.md`. I also read the output and `--help` of `version.py`, and the project's `CLAUDE.md`, `DEPLOY.md` and `.tracker/issues.json`.
- `expectations.md` was written before my first command. The first command (`date -Is`) printed 2026-11-19T14:23:34+01:00.

## The path
- **1** Playbook. `version.py playbook be291086` printed nothing (silent, as it should be). Step 1 asked where the tool writes and whether the spectra are the originals. My answer [made up]: a separate output folder; the instrument PC keeps the originals for a few weeks.
- **2** Playbook step 1, second round, because the public site counts as something real it could damage. Owner: me. Risk: a broken page, which I may authorise. Stand-in: none, and I don't know how to make one. All [made up].
- **3** Playbook step 2. The agent read the tracker and found #3. Who needs the tool: "me, maybe that colleague; I don't know exactly what they need" [made up].
- **4** Playbook path: the new-project path, i.e. the full process. No question.
- **5** Playbook step 3. It suggested `/kaizen:update` and asked whether the repository is public. Answer: "private" (a scenario fact, given because it was asked).
- **6** Playbook steps 4–7: no companions present; no case named; nothing to ask. Not asked.
- **7** `/kaizen:update`. `version.py --project` printed "first rollout". It proposed a branch, and I agreed [made up].
- **8** Update, step 3: two overlaps with my rules plus the block. I said yes to all three [made up].
- **9** Update, steps 4 and 5: tracker confirmed as GitHub; #3 named. "I'll answer it myself" [made up]. It did not ask how far back to look at closed issues, though the skill says to; I skipped it because there were none.
- **10** It wrote to the project on branch `kaizen-rollout`: the `CLAUDE.md` section and `design/kaizen.md`, committed as ca0019c. Hand-over, next step `/kaizen:playbook`.
- **11** Requirements: that's what I would have done now: round 1 (the vocabulary question, then sections 1.1–1.4 with leans), producing `design/requirements.md` and `design/stakeholders.md`. The skill states no cost.

## Findings, ranked
- **1 (gap)** The README says "Then, once in each project: `/kaizen:update`", but its "First steps" says "Not sure where you are? Start with `/kaizen:playbook`". The playbook only suggests the rollout in step 3, after three rounds of questions. The answer to "What should I do first?" arrived in message 5.
  - Fix: on a first rollout, the playbook answers the question first, in one line ("type `/kaizen:update`"), and only then asks the rest.
- **2 (gap)** No cost is stated anywhere a newcomer meets. Neither the playbook, the update nor the requirements skill says what the rollout or the interview costs; the README's cost section is for plugin developers.
  - Fix: one line of cost in the playbook's path message.
- **3 (gap)** `companions.md` sends Matt Pocock's ADRs to `docs/adr/`. In this project `docs/` is the public site, so a recommended companion would publish them.
  - Fix: apply the playbook's step 3 publication check to the companions' folders as well.
- **4 (surprising)** `version.py playbook <id>` silently wrote `.git/info/kaizen-update-noticed` (content `0.6.1-dev.2`) on a first rollout and printed nothing. Nobody announced the write.
  - Question: does the marker suppress a later reminder if the newcomer never runs the rollout?
- **5 (gap)** The update's first rollout says "ask where its files would end up … unless the project already says". The playbook had already asked this in the conversation, but nothing in the project says it. Taken literally, the update asks twice.
  - Fix: "unless the project or this session already says".
- **6 (question)** The template's ledger requires a line `Message size: …`, but the update says that question "waits for the first debrief". The line's content in between is unspecified; I wrote "not asked yet".
- **7 (question)** Playbook step 3 says "ask whether committed files become public … unless step 1 already told you". `DEPLOY.md` covers only `docs/`, so whether step 1 "told" is ambiguous. I asked.
- **8 (question)** The playbook's Rules ("At the end, one line into the project's ledger … start it from the template") would create `design/kaizen.md` before `/kaizen:update` decides where it goes. I deferred it.
- **9 (surprising but defensible)** "Larger change or a new project: the full table": a small CSV converter gets the full requirements form. The small path ("one command … a few hours") may fit better.
- **10 (gap)** The tracker is read twice: playbook step 2 for users, update step 5 for waiting issues. Neither tells the agent to announce the read.
- **11 (surprising)** Update step 5 asks how far back to look at closed issues "with no version or date". That question is pointless in a project with nothing in it.

## The agent's messages (verbatim)
- **M1** (6 lines, no restart): "Before I suggest a first step, one question about what the tool will touch. - **1** The converter reads your instrument's spectra and writes CSV. Where should the CSV files go: next to the spectra, into a separate folder, or elsewhere? And are the spectra it reads the originals from the instrument, or copies (is there another copy anywhere)? I also see in `DEPLOY.md` that every push to `main` publishes `docs/` as your group's public site; I'll keep that in mind."
- **M2** (11 lines, no restart): "Thanks. One thing here is live and public: pushing to `main` publishes `docs/` as the group's public site. Three short questions about it: - **2** Who owns that site, that is, who may decide what appears on it? If you publish there on your own authority, that is you; if someone else must approve changes, who? - **3** What could go wrong there (for example a page broken in public, or something published that should not be), and who may authorise a push that changes it? - **4** Is there a stand-in, such as a local preview of the site, or a branch that does not deploy? If not, the cheapest is to work on a branch and preview `docs/` locally before merging. Until **2** is answered, I will not push to `main`: a push there is a release. Reading and writing locally on a branch is fine meanwhile."
- **M3** (6 lines, no restart): "I looked at the open issues (`gh issue list`): #3 from a colleague, "How do I run this on my own files?", open for a week with no answer. So at least one colleague wants to use the tool too. - **5** Who needs this tool besides you, and what would you and they do differently once it exists? "I don't know" is a fine answer; then the first step is to find that out."
- **M4** (8 lines, no restart): "Thanks. Since this is a new tool, I suggest this order; each step is a short conversation, and I write nothing without asking: - **6** First: a short interview on what the converter must do and for whom, written down as a list of requirements (`/kaizen:requirements`). - **7** Then: we go through how you and your colleague would use it, step by step, to find open questions and concrete examples of correct output (`/kaizen:walkthrough`). - **8** A short record of what we decided, then building it, on a branch. - **9** Before your colleague uses it: a fresh agent tries it as a first user would (`/kaizen:hallway-test`), and afterwards we look back at how the work went (`/kaizen:debrief`)."
- **M5** (7 lines, no restart): "None of the plugin's documents exist yet, and the plugin has not been set up in this project. - **10** The plugin's setup is a command you type yourself: `/kaizen:update`. It reads your `CLAUDE.md`, proposes adding the plugin's rules for the agent as one section of it, and asks where the plugin's files may go, all on a branch. I suggest doing that first. - **11** The requirements would go into a new folder `design/` (`design/requirements.md`, plus a short list of the tool's users in `design/stakeholders.md`), committed with the project. Is this repository public, or may it become public? `design/` is outside `docs/`, so the site would not publish it."
- **M6** (10 lines, no restart): "This is the plugin's first rollout in this project. What it adds, briefly: - **12** Rules for the agent (the plugin calls them "standing instructions"): about 17 lines, as a new section in your `CLAUDE.md`, beside your own rules. - **13** A short file where notes on how we work together collect (the "ledger"), `design/kaizen.md`, committed; the repository is private and `design/` is outside the published `docs/`, so it stays off the site. - **14** Later, only when a skill needs them: the requirements and the list of the tool's users, also in `design/`. All of it goes on a new branch, `kaizen-rollout`, not on `main`, so nothing is published. Nothing is written before you agree. Shall I go ahead on that basis?"
- **M7** (10 lines, no restart): "Your `CLAUDE.md` has two rules that touch lines of the plugin's block: - **15** "Keep diffs small; one concern per pull request." The block's line "Keep changes tight: no speculative generality, …" is about what to build, not diff size. I lean to keeping yours as it is and adding the block's line beside it. - **16** "Tests: `python3 -m pytest`." The block says to report "clean" only from the command the commit or CI runs. I lean to naming `python3 -m pytest` in that line. - **17** The whole block goes in as one section, `## Kaizen standing instructions`, after your rules; its first line names the plugin version (0.6.1-dev.2) so a later update can see what changed. Take **15** to **17** as proposed?"
- **M8** (9 lines, no restart): "Two settings, and a first look at your issues: - **18** Your issues are on GitHub (I read them with `gh issue list`). I'll record that in the ledger as the project's tracker; correct? - **19** Issue #3 from a colleague, "How do I run this on my own files?", has waited a week with no reply. It asks you for an answer: there is no tool yet, so perhaps when to expect one. I can draft a reply for you to post; I post nothing myself. From now on, `/kaizen:sync` (a command you type) does this look at the tracker. The repository is private, as you said; I'll record that too."
- **M9** (8 lines, no restart): "Done, on branch `kaizen-rollout` (commit ca0019c, not pushed): `CLAUDE.md`: your rules unchanged; a new section with the plugin's rules, the test line naming `python3 -m pytest` (**15**–**17** as you agreed). `design/kaizen.md` (new, committed): the ledger, with "Public: no", GitHub as the tracker, and a note on #3 and on the missing preview of the site. Waiting for you: **19**, the reply to #3, which you said you'd write yourself; and **4**, a local preview of the site before anything in `docs/` changes. Merge the branch when you're ready; the merge does not touch `docs/`. Next step: `/kaizen:playbook`, which picks up at the requirements interview (**6**)."

## Words the newcomer did not understand
- **(a) In the agent's messages:** "stand-in" in M2 was explained only by example; "release" in M2 ("a push there is a release"); "I lean to" in M7; "ledger" in M6 was glossed loosely.
- **(b) In the plugin's files:** frontier, lean, principal, owner, ER-C, ledger, inbox, decision record, safety row, upstream, two hats, retcon, ADR, OpenSpec, text id, `[record]`, hand-over, persona.
- **Concepts under two names:**
  - inbox / "Notes for the next debrief" / notes section (b)
  - block / standing instructions (both lists)
  - first rollout / "roll out" / "bring the plugin into" (b)

## What worked well
- The version line stayed silent.
- The playbook's step 1 caught the public site and the possible only copy of the data before anything ran.
- The update used a branch, named the overlaps with my own rules, kept them, and asked before every write.
- Waiting issues were surfaced without the agent posting anything.

## Setup misfit
`.tracker/issues.json` stands in for `gh`, so whether the agent would really run `gh` without asking cannot be observed. The newcomer's question to the agent also sits awkwardly beside the README's instruction to type `/kaizen:update` first.
