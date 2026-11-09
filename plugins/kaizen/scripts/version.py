#!/usr/bin/env python3
"""Which version of the kaizen plugin, and of one skill's text, is on disk.

    version.py SKILL ID   what a skill runs at its start, with the text id it was given: prints nothing when
                          that text is current in an installed copy; one line when the session runs an older
                          text, and a short status line in the maintainer's checkout
    version.py SKILL      the full line: plugin version, commit in a checkout, the skill's text id
    version.py --stamp    write the current text id into every SKILL.md (maintainer's checkout only)
    version.py --project  which version the project's records belong to, against the installed plugin

With SKILL and ID it also looks at the project it runs in (the git top level of the working directory): when
the project's records belong to an older version of the plugin than the installed one, it prints one line
naming /kaizen:update, once per installed version (remembered in the clone's .git/info/, never committed).
The records: the standing instructions in CLAUDE.md or AGENTS.md (their first line names the version they
are from; a copy without that line is older than any versioned one), and a ledger missing a line the current
template has.

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


MARKER = re.compile(r"^Kaizen standing instructions, version (\S+?)[.:]?(?:\s|$)", re.M)
BLOCK_START = "- Keep changes tight: no speculative generality"  # the block's first rule, in every version so far
LEDGER_LINES = ("Public:", "Message size:")  # lines of references/ledger.md's header a current ledger carries
NOTICED = "kaizen-update-noticed"


def version_key(v: str) -> tuple:
    """0.6.0-dev.1 < 0.6.0 < 0.6.1: numbers first, a pre-release before its release."""
    main, _, pre = v.partition("-")
    nums = tuple(int(n) if n.isdigit() else 0 for n in main.split("."))
    parts = tuple((0, int(p), "") if p.isdigit() else (1, 0, p) for p in pre.split(".")) if pre else ()
    return nums, not pre, parts


def project_root() -> Path:
    r = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True)
    return Path(r.stdout.strip()) if r.returncode == 0 and r.stdout.strip() else Path.cwd()


def project_records(root: Path, installed: str) -> list[str]:
    """What in the project belongs to an older version of the plugin; empty when nothing does."""
    older = []
    for name in ("CLAUDE.md", "AGENTS.md", ".claude/CLAUDE.md"):
        f = root / name
        if not f.is_file():
            continue
        text = f.read_text(errors="replace")
        m = MARKER.search(text)
        if m and version_key(m.group(1)) < version_key(installed):
            older.append(f"{name}: standing instructions from {m.group(1)}")
        elif not m and BLOCK_START in text:
            older.append(f"{name}: standing instructions from before 0.6 (no version line)")
    ledger = root / "design" / "kaizen.md"
    if ledger.is_file():
        head = ledger.read_text(errors="replace")
        missing = [line for line in LEDGER_LINES if not re.search(rf"^{re.escape(line)}", head, re.M)]
        if missing:
            older.append(f"design/kaizen.md: no {' or '.join(missing)} line")
    return older


def notice(installed: str):
    """One line naming /kaizen:update when the project is behind, once per installed version and clone."""
    root = project_root()
    older = project_records(root, installed)
    if not older:
        return
    gitdir = subprocess.run(["git", "-C", str(root), "rev-parse", "--absolute-git-dir"], capture_output=True, text=True)
    seen = Path(gitdir.stdout.strip()) / "info" / NOTICED if gitdir.returncode == 0 else None
    if seen and seen.is_file() and seen.read_text().strip() == installed:
        return
    print(f"kaizen {installed} is installed; this project's records are older ({'; '.join(older)}): "
          f"/kaizen:update brings them up to date, on a branch, asking before each change. Said once for {installed}.")
    if seen:
        seen.parent.mkdir(exist_ok=True)
        seen.write_text(installed + "\n")


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
    version = json.loads((PLUGIN / ".claude-plugin" / "plugin.json").read_text())["version"]
    if sys.argv[1] == "--project":
        root = project_root()
        older = project_records(root, version)
        print(f"kaizen {version} installed; project {root}: " + ("; ".join(older) if older else "nothing older found"))
        return
    p = PLUGIN / "skills" / sys.argv[1].removeprefix("kaizen:") / "SKILL.md"
    if not p.is_file():
        sys.exit(f"no skill {sys.argv[1]}; skills: {', '.join(s.parent.name for s in skills)}")
    if len(sys.argv) == 3:
        verdict(p, sys.argv[2].strip("`"), version)
        if p.parent.name != "update":
            notice(version)
        return
    line = f"kaizen {version}{commit()}; {p.parent.name} text id {written_id(p)} (compare with the id at the top of the skill)"
    if written_id(p) != text_id(p):
        line += "; the file on disk was edited after its last --stamp, so the comparison cannot tell (run --stamp in the checkout)"
    print(line)


if __name__ == "__main__":
    main()
