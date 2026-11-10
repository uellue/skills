"""plugins/kaizen/evals/scan_lists.py: replies in markdown numbered-list syntax in stored eval results (principal
2026-11-10: a display renumbers such lists, so answers by number went to the wrong items; items are "- **7**")."""

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "plugins" / "kaizen" / "evals" / "scan_lists.py"


def result(folder: Path, replies: dict):
    """An aggregate-result.json with one case per name, one run per reply, the reply as a grader's evidence."""
    folder.mkdir(parents=True)
    cases = [{"dir": f"evals/x/{name}", "arms": {"with": [{"graders": [{"name": "g", "evidence": text}]}]}}
             for name, text in replies.items()]
    (folder / "aggregate-result.json").write_text(json.dumps({"cases": cases}))


class TestScanLists(unittest.TestCase):
    def scan(self, *folders):
        r = subprocess.run([sys.executable, str(SCRIPT), *map(str, folders)], capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stderr)
        return r.stdout

    def test_list_syntax_is_reported_with_gaps_and_bold_labels_are_not(self):
        with tempfile.TemporaryDirectory() as d:
            f = Path(d) / "20261110-1-sync"
            result(f, {
                "gaps": "Open:\n17. review\n18. push\n35. hallway",
                "plain": "Steps:\n1. a\n2. b",
                "labels": "Open:\n- **17** review\n- **35** hallway",
                "fenced": "```\n1. copied\n2. list\n```",
            })
            out = self.scan(f)
        self.assertIn("x/gaps", out)
        self.assertIn("gaps: shown renumbered", out)
        self.assertIn("x/plain", out)
        self.assertNotIn("x/labels", out)
        self.assertNotIn("x/fenced", out)
        self.assertIn("2 of 4 replies in list syntax", out)

    def test_a_folder_without_results_is_skipped(self):
        with tempfile.TemporaryDirectory() as d:
            (Path(d) / "empty").mkdir()
            self.assertIn("0 of 0 replies", self.scan(Path(d) / "empty"))


if __name__ == "__main__":
    unittest.main()
