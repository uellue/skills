"""The PreToolUse hook against in-place edits (ledger 227), on a throwaway repository: what it blocks and what it lets through.

Cases marked "review" are the reproductions of the independent review of 2026-11-07.
"""

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
        self.out = self.tmp.name  # outside the repository
        self.repo = Path(self.tmp.name) / "repo"
        (self.repo / "design").mkdir(parents=True)
        (self.repo / "sub dir").mkdir()
        for f in ("README.md", "design/kaizen.md", "sub dir/a b.md", "scratch.txt"):
            (self.repo / f).write_text("x\n")
        subprocess.run(["git", "init", "-q"], cwd=self.repo, check=True)
        subprocess.run(["git", "add", "README.md", "design/kaizen.md", "sub dir/a b.md"], cwd=self.repo, check=True)

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
        r = self.run_hook(command, **kw)
        self.assertEqual(r.returncode, 0, f"{command}\n{r.stderr}")

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
        self.assertBlocked(f"sed -i 's/a/b/' {self.repo}/README.md", cwd=self.out)

    def test_blocks_the_reviews_misses(self):
        self.assertBlocked("cd design && sed -i 's/a/b/' kaizen.md")  # review 2
        self.assertBlocked("echo y > \"README.md\"")  # review 3, quoted paths
        self.assertBlocked("sed -i 's/a/b/' \"sub dir/a b.md\"")
        self.assertBlocked("echo y 1>README.md")
        self.assertBlocked("echo y &>README.md")
        self.assertBlocked("echo y >| README.md")
        self.assertBlocked("echo y | tee --append README.md")
        self.assertBlocked("echo y | tee new.log README.md")
        self.assertBlocked("sed 's/a/b/' -i README.md")
        self.assertBlocked("python3 -c \"open('README.md','r+').write('y')\"")
        self.assertBlocked("cat <<'EOF' | python3\nopen('README.md','w').write('y')\nEOF")
        self.assertBlocked("git ls-files '*.md' | xargs sed -i 's/a/b/'")
        self.assertBlocked("find . -name '*.md' -exec sed -i 's/a/b/' {} +")

    def test_lets_other_commands_through(self):
        self.assertPasses("sed -n 1,5p README.md")
        self.assertPasses("grep -n x README.md 2>&1 | head")
        self.assertPasses("sed -i 's/a/b/' scratch.txt")  # untracked
        self.assertPasses(f"echo y > {self.out}/out.log 2>&1")  # outside the repository
        self.assertPasses("python3 .githooks/rehash.py --apply")  # a project script that rewrites by design
        self.assertPasses("python3 -c \"print(open('README.md').read())\"")  # reads only
        self.assertPasses("git commit -q -m 'x' > /dev/null")
        # the hook's first false alarm, 2026-11-07: a commit message that names the forms it blocks
        self.assertPasses("git add README.md && git commit -q -F - <<'EOF'\nsed -i, perl -i and python3 writes are blocked\nEOF\ngit log -1")
        # its second: grep's -i inside sed's argument
        self.assertPasses("sed -n \"$(grep -n -i review README.md | head -1 | cut -d: -f1),+25p\" README.md")

    def test_lets_the_reviews_false_alarms_through(self):
        o = self.out
        self.assertPasses(f"python3 -c \"import json; json.dump({{}}, open('{o}/o.json','w'))\"; cat README.md")  # review 1
        self.assertPasses(f"python3 -c \"d=open('design/kaizen.md').read(); open('{o}/o','w').write(d)\"")
        self.assertPasses(f"sed -i 's/a/b/' {o}/other.md; cat README.md")
        self.assertPasses("git add README.md && git commit -q -m 'sed -i and python3 writes are blocked'")
        self.assertPasses("echo 'a > README.md is bad'")
        self.assertPasses(f"cd {o} && python3 - <<'EOF'\nopen('README.md','w').write('y')\nEOF")  # review 2
        self.assertPasses("cat <<< hi\necho done\nhi")  # review 6

    def test_errors_let_the_call_through(self):
        self.assertEqual(self.run_hook("", stdin="not json").returncode, 0)
        self.assertPasses("echo 'unbalanced")


if __name__ == "__main__":
    unittest.main()
