# skills

A place to keep and share my AI agent skills, as a Claude Code plugin marketplace.

## Install

```bash
claude plugin marketplace add uellue/skills
claude plugin install kaizen@uellue --scope user
```

Or inside a session: `/plugin marketplace add uellue/skills`, then `/plugin install kaizen@uellue`.
To follow updates, turn on auto-update for the `uellue` marketplace under `/plugin` → Marketplaces.

## Plugins

- **kaizen**: continuous improvement of how we work with agents (Toyota's word for improving the processes themselves). Three skills:
  - `/kaizen:debrief`: debrief a Claude Code session or a stretch of work on how the collaboration went, not on what it produced. Cited moments, coaching for the person writing the prompts, proposals with a destination, a usage check from the session transcript, and a history of earlier debriefs so recurring issues are visible. Structure adapted, with thanks, from the MIT-licensed `debrief` skill by Wavez and the `retrospective` plugin by florianbuetow.
  - `/kaizen:walkthrough`: put on the shoes of a stakeholder and walk through a process step by step, to find the questions, gaps and acceptance examples nobody wrote down. The two-hat interview and the "simulated stakeholders are lower confidence" rule are borrowed from Feature Forge (jeffallan) and melodic-software's requirements-elicitation skills.
  - `/kaizen:hallway-test`: a fresh sub-agent that sees only the requirements and the user documentation builds test cases, writes expectations before running, asks questions and reports bugs, surprises and gaps; by eye too, through a bundled xterm screenshot driver (needs xvfb, xterm, xdotool, imagemagick). The CLI usability checklist is adapted from the MIT-licensed cli-ux-tester skill by Alister Lewis-Bowen.

## Licence

MIT, see `LICENSE`.
