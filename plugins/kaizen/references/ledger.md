# Ledger template

The project's `design/kaizen.md`, shared by every kaizen skill: the debrief writes proposals and the status of earlier ones, every skill one friction line at the end of a run, anyone a "note for the debrief". The first skill that writes it starts it from this template, after saying where it goes and whether it will be committed, and asking once whether the repository is or may become public (the `Public:` line; then no details of other projects and no security findings): committed by default, but never into a tree whose committed files are published (the playbook's step 3 places it then). When a version is released, the debrief moves the closed rows, with their sections and decisions, into `design/archive/` (as `ledger-<period>.md`), and keeps the open ones here with their numbers; built decision records, old hallway records and walk-throughs go there too. The skills read only what is current; the archive stays for history, read when a recurrence needs its context.

The notes section also takes, before the topic changes, an offer the person neither took nor dropped ("the rest later"), and any idea or note dropped during work (a next step, a wish), about the project too: it is the inbox. Whichever skill is running writes such a note at once, other people by role, not by name, and says so in its reply; with no ledger yet, once its creation is agreed. A note stays there until `/kaizen:sync` or the debrief routes each note to its place and leaves only the link ("→ #18", "→ row 12", "dropped"). The `Message size:` line holds the person's last answer to the debrief's question whether the messages' length suited them.

```markdown
# Kaizen ledger

What leaves a debrief: proposals with decisions, the fate of earlier ones, what did not fit in the plugin's skills, and notes for the next debrief. The full reports are private, in `.claude/debriefs/`.

Public: <yes / no / may become>, asked <date>.
Message size: <comfortable / shorter / longer> ("<their words>"), asked <date>.

## Proposals
### <date>
| # | Proposal | Destination | Effort | Decision / status |

## Skill friction
- <date, skill>: <what did not fit, one line>

## Notes for the next debrief
- <date>: <the note, with the moment>
```
