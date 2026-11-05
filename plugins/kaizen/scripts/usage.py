#!/usr/bin/env python3
"""Usage summary of a Claude Code session for a debrief: messages, tools, sub-agents, tokens, span.

    usage.py              the newest transcript of the current project
    usage.py SESSION_ID   that session of the current project (prefix is enough)
    usage.py PATH.jsonl   a transcript file (a session or a sub-agent)

Transcripts are found with transcript.py's rules (the harness's ~/.claude/projects/<slug>/ and the copies a
checkout keeps). Prints a Markdown table.

Counting: the harness writes one JSONL line per content block of an API message (thinking, text, each tool
call), and every line carries the usage of the whole message, so tokens are counted once per message id and
"API messages" counts messages, not lines. Verified 2026-11-05 against seven sessions: summing per line
over-counts by 2 to 5 times.
"""

import sys
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from transcript import has_text, read, resolve  # noqa: E402


def summarise(path: Path) -> dict:
    tokens = defaultdict(Counter)  # model -> usage counters, once per message id
    tools = Counter()
    users = 0
    seen = set()
    first = last = None
    compactions = 0
    for _, o in read(path):
        t = o.get("type")
        ts = o.get("timestamp")
        if ts:
            first = first or ts
            last = ts
        if t == "user" and has_text(o):
            users += 1
        elif t == "assistant":
            m = o.get("message") or {}
            for c in m.get("content") or []:
                if isinstance(c, dict) and c.get("type") == "tool_use":
                    tools[c.get("name")] += 1
            mid = m.get("id")
            if mid in seen:
                continue
            seen.add(mid)
            model = m.get("model") or "?"
            for k, v in (m.get("usage") or {}).items():
                if isinstance(v, (int, float)):
                    tokens[model][k] += v
        if o.get("isCompactSummary") or t == "summary":
            compactions += 1
    return {
        "path": path,
        "first": first,
        "last": last,
        "users": users,
        "messages": len(seen),
        "tools": tools,
        "tokens": tokens,
        "compactions": compactions,
    }


def output_tokens(s: dict) -> int:
    return sum(c.get("output_tokens", 0) for m, c in s["tokens"].items() if m != "<synthetic>")


def subagents(session: Path) -> list[dict]:
    """Per sub-agent output tokens, from the transcripts beside the session file."""
    out = []
    sub = session.with_suffix("") / "subagents"
    if not sub.is_dir():
        return out
    for f in sorted(sub.rglob("*.jsonl")):
        s = summarise(f)
        models = ", ".join(m.replace("claude-", "") for m in s["tokens"] if m != "<synthetic>")
        out.append(
            {
                "name": f.relative_to(sub).as_posix(),
                "output_tokens": output_tokens(s),
                "messages": s["messages"],
                "tools": sum(s["tools"].values()),
                "models": models,
                "span": span(s["first"], s["last"], short=True),
            }
        )
    return out


def span(first: str | None, last: str | None, short: bool = False) -> str:
    if not (first and last):
        return "?"
    a = datetime.fromisoformat(first.replace("Z", "+00:00"))
    b = datetime.fromisoformat(last.replace("Z", "+00:00"))
    d = b - a
    if short:
        return f"{d.seconds // 60 + d.days * 1440} min"
    return f"{a.date()} to {b.date()} ({d.days} d {d.seconds // 3600} h)"


def main():
    path = resolve(sys.argv[1] if len(sys.argv) > 1 else None, Path.cwd())
    s = summarise(path)
    print(f"Session `{path.stem}`: {span(s['first'], s['last'])}, compactions: {s['compactions']}\n")
    print("| Measure | Value |\n|---|---|")
    print(f"| User messages | {s['users']} |")
    print(f"| API messages | {s['messages']} |")
    print(f"| Tool calls | {sum(s['tools'].values())} |")
    for name, n in s["tools"].most_common():
        print(f"| &nbsp;&nbsp;{name} | {n} |")
    for model, c in s["tokens"].items():
        if model == "<synthetic>":
            continue
        print(f"| Output tokens, {model} | {c.get('output_tokens', 0):,} |")
        print(
            f"| Input tokens, {model} (cache read / created / uncached) | "
            f"{c.get('cache_read_input_tokens', 0):,} / {c.get('cache_creation_input_tokens', 0):,} / "
            f"{c.get('input_tokens', 0):,} |"
        )
    subs = subagents(path)
    if subs:
        total = sum(x["output_tokens"] for x in subs)
        print(f"| Sub-agent transcripts | {len(subs)}, {total:,} output tokens |")
        for x in sorted(subs, key=lambda x: -x["output_tokens"])[:12]:
            print(
                f"| &nbsp;&nbsp;{x['name']} | {x['output_tokens']:,} output tokens, {x['messages']} messages, "
                f"{x['tools']} tool calls, {x['span']}, {x['models']} |"
            )
    print("\nTokens are counted once per API message; see the script's docstring.")


if __name__ == "__main__":
    main()
