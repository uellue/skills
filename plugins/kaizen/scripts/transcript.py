#!/usr/bin/env python3
"""Find, render and export Claude Code session transcripts for a debrief.

    transcript.py locate [DIR]                 list the transcripts of the project at DIR (default: cwd)
    transcript.py render FILE.jsonl [options]  print a transcript as readable text
    transcript.py export [ID|FILE] [--to DIR]  copy a session (with its sub-agents) and its rendering into
                                               DIR (default: <repo>/.claude/transcripts/<id>/)

Where transcripts live: the harness writes them to ~/.claude/projects/<slug>/<id>.jsonl, the slug being the
checkout path with "/" replaced by "-", and the sub-agents' transcripts to <id>/subagents/ beside the file.
A worktree or a VM has its own slug and its own home; projects also keep copies inside the checkout
(.claude/transcripts/, .transcripts/, .claude/home-backup/projects/*/, .claude/projects/*/). `locate` looks in all
of these.

Render options: --results N, --tools N, --text N limit the characters kept per tool result, tool input and
message text (defaults 400, 600, 6000). Every event carries the JSONL line number (L<n>) and a timestamp, so a
finding can cite the moment. Messages the person queued while a turn was running appear as "USER (queued
mid-turn)"; task notifications queued the same way appear as NOTIFICATION.

Export copies files, it does not scan them: a transcript holds everything pasted into the chat, so keep the
export directory out of version control (it is under .claude/ by default; check that .claude/ is ignored).
"""

import json
import os
import shutil
import sys
from datetime import datetime
from pathlib import Path


def slug(path: Path) -> str:
    return str(path.resolve()).replace("/", "-")


def repo_root(start: Path) -> Path:
    p = start.resolve()
    for q in [p, *p.parents]:
        if (q / ".git").exists():
            return q
    return p


def candidates(project: Path):
    """Yield (origin, transcript path) for every session transcript of the project, newest last."""
    home = Path.home() / ".claude" / "projects"
    seen = set()
    dirs = [("home", home / slug(project))]
    root = repo_root(project)
    for sub in (".claude/transcripts", ".transcripts"):
        dirs.append(("checkout", root / sub))
    for pattern in (".claude/home-backup/projects/*", ".claude/projects/*"):
        for d in sorted(root.glob(pattern)):
            dirs.append(("checkout", d))
    out = []
    for origin, d in dirs:
        if not d.is_dir():
            continue
        for f in d.rglob("*.jsonl"):
            if "subagents" in f.parts or f.name == "history.jsonl":
                continue
            key = f.resolve()
            if key in seen:
                continue
            seen.add(key)
            out.append((origin, f))
    return sorted(out, key=lambda t: t[1].stat().st_mtime)


def read(path: Path):
    with open(path) as f:
        for n, line in enumerate(f, 1):
            try:
                yield n, json.loads(line)
            except json.JSONDecodeError:
                continue


def summary(path: Path) -> dict:
    first = last = None
    users = 0
    ids = set()
    for _, o in read(path):
        ts = o.get("timestamp")
        if ts:
            first = first or ts
            last = ts
        if o.get("type") == "user" and has_text(o):
            users += 1
        elif o.get("type") == "assistant":
            ids.add((o.get("message") or {}).get("id"))
    return {"first": first, "last": last, "users": users, "messages": len(ids)}


def has_text(o: dict) -> bool:
    c = (o.get("message") or {}).get("content")
    if isinstance(c, str):
        return bool(c.strip())
    return isinstance(c, list) and any(isinstance(x, dict) and x.get("type") == "text" for x in c)


def locate(project: Path):
    rows = candidates(project)
    if not rows:
        print(f"no transcripts found for {project} (slug {slug(project)})")
        return
    for origin, f in rows:
        s = summary(f)
        subs = f.with_suffix("") / "subagents"
        n_sub = len(list(subs.glob("*.jsonl"))) if subs.is_dir() else 0
        span = f"{(s['first'] or '?')[:16]} to {(s['last'] or '?')[:16]}"
        print(
            f"{f.stem}  {span}  {f.stat().st_size / 1e6:.1f} MB  user messages {s['users']}, "
            f"API messages {s['messages']}, sub-agents {n_sub}  [{origin}] {f}"
        )


def trunc(s, n: int) -> str:
    s = s if isinstance(s, str) else json.dumps(s, ensure_ascii=False)
    s = s.replace("\r", "")
    return s if len(s) <= n else s[:n] + f" …[+{len(s) - n} chars]"


def render(path: Path, lim: dict, out=sys.stdout):
    p = lambda *a: print(*a, file=out)  # noqa: E731
    for n, o in read(path):
        t = o.get("type")
        ts = (o.get("timestamp") or "")[:16].replace("T", " ")
        if o.get("isCompactSummary"):
            p(f"\n##### L{n} {ts} COMPACTION SUMMARY #####")
        att = o.get("attachment")
        if isinstance(att, dict) and att.get("type") == "queued_command":
            text = att.get("prompt") or ""
            head = text.lstrip()
            if head.startswith("<task-notification>"):
                kind = "NOTIFICATION"
            elif head.startswith("<agent-message"):
                kind = "AGENT MESSAGE (queued)"
            else:
                kind = "USER (queued mid-turn)"
            p(f"\n=== L{n} {ts} {kind}\n{trunc(text, lim['text'])}")
            continue
        m = o.get("message") or {}
        content = m.get("content")
        if t == "user":
            if isinstance(content, str):
                p(f"\n=== L{n} {ts} USER\n{trunc(content, lim['text'])}")
            elif isinstance(content, list):
                for c in content:
                    if not isinstance(c, dict):
                        continue
                    if c.get("type") == "text":
                        p(f"\n=== L{n} {ts} USER\n{trunc(c.get('text', ''), lim['text'])}")
                    elif c.get("type") == "tool_result":
                        cc = c.get("content")
                        if isinstance(cc, list):
                            cc = "\n".join(x.get("text", "") for x in cc if isinstance(x, dict))
                        flag = " ERROR" if c.get("is_error") else ""
                        p(f"\n--- L{n} {ts} RESULT{flag}\n{trunc(cc or '', lim['results'])}")
        elif t == "assistant":
            model = (m.get("model") or "?").replace("claude-", "")
            for c in content or []:
                if not isinstance(c, dict):
                    continue
                if c.get("type") == "text":
                    p(f"\n=== L{n} {ts} ASSISTANT ({model})\n{trunc(c.get('text', ''), lim['text'])}")
                elif c.get("type") == "tool_use":
                    p(f"\n--- L{n} {ts} TOOL {c.get('name')}\n{trunc(c.get('input'), lim['tools'])}")
        elif t == "summary":
            p(f"\n##### L{n} SUMMARY: {trunc(o.get('summary', ''), 300)}")


def resolve(arg: str | None, project: Path) -> Path:
    if arg and arg.endswith(".jsonl"):
        return Path(arg)
    rows = candidates(project)
    if arg:
        for _, f in rows:
            if f.stem == arg or f.stem.startswith(arg):
                return f
        sys.exit(f"no transcript {arg} for {project}; try: transcript.py locate")
    if not rows:
        sys.exit(f"no transcripts found for {project}")
    return rows[-1][1]


def export(src: Path, to: Path | None):
    root = repo_root(Path.cwd())
    dest = to or root / ".claude" / "transcripts" / src.stem
    dest.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dest / src.name)
    subs = src.with_suffix("") / "subagents"
    if subs.is_dir():
        shutil.copytree(subs, dest / "subagents", dirs_exist_ok=True)
    with open(dest / f"{src.stem}.txt", "w") as f:
        render(src, {"results": 400, "tools": 600, "text": 6000}, out=f)
    n_sub = len(list(subs.glob("*.jsonl"))) if subs.is_dir() else 0
    print(f"exported {src.name} and {n_sub} sub-agent transcripts to {dest}")
    print(f"rendered text: {dest / (src.stem + '.txt')}")
    print(f"exported {datetime.now().isoformat(timespec='seconds')}; keep this directory out of version control")


def main():
    args = sys.argv[1:]
    if not args or args[0] in ("-h", "--help"):
        print(__doc__)
        return
    cmd, rest = args[0], args[1:]
    project = Path.cwd()
    if cmd == "locate":
        locate(Path(rest[0]) if rest else project)
    elif cmd == "render":
        lim = {"results": 400, "tools": 600, "text": 6000}
        for k in list(lim):
            flag = f"--{k}"
            if flag in rest:
                lim[k] = int(rest[rest.index(flag) + 1])
        render(resolve(rest[0] if rest and not rest[0].startswith("--") else None, project), lim)
    elif cmd == "export":
        to = Path(rest[rest.index("--to") + 1]) if "--to" in rest else None
        arg = rest[0] if rest and not rest[0].startswith("--") else None
        export(resolve(arg, project), to)
    else:
        sys.exit(f"unknown command {cmd}; see --help")


if __name__ == "__main__":
    os.environ.setdefault("PYTHONIOENCODING", "utf-8")
    main()
