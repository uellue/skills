"""The PreToolUse hook against in-place edits (ledger 227), on a throwaway repository: what it blocks and what it lets through."""

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HOOK = Path(__file__).resolve().parents[1] / ".claude" / "hooks" / "no_inplace_edit.py"


class TestInplaceHook(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.repo = Path(self.tmp.name) / "repo"
        (self.repo / "design").mkdir(parents=True)
        (self.repo / "README.md").write_text("x\n")
        (self.repo / "design" / "kaizen.md").write_text("x\n")
        (self.repo / "scratch.txt").write_text("untracked\n")
        subprocess.run(["git", "init", "-q"], cwd=self.repo, check=True)
        subprocess.run(["git", "add", "README.md", "design/kaizen.md"], cwd=self.repo, check=True)

    def tearDown(self):
        self.tmp.cleanup()

    def run_hook(self, command, cwd=None, stdin=None):
        payload = stdin if stdin is not None else json.dumps(
            {"tool_name": "Bash", "tool_input": {"command": command}, "cwd": str(cwd or self.repo)})
        env = {**os.environ, "CLAUDE_PROJECT_DIR": str(self.repo)}
        return subprocess.run([sys.executable, str(HOOK)], input=payload, env=env, capture_output=True, text=True)

    def assertBlocked(self, command, **kw):
        r = self.run_hook(command, **kw)
        self.assertEqual(r.returncode, 2, command)
        self.assertIn("Edit tool", r.stderr)

    def assertPasses(self, command, **kw):
        self.assertEqual(self.run_hook(command, **kw).returncode, 0, command)

    def test_blocks_in_place_edits_of_tracked_files(self):
        self.assertBlocked("sed -i 's/a/b/' README.md")  # the slip of 2026-11-07
        self.assertBlocked("sed -E -i.bak 's/a/b/' design/kaizen.md")
        self.assertBlocked("sed --in-place 's/a/b/' README.md")
        self.assertBlocked("perl -pi -e 's/a/b/' README.md")
        self.assertBlocked("python3 -c \"p='design/kaizen.md'; open(p,'w').write('y')\"")  # the slip of 2026-11-07
        self.assertBlocked("python3 - <<'EOF'\nfrom pathlib import Path\nPath('README.md').write_text('y')\nEOF")
        self.assertBlocked("cat > README.md <<'EOF'\ny\nEOF")
        self.assertBlocked("echo y >> design/kaizen.md")
        self.assertBlocked("echo y | tee -a README.md")
        self.assertBlocked(f"sed -i 's/a/b/' {self.repo}/README.md", cwd=Path(self.tmp.name))

    def test_lets_other_commands_through(self):
        self.assertPasses("sed -n 1,5p README.md")
        self.assertPasses("grep -n x README.md 2>&1 | head")
        self.assertPasses("sed -i 's/a/b/' scratch.txt")  # untracked
        self.assertPasses(f"echo y > {self.tmp.name}/out.log 2>&1")  # outside the repository
        self.assertPasses("python3 .githooks/rehash.py --apply")  # a project script that rewrites by design
        self.assertPasses("python3 -c \"print(open('README.md').read())\"")  # reads only
        self.assertPasses("git commit -q -m 'x' > /dev/null")
        # its second: grep's -i inside sed's argument
        self.assertPasses("sed -n \"$(grep -n -i review README.md | head -1 | cut -d: -f1),+25p\" README.md")
        # the hook's first false alarm, 2026-11-07: a commit message that names the forms it blocks
        self.assertPasses("git add README.md check.sh && git commit -q -F - <<'EOF'\nsed -i, perl -i and python3 writes are blocked\nEOF\ngit log -1")

    def test_errors_let_the_call_through(self):
        self.assertEqual(self.run_hook("", stdin="not json").returncode, 0)


if __name__ == "__main__":
    unittest.main()
