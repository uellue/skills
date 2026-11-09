# Runbook: field test of kaizen in devvm

You test the plugin by using it in devvm. Everything below runs on the host unless it says "in the VM". `S` is this repository (`~/src/skills`), `D` the folder the VM `devvm-snapshots` shares with the host.

## Once

```
S/design/field-tests/record.sh            # starts recording (run-0); type exit at the end
devvm ls -a                               # find devvm-snapshots and its shared folder: that is D
devvm -n devvm-snapshots snapshot field-start
touch ~/field-test-notes.md               # your notes file
exit
```

## Each run

1. Start recording: `S/design/field-tests/record.sh`
2. Put a fresh devvm into `D` (with the VM stopped: it may keep seeing the old folder otherwise; not checked):
   ```
   devvm -n devvm-snapshots stop
   mv D ~/field-test/previous-devvm-$(date +%s)    # only if D holds an earlier run's clone
   git clone https://github.com/modama-rdm/devvm D
   echo /.claude/transcripts/ >> D/.git/info/exclude
   devvm -n devvm-snapshots start
   ```
3. In the VM (`devvm -n devvm-snapshots ssh`), install the test version:
   ```
   claude plugin marketplace remove uellue          # if present
   claude plugin marketplace add uellue/skills#field-tests-269
   claude plugin install kaizen@uellue --scope user
   claude plugin list                               # shows the version
   ```
4. In the VM, in the checkout: `claude`. From here, follow `S/design/field-tests/devvm-brief.md`.
5. When you are done, still in the VM, in the checkout:
   ```
   t=$(find ~/.claude/plugins -name transcript.py -path '*kaizen*' | head -1)
   python3 "$t" locate              # note the session id
   python3 "$t" export <id>
   exit                             # leave the VM
   exit                             # end the recording
   ```
6. Tell me here: the run number, the session id. I take it from there.

## Reset (only for testing the plugin, never in normal use)

```
devvm -n devvm-snapshots reset field-start
devvm ls -a                       # destroy the testing VMs this run created: devvm -n <name> destroy
```

Then the next run, from step 1. Nothing is deleted: recordings, notes and old clones stay in `~/field-test/`.

## The last run, kept

Skip the reset. In the brief, the rule "nothing goes upstream" does not apply. `D` stays devvm's working checkout.

## Why it is done this way

- The recording runs on the host, so it also covers the VM; output and timing only, never keystrokes.
- The snapshot resets everything inside the VM (plugin, the agent's memory, settings); the git tree comes from the host, hence the fresh clone.
- The session is exported into `D` because the reset would erase it inside the VM.
- Layers and the reasons in full: `design/walkthroughs/maintainer-field-test-devvm.md`.
