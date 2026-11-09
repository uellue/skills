# Field test of the kaizen plugin in devvm: your brief

You try the kaizen plugin (version 0.6.0-dev.1) while you work on devvm as you normally would. The plugin is under test, not you and not devvm; whatever is unclear or awkward is a finding about the plugin. This brief is the same for the maintainer (variant 1) and for a colleague (variant 2).

## What to do

In your devvm session (Claude Code in the VM, in the devvm checkout):

1. Start with any kaizen skill, or simply with `/kaizen:update`; the plugin should tell you that devvm is behind and what to run. Follow it.
2. Then type `/kaizen:sync`, and follow it.
3. Then work on the open issues from devvm's tracker, as far as you like, with the plugin guiding you.

You decide everything the plugin asks; answer as yourself. Do not look up how the plugin works; if you would have to, that is a finding.

## Notes while you work

Whenever something about the plugin strikes you (confusing, missing, good, annoying), add one line to the notes file named in your runbook, outside devvm, with the time. Notes about devvm itself go wherever the plugin tells you, as usual.

## Rules for this run

- Nothing goes upstream: no pushes, no comments, no issues, no pull requests. Let the plugin draft them; say "not now" when it offers to post. (In the run that is kept, this rule is lifted.)
- Stop when you want to; there is no target.

## When you are done

1. Tell the plugin you are done, and let it hand over as it would.
2. Answer in the notes file: Did we do OK? Was anything in this brief, or in the plugin, uncomfortable or unclear?
3. Follow "Handing back" in your runbook.
