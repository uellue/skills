---
description: "E51 (issue 13): an existing project with its own instruction file, rules and a folder of decision records, never used with the plugin; the person types /kaizen:update. Expected: a first rollout that names what the project has, proposes the standing instructions as a section of the existing CLAUDE.md, creates no second instruction file and writes nothing before the person agrees. The overlapping rules come in the next message, which a single-turn eval does not reach."
max_turns: 20
allowed_tools: [Read, Glob, Grep, Bash, Skill, Write, Edit]
---

/kaizen:update
