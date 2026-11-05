"""The pre-push hook against a throwaway repository: what it must refuse and what it must let through."""

import os
import subprocess
import tempfile
import unittest
from pathlib import Path

HOOK = Path(__file__).resolve().parents[1] / ".githooks" / "pre-push"
ZERO = "0" * 40


class TestPrePush(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.repo = Path(self.tmp.name)
        self.git("init", "-q")
        self.deny("SECRETX")

    def tearDown(self):
        self.tmp.cleanup()

    def git(self, *args):
        env = {**os.environ, "GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t", "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@t"}
        return subprocess.run(["git", *args], cwd=self.repo, env=env, capture_output=True, text=True, check=True).stdout.strip()

    def deny(self, text):
        (self.repo / ".git" / "info").mkdir(exist_ok=True)
        (self.repo / ".git" / "info" / "denylist").write_text("# comment\n" + text + "\n")

    def commit(self, content, message="change"):
        (self.repo / "f").write_text(content)
        self.git("add", "f")
        self.git("commit", "-q", "-m", message)
        return self.git("rev-parse", "HEAD")

    def push(self, remote_sha=ZERO):
        head = self.git("rev-parse", "HEAD")
        r = subprocess.run(["sh", str(HOOK)], cwd=self.repo, input=f"refs/heads/x {head} refs/heads/x {remote_sha}\n", capture_output=True, text=True)
        return r.returncode

    def published(self):
        sha = self.git("rev-parse", "HEAD")
        self.git("update-ref", "refs/remotes/origin/x", sha)
        return sha

    def test_added_line_refused(self):
        self.commit("hello SECRETX\n")
        self.assertEqual(self.push(), 1)

    def test_commit_message_body_refused(self):
        self.commit("hello\n", "harmless subject\n\nbody names SECRETX")
        self.assertEqual(self.push(), 1)

    def test_file_name_refused(self):
        (self.repo / "notes-SECRETX.md").write_text("harmless\n")
        self.git("add", "notes-SECRETX.md")
        self.git("commit", "-q", "-m", "harmless")
        self.assertEqual(self.push(), 1)

    def test_removing_a_badly_named_file_passes(self):
        (self.repo / "notes-SECRETX.md").write_text("harmless\n")
        self.git("add", "notes-SECRETX.md")
        self.git("commit", "-q", "-m", "old")
        base = self.published()
        self.git("rm", "-q", "notes-SECRETX.md")
        self.git("commit", "-q", "-m", "remove")
        self.assertEqual(self.push(base), 0)

    def test_invalid_pattern_refuses_instead_of_passing(self):
        self.deny("(unclosed")
        self.commit("hello\n")
        self.assertEqual(self.push(), 1)

    def test_removing_or_editing_near_a_public_line_passes(self):
        self.commit("keep\nold SECRETX line\nnext\n")
        base = self.published()
        self.commit("keep\ngeneralised\nnext\n")
        self.assertEqual(self.push(base), 0)
        self.commit("keep\ngeneralised\nnext changed\n")
        self.assertEqual(self.push(base), 0)

    def test_no_denylist_passes(self):
        (self.repo / ".git" / "info" / "denylist").unlink()
        self.commit("hello SECRETX\n")
        self.assertEqual(self.push(), 0)


if __name__ == "__main__":
    unittest.main()
