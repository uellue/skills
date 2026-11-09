# Copying an existing devvm VM as-is, with libvirt

Research note, 2026-11-09, for a new devvm requirement (to be filed in devvm's tracker; here it waits in the ledger's inbox). Goal: variant 1 of the field test starts from a copy of the maintainer's VM `devvm-snapshots`, warts and all, instead of a freshly created VM. Checked: `virt-clone` 5.0.0 on this host (`--help`, man page) and devvm's script at `81c3137`. Not checked: anything marked so; nothing was run against a real VM.

## For people

- `virt-clone` is the libvirt tool for this: it copies a shut-off VM's definition and disks under a new name, with a new UUID and MAC address.
  `virt-clone --original devvm-snapshots --name devvm-field --file <pool>/devvm-field.qcow2`
- On this host it must run with the system Python (`PATH=/usr/bin:$PATH virt-clone …`): miniforge's Python first on PATH makes it crash, as devvm's own script notes for `virt-install`.
- A plain clone is not yet a working devvm VM. Four things need doing by hand (or by a future `devvm clone`):
  1. **The shared folder.** The clone's virtiofs `source.dir` still points at the original's host checkout; it must point at the working copy, e.g. `virt-xml devvm-field --edit --filesystem source.dir=<working copy>` (not checked).
  2. **devvm's own files.** devvm keeps `<pool>/<name>.hostkey` and `<name>.known_hosts` per VM name; the clone needs copies under its name, or `devvm ssh` will not know it (not checked).
  3. **Snapshots.** devvm's snapshots are libvirt snapshots stored in the qcow2 (`virsh snapshot-create-as … --atomic`). Whether `virt-clone` carries them over: not stated in the man page, not checked; assume not, and take a new snapshot `field-start` on the clone.
  4. **The disk chain.** devvm's disks are qcow2 overlays on a shared base image (`qemu-img create -b <base>`). Whether the clone's copy keeps that backing link or becomes a full, larger image: not checked.
- Inside the clone everything is identical to the original (hostname, SSH host keys, the agent's memory, logins): that is the point ("warts and all"), but both should not run under the same name on one network at once.
- Lean for devvm: a `devvm clone <new name>` command that does the four steps and refuses while the original runs.

## For agents

- Commands seen: `virt-clone -o/--original`, `-n/--name`, `-f/--file` (once per disk), `--auto-clone`, `--reflink` (btrfs only), `--preserve-data`, `--skip-copy`, `--check path_in_use=off`.
- devvm script lines: disk `DISK=$DEVVM_POOL_DIR/$DEVVM_VM_NAME.qcow2` (290), host key and known hosts (294, 295), overlay creation (894), virtiofs `--filesystem type=mount,…,driver.type=virtiofs,source.dir=…` (860), snapshots `virsh snapshot-create-as` (1080), the note on the system Python (284).
- To verify before relying on it: run `virt-clone` on a throwaway devvm VM; compare `qemu-img info --backing-chain` of both disks; `virsh snapshot-list` on the clone; `devvm -n <clone> ssh`.
