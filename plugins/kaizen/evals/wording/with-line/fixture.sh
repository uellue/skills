#!/bin/bash
# Fixture for the wording cases (ledger 297, Alex Clausen's wording review): a small tool whose CLAUDE.md carries the
# kaizen wording line, copied from references/standing-instructions.md; tests/test_evals.py does not check the copy.
set -euo pipefail
git init -q -b main .
cat > README.md <<'MD'
# tally

Counts the files in a directory tree by extension: `python3 tally.py <directory>`. Keeps its results between runs in
`~/.cache/tally/`, so a second run over an unchanged tree is fast.
MD
cat > tally.py <<'PY'
"""Count the files in a directory tree by extension."""
import json
import sys
from collections import Counter
from pathlib import Path

CACHE = Path.home() / ".cache" / "tally"


def count(root: Path) -> Counter:
    return Counter(p.suffix or "(none)" for p in root.rglob("*") if p.is_file())


def main() -> int:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".")
    counts = count(root)
    CACHE.mkdir(parents=True, exist_ok=True)
    (CACHE / "last.json").write_text(json.dumps(counts))
    for ext, n in counts.most_common():
        print(f"{n:6d} {ext}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
PY
printf '# tally\n\n## Working rules\n' > CLAUDE.md
cat >> CLAUDE.md <<'MD'
- Before text that people will read counts as done (messages, help, docs, docstrings, comments, commit, pull request and issue text), and in any review, reread it as its reader, who has not seen the conversation: correct, and saying what happened or what to do next; no terms coined in the session, internal names or "as discussed"; short, without filler or hedging; one term for each thing, as in the rest of the codebase; spelling, grammar and tone for the audience.
MD
cat >> CLAUDE.md <<'MD'
- Keep changes tight: no speculative generality, no abstraction without a second concrete user.
MD
git add -A && git -c user.name=t -c user.email=t@example.org commit -qm "tally"
