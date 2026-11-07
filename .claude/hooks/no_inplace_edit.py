#!/usr/bin/env python3
"""PreToolUse hook on Bash: block commands that edit a file git tracks in place (ledger 227).

The standing instructions say to edit files with the Edit tool; as a sentence the rule broke in three
sessions. Edits through Bash show no diff to the person and are not restored by rewind
(code.claude.com/docs/en/checkpointing, "Bash command changes not tracked", checked 2026-11-07).

The command is split into simple commands (shell quoting respected, `cd` followed); blocked are:
`sed -i` and `perl -i` on a tracked operand, or fed by `xargs` or `find -exec` inside the repository;
a redirect (`>`, `>>`, `>|`, `&>`) or `tee` into a tracked file; and inline Python (`-c`, or a heredoc
fed to Python) whose `open(…, 'w'/'a'/'+')` or `Path(…).write_text/bytes` names a tracked file, as a
literal or through a variable assigned one. Untracked files, files outside the repository, quoted text
(a commit message) and the project's own scripts (`rehash.py --apply`) pass. Exit 2 blocks the call and
shows stderr to the agent (code.claude.com/docs/en/hooks, "PreToolUse", checked 2026-11-07). Any error
lets the call through: a broken guardrail must not stop all work. Known gaps, left until a slip shows
them: cp, mv, awk -i inplace, truncate, dd, other interpreters' in-place modes, a `sed` inside `$(…)`.
"""

import json
import os
import re
import shlex
import subprocess
import sys

SEPARATORS = {"&&", "||", ";", "|", "&", "(", ")", ";;", "|&"}
REDIRECTS = {">", ">>", ">|", "&>", "&>>"}
WRAPPERS = {"env", "sudo", "command", "nice", "time", "nohup"}
HEREDOC = re.compile(r"(?<!<)<<-?\s*(['\"]?)(\w+)\1")
WRITE_CALLS = [
    re.compile(r"\bopen\(\s*([^,()]+?)\s*,\s*(?:mode\s*=\s*)?['\"]([^'\"]*)['\"]"),
    re.compile(r"\bPath\(\s*([^()]+?)\s*\)\s*\.(write_text|write_bytes)\("),
]
ASSIGN = re.compile(r"\b(\w+)\s*=\s*(?:Path\(\s*)?['\"]([^'\"]+)['\"]")
LITERAL = re.compile(r"^['\"]([^'\"]+)['\"]$")


def split_heredocs(command):
    """(the command lines without heredoc bodies, {line index: [bodies]})."""
    lines, out, bodies, i = command.split("\n"), [], {}, 0
    while i < len(lines):
        line = lines[i]
        i += 1
        idx = len(out)
        out.append(line)
        for m in HEREDOC.finditer(line):
            body = []
            while i < len(lines) and lines[i].strip() != m.group(2):
                body.append(lines[i])
                i += 1
            i += 1
            bodies.setdefault(idx, []).append("\n".join(body))
    return out, bodies


def segments(line):
    lx = shlex.shlex(line, posix=True, punctuation_chars=True)
    lx.whitespace_split = True
    seg = []
    for tok in lx:
        if tok in SEPARATORS:
            if seg:
                yield seg
            seg = []
        else:
            seg.append(tok)
    if seg:
        yield seg


def command_name(seg):
    words = list(seg)
    while words and (re.match(r"^\w+=", words[0]) or os.path.basename(words[0]) in WRAPPERS):
        words = words[1:]  # leading VAR=value and wrappers such as env
    return (os.path.basename(words[0]) if words else ""), words


def in_place(words):
    name = os.path.basename(words[0])
    if name == "sed":
        return any(re.match(r"^(?:-[a-zA-Z]*i|--in-place)", w) for w in words[1:])
    if name == "perl":
        return any(re.match(r"^-[a-zA-Z]*i", w) for w in words[1:])
    return False


def python_writes(code):
    names = dict(ASSIGN.findall(code))
    for rx in WRITE_CALLS:
        for m in rx.finditer(code):
            arg, mode = m.group(1), m.group(2)
            if rx is WRITE_CALLS[0] and not re.search(r"[wax+]", mode):
                continue
            lit = LITERAL.match(arg)
            if lit:
                yield lit.group(1)
            elif arg in names:
                yield names[arg]


def targets(command, cwd):
    """(paths the command would write, whether it runs a bulk in-place edit), paths resolved against `cd`."""
    found, bulk = [], None
    lines, bodies = split_heredocs(command)
    for idx, line in enumerate(lines):
        for seg in segments(line):
            name, words = command_name(seg)
            for i, tok in enumerate(seg[:-1]):
                if tok in REDIRECTS:
                    found.append((cwd, seg[i + 1]))
            if not words:
                continue
            if name == "cd" and len(words) > 1:
                cwd = os.path.normpath(os.path.join(cwd, os.path.expanduser(words[1])))
            elif name == "tee":
                found += [(cwd, w) for w in words[1:] if not w.startswith("-")]
            elif name in ("sed", "perl") and in_place(words):
                found += [(cwd, w) for w in words[1:] if not w.startswith("-")]
            elif name in ("xargs", "find"):
                for j, w in enumerate(words):
                    if os.path.basename(w) in ("sed", "perl") and in_place(words[j:]):
                        bulk = cwd
            elif name.startswith("python"):
                code = words[words.index("-c") + 1] if "-c" in words[:-1] else "\n".join(bodies.get(idx, []))
                found += [(cwd, p) for p in python_writes(code)]
    return [os.path.normpath(os.path.join(d, p)) for d, p in found], bulk


def tracked(root):
    out = subprocess.run(["git", "-C", root, "ls-files", "-z"], capture_output=True, text=True, check=True).stdout
    return {os.path.normpath(os.path.join(root, p)) for p in out.split("\0") if p}


def main():
    try:
        data = json.load(sys.stdin)
        command = data.get("tool_input", {}).get("command", "")
        cwd = data.get("cwd") or os.getcwd()
        root = os.path.normpath(os.environ.get("CLAUDE_PROJECT_DIR") or cwd)
        paths, bulk = targets(command, cwd)
        if not paths and not bulk:
            return 0
        files = tracked(root)
        found = sorted({p for p in paths if p in files})
        if bulk and (bulk + os.sep).startswith(root + os.sep):
            found.append(f"files under {os.path.relpath(bulk, root)}/ (sed or perl -i through xargs or find)")
    except Exception:
        return 0
    if not found:
        return 0
    names = ", ".join(p if p.startswith("files under") else os.path.relpath(p, root) for p in found)
    print(f"Blocked (.claude/hooks/no_inplace_edit.py, ledger 227): this command edits {names} in place, "
          "tracked by git. Use the Edit tool (Write for a whole new file), so the change shows as a diff "
          "and rewind can restore it.", file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main())
