# Runbook: field test of kaizen in devvm

You test the plugin by using it in devvm. Everything runs on the host unless it says "in the VM".

Two variants:
- **Variant 1, repeatable** (the maintainer, testing changes to the plugin): a fixed starting state, copied once from your VM and checkout, reset after each run. Your own checkout is only read; your VM is shut off once while it is copied, and otherwise never touched.
- **Variant 2, real work** (a colleague, or the maintainer's last run): their own checkout and VM, only the recording and notes added; nothing is reset.

## In every new terminal on the host, first

```
export SKILLS="$HOME/src/skills"                 # this repository
export FIELD_TEST_DIR="$HOME/field-test"         # the scratch folder; record.sh asks before creating it
export VM=devvm-field                            # variant 1's VM
```

Inside a recording, `$FIELD_TEST_RUN` is the run's folder (`$FIELD_TEST_DIR/run-<n>`), set by `record.sh`.

## Variant 1

### Run 0: the starting state, once

A copy of your VM `devvm-snapshots` and of its checkout, as they are. Your VM is shut off while they are copied (its disk is about 70 GiB).
```
export ORIG=devvm-snapshots
export ORIG_CHECKOUT="$HOME/src/devvm"                          # what it shares: virsh metadata "$ORIG" --uri https://devvm.invalid/1 --key devvm
export POOL=/cachedata/weber/libvirt                            # DEVVM_POOL_DIR in ~/.config/devvm/site.env
export LIBVIRT_DEFAULT_URI=qemu:///system
"$SKILLS"/design/field-tests/record.sh                          # asks to create the folder, records run-0
devvm -n "$ORIG" stop
mkdir "${FIELD_TEST_DIR:?}"/work
cp -a "${ORIG_CHECKOUT:?}" "${FIELD_TEST_DIR:?}"/work/devvm     # same folder name: the VM sees it at /workspaces/devvm
PATH=/usr/bin:$PATH virt-clone --original "$ORIG" --name "$VM" --file "${POOL:?}/$VM.qcow2"
devvm -n "$ORIG" start                                          # your VM is free again
cp -a "${POOL:?}/$ORIG.hostkey" "${POOL:?}/$VM.hostkey"         # the clone has the same host key; devvm writes
cp -a "${POOL:?}/$ORIG.hostkey.pub" "${POOL:?}/$VM.hostkey.pub" #   $VM.known_hosts from it by itself
```
Point the copy's shared folder at the working copy, and the working copy at the copy's VM:
```
PATH=/usr/bin:$PATH virt-xml "$VM" --edit target=devvm-ws --filesystem source.dir="${FIELD_TEST_DIR:?}"/work/devvm
virsh metadata "$VM" --uri https://devvm.invalid/1 --key devvm --config \
  --set "<workspace host=\"${FIELD_TEST_DIR:?}/work/devvm\" guest=\"/workspaces/devvm\"/>"
cd "${FIELD_TEST_DIR:?}"/work/devvm && devvm use "$VM"          # the copy said devvm-snapshots
devvm status                                                    # VM: devvm-field; the workspace: the working copy
virsh dumpxml "$VM" | grep -B2 devvm-ws                         # source dir: the working copy
virsh snapshot-list "$VM"                                       # expected empty; if not, stop and tell me
qemu-img info "${POOL:?}/$VM.qcow2" | grep -i 'backing\|disk size'   # for the research note
```
Then start it, `devvm -n "$VM" ssh`, and check that the state is the one each run should start from (for this test: the released kaizen, before the update; `claude plugin list`). Back on the host:
```
devvm -n "$VM" stop
cp -a "${FIELD_TEST_DIR:?}"/work "${FIELD_TEST_DIR:?}"/master  # the master copy of the working copy
devvm -n "$VM" snapshot field-start
exit                                                            # ends the recording
```
Never revert the snapshots `clean`, `dev`, `dev2` on the copy if they show up there: they would share your real checkout again (`design/research/vm-clone.md`).

### Each run

```
"$SKILLS"/design/field-tests/record.sh                          # run-<n>, with $FIELD_TEST_RUN/notes.md
devvm -n "$VM" reset field-start
devvm -n "$VM" ssh                                              # in the VM, in the checkout:
  claude plugin marketplace remove uellue
  claude plugin marketplace add uellue/skills#field-tests-269
  claude plugin install kaizen@uellue --scope user
  claude                                                        # then follow $SKILLS/design/field-tests/devvm-brief.md
```
When you are done, still in the VM, in the checkout:
```
  t=$(find ~/.claude/plugins -name transcript.py -path '*kaizen*' | head -1)
  python3 "$t" locate                                           # note the session id
  python3 "$t" export <id>                                      # into the checkout, which the host keeps
  exit                                                          # leaves the VM
devvm -n "$VM" stop
mv "${FIELD_TEST_DIR:?}"/work "${FIELD_TEST_RUN:?}"/work        # this run's working copy, kept as evidence
cp -a "${FIELD_TEST_DIR:?}"/master "${FIELD_TEST_DIR:?}"/work   # the next run starts from the master again
exit                                                            # ends the recording
"$SKILLS"/design/field-tests/record.sh --pack                   # the latest run as one file: run-<n>.tar.gz
```
Tell me here: the run number. The testing VMs a run created: `devvm ls -a`, then `devvm -n <name> destroy`.

## Variant 2

In the terminal you will work in, after the variables above:
```
"$SKILLS"/design/field-tests/record.sh                          # (a colleague gets the script with the brief)
```
Then work on devvm as you normally would, in your own checkout and VM, with `devvm-brief.md` beside you. At the end, in the VM, in your checkout, export the session as in variant 1 (the `find`, `locate`, `export` lines); back on the host, `cp -a <your checkout>/.claude/transcripts "${FIELD_TEST_RUN:?}"/`, `exit`, then `"$SKILLS"/design/field-tests/record.sh --pack` and send the archive (a colleague: as an attachment to an issue in the private repository, after looking through it).

## Why it is done this way

- The recording runs on the host, so it also covers the VM; output and timing only, never keystrokes.
- Variant 1 starts from copies of your VM and checkout, warts and all, so the test meets the setting a real user has (principal, 2026-11-09). The copy's shared folder and devvm's record of it are moved before the snapshot, because a snapshot keeps the definition of its moment.
- The snapshot resets everything inside the VM (plugin, the agent's memory, settings); the working copy comes from the host, so it is reset by copying the master; the VM is stopped while it changes. The snapshot keeps the shared folder pointing at `work/devvm`, so the fresh copy is what the VM sees after the reset.
- The session is exported into the checkout because the reset would erase it inside the VM.
- Nothing is deleted: every run's folder keeps its recording, notes, working copy and session.
- `${VAR:?}` stops a command when the variable is empty, so no path is ever built from nothing.
- Layers and the reasons in full: `design/walkthroughs/maintainer-field-test-devvm.md`.
