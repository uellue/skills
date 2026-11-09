# Copying an existing devvm VM as-is, with libvirt

Research note, 2026-11-09, for a new devvm requirement (to be filed in devvm's tracker; here it waits in the ledger's inbox). Goal: variant 1 of the field test starts from a copy of the maintainer's VM `devvm-snapshots`, warts and all, instead of a freshly created VM. Checked: `virt-clone` 5.0.0 on this host (`--help`, man page) and devvm's script at `81c3137`. Not checked: anything marked so; nothing was run against a real VM.

## For people

- `virt-clone` is the libvirt tool for this: it copies a shut-off VM's definition and disks under a new name, with a new UUID and MAC address.
  `virt-clone --original devvm-snapshots --name devvm-field --file <pool>/devvm-field.qcow2`
- On this host it must run with the system Python (`PATH=/usr/bin:$PATH virt-clone …`): miniforge's Python first on PATH makes it crash, as devvm's own script notes for `virt-install`.
- A plain clone is not yet a working devvm VM. Five things need doing by hand (or by a future `devvm clone`):
  1. **The shared folder.** The clone's virtiofs `source.dir` still points at the original's host checkout; it must point at the working copy, and devvm's own record of it too (see "Pointing the shared folder at a new source" below).
  2. **devvm's own files.** devvm keeps `<pool>/<name>.hostkey` (and `.pub`) and `<name>.known_hosts` per VM name; ssh checks the host key under the alias `<name>`. The clone needs the two host-key files copied under its name; devvm writes the missing `known_hosts` from `.hostkey.pub` by itself (script lines 462–470).
  5. **The checkout's VM.** `devvm use` stores the VM name in the checkout's git directory (`.git/devvm-vm`), so a copy of the checkout still names the original VM: every `devvm` command run in the copy would act on the original until `devvm use <clone>` is run there.
  3. **Snapshots.** devvm's snapshots are libvirt snapshots stored in the qcow2 (`virsh snapshot-create-as … --atomic`). Whether `virt-clone` carries them over: not stated in the man page, not checked; assume not, and take a new snapshot `field-start` on the clone.
  4. **The disk chain.** devvm's disks are qcow2 overlays on a shared base image (`qemu-img create -b <base>`). Whether the clone's copy keeps that backing link or becomes a full, larger image: not checked.
- **Seen in run 0 (2026-11-09):** the clone of `devvm-snapshots` (about 70 GiB in the original, a backing link to the base image) came out as a full 54 GiB image without the backing link, with no snapshots. It started, but never asked for an IP address: no DHCP lease for its new MAC in `virsh net-dhcp-leases default` after five minutes, so `devvm ssh` had no address. Confirmed the same day: with the original's MAC (`virt-xml <clone> --edit --network mac=<original's>`, the original shut off) the clone got the original's address, 192.168.122.128, and SSH came up; so the network setup inside the guest is tied to the original's MAC (which file does it was not looked at). The tie: `/etc/netplan/50-cloud-init.yaml` matched `macaddress: "52:54:00:d0:cd:b4"` with `set-name: "enp2s0"`; the machine id was the original's.
- **Fixed in run 0, with the principal (2026-11-09),** inside the clone while it still had the original's MAC (the original shut off), then back to its own MAC:
  1. the netplan match `macaddress: …` replaced by `driver: virtio_net` (the old file kept as `50-cloud-init.yaml.orig-mac`), checked with `netplan generate`;
  2. `/etc/cloud/cloud.cfg.d/99-devvm-clone-network.cfg` with `network: {config: disabled}`, so cloud-init does not write the MAC back;
  3. a new machine id: `truncate -s 0 /etc/machine-id; systemd-machine-id-setup` ("Initializing machine ID from SMBIOS/DMI UUID", the clone's new UUID);
  4. shut down, `virt-xml <clone> --edit --network mac=<its own>`, started.

  Result: the clone got its own address (192.168.122.129) with a new DHCP client id; the original keeps 192.168.122.128, so both can run side by side. Still the original's: the hostname (`devvm-snapshots`, also in the DHCP lease list) and the SSH host key; harmless for devvm, which addresses VMs by name and IP, but confusing in a lease list.
- **For a `devvm clone`:** steps 1 to 4 are what it must do (or the equivalent before the first boot, e.g. with `virt-customize`), besides the five steps above; the original may run meanwhile only after step 4.
- Inside the clone everything is identical to the original (hostname, SSH host keys, the agent's memory, logins): that is the point ("warts and all"), but both should not run under the same name on one network at once.
- Lean for devvm: a `devvm clone <new name>` command that does these steps and refuses while the original runs.

## Pointing the shared folder at a new source

How devvm sets it up now (script at `81c3137`):
- At `create`, devvm shares the checkout (its git top level) through virtiofs with the tag `devvm-ws`, mounted in the VM at `/workspaces/<the checkout folder's name>` (`plan_mounts`, `add_fs devvm-ws`); a linked worktree adds the main repository's git directory as `devvm-git`; `DEVVM_MOUNTS` adds more. The VM mounts them by tag through its `/etc/fstab`.
- It records the pair in libvirt metadata: `<workspace host="<checkout>" guest="<path in the VM>"/>` under the namespace `https://devvm.invalid/1` (`virsh metadata … --set`), which `vm_workspace` and `vm_workspace_host` read back.
- Before `start` and `reset` it checks that every share's source exists (`check_shares`), and says: "shared folders are fixed when a VM is created; to drop a mount, re-create the VM without it". So devvm has no command to move a share.

How to move it by hand (the VM shut off; not checked on a real VM):
1. The definition: `PATH=/usr/bin:$PATH virt-xml <vm> --edit target=devvm-ws --filesystem source.dir=<new path>` (checked on `devvm-snapshots` with `--print-diff`, which changes nothing: it alters exactly the `<source dir>` of that filesystem); or, safest, `virsh dumpxml --inactive <vm> > vm.xml`, change the `<source dir=…>` of the filesystem whose `<target dir='devvm-ws'/>`, `virsh define vm.xml`.
2. devvm's record: `virsh metadata <vm> --uri https://devvm.invalid/1 --key devvm --config --set '<workspace host="<new path>" guest="<the old guest path>"/>'`. The guest path stays: the tag and the VM's fstab do not change, so the copy appears where the old checkout did.
3. **Snapshots carry the old definition.** A libvirt snapshot keeps the domain XML of its moment, and reverting restores it; reverting a snapshot taken before the move brings the old source back. If the old path still exists (for a clone of `devvm-snapshots`: the maintainer's real checkout), the VM silently shares it again, since `check_shares` only sees that a source exists. So: move the share first, then take the new snapshot (`field-start`), and delete or never use the older ones on the clone.

For the field test this means: clone `devvm-snapshots` (shut off), move its `devvm-ws` share to the working copy, update the metadata, take `field-start`; the runbook's reset by snapshot then keeps pointing at the working copy, which the runbook swaps for a fresh copy of the master between runs while the VM is off.

## For agents

- Commands seen: `virt-clone -o/--original`, `-n/--name`, `-f/--file` (once per disk), `--auto-clone`, `--reflink` (btrfs only), `--preserve-data`, `--skip-copy`, `--check path_in_use=off`.
- devvm script lines: disk `DISK=$DEVVM_POOL_DIR/$DEVVM_VM_NAME.qcow2` (290), host key and known hosts (294, 295), overlay creation (894), virtiofs `--filesystem type=mount,…,driver.type=virtiofs,source.dir=…` (860), snapshots `virsh snapshot-create-as` (1080), the note on the system Python (284).
- To verify before relying on it: run `virt-clone` on a throwaway devvm VM; compare `qemu-img info --backing-chain` of both disks; `virsh snapshot-list` on the clone; `devvm -n <clone> ssh`.
