#!/usr/bin/env python3
"""Point commit hashes cited in the repository's text files at main after a rebase merge (ledger 220).

    python3 .githooks/rehash.py [--onto main] [--apply]

A rebase merge gives every commit of a branch a new hash, so a record that cites the branch's commit
(`ff82161`) no longer names a commit on main. For each hash cited in backticks in a tracked .md or .json
file that is a commit in this clone but not on --onto, this looks for the commit on --onto with the same
patch-id (the change itself, unaffected by the rebase) since the two diverged. Exactly one match: the
citation can move to it. None or several (a conflict resolved in the rebase, a squash, a merge commit):
reported, left alone, for a person or an agent to resolve. Without --apply it only reports.
It works only where the branch's old commits still exist, usually the clone the branch was made in.
"""

import argparse
import re
import subprocess
import sys

SPAN = re.compile(r"`[^`\n]+`")
HEX = re.compile(r"(?<![0-9a-zA-Z])[0-9a-f]{7,40}(?![0-9a-zA-Z])")


def git(*args, input=None, check=True):
    r = subprocess.run(["git", *args], capture_output=True, text=True, input=input)
    if check and r.returncode != 0:
        raise SystemExit(f"git {' '.join(args)}: {r.stderr.strip()}")
    return r


def is_commit(h):
    return git("cat-file", "-e", f"{h}^{{commit}}", check=False).returncode == 0


def patch_id(commit):
    diff = git("show", "--no-color", commit).stdout
    out = git("patch-id", "--stable", input=diff).stdout.split()
    return out[0] if out else None


def cited():
    """{hash: {path: count}} for hex tokens inside backticks in tracked .md and .json files."""
    found = {}
    files = git("ls-files", "*.md", "*.json").stdout.split()
    for path in files:
        try:
            text = open(path, encoding="utf-8").read()
        except (OSError, UnicodeDecodeError):
            continue
        for span in SPAN.findall(text):
            for h in HEX.findall(span):
                found.setdefault(h, {}).setdefault(path, 0)
                found[h][path] += 1
    return found


def plan(onto):
    moves, unmatched = {}, {}
    ids = {}  # merge base -> {patch-id: [commits on onto since that base]}
    for h, where in sorted(cited().items()):
        if not is_commit(h) or any(git("merge-base", "--is-ancestor", h, ref, check=False).returncode == 0
                                   for ref in (onto, "HEAD")):
            continue  # on main already, or a commit of the branch checked out now (moved after its merge)
        pid = patch_id(h)
        if pid is None:
            unmatched[h] = (where, "no patch-id (a merge commit or an empty change)")
            continue
        base = git("merge-base", h, onto).stdout.strip()
        if base not in ids:
            ids[base] = {}
            for c in git("rev-list", "--no-merges", f"{base}..{onto}").stdout.split():
                p = patch_id(c)
                if p:
                    ids[base].setdefault(p, []).append(c)
        hits = ids[base].get(pid, [])
        if len(hits) == 1:
            moves[h] = (git("rev-parse", f"--short={len(h)}", hits[0]).stdout.strip(), where)
        else:
            unmatched[h] = (where, "no commit on main with the same change" if not hits else f"{len(hits)} commits with the same change")
    return moves, unmatched


def apply(moves):
    files = {path for _, where in moves.values() for path in where}
    dirty = git("status", "--porcelain", "--", *sorted(files)).stdout if files else ""
    if dirty:
        raise SystemExit("uncommitted changes in files to rewrite; commit or stash them first:\n" + dirty)
    for path in sorted(files):
        text = open(path, encoding="utf-8").read()

        def fix_span(m):
            return HEX.sub(lambda x: moves[x.group(0)][0] if x.group(0) in moves else x.group(0), m.group(0))

        with open(path, "w", encoding="utf-8") as f:
            f.write(SPAN.sub(fix_span, text))


def main(argv=None):
    a = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    a.add_argument("--onto", default="main")
    a.add_argument("--apply", action="store_true")
    args = a.parse_args(argv)
    moves, unmatched = plan(args.onto)
    for old, (new, where) in moves.items():
        print(f"{old} -> {new}  ({sum(where.values())} in {', '.join(sorted(where))})")
    for old, (where, why) in unmatched.items():
        print(f"{old}: not moved, {why}  ({', '.join(sorted(where))})")
    if moves and args.apply:
        apply(moves)
        print(f"rewrote {len(moves)} hashes; review with git diff and commit")
    elif moves:
        print("run with --apply to rewrite them")
    return 0


if __name__ == "__main__":
    sys.exit(main())
