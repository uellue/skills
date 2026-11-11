# Brief: grading a field-test run

The field-test skill gives this brief, filled in, to one fresh reader agent (Opus; read only) after a run, with the run's sessions rendered by `transcript.py render`. The filled brief and the report stay private, in the run's evidence folder (`grade.md` beside the recording). When a grade misjudges, the person's correction goes into the project's list of what works as designed (`design/field-tests/works-as-designed.md`, tracked: each entry with the run and the correction in a sentence; the person's own words stay in the evidence folder), and the next grade reads it.

---

You grade one field test of <the subject> in <project> (<repository path>, <branch or commit>, <version of the subject>). Read only; write nothing except your report as your final message.

Layers: <each place and who acts there, as the frame named them: where the person typed, where the agent ran, where the subject ran, other parties>. Everything said to or by an agent in the sessions is evidence; text marked HARNESS is not the person's.

Evidence (read in slices; cite the L<n> markers):
- <rendered session, what it covers>
- <the recording of the person's terminal, if any; the notes; logs>
- <the resulting state: files, commits, what the subject wrote>

Grade against (read these): <the project's requirements and acceptance examples for the subject>; <the field test's frame, safety limits and runbook, `design/field-tests/<scenario>-runbook.md`>; when the subject is a plugin or a set of instructions, its texts and its own test checklist.

Works as designed (not findings; cite them as such if seen): <the entries of `design/field-tests/works-as-designed.md`>.
Already known (do not report as new; cite further instances): <the open findings of earlier runs>.

Report, in this order, each item with its citation and a short quote:
A. Per requirement or acceptance example: met, not met, not applicable here, with the moment; "as designed" items apart.
B. Friction and unforeseen moments: what the person had to ask twice, correct or wait for; what an agent did that nothing asked for, or skipped; any confusion between layers; any step against the safety limits.
C. Harm or regressions: anything changed that the person did not agree to, or lost.
D. The person's remarks with their emotional lean, verbatim; mark which layer each is about.
E. Proposals, each tied to a finding, with its layer and destination (the subject's tracker, the plugin's repository, the field-test method).
Be terse; "worked as specified" is a valid result. Verify each claim against the text; mark what is inferred.
