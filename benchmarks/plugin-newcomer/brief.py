#!/usr/bin/env python3
"""Prepare one self-test run of the kaizen plugin: a scratch project and the filled brief.

    brief.py SCENARIO [--scratch DIR]   scenarios: the names of scenarios/*.md

Creates DIR (default: a new directory under the system's temp directory) with `project/`, a git
repository holding the scenario's files (scenarios/<name>/, if any), writes the filled brief to
DIR/brief.txt and prints it, with a header naming the commit under test. The subject under test is
always the plugin; the scenario is only the input the newcomer brings.
"""

import argparse
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]


def brief_text() -> str:
    t = (HERE / "brief.md").read_text()
    start = t.index("```text\n") + len("```text\n")
    return t[start : t.index("```", start)]


def main():
    scenarios = sorted(p.stem for p in (HERE / "scenarios").glob("*.md"))
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("scenario", choices=scenarios)
    ap.add_argument("--scratch", type=Path, help="directory for the run (created; must not exist or be empty)")
    a = ap.parse_args()
    scratch = a.scratch or Path(tempfile.mkdtemp(prefix=f"kaizen-selftest-{a.scenario}-"))
    scratch.mkdir(parents=True, exist_ok=True)
    if any(scratch.iterdir()):
        sys.exit(f"{scratch} is not empty")
    project = scratch / "project"
    fixture = HERE / "scenarios" / a.scenario
    if fixture.is_dir():
        shutil.copytree(fixture, project, ignore=shutil.ignore_patterns("__pycache__"))
    else:
        project.mkdir()
    subprocess.run(["git", "init", "-q", str(project)], check=True)
    commit = subprocess.run(["git", "-C", str(REPO), "rev-parse", "--short", "HEAD"], capture_output=True, text=True).stdout.strip()
    dirty = subprocess.run(["git", "-C", str(REPO), "status", "--porcelain", "--", "plugins", "README.md"], capture_output=True, text=True).stdout.strip()
    text = (
        brief_text()
        .replace("<SCENARIO>", (HERE / "scenarios" / f"{a.scenario}.md").read_text().strip())
        .replace("<REPO>", str(REPO))
        .replace("<SCRATCH>", str(scratch))
    )
    (scratch / "brief.txt").write_text(text)
    print(f"# self-test of the kaizen plugin: scenario {a.scenario}, commit {commit or '?'}"
          + (" with uncommitted changes to the plugin or README" if dirty else "") + f", scratch {scratch}\n")
    print(text)


if __name__ == "__main__":
    main()
