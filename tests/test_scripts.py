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

    def test_found_from_a_subdirectory_of_the_checkout(self):
        sub = self.project / "plugins" / "kaizen"
        sub.mkdir(parents=True)
        env = {**os.environ, "HOME": str(self.home)}
        r = subprocess.run([sys.executable, SCRIPTS / "usage.py", OLD], cwd=sub, env=env, capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("| API messages | 2 |", r.stdout)

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


class TestMessages(unittest.TestCase):
    """transcript.py messages: numbering and length of the agent's replies to the person (ledger 209; field-test
    run 8: the sync restarted at 1 while the update's questions 6 to 8 were open, the debrief jumped from 7 to 13)."""

    def measure(self, lines):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "s.jsonl"
            write_jsonl(p, lines)
            r = subprocess.run([sys.executable, SCRIPTS / "transcript.py", "messages", str(p)], capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stderr)
        return r.stdout

    def reply(self, ts, text, mid):
        return assistant_lines(ts, mid, [{"type": "text", "text": text}])

    def test_a_restart_while_numbers_were_used_is_flagged_a_continuation_is_not(self):
        out = self.measure([
            user("2026-01-02T10:00:00Z", "/kaizen:update"),
            *self.reply("2026-01-02T10:00:01Z", "Questions:\n1. Branch?\n2. Ledger?\n3. Tracker?", "m1"),
            user("2026-01-02T10:00:02Z", "1 yes"),
            *self.reply("2026-01-02T10:00:03Z", "Next:\n1. Push?\n2. Draft?", "m2"),
            user("2026-01-02T10:00:04Z", "go on"),
            *self.reply("2026-01-02T10:00:05Z", "Then:\n3. Commit?\n4. PR?", "m3"),
        ])
        self.assertEqual(out.count("RESTART"), 1, out)
        self.assertIn("RESTART at 1 after 3", out)
        self.assertIn("1 restart", out)

    def test_a_jump_within_a_reply_is_flagged(self):
        out = self.measure([user("2026-01-02T10:00:00Z", "go"), *self.reply("2026-01-02T10:00:01Z", "1. a\n2. b\n**7.** c\n8. d", "m1")])
        self.assertIn("JUMP 2->7", out)

    def test_code_blocks_and_indented_sublists_are_not_items(self):
        text = "1. Run:\n```\n1. not an item\n```\n   1. a sub-step\n2. Done."
        out = self.measure([user("2026-01-02T10:00:00Z", "go"), *self.reply("2026-01-02T10:00:01Z", text, "m1")])
        self.assertNotIn("RESTART", out)
        self.assertNotIn("JUMP", out)
        self.assertIn("numbers 1-2", out)

    def test_text_blocks_between_tool_calls_make_one_reply_and_harness_text_does_not_split_it(self):
        out = self.measure([
            user("2026-01-02T10:00:00Z", "go"),
            *assistant_lines("2026-01-02T10:00:01Z", "m1", [{"type": "text", "text": "1. first"},
                                                            {"type": "tool_use", "id": "t1", "name": "Bash", "input": {}}]),
            user("2026-01-02T10:00:02Z", [{"type": "tool_result", "tool_use_id": "t1", "content": "ok"}]),
            user("2026-01-02T10:00:02Z", "Base directory for this skill: /x"),
            *self.reply("2026-01-02T10:00:03Z", "1. again", "m2"),
        ])
        self.assertIn("RESTART", out)  # within one reply: a restart, flagged as such
        self.assertIn("1 replies", out)

    def test_restating_open_items_with_their_numbers_is_not_a_restart(self):
        # review of 2026-11-10: open items restated keep their numbers (standing instructions)
        out = self.measure([
            user("2026-01-02T10:00:00Z", "go"),
            *self.reply("2026-01-02T10:00:01Z", "1. a\n2. b\n3. c", "m1"),
            user("2026-01-02T10:00:02Z", "1 yes"),
            *self.reply("2026-01-02T10:00:03Z", "Still open:\n2. b\n3. c\n4. new", "m2"),
        ])
        self.assertNotIn("RESTART", out)
        self.assertIn("restates 2-3", out)

    def test_bold_numbers_tilde_fences_years_and_a_one_space_indent(self):
        text = "1. a\n**2**. b\n~~~\n1. code\n~~~\n2026. was a year\n 3. c"
        out = self.measure([user("2026-01-02T10:00:00Z", "go"), *self.reply("2026-01-02T10:00:01Z", text, "m1")])
        self.assertIn("numbers 1-3", out)
        self.assertNotIn("RESTART", out)
        self.assertNotIn("JUMP", out)

    def test_bold_labels_count_and_markdown_list_syntax_is_flagged(self):
        # principal 2026-11-10: a markdown display renumbers "17. 18. 35." as 17, 18, 19; items are "- **17** ..."
        out = self.measure([
            user("2026-01-02T10:00:00Z", "go"),
            *self.reply("2026-01-02T10:00:01Z", "- **17** Review?\n- **18** Push?\n- **35** Hallway test?", "m1"),
            user("2026-01-02T10:00:02Z", "17 yes"),
            *self.reply("2026-01-02T10:00:03Z", "Steps:\n1. a\n2. b", "m2"),
        ])
        self.assertIn("numbers 17,18,35", out)
        self.assertEqual(out.count("LIST SYNTAX"), 1, out)
        self.assertIn("1 in list syntax", out)

    def test_a_long_reply_is_flagged_with_its_line_count(self):
        out = self.measure([user("2026-01-02T10:00:00Z", "go"), *self.reply("2026-01-02T10:00:01Z", "\n".join(f"line {i}" for i in range(25)), "m1")])
        self.assertIn("25 lines", out)
        self.assertIn("LONG", out)


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

    def written(self, skill="debrief"):
        return re.search(r"^Text id `([0-9a-f]{8})`", (self.copy / f"skills/{skill}/SKILL.md").read_text(), re.M).group(1)

    def test_installed_and_current_is_silent(self):  # E16, principal 2026-11-05: only where relevant
        r = self.run_version("debrief", self.written())
        self.assertEqual((r.returncode, r.stdout), (0, ""))

    def test_older_text_in_the_session_says_reload(self):  # E16
        out = self.run_version("debrief", "0000aaaa").stdout
        self.assertIn("older text of debrief", out)
        self.assertIn("/reload-plugins", out)

    def test_checkout_gets_a_short_status(self):
        self.git("init", "-q")
        self.git("add", ".")
        self.git("commit", "-q", "-m", "checkout")
        self.assertRegex(self.run_version("debrief", self.written()).stdout.strip(), r"^kaizen \S+, commit \w+: debrief current$")

    def test_unknown_skill_names_the_known_ones(self):
        r = self.run_version("nosuch")
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("debrief", r.stderr)


class TestProjectNotice(unittest.TestCase):
    """version.py at a skill's start, in a project whose records are older than the installed plugin (ledger 280, E33)."""

    OLD_BLOCK = "## Working rules\n\n- Keep changes tight: no speculative generality, no abstraction without a second concrete user.\n"

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.project = Path(self.tmp.name) / "project"
        self.project.mkdir()
        env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
        subprocess.run(["git", "init", "-q"], cwd=self.project, env=env, check=True)
        self.installed = json.loads((SCRIPTS.parent / ".claude-plugin" / "plugin.json").read_text())["version"]
        skill = SCRIPTS.parent / "skills" / "playbook" / "SKILL.md"
        self.text_id = re.search(r"^Text id `([0-9a-f]{8})`", skill.read_text(), re.M).group(1)

    def tearDown(self):
        self.tmp.cleanup()

    def start(self, skill="playbook", cwd=None):
        """What a skill runs at its start, in the project; only the notice line, not the maintainer's status line.
        Without git's hook variables, so that a commit hook's GIT_DIR cannot point it at the real repository (279)."""
        env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
        r = subprocess.run([sys.executable, SCRIPTS / "version.py", skill, self.text_id], cwd=cwd or self.project,
                           capture_output=True, text=True, env=env)
        self.last = r
        return "\n".join(l for l in r.stdout.splitlines() if "/kaizen:update" in l)

    def test_a_version_line_in_a_quote_or_bold_after_a_merge_is_read(self):
        for line in (f"> Kaizen standing instructions, version {self.installed}: x",
                     f"**Kaizen standing instructions, version {self.installed}**: x",
                     f"- Kaizen standing instructions, version: {self.installed}"):
            with self.subTest(line):
                (self.project / "CLAUDE.md").write_text(line + "\n" + self.OLD_BLOCK)
                self.assertEqual(self.start(), "")

    def test_a_read_only_git_dir_or_no_git_never_breaks_the_line_nor_claims_once(self):
        (self.project / "CLAUDE.md").write_text(self.OLD_BLOCK)
        info = self.project / ".git" / "info"
        info.mkdir(exist_ok=True)
        info.chmod(0o500)
        try:
            out = self.start()
            self.assertEqual(self.last.returncode, 0, self.last.stderr)
            self.assertIn("/kaizen:update", out)
            self.assertNotIn("Said once", out)
        finally:
            info.chmod(0o700)
        plain = Path(self.tmp.name) / "plain"
        plain.mkdir()
        (plain / "CLAUDE.md").write_text(self.OLD_BLOCK)
        out = self.start(cwd=plain)
        self.assertIn("/kaizen:update", out)
        self.assertNotIn("Said once", out)

    def test_the_update_marks_the_notice_as_said_so_skills_inside_it_stay_quiet(self):
        (self.project / "CLAUDE.md").write_text(self.OLD_BLOCK)
        update = SCRIPTS.parent / "skills" / "update" / "SKILL.md"
        playbook_id = self.text_id
        self.text_id = re.search(r"^Text id `([0-9a-f]{8})`", update.read_text(), re.M).group(1)
        self.assertEqual(self.start("update"), "")
        self.text_id = playbook_id
        self.assertEqual(self.start("playbook"), "")

    def test_an_unversioned_copy_is_named_once_per_installed_version(self):
        (self.project / "CLAUDE.md").write_text(self.OLD_BLOCK)
        first = self.start()
        self.assertIn("CLAUDE.md: standing instructions from before 0.6 (no version line)", first)
        self.assertIn(f"Said once for {self.installed}", first)
        self.assertEqual(self.start(), "")
        self.assertEqual((self.project / ".git" / "info" / "kaizen-update-noticed").read_text().strip(), self.installed)
        (self.project / ".git" / "info" / "kaizen-update-noticed").write_text("0.5.5\n")
        self.assertIn("/kaizen:update", self.start())

    def test_an_older_version_line_and_an_old_ledger_are_named(self):
        (self.project / "AGENTS.md").write_text("Kaizen standing instructions, version 0.5.9: /kaizen:update brings them up to date.\n" + self.OLD_BLOCK)
        (self.project / "design").mkdir()
        (self.project / "design" / "kaizen.md").write_text("# Kaizen ledger\n\nMessage size: comfortable, asked 2026-11-01.\n")
        out = self.start()
        self.assertIn("AGENTS.md: standing instructions from 0.5.9", out)
        self.assertIn("design/kaizen.md: no Public: line", out)

    def test_silent_when_current_or_when_the_project_never_used_the_plugin(self):
        self.assertEqual(self.start(), "")
        (self.project / "CLAUDE.md").write_text(f"Kaizen standing instructions, version {self.installed}: x\n" + self.OLD_BLOCK)
        self.assertEqual(self.start(), "")

    def test_the_update_skill_itself_does_not_point_at_itself(self):
        (self.project / "CLAUDE.md").write_text(self.OLD_BLOCK)
        update = SCRIPTS.parent / "skills" / "update" / "SKILL.md"
        self.text_id = re.search(r"^Text id `([0-9a-f]{8})`", update.read_text(), re.M).group(1)
        self.assertEqual(self.start("update"), "")

    def test_versions_compare_with_a_pre_release_before_its_release(self):
        import importlib.util

        spec = importlib.util.spec_from_file_location("version", SCRIPTS / "version.py")
        v = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(v)
        order = ["0.5.5", "0.5.10", "0.6.0-dev.1", "0.6.0-dev.2", "0.6.0", "0.6.1", "1.0.0"]
        self.assertEqual(sorted(order, key=v.version_key), order)


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


class TestSelftestBrief(unittest.TestCase):
    def test_brief_names_the_subject_and_prepares_the_project(self):
        repo = Path(__file__).resolve().parents[1]
        with tempfile.TemporaryDirectory() as d:
            run = Path(d) / "run"
            r = subprocess.run([sys.executable, repo / "benchmarks/plugin-newcomer/brief.py", "existing-tool", "--scratch", run], capture_output=True, text=True)
            self.assertEqual(r.returncode, 0, r.stderr)
            brief = (run / "brief.txt").read_text()
            self.assertTrue(brief.startswith("UNDER TEST: the kaizen plugin"))
            self.assertNotRegex(brief, r"<(REPO|SCRATCH|SCENARIO)>")
            self.assertIn("tally", brief)
            self.assertTrue((run / "project" / "tally.py").is_file())
            self.assertTrue((run / "project" / ".git").is_dir())
            git = lambda *a: subprocess.run(["git", "-C", run / "project", *a], capture_output=True, text=True).stdout.strip()
            self.assertEqual(git("rev-parse", "--abbrev-ref", "HEAD"), "main", "the scenario's files are committed on main")
            self.assertIn("tally.py", git("ls-files"))
            self.assertEqual(git("status", "--porcelain"), "")
            copy = run / "kaizen"
            self.assertIn(str(copy), brief)
            self.assertNotIn(str(repo) + "/", brief, "the tester reads the copy, never this repository")
            self.assertTrue((copy / "plugins/kaizen/scripts/version.py").is_file())
            skill = (copy / "plugins/kaizen/skills/debrief/SKILL.md").read_text()
            written = re.search(r"^Text id `([0-9a-f]{8})`", skill, re.M).group(1)
            silent = subprocess.run([sys.executable, copy / "plugins/kaizen/scripts/version.py", "debrief", written], capture_output=True, text=True)
            self.assertEqual(silent.stdout, "", "the copy behaves as an installed plugin: silent when current")
            bad = subprocess.run([sys.executable, repo / "benchmarks/plugin-newcomer/brief.py", "existing-tool", "--scratch", run / "brief.txt"], capture_output=True, text=True)
            self.assertNotIn("Traceback", bad.stderr)
            again = subprocess.run([sys.executable, repo / "benchmarks/plugin-newcomer/brief.py", "existing-tool", "--scratch", run], capture_output=True, text=True)
            self.assertNotEqual(again.returncode, 0, "a used scratch directory is refused")
            cfg = Path(d) / "gitconfig"
            cfg.write_text("[commit]\n\tgpgsign = true\n[core]\n\thooksPath = /nonexistent\n")
            signed = subprocess.run([sys.executable, repo / "benchmarks/plugin-newcomer/brief.py", "existing-tool", "--scratch", Path(d) / "run2"],
                                    capture_output=True, text=True, env={**os.environ, "GIT_CONFIG_GLOBAL": str(cfg)})
            self.assertEqual(signed.returncode, 0, "a maintainer who signs commits can prepare a run: " + signed.stderr[-200:])


class TestSkim(unittest.TestCase):
    def test_readme_skim_names_the_first_command_after_install(self):  # E7
        readme = Path(__file__).resolve().parents[1] / "README.md"
        out = subprocess.run([sys.executable, SCRIPTS / "skim.py", readme], capture_output=True, text=True).stdout
        after = out[out.index("claude plugin install"):]
        self.assertIn("/kaizen:debrief", after[:800])
        self.assertIn("/kaizen:playbook", after[:800])

    def test_list_item_with_inline_command_is_kept(self):
        # The one README skim measured against a person (2026-11-06): their first command was inline code in a
        # Prerequisites bullet, which the view dropped. Bullets with inline code stay; plain bullets go.
        with tempfile.TemporaryDirectory() as d:
            readme = Path(d) / "README.md"
            readme.write_text("## Prerequisites\n\n- Debian 13 with `apt install qemu-system-x86 virtinst`\n- a user in the libvirt group\n\n1. then run `tool setup`\n")
            out = subprocess.run([sys.executable, SCRIPTS / "skim.py", readme], capture_output=True, text=True).stdout
            self.assertIn("`apt install qemu-system-x86 virtinst`", out)
            self.assertIn("`tool setup`", out)
            self.assertNotIn("libvirt group", out)

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
