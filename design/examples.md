# Acceptance examples

One line each: ID, situation and observable outcome, priority, source. Requirements, walk-throughs, decision records, tests and tester briefs cite the IDs; nobody keeps a copy.

- **E1** (must; requirements S3): when a walk-through is invoked and the stakeholder record has no matching persona, then the skill shows the known personas and asks, offering to add one, before walking.
- **E2** (must; requirements 2.5): when `usage.py` runs on a session, then its output tokens equal the sum over distinct API message ids.
- **E3** (must; requirements S4): when a hallway test ends, then its record exists under `design/hallway/` and names, per defect, what would have caught it.
- **E4** (must; requirements S5, 2.9): when a transcript is exported into a directory git would track, then the export is refused and nothing is written.
- **E5** (must; requirements S5): when a session contains messages the person typed while a turn ran, then the rendering shows them as `USER (queued mid-turn)` and the usage counts them, and harness text is never labelled or counted as the person's.
- **E6** (should; requirements S1): when the requirements interview starts on a topic with an existing record, then its first round is drafted from the record and asks only the frontier questions the record does not settle.
