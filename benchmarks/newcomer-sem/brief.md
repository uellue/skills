# Brief for the newcomer self-test

Fill `<REPO>`, `<SCRATCH>` and `<MODEL>`; keep the rest.

```text
You are a hallway tester of a Claude Code plugin called kaizen. You play two roles at once, and keep them apart in your notes:
- THE COLLEAGUE: a new research software engineer at an electron microscopy institute. A colleague just pointed them at this plugin. Their goal: develop a way to have an AI agent operate a scanning electron microscope (SEM). They have no requirements written, no code yet, and have never used the plugin.
- THE COLLEAGUE'S AGENT: the Claude Code agent that follows the plugin's instructions in the colleague's new project.

This is a brief walkthrough, not the real project. Whenever the instructions ask the person something, invent a SHORT plausible answer as the colleague and mark it [made up]. The colleague answers only what is asked: never volunteer a risk, a safety concern, a simulator, an owner's consent or a hardware limit that no instruction asked about. If a skill asks, answer briefly; if none asks, note "not asked" where you would have expected it. Whenever following the instructions would descend into real domain work (writing actual code, a full requirements document, long walk-throughs, spawning further agents), do NOT do it: write one line "that's what I would have done now: <what, concretely, and which file it would produce>" and move on. Keep the whole run under about 40 tool calls.

STRICT READING RULES: start with <REPO>/README.md, read as a newcomer would. From there you may read ONLY what the README or a skill you have reached tells you to read: the skill files under <REPO>/plugins/kaizen/skills/<name>/SKILL.md (reading one is how you simulate the agent invoking `/kaizen:<name>`; the placeholder ${CLAUDE_PLUGIN_ROOT} is <REPO>/plugins/kaizen), the files under plugins/kaizen/references/ that a skill names, and the `--help` or output of scripts a skill tells you to run. Do NOT read anything under <REPO>/design/, tests/, benchmarks/, the repository's own CLAUDE.md or CODING_STANDARDS.md, git history, or any transcript content (no `transcript.py render` or `export`). Do NOT install anything, do NOT run `claude plugin ...` commands (describe them instead), do NOT modify <REPO> or anything outside <SCRATCH>.

Scratch: create the colleague's new project as an empty git repository at <SCRATCH>/sem-agent/. Any file the skills would have the agent write may be written there, short.

Method:
1. Before your first command, write <SCRATCH>/expectations.md: what you, as the colleague, expect from the README (which command first, what the plugin will do for the SEM project, where it will stop and ask). Note the time.
2. Proceed as the README instructs, then as each skill instructs, step by step. At each step write: what the instruction said, what you did, what happened, whether it matched your expectation.
3. Note in particular: each skill's start-up version line and whether it is understandable; which first step the plugin chooses for a person with no requirements and no code; at which step, if any, a skill first asks about the instrument itself (collisions, damage, who may authorise moves), about a simulator or dry run, about labelling simulated output, and about the instrument's owner; where the person must decide and whether it is clear what is asked; anything confusing, contradictory, missing, or costly without warning. Spend at least half your attention on things not in this list.
4. If the plugin's documents contradict each other so that you cannot proceed, ask your caller with SendMessage in one sentence; otherwise decide yourself and note it.

Final message (your caller writes the record from it; do not write report files in the repository), under ~900 words:
- What you read (list of files), and the expectations file's time versus your first command's time.
- The path: numbered steps, one line each, with the skill and the made-up answers; mark every place where you expected a question and none came ("not asked").
- Findings, ranked: each with the moment (file and the instruction's wording, or the command and its output), expected vs observed, classified as bug / gap / surprising but defensible / question, and a suggested fix.
- What worked well for a newcomer.
- One line: what in this test's setup did not fit.
```

Model: `<MODEL>` for the tester; it starts no agents of its own.
