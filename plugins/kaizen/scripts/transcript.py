#!/usr/bin/env python3
"""Find, render and export Claude Code session transcripts for a debrief.

Where transcripts live: the harness writes them to ~/.claude/projects/<slug>/<id>.jsonl, the slug being the
checkout path with every character other than a letter or digit replaced by "-", and the sub-agents'
transcripts to <id>/subagents/agent-<agent id>.jsonl beside the file. A worktree or a VM has its own slug
and its own home; projects also keep copies inside the checkout (.claude/transcripts/, .transcripts/,
.claude/home-backup/projects/*/, .claude/projects/*/). `locate` looks in all of these.

A session or sub-agent can be named by its id, a unique prefix of it, or a path to its .jsonl file.

Rendering: every event carries the JSONL line number (L<n>) and a timestamp, so a finding can cite the
moment. Headers start at column zero and every body line is indented by two spaces, so text inside a
message or a tool result (a rendered transcript, a pasted log) can never pass for a header.
Labels: USER (typed by the person, including messages queued while a turn ran), ASSISTANT, TOOL,
RESULT, and HARNESS for everything the harness put in the user's place (skill texts, sub-agent reports,
task notifications, slash-command output, reminders, interrupt markers).

Export copies files and renders them; it does not scan them. A transcript holds everything pasted into
the chat, credentials included, so the export refuses a destination that git would track, and the files
it writes are readable by their owner only.
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

if sys.version_info < (3, 10):
    sys.exit(f"{Path(sys.argv[0]).name} needs Python 3.10 or newer; this is {sys.version.split()[0]}")

LIMITS = {"results": 400, "tools": 600, "text": 6000}

# Text the harness writes in the user's place; never counted or labelled as the person's.
HARNESS_PREFIXES = (
    "<local-command",
    "<task-notification",
    "<agent-message",
    "<system-reminder",
    "<ide_",
    "<user-prompt-submit-hook",
    "Another Claude session sent a message",
    "Base directory for this skill",
    "[Request interrupted",
    "Caveat: The messages below",
    "This session is being continued",
)


def slugs(path: Path) -> list[str]:
    """Candidate slugs: the harness's rule, and the older slash-only rule."""
    p = str(path.resolve())
    return list(dict.fromkeys([re.sub(r"[^A-Za-z0-9]", "-", p), p.replace("/", "-")]))


def repo_root(start: Path) -> Path | None:
    p = start.resolve()
    for q in [p, *p.parents]:
        if (q / ".git").exists():
            return q
    return None


def candidates(project: Path) -> list[tuple[str, Path]]:
    """(origin, path) for every session transcript of the project, oldest first."""
    home = Path.home() / ".claude" / "projects"
    root = repo_root(project)
    # the harness names the folder after the directory the session started in, usually the checkout's root,
    # so a script run from a subdirectory looks there too
    starts = [project] + ([root] if root is not None and root != project.resolve() else [])
    dirs = [("home", home / s) for p in starts for s in slugs(p)]
    if root is not None:
        for sub in (".claude/transcripts", ".transcripts"):
            dirs.append(("checkout", root / sub))
        for pattern in (".claude/home-backup/projects/*", ".claude/projects/*"):
            dirs.extend(("checkout", d) for d in sorted(root.glob(pattern)))
    seen, out = set(), []
    for origin, d in dirs:
        if not d.is_dir():
            continue
        for f in sorted(d.rglob("*.jsonl")):
            if "subagents" in f.parts or f.name == "history.jsonl":
                continue
            if f.stem in seen:  # one copy per session: the harness's own first, then the first checkout copy
                continue
            seen.add(f.stem)
            out.append((origin, f))
    return sorted(out, key=lambda t: t[1].stat().st_mtime)


def subagent_files(session: Path) -> list[Path]:
    sub = session.with_suffix("") / "subagents"
    return sorted(sub.rglob("*.jsonl")) if sub.is_dir() else []


def read(path: Path):
    """Yield (line number, object) for every JSON object line; other lines are skipped."""
    with open(path) as f:
        for n, line in enumerate(f, 1):
            try:
                o = json.loads(line)
            except json.JSONDecodeError:
                continue
            if isinstance(o, dict):
                yield n, o


def as_text(value) -> str:
    """Text of a string or a list of content blocks."""
    if isinstance(value, str):
        return value
    if isinstance(value, list):
        return "\n".join(x.get("text", "") for x in value if isinstance(x, dict) and x.get("type") == "text")
    return ""


def is_harness(text: str) -> bool:
    return text.lstrip().startswith(HARNESS_PREFIXES)


def person_texts(o: dict) -> list[str]:
    """What the person typed in this line: a user message or a message queued mid-turn. Empty otherwise."""
    if o.get("isMeta") or o.get("isCompactSummary"):
        return []
    att = o.get("attachment")
    if isinstance(att, dict) and att.get("type") == "queued_command":
        text = as_text(att.get("prompt"))
        return [text] if text.strip() and not is_harness(text) else []
    if o.get("type") != "user":
        return []
    c = (o.get("message") or {}).get("content")
    blocks = [c] if isinstance(c, str) else [x.get("text", "") for x in c or [] if isinstance(x, dict) and x.get("type") == "text"]
    return [b for b in blocks if b.strip() and not is_harness(b)]


def has_text(o: dict) -> bool:
    """Kept for callers: true when the line carries text the person typed."""
    return bool(person_texts(o))


def gist(text: str, n: int = 70) -> str:
    """One line a person recognises: a slash command as typed, whitespace collapsed, shortened."""
    m = re.search(r"<command-name>\s*(\S+)\s*</command-name>", text)
    if m:
        args = re.search(r"<command-args>(.*?)</command-args>", text, re.S)
        text = m.group(1) + (" " + args.group(1) if args and args.group(1).strip() else "")
    text = " ".join(text.split())
    return text if len(text) <= n else text[: n - 1] + "…"


def summary(path: Path) -> dict:
    first = last = opening = None
    users, ids = 0, set()
    for _, o in read(path):
        ts = o.get("timestamp")
        if ts:
            first = first or ts
            last = ts
        texts = person_texts(o)
        if texts and opening is None:
            opening = gist(texts[0])
        users += len(texts)
        if o.get("type") == "assistant":
            ids.add((o.get("message") or {}).get("id"))
    return {"first": first, "last": last, "users": users, "messages": len(ids), "opening": opening}


def locate(project: Path):
    if repo_root(project) is None:
        print(f"{project.resolve()} is not inside a git checkout: only the harness's own directory is searched")
    rows = candidates(project)
    if not rows:
        print(f"no transcripts found for {project.resolve()} (slugs {', '.join(slugs(project))})")
        return
    for origin, f in rows:
        s = summary(f)
        span = f"{(s['first'] or '?')[:16]} to {(s['last'] or '?')[:16]}"
        print(
            f"{f.stem}  {span}  {f.stat().st_size / 1e6:.1f} MB  user messages {s['users']}, "
            f"API messages {s['messages']}, sub-agents {len(subagent_files(f))}  [{origin}] {f}\n"
            f"    first message: {s['opening'] or '(none typed)'}"
        )


def trunc(s, n: int) -> str:
    s = s if isinstance(s, str) else json.dumps(s, ensure_ascii=False)
    s = s.replace("\r", "")
    return s if len(s) <= n else s[:n] + f" …[+{len(s) - n} chars]"


def body(s: str) -> str:
    """Indent every line by two spaces: a line at column zero in a rendering is always a header."""
    return "\n".join("  " + line for line in s.split("\n"))


def render(path: Path, lim: dict, out=sys.stdout):
    def p(*a):
        print(*a, file=out)

    for n, o in read(path):
        t = o.get("type")
        ts = (o.get("timestamp") or "")[:16].replace("T", " ")
        if o.get("isCompactSummary"):
            p(f"\n##### L{n} {ts} COMPACTION SUMMARY #####")
        att = o.get("attachment")
        if isinstance(att, dict) and att.get("type") == "queued_command":
            text = as_text(att.get("prompt"))
            label = "HARNESS (queued)" if is_harness(text) else "USER (queued mid-turn)"
            p(f"\n=== L{n} {ts} {label}\n{body(trunc(text, lim['text']))}")
            continue
        content = (o.get("message") or {}).get("content")
        if t == "user":
            blocks = [content] if isinstance(content, str) else content or []
            for c in blocks:
                if isinstance(c, str) or (isinstance(c, dict) and c.get("type") == "text"):
                    text = c if isinstance(c, str) else c.get("text", "")
                    label = "HARNESS" if (o.get("isMeta") or is_harness(text)) else ("USER (command)" if text.lstrip().startswith("<command-") else "USER")
                    if label.startswith("USER") and "subagents" in path.parts:
                        label = "PARENT"
                    p(f"\n=== L{n} {ts} {label}\n{body(trunc(text, lim['text']))}")
                elif isinstance(c, dict) and c.get("type") == "tool_result":
                    flag = " ERROR" if c.get("is_error") else ""
                    p(f"\n--- L{n} {ts} RESULT{flag}\n{body(trunc(as_text(c.get('content')) or str(c.get('content') or ''), lim['results']))}")
        elif t == "assistant":
            model = ((o.get("message") or {}).get("model") or "?").replace("claude-", "")
            for c in content or []:
                if not isinstance(c, dict):
                    continue
                if c.get("type") == "text":
                    p(f"\n=== L{n} {ts} ASSISTANT ({model})\n{body(trunc(c.get('text', ''), lim['text']))}")
                elif c.get("type") == "tool_use":
                    p(f"\n--- L{n} {ts} TOOL {c.get('name')}\n{body(trunc(c.get('input'), lim['tools']))}")
        elif t == "summary":
            p(f"\n##### L{n} SUMMARY: {trunc(o.get('summary', ''), 300)}")


def resolve(arg: str | None, project: Path) -> Path:
    """A session or sub-agent transcript by path, id or unique id prefix; the newest session without arg."""
    if arg and (arg.endswith(".jsonl") or "/" in arg):
        p = Path(arg)
        if not p.is_file():
            sys.exit(f"no such transcript file: {arg}")
        return p
    rows = candidates(project)
    if not arg:
        if not rows:
            sys.exit(f"no transcripts found for {project}; try: transcript.py locate")
        return rows[-1][1]
    files = [f for _, f in rows]
    files += [s for f in files for s in subagent_files(f)]
    key = arg.removeprefix("agent-")
    matches = list({f.stem: f for f in reversed(files) if f.stem.removeprefix("agent-").startswith(key)}.values())
    if not matches:
        sys.exit(f"no transcript {arg} for {project}; try: transcript.py locate")
    if len(matches) > 1:
        sys.exit(f"{arg} is ambiguous: " + ", ".join(str(f) for f in matches))
    return matches[0]


def tracked_by_git(dest: Path, names: list[str]) -> list[str]:
    """The names under dest that `git add` would see (inside a checkout and not ignored). dest need not exist."""
    root = repo_root(dest)
    if root is None:
        return []
    seen = []
    for n in names:
        r = subprocess.run(["git", "-C", str(root), "check-ignore", "-q", str(dest.resolve() / n)], capture_output=True)
        if r.returncode != 0:
            seen.append(n)
    return seen


def export(src: Path, to: Path | None, allow_tracked: bool):
    root = repo_root(Path.cwd())
    if to is None:
        if root is None:
            sys.exit("not inside a git checkout; name a destination with --to")
        to = root / ".claude" / "transcripts" / src.stem
    subs = subagent_files(src)
    metas = [m for s in subs for m in [s.with_suffix(".meta.json")] if m.is_file()]
    targets = [(src, to / src.name)] + [(s, to / "subagents" / s.name) for s in subs + metas]
    names = [b.relative_to(to).as_posix() for _, b in targets] + [f"{src.stem}.txt"]
    visible = tracked_by_git(to, names)
    if visible and not allow_tracked:
        sys.exit(
            f"{to} is inside a git checkout and git would see {visible[0]}"
            + (f" and {len(visible) - 1} more" if len(visible) > 1 else "")
            + ": a transcript may hold credentials. Ignore the directory in .gitignore or .git/info/exclude, "
            "or pass --allow-tracked. Nothing was written."
        )
    to.mkdir(parents=True, exist_ok=True)
    for a, b in targets:
        b.parent.mkdir(parents=True, exist_ok=True)
        if b.exists() and b.resolve() == a.resolve():
            continue
        shutil.copy2(a, b)
        os.chmod(b, 0o600)
    txt = to / f"{src.stem}.txt"
    fd = os.open(txt, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, "w") as f:
        render(src, LIMITS, out=f)
    os.chmod(txt, 0o600)
    print(f"exported {src.name} and {len(subs)} sub-agent transcripts to {to} (owner-only permissions)")
    print(f"rendered text: {txt}")
    print(f"exported {datetime.now().isoformat(timespec='seconds')}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("locate", help="list the transcripts of a project")
    a.add_argument("dir", nargs="?", default=".", help="the project directory (default: the current one)")
    a = sub.add_parser("render", help="print a transcript as readable text")
    a.add_argument("id", nargs="?", help="session or sub-agent id, prefix or .jsonl path (default: the newest session)")
    for k, v in LIMITS.items():
        a.add_argument(f"--{k}", type=int, default=v, help=f"characters kept per {k} item (default {v})")
    a = sub.add_parser("export", help="copy a session with its sub-agents and its rendering")
    a.add_argument("id", nargs="?", help="session id, prefix or .jsonl path (default: the newest session)")
    a.add_argument("--to", type=Path, help="destination (default: <repo>/.claude/transcripts/<id>/)")
    a.add_argument("--allow-tracked", action="store_true", help="export into a directory git would track")
    args = ap.parse_args()
    project = Path.cwd()
    if args.cmd == "locate":
        locate(Path(args.dir))
    elif args.cmd == "render":
        render(resolve(args.id, project), {k: getattr(args, k) for k in LIMITS})
    elif args.cmd == "export":
        export(resolve(args.id, project), args.to, args.allow_tracked)


if __name__ == "__main__":
    import signal

    signal.signal(signal.SIGPIPE, signal.SIG_DFL)  # `render ... | head` ends quietly
    main()
