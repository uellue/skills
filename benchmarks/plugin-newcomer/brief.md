# Brief for the plugin self-test

`brief.py <scenario>` fills the placeholders and prints the brief; keep the rest as it is.

```text
UNDER TEST: the kaizen plugin, a Claude Code plugin, as a newcomer meets it, starting from its README. NOT UNDER TEST: the scenario project described below; it is only the input the newcomer brings along, the way a build tool is tried on a sample project. When the scenario reaches one of the plugin's skills, including the plugin's own `hallway-test` skill, that is a step of the plugin to observe and report on, not your test: follow it only until it would start real work.

You play two roles at once, and keep them apart in your notes:
- THE NEWCOMER: the person in the scenario. They answer only what is asked: never volunteer anything listed under "never volunteer" in the scenario. Invent SHORT plausible answers to what the plugin asks and mark them [made up]. If nothing asks where you would have expected a question, note "not asked".
- THE NEWCOMER'S AGENT: the Claude Code agent that follows the plugin's instructions in the newcomer's project.

SCENARIO:
<SCENARIO>

Whenever following the plugin would descend into real domain work (writing actual code, a full requirements document, long walk-throughs, spawning agents, running a real hallway test), do NOT do it: write one line "that's what I would have done now: <what, concretely, which file it would produce, what it would cost if the plugin said>" and move on. Keep the whole run under about 40 tool calls.

STRICT READING RULES: start with <REPO>/README.md, read as a newcomer would. From there you may read ONLY what the README or a skill you have reached tells you to read: the skill files under <REPO>/plugins/kaizen/skills/<name>/SKILL.md (reading one is how you simulate the agent invoking `/kaizen:<name>`; ${CLAUDE_PLUGIN_ROOT} is <REPO>/plugins/kaizen), the files under plugins/kaizen/references/ that a skill names, the `--help` or output of scripts a skill tells you to run, and the scenario project's own files. Do NOT read anything else under <REPO> (no design/, tests/, benchmarks/, CLAUDE.md, CODING_STANDARDS.md, git history) and no transcript content (no `transcript.py render` or `export`). Do NOT install anything, do NOT run `claude plugin ...` commands (describe them instead), do NOT modify <REPO> or anything outside <SCRATCH>.

The newcomer's project is at <SCRATCH>/project/ (a git repository on `main`, with the scenario's files committed if it brings any; otherwise empty, with no commit yet). Anything the plugin would have the agent write goes there, short.

Method:
1. Before your first command, write <SCRATCH>/expectations.md: what you, as the newcomer, expect from the README (which command first, what the plugin will do for the project, where it will stop and ask). Your first command after writing it prints the time (`date -Is`); that time stands for the file's.
2. Follow the README, then each skill, step by step. At each step write: what the instruction said, what you did, what happened, whether it matched your expectation.
3. Note in particular what the scenario lists under "note in particular", every announcement the agent makes before it writes a file (where, and whether it will be committed), each skill's start-up version line (it should be silent unless something is wrong), where the newcomer must decide and whether it is clear what is asked, and anything confusing, contradictory, missing, or costly without warning. Spend at least half your attention on things nobody listed.
4. If the plugin's documents contradict each other so that you cannot proceed, ask your caller with SendMessage in one sentence; otherwise decide yourself and note it.

Final message (your caller writes the record from it; do not write report files in the repository), under ~900 words:
- What you read (list of files), and the expectations file's time versus your first command's time.
- The path: numbered steps, one line each, with the skill and the made-up answers; mark "not asked" where you expected a question.
- Findings about the plugin, ranked: each with the moment (file and the instruction's wording, or the command and its output), expected vs observed, classified as bug / gap / surprising but defensible / question, and a suggested fix.
- The agent's messages to the newcomer, quoted word for word (the questions and the summaries, not your notes about them).
- Words the newcomer did not understand, in two lists: (a) in the agent's quoted messages, every term a newcomer could not be expected to know that was not explained on first use; (b) in the plugin's files you read (README, skills, references), the same. Add any concept that went by two names, and say in which list. "None" is a valid answer for either.
- What worked well for a newcomer.
- One line: what in this test's setup did not fit.
```
