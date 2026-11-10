"""Checks of the plugin's eval suite (plugins/kaizen/evals/, ledger 214)."""

import unittest
from pathlib import Path

EVALS = Path(__file__).resolve().parents[1] / "plugins" / "kaizen" / "evals"


class Evals(unittest.TestCase):
    def test_fixture_copies_are_identical(self):
        # A scaffold script must sit in its case's directory, so every case carries a copy. Copies are identical
        # within a suite (triggers and walkthrough share one, every other folder has its own); the update cases
        # differ only in their VERSION_LINE, which is what they test (ledger 280).
        def text(p):
            return "".join(l for l in p.read_text().splitlines(keepends=True) if not l.startswith("VERSION_LINE="))
        suites = {}
        for p in sorted(EVALS.glob("*/*/fixture.sh")):
            suites.setdefault("tally" if p.parts[-3] in ("triggers", "walkthrough") else p.parts[-3], []).append(p)
        self.assertGreater(len(suites["tally"]), 1)
        for name, copies in suites.items():
            for copy in copies[1:]:
                with self.subTest(name):
                    self.assertEqual(text(copy), text(copies[0]), f"{copy} differs from {copies[0]}")


if __name__ == "__main__":
    unittest.main()
