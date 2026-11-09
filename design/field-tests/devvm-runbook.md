# Runbook: field test of kaizen 0.6.0-dev.1 in devvm, variant 1 (kaizen on kaizen)

For the maintainer. From the walk-through `design/walkthroughs/maintainer-field-test-devvm.md` (its answers, 2026-11-09). Layers: **L1** this repository; **L2** the plugin; **L3** devvm and its session, where you play the inner role from `devvm-brief.md`; **L4** what devvm creates (the VM `devvm-snapshots`, where the session runs, and its testing VMs). How to test devvm itself is not here: the plugin must guide that.

## Recording, always first

Every part below starts in a terminal on the host with `design/field-tests/record.sh` from this repository, before anything else, and ends with `exit`. It records into the next free `~/field-test/run-<n>` (`run-0` the first time, which is the once-only part; `record.sh --next` shows the folder without starting), with util-linux `script`, output and timing only: never `--log-in`, which records every key, passwords included. Outside devvm, so it survives the reset. `devvm ssh` runs inside it, so the VM side is recorded too. It records what the transcript cannot (the commands outside Claude, their output, the timing) and tests the method a colleague will use (variant 2); the Claude session's own record stays its transcript (step 7), since Claude's full-screen interface makes the recording large and hard to read; whether it is still useful for the session is one of the run's findings.

## Once, before the first run (recorded as run-0)

1. **L4, find the VM and its checkout.** On the host: `devvm ls -a`. Note which host folder `devvm-snapshots` shares (`/workspaces/<folder>` in the VM). That folder is the run's checkout below.
2. **L4, baseline snapshot.** Before kaizen 0.6.0-dev.1 is in the VM: `devvm -n devvm-snapshots snapshot field-start` (or `-u field-start` to refresh it). It holds the VM's plugin install, the agent's memory, the VM's `~/.claude/CLAUDE.md` and everything else inside the VM.
3. **L1, the notes file.** On the host, outside devvm: `~/field-test-notes.md`, so it survives every reset.

## Each run

3a. **Recording:** `record.sh` (see "Recording, always first"); every step below in that terminal, `exit` after step 7. The reset (steps 9 to 11) is recorded too, as part of the next run's recording or of its own.

4. **L3, the checkout.** On the host, a fresh clone of devvm's `main` in the folder the VM shares (or a new folder the VM is pointed at with `devvm use`). Record its commit in L1: tell me, or add a line `run <n>: devvm <commit>` to the notes file. Then, for the hand-back only: `echo /.claude/transcripts/ >> <clone>/.git/info/exclude` (nothing else is ignored for the run, so that what the plugin itself sets up is still visible).
5. **L2, install the branch inside the VM.** `devvm -n devvm-snapshots ssh`, then:
   `claude plugin marketplace remove uellue` (if present; it also uninstalls kaizen there),
   `claude plugin marketplace add uellue/skills#field-tests-269`,
   `claude plugin install kaizen@uellue --scope user`,
   `claude plugin list` (expect 0.6.0-dev.1, or the newer dev version this repository names).
6. **L3, the run.** In the VM, in the checkout: `claude`, then follow `design/field-tests/devvm-brief.md` (a copy is in this repository; read it as the inner role, nothing else). Notes about the plugin go to `~/field-test-notes.md` on the host.
7. **L3 to L1, handing back.** Before anything is reset:
   - in the VM, in the checkout: `t=$(find ~/.claude/plugins -name transcript.py -path '*kaizen*' | head -1); python3 "$t" locate` lists the sessions of this checkout with their ids; `python3 "$t" export <id>` writes the run's session into the checkout's `.claude/transcripts/<id>/`, which the host sees (ignored by git since step 4; the script refuses otherwise). Where the plugin is installed inside `~/.claude/plugins/` was not checked, hence the `find`.
   - `exit` the recording (step 3a); look through `session.log` for anything private first.
   - tell me here: the run number, the session id, the checkout's path on the host, the recording's folder, anything posted (nothing, in a churn run).

## Here, after each run (L1, with me)

8. I read the exported session, your notes and the checkout's diff; grade against N32 to N50 and the walk's E38 to E41; check row 292 (did the plugin walk the inner role through environment, roles, what runs where); findings go to the ledger by layer: the plugin (fix here), devvm (a draft for devvm's tracker, for the run that is kept), the field-test method. Fixes, then the version raised (0.6.0-dev.2, …) and pushed, so that step 5 brings them.

## Reset for the next run (kaizen on kaizen only; never part of normal plugin use)

9. **L4:** `devvm -n devvm-snapshots reset field-start` (the VM back to before the plugin was installed). Testing VMs the run created: list with `devvm ls -a`, destroy the run's own with `devvm -n <name> destroy`.
10. **L3:** the run's clone stays, named after its run (e.g. `~/field-test/run-<n>-devvm`), with its exported session; the next run gets a fresh clone (step 4). Everything a run leaves (clone, recording, notes) is kept: it is real-world evidence of kaizen on kaizen (principal, 2026-11-09). Nothing in this runbook deletes it.
11. Then from step 4.

## The last run: turning it into variant 2

12. Decide before step 6 of that run. Drop the rule "nothing goes upstream" from the brief for it; skip the reset; the clone becomes devvm's working checkout (push its branch, open the pull request the plugin drafts). The material still comes here (step 7) for the analysis.
