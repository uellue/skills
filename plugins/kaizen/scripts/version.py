#!/usr/bin/env python3
"""Which version of the kaizen plugin, and of one skill's text, is on disk.

    version.py SKILL ID   what a skill runs at its start, with the text id it was given: prints nothing when
                          that text is current in an installed copy; one line when the session runs an older
                          text, and a short status line in the maintainer's checkout
    version.py SKILL      the full line: plugin version, commit in a checkout, the skill's text id
    version.py --stamp    write the current text id into every SKILL.md (maintainer's checkout only)

Each SKILL.md carries one line "Text id `<id>`" at the top of its body, a hash of its own text. A session
keeps the skill text it loaded until /reload-plugins or a new session; when the id in the text a session
was given differs from the id printed here, the session runs an older text. When a skill on disk was
edited after its last --stamp, the line says so instead of offering a misleading id.
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
STAMP = re.compile(r"^Text id `([^`\n]*)`", re.M)  # only at the start of a line; quotes elsewhere do not count
CMD = re.compile(r"(scripts/version\.py [a-z-]+ )([0-9a-f]{8}|<this text id>)`")  # the start-up command carries the id too


def text_id(path: Path) -> str:
    """Hash of the skill file with its stamp blanked, so that writing the stamp does not change it."""
    blanked = CMD.sub(r"\1`", STAMP.sub("Text id ``", path.read_text()))
    return hashlib.sha256(blanked.encode()).hexdigest()[:8]


def written_id(path: Path) -> str | None:
    """The id written in the file, if it has exactly one well-formed stamp line."""
    found = STAMP.findall(path.read_text())
    return found[0] if len(found) == 1 and re.fullmatch(r"[0-9a-f]{8}|", found[0]) else None


def git(*args) -> subprocess.CompletedProcess:
    return subprocess.run(["git", "-C", str(PLUGIN), *args], capture_output=True, text=True)


def tracked() -> bool:
    """True when a git checkout tracks this plugin's files (not merely an enclosing repository)."""
    return git("ls-files", "--error-unmatch", ".claude-plugin/plugin.json").returncode == 0


def commit() -> str:
    r = git("rev-parse", "--short", "HEAD")
    if not tracked() or r.returncode != 0:
        return ""
    dirty = git("status", "--porcelain", "--", ".").stdout
    return f", commit {r.stdout.strip()}" + (" with uncommitted changes" if dirty.strip() else "")


def stamp(skills: list[Path]):
    if not tracked():
        sys.exit(f"{PLUGIN} is not tracked by a git checkout: --stamp is for the maintainer's checkout, never an installed copy")
    bad = [p for p in skills if written_id(p) is None]
    if bad:
        sys.exit("need exactly one line starting with 'Text id `<8 hex digits or empty>`' in: " + ", ".join(map(str, bad)))
    for p in skills:
        i, t = text_id(p), p.read_text()
        p.write_text(CMD.sub(lambda m: f"{m.group(1)}{i}`", STAMP.sub(f"Text id `{i}`", t, count=1)))
    print(f"stamped {len(skills)} skills")


def verdict(p: Path, loaded: str, version: str):
    """Silent unless it matters: an older text in the session, or the maintainer's checkout."""
    name, on_disk = p.parent.name, written_id(p)
    if loaded != on_disk:
        print(f"kaizen: this session runs an older text of {name} (loaded {loaded}, on disk {on_disk}): run /reload-plugins")
    elif tracked():
        edited = "; edited after its last --stamp: run version.py --stamp" if on_disk != text_id(p) else ""
        print(f"kaizen {version}{commit()}: {name} current{edited}")


def main():
    if len(sys.argv) == 2 and sys.argv[1] in ("-h", "--help"):
        print(__doc__)
        return
    if len(sys.argv) not in (2, 3):
        sys.exit("usage: version.py SKILL [ID] | --stamp | --help")
    skills = sorted(PLUGIN.glob("skills/*/SKILL.md"))
    if sys.argv[1] == "--stamp":
        return stamp(skills)
    p = PLUGIN / "skills" / sys.argv[1].removeprefix("kaizen:") / "SKILL.md"
    if not p.is_file():
        sys.exit(f"no skill {sys.argv[1]}; skills: {', '.join(s.parent.name for s in skills)}")
    version = json.loads((PLUGIN / ".claude-plugin" / "plugin.json").read_text())["version"]
    if len(sys.argv) == 3:
        return verdict(p, sys.argv[2].strip("`"), version)
    line = f"kaizen {version}{commit()}; {p.parent.name} text id {written_id(p)} (compare with the id at the top of the skill)"
    if written_id(p) != text_id(p):
        line += "; the file on disk was edited after its last --stamp, so the comparison cannot tell (run --stamp in the checkout)"
    print(line)


if __name__ == "__main__":
    main()
