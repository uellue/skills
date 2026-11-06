# Ledger template

The project's `design/kaizen.md`, shared by every kaizen skill: the debrief writes proposals and the status of earlier ones, every skill one friction line at the end of a run, anyone a "note for the debrief". The first skill that writes it starts it from this template, after saying where it goes and whether it will be committed: committed by default, but never into a tree whose committed files are published (the playbook's step 3 places it then). When a version is released, the debrief moves the closed rows, with their sections and decisions, into `design/archive/` (as `ledger-<period>.md`), and keeps the open ones here with their numbers; built decision records, old hallway records and walk-throughs go there too. The skills read only what is current; the archive stays for history, read when a recurrence needs its context.

```markdown
# Kaizen ledger

What leaves a debrief: proposals with decisions, the fate of earlier ones, what did not fit in the plugin's skills, and notes for the next debrief. The full reports are private, in `.claude/debriefs/`.

## Proposals
### <date>
| # | Proposal | Destination | Effort | Decision / status |

## Skill friction
- <date, skill>: <what did not fit, one line>

## Notes for the next debrief
- <date>: <the note, with the moment>
```
