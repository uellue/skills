#!/usr/bin/env python3
"""Usage summary of a Claude Code session for a debrief: turns, tools, sub-agents, tokens, span.

    usage.py              the newest transcript of the current project
    usage.py SESSION_ID   that session of the current project
    usage.py PATH.jsonl   a transcript file

Reads only local transcript files under ~/.claude/projects/. Prints a Markdown table.
"""

import json
import os
import sys
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path


def project_dir() -> Path:
    slug = os.getcwd().replace("/", "-")
    return Path.home() / ".claude" / "projects" / slug


def transcript_path(arg: str | None) -> Path:
    if arg and arg.endswith(".jsonl"):
        return Path(arg)
    pdir = project_dir()
    if arg:
        return pdir / f"{arg}.jsonl"
    files = sorted(pdir.glob("*.jsonl"), key=lambda p: p.stat().st_mtime)
    if not files:
        sys.exit(f"no transcripts under {pdir}")
    return files[-1]


def read(path: Path):
    with open(path) as f:
        for line in f:
            try:
                yield json.loads(line)
            except json.JSONDecodeError:
                continue


def summarise(path: Path) -> dict:
    tokens = defaultdict(Counter)  # model -> usage counters
    tools = Counter()
    turns = Counter()
    first = last = None
    compactions = 0
    for o in read(path):
        t = o.get("type")
        ts = o.get("timestamp")
        if ts:
            first = first or ts
            last = ts
        if t == "user":
            content = (o.get("message") or {}).get("content")
            if isinstance(content, str) or (
                isinstance(content, list) and any(c.get("type") == "text" for c in content if isinstance(c, dict))
            ):
                turns["user"] += 1
        elif t == "assistant":
            turns["assistant"] += 1
            m = o.get("message") or {}
            model = m.get("model") or "?"
            for k, v in (m.get("usage") or {}).items():
                if isinstance(v, (int, float)):
                    tokens[model][k] += v
            for c in m.get("content") or []:
                if isinstance(c, dict) and c.get("type") == "tool_use":
                    tools[c.get("name")] += 1
        if o.get("isCompactSummary") or t == "summary":
            compactions += 1
    return {
        "path": path,
        "first": first,
        "last": last,
        "turns": turns,
        "tools": tools,
        "tokens": tokens,
        "compactions": compactions,
    }


def subagents(session: Path) -> list[dict]:
    """Per sub-agent output tokens, from the transcripts beside the session file."""
    out = []
    sub = session.with_suffix("") / "subagents"
    if not sub.is_dir():
        return out
    for f in sorted(sub.rglob("*.jsonl")):
        s = summarise(f)
        total_out = sum(c.get("output_tokens", 0) for c in s["tokens"].values())
        out.append({"name": f.relative_to(sub).as_posix(), "output_tokens": total_out, "turns": s["turns"]["assistant"]})
    return out


def span(first: str | None, last: str | None) -> str:
    if not (first and last):
        return "?"
    a = datetime.fromisoformat(first.replace("Z", "+00:00"))
    b = datetime.fromisoformat(last.replace("Z", "+00:00"))
    d = b - a
    return f"{a.date()} to {b.date()} ({d.days} d {d.seconds // 3600} h)"


def main():
    path = transcript_path(sys.argv[1] if len(sys.argv) > 1 else None)
    s = summarise(path)
    print(f"Session `{path.stem}`: {span(s['first'], s['last'])}, compactions: {s['compactions']}\n")
    print("| Measure | Value |\n|---|---|")
    print(f"| User turns | {s['turns']['user']} |")
    print(f"| Assistant turns | {s['turns']['assistant']} |")
    print(f"| Tool calls | {sum(s['tools'].values())} |")
    for name, n in s["tools"].most_common():
        print(f"| &nbsp;&nbsp;{name} | {n} |")
    for model, c in s["tokens"].items():
        if model == "<synthetic>":
            continue
        print(
            f"| Output tokens, {model} | {c.get('output_tokens', 0):,} |"
        )
        print(
            f"| Cache read / created, {model} | {c.get('cache_read_input_tokens', 0):,} / {c.get('cache_creation_input_tokens', 0):,} |"
        )
    subs = subagents(path)
    if subs:
        total = sum(x["output_tokens"] for x in subs)
        print(f"| Sub-agent transcripts | {len(subs)}, {total:,} output tokens |")
        for x in sorted(subs, key=lambda x: -x["output_tokens"])[:10]:
            print(f"| &nbsp;&nbsp;{x['name']} | {x['output_tokens']:,} output tokens, {x['turns']} turns |")


if __name__ == "__main__":
    main()
