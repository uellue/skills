#!/usr/bin/env python3
"""List what the plugin says about other projects, for rereading before a release (ledger 311).

    python3 tests/external_links.py            every external link, with whether it still answers, and every
                                               "checked <date>" older than the last release
    python3 tests/external_links.py --offline  the same lists without fetching anything

Links to third-party projects and claims about them ("checked 2026-11-05") go stale: a moved page, a changed
install command, a new telemetry default. This lists them; whether a page still says what we say it says is for
a person to read. Exit status 1 when a link does not answer, so that a release step notices. It needs the network,
so it is not part of check.sh. The last release is the last commit that set a version without a pre-release part
in the plugin's plugin.json.
"""

import http.client
import json
import re
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
MANIFEST = "plugins/kaizen/.claude-plugin/plugin.json"
FILES = ["README.md", "CLAUDE.md", "CODING_STANDARDS.md", "GLOSSARY.md"]
GLOBS = ["plugins/kaizen/skills/*/SKILL.md", "plugins/kaizen/references/*.md", "plugins/kaizen/evals/README.md"]
LINK = re.compile(r"https?://[^\s)\]<>`'\"]+|(?<![\w/.])(?:github\.com|gitlab\.com|skills\.sh|code\.claude\.com)/[^\s)\]<>`'\"]+")
CHECKED = re.compile(r"\bchecked(?: on|:)? (\d{4}-\d{2}-\d{2})\b")


def sources(root: Path) -> list[Path]:
    found = [root / f for f in FILES if (root / f).is_file()]
    for g in GLOBS:
        found += sorted(root.glob(g))
    return found


def scan(path: Path, root: Path):
    """(links, dated claims) in one file: [(url, 'file:line')], [(date, 'file:line', line text)]."""
    links, claims = [], []
    for n, line in enumerate(path.read_text(errors="replace").splitlines(), 1):
        where = f"{path.relative_to(root)}:{n}"
        for m in LINK.finditer(line):
            url = m.group(0).rstrip(".:,;")
            if line[m.end():m.end() + 1] == "<":
                continue  # a placeholder such as https://github.com/<owner>/<repo>, not a link
            links.append((url if url.startswith("http") else "https://" + url, where))
        for m in CHECKED.finditer(line):
            claims.append((m.group(1), where, line.strip()))
    return links, claims


def last_release(root: Path) -> str | None:
    """The date (YYYY-MM-DD) of the last commit that set a release version in the manifest."""
    log = subprocess.run(["git", "-C", str(root), "log", "--format=%H %cs", "--", MANIFEST],
                         capture_output=True, text=True).stdout.split("\n")
    for entry in filter(None, log):
        commit, date = entry.split()
        shown = subprocess.run(["git", "-C", str(root), "show", f"{commit}:{MANIFEST}"], capture_output=True, text=True)
        if shown.returncode == 0 and "-" not in json.loads(shown.stdout).get("version", "-"):
            return date
    return None


def answers(url: str, timeout: float = 15) -> str:
    """'ok' or the reason it does not answer; a generic client name, no personal details."""
    try:
        req = urllib.request.Request(url, method="GET", headers={"User-Agent": "link-check"})
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return "ok" if r.status < 400 else f"HTTP {r.status}"
    except urllib.error.HTTPError as e:
        return f"HTTP {e.code}"
    except (urllib.error.URLError, TimeoutError, OSError) as e:
        return f"no answer ({getattr(e, 'reason', e)})"
    except (http.client.HTTPException, ValueError) as e:  # InvalidURL, e.g. a port that is not a number
        return f"invalid ({e})"


def report(root: Path, fetch=answers, offline=False) -> tuple[list[str], int]:
    links, claims = {}, []
    for p in sources(root):
        l, c = scan(p, root)
        for url, where in l:
            links.setdefault(url, []).append(where)
        claims += c
    release = last_release(root)
    found = release or "none found (in a shallow clone, fetch the history first), so no claim is listed as old"
    out, broken = [f"last release: {found}", f"external links: {len(links)}"], 0
    for url, wheres in sorted(links.items()):
        state = "not fetched" if offline else fetch(url)
        broken += state not in ("ok", "not fetched")
        out.append(f"  {state:12} {url}  ({', '.join(wheres)})")
    stale = [c for c in claims if release and c[0] < release]
    out.append(f"claims checked before the last release: {len(stale)} of {len(claims)}")
    out += [f"  {date}  {where}: {text[:160]}" for date, where, text in sorted(stale)]
    return out, broken


def main():
    offline = "--offline" in sys.argv[1:]
    if set(sys.argv[1:]) - {"--offline"}:
        sys.exit(__doc__)
    lines, broken = report(REPO, offline=offline)
    print("\n".join(lines))
    sys.exit(1 if broken else 0)


if __name__ == "__main__":
    main()
