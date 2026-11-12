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


if __name__ == "__main__":
    unittest.main()
