---
name: requirements
description: Interview the person who needs a solution and write a demand and requirements specification in the structure of ER-C's form (demand, users, use scenarios, uncertainties, interfaces, operating conditions, reliability, performance, installation, portability, jurisdictions, lifetime, risks, standards). Use it at the start of a project or a larger change, whenever the user wants to specify, clarify or write down requirements, says "requirements", "Lastenheft", "Pflichtenheft", "demand specification", "what do we actually need", or asks to fill in the requirements form; also to check an existing requirements document for what it skips.
---

# Requirements interview

The questions that clarify a requirement between the person who needs a solution and the person who builds it are known; what goes wrong is that they are not asked, or are asked all at once, or are answered with a solution instead of a need. This skill asks them one section at a time, in the order of ER-C's demand and requirements form, writes down the answers in the person's words, and says plainly which sections are answered, assumed, or unknown. The questions are in `${CLAUDE_PLUGIN_ROOT}/references/requirements-questions.md`; read that file first.

## Who answers

- **The principal**, the person who needs the solution, answering in the chat: the normal case. Their answers are the record.
- **A simulated stakeholder**, when the principal is not available: say so, answer as a named persona would, and mark every such section as assumed, lower in confidence than anything a real person said (a rule borrowed from melodic-software's requirements-elicitation skills). Hand the document to the real principal for correction before anyone builds on it.
- **An existing document**: read it against the questionnaire and report what it answers, what it skips, and where an answer is a solution in disguise; then interview only for the gaps.

## The interview

Work through the form's sections in order, one section per round, and keep each round short: two to four questions, the ones the conversation and the repository have not already answered. Before asking, check what is already known (the instruction files, design notes, an earlier walk-through or play test) and say what you took from there, so the person corrects rather than repeats.

Habits that make the answers usable:

- **Need before solution.** When an answer names a solution ("we need a Zarr index"), ask why until the need appears ("people cannot find last year's measurements"), then write the need and note the proposed solution as one option (five whys; stop when the answer leaves the person's control).
- **Numbers are numbers.** For performance, users and benefits, ask for a figure, a range or an example; "fast" and "many" go into the uncertainties section until they have one.
- **"Unknown" is an answer.** Record it under demand uncertainties with what would resolve it (a measurement, a decision, a conversation with someone named), and move on.
- **Examples, labelled.** When the person gives a case, ask whether it is the whole need or an example of a general one, and write the general one with the example attached.
- **Two hats.** After the demand sections, read the answers back with the product hat (what does "done" look like for this person, what would they complain about) and with the developer hat (what is infeasible, insecure, slow at the stated scale, fragile at the interfaces), and ask the questions those raise.
- **Play back and confirm.** At the end of each section, summarise the answers in two or three sentences in the person's words and ask whether that is right, before the next section.
- **Prior art before "nothing exists".** For current solutions (1.2), search for upstream projects, libraries or services that address the problem before writing that none does; name what was found and what it lacks.

Match the depth to the project: a two-week tool gets the demand sections and the use scenarios in full and one line each for the rest; an instrument-facing service gets every section.

## Output

Write the document to the project's requirements location if it has one (for example `design/requirements.md` or `docs/requirements/<project>.md`), otherwise `docs/requirements/<project>.md`, and keep it updated through the interview so nothing is lost if the session ends. Structure, with the form's numbering so that it transfers to the institute's Word template:

```markdown
# Demand and requirements: <project title>

Author: <who wrote it>. Principal: <who needs it>. Date: <date>. Interviewed: <the principal in person | simulated as <persona> | from the document <name>>.
Confidence per section: answered by the principal, assumed, or unknown; see the markers.

## 1. Demand
### 1.1 Problem and context   [answered | assumed | unknown]
### 1.2 Current solutions   (with the prior art found)
### 1.3 Benefits   (with figures where given)
### 1.4 Users   (who, how many, how often, skills)

## 2. Requirements
### 2.1 Use scenarios   (step by step, who does what; main and optional; frequent and rare)
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
Decides: <...>. Builds: <...>. Pays: <...>. Signs off: <...>.

## Open questions
- <question>, for <person>, resolves <section>
```

If the person wants the institute's Word form filled, produce it from this Markdown with the document tools available, section by section under the same numbers; the Markdown stays the working copy.

## Rules

- Write the person's words, not yours; where you rephrase, read it back.
- Never fill a section the person did not answer; mark it unknown or assumed, and keep the two apart.
- A requirement that cannot be checked is not finished: for each main scenario, add one acceptance example ("when <situation>, then <observable outcome>") that a test or a play test could use.
- Keep names of people in the project's own record; keep them out of anything published.
- Hand the document over with the three lists the builder needs first: the unknowns, the interfaces outside our control, and the risks.
