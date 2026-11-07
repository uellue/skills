"""Checks of the plugin's eval suite (plugins/kaizen/evals/, ledger 214)."""

import unittest
from pathlib import Path

EVALS = Path(__file__).resolve().parents[1] / "plugins" / "kaizen" / "evals"


class Evals(unittest.TestCase):
    def test_fixture_copies_are_identical(self):
        # A scaffold script must sit in its case's directory, so each walkthrough case carries a copy.
        copies = sorted(EVALS.glob("walkthrough/*/fixture.sh"))
        self.assertGreater(len(copies), 1)
        first = copies[0].read_text()
        for copy in copies[1:]:
            self.assertEqual(copy.read_text(), first, f"{copy} differs from {copies[0]}")


if __name__ == "__main__":
    unittest.main()
