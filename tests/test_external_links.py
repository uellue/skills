"""The release list of external links and dated claims (ledger 311), on a synthetic repository, without the network."""

import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path

from external_links import MANIFEST, last_release, report


class TestExternalLinks(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")} | {
            "GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@example.invalid",
            "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@example.invalid"}
        self.git("init", "-q")
        (self.root / "plugins/kaizen/.claude-plugin").mkdir(parents=True)
        (self.root / "plugins/kaizen/references").mkdir()

    def tearDown(self):
        self.tmp.cleanup()

    def git(self, *args, date=None):
        env = self.env | ({"GIT_AUTHOR_DATE": date, "GIT_COMMITTER_DATE": date} if date else {})
        subprocess.run(["git", "-C", str(self.root), *args], check=True, env=env, capture_output=True)

    def release(self, version, date):
        (self.root / MANIFEST).write_text(json.dumps({"name": "kaizen", "version": version}))
        self.git("add", "-A")
        self.git("commit", "-qm", version, date=f"{date}T12:00:00")

    def test_the_last_release_skips_pre_releases(self):
        self.release("0.5.5", "2026-11-09")
        self.release("0.6.0-dev.1", "2026-11-10")
        self.assertEqual(last_release(self.root), "2026-11-09")
        self.release("0.6.0", "2026-11-12")
        self.assertEqual(last_release(self.root), "2026-11-12")

    def test_links_and_claims_older_than_the_release_are_listed(self):
        (self.root / "README.md").write_text(
            "See [OpenSpec](https://github.com/Fission-AI/OpenSpec#readme).\n"
            "Matt Pocock's skills (github.com/mattpocock/skills, 27 skills, checked 2026-11-05).\n")
        (self.root / "plugins/kaizen/references/companions.md").write_text(
            "Docs: https://code.claude.com/docs/en/plugins.md (checked 2026-11-15).\n")
        self.release("0.6.0", "2026-11-12")
        fetched = []
        lines, broken = report(self.root, fetch=lambda u: fetched.append(u) or ("HTTP 404" if "mattpocock" in u else "ok"))
        text = "\n".join(lines)
        self.assertEqual(sorted(fetched), ["https://code.claude.com/docs/en/plugins.md",
                                           "https://github.com/Fission-AI/OpenSpec#readme",
                                           "https://github.com/mattpocock/skills"])
        self.assertEqual(broken, 1)
        self.assertIn("HTTP 404     https://github.com/mattpocock/skills  (README.md:2)", text)
        self.assertIn("claims checked before the last release: 1 of 2", text)
        self.assertIn("2026-11-05  README.md:2", text)
        self.assertNotIn("2026-11-15  plugins", text)

    def test_offline_fetches_nothing(self):
        (self.root / "README.md").write_text("https://example.org/x\n")
        lines, broken = report(self.root, fetch=lambda u: self.fail("fetched"), offline=True)
        self.assertEqual(broken, 0)
        self.assertIn("not fetched", "\n".join(lines))


if __name__ == "__main__":
    unittest.main()
