# Human trials: getting the recording from the participant to the agent session

Research note, 2026-11-09. Status: background, facts only; the decisions are not made here. Follows `human-trials.md` (recording with `script`), which is not repeated. "Not verified" marks anything I did not read in a source or run myself. "Tried here" marks my own runs (bash 5.2.37, util-linux `script`, gh 2.46.0 on Debian; zsh and asciinema are not installed here).

## For people

### What we learned

1. No single channel wins on all three criteria (low friction, participant reviews first, agent reads it directly). The best fit for friction plus review is a file the participant uploads by hand after looking at it; the best fit for the agent is anything reachable by `gh`.
2. A GitHub issue comment accepts `.log`, `.txt`, `.zip`, `.gz` attachments up to 25 MB and, in a private repository, only people with repository access see the files. That covers the recording and the timing file without conversion. The participant needs a GitHub account with access to that repository.
3. A secret gist is not private: anyone with the URL can read it. It is the lowest-friction option with `gh`, but the participant must be told it is "unlisted", not "private".
4. `magic-wormhole` needs both sides online within about an hour of each other and a Python-based install on both; a good fit when a person is in a live call, a poor fit for "do it on your own time".
5. Claude Code's own cross-machine features (cross-session messaging, Remote Control, cloud sessions) are for one person's own sessions and for plain text between sessions; I found nothing in code.claude.com for sending files or a recording from another person's machine. "Channels" can push messages (chat, webhooks) into a session but are a research preview, need Bun and a chat plugin, and carry text, not a file-exchange feature as documented.
6. In bash, a `# note` line at the prompt works (interactive comments are on by default). In zsh the option is off by default per the manual, so `# note` is likely to fail there; `: note` works in both, but an apostrophe in it breaks both (tried in bash). Not tried in zsh: not installed.
7. For redaction before sharing, established secret scanners exist (gitleaks, detect-secrets, trufflehog) and can scan a plain file. They find secrets, not personal data, and none claims completeness. A participant-side prompt for a local agent is plausible but I found no published prior art for exactly that.

### Options compared

| Option | Participant steps | Agent reads with | Who can see it, deletable | New dependency on participant side |
|---|---|---|---|---|
| Issue comment in a private repository | open issue, drag two files in, submit | `gh issue view`, `gh api` (attachment download: not verified) | repository members only (GitHub docs); participant can delete own comment (not verified) | GitHub account with repository access |
| Issue in a public repository | same | same | everyone; deletion of attachment URLs not verified | GitHub account; not recommended for raw recordings |
| Secret gist (`gh gist create`) | one command | `gh gist view <id>`, `gh gist clone` (not verified) | anyone with the URL; `gh gist delete` exists | `gh` plus login (or browser upload at gist.github.com) |
| Private repo or branch the participant pushes to | clone, copy files, commit, push | `git`, `gh` | collaborators only; history keeps the files after deletion | git, push access |
| Mail or chat attachment | attach two files | person saves the file and tells the agent the path | recipients of the mail or channel | none |
| Shared directory (virtiofs, sshfs, syncthing) | none or one setup | plain file read | whoever has the mount | virtiofs: libvirt stack (devvm already has it); sshfs: sshfs and SSH access; syncthing: daemon on both sides |
| `magic-wormhole` | `wormhole send file`, read out the code | person runs `wormhole receive`, tells the agent the path | only the two ends (encrypted); transient | Python 3.10+ tool, or distro package |
| Claude Code cross-session messaging | none for the participant | message text only, no files | Anthropic servers for cross-machine; own sessions only | Claude Code on both sides, same account |

### Open questions

- Does the participant have a GitHub account (and access to a private repository), or only mail and chat?
- Is the participant's own agent available (Claude Code or other) for the redaction prompt, or is review by eye the only step?
- Should the agent read the files directly (needs `gh` access) or may a person place them (the "known working pattern" with a person in the middle)?
- Is a public issue acceptable for findings only, with the raw recording elsewhere?
- zsh and macOS: the participant's shell may be zsh with default options; is `: note` acceptable as the marker instead of `#`?

## For agents

### 1. Transport

**GitHub issue attachments.** Source: https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/attaching-files (read 2026-11-09). Limits: 10 MB images and GIFs; videos 10 MB (free plan owner) or 100 MB (paid); 25 MB for all other files. Types allowed in issue, pull request and discussion comments include TXT, MD, CSV, TSV, LOG, JSON, ZIP, GZ, TGZ, PDF, shell scripts. Statement: "In the case of private and internal repositories, only people with access to the repository can view the uploaded files." So `session.log` and `timing.log` can be attached as they are; a `.cast` file (asciinema) is not in the list as I read it, so zip it (not verified whether `.cast` is accepted). A participant must be able to open the repository. A "Linux `.patch` upload error" is mentioned by the page as a known issue; irrelevant here. Public repository visibility of attachment URLs, and whether deleting a comment removes the file: not verified. Agent side: `gh issue view <n> --comments` gives text; downloading the attached file by URL from a private repository needs authentication, which I did not test. Local `gh issue create --help` (gh 2.46.0) lists only title/body/body-file/template style flags and shows no attachment flag; attaching is a browser action, so the participant needs the web UI. An issue form (YAML template) can structure the notes: not read here, no claim.

**GitLab.** The official GitLab docs page for attachments did not come up. A search returned a third-party site stating 100 MB default for web UI attachments and an older blog post stating 10 MB (https://gitlab.com/gitlab-org/gitlab/-/work_items/20060 and /20061 are issues about raising the limit); I could not verify the current default. Not verified; ask the instance admin if GitLab is chosen.

**Secret gist.** Sources: https://docs.github.com/en/get-started/writing-on-github/editing-and-sharing-content-with-gists/creating-gists and https://cli.github.com/manual/gh_gist_create (both read 2026-11-09). "Secret gists aren't private"; anyone with the URL can view; not searchable unless you are the logged-in author; GitHub scans secret gists for partner secrets. `gh gist create [<filename>... | -] [-d desc] [-f name] [-p] [-w]`; secret by default, `--public` for listed. `-` reads stdin, `-f` names it. `gh gist delete {<id>|<url>}` exists (tried here: `--help` printed). Size limit and binary-file handling: not verified, so `session.log` with escape bytes may be mangled; the cleaned text version is safer. Two files in one gist: `gh gist create session.log timing.log` follows from the usage line (not run, it would publish).

**Private repository or branch.** No source read. From general git knowledge: collaborator access gives push; deleting a file later leaves it in history, so a branch the participant pushes to is the least deletable option. Not verified against docs; listed for completeness.

**Mail or chat.** No source needed; the person saves the attachment and gives the agent the path (the same person-in-the-middle step as the known pattern). Privacy is the mail or chat system's.

**Shared directory.** devvm's README (https://github.com/modama-rdm/devvm, read 2026-11-09): virtiofs via `virtiofsd`, the checkout is shared read-write at `/workspaces/<folder name>` by default (`DEVVM_SHARE_WORKSPACE=1`), `DEVVM_MOUNTS` adds folders with `type=bind` (optionally read-only), `DEVVM_SHARE_WORKSPACE=0` switches to SSH push and fetch. 9p is not mentioned. Consequence: for a trial inside a devvm VM, a recording written under the shared workspace appears on the participant's host without a step; it still has to cross from that host to the developer's session by one of the other rows. Prerequisites listed there: KVM, libvirt, `virt-install`, `qemu-img`, `virtiofsd`, membership of the `libvirt` group. sshfs and syncthing: no source read, not verified; both need software and a persistent connection or daemon on both ends, which is more than the "lowest friction" requirement.

**magic-wormhole.** Sources: https://raw.githubusercontent.com/magic-wormhole/magic-wormhole/master/README.md and https://magic-wormhole.readthedocs.io/en/latest/welcome.html (read 2026-11-09). `wormhole send <file>` prints a code like `7-crossover-clockwork`; the receiver runs `wormhole receive`, types the code, answers `ok? (y/n)`. SPAKE2 key exchange, data encrypted with libsodium secretbox; the transit relay forwards only encrypted data; the 16-bit default code gives about 1 in 65536 guess chance per attempt and each code is single-use. "Both clients must be left running until the transfer has finished"; clients are expected to run within an hour or so of each other. Install: `apt install magic-wormhole`, `brew install magic-wormhole`, `winget install -e --id magic-wormhole.magic-wormhole`, `pip install --user magic-wormhole`; Python 3.10 or later; MIT. The agent cannot type the receive command itself unless it has a shell on the receiving host, which it has when it runs `wormhole receive` in its own session and shows the code to the person, who relays it: that is the natural variant (agent starts `wormhole receive`, person runs `wormhole send` with the code). Not run here (not installed).

**Claude Code features (official docs, read 2026-11-09).**
- Cross-session messaging, https://code.claude.com/docs/en/cross-session-messaging.md: "A message is a piece of text one Claude writes to another, never the sender's conversation history or files." Cross-machine goes through Anthropic servers and needs a claude.ai sign-in with Remote Control; it reaches "your sessions", i.e. one person's. Not a route from another colleague's machine. `isolatePeerMachines` can require approval before a message leaves.
- Sessions, https://code.claude.com/docs/en/sessions.md: `/export` writes the conversation as plain text; transcripts are JSONL under `~/.claude/projects/<project>/<session-id>.jsonl`; `claude --resume <transcript-path>` resumes from a `.jsonl` at an absolute path (this is how a transcript copied by hand could be opened; I did not try it, and the entry format is stated to be internal and version-dependent). This is the participant's own agent's log, a different thing from the `script` recording, and carries more private material.
- Channels, https://code.claude.com/docs/en/channels.md: research preview, pushes events from an MCP server (Telegram, Discord, iMessage, webhooks) into a running session; each channel has a sender allowlist; needs Bun; the page describes message events, and says the Discord plugin has "Attach Files" permission (not a documented receiving path for files into the session). Not verified whether an attachment sent over a channel reaches the session as a file.
- GitHub Actions, https://code.claude.com/docs/en/github-actions.md: `@claude` in an issue or PR comment starts a run in the repository's workflow; requires write access for the triggering user by default. That is the participant-hostile direction (the participant would need write access to trigger it); the developer session is not the one reading. Not an exchange feature for this purpose.
- Cloud sessions and Remote Control, https://code.claude.com/docs/en/claude-code-on-the-web.md and https://code.claude.com/docs/en/remote-control.md: listed in the docs index; I did not read them, so no claim beyond their titles in https://code.claude.com/docs/llms.txt.

### 2. Prior art

- Issue tracker as agent inbox: GitHub Copilot coding agent starts from an issue assigned to Copilot, creates a draft pull request and requests a review (https://docs.github.com/en/copilot/using-github-copilot/coding-agent/using-copilot-to-work-on-an-issue; I saw this only in search snippets, did not open the page; the same snippets say later issue comments are not seen by the agent and new information goes on its pull request, which comes from a Microsoft Learn page, not verified). Claude Code GitHub Actions: `@claude` mentions in issues and pull requests (page above, read).
- Push into a running session: Claude Code channels (above, read).
- Agent scratchpad repositories: I searched for no source on this and have none; not verified, no claim.
- Unmoderated remote usability testing: Nielsen Norman Group describes unmoderated sessions as recorded for later review (https://www.nngroup.com/articles/remote-usability-tests/, read in the earlier note, 2026-11-09). Maze returns results per test with screen recordings ("Clips") per task and automatic transcripts, per search snippets from https://help.maze.co and https://maze.co/features/clips-video-recordings/ (not opened; export options for transcripts not confirmed). UserTesting: no source found, no claim. The common practice in these tools is that the platform hosts the recording and the researcher reviews it there, which the participant cannot review beforehand; that is the point where this plan differs.

### 3. Comments while `script` records

Everything the shell echoes goes into `session.log`, so any line that the shell accepts without error is a note.

- bash: `man bash` here (5.2.37): "interactive_comments ... If set, allow a word beginning with # to cause that word and all remaining characters on that line to be ignored in an interactive shell ... This option is enabled by default." Tried here: `# this confused me` and `: note two` and `echo "note three"` piped into `script -q -T t.tm -O o.log` all appear verbatim in `o.log`, with the prompt before them; no error output. The timing file records when each was typed.
- Apostrophes: tried here, `# it's confusing` is fine (comment), but `: don't know` leaves bash waiting for the closing quote and swallows the following lines (the subsequent `echo hi` and `exit` became a continuation, then `unexpected EOF while looking for matching '`). The same happens with `echo don't`. So notes after `:` or `echo` must avoid or quote apostrophes; `#` notes need no quoting in bash.
- zsh: https://zsh.sourceforge.io/Doc/Release/Options.html (read 2026-11-09): `INTERACTIVE_COMMENTS` (`-k`) "Allow comments even in interactive shells", marked `<K> <S>` and not `<D>`, i.e. on by default only in ksh and sh emulation, off in native zsh. So in a default zsh a line starting with `#` is not a comment; zsh would try to run a command named `#` (my expectation from the option text; not run, zsh not installed). `setopt interactive_comments` turns it on. `:` and `echo` work in zsh as in any POSIX shell (not run); the quoting problem is the same, and `?`, `*`, `[`, `!` in an unquoted echo text can still be expanded (zsh also errors on an unmatched glob, "no matches found"; my knowledge, not verified in the manual here).
- The brief could therefore say: type `: your note` (no apostrophes) or, in bash, `# your note`; in zsh first `setopt interactive_comments`. Separately, `script -c` can run a shell of the participant's choice, so `script -c bash` gives bash on a zsh machine (option exists per the earlier note; not tried with zsh).
- Recorder markers. asciinema: https://docs.asciinema.org/manual/cli/markers/ (read 2026-11-09): a key binding adds a marker in real time, "there's no default binding at the moment", so `rec.add_marker_key` must be set in the config first; a desktop notification confirms; markers are marker events in the `.cast` file and can be inserted by hand. Format link from the earlier note: asciicast v2 has event code `m`. A marker has no text from the key press as described on that page (a label is not mentioned there; not verified). tmux: no source read here; the earlier note covers `capture-pane`; no marker feature was found or claimed. `script`: none; the only marker is typed text.

### 4. Redaction before sharing

- gitleaks, https://github.com/gitleaks/gitleaks (read 2026-11-09): commands `git`, `dir`, `stdin`; `gitleaks dir -v <file-or-dir>` scans without git; `--redact` redacts secrets in logs and output (default 100%); MIT; install via Homebrew, Docker, Go, release binaries. README states the project is feature complete and future releases are security patches only (maintainer moving to another project). Detects secrets, not names or hostnames.
- detect-secrets, https://github.com/Yelp/detect-secrets (read 2026-11-09): `detect-secrets scan <dir> --all-files` for non-git files; `pip install detect-secrets` or Homebrew; Apache-2.0; page says it is "not a sure-fire solution", misses multi-line secrets and weak default passwords such as `login = "hunter2"`, entropy detectors need tuning. Output is a baseline JSON of findings, not a redacted copy.
- trufflehog, https://github.com/trufflesecurity/trufflehog (read 2026-11-09): `trufflehog filesystem <paths>` and `trufflehog stdin`; AGPL-3.0 since v3; the page documents no redaction option, and its example outputs show the raw value (so findings can contain the secret).
- None of these is a drop-in "redact a terminal recording" tool; the `script` file also holds user name, host name and paths in the prompt (seen in my run: the prompt printed user, host, directory), which scanners do not treat as secrets. A plain `sed` on `$USER`, `$HOSTNAME`, `$HOME` is the cheap complement (suggestion, not run on a real session).
- Prior art for "prompt for the participant's own agent that produces a postable report": I found none in the sources above. Not verified; no claim.
- Shape of such a prompt (suggestion, with sources only for the building blocks): read `session.log` after the escape-stripping from the earlier note; produce a report with commands, expected, observed, timings; list every line that contains a user name, host, home path, token-like string, address, or free text from the participant, as a table of "line, why flagged, proposed replacement"; run gitleaks or detect-secrets as a second opinion if installed (new dependency, flag it); write the redacted file to a new name, never overwrite; show the diff between original and redacted; end with "type ok to send"; send nothing itself. The agent session never sees the unredacted file.

### New third-party dependencies each option would add (participant side unless noted)

- Issue attachment: none beyond a browser and a GitHub account with access. Agent side: `gh` (already used).
- Secret gist: `gh` CLI with login (gh 2.46.0 here; current release not looked up).
- Private repo push: git (usually present).
- Shared directory: virtiofs none beyond devvm's stack; sshfs, syncthing: new packages, versions not looked up.
- magic-wormhole: Python 3.10+ package on both sides (current release not looked up).
- Redaction helpers: gitleaks (MIT) or detect-secrets (Apache-2.0) or trufflehog (AGPL-3.0, licence worth noting); asciinema if markers wanted; `pyte` or tmux for terminal-faithful cleaning (earlier note). Per the standing rule, none to be added without asking, and a current release looked up first.

### Sources opened (all 2026-11-09)

- https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/attaching-files
- https://docs.github.com/en/get-started/writing-on-github/editing-and-sharing-content-with-gists/creating-gists
- https://cli.github.com/manual/gh_gist_create
- https://raw.githubusercontent.com/magic-wormhole/magic-wormhole/master/README.md
- https://magic-wormhole.readthedocs.io/en/latest/welcome.html
- https://code.claude.com/docs/llms.txt, /docs/en/cross-session-messaging.md, /docs/en/sessions.md, /docs/en/github-actions.md, /docs/en/channels.md
- https://zsh.sourceforge.io/Doc/Release/Options.html
- https://docs.asciinema.org/manual/cli/markers/
- https://github.com/modama-rdm/devvm
- https://github.com/gitleaks/gitleaks, https://github.com/trufflesecurity/trufflehog, https://github.com/Yelp/detect-secrets
- Local: `man bash` 5.2.37, `man script`, `gh gist delete --help`, `gh issue create --help` (2.46.0)
- Search only (snippets, pages not opened): Copilot coding agent issue assignment (docs.github.com), GitLab attachment size (gitlab.com issues 20060 and 20061), Maze help centre.
- Failed: https://docs.asciinema.org/manual/cli/usage/ (404, as in the earlier note); the asciinema CLI overview page did not cover markers (the markers page did).
