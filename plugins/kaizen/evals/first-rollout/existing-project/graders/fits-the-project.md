---
type: llm
focus: last_message
---

The project has never used the kaizen plugin. Its CLAUDE.md has its own rules ("Keep diffs small and focused; one concern per pull request", "Never touch files under /data", English commit messages), a test command (`python3 -m pytest`), and decision records in `docs/decisions/`. The skill works one step per message, so this first reply need not list the rules line by line yet.

PASS if the reply does all of these: treats this as a first setup of the plugin in the project (not as an update of an older version); names at least two things the project already has (its rules, its test command, its decision records in `docs/decisions/`) and says the plugin will use or keep them rather than replace or duplicate them; says the plugin's rules for the agent would go into the existing CLAUDE.md, not a new file; and asks before writing anything.
FAIL if it misses any of these, says the project is up to date or that there is nothing to do, proposes a second instruction file, or says it has already written to the project's files.
