# Runbook: field test of kaizen in devvm

You test the plugin by using it in devvm. Everything runs on the host unless it says "in the VM". `S` is this repository (`~/src/skills`), `F` the scratch folder `~/field-test` (`record.sh` asks before creating it).

Two variants:
- **Variant 1, repeatable** (the maintainer, testing changes to the plugin): a fixed starting state, reset after each run. Your own devvm checkout and VMs are never touched.
- **Variant 2, real work** (a colleague, or the maintainer's last run): their own checkout and VM, only the recording and notes added; nothing is reset.

## Variant 1

### Run 0: the starting state, once

```
S/design/field-tests/record.sh                    # asks to create F, records run-0
git clone https://github.com/modama-rdm/devvm F/work/devvm
cd F/work/devvm
devvm use devvm-field && devvm create             # a VM of its own, with F/work/devvm mounted
devvm setup-dev                                    # as you normally set up a devvm VM; log in to Claude
```
Bring VM and working copy into the state you want each run to start from (for this test: the released kaizen, before the update). Then:
```
devvm -n devvm-field stop
cp -a F/work F/master                              # the master copy of the working copy
devvm -n devvm-field snapshot field-start
exit                                               # ends the recording
```

### Each run

```
S/design/field-tests/record.sh                    # run-<n>, with F/run-<n>/notes.md
devvm -n devvm-field reset field-start
devvm -n devvm-field ssh                           # in the VM, in the checkout:
  claude plugin marketplace remove uellue
  claude plugin marketplace add uellue/skills#field-tests-269
  claude plugin install kaizen@uellue --scope user
  claude                                           # then follow S/design/field-tests/devvm-brief.md
```
When you are done, still in the VM, in the checkout:
```
  t=$(find ~/.claude/plugins -name transcript.py -path '*kaizen*' | head -1)
  python3 "$t" locate                              # note the session id
  python3 "$t" export <id>                         # into the checkout, which the host keeps
  exit                                             # leaves the VM
devvm -n devvm-field stop
mv F/work F/run-<n>/work                           # this run's working copy, kept as evidence
cp -a F/master F/work                              # the next run starts from the master again
exit                                               # ends the recording
S/design/field-tests/record.sh --pack <n>          # F/run-<n>.tar.gz
```
Tell me here: the run number. The testing VMs a run created: `devvm ls -a`, then `devvm -n <name> destroy`.

## Variant 2

In the terminal you will work in, before anything else:
```
S/design/field-tests/record.sh                    # (a colleague gets the script with the brief)
```
Then work on devvm as you normally would, in your own checkout and VM, with `devvm-brief.md` beside you. At the end, in the VM, in your checkout, export the session as in variant 1 (the `find`, `locate`, `export` lines), copy `.claude/transcripts/<id>` into `F/run-<n>/`, `exit`, then `record.sh --pack <n>` and send the archive (a colleague: as an attachment to an issue in the private repository, after looking through it).

## Why it is done this way

- The recording runs on the host, so it also covers the VM; output and timing only, never keystrokes.
- Variant 1: the snapshot resets everything inside the VM (plugin, the agent's memory, settings); the working copy comes from the host, so it is reset by copying the master; the VM is stopped while it changes. Whether devvm's reset boots the VM so that it sees the new copy was not checked.
- The session is exported into the checkout because the reset would erase it inside the VM.
- Nothing is deleted: every run's folder keeps its recording, notes, working copy and session.
- Layers and the reasons in full: `design/walkthroughs/maintainer-field-test-devvm.md`.
