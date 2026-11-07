# Feedback (template)

The committed file `design/feedback.md`, which the debrief starts and appends to. Its counterpart `.claude/debriefs/feedback-raw.md` holds the same remarks word for word with their source (session, moment); it is private and must be ignored by git before the first line goes in (the same check as for the report).

```markdown
# Feedback

What people said about working with the agents and the plugin, positive and negative, as the source of goals. One entry per line, so that `grep negative`, `grep <area>` or `grep "effect: none"` finds candidates for new work:

`- <date> | positive or negative | <area> | <what was said, cleaned> | effect: <what it became: a ledger row, a rule, a test; or none yet>`

Cleaned means: no session ids, no names of people, no private projects, nothing caustic or personal; paraphrased where the words would be, after offering the person the paraphrase. When a ledger row acts on an entry, its effect is updated in the same commit.

## Entries

```

Areas are the skill or the part of the work the remark is about (`hallway-test`, `messages`, `safety`, `collaboration`); keep them few and reuse them, so that a search finds all entries of one kind.
