#!/usr/bin/env python3
"""Which version of the kaizen plugin, and of one skill's text, is on disk.

    version.py SKILL      one line: plugin version, commit when run from a checkout, the skill's text id
    version.py --stamp    write the current text id into every SKILL.md (for the maintainer)

Each SKILL.md carries "Text id `<id>`", a hash of its own text. A session keeps the skill text it loaded
until /reload-plugins or a new session; when the id in the text a session was given differs from the id
printed here, the session runs an older text of the skill.
"""

import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

if sys.version_info < (3, 10):
    sys.exit(f"{Path(sys.argv[0]).name} needs Python 3.10 or newer; this is {sys.version.split()[0]}")

PLUGIN = Path(__file__).resolve().parents[1]
STAMP = re.compile(r"Text id `[0-9a-f]*`")


def text_id(path: Path) -> str:
    """Hash of the skill file with its own stamp blanked, so that writing the stamp does not change it."""
    return hashlib.sha256(STAMP.sub("Text id ``", path.read_text()).encode()).hexdigest()[:8]


def commit() -> str:
    r = subprocess.run(["git", "-C", str(PLUGIN), "rev-parse", "--short", "HEAD"], capture_output=True, text=True)
    if r.returncode != 0:
        return ""
    dirty = subprocess.run(["git", "-C", str(PLUGIN), "status", "--porcelain", "--", "."], capture_output=True, text=True).stdout
    return f", commit {r.stdout.strip()}" + (" with uncommitted changes" if dirty.strip() else "")


def main():
    if len(sys.argv) != 2 or sys.argv[1] in ("-h", "--help"):
        print(__doc__)
        return
    skills = sorted(PLUGIN.glob("skills/*/SKILL.md"))
    if sys.argv[1] == "--stamp":
        for p in skills:
            t = p.read_text()
            if not STAMP.search(t):
                sys.exit(f"{p}: no 'Text id `...`' line to stamp")
            p.write_text(STAMP.sub(f"Text id `{text_id(p)}`", t, count=1))
        print(f"stamped {len(skills)} skills")
        return
    p = PLUGIN / "skills" / sys.argv[1].removeprefix("kaizen:") / "SKILL.md"
    if not p.is_file():
        sys.exit(f"no skill {sys.argv[1]}; skills: {', '.join(s.parent.name for s in skills)}")
    version = json.loads((PLUGIN / ".claude-plugin" / "plugin.json").read_text())["version"]
    print(f"kaizen {version}{commit()}; {p.parent.name} text id {text_id(p)}")


if __name__ == "__main__":
    main()
