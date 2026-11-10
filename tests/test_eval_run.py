"""plugins/kaizen/evals/run.py: a stretch's eval budget, enforced before each run (principal 2026-11-10: "Standing
instructions didn't work too well regarding budget"; 325 runs, $96.74 in one day hit the session limit)."""

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "plugins" / "kaizen" / "evals" / "run.py"


class TestEvalRun(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        t = Path(self.tmp.name)
        self.results = t / "results"
        bindir = t / "bin"
        bindir.mkdir()
        # a stand-in for claude: records its arguments and PATH, writes a result costing $COST into --output-dir
        fake = bindir / "claude"
        fake.write_text(
            "#!/usr/bin/env python3\n"
            "import json, os, sys, time\n"
            "a = sys.argv[1:]\n"
            "time.sleep(float(os.environ.get('FAKE_SLEEP', '0')))\n"
            "out = a[a.index('--output-dir') + 1]\n"
            "open(os.environ['FAKE_ARGS'], 'w').write(json.dumps({'args': a, 'path': os.environ['PATH']}))\n"
            "json.dump({'costUsd': float(os.environ.get('COST', '1.5'))}, open(os.path.join(out, 'aggregate-result.json'), 'w'))\n"
            "print('CASE  SCORE')\n"
        )
        fake.chmod(0o755)
        self.args = t / "args.json"
        self.env = {**os.environ, "PATH": f"{bindir}:{os.environ['PATH']}", "FAKE_ARGS": str(self.args),
                    "KAIZEN_EVAL_RESULTS": str(self.results), "KAIZEN_EVAL_CLAUDE": str(fake)}

    def tearDown(self):
        self.tmp.cleanup()

    def run_it(self, *args, **env):
        return subprocess.run([sys.executable, str(SCRIPT), *args], env={**self.env, **env}, capture_output=True, text=True)

    def test_a_run_needs_a_stretch_and_a_cost_ceiling(self):
        r = self.run_it("sync", "--case", "sync-*")
        self.assertEqual(r.returncode, 2)
        self.assertIn("--new-stretch", r.stderr)
        self.run_it("--new-stretch")
        r = self.run_it("sync", "--case", "sync-*")
        self.assertEqual(r.returncode, 2)
        self.assertIn("--max-cost-usd", r.stderr)

    def test_the_default_budget_is_20_and_the_reserve_a_quarter(self):
        r = self.run_it("--new-stretch")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("$20.00", r.stdout)
        self.assertIn("$15.00", r.stdout)  # runs stop at three quarters

    def test_it_runs_with_the_system_python_first_and_its_own_output_folder(self):
        self.run_it("--new-stretch", "10")
        r = self.run_it("sync", "--case", "sync-*", "--max-cost-usd", "2")
        self.assertEqual(r.returncode, 0, r.stderr)
        seen = json.loads(self.args.read_text())
        self.assertEqual(seen["args"][:3], ["plugin", "eval", str(ROOT / "plugins" / "kaizen")])
        self.assertIn("--max-cost-usd", seen["args"])
        self.assertTrue(seen["path"].startswith("/usr/bin:"), seen["path"])
        out = Path(seen["args"][seen["args"].index("--output-dir") + 1])
        self.assertEqual(out.parent, self.results)
        self.assertTrue(out.name.endswith("-sync"))
        self.assertTrue((out / "run.log").is_file())
        self.assertIn("spent $1.50 of $10.00", r.stdout)
        self.assertIn("replies in list syntax", r.stdout)  # the scan runs after each run (scan_lists.py)

    def test_it_refuses_a_run_that_could_pass_the_reserve(self):
        self.run_it("--new-stretch", "10")  # reserve: runs stop at $7.50
        self.assertEqual(self.run_it("a", "--max-cost-usd", "3", COST="4").returncode, 0)
        r = self.run_it("b", "--max-cost-usd", "4")  # $4 spent + up to $4 > $7.50
        self.assertEqual(r.returncode, 3)
        self.assertIn("$4.00", r.stderr)
        self.assertIn("$7.50", r.stderr)
        self.assertEqual(self.run_it("c", "--max-cost-usd", "3").returncode, 0)  # $4 + $3 fits

    def test_only_runs_since_the_stretch_began_count(self):
        self.run_it("--new-stretch", "10")
        self.run_it("a", "--max-cost-usd", "3", COST="5")
        self.run_it("--new-stretch", "10", "--force")
        r = self.run_it("--status")
        self.assertIn("spent $0.00 of $10.00", r.stdout)

    def test_a_new_stretch_does_not_silently_replace_one_with_spend(self):
        # review of 2026-11-10, M3: after a refusal, --new-stretch would start again at $0
        self.run_it("--new-stretch", "10")
        self.run_it("a", "--max-cost-usd", "3", COST="5")
        r = self.run_it("--new-stretch", "10")
        self.assertEqual(r.returncode, 3)
        self.assertIn("$5.00", r.stderr)
        r = self.run_it("--new-stretch", "10", "--force")  # the person's decision; the old stretch is kept
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertTrue(list(self.results.glob(".stretch-*.json")))

    def test_a_corrupt_stretch_file_is_an_error_not_a_fresh_start(self):
        self.run_it("--new-stretch", "10")
        (self.results / ".stretch.json").write_text('{"start": "x", "budget": 10')
        r = self.run_it("a", "--max-cost-usd", "1")
        self.assertEqual(r.returncode, 2)
        self.assertIn("corrupt", r.stderr)

    def test_numbers_and_labels_are_checked(self):
        # review L1, L2: a negative or non-finite ceiling, a label that leaves the results folder
        self.run_it("--new-stretch", "10")
        for bad in ("-50", "nan", "inf", "x"):
            self.assertEqual(self.run_it("a", "--max-cost-usd", bad).returncode, 2, bad)
        self.assertEqual(self.run_it("a", "--max-cost-usd").returncode, 2)
        for label in ("sync/x", "../up", ".."):
            self.assertEqual(self.run_it(label, "--max-cost-usd", "1").returncode, 2, label)
        self.assertEqual(self.run_it("--new-stretch", "nan", "--force").returncode, 2)

    def test_an_older_plugin_runs_within_the_same_stretch(self):
        # review M2: the comparison with an older version must not bypass the budget
        self.run_it("--new-stretch", "10")
        old = Path(self.tmp.name) / "old-kaizen"
        old.mkdir()
        r = self.run_it("old", "--plugin", str(old), "--max-cost-usd", "2")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual(json.loads(self.args.read_text())["args"][2], str(old))
        self.assertIn("spent $1.50 of $10.00", r.stdout)

    def test_parallel_runs_cannot_pass_the_reserve_together(self):
        # review M1: three parallel runs of $3 under a $7.50 limit all ran
        self.run_it("--new-stretch", "10")
        procs = [subprocess.Popen([sys.executable, str(SCRIPT), f"p{i}", "--max-cost-usd", "3"],
                                  env={**self.env, "COST": "3", "FAKE_SLEEP": "1"}, stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE, text=True) for i in range(3)]
        codes = sorted(p.wait() for p in procs)
        self.assertEqual(codes, [0, 0, 3])
        self.assertIn("spent $6.00", self.run_it("--status").stdout)

    def test_the_output_folder_is_the_wrappers_own(self):
        self.run_it("--new-stretch")
        r = self.run_it("x", "--max-cost-usd", "1", "--output-dir", "/tmp/elsewhere")
        self.assertEqual(r.returncode, 2)


if __name__ == "__main__":
    unittest.main()
