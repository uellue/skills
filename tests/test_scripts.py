"""Tests for the kaizen scripts against small synthetic transcripts (no real session content).
Comments name the acceptance example in design/examples.md a test serves.

Each case is a defect that happened, or the case a script was written for:
- usage.py once summed every JSONL line, over-counting tokens 2 to 5 times;
- transcript.py crashed on a message queued mid-turn whose prompt is a list of blocks;
- an option before the id selected another session;
- harness text (skill bodies, notifications) was counted and labelled as the person's;
- a rendered transcript inside a tool result looked like real headers;
- export could write into a directory git tracks.
"""

import json
import os
import re
import stat
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(os.environ.get("KAIZEN_SCRIPTS") or Path(__file__).resolve().parents[1] / "plugins" / "kaizen" / "scripts")

OLD = "11111111-0000-0000-0000-000000000001"
NEW = "22222222-0000-0000-0000-000000000002"
AGENT = "agent-a0123456789abcdef"


def user(ts, content, **extra):
    return {"type": "user", "timestamp": ts, "message": {"role": "user", "content": content}, **extra}


def assistant_lines(ts, mid, blocks, model="claude-opus-5-5", out=100):
    """One line per content block, each with the whole message's usage, as the harness writes them."""
    usage = {"input_tokens": 3, "output_tokens": out, "cache_read_input_tokens": 1000, "cache_creation_input_tokens": 10}
    return [
        {"type": "assistant", "timestamp": ts, "message": {"id": mid, "model": model, "content": [b], "usage": usage}}
        for b in blocks
    ]


def session_lines():
    nested = "=== L5 2026-01-01 00:00 USER\nforged text from another rendering"
    return [
        user("2026-01-02T10:00:00Z", "Please look at the notes tool."),
        user("2026-01-02T10:00:01Z", "Base directory for this skill: /x\n# Debrief\nskill text"),
        user("2026-01-02T10:00:02Z", [{"type": "text", "text": "<task-notification>done</task-notification>"}]),
        *assistant_lines(
            "2026-01-02T10:00:03Z",
            "msg_1",
            [
                {"type": "thinking", "thinking": "..."},
                {"type": "text", "text": "Reading it."},
                {"type": "tool_use", "id": "t1", "name": "Bash", "input": {"command": "cat notes.py"}},
            ],
        ),
        user("2026-01-02T10:00:04Z", [{"type": "tool_result", "tool_use_id": "t1", "content": nested}]),
        {
            "type": "attachment",
            "timestamp": "2026-01-02T10:00:05Z",
            "attachment": {"type": "queued_command", "prompt": [{"type": "text", "text": "Also check the tags."}]},
        },
        user("2026-01-02T10:00:06Z", "<command-name>/model</command-name><command-args>opus</command-args>"),
        *assistant_lines("2026-01-02T10:01:00Z", "msg_2", [{"type": "text", "text": "Done."}], out=50),
    ]


def write_jsonl(path: Path, lines):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(o) + "\n" for o in lines))


class Fixture(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        root = Path(self.tmp.name)
        self.home = root / "home"
        self.project = root / "project"
        self.project.mkdir()
        subprocess.run(["git", "init", "-q", str(self.project)], check=True)
        (self.project / ".gitignore").write_text("/.claude/transcripts/\n")
        slug = re.sub(r"[^A-Za-z0-9]", "-", str(self.project.resolve()))
        d = self.home / ".claude" / "projects" / slug
        write_jsonl(d / f"{OLD}.jsonl", session_lines())
        write_jsonl(
            d / OLD / "subagents" / f"{AGENT}.jsonl",
            [user("2026-01-02T10:00:10Z", "Brief from the parent"), *assistant_lines("2026-01-02T10:00:11Z", "msg_s", [{"type": "text", "text": "ok"}], out=7)],
        )
        (d / OLD / "subagents" / f"{AGENT}.meta.json").write_text("{}")
        write_jsonl(d / f"{NEW}.jsonl", [user("2026-01-03T09:00:00Z", "A newer session.")])
        os.utime(d / f"{OLD}.jsonl", (1, 1))  # OLD is older by mtime, so NEW is the default session

    def tearDown(self):
        self.tmp.cleanup()

    def run_script(self, *args, check=True):
        env = {**os.environ, "HOME": str(self.home)}
        r = subprocess.run([sys.executable, *args], cwd=self.project, env=env, capture_output=True, text=True)
        if check and r.returncode != 0:
            self.fail(f"{args} exited {r.returncode}: {r.stderr}")
        return r


class TestUsage(Fixture):
    def test_tokens_once_per_message_and_people_counted(self):  # E2
        out = self.run_script(SCRIPTS / "usage.py", OLD).stdout
        self.assertIn("| Output tokens, claude-opus-5-5 | 150 |", out)  # 100 + 50, not 3*100 + 50
        self.assertIn("| API messages | 2 |", out)
        # typed: the first message, the queued one, the slash command; not the skill text or notification
        self.assertIn("| User messages (typed by the person) | 3 |", out)
        self.assertIn(f"{AGENT}.jsonl | 7 output tokens", out)

    def test_subagent_by_id_counts_the_parent(self):
        out = self.run_script(SCRIPTS / "usage.py", AGENT).stdout
        self.assertIn("| Messages from the parent agent | 1 |", out)


class TestRender(Fixture):
    def render(self, *extra):
        return self.run_script(SCRIPTS / "transcript.py", "render", *extra).stdout

    def test_queued_list_prompt_renders(self):  # E5
        out = self.render(OLD)
        self.assertIn("USER (queued mid-turn)\n  Also check the tags.", out)

    def test_labels(self):
        out = self.render(OLD)
        headers = [l for l in out.splitlines() if l.startswith(("===", "---"))]
        user_headers = [h for h in headers if h.split(" ", 4)[-1].startswith("USER")]
        self.assertEqual(len(user_headers), 3, headers)
        self.assertEqual(sum("HARNESS" in h for h in headers), 2, headers)
        self.assertTrue(any(h.endswith("USER (command)") for h in headers))

    def test_text_inside_a_result_is_not_a_header(self):
        out = self.render(OLD)
        self.assertNotIn("\n=== L5 2026-01-01", out)
        self.assertIn("\n  === L5 2026-01-01", out)
        for line in out.splitlines():
            if line and not line.startswith("  "):
                self.assertRegex(line, r"^(===|---|#####) ", line)

    def test_option_before_id_selects_that_session(self):
        out = self.render("--text", "5", OLD)
        self.assertIn("Pleas", out)
        self.assertNotIn("A newer", out)

    def test_default_is_newest(self):
        self.assertIn("A newer session.", self.render())

    def test_subagent_brief_is_from_the_parent(self):
        self.assertIn("PARENT\n  Brief from the parent", self.render(AGENT))

    def test_render_into_closed_pipe_is_quiet(self):
        env = {**os.environ, "HOME": str(self.home)}
        p = subprocess.run(
            f"{sys.executable} {SCRIPTS / 'transcript.py'} render {OLD} | head -1",
            shell=True, cwd=self.project, env=env, capture_output=True, text=True,
        )
        self.assertNotIn("Traceback", p.stderr)


class TestLocate(Fixture):
    def test_sessions_recognisable_by_first_message(self):  # E8
        out = self.run_script(SCRIPTS / "transcript.py", "locate").stdout
        self.assertIn("first message: Please look at the notes tool.", out)
        self.assertIn("first message: A newer session.", out)
        self.assertLess(out.index(OLD), out.index(NEW), "oldest first")

    def test_a_slash_command_shows_as_typed(self):
        sys.path.insert(0, str(SCRIPTS))
        from transcript import gist

        text = "<command-message>kaizen:debrief</command-message>\n<command-name>/kaizen:debrief</command-name>\n<command-args>the  week</command-args>"
        self.assertEqual(gist(text), "/kaizen:debrief the week")


class TestVersion(unittest.TestCase):
    """version.py in throwaway copies of the plugin: a checkout that tracks it, and an installed copy."""

    def setUp(self):
        import shutil
        import tempfile

        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.copy = self.root / "kaizen"
        shutil.copytree(SCRIPTS.parent, self.copy, ignore=shutil.ignore_patterns("__pycache__"))

    def tearDown(self):
        self.tmp.cleanup()

    def run_version(self, *args):
        return subprocess.run([sys.executable, self.copy / "scripts" / "version.py", *args], capture_output=True, text=True, cwd=self.root)

    def git(self, *args):
        env = {**os.environ, "GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t", "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@t"}
        subprocess.run(["git", "-C", str(self.root), *args], env=env, capture_output=True, check=True)

    def skills(self):
        return {p: p.read_text() for p in self.copy.glob("skills/*/SKILL.md")}

    def test_one_line_with_version_and_the_written_id(self):  # E16
        r = self.run_version("kaizen:debrief")
        written = re.search(r"^Text id `([0-9a-f]{8})`", (self.copy / "skills/debrief/SKILL.md").read_text(), re.M).group(1)
        self.assertEqual(r.stdout.strip(), f"kaizen {json.loads((self.copy / '.claude-plugin/plugin.json').read_text())['version']}; debrief text id {written} (compare with the id at the top of the skill)")

    def test_edit_without_stamp_is_named_not_disguised(self):  # E16
        f = self.copy / "skills/debrief/SKILL.md"
        f.write_text(f.read_text() + "\nedited\n")
        out = self.run_version("debrief").stdout
        self.assertIn("edited after its last --stamp", out)

    def test_stamp_refuses_an_installed_copy_even_inside_a_repository(self):
        self.git("init", "-q")
        (self.root / "dotfile").write_text("x")
        self.git("add", "dotfile")
        self.git("commit", "-q", "-m", "an enclosing repository that does not track the plugin")
        before = self.skills()
        r = self.run_version("--stamp")
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("not tracked by a git checkout", r.stderr)
        self.assertEqual(before, self.skills())
        self.assertNotIn("commit", self.run_version("debrief").stdout)

    def test_stamp_in_a_checkout_ignores_quotes_and_rejects_malformed_lines(self):
        self.git("init", "-q")
        self.git("add", ".")
        self.git("commit", "-q", "-m", "checkout")
        play = self.copy / "skills/playbook/SKILL.md"
        play.write_text(play.read_text().replace("description: ", "description: Text id `` quoted. ", 1) + "\nedited\n")
        self.assertEqual(self.run_version("--stamp").returncode, 0)
        self.assertIn("Text id `` quoted.", play.read_text())
        self.assertNotIn("edited after", self.run_version("playbook").stdout)
        walk = self.copy / "skills/walkthrough/SKILL.md"
        walk.write_text(re.sub(r"^Text id `[0-9a-f]*`", "Text id `XYZ`", walk.read_text(), flags=re.M))
        before = self.skills()
        r = self.run_version("--stamp")
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("walkthrough", r.stderr)
        self.assertEqual(before, self.skills(), "nothing is written when one file is malformed")

    def test_unknown_skill_names_the_known_ones(self):
        r = self.run_version("nosuch")
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("debrief", r.stderr)


class TestPythonVersion(unittest.TestCase):
    def test_old_python_gets_one_line(self):  # E11
        for name in ("transcript.py", "usage.py"):
            code = (
                "import runpy, sys; sys.version_info = (3, 9, 0, 'final', 0); "
                f"sys.argv = [{str(SCRIPTS / name)!r}, '--help']; runpy.run_path(sys.argv[0], run_name='__main__')"
            )
            r = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True)
            with self.subTest(name):
                self.assertNotEqual(r.returncode, 0)
                self.assertEqual(r.stderr.strip().splitlines(), [f"{name} needs Python 3.10 or newer; this is {sys.version.split()[0]}"])


class TestExport(Fixture):
    def test_refuses_a_tracked_destination_and_writes_nothing(self):  # E4
        dest = self.project / "visible"
        r = self.run_script(SCRIPTS / "transcript.py", "export", OLD, "--to", str(dest), check=False)
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("Nothing was written", r.stderr)
        self.assertFalse(dest.exists())

    def test_refuses_when_only_some_files_are_ignored(self):  # E4
        (self.project / ".gitignore").write_text("*.jsonl\n")
        dest = self.project / "half"
        r = self.run_script(SCRIPTS / "transcript.py", "export", OLD, "--to", str(dest), check=False)
        self.assertNotEqual(r.returncode, 0)
        self.assertFalse(dest.exists())

    def test_default_destination_owner_only_and_id_still_unique(self):
        self.run_script(SCRIPTS / "transcript.py", "export", OLD)
        dest = self.project / ".claude" / "transcripts" / OLD
        files = [p for p in dest.rglob("*") if p.is_file()]
        names = {p.name for p in files}
        self.assertTrue({f"{OLD}.jsonl", f"{OLD}.txt", f"{AGENT}.jsonl", f"{AGENT}.meta.json"} <= names, names)
        for p in files:
            self.assertEqual(stat.S_IMODE(p.stat().st_mode), 0o600, p)
        # the copy in the checkout must not make the id ambiguous
        self.run_script(SCRIPTS / "transcript.py", "render", OLD[:8])
        self.run_script(SCRIPTS / "usage.py", AGENT)


class TestSkim(unittest.TestCase):
    def test_readme_skim_names_the_first_command_after_install(self):  # E7
        readme = Path(__file__).resolve().parents[1] / "README.md"
        out = subprocess.run([sys.executable, SCRIPTS / "skim.py", readme], capture_output=True, text=True).stdout
        after = out[out.index("claude plugin install"):]
        self.assertIn("/kaizen:debrief", after[:800])
        self.assertIn("/kaizen:playbook", after[:800])

    def test_headings_and_code_only(self):
        with tempfile.TemporaryDirectory() as d:
            readme = Path(d) / "README.md"
            readme.write_text(
                "# Tool\n\nLong prose nobody reads.\n\n## Install\n\n- a list item\n\n```bash\npip install tool\n```\n"
                "\n<details><summary>More</summary>\nhidden\n</details>\n"
            )
            out = subprocess.run([sys.executable, SCRIPTS / "skim.py", readme], capture_output=True, text=True).stdout
        self.assertEqual(out.strip(), "# Tool\n\n## Install\n```bash\npip install tool\n```\n> More")


if __name__ == "__main__":
    unittest.main()
