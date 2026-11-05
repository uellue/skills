# Requirements questionnaire

Adapted for software from the "Demand and Requirements Specification" form (version 1.1, 2026) that Dieter Weber wrote at ER-C to clarify requirements between the person who needs a solution and the person who builds it. It is not an institute requirement; the plugin uses it as a checklist for work with agents. The original covers all kinds of projects, instruments included; the questions below keep its structure and translate the physical ones. Use it in two ways: before a walk-through, to see which questions the project's record already answers and which it skips; after a walk-through, to turn the steps into section 2.1 and to fill the rest from the conversation with the real stakeholder. A question that has no answer is a finding, not an omission to hide.

## 1. Demand

1.1 **Problem and context.** What is the starting situation and the larger context that leads to the demand? Which problems will this solve, for whom, and what happens if nothing is done?

1.2 **Current solutions.** How is the problem addressed today, and why is that inadequate? Which alternatives exist: in-house scripts, upstream projects, commercial services, a colleague doing it by hand? Name them, with what each lacks. (For software: this is the prior-art question; "nothing exists" is rarely true.)

1.3 **Benefits.** What does a better solution buy: time saved per week and for whom, cost saved, new results made possible, risks removed? Which ongoing or planned projects would use it?

1.4 **Users.** Who would use it inside and outside the institute? How many, how often, with what skills? Who is the target audience, and who is explicitly not?

## 2. Requirements

2.1 **Use scenarios.** Step by step, who does what: the main applications and the optional ones, the actions performed very often and the rare ones, each type of user separately. (This is the walk-through's output: the persona, the process, the steps.)

2.2 **Demand uncertainties.** What is uncertain now? Which future events could change the demand or the requirements: a new instrument, a new file format, a policy, a funding decision, a user base that grows?

2.3 **Interfaces with existing systems.** Which existing or planned systems does it talk to, in which direction, in which format, with which identity? Which of those are outside our control, and what do we know about their quirks?

2.4 **Operating conditions.** Where does it run: a container on a server, a lab PC next to an instrument, a laptop in the field, a cloud account, a CI runner? With which network, which mounts, which permissions, which user?

2.5 **Availability and reliability.** Is anything mission-critical depending on it? What happens if it is down for an hour, a day, a month, or wrong without anyone noticing? How would a wrong result be detected, and by whom?

2.6 **Performance.** The relevant quantities with numbers: data volume, file counts, rate of change, latency a user will tolerate, memory and disk, concurrent users. "Fast" is not a number.

2.7 **Testing, installation and service.** What is special about testing it (real data, real clients, a reference implementation)? What does installation depend on? Who operates it after the project, with what time, and what do they need to see to know it works?

2.8 **Portability and distribution.** (The form's "transport and storage".) Where else must it run, and how does it get there: pip, container image, a repository, a USB stick to an air-gapped instrument PC? How is it kept when not in use: archived with its data, kept installable, let go?

2.9 **Jurisdictions.** (The form's "countries".) Where is it made, run and used, and what follows: export restrictions, licences of dependencies, data residency, personal data and the rules that apply to it.

2.10 **Lifetime and decommissioning.** How long must it live? What happens to its data, its identifiers and its users when it is retired, and who decides?

2.11 **Safety and risks.** What can it damage: data loss or corruption, leaked credentials or personal data, a flood of records that drowns a search, an instrument PC it shares, a service it overloads? What could impair it? Which risks must be mitigated, and whom to consult (IT security, data protection, the instrument's owners)?

2.12 **Applicable standards.** Which standards, protocols, formats or regulations apply: OAI-PMH, Dublin Core, NeXus, FAIR principles, institute IT rules, a funder's data policy?

## Release

The original form ends with a release table: who is the principal (the person who needs it), the project manager, the coordinator, engineering, the cost centre. For a software project this is still the right question: who decides, who builds, who pays, and who signs off that the requirements are complete. Name people, not roles, in the project's own record; keep names out of anything published.
