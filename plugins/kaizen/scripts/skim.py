#!/usr/bin/env python3
"""The README as an impatient reader sees it: headings and copy-pasteable command blocks, nothing else.

    skim.py README.md [MORE.md ...]

Prints every heading (with its level) and every fenced code block under the heading it belongs to.
Prose, tables, lists and links are dropped. The hallway test's hint-following mode gives the tester
only this view, so that its laziness is enforced by what it can see, not by role-play.
"""

import re
import sys
from pathlib import Path


def skim(path: Path) -> str:
    out, in_code, fence = [], False, ""
    for line in path.read_text(errors="replace").splitlines():
        m = re.match(r"^\s*(`{3,}|~{3,})", line)
        if in_code:
            out.append(line)
            if m and m.group(1)[0] == fence[0] and len(m.group(1)) >= len(fence):
                in_code = False
            continue
        if m:
            in_code, fence = True, m.group(1)
            out.append(line)
        elif re.match(r"^#{1,6}\s", line):
            if out:
                out.append("")
            out.append(line)
        elif "<summary>" in line:  # collapsed sections show their title, as on a rendered page
            out.append("> " + re.sub(r"<[^>]+>", "", line).strip())
    return "\n".join(out).strip() + "\n"


def main():
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"):
        print(__doc__)
        return
    for name in sys.argv[1:]:
        p = Path(name)
        if not p.is_file():
            sys.exit(f"no such file: {name}")
        if len(sys.argv) > 2:
            print(f"==> {name} <==")
        print(skim(p))


if __name__ == "__main__":
    main()
