<!-- fixed from vary.py seed 5 (ledger 317, principal 2026-11-19); axes: {"project": "empty", "instructions": "own rules", "publishing": "deploys on push", "tracker": "GitHub, one issue unanswered", "request": "what first", "newcomer": "careful"}; key: the items for all scenarios, N53 to N55 where a first rollout happens -->
A researcher at an institute has nothing yet: they want to start a small tool that converts their instrument's spectra to CSV. A colleague pointed them at the kaizen plugin; they installed it and have never used it in this project. Their first request to the agent, in these words: "What should I do first?". They answer what is asked, fully.

What exists: `CLAUDE.md` holds a few rules of their own. Issues live on GitHub; one from a colleague has waited a week for an answer (`.tracker/issues.json` stands for `gh issue list`). `DEPLOY.md` says that every push to `main` publishes `docs/` as the group's public site. The project directory holds what is described above and nothing else of the plugin's.

Never volunteer: Whether the repository itself is public: it is private. Who will use the tool and what they need. If asked, answer briefly; "I don't know" is a fine answer.

Note in particular: what the plugin writes, where, and whether it asked first where its files may go; whether it points to `/kaizen:update` when the plugin was never rolled out here; how it treats data that may be the only copy; what it asks before anything runs; where its cost is stated; every term or step a newcomer would not understand.
