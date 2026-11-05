# Reference findings

Reference findings for the change request in `project/README.md`, collected from the runs so far. Not a list of right answers: it makes differences between runs visible, and real use is authoritative. Each item: what it is, why it matters, how a run can show it. Items K6, K7 and K9 only appear when a run implements the change; they test whether the process catches what an implementation gets wrong.

## Findings

- **K1. The need behind "tags".** The complaint is that people cannot find *old* notes; there are hundreds, and none has a tag. Tags only help notes written from now on, so search over the existing text is the must and tags at most a should. Shows as: the need stated separately from the requested solution, and search ranked above tags.
- **K2. Lost updates.** Two concurrent `add` calls each load, append and save; one overwrites the other. Shows as: the race named, ideally measured against the original tool (the baseline measured 18 of 40 notes lost).
- **K3. Torn file.** A write interrupted or interleaved leaves invalid JSON, after which every command fails for everyone. Shows as: named, ideally measured.
- **K4. ID reuse.** IDs are `max + 1`, so deleting the newest note frees its ID; a colleague who listed earlier and runs `rm 7` deletes the new note 7. A second, non-obvious cause of "a note disappears". Shows as: named, with the two-person sequence.
- **K5. What "the group drive" is.** Whether file locking works depends on SMB, NFS or a sync client; the answer decides the design. Shows as: a question to the principal, or an explicit assumption that blocks or conditions the build.
- **K6. Atomic replace breaks a symlinked shared file.** A fix that writes a temporary file and `os.replace`s it replaces a symlink with a local file, so notes silently stop reaching the shared file: the original complaint, re-created by the fix. Implementation only.
- **K7. Rewriting the file resets its mode and owner.** A colleague can lose access to the shared file after the first write. Implementation only.
- **K8. Unquoted tags vanish.** In `notes add ... #x17` the shell treats `#x17` as a comment and drops it silently. Shows as: an interface decision that avoids `#` (an option such as `-t`), or the trap named.
- **K9. Duplicate IDs make `rm` delete several notes.** If IDs ever collide (old files, copied files, a lost high-water mark), `rm` removes all matches and reports one. Implementation only.
- **K10. Old clients on a changed file.** Colleagues will run old and new versions on the same file for a while; a format change must not break old clients or lose the new fields when an old client writes. Shows as: compatibility checked or stated as a requirement.

## Process measures

- Decisions an implementer had to invent because no document settled them (the baseline's kaizen-only condition: 21).
- Size of the records against the size of the change (baseline: up to 34 KB of records for a 4 KB tool).
- Findings that are wrong (claims a grader refutes against the code), and claims about the tool that were never checked.
- Tokens and minutes per condition and per stage.
