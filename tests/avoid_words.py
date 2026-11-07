#!/usr/bin/env python3
"""Report words from the glossary's _Avoid_ lists in lines this branch adds to what the plugin says (ledger 229).

Information, not a failure: some avoided words are right in context ("user" in a skill's description).
Only added lines count, against the merge base with origin/main, so old text does not drown the report.
Text in backticks is skipped, and so are the glossary's own terms ("use scenario" does not report
"scenario"). Two slips of 2026-11-07 are the reason: "the thing" for *subject*, and "prediction" for
*expected effect*, both caught by a person or a review instead of a check.
"""

import re
import subprocess
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
PATHS = ["README.md", "plugins/kaizen/skills", "plugins/kaizen/references"]


def split_top(text):
    """Split at commas outside parentheses."""
    parts, depth, cur = [], 0, ""
    for ch in text:
        depth += ch == "("
        depth -= ch == ")"
        if ch == "," and depth == 0:
            parts.append(cur)
            cur = ""
        else:
            cur += ch
    return parts + [cur]


def glossary(text):
    """(the glossary's terms, the words to avoid), both lower case."""
    terms = {t.lower() for t in re.findall(r"^\*\*(.+?)\*\*:", text, re.M)}
    terms = {re.sub(r"\s*\(.*\)", "", t) for t in terms}
    avoid = set()
    for line in re.findall(r"^_Avoid_: (.*)$", text, re.M):
        for part in split_top(line):
            quoted = re.search(r"\"(.+?)\"", part)
            word = quoted.group(1) if quoted else re.sub(r"\(.*", "", part)
            word = word.strip().lower()
            if word:
                avoid.add(word)
    return terms, avoid


def flags(line, terms, avoid):
    """The avoided words in one line, outside backticks and outside the glossary's own terms."""
    text = re.sub(r"`[^`]*`", " ", line).lower()
    for t in sorted(terms, key=len, reverse=True):
        text = re.sub(r"\b" + re.escape(t) + r"\b", " ", text)
    return sorted(w for w in avoid if re.search(r"\b" + re.escape(w) + r"\b", text))


def added_lines(root):
    """(path, line number, text) of the lines added since the merge base with origin/main, working tree included."""
    base = subprocess.run(["git", "-C", str(root), "merge-base", "HEAD", "origin/main"], capture_output=True, text=True)
    if base.returncode:
        return None
    diff = subprocess.run(["git", "-C", str(root), "diff", "-U0", base.stdout.strip(), "--", *PATHS],
                          capture_output=True, text=True, check=True).stdout
    out, path, n = [], None, 0
    for line in diff.splitlines():
        if line.startswith("+++ "):
            path = line[6:] if line.startswith("+++ b/") else None
        elif line.startswith("@@"):
            n = int(re.search(r"\+(\d+)", line).group(1))
        elif line.startswith("+") and path:
            out.append((path, n, line[1:]))
            n += 1
    return out


def main():
    lines = added_lines(REPO)
    if lines is None:
        print("glossary words to avoid: skipped (no origin/main to compare with)")
        return
    terms, avoid = glossary((REPO / "GLOSSARY.md").read_text())
    found = [(p, n, w) for p, n, t in lines for w in flags(t, terms, avoid)]
    print(f"glossary words to avoid in added lines: {len(found)}")
    for p, n, w in found:
        print(f"  {p}:{n}: {w}")


if __name__ == "__main__":
    main()
