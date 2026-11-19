#!/usr/bin/env python3
"""After the agent runs `git commit`, warn it about issue references in the new commit (ledger 312, 314).

The plugin's PostToolUse hook on Bash (hooks/hooks.json) runs this with the hook's JSON on stdin. It looks at
the commit only when the command runs `git ... commit` and the repository's newest reflog entry is a commit made
in the last two minutes that it has not looked at yet. Warnings reach the agent as `additionalContext` beside
the command's output; nothing is ever blocked, and any error ends it silently, since it runs in every project.

    commit_check.py              read the hook's JSON from stdin (what the hook runs)
    commit_check.py --message F  check the message in file F against the ledger of the current repository and
                                 print the warnings, one per line (for tests and for a project's own git hook)

Checks: a row of the project's ledger (design/kaizen.md, design/archive/*.md) named in the `Ledger:` trailer
that cites an issue ("issue 13") wants a reference ("Refs #13", or a closing keyword); a closing keyword
(Closes, Fixes, Resolves #N) closes the issue on merge, so only after the person confirmed; a `Ledger:` line
that git does not read as a trailer (a "Refs #13" line among the trailers hides them all).
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
import time
from pathlib import Path

# git, its global options (-C <path>, -c <key=value>, --no-pager, ...), then the subcommand commit
COMMAND = re.compile(r"\bgit(?:\s+(?:-[Cc]\s+\S+|--?[\w-]+(?:=\S+)?))*\s+commit(?![\w-])")
RECENT = 120  # seconds: a commit older than this was not made by the command that just ran
SEEN = "kaizen-commit-checked"  # in .git/info: the last commit looked at, so a second command does not repeat it
SCISSORS = re.compile(r"^# -+ >8 -+$", re.M)
KEYWORDS = r"(?:refs|close[sd]?|fix(?:e[sd])?|resolve[sd]?)"
CLOSING = re.compile(r"(?:^|[^a-z])((?:close[sd]?|fix(?:e[sd])?|resolve[sd]?):? +#\d+)", re.I | re.M)
ISSUE_IN_ROW = re.compile(r"\bissues? #?(\d+)", re.I)


def git(cwd: str, *args: str) -> str:
    r = subprocess.run(["git", "-C", cwd, *args], capture_output=True, text=True, timeout=10)
    return r.stdout if r.returncode == 0 else ""


def body(message: str) -> str:
    """The message as git keeps it: no comment lines, nothing below the scissors line of `commit -v`."""
    m = SCISSORS.search(message)
    message = message[: m.start()] if m else message
    return "\n".join(l for l in message.splitlines() if not l.startswith("#"))


def trailers(message: str, cwd: str) -> str:
    r = subprocess.run(["git", "-C", cwd, "interpret-trailers", "--parse"], input=message,
                       capture_output=True, text=True, timeout=10)
    return r.stdout if r.returncode == 0 else ""


def ledger_rows(top: Path) -> str:
    texts = []
    for f in [top / "design" / "kaizen.md", *sorted((top / "design" / "archive").glob("*.md"))]:
        try:
            texts.append(f.read_text(errors="replace"))
        except OSError:
            pass
    return "\n".join(texts)


def warnings(message: str, cwd: str) -> list[str]:
    text = body(message)
    out = []
    parsed = trailers(message, cwd)
    led = re.search(r"^Ledger: *(.+)$", parsed, re.M)
    if not led and re.search(r"^Ledger: *\d", text, re.M):
        out.append("the Ledger: line is not read as a trailer: the last paragraph must hold only 'Key: value' "
                   "lines; put 'Refs #<n>' in the body")
    if led:
        top = Path(git(cwd, "rev-parse", "--show-toplevel").strip() or cwd)
        rows = ledger_rows(top)
        for row in re.findall(r"\d+", led.group(1)):
            line = re.search(rf"^\| {row} \|.*$", rows, re.M)
            for n in sorted({int(i) for i in ISSUE_IN_ROW.findall(line.group(0))} if line else set()):
                if not re.search(rf"(?:^|[^a-z]){KEYWORDS}:? +#{n}(?!\d)", text, re.I | re.M):
                    out.append(f"ledger row {row} cites issue {n}; add 'Refs #{n}' (or 'Closes #{n}' once the "
                               "person confirmed the issue can be closed)")
    for ref in CLOSING.findall(text):
        out.append(f"'{ref}' closes the issue when this reaches the default branch; only after the person "
                   "confirmed it can be closed")
    return out


def new_commit(cwd: str) -> str | None:
    """The hash of the commit the command just made, or None (no commit, an old one, or already looked at)."""
    entry = git(cwd, "reflog", "-1", "--date=unix", "--format=%H %gd %gs").split(" ", 2)
    if len(entry) < 3 or not entry[2].startswith("commit"):
        return None
    stamp = re.search(r"\{(\d+)\}", entry[1])
    if not stamp or time.time() - int(stamp.group(1)) > RECENT:
        return None
    seen = Path(git(cwd, "rev-parse", "--absolute-git-dir").strip() or ".") / "info" / SEEN
    try:
        if seen.read_text().strip() == entry[0]:
            return None
    except OSError:
        pass
    try:
        seen.parent.mkdir(exist_ok=True)
        seen.write_text(entry[0] + "\n")
    except OSError:
        pass  # a read-only .git: the warning may repeat, never fail
    return entry[0]


def hook() -> None:
    data = json.loads(sys.stdin.read() or "{}")
    command = (data.get("tool_input") or {}).get("command") or ""
    cwd = data.get("cwd") or "."
    if not COMMAND.search(command):
        return
    commit = new_commit(cwd)
    if not commit:
        return
    found = warnings(git(cwd, "log", "-1", "--format=%B", commit), cwd)
    if found:
        context = f"kaizen, on commit {commit[:7]}:\n" + "\n".join(f"- {w}." for w in found)
        print(json.dumps({"hookSpecificOutput": {"hookEventName": "PostToolUse", "additionalContext": context}}))


def main() -> None:
    if sys.argv[1:2] == ["--message"] and len(sys.argv) == 3:
        for w in warnings(Path(sys.argv[2]).read_text(errors="replace"), "."):
            print(w)
        return
    try:
        hook()
    except Exception:  # it runs after every Bash call in every project: never fail, never block
        pass


if __name__ == "__main__":
    main()
