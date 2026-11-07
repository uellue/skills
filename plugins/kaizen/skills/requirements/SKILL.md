---
name: requirements
description: Interview the person who needs a solution and write a demand and requirements specification along a demand and requirements form written at ER-C. Use it at the start of a project or a larger change, whenever the user wants to specify, clarify or write down requirements, says "requirements", "Lastenheft", "Pflichtenheft", "demand specification", "what do we actually need", or asks to fill in the requirements form; to check an existing requirements document for what it skips; to reconstruct ("retcon") the requirements of something that grew from playing around, from its history, code and conversations; and on one topic whenever an open question or a vague idea needs fleshing out. Where OpenSpec is also installed, use this skill rather than /opsx:explore to clarify a need.
---

# Requirements interview

Text id `caf601c4`: first run `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/version.py requirements caf601c4` as it stands and pass on what it prints, if anything (it is silent when all is well; if it fails, carry on).

The questions that clarify a requirement between the person who needs a solution and the person who builds it are known; what goes wrong is that they are not asked, or are asked all at once, or are answered with a solution instead of a need. This skill asks them in short rounds, covers the sections of a demand and requirements form written at ER-C (a checklist; no institute requires it), writes down the answers in the person's words, and says plainly which items are answered, taken from the record, assumed, unknown or deferred. The questions are in `${CLAUDE_PLUGIN_ROOT}/references/requirements-questions.md`; read that file first.

Use plain words with the person: explain a term of this plugin the first time you use it with them, as `${CLAUDE_PLUGIN_ROOT}/references/words.md` does; keep a message to about fifteen lines, one step or question at a time; number a message's items from 1 in one sequence that never restarts within it, so the person can answer by number.

This skill tightens an idea that exists, however loosely (the playbook's test decides); from nothing to an idea, a discovery interview such as Matt Pocock's `grill-me` serves better, and its result is the record this interview starts from. Where the project keeps a `GLOSSARY.md`, write the requirements in its terms, and raise a term the interview finds missing or contradictory instead of defining it here.

## Who answers

- **The principal**, the person who needs the solution, answering in the chat: the normal case. Their answers are the record.
- **The record**, when the facts were gathered before the interview or the thing already exists: the conversation so far, the issue tracker and merge requests, the git history, the README, test reports, hallway-test records, earlier session transcripts. Read them first, draft every section the record answers and mark each such item `[record]` with its source, keep the principal's own words apart from what they merely accepted, and interview only for what the record does not answer or where sources disagree. A tool that grew out of "can you quickly solve this" gets its requirements reconstructed this way, with a source on every line and a question list instead of guesses; ask the questionnaire's questions for the sections the record is silent on, in particular current solutions (1.2), benefits (1.3), what happens when it fails and how a wrong result is noticed (2.5), performance (2.6) and lifetime (2.10): they are what the next day's bug or the next colleague's remark will be about.
- **A simulated stakeholder**, when the principal is not available: follow the playbook's "Working without a person" and mark every such item `[assumed]`, lower in confidence than anything a real person said. Hand the document to the real principal for correction before anyone builds on it.
- **An existing document**: read it against the questionnaire and report what it answers, what it skips, and where an answer is a solution in disguise; then interview only for the gaps.

## The interview

Before asking, check what is already known (the instruction files, design notes, the stakeholder record, an earlier walk-through or hallway test, the record above), draft the sections from it and ask the person to correct rather than repeat. Unless the playbook's step 7 settled it, ask in the first round which vocabulary the field already uses (the project's glossary, a community glossary or ontology), and write the record in its terms from the start rather than in words of your own.

Then work in rounds (after Matt Pocock's MIT-licensed `grilling` skill). Each round asks the **frontier**: every open question whose prerequisites are already settled, numbered, each with your lean, worded so that "yes" accepts it. Give no lean for safety limits, who may authorise what the software does, or who owns the instrument or system it acts on (2.11, Release): those answers must come from the person or the owner. A question that depends on another one still open waits for a later round. Facts are yours to find (look them up, or send a sub-agent without blocking the round); decisions are the person's. The form's sections are the checklist of what must be covered, not an order: the demand (1.1 to 1.4) usually settles first because the rest depends on it; otherwise follow what the answers unblock. Keep rounds short, about fifteen lines, the questions numbered in one sequence; the interview is done when the frontier is empty or the rest is deferred.

Habits that make the answers usable:

- **Need before solution.** When an answer names a solution ("we need a Zarr index"), ask why until the need appears ("people cannot find last year's measurements"), then write the need and note the proposed solution as one option (five whys; stop when the answer leaves the person's control).
- **Numbers are numbers.** For performance, users and benefits, ask for a figure, a range or an example; "fast" and "many" go into the uncertainties section until they have one. The same rule binds your own prose: a figure you write without a source is marked as your estimate, or left out.
- **"Unknown" and "later" are answers.** Record an unknown under demand uncertainties with what would resolve it (a measurement, a decision, a conversation with someone named). Record a deferral ("not now", "at a later stage", "up to you") under open questions with the stage it is deferred to and who owns it; deferring is a good way to keep the interview moving, and a deferral that lives only in chat is lost.
- **Examples, labelled.** When the person gives a case, ask whether it is the whole need or an example of a general one, and write the general one with the example attached.
- **Two hats.** After the demand sections, read the answers back with the product hat (what does "done" look like for this person, what would they complain about) and with the developer hat (what is infeasible, insecure, slow at the stated scale, fragile at the interfaces), and ask the questions those raise; this pass is where the real risk tends to surface ("the first jump is the risk, not the regular upgrade").
- **Play back and confirm.** At the end of each round, summarise the answers in a few sentences in the person's words and ask whether that is right, before the next round. Items taken from the record are read back too: `[record]` becomes `[answered]` only when the principal confirms it.
- **Prior art before "nothing exists".** For current solutions (1.2), search for upstream projects, libraries or services that address the problem before writing that none does; name what was found and what it lacks.
- **The stakeholders are a document.** Section 1.4 writes or updates the project's stakeholder record (`design/stakeholders.md`): one entry per persona with who they are, what they want, what they know, what they have, what they would never read, and whether the entry is from an interview, described by someone else (named), or simulated. The `walkthrough` and `hallway-test` skills take their personas from it; their desired experiences are requirements.
- **Walk the main scenarios.** For section 2.1, the `walkthrough` skill is the method: when the two skills are invoked together, the walks become the scenarios, and each walk's questionnaire footer lists the questions the record does not answer yet, for the next rounds.

Match the depth to the project: a two-week tool gets the demand sections and the use scenarios in full and one line each for the rest; an instrument-facing service gets every section. Never skip a section silently; a one-line "not asked, because <reason>" is a legitimate entry.

## Output

Write the document to `design/requirements.md` (or the project's existing requirements location), and keep it updated through the interview so nothing is lost if the session ends. Structure, with the form's numbering as a checklist:

```markdown
# Demand and requirements: <project title>

Author: <who wrote it>. Principal: <who needs it>. Date: <date>. Interviewed: <the principal in person | from the record (<sources>) | simulated as <persona> | from the document <name>>.
Markers per item: [answered] said or confirmed by the principal; [record] taken from <source>, not yet confirmed; [assumed] proposed by the author; [unknown] listed in 2.2 with what would resolve it; [deferred] listed under open questions with stage and owner.

## 1. Demand
### 1.1 Problem and context
### 1.2 Current solutions   (with the prior art found)
### 1.3 Benefits   (with figures where given)
### 1.4 Users   (who, how many, how often, skills; the stakeholder record)

## 2. Requirements
### 2.1 Use scenarios   (step by step, who does what; main and optional; frequent and rare; the walk-throughs; acceptance examples by ID from design/examples.md)
### 2.2 Demand uncertainties   (every "unknown", with what would resolve it)
### 2.3 Interfaces with existing systems
### 2.4 Operating conditions
### 2.5 Availability and reliability   (consequences of failure; how a wrong result is noticed)
### 2.6 Performance   (numbers)
### 2.7 Testing, installation and service   (who operates it afterwards)
### 2.8 Portability and distribution
### 2.9 Jurisdictions   (export, licences, data residency, personal data)
### 2.10 Lifetime and decommissioning
### 2.11 Safety and risks
### 2.12 Applicable standards

## Release
Decides: <...>. Builds: <...>. Pays: <...>. Signs off: <...>. Owns the instrument or shared system it acts on: <... | none>.

## Open questions
- <question>, for <person>, resolves <section>, deferred to <stage>
```

Mark each item, not only each section: a section marked "answered" with assumed lines inside misleads the next builder. If the person wants the form's Word version filled, produce it from this Markdown with the document tools available, section by section under the same numbers; the Markdown stays the working copy.

## Handover

Before saying the document is ready, run the handover check and show its result:

1. Every item still marked `[record]`, `[assumed]`, `[unknown]` or `[deferred]`, as one numbered list quoted in full in the message itself, grouped by section (a number or a file reference alone tells the person nothing), so the person can confirm or strike them in minutes even when they do not want to review the text; a `[record]` item that is never read back counts as confirmed downstream, which it is not.
2. Section headers whose marker is stale (a section says "pending" while its items are answered, or the reverse).
3. Every quote or figure taken from a sub-agent's report, checked against the source by you (a grep per quote is enough); say which you could not check.
4. The three lists the builder needs first: the unknowns, the interfaces outside our control, and the risks.
5. Whether the build may start, and on which assumptions; the questions that block it, with who answers. The decisions the build will need go into a decision record (the playbook's "what we decided" moment).
6. The questions for a person who was not in the interview (the instrument's owner, a facility manager, an administrator), as a short text ready to send, with Matt Pocock's `to-questionnaire` where installed; offer the text as soon as they arise, so the person can send it while the interview goes on; their answers come back as `[answered]` with the name.

## Rules

- Write the person's words, not yours; where you rephrase, read it back.
- Never fill a section the person did not answer; mark it `[record]`, `[assumed]` or `[unknown]`, and keep them apart.
- A requirement that cannot be checked is not finished: for each main scenario, add one acceptance example ("when <situation>, then <observable outcome>") to `design/examples.md`, with the next free ID, a priority and the scenario it comes from, and cite the ID in 2.1. The examples live only there.
- Keep names of people in the project's own record; keep them out of anything published.
- Hand the document over with the handover check above, not with "ready for review" alone.
- At the end, one line into the project's ledger: what in this skill did not fit. If the file is new, announce it first (playbook, Rules).
- Offer the debrief in one line (`/kaizen:debrief`) when the interview ends a stretch of work or was this skill's first use in the project.
