#!/usr/bin/env python3
"""Point commit hashes cited in the repository's text files at main after a rebase merge (ledger 220).

    python3 .githooks/rehash.py [--onto main] [--apply]

A rebase merge gives every commit of a branch a new hash, so a record that cites the branch's commit
(`ff82161`) no longer names a commit on main. For each hash cited in backticks in a tracked .md or .json
file that is a commit in this clone but not on --onto, this looks for the commit on --onto with the same
patch-id (the change itself, unaffected by the rebase) since the two diverged. Exactly one match whose
content (the whole tree) is identical: the citation can move to it, since it names the same state. Anything
else is reported and left alone, for a person or an agent to resolve: no match or several (a conflict
resolved in the rebase, a squash, a merge commit), a match whose content differs (main moved before the
merge, or an unrelated commit made the same change), an ambiguous abbreviation. A line that already cites
the new hash is left as it is. Without --apply it only reports. Hashes outside backticks are not seen.
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
    # bytes, not text: a diff need not be UTF-8, and CRLF must reach patch-id unchanged
    diff = subprocess.run(["git", "show", "--no-color", commit], capture_output=True, check=True).stdout
    out = subprocess.run(["git", "patch-id", "--stable"], input=diff, capture_output=True, check=True).stdout.split()
    return out[0].decode() if out else None


def same_tree(a, b):
    return git("diff", "--quiet", a, b, check=False).returncode == 0


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
        if not is_commit(h) and len(git("rev-parse", f"--disambiguate={h}", check=False).stdout.split()) > 1:
            unmatched[h] = (where, "ambiguous abbreviation")
            continue
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
        if len(hits) != 1:
            unmatched[h] = (where, "no commit on main with the same change" if not hits else f"{len(hits)} commits with the same change")
            continue
        new = git("rev-parse", f"--short={len(h)}", hits[0]).stdout.strip()
        if not same_tree(h, hits[0]):
            # main moved before the merge, or an unrelated commit makes the same change: the content differs,
            # so the citation would name a state nobody tested
            unmatched[h] = (where, f"same change as {new}, but the content of the two commits differs")
            continue
        moves[h] = (new, where)
    return moves, unmatched


def apply(moves):
    files = {path for _, where in moves.values() for path in where}
    dirty = git("status", "--porcelain", "--", *sorted(files)).stdout if files else ""
    if dirty:
        raise SystemExit("uncommitted changes in files to rewrite; commit or stash them first:\n" + dirty)
    skipped = []
    for path in sorted(files):
        with open(path, encoding="utf-8", newline="") as f:
            lines = f.read().splitlines(keepends=True)
        for i, line in enumerate(lines):
            # a line that already cites the new hash documents the pair ("moved `old` to `new`"): leave it
            keep = {old for old, (new, _) in moves.items() if old in line and new in line}
            skipped += [f"{path}:{i + 1}: {old}" for old in sorted(keep)]

            def fix(m):
                return HEX.sub(lambda x: moves[x.group(0)][0] if x.group(0) in moves and x.group(0) not in keep else x.group(0), m.group(0))

            lines[i] = SPAN.sub(fix, line)
        with open(path, "w", encoding="utf-8", newline="") as f:
            f.write("".join(lines))
    return skipped


def main(argv=None):
    a = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    a.add_argument("--onto", default="main")
    a.add_argument("--apply", action="store_true")
    args = a.parse_args(argv)
    if git("rev-parse", "--verify", "--quiet", f"{args.onto}^{{commit}}", check=False).returncode != 0:
        raise SystemExit(f"--onto {args.onto}: no such commit")
    moves, unmatched = plan(args.onto)
    for old, (new, where) in moves.items():
        print(f"{old} -> {new}  ({sum(where.values())} in {', '.join(sorted(where))})")
    for old, (where, why) in unmatched.items():
        print(f"{old}: not moved, {why}  ({', '.join(sorted(where))})")
    if moves and args.apply:
        for line in apply(moves):
            print(f"left as it is, the line also cites the new hash: {line}")
        print(f"rewrote {len(moves)} hashes; review with git diff and commit")
    elif moves:
        print("run with --apply to rewrite them")
    return 0


if __name__ == "__main__":
    sys.exit(main())
