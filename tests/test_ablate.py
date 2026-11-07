"""Tests for benchmarks/rule-ablation/ablate.py on a synthetic plugin (ledger 204, 214)."""

import importlib.util
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("ablate", ROOT / "benchmarks" / "rule-ablation" / "ablate.py")
ablate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ablate)


class Ablate(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.plugin = self.tmp / "plugin"
        (self.plugin / "skills" / "s").mkdir(parents=True)
        (self.plugin / "evals" / "results").mkdir(parents=True)
        (self.plugin / "evals" / "results" / "old.json").write_text("{}")
        (self.plugin / "skills" / "s" / "SKILL.md").write_text("Keep this. Drop this. Keep that.")

    def variant(self, remove):
        return {"id": "v", "file": "skills/s/SKILL.md", "remove": remove}

    def test_removes_once_and_leaves_the_original(self):
        out = ablate.ablate(self.variant(" Drop this."), self.plugin, self.tmp / "copy")
        self.assertEqual((out / "skills/s/SKILL.md").read_text(), "Keep this. Keep that.")
        self.assertEqual((self.plugin / "skills/s/SKILL.md").read_text(), "Keep this. Drop this. Keep that.")
        self.assertFalse((out / "evals" / "results").exists())

    def test_text_must_occur_exactly_once(self):
        for remove in ("Missing.", "Keep th"):
            with self.assertRaises(SystemExit):
                ablate.ablate(self.variant(remove), self.plugin, self.tmp / f"copy-{len(remove)}")

    def test_never_writes_into_an_existing_directory(self):
        (self.tmp / "taken").mkdir()
        with self.assertRaises(SystemExit):
            ablate.ablate(self.variant(" Drop this."), self.plugin, self.tmp / "taken")

    def test_every_shipped_variant_matches_the_plugin_once(self):
        for v in ablate.load().values():
            text = (ablate.PLUGIN / v["file"]).read_text()
            self.assertEqual(text.count(v["remove"]), 1, v["id"])


if __name__ == "__main__":
    unittest.main()
