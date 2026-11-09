# Field test of the kaizen plugin in devvm: your brief

You try the kaizen plugin (version 0.6.0-dev.1) while you work on devvm as you normally would. The plugin is under test, not you and not devvm; whatever is unclear or awkward is a finding about the plugin. This brief is the same for the maintainer (variant 1) and for a colleague (variant 2).

## What to do

In your devvm session (Claude Code in the VM, in the devvm checkout), type `/kaizen:update`. From there on, work as you normally would.

## Notes while you work

Whenever something about the plugin strikes you (confusing, missing, good, annoying), note it. Be frank: the raw reaction is what helps, swearing and sighs included; nothing you write here is held against anyone. Also note what you do that the recording does not see, such as reading the README in a browser, asking a colleague, or looking something up elsewhere. Use whichever of these is at hand:

- **At a shell prompt** (not inside Claude): type the note as a comment, `# the update asked twice about the tracker`. The shell ignores it, and the recording keeps it with its time. In zsh, run `setopt interactivecomments` once first; bash needs nothing.
- **While Claude is running:** one line in the notes file named in your runbook, from a second terminal or your editor. It stays outside your Claude session.
- **Through the plugin itself:** everything it offers is yours to use, including "note for the debrief" and `/kaizen:debrief` in devvm; what lands in devvm's ledger and feedback files is read in the analysis, too.

Notes about devvm itself go wherever you see fit. Please follow your normal procedures there.

## Rules for this run

- Nothing goes upstream: no pushes, no comments, no issues, no pull requests. (In the run that is kept, this rule is lifted.)
- Stop when you want to; there is no target.

## When you are done

1. Wind the session down as you normally would.
2. Answer in the notes file: Did we do OK? Was anything in this brief, or in the plugin, uncomfortable or unclear?
3. Follow "Handing back" in your runbook.
