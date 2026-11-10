"""plugins/kaizen/scripts/record.sh: the next run folder, and the recording command it starts (ledger 269, E38)."""

import os
import stat
import subprocess
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "plugins" / "kaizen" / "scripts" / "record.sh"


class TestRecord(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.base = Path(self.tmp.name) / "field-test"
        bindir = Path(self.tmp.name) / "bin"
        bindir.mkdir()
        # a stand-in for util-linux script that writes down its arguments instead of recording
        fake = bindir / "script"
        fake.write_text('#!/bin/sh\nprintf "%s\\n" "$@" > "$FAKE_ARGS"\necho "$FIELD_TEST_RUN" > "$FAKE_ARGS.run"\numask > "$FAKE_ARGS.umask"\n')
        fake.chmod(fake.stat().st_mode | stat.S_IEXEC)
        self.args = Path(self.tmp.name) / "args"
        self.env = {**os.environ, "FIELD_TEST_DIR": str(self.base), "PATH": f"{bindir}:{os.environ['PATH']}",
                    "FAKE_ARGS": str(self.args)}

    def tearDown(self):
        self.tmp.cleanup()

    def run_record(self, *args, answer="y\n"):
        return subprocess.run(["bash", str(SCRIPT), *args], env=self.env, capture_output=True, text=True, input=answer)

    def test_it_asks_before_creating_the_scratch_folder(self):
        r = self.run_record(answer="n\n")
        self.assertEqual(r.returncode, 1)
        self.assertFalse(self.base.exists())
        self.assertIn("folder for field-test runs", r.stdout)
        r = self.run_record(answer="")  # no terminal, no answer: nothing created
        self.assertFalse(self.base.exists())
        self.assertEqual(self.run_record().returncode, 0)
        self.assertTrue((self.base / "run-0" / "notes.md").is_file())
        r = self.run_record(answer="n\n")  # asked only the first time
        self.assertEqual(r.returncode, 0, r.stdout)
        self.assertTrue((self.base / "run-1").is_dir())

    def test_pack_makes_one_archive_and_never_overwrites(self):
        self.run_record()
        (self.base / "run-0" / "session.log").write_text("x\n")
        r = self.run_record("--pack", "0")
        self.assertEqual(r.returncode, 0, r.stderr)
        archive = self.base / "run-0.tar.gz"
        listing = subprocess.run(["tar", "-tzf", str(archive)], capture_output=True, text=True).stdout.split()
        self.assertIn("run-0/session.log", listing)
        self.assertIn("run-0/notes.md", listing)
        self.assertEqual(self.run_record("--pack", "0").returncode, 1)
        self.assertEqual(self.run_record("--pack", "7").returncode, 1)
        self.run_record()  # run-1
        self.assertEqual(self.run_record("--pack").returncode, 0)  # the latest by default
        self.assertTrue((self.base / "run-1.tar.gz").is_file())
        self.assertEqual(self.run_record("--pack", "x").returncode, 2)

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
        self.assertEqual(self.args.read_text().split("\n")[:6],
                         ["-q", "-f", "-T", str(run / "timing.log"), "-O", str(run / "session.log")])
        self.assertNotIn("--log-in", self.args.read_text())
        self.assertEqual(Path(str(self.args) + ".run").read_text().strip(), str(run))  # FIELD_TEST_RUN in the shell
        self.assertNotIn("-I", self.args.read_text().split("\n"))
        self.assertEqual(self.run_record("--next").stdout.strip(), str(self.base / "run-1"))

    def test_the_run_and_its_archive_are_private_to_the_owner(self):
        # review of 2026-11-10: on a shared machine, a recording readable by others leaks what the terminal showed
        # and the recorded shell keeps the person's own umask (review of 2026-11-10, H1: a umask of 077 there made
        # every file of the session owner-only, which changes the setting under test)
        r = subprocess.run(["bash", "-c", f"umask 0022; exec bash {SCRIPT}"], env=self.env, capture_output=True,
                           text=True, input="y\n")
        self.assertEqual(r.returncode, 0, r.stderr)
        run = self.base / "run-0"
        self.assertEqual(stat.S_IMODE(run.stat().st_mode), 0o700, oct(run.stat().st_mode))
        self.assertEqual(Path(str(self.args) + ".umask").read_text().strip(), "0022")  # the session's own umask
        self.run_record("--pack")
        self.assertEqual(stat.S_IMODE((self.base / "run-0.tar.gz").stat().st_mode) & 0o077, 0)

    def test_a_relative_folder_gives_an_absolute_run_path(self):
        # review of 2026-11-10, L5: FIELD_TEST_RUN must stay valid after a cd in the recorded shell
        self.env["FIELD_TEST_DIR"] = "ft"
        r = subprocess.run(["bash", str(SCRIPT)], env=self.env, capture_output=True, text=True, input="y\n",
                           cwd=self.tmp.name)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual(Path(str(self.args) + ".run").read_text().strip(), str(Path(self.tmp.name) / "ft" / "run-0"))

    def test_unknown_arguments_are_refused(self):
        self.assertEqual(self.run_record("now").returncode, 2)


if __name__ == "__main__":
    unittest.main()
