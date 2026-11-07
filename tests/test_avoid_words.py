"""The report of glossary words to avoid in added lines (ledger 229), on synthetic text."""

import unittest

from avoid_words import flags, glossary, split_top

GLOSSARY = """**Subject**:
What a hallway test judges.
_Avoid_: target, the thing (it reads as the real thing)

**Use scenario**:
A situation of use.
_Avoid_: scenario (unqualified), use case

**Revisit**:
Kept for later, with a trigger.
_Avoid_: BF, "later" without a trigger
"""


class TestAvoidWords(unittest.TestCase):
    def setUp(self):
        self.terms, self.avoid = glossary(GLOSSARY)

    def test_parses_the_avoid_lists(self):
        self.assertEqual(self.avoid, {"target", "the thing", "scenario", "use case", "bf", "later"})
        self.assertIn("use scenario", self.terms)

    def test_reports_the_slip_of_2026_11_07(self):
        self.assertEqual(flags("once the thing exists and is being polished", self.terms, self.avoid), ["the thing"])

    def test_skips_backticks_and_glossary_terms(self):
        self.assertEqual(flags("the use scenario names the `target` dir", self.terms, self.avoid), [])
        self.assertEqual(flags("a scenario, unqualified", self.terms, self.avoid), ["scenario"])

    def test_a_quote_inside_the_explanation_is_not_the_word(self):  # review 7, GLOSSARY.md "kaizen file"
        _, avoid = glossary('_Avoid_: kaizen file (as its name: "backlog" is the project\'s own list)\n')
        self.assertEqual(avoid, {"kaizen file"})

    def test_commas_inside_parentheses_do_not_split(self):
        self.assertEqual(split_top("a (b, c), d"), ["a (b, c)", " d"])


if __name__ == "__main__":
    unittest.main()
