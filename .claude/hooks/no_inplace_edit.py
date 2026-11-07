#!/usr/bin/env python3
"""PreToolUse hook on Bash: block commands that edit a file git tracks in place (ledger 227).

The standing instructions say to edit files with the Edit tool; as a sentence the rule broke in three
sessions. Edits through Bash show no diff to the person and are not restored by rewind
(code.claude.com/docs/en/checkpointing, "Bash command changes not tracked", checked 2026-11-07).

Blocked: `sed -i`, `perl -i`, inline Python that writes (`python3 -c`, `python3 - <<EOF`), and a shell
redirect or `tee` into the file, each only when one of its targets is a tracked file of this
repository. Files outside the repository, untracked files and the project's own scripts (which
rewrite files by design, such as `rehash.py --apply`) pass. Exit 2 blocks the call and shows stderr to
the agent (code.claude.com/docs/en/hooks, "PreToolUse", checked 2026-11-07). Any error lets the call
through: a broken guardrail must not stop all work.
"""

import json
import os
import re
import subprocess
import sys

EDIT_FORMS = [
    re.compile(r"\bsed\b[^|;&\n]*\s(?:-[a-zA-Z]*i|--in-place)"),
    re.compile(r"\bperl\b[^|;&\n]*\s-[a-zA-Z]*i"),
    re.compile(r"\bpython3?\b[\s\S]*(?:write_text\(|write_bytes\(|open\([^)]*['\"][wa]b?\+?['\"])"),
]
REDIRECT = re.compile(r"(?<![0-9&])>{1,2}\s*(?!&)([^\s;&|<>()]+)|\btee\s+(?:-a\s+)?([^\s;&|<>()]+)")


def tracked(root):
    out = subprocess.run(["git", "-C", root, "ls-files", "-z"], capture_output=True, text=True, check=True).stdout
    return {os.path.normpath(os.path.join(root, p)) for p in out.split("\0") if p}


def candidates(command):
    # Every path-like run of characters, inside quotes and code too; only those naming a tracked file count.
    return set(re.findall(r"[\w.~/+-]+", command))


HEREDOC = re.compile(r"<<-?\s*(['\"]?)(\w+)\1")
INTERPRETER = re.compile(r"(?:^|[;&|(]\s*|\s)(?:python3?|perl|bash|sh)\b")


def without_text_heredocs(command):
    """Drop the bodies of heredocs that feed something other than an interpreter (a commit message, cat to a log)."""
    lines, out, i = command.split("\n"), [], 0
    while i < len(lines):
        line = lines[i]
        out.append(line)
        i += 1
        for m in HEREDOC.finditer(line):
            keep = INTERPRETER.search(line[:m.start()]) is not None
            while i < len(lines) and lines[i].strip() != m.group(2):
                if keep:
                    out.append(lines[i])
                i += 1
            if i < len(lines):
                out.append(lines[i])
                i += 1
    return "\n".join(out)


def hits(command, cwd, files):
    command = without_text_heredocs(command)

    def resolve(p):
        return os.path.normpath(p if os.path.isabs(p) else os.path.join(cwd, p))

    found = set()
    for m in REDIRECT.finditer(command):
        p = resolve(m.group(1) or m.group(2))
        if p in files:
            found.add(p)
    if any(f.search(command) for f in EDIT_FORMS):
        found |= {resolve(w) for w in candidates(command) if resolve(w) in files}
    return sorted(found)


def main():
    try:
        data = json.load(sys.stdin)
        command = data.get("tool_input", {}).get("command", "")
        cwd = data.get("cwd") or os.getcwd()
        root = os.environ.get("CLAUDE_PROJECT_DIR") or cwd
        found = hits(command, cwd, tracked(root))
    except Exception:
        return 0
    if not found:
        return 0
    names = ", ".join(os.path.relpath(p, root) for p in found)
    print(f"Blocked (.claude/hooks/no_inplace_edit.py, ledger 227): this command edits {names} in place, "
          "a file git tracks. Use the Edit tool (Write for a whole new file), so the change shows as a diff "
          "and rewind can restore it.", file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main())
