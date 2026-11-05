# Stakeholders of the kaizen plugin

One entry per persona. The `requirements` skill writes this record (section 1.4), the `walkthrough` and `hallway-test` skills take their personas from it. Confidence per entry: interviewed (a real person said it) or simulated (the author's guess, to be corrected).

## The manager

Who: a research software engineer or scientist at ER-C who leads one or more coding agents on a project, writes the prompts, decides, reviews. The plugin's principal (Dieter Weber, interviewed 2026-11-03 to 11-05).
Wants: to be effective with agents; to specify outcomes rather than solutions; to judge behaviour instead of reading generated text; a record of decisions that survives sessions; to improve their own prompting from evidence.
Knows: the project, the demand and requirements form they wrote, product-management habits; the agent's tooling well enough to read transcripts.
Has: Claude Code in a VM, a devcontainer or on the host; several checkouts and worktrees; the repositories' design records.
Never reads: long generated text when a behaviour can be tried instead; a report that narrates instead of reminding.
Confidence: interviewed.

## The colleague starting with agents

Who: an ER-C research software engineer or scientist who begins to use Claude Code or Codex on a project, often with a colleague's guide as the only introduction.
Wants: to know what to write down and where (instruction file, decision log, backlog), how to lead an agent, what not to delegate, what it costs.
Knows: their science and their code; not the agent's conventions, memory locations or plugin mechanics.
Has: a fresh checkout; possibly a different tool (Codex reads `AGENTS.md`, not skills).
Never reads: the plugin's source; a ledger of someone else's project; a README beyond the headings and the commands to copy. Works by skimming for a command that looks right, running it, and then following the program's output; is annoyed when the chain of hints breaks and the README has to be read after all (a colleague's account of trying devvm, 2026-11-05).
Confidence: simulated, from the guide's "Goal 2" and remarks relayed by the manager (a colleague found that the walk-through assumed personas without asking; another described the skim-and-follow-the-hints way of working, 2026-11-05).

## The coding agent

Who: the Claude Code session that runs a skill of this plugin on a project.
Wants: instructions it can follow without the author's context: where the inputs are, what blocks, what the output template is, what "done" is; names of files that exist.
Knows: only the repository, its instruction files, the memory of its own checkout path, and the skill text.
Has: the tools of the session; sub-agents; sometimes no memory and no instruction file (worktrees, VMs).
Never reads: a rule stated once in a long paragraph when a step would do.
Confidence: interviewed through seven transcripts (debrief 2026-11-05).

## The fresh tester or reader agent

Who: a sub-agent spawned by a skill: the hallway tester, the by-eye tester, the diagnosis agent, the session reader.
Wants: a brief that is the whole context; permission to ask; a report channel that the harness does not forbid.
Knows: nothing but the brief and what it is allowed to read.
Has: a scratch directory, possibly a terminal driver, SendMessage.
Never reads: what it is forbidden (and says so when the harness attaches something anyway).
Confidence: interviewed through the sub-agent transcripts of the first week.

## The plugin maintainer

Who: whoever changes the skills (today the manager; later anyone in the marketplace's repository).
Wants: to know what did not fit in a skill's use, with the moment; proposals that are issues or merge requests; a way to test a skill before shipping it.
Knows: the skill texts and the scripts.
Has: this repository, its design record, the debriefs.
Never reads: a debrief's coaching section (private to the person debriefed).
Confidence: interviewed (the manager, 2026-11-05).

## The recipient of agent output outside the project

Who: an upstream maintainer, a colleague reading an issue or a merge request, another team's agent.
Wants: a short part for people (what is wrong or decided, what to do, one example) and, separately, the details an agent can use (versions, commits, commands, what was verified), with a visible mark of whether a human endorsed the details or merely attached them.
Knows: their own project, not ours.
Has: increasingly, their own agent reading our output.
Never reads: bulk generated text posted as if a person wrote it.
Confidence: simulated, from the manager's "two audiences" notes (2026-11-04 and 11-05).
