"""The self-test scenario tracked-project: its fixture holds what the scenario text and the key say it holds.

An earlier fixture contradicted its scenario (the after-merge copy carried bugs the scenario called fixed), and
a run then built findings on that. These checks pin the premises of N32 to N41 (ledger 269, 271).
"""

import json
import re
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
BENCH = REPO / "benchmarks" / "plugin-newcomer"
FIXTURE = BENCH / "scenarios" / "tracked-project"


def standing_instructions(readme: str) -> list[str]:
    """The bullet lines of the README's block for agents, each cut to its first words."""
    block = readme.split("### What you paste for the agent", 1)[1].split("\n### ", 1)[0]
    return [line for line in block.splitlines() if line.startswith("- ")]


class TestTrackedProject(unittest.TestCase):
    def setUp(self):
        self.issues = {i["number"]: i for i in json.loads((FIXTURE / ".tracker" / "issues.json").read_text())}
        self.pulls = {p["number"]: p for p in json.loads((FIXTURE / ".tracker" / "pulls.json").read_text())}

    def test_the_issues_the_scenario_and_key_name_exist_in_the_state_they_assume(self):
        self.assertEqual(self.issues[16]["state"], "OPEN")
        self.assertEqual(self.issues[17]["state"], "OPEN")
        self.assertEqual(self.issues[8]["state"], "CLOSED")
        for n in (16, 17):
            self.assertEqual(self.issues[n]["author"]["login"], "second-user")
            self.assertEqual(self.issues[n]["comments"], [], f"#{n} must be unanswered (N36)")
        self.assertIn("longer-lived", self.pulls[15]["body"])

    def test_the_quoted_remarks_are_in_issue_16(self):
        body = self.issues[16]["body"]
        self.assertIn("I liked the guidance after `./install.sh`", body)
        self.assertIn("claudism", body)

    def test_no_account_names_and_no_other_project_in_the_export(self):
        text = (FIXTURE / ".tracker" / "issues.json").read_text() + (FIXTURE / ".tracker" / "pulls.json").read_text()
        logins = set(re.findall(r'"login": "([^"]+)"', text))
        self.assertLessEqual(logins, {"owner", "second-user"})
        # the export's author objects also carried full names (run 2 of 2026-11-09): only the role stays
        for item in [*self.issues.values(), *self.pulls.values()]:
            self.assertEqual(set(item["author"]), {"login"})
        self.assertNotRegex(text, r"@(?!second-user|owner)[A-Za-z0-9-]{2,}\b(?![.@])")
        self.assertIn("[Body shortened for this fixture", self.issues[8]["body"])  # it quoted another project's paths

    def test_the_copied_instructions_are_older_than_the_readme_as_n32_says(self):
        readme = standing_instructions((REPO / "README.md").read_text())
        copy = (FIXTURE / "CLAUDE.md").read_text()
        missing = [line for line in readme if line[2:40] not in copy]
        for start in ("A pull request or release description", "When a word in a request is ambiguous",
                      "Offer a debrief", "When routing work with"):
            self.assertTrue(any(line.startswith("- " + start) for line in missing), start)
        self.assertIn("A change beyond a few hundred lines gets a review", copy)
        self.assertNotIn("code that changes files or data on its own", copy)

    def test_the_tool_that_creates_vms_is_not_in_the_copy(self):
        self.assertFalse((FIXTURE / "devvm").exists())
        self.assertFalse((FIXTURE / "install.sh").exists())

    def test_the_mit_licence_and_the_source_note_travel_with_the_copy(self):
        self.assertIn("MIT License", (FIXTURE / "LICENSE").read_text())
        self.assertIn("2649ab5", (FIXTURE / "SOURCE.md").read_text())

    def test_every_key_item_of_the_scenario_cites_an_example(self):
        rows = [r for r in (BENCH / "key.md").read_text().splitlines() if "| tracked-project |" in r]
        self.assertEqual(len(rows), 14)
        for r in rows:
            self.assertRegex(r, r"\bE\d+\b", r[:12])

    def test_the_choices_n42_protects_are_in_the_copy(self):
        self.assertIn("deliberately not committed", (FIXTURE / "design" / "requirements.md").read_text())
        self.assertIn("record open questions at the end of `spec.md`", (FIXTURE / "CLAUDE.md").read_text())


class TestTrackedSync(unittest.TestCase):
    """The scenario tracked-sync: its fixture holds what N44 to N50 assume (ledger 291)."""

    SYNC = BENCH / "scenarios" / "tracked-sync"

    def test_the_tracker_state_the_scenario_assumes(self):
        issues = {i["number"]: i for i in json.loads((self.SYNC / ".tracker" / "issues.json").read_text())}
        pulls = {p["number"]: p for p in json.loads((self.SYNC / ".tracker" / "pulls.json").read_text())}
        self.assertEqual(issues[17]["state"], "CLOSED")
        self.assertEqual(pulls[21]["state"], "MERGED")
        self.assertIn("Closes #17", pulls[21]["body"])
        self.assertEqual((issues[16]["state"], issues[16]["comments"]), ("OPEN", []))
        for item in [*issues.values(), *pulls.values()]:
            self.assertEqual(set(item["author"]), {"login"})
            self.assertIn(item["author"]["login"], {"owner", "second-user"})

    def test_the_setting_the_inbox_and_the_stale_question_are_there(self):
        claude = (self.SYNC / "CLAUDE.md").read_text()
        self.assertIn("## Issue tracker", claude)
        self.assertIn("Kaizen standing instructions, version ", claude)
        ledger = (self.SYNC / "design" / "kaizen.md").read_text()
        notes = ledger.split("## Notes for the next debrief", 1)[1]
        self.assertEqual(len(re.findall(r"^- 2026-11-09, \d\d:\d\d:", notes, re.M)), 4)
        self.assertIn("as #8 suggests", (self.SYNC / "design" / "spec.md").read_text())

    def test_every_key_item_cites_an_example_and_the_state_is_marked_invented(self):
        rows = [r for r in (BENCH / "key.md").read_text().splitlines() if "| tracked-sync |" in r]
        self.assertEqual(len(rows), 7)
        for r in rows:
            self.assertRegex(r, r"\bE\d+\b", r[:12])
        self.assertIn("Invented for this scenario", (self.SYNC / "SOURCE.md").read_text())


class TestVary(unittest.TestCase):  # item 50: varied scenarios, replayable from their seed
    def setUp(self):
        import importlib.util
        spec = importlib.util.spec_from_file_location("vary", BENCH / "vary.py")
        self.vary = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.vary)

    def test_the_same_seed_gives_the_same_scenario_and_records_its_axes(self):
        v = self.vary
        self.assertEqual(v.scenario(7, v.draw(7)), v.scenario(7, v.draw(7)))
        self.assertIn('generated by vary.py, seed 7; axes: {"project"', v.scenario(7, v.draw(7)))
        self.assertGreater(len({json.dumps(v.draw(s)) for s in range(40)}), 10)  # the seeds do vary

    def test_a_scenario_is_written_with_its_project_folder(self):
        import tempfile
        v = self.vary
        for seed in range(30):  # every project, every instruction file, a tracker among them
            axes = v.draw(seed)
            with tempfile.TemporaryDirectory() as tmp:
                md = v.write(seed, axes, Path(tmp))
                folder = md.with_suffix("")
                self.assertTrue(md.read_text().startswith(f"<!-- generated by vary.py, seed {seed}"))
                self.assertEqual((folder / "CLAUDE.md").exists(), axes["instructions"] != "none")
                self.assertEqual((folder / ".tracker" / "issues.json").exists(), axes["tracker"] != "none")
                self.assertEqual((folder / "fitpeaks.py").exists(), axes["project"] == "fitpeaks")
                self.assertFalse(axes["project"] == "empty" and axes["request"] == "try it")

    def test_a_newer_plugin_asks_for_a_review_of_the_evidence_first(self):  # item 53
        import tempfile
        v = self.vary
        self.assertEqual(v.review_notice(v.REVIEWED["version"]), "")
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            subprocess_run = __import__("subprocess").run
            subprocess_run(["git", "init", "-q", str(root)], check=True)
            (root / "design").mkdir()
            (root / "design" / "kaizen.md").write_text(
                f"- 2000-01-01, principal: old note\n- 2999-01-01, principal: a field test showed something new\n")
            notice = v.review_notice("9.9.9", root)
        self.assertIn(f"last checked against real use for {v.REVIEWED['version']}", notice)
        self.assertIn("a field test showed something new", notice)
        self.assertNotIn("old note", notice)

    def test_what_the_project_shows_is_not_held_back(self):  # the varied runs of 2026-11-19: DEPLOY.md vs "never volunteer"
        v = self.vary
        for seed in range(40):
            axes = v.draw(seed)
            text = v.scenario(seed, axes)
            never = text.split("Never volunteer:", 1)[1].split("\n", 1)[0]
            if axes["publishing"] == "deploys on push":
                self.assertIn("`DEPLOY.md` says", text.split("Never volunteer:")[0])
                self.assertNotIn("publishes", never)

    def test_generated_scenarios_stay_out_of_git(self):
        import subprocess
        r = subprocess.run(["git", "-C", str(REPO), "check-ignore", "-q", "benchmarks/plugin-newcomer/scenarios/varied-3.md"])
        self.assertEqual(r.returncode, 0)


class TestBrief(unittest.TestCase):
    def test_the_newcomer_gets_an_empty_home(self):  # ledger 315 f: every run saw the host's ~/.claude/CLAUDE.md
        import subprocess
        import sys
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            scratch = Path(tmp) / "run"
            r = subprocess.run([sys.executable, str(BENCH / "brief.py"), "existing-tool", "--scratch", str(scratch)],
                               capture_output=True, text=True)
            self.assertEqual(r.returncode, 0, r.stderr)
            self.assertTrue((scratch / "home").is_dir())
            self.assertEqual(list((scratch / "home").iterdir()), [])
            self.assertIn(f"HOME={scratch}/home", r.stdout)


if __name__ == "__main__":
    unittest.main()
