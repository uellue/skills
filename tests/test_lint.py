"""Mechanical checks of the skill texts, references and design record.

Each rule stands for a defect that happened: a brief contradicting its skill (REPORT.md), paths that
pointed nowhere, dated anecdotes inside skill bodies, ledger tables broken by a stray pipe, and skill
descriptions that keep growing although they load into every session.
"""

import json
import re
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
PLUGIN = REPO / "plugins" / "kaizen"
SKILLS = sorted(PLUGIN.glob("skills/*/SKILL.md"))

# Budgets: descriptions load into every session; bodies load on every run. Raise only with a reason in the commit.
DESCRIPTION_MAX_CHARS = 800
BODY_MAX_WORDS = 2700

# Strings that once meant something and now contradict the skills.
STALE = {
    "REPORT.md": "testers hand their report back as their final message",
    "docs/kaizen.md": "the ledger is design/kaizen.md",
    "docs/debriefs": "reports are private in .claude/debriefs/",
    "design/playtest.md": "the hallway record lives in design/hallway/",
}

FRONTMATTER = re.compile(r"\A---\nname: (\S+)\ndescription: (.+?)\n(?:[a-z-]+: .*\n)*---\n", re.S)


def body(path: Path) -> str:
    t = path.read_text()
    m = FRONTMATTER.match(t)
    return t[m.end():] if m else t


class TestSkills(unittest.TestCase):
    def test_there_are_skills(self):
        self.assertGreaterEqual(len(SKILLS), 5)

    def test_frontmatter(self):
        for p in SKILLS:
            with self.subTest(p.parent.name):
                m = FRONTMATTER.match(p.read_text())
                self.assertIsNotNone(m, "frontmatter must start with name and description")
                self.assertEqual(m.group(1), p.parent.name)
                self.assertLessEqual(len(m.group(2)), DESCRIPTION_MAX_CHARS, "description over budget")

    def test_body_budget(self):
        for p in SKILLS:
            with self.subTest(p.parent.name):
                self.assertLessEqual(len(body(p).split()), BODY_MAX_WORDS, "body over budget")

    def test_text_ids_current(self):  # E16
        import importlib.util

        spec = importlib.util.spec_from_file_location("version", PLUGIN / "scripts" / "version.py")
        version = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(version)
        for p in SKILLS:
            with self.subTest(p.parent.name):
                found = version.STAMP.findall(p.read_text())
                self.assertEqual(len(found), 1, "exactly one line starting with 'Text id `...`'")
                self.assertRegex(body(p), r"\A\s*# [^\n]+\n\s*Text id `", "the text id line comes right after the title")
                self.assertEqual(found[0], version.text_id(p), "stale text id: run python3 plugins/kaizen/scripts/version.py --stamp")
                self.assertIn(f"scripts/version.py {p.parent.name} {found[0]}`", p.read_text(), "the start-up command carries the same id, runnable as it stands")

    def test_dates_only_as_checked_facts(self):
        # A date in a skill body is a dated fact ("checked 2026-11-05"), never an anecdote.
        for p in SKILLS:
            for m in re.finditer(r"\b20\d\d-\d\d-\d\d\b", body(p)):
                before = body(p)[max(0, m.start() - 40): m.start()]
                with self.subTest(p.parent.name, date=m.group()):
                    self.assertIn("checked", before, "a date in a skill body must say what was checked")


class TestReferences(unittest.TestCase):
    def test_standing_instructions_match_the_readme(self):
        # One text in two places: the README's paste block and the plugin's reference (the playbook offers it).
        def block(text):
            start = text.index("```text\n", text.index("standing instructions") if "standing instructions" in text else 0)
            return text[start + len("```text\n") : text.index("```", start + 8)]
        readme = (REPO / "README.md").read_text()
        ref = (PLUGIN / "references" / "standing-instructions.md").read_text()
        readme_block = block(readme[readme.index("### What you paste for the agent"):])
        self.assertEqual(block(ref), readme_block, "references/standing-instructions.md and the README block differ")

    def files(self):
        return [*SKILLS, *sorted((PLUGIN / "references").glob("*"))]

    def test_plugin_paths_exist(self):  # E12
        for p in self.files():
            for m in re.finditer(r"\$\{CLAUDE_PLUGIN_ROOT\}/([A-Za-z0-9_./-]+[A-Za-z0-9_])", p.read_text()):
                with self.subTest(p.name, path=m.group(1)):
                    self.assertTrue((PLUGIN / m.group(1)).exists(), f"{m.group(1)} does not exist")

    def test_bare_reference_names_exist(self):
        names = {f.name for f in (PLUGIN / "references").iterdir()} | {f.name for f in (PLUGIN / "scripts").iterdir()}
        for p in self.files():
            for m in re.finditer(r"\b(?:references|scripts)/([A-Za-z0-9_-]+\.(?:md|py|yaml))", p.read_text()):
                with self.subTest(p.name, name=m.group(1)):
                    self.assertIn(m.group(1), names)

    def test_no_stale_strings(self):
        for p in self.files():
            text = p.read_text()
            for s, why in STALE.items():
                with self.subTest(p.name, stale=s):
                    self.assertNotIn(s, text, why)


def table_rows(text: str):
    """(line number, cell count) per Markdown table row, with code spans and escaped pipes removed."""
    in_code = False
    for n, line in enumerate(text.splitlines(), 1):
        if line.lstrip().startswith(("```", "~~~")):
            in_code = not in_code
            continue
        if in_code or not line.startswith("|"):
            yield n, None
            continue
        clean = re.sub(r"`[^`]*`", "", line).replace("\\|", "")
        yield n, clean.strip().strip("|").count("|") + 1


class TestTables(unittest.TestCase):
    def test_rows_match_their_header(self):
        files = [*REPO.glob("*.md"), *REPO.glob("design/**/*.md"), *PLUGIN.rglob("*.md"), *REPO.glob("benchmarks/*/*.md")]
        for p in files:
            width = None
            for n, cells in table_rows(p.read_text()):
                if cells is None:
                    width = None
                elif width is None:
                    width = cells
                else:
                    with self.subTest(p.relative_to(REPO).as_posix(), line=n):
                        self.assertEqual(cells, width, "row has a different number of cells than its header")


class TestCoverageReport(unittest.TestCase):  # E13
    def test_lists_examples_no_test_cites(self):
        import sys
        import tempfile

        sys.path.insert(0, str(REPO / "tests"))
        from coverage import uncovered

        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / "design").mkdir()
            # IDs built at run time, so that this file does not count as citing them
            a, b, c, d100 = (f"E{n}" for n in (1, 2, 10, 100))
            (root / "design" / "examples.md").write_text(f"- **{a}** (must; x): a\n- **{b}** (should; y): b\n- **{c}** (must; z): c\n")
            (root / "tests").mkdir()
            (root / "tests" / "test_x.py").write_text(f"def test_a():  # {a}\n    pass  # {d100} is another example\n")
            self.assertEqual(uncovered(root), (3, [f"{b} (should)", f"{c} (must)"]))


class TestManifests(unittest.TestCase):
    def test_versions_and_names(self):
        plugin = json.loads((PLUGIN / ".claude-plugin" / "plugin.json").read_text())
        market = json.loads((REPO / ".claude-plugin" / "marketplace.json").read_text())
        self.assertRegex(plugin["version"], r"^\d+\.\d+\.\d+$")
        self.assertIn(plugin["name"], [p["name"] for p in market["plugins"]])


if __name__ == "__main__":
    unittest.main()
