# Diagnosis brief (template)

For a hallway test or a measured walk-through where the process under test is finding out what is wrong. The main session injects the faults and keeps this brief free of any hint of them. Fill the angle brackets; delete what does not apply.

---

You are <persona from the stakeholder record: role, what they know, what they have on their machine>. Something looks wrong and you have to find out what and why.

**The symptom, exactly as it was noticed:** <one or two sentences in the persona's words: the search result, the log line, the complaint. No cause, no hint.>

**What you may read and run:** <the user-facing documentation; the commands a user of this role has; the running system's endpoints or CLI>. You may run read-only commands against the system. You may not read the source code, the tests, the specifications, the design notes or the git history, and you may not change anything. If the harness attaches something you did not ask for, say so in your report and do not use it.

**Method.** Keep an investigation log: every command or page you looked at, what you expected it to show, what it showed, and what you concluded; the order matters. Before you form a verdict, write down what else could explain the symptom and what would rule it out. Stop when you can name the cause with evidence, or when you have run out of things a person in this role could do; say which.

**If the documentation does not say what should happen,** ask the main session with SendMessage; the question itself is a finding, so record it in the log.

**Report**, as your final message (the main session writes the file):

1. Verdict: the cause, in one sentence, with the evidence that supports it; or "could not determine", with what was ruled out and what was missing.
2. Investigation log, in order, with times.
3. What the system or the documentation should have told you earlier, and where (concrete: the command, the page, the message).
4. Questions you had to ask or would have asked the owner.
5. What you were given, and anything attached that you did not ask for.

---

Notes for the main session: inject faults that look real (the system's own formats, no test markers, no timestamps the system never writes); record the tester's calls, time and tokens (`usage.py <its transcript>`); say in the record whether the tester's verdict was right, and what in the system's output or documentation made the diagnosis take longer than it should.
