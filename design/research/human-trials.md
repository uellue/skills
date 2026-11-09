# Field tests of a tool, with a recording for the agent

(First written as "human trials"; renamed 2026-11-09, glossary *field test*. The file name stays.)

Research note, 2026-11-09. Status: background, not a requirement. "Suggestion" marks my own proposals; everything else is from a named source or a run I did (marked "tried here").

## For people

### What we learned

1. `script` (util-linux) records output to a plain file and timing to a second file; with `--log-in` it also records every keystroke, including passwords. A recording is text plus raw escape sequences: an agent can read it after stripping them, but then sees no layout, colour, pager screen or wrapping. It is a transcript, not a picture.
2. So a recording complements the screenshot tester and does not replace it. It is the right tool where copy and paste fails: a colleague in their own environment, a VM, a devcontainer. It also catches what screenshots miss: timing, what the person typed, mistakes, retries.
3. Usability practice already has the pieces: task scenarios, think-aloud, moderated versus unmoderated sessions. An unmoderated trial handed back as files is the normal "recording for later review" case.
4. Devcontainers and disposable VMs give a clean start: a `devcontainer.json` in the repository defines the environment reproducibly.
5. Privacy is the main risk: output logs hold whatever was on screen, input logs hold passwords.

### Proposals (all my suggestions)

1. Smallest version first: the brief asks the participant to run `script -q -T timing.log -O session.log` (output and timing only, no input log), do the task, type `exit`, and send both files. The agent reads `session.log` as cleaned text.
2. A small script in `plugins/kaizen/scripts/` that turns a recording into plain text (strip escapes, apply backspaces and carriage returns), and refuses to run without the timing file. Only worth writing after proposal 1 has run once with a real colleague.
3. Participant checklist in the brief: no secrets on screen, start in a fresh shell, look through the file before sending, and say which lines to delete (editing is allowed; see sources).
4. Environment: for a trial in a devcontainer or VM, the brief names the `devcontainer.json` (or image) and a fresh checkout; the participant's own machine is allowed but marked "uncontrolled" in the record.
5. Keep the by-eye tester for look and feel. Add the recording only for the question "what happened and when, in an environment we cannot see".

### Open questions

- Which participants and which environments are real (own laptop, Windows, macOS)? `script` differs on macOS (BSD `script`; I did not check its flags).
- Is the participant allowed to see the brief's expectations first, or is it moderated by chat?
- Where do the files live (they may hold private material; the repository is public, so `.claude/debriefs/`, ignored)?
- Is a cleaning script wanted, or is the regex in the next part enough?

## For agents

### script and scriptreplay (util-linux 2.41.5 installed here; man7.org page footer 2.43.devel, 2026-05-24)

Sources: `man script` on this host (2.41.5); https://man7.org/linux/man-pages/man1/scriptreplay.1.html; https://www.redhat.com/en/blog/record-terminal-script-scriptreplay (Seth Kenlon, 2022-01-18).

- Since util-linux 2.35 `script` has multiple streams: `-O/--log-out`, `-I/--log-in`, `-B/--log-io` (both in one file; useful only with `-T`), timing `-T/--log-timing`. Classic timing format (one stream): two fields, delay and character count. Advanced format (input and output, or `-m advanced`): first field I/O/H/S (input, output, header, signal), then delay, then data. `-m/--logging-format` forces either.
- Other options from the man page: `-q` quiet, `-c cmd` run a command instead of a shell, `-e` return child exit status, `-o size` output limit, `-f` flush, `-a` append.
- Replay: `scriptreplay -T timing.log -O session.log`; `-d` divisor, `-m` maxdelay, `-x in|out|signal|info` one stream, `--summary` (needs advanced format). Replay does not rerun anything, but sends raw escapes, so it works reliably only on the same terminal type.
- Tried here (2.41.5): `printf '...' | script -q -T t.tm -O o.log -I i.log` gave an advanced-format timing file starting with `H` lines (START_TIME, SHELL, TIMING_LOG), and `scriptreplay --summary` printed duration and exit code. The typescript starts with a "Script started on ..." line and keeps `^M`, colour codes and bracketed-paste codes (`ESC[?2004h`).
- Agent-readable text, tried here: `col -b` is not enough: it removed ESC but left `[31m`, `?2004h` and mangled the line ends. `sed -r 's/\x1b\[[0-9;?]*[A-Za-z]//g' o.log | tr -d '\r'` gave clean text. It does not handle cursor movement, `ESC]` title sequences, backspace editing, or full-screen programs (less, vim, progress bars). `ansi2txt` (colorized-logs) is not installed here and I did not check it. Robust alternative, not tried: feed the typescript to a terminal emulator library (for example `pyte`, a new dependency, to be flagged) with a fixed size and read the screen, or replay into `tmux` and `capture-pane -p` (flags `-p`, `-e`, `-J`, `-S` confirmed in https://man7.org/linux/man-pages/man1/tmux.1.html, version not shown on the page).
- Size: text only. My 5-line session: 375 bytes output, 238 bytes timing, 196 bytes input. Long runs with progress bars grow fast; `-o size` caps it.
- Privacy: the man page warns that `--log-in`/`--log-io` may record security-sensitive information such as passwords regardless of the echo flag. The output log also holds anything printed (tokens in env dumps, paths, user and host name in the prompt: seen in my run). Mitigate: no `-I`/`-B` by default; fresh shell; review and redact before sending (the Red Hat post says small edits are fine, heavy edits desynchronize the timing); do not commit recordings.

### Comparison (briefly)

- asciinema, asciicast v2 (https://docs.asciinema.org/manual/asciicast/v2/, checked 2026-11-09): newline-delimited JSON, header with `version`, `width`, `height` (optional `timestamp`, `command`, `env`, `idle_time_limit`, `theme`), events `[time, code, data]` with codes `o`, `i`, `m`, `r` (resize). Input is not captured by default. Advantages over `script`: one file, terminal size recorded, resize events, easy to parse as JSON. Cost: a third-party install on the participant's machine. The CLI usage page returned 404, so I cannot confirm `rec`/`play`/`cat` flags or the current CLI version; not verified.
- tmux `pipe-pane`: I could not read its section of the man page (the fetch cut it off), so I make no claim about its options. `capture-pane` is described above. Both need tmux and give no timing.

### Screenshot tester versus recording (my analysis)

- Screenshots (existing by-eye mode) catch: layout, colour, wrapping at a given width, pager state, text scrolled off. Miss: timing, history.
- Cleaned recording text catches: exact commands, errors, order, long pauses (from the timing file), retries, what the person typed wrongly. Misses: colour (stripped), wrapping (depends on the participant's width, which `script` does not record in the timing file as far as I saw; ask for it), full-screen and pager content.
- Combination (suggestion): the agent tester drives under `script` in the xterm and keeps screenshots; the recording adds timing. A human recording judged by an agent covers environments we cannot reproduce.

### Usability practice

- Think-aloud: Nielsen, 2012-01-15, https://www.nngroup.com/articles/thinking-aloud-the-1-usability-tool/. Representative users, representative tasks, silent facilitator; caveats: unnatural, prompts bias. A terminal log cannot carry the spoken thoughts; ask the participant to type notes with a `# ` comment line, or to send a few sentences afterwards (suggestion).
- Moderated versus unmoderated: Schade, 2013-10-12, https://www.nngroup.com/articles/remote-usability-tests/. Unmoderated sessions are recorded for later review; you learn about problems only afterwards; participants think aloud less.
- Task scenarios, about five participants, priming by task wording: Moran, 2019-12-01 (reviewed 2026-07-15), https://www.nngroup.com/articles/usability-testing-101/. None of these three pages defines the "hallway test"; I have no source for it and did not search further.
- Devcontainers: https://containers.dev/implementors/spec/ (checked 2026-11-09): `devcontainer.json` "deterministically creates containers"; `image` or `build.dockerfile`, `features`, lifecycle commands such as `postCreateCommand`, `remoteUser`. I did not check disposable-VM tooling (Vagrant, multipass, cloud-init); no source, no claim.

### Draft brief for the participant (suggestion, smallest version)

1. Open a new terminal, wide enough for the tool (say the width: `stty size`).
2. `script -q -T timing.log -O session.log`
3. Do tasks 1 to 3 (scenario text, written like the stakeholder's own goal). Type `# ` lines for what confuses you.
4. `exit`. Open `session.log` in an editor, remove anything private, send `session.log`, `timing.log` and the `stty size` line.

Agent side: clean with the sed line above, read with the record's expectations beside it, list moments (command, expected, observed, seconds from the timing file), classify as in the behaviour brief. Stays private: both files and the participant's name, in `.claude/debriefs/`; the record in `design/hallway/` gets findings only.

Smallest version worth trying: steps 1 to 4 once, with one colleague, no new script; judge afterwards whether cleaning by regex was enough.

### Sources opened

- https://www.redhat.com/en/blog/record-terminal-script-scriptreplay (2022-01-18)
- https://man7.org/linux/man-pages/man1/scriptreplay.1.html (2.43.devel, 2026-05-24); local `man script` 2.41.5
- https://docs.asciinema.org/manual/asciicast/v2/
- https://man7.org/linux/man-pages/man1/tmux.1.html (partly read)
- https://containers.dev/implementors/spec/
- https://www.nngroup.com/articles/thinking-aloud-the-1-usability-tool/
- https://www.nngroup.com/articles/remote-usability-tests/
- https://www.nngroup.com/articles/usability-testing-101/
- Not available: docs.asciinema.org CLI usage page (404).
