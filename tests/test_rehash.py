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
