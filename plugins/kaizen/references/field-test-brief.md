# A brief for a field-test participant

What a field test's brief for a person gives, and what it leaves out. Learned from the briefs of the first field tests, where the person's edits removed everything that told the participant how to behave.

## What it gives

- **The start:** one command or one situation ("open the tool on your last session's export"; "type `/kaizen:update`, then work as you normally would").
- **The method:** the recording, started for them; the ways to note things in the moment, whichever is at hand (a `#` line at the shell prompt, which lands in the recording, with `setopt interactivecomments` first in zsh; the notes file from a second terminal or an editor; the subject's own features for feedback); what to note that the recording cannot see (a page read in a browser, a colleague asked, something looked up elsewhere).
- **Be frank:** the raw reaction is what helps, swearing and sighs included; nothing written there is held against anyone.
- **The setting's rules:** what must not leave the machine during the test (posts, pushes), and those safety limits that the participant's own actions could break ("stop with `./downstaging.sh`, never the test reset"), as rules of the setting, not as a script for reacting to the subject. Limits the setup enforces (a read-only mount, ports on localhost) stay out: each one enforced is a line less in the brief.
- **The hand-back:** wind the session down as you normally would; how the evidence reaches the developer (one archive, looked through first for anything private); and the closing question: "Did we do OK? Was anything in this brief uncomfortable or unclear?"

## What it leaves out

- How to behave, answer or decide: people come with their own role, persona and agenda; telling them to "follow" the subject or how to answer is a personality change. Prefer participants who have the role naturally over asking someone to play it.
- Disturbances the test would inject: a scripted sequence of steps, a role word that reads as a job title, a reason to look things up or not.
- Anything the developer knows that the participant would not: the test is worth most when the person follows their nose and goes off script. Scripts and scenarios belong to the automated hallway tests.
