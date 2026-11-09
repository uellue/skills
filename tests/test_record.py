"""design/field-tests/record.sh: the next run folder, and the recording command it starts (ledger 269, E38)."""

import os
import stat
import subprocess
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "design" / "field-tests" / "record.sh"


class TestRecord(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.base = Path(self.tmp.name) / "field-test"
        bindir = Path(self.tmp.name) / "bin"
        bindir.mkdir()
        # a stand-in for util-linux script that writes down its arguments instead of recording
        fake = bindir / "script"
        fake.write_text('#!/bin/sh\nprintf "%s\\n" "$@" > "$FAKE_ARGS"\n')
        fake.chmod(fake.stat().st_mode | stat.S_IEXEC)
        self.args = Path(self.tmp.name) / "args"
        self.env = {**os.environ, "FIELD_TEST_DIR": str(self.base), "PATH": f"{bindir}:{os.environ['PATH']}",
                    "FAKE_ARGS": str(self.args)}

    def tearDown(self):
        self.tmp.cleanup()

    def run_record(self, *args):
        return subprocess.run(["bash", str(SCRIPT), *args], env=self.env, capture_output=True, text=True)

    def test_first_is_run_0_then_it_counts_up_past_gaps_and_odd_names(self):
        self.assertEqual(self.run_record("--next").stdout.strip(), str(self.base / "run-0"))
        self.assertFalse(self.base.exists(), "--next must not create anything")
        for name in ("run-0", "run-2", "run-x", "run-"):
            (self.base / name).mkdir(parents=True)
        self.assertEqual(self.run_record("--next").stdout.strip(), str(self.base / "run-3"))

    def test_it_records_output_and_timing_only_into_a_new_folder(self):
        r = self.run_record()
        self.assertEqual(r.returncode, 0, r.stderr)
        run = self.base / "run-0"
        self.assertTrue(run.is_dir())
        self.assertEqual(self.args.read_text().split("\n")[:5],
                         ["-q", "-T", str(run / "timing.log"), "-O", str(run / "session.log")])
        self.assertNotIn("--log-in", self.args.read_text())
        self.assertNotIn("-I", self.args.read_text().split("\n"))
        self.assertEqual(self.run_record("--next").stdout.strip(), str(self.base / "run-1"))

    def test_unknown_arguments_are_refused(self):
        self.assertEqual(self.run_record("now").returncode, 2)


if __name__ == "__main__":
    unittest.main()
