"""The plugin's hook after `git commit` (ledger 314), on throwaway repositories, run the way Claude Code runs it.

It fires after every Bash call in every project where the plugin is installed, so besides the warnings these
tests hold it to: silent and exit 0 on anything else (other commands, old or repeated commits, no repository,
bad input, no python3), and the same verdicts as this repository's own commit-msg hook (one table, both hooks).
"""

import json
import os
import shutil
import subprocess
import tempfile
import time
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
PLUGIN = REPO / "plugins" / "kaizen"
SCRIPT = PLUGIN / "scripts" / "commit_check.py"
GIT_HOOK = REPO / ".githooks" / "commit-msg"
HOOK_COMMAND = json.loads((PLUGIN / "hooks" / "hooks.json").read_text())["hooks"]["PostToolUse"][0]["hooks"][0]["command"]

LEDGER = ("| 310 | Onboarding (issue 13, S8) | README | small | built |\n"
          "| 311 | Links | tests | small | built |\n"
          "| 320 | Discussed in pull request #14 and run #3 | x | small | done |\n"
          "| 321 | A tissue 5 sample | x | small | done |\n")

# (message, warnings expected: substrings, one per warning); both hooks must give exactly these
CASES = [
    ("Onboarding\n\nLedger: 310", ["ledger row 310 cites issue 13"]),
    ("Onboarding\n\nRefs #13\n\nLedger: 310, 311", []),
    ("Links\n\nLedger: 311", []),
    ("Numbers\n\nLedger: 320", []),
    ("Onboarding\n\nCloses #13\n\nLedger: 310", ["'Closes #13' closes the issue"]),
    ("Onboarding, which fixes #13.\n\nLedger: 310", ["'fixes #13' closes the issue"]),
    ("Merged\n\nLedger: 310\nRefs #13\nCo-Authored-By: t <t@t>", ["the Ledger: line is not read as a trailer"]),
    # review of a1ebc1b, finding 4: where the two hooks disagreed
    ("Two trailers\n\nLedger: 311\nLedger: 310", ["ledger row 310 cites issue 13"]),
    ("Tissue\n\nLedger: 321", []),
    ("Spaces\n\nfixes  #7\n\nLedger: 311", ["'fixes #7' closes the issue"]),
]


class Repo:
    def __init__(self, root: Path):
        self.root = root
        root.mkdir()
        self.env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")} | {
            "GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t", "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@t"}
        self.git("init", "-q")
        (root / "design").mkdir()
        (root / "design" / "kaizen.md").write_text(LEDGER)
        self.n = 0

    def git(self, *args, env=None):
        return subprocess.run(["git", *args], cwd=self.root, env=env or self.env, capture_output=True, text=True)

    def commit(self, message, date=None):
        self.n += 1
        (self.root / "plugins").mkdir(exist_ok=True)
        (self.root / "plugins" / f"f{self.n}.txt").write_text(str(self.n))
        self.git("add", "-A")
        env = self.env | ({"GIT_COMMITTER_DATE": date, "GIT_AUTHOR_DATE": date} if date else {})
        return self.git("commit", "-q", "-m", message, env=env)


class TestCommitCheck(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.tmp = Path(tmp.name)
        self.repo = Repo(self.tmp / "project")

    def hook(self, command="git commit -m x", cwd=None, stdin=None, path=None, **extra):
        """Run the hooks.json command as Claude Code does, with the hook's JSON on stdin."""
        data = stdin if stdin is not None else json.dumps(
            {"hook_event_name": "PostToolUse", "tool_name": "Bash", "cwd": str(cwd or self.repo.root),
             "tool_input": {"command": command}, **extra})
        env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")} | {"CLAUDE_PLUGIN_ROOT": str(PLUGIN)}
        if path is not None:
            env["PATH"] = path
        r = subprocess.run(["sh", "-c", HOOK_COMMAND], input=data, capture_output=True, text=True, env=env, timeout=30)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual(r.stderr, "")
        return json.loads(r.stdout)["hookSpecificOutput"]["additionalContext"] if r.stdout.strip() else ""

    def test_a_commit_that_misses_its_reference_is_named_once(self):
        self.repo.commit("Onboarding\n\nLedger: 310")
        out = self.hook()
        self.assertIn("ledger row 310 cites issue 13 and the message has no 'Refs #13'", out)
        self.assertRegex(out, r"^kaizen, on commit [0-9a-f]{7}:\n- ")
        self.assertEqual(self.hook(), "")  # the same commit again: already said

    def test_silent_on_everything_else(self):
        self.repo.commit("Onboarding\n\nLedger: 310")
        for command in ("ls -la", "git log --grep commit", "git commit-tree HEAD^{tree}"):
            self.assertEqual(self.hook(command=command), "", command)  # not a commit command, though it names one
        self.assertIn("cites issue 13", self.hook(command="cd x && git -C . -c a=b --no-pager commit -q -m y"))
        self.assertEqual(self.hook(stdin="not json"), "")
        self.assertEqual(self.hook(stdin=""), "")
        plain = self.tmp / "plain"
        plain.mkdir()
        self.assertEqual(self.hook(cwd=plain), "")  # not a repository
        self.assertEqual(self.hook(cwd=self.tmp / "missing"), "")

    def test_the_agent_is_told_what_to_do(self):  # review finding 1: the commit may already be pushed
        self.repo.commit("Onboarding\n\nLedger: 310")
        out = self.hook()
        self.assertIn("if the commit is not pushed, add it with git commit --amend", out)
        self.assertIn("otherwise tell the person instead of rewriting a pushed commit", out)
        self.repo.commit("Onboarding\n\nCloses #13\n\nLedger: 310")
        self.assertIn("ask the person whether it can be closed, or write 'Refs' instead", self.hook())

    def test_options_that_take_a_value_are_not_the_subcommand(self):  # review finding 2b
        self.repo.commit("Onboarding\n\nLedger: 310")
        for command in ("git -c commit.gpgsign=false log -1", "git -C commit status"):
            self.assertEqual(self.hook(command=command), "", command)

    def test_a_commit_older_than_the_command_is_not_its_own(self):  # review finding 2a
        self.repo.commit("Person's own\n\nCloses #9\n\nLedger: 311")
        time.sleep(3.2)  # the person committed a few seconds ago; the agent's commit then failed
        self.assertEqual(self.hook(command='git commit -m "agent"; git log --oneline -1', duration_ms=120), "")
        self.assertIn("'Closes #9'", self.hook(duration_ms=5000))  # made while the command ran: its own

    def test_output_that_names_commit_starts_python_silently(self):  # review finding 6: the filter sees the output too
        self.repo.commit("Onboarding\n\nLedger: 310")
        self.hook()
        self.assertEqual(self.hook(command="git log", tool_response={"stdout": "commit abc\n" * 1000}), "")

    def test_an_old_commit_is_not_the_one_just_made(self):
        old = time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime(time.time() - 600))
        self.repo.commit("Onboarding\n\nLedger: 310", date=old)
        self.assertEqual(self.hook(), "")

    def test_a_failed_commit_says_nothing(self):
        self.repo.commit("Onboarding\n\nLedger: 310")
        self.hook()  # said once
        r = self.repo.git("commit", "-q", "-m", "nothing staged\n\nLedger: 310")
        self.assertNotEqual(r.returncode, 0)
        self.assertEqual(self.hook(), "")

    def test_without_python3_it_stays_silent(self):
        bindir = self.tmp / "bin"
        bindir.mkdir()
        for tool in ("sh", "cat", "printf"):
            found = shutil.which(tool)
            if found:
                (bindir / tool).symlink_to(found)
        self.repo.commit("Onboarding\n\nLedger: 310")
        self.assertEqual(self.hook(path=str(bindir)), "")

    def test_a_python3_that_exits_at_once_leaves_no_stderr(self):  # review finding 7: printf into a closed pipe
        bindir = self.tmp / "fakebin"
        bindir.mkdir()
        (bindir / "python3").write_text("#!/bin/sh\nexit 1\n")
        (bindir / "python3").chmod(0o755)
        data = json.dumps({"cwd": str(self.repo.root), "tool_input": {"command": "git commit -m x"},
                           "tool_response": {"stdout": "x" * 200000}})
        env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")} | {
            "CLAUDE_PLUGIN_ROOT": str(PLUGIN), "PATH": f"{bindir}:{os.environ['PATH']}"}
        r = subprocess.run(["sh", "-c", "trap '' PIPE; " + HOOK_COMMAND], input=data, capture_output=True, text=True,
                           env=env, timeout=30)
        self.assertEqual((r.returncode, r.stdout, r.stderr), (0, "", ""))

    def test_without_a_ledger_only_the_closing_reminder(self):
        (self.repo.root / "design" / "kaizen.md").unlink()
        self.repo.commit("Onboarding\n\nCloses #13\n\nLedger: 310")
        out = self.hook()
        self.assertIn("'Closes #13' closes the issue", out)
        self.assertNotIn("cites issue", out)

    def test_both_hooks_agree_on_the_cases(self):
        hooks = self.tmp / "hooks"
        hooks.mkdir()
        shutil.copy(GIT_HOOK, hooks / "commit-msg")
        for message, expected in CASES:
            with self.subTest(message):
                r = self.repo.commit(message)  # without the git hook: the plugin hook's view
                self.assertEqual(r.returncode, 0, r.stderr)
                plugin = [l for l in self.hook().splitlines() if l.startswith("- ")]
                self.repo.git("config", "core.hooksPath", str(hooks))
                r = self.repo.commit(message)  # with the git hook: its view, on stderr
                self.repo.git("config", "--unset", "core.hooksPath")
                githook = [l for l in r.stderr.splitlines() if l.startswith("commit-msg:")]
                for verdicts in (plugin, githook):
                    self.assertEqual(len(verdicts), len(expected), verdicts)
                    for want in expected:
                        self.assertTrue(any(want in v for v in verdicts), (want, verdicts))
                self.hook()  # mark the second commit as looked at


if __name__ == "__main__":
    unittest.main()
