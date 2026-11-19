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

    def ledger(self, text):
        (self.repo / "design").mkdir(exist_ok=True)
        (self.repo / "design" / "kaizen.md").write_text(text)

    def test_a_row_that_cites_an_issue_wants_a_reference(self):  # ledger 312: f326b60 served issue 13 without one
        self.ledger("| 310 | Onboarding (issue 13, S8) | README | small | built |\n| 311 | Links | tests | small | built |\n")
        r = self.commit("plugins/x/SKILL.md", "Onboarding of first-time users (issue 13)\n\nLedger: 310")
        self.assertEqual(r.returncode, 0)
        self.assertIn("ledger row 310 cites issue 13; add 'Refs #13'", r.stderr)
        r = self.commit("plugins/y/SKILL.md", "Onboarding\n\nRefs #13\n\nLedger: 310, 311")
        self.assertEqual(r.stderr, "")
        r = self.commit("plugins/z/SKILL.md", "Links\n\nLedger: 311")
        self.assertEqual(r.stderr, "")

    def test_closing_an_issue_reminds_of_the_managers_confirmation(self):
        self.ledger("| 310 | Onboarding (issue 13) | README | small | built |\n")
        r = self.commit("plugins/x/SKILL.md", "Onboarding\n\nCloses #13\n\nLedger: 310")
        self.assertEqual(r.returncode, 0)
        self.assertNotIn("add 'Refs #13'", r.stderr)
        self.assertIn("'Closes #13' closes the issue", r.stderr)
        self.assertIn("only after the person confirmed", r.stderr)

    def test_only_issues_count_and_any_closing_keyword_references(self):  # review L1, L2 of pull request 14
        self.ledger("| 320 | Discussed in pull request #14 and run #3 | x | small | done |\n"
                    "| 321 | From issue 13 | x | small | done |\n")
        r = self.commit("plugins/a/SKILL.md", "A\n\nLedger: 320")
        self.assertEqual(r.stderr, "")
        r = self.commit("plugins/b/SKILL.md", "B\n\nFixed #13\n\nLedger: 321")
        self.assertNotIn("add 'Refs #13'", r.stderr)
        self.assertIn("'Fixed #13' closes the issue", r.stderr)
        r = self.commit("plugins/c/SKILL.md", "C, which closes #13.\n\nLedger: 321")
        self.assertIn("'closes #13' closes the issue", r.stderr)
        r = self.commit("plugins/d/SKILL.md", "D\n\nLedger: 321\n# Refs #13")
        self.assertIn("add 'Refs #13'", r.stderr)  # a comment line does not count

    def test_the_diff_below_the_scissors_line_is_not_the_message(self):  # re-review N1: `git commit -v`
        self.ledger("| 401 | From issue 13 | x | small | done |\n")
        (self.repo / "plugins").mkdir()
        (self.repo / "plugins" / "fixture.txt").write_text("Fixes #13\n")
        self.git("add", "plugins/fixture.txt")
        msg = self.repo / "MSG"
        msg.write_text("Add a fixture\n\nLedger: 401\n# ------------------------ >8 ------------------------\n"
                       "# Do not modify or remove the line above.\ndiff --git a/plugins/fixture.txt\n+Fixes #13\n+Refs #13\n")
        r = subprocess.run(["sh", str(HOOK), str(msg)], cwd=self.repo, capture_output=True, text=True)
        self.assertIn("add 'Refs #13'", r.stderr)
        self.assertNotIn("closes the issue", r.stderr)

    def test_a_reference_among_the_trailers_is_named(self):  # 47c7383: "Refs #13" between Ledger: and Co-Authored-By:
        r = self.commit("plugins/x/SKILL.md", "Merged\n\nLedger: 312, 313\nRefs #13\nCo-Authored-By: t <t@t>")
        self.assertEqual(r.returncode, 0)
        self.assertIn("not read as a trailer", r.stderr)
        self.assertIn("put 'Refs #<n>' in the body", r.stderr)
        r = self.commit("plugins/y/SKILL.md", "Merged\n\nRefs #13\n\nLedger: 312, 313\nCo-Authored-By: t <t@t>")
        self.assertNotIn("trailer", r.stderr)

    def test_other_files_need_no_trailer(self):
        r = self.commit("tests/test_x.py", "A test")
        self.assertEqual(r.returncode, 0)
        self.assertEqual(r.stderr, "")


if __name__ == "__main__":
    unittest.main()
