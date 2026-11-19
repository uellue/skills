---
description: "E51 (issue 13): an existing project with its own instruction file, rules and a folder of decision records, never used with the plugin; the person types /kaizen:update. Expected: a first rollout that names what the project has, offers the standing instructions as a section of the existing CLAUDE.md with the overlapping rule named, creates no second instruction file and writes nothing before the person agrees."
max_turns: 20
allowed_tools: [Read, Glob, Grep, Bash, Skill, Write, Edit]
---

/kaizen:update
