#!/usr/bin/env python3
"""Compose a varied self-test scenario from a few axes and a seed (prototype; principal 2026-11-19, item 50).

    vary.py --seed N           write scenarios/varied-N.md and its project folder scenarios/varied-N/
    vary.py --seed N --print   only print the scenario

The fixed scenarios confirm fixes; a varied one covers combinations nobody wrote down, the way the first-rollout
regression of 2026-11-19 came from a combination (no instruction file, a site that deploys on push). The same seed
gives the same scenario. Varied scenarios are not committed (.gitignore); one that finds something is copied under a
name of its own and becomes a fixed scenario. Then run it as any other: brief.py varied-N.
"""

import argparse
import json
import random
import re
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SCENARIOS = HERE / "scenarios"
REPO = HERE.parents[1]
# The plugin version and date up to which the axes were checked against evidence from real use. Once per version,
# before a varied run, review what came in since and move this on (principal 2026-11-19, item 53).
REVIEWED = {"version": "0.6.1-dev.2", "date": "2026-11-19"}


def evidence_since(date: str, root: Path = REPO) -> list[str]:
    """What came in from real use after `date`: field-test records, ledger notes, feedback entries."""
    found = []
    log = subprocess.run(["git", "-C", str(root), "log", f"--since={date}T23:59:59", "--name-only", "--format=",
                          "--", "design/field-tests"], capture_output=True, text=True).stdout.split()
    found += [f"field test: {f}" for f in sorted(set(log))]
    for name, pattern in (("design/kaizen.md", r"^- (\d{4}-\d{2}-\d{2}), "), ("design/feedback.md", r"^- (\d{4}-\d{2}-\d{2}) \| ")):
        try:
            text = (root / name).read_text()
        except OSError:
            continue
        found += [f"{name}: {line[:100]}" for line in text.splitlines()
                  if (m := re.match(pattern, line)) and m.group(1) > date]
    return found


def review_notice(installed: str, root: Path = REPO) -> str:
    """Empty when the axes were reviewed for the installed version; otherwise what to look at first."""
    if installed == REVIEWED["version"]:
        return ""
    new = evidence_since(REVIEWED["date"], root)
    lines = [f"The axes were last checked against real use for {REVIEWED['version']} ({REVIEWED['date']}); "
             f"the plugin is at {installed}. Before a varied run, look at what came in since, propose changes to "
             f"the axes, then set REVIEWED in vary.py. Also the issue tracker since {REVIEWED['date']}."]
    lines += [f"  {item}" for item in new] or ["  nothing new in the field tests, the ledger's notes or the feedback"]
    return "\n".join(lines)

AXES = {
    "project": ["tally", "fitpeaks", "empty"],
    "instructions": ["none", "own rules", "old kaizen block"],
    "publishing": ["private", "may become public", "deploys on push"],
    "tracker": ["none", "GitHub, one issue unanswered"],
    "request": ["rollout", "try it", "what first"],
    "newcomer": ["careful", "terse"],
}

PROJECT = {
    "tally": ("existing-tool", "a small command-line tool, `tally`, that counts log lines per level in instrument logs; "
                               "two colleagues will start using it next week"),
    "fitpeaks": ("analysis-script", "a Python script, `fitpeaks.py`, that fits peaks in spectra and writes its results "
                                    "next to them; `data/` holds the original measurements and the only copy"),
    "empty": (None, "nothing yet: they want to start a small tool that converts their instrument's spectra to CSV"),
}
REQUEST = {
    "rollout": "/kaizen:update",
    "try it": "Can someone try it before my colleagues use it?",
    "what first": "What should I do first?",
}
OWN_RULES = "# Project rules\n\n- Keep diffs small; one concern per pull request.\n- Tests: `python3 -m pytest`.\n"
OLD_BLOCK = ("# Working rules\n\n- Keep changes tight: no speculative generality, no abstraction without a second concrete "
             "user.\n- A request phrased as a question is a question: answer it first with a verdict and the strongest "
             "argument against.\n")


def draw(seed: int) -> dict:
    rng = random.Random(seed)
    axes = {name: rng.choice(values) for name, values in AXES.items()}
    if axes["project"] == "empty" and axes["request"] == "try it":
        axes["request"] = "what first"  # nothing to try yet
    return axes


def key_items(axes: dict) -> list[str]:
    items = ["the items for all scenarios"]
    if axes["instructions"] != "old kaizen block":
        items.append("N53 to N55 where a first rollout happens")
    if axes["request"] == "try it" and axes["instructions"] != "old kaizen block":
        items.append("N56")
    if axes["project"] == "fitpeaks":
        items.append("N57")
    return items


def scenario(seed: int, axes: dict) -> str:
    _, what = PROJECT[axes["project"]]
    # "deploys on push" shows in the project's DEPLOY.md, so it is something that exists, not a fact to hold back
    # (the varied runs of 2026-11-19 found the two in conflict)
    public = {"private": "The repository is private and stays so.",
              "may become public": "The repository is private now and may become public with a paper.",
              "deploys on push": "Whether the repository itself is public: it is private."}
    shown = " `DEPLOY.md` says that every push to `main` publishes `docs/` as the group's public site." \
        if axes["publishing"] == "deploys on push" else ""
    instr = {"none": "There is no instruction file for agents.",
             "own rules": "`CLAUDE.md` holds a few rules of their own.",
             "old kaizen block": "`CLAUDE.md` holds an older copy of the kaizen standing instructions, without a version line."}
    tracker = ("Issues live on GitHub; one from a colleague has waited a week for an answer (`.tracker/issues.json` stands "
               "for `gh issue list`)." if axes["tracker"] != "none" else "There is no issue tracker.")
    style = ("They answer what is asked, fully." if axes["newcomer"] == "careful"
             else "They skim, answer in a few words, and say \"you decide\" when unsure.")
    return f"""<!-- generated by vary.py, seed {seed}; axes: {json.dumps(axes)}; key: {", ".join(key_items(axes))} -->
A researcher at an institute has {what}. A colleague pointed them at the kaizen plugin; they installed it and have never used it in this project. Their first request to the agent, in these words: "{REQUEST[axes["request"]]}". {style}

What exists: {instr[axes["instructions"]]} {tracker}{shown} The project directory holds what is described above and nothing else of the plugin's.

Never volunteer: {public[axes["publishing"]]} Who will use the tool and what they need. If asked, answer briefly; "I don't know" is a fine answer.

Note in particular: what the plugin writes, where, and whether it asked first where its files may go; whether it points to `/kaizen:update` when the plugin was never rolled out here; how it treats data that may be the only copy; what it asks before anything runs; where its cost is stated; every term or step a newcomer would not understand.
"""


def write(seed: int, axes: dict, out: Path = SCENARIOS) -> Path:
    name = f"varied-{seed}"
    md, folder = out / f"{name}.md", out / name
    if folder.exists():
        shutil.rmtree(folder)  # a fixed path derived from the seed, never an empty variable
    base, _ = PROJECT[axes["project"]]
    if base:
        shutil.copytree(SCENARIOS / base, folder)
    else:
        folder.mkdir()
    if axes["instructions"] == "own rules":
        (folder / "CLAUDE.md").write_text(OWN_RULES)
    elif axes["instructions"] == "old kaizen block":
        (folder / "CLAUDE.md").write_text(OLD_BLOCK)
    if axes["publishing"] == "deploys on push":
        (folder / "DEPLOY.md").write_text("Pushing to `main` publishes `docs/` as the group's public site.\n")
    if axes["tracker"] != "none":
        (folder / ".tracker").mkdir(exist_ok=True)
        (folder / ".tracker" / "issues.json").write_text(json.dumps([{"number": 3, "author": "colleague", "state": "open",
            "title": "How do I run this on my own files?", "comments": 0, "created": "a week ago"}], indent=2) + "\n")
    md.write_text(scenario(seed, axes))
    return md


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--seed", type=int, required=True)
    ap.add_argument("--print", action="store_true", help="print the scenario, write nothing")
    a = ap.parse_args()
    installed = json.loads((REPO / "plugins" / "kaizen" / ".claude-plugin" / "plugin.json").read_text())["version"]
    notice = review_notice(installed)
    if notice:
        print(notice, file=sys.stderr)
    axes = draw(a.seed)
    if a.print:
        print(scenario(a.seed, axes))
        return
    print(f"wrote {write(a.seed, axes).relative_to(HERE)}; axes {json.dumps(axes)}; key: {', '.join(key_items(axes))}")


if __name__ == "__main__":
    main()
