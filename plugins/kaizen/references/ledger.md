# Ledger template

The project's `design/kaizen.md`, shared by every kaizen skill: the debrief writes proposals and the status of earlier ones, every skill one friction line at the end of a run, anyone a "note for the debrief". The first skill that writes it starts it from this template, after saying where it goes and that it is meant to be committed. When a version is released, the debrief moves its closed rows under `## Closed, <version>` at the end, so that the next debrief reads the open ones first.

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
