"""rehash.py against a throwaway repository: a branch merged by rebase, its hashes cited in a record (ledger 220)."""

import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / ".githooks" / "rehash.py"


class TestRehash(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.repo = Path(tmp.name)
        self.git("init", "-q", "-b", "main")
        self.commit("a.txt", "one\n", "start")

    def git(self, *args, date="2026-01-01T00:00:00"):
        env = {**os.environ, "GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t", "GIT_COMMITTER_NAME": "t",
               "GIT_COMMITTER_EMAIL": "t@t", "GIT_COMMITTER_DATE": date, "GIT_AUTHOR_DATE": "2026-01-01T00:00:00"}
        return subprocess.run(["git", *args], cwd=self.repo, env=env, capture_output=True, text=True, check=True).stdout.strip()

    def commit(self, name, content, message):
        (self.repo / name).write_text(content)
        self.git("add", name)
        self.git("commit", "-q", "-m", message)
        return self.git("rev-parse", "--short", "HEAD")

    def rebase_merge(self, branch):
        """What GitHub's rebase merge does: the branch's commits replayed onto main with new hashes."""
        self.git("switch", "-q", "main")
        for c in self.git("rev-list", "--reverse", f"main..{branch}").split():
            self.git("cherry-pick", c, date="2026-02-01T00:00:00")

    def run_script(self, *args):
        return subprocess.run([sys.executable, str(SCRIPT), *args], cwd=self.repo, capture_output=True, text=True)

    def test_cited_hash_moves_to_its_rebased_commit(self):
        self.git("switch", "-q", "-c", "feature")
        old = self.commit("b.txt", "feature\n", "feature")
        self.commit("record.md", f"tested at `{old}`; text id `5bd7cae7`\n", "record")
        self.rebase_merge("feature")
        new = self.git("rev-parse", "--short", "HEAD~1")
        self.assertNotEqual(old, new)
        report = self.run_script()
        self.assertIn(f"{old} -> {new}", report.stdout)
        self.assertEqual((self.repo / "record.md").read_text(), f"tested at `{old}`; text id `5bd7cae7`\n")
        self.run_script("--apply")
        self.assertEqual((self.repo / "record.md").read_text(), f"tested at `{new}`; text id `5bd7cae7`\n")

    def test_hash_already_on_main_and_unchanged_commits_stay(self):
        first = self.git("rev-parse", "--short", "HEAD")
        self.commit("record.md", f"start was `{first}`\n", "record")
        self.assertEqual(self.run_script().stdout, "")

    def test_commits_of_the_checked_out_branch_are_left_for_after_its_merge(self):
        self.git("switch", "-q", "-c", "feature")
        old = self.commit("b.txt", "feature\n", "feature")
        self.commit("record.md", f"tested at `{old}`\n", "record")
        self.assertEqual(self.run_script().stdout, "")

    def test_changed_in_the_rebase_is_reported_not_moved(self):
        self.git("switch", "-q", "-c", "feature")
        old = self.commit("b.txt", "feature\n", "feature")
        self.git("switch", "-q", "main")
        self.commit("b.txt", "conflict resolved differently\n", "on main")
        self.commit("record.md", f"tested at `{old}`\n", "record")
        report = self.run_script("--apply")
        self.assertIn(f"{old}: not moved", report.stdout)
        self.assertEqual((self.repo / "record.md").read_text(), f"tested at `{old}`\n")

    def merged_feature(self):
        """A feature commit, a rebase merge, and a record citing the old hash; returns (old, new)."""
        self.git("switch", "-q", "-c", "feature")
        old = self.commit("b.txt", "feature\n", "feature")
        self.rebase_merge("feature")
        return old, self.git("rev-parse", "--short", "HEAD")

    def test_main_moved_before_the_merge_is_reported_not_moved(self):
        # review 2, finding 4: the rebased commit holds main's newer commits, a state nobody tested
        self.git("switch", "-q", "-c", "feature")
        old = self.commit("b.txt", "feature\n", "feature")
        self.git("switch", "-q", "main")
        self.commit("m.txt", "main moved\n", "main moved")
        self.rebase_merge("feature")
        self.commit("record.md", f"tested at `{old}`\n", "record")
        report = self.run_script()
        self.assertIn(f"{old}: not moved, same change as", report.stdout)

    def test_unrelated_commit_with_the_same_change_is_not_a_match(self):
        # review 2, finding 3: a commit of an open branch, the same change made independently on main
        self.git("switch", "-q", "-c", "other")
        old = self.commit("fix.txt", "fix\n", "fix on other")
        self.git("switch", "-q", "main")
        self.commit("m.txt", "main\n", "main")
        self.commit("fix.txt", "fix\n", "fix on main")
        self.commit("record.md", f"see `{old}`\n", "record")
        self.assertIn(f"{old}: not moved", self.run_script().stdout)

    def test_a_commit_on_main_that_is_not_utf8_does_not_stop_it(self):
        # review 2, finding 1: the latin-1 commit lands on main after the branch point, so its diff is read
        self.git("switch", "-q", "-c", "feature")
        old = self.commit("b.txt", "feature\n", "feature")
        self.git("switch", "-q", "main")
        (self.repo / "latin1.txt").write_bytes(b"caf\xe9\n")
        self.git("add", "latin1.txt")
        self.git("commit", "-q", "-m", "latin-1")
        self.rebase_merge("feature")
        self.commit("record.md", f"tested at `{old}`\n", "record")
        report = self.run_script()
        self.assertEqual(report.returncode, 0, report.stderr)
        self.assertIn(f"{old}: not moved, same change as", report.stdout)

    def test_crlf_and_a_line_documenting_the_pair_are_kept(self):
        # review 2, findings 2 and 5
        old, new = self.merged_feature()
        (self.repo / "record.md").write_bytes(f"tested at `{old}`\r\nmoved `{old}` to `{new}`\r\n".encode())
        self.git("add", "record.md")
        self.git("commit", "-q", "-m", "record")
        report = self.run_script("--apply")
        self.assertIn("left as it is", report.stdout)
        self.assertEqual((self.repo / "record.md").read_bytes(), f"tested at `{new}`\r\nmoved `{old}` to `{new}`\r\n".encode())

    def test_main_behind_its_upstream_is_named_with_the_command_that_updates_it(self):
        # ledger 278: the local main had not been updated after the rebase merge upstream
        self.git("switch", "-q", "-c", "feature")
        old = self.commit("b.txt", "feature\n", "feature")
        self.commit("record.md", f"tested at `{old}`\n", "record")
        self.rebase_merge("feature")
        self.git("update-ref", "refs/remotes/origin/main", "main")
        self.git("remote", "add", "origin", "https://example.invalid/repo.git")
        self.git("config", "branch.main.remote", "origin")
        self.git("config", "branch.main.merge", "refs/heads/main")
        self.git("switch", "-q", "feature")
        self.git("branch", "-f", "main", "main~2")
        out = self.run_script().stdout
        self.assertIn("main is 2 commits behind origin/main", out)
        self.assertIn("git fetch origin main:main", out)
        self.git("remote", "rename", "origin", "upstream")
        out = self.run_script().stdout
        self.assertIn("main is 2 commits behind upstream/main", out)
        self.assertIn("git fetch upstream main:main", out)
        self.git("branch", "-f", "main", "upstream/main~1")
        self.assertIn("main is 1 commit behind", self.run_script().stdout)
        self.git("branch", "-f", "main", "upstream/main")
        self.assertNotIn("behind", self.run_script().stdout)

    def test_onto_a_missing_ref_fails(self):
        self.assertNotEqual(self.run_script("--onto", "nosuch").returncode, 0)

    def test_post_merge_reports_on_main_and_says_when_it_cannot_run(self):
        # review 2, finding 6
        hook = SCRIPT.parent / "post-merge"
        old, new = self.merged_feature()
        self.commit("record.md", f"tested at `{old}`\n", "record")
        (self.repo / ".githooks").mkdir()
        (self.repo / ".githooks" / "rehash.py").write_bytes(SCRIPT.read_bytes())
        r = subprocess.run(["sh", str(hook)], cwd=self.repo, capture_output=True, text=True)
        self.assertIn(f"{old} -> {new}", r.stderr)
        (self.repo / ".githooks" / "rehash.py").unlink()
        r = subprocess.run(["sh", str(hook)], cwd=self.repo, capture_output=True, text=True)
        self.assertEqual(r.returncode, 0)
        self.assertIn("could not run", r.stderr)

    def test_refuses_to_rewrite_a_file_with_uncommitted_changes(self):
        self.git("switch", "-q", "-c", "feature")
        old = self.commit("b.txt", "feature\n", "feature")
        self.commit("record.md", f"tested at `{old}`\n", "record")
        self.rebase_merge("feature")
        (self.repo / "record.md").write_text(f"tested at `{old}`, edited\n")
        report = self.run_script("--apply")
        self.assertNotEqual(report.returncode, 0)
        self.assertEqual((self.repo / "record.md").read_text(), f"tested at `{old}`, edited\n")


if __name__ == "__main__":
    unittest.main()
