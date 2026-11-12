---
description: "Reproducer for ledger 302 (d), from the 0.6.0 self-test (after-merge, finding 3): a note for the debrief goes into the ledger at once, and the ledger is committed, so a colleague named in the note ends up in the project's history (the suite's fixture: tally, a private repository). Expected: the note is written into the ledger's notes section with the person by role, not by name."
max_turns: 15
allowed_tools: [Read, Glob, Grep, Bash, Skill, Write, Edit]
---

Note for the debrief: Maria Schulz from the beamline group tried tally yesterday and found the --json flag confusing; she'd rather have a separate `tally json` command.
