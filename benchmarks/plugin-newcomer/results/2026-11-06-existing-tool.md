# Run 2026-11-06: scenario existing-tool, commit `1b09667`, Opus, 10,516 output tokens, 2.2 minutes

Result format: E15. Graded by the main session that had changed the skills (not blind). The tester got its brief through a file it was told to read (same text as `brief.py` printed); the claims the new findings rest on were checked with a grep each.

| # | Result |
|---|---|
| N1 | held: the README's hallway-test line led straight there |
| N2 | held |
| N6 | not reached |
| N7 | held: announced |
| N8 | held: a read-only tool, no stand-in needed; the logs copied with links resolved |
| N9 | not reached |
| N10 | held for the tester |
| N13 | held: directly, no detour through the playbook |
| N14 | held |
| N15 | held: one question, "not on record", no default |
| N16 | held: stated, the Opus figure called a guess |

Compared with run 2 (`ba2fbd8`): the detour through the playbook is gone; N10 and N16 from partly to held.

New findings (ledger 97 to 99): the After section never offers the requirements reconstruction that item 2 promises; "I don't know" to the persona question leads nowhere; a one-file tool is its own source, so the tester needs a copy to run and a rule not to read it.

Setup misfit (tester): a read-only tool never exercises the safety path.
