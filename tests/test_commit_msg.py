"""The commit-msg hook against a throwaway repository: it warns about a missing Ledger: trailer, never refuses."""

import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

HOOK = Path(__file__).resolve().parents[1] / ".githooks" / "commit-msg"


class TestCommitMsg(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.repo = Path(tmp.name)
        self.git("init", "-q")
        hooks = self.repo / "hooks"
        hooks.mkdir()
        shutil.copy(HOOK, hooks / "commit-msg")
        self.git("config", "core.hooksPath", str(hooks))

    def git(self, *args):
        env = {**os.environ, "GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t", "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@t"}
        return subprocess.run(["git", *args], cwd=self.repo, env=env, capture_output=True, text=True)

    def commit(self, path, message):
        f = self.repo / path
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text(message)
        self.git("add", path)
        return self.git("commit", "-q", "-m", message)

    def test_design_change_without_trailer_warns_and_commits(self):
        r = self.commit("design/kaizen.md", "Ledger row changed")
        self.assertEqual(r.returncode, 0)
        self.assertIn("no 'Ledger: <rows>' trailer", r.stderr)

    def test_trailer_silences_the_warning(self):
        r = self.commit("plugins/x/SKILL.md", "Skill changed\n\nLedger: 214, 215")
        self.assertEqual(r.returncode, 0)
        self.assertEqual(r.stderr, "")

    def test_lower_case_or_empty_trailer_warns(self):
        # review 2, finding 9: git log --grep is case-sensitive
        for i, message in enumerate(("Changed\n\nledger: 3", "Changed\n\nLedger:")):
            r = self.commit(f"design/{i}.md", message)
            self.assertIn("no 'Ledger: <rows>' trailer", r.stderr, message)

    def test_other_files_need_no_trailer(self):
        r = self.commit("tests/test_x.py", "A test")
        self.assertEqual(r.returncode, 0)
        self.assertEqual(r.stderr, "")


if __name__ == "__main__":
    unittest.main()
