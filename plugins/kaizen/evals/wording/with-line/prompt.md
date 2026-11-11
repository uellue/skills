---
description: "Ledger 297 (Alex Clausen's wording review, folded in for 0.6): a term coined in the session ('the attic') must not leak into an error message a user reads, and the message says what to do. A guard against getting worse: without the line it passed too (2026-11-11), so it does not show the line's effect."
max_turns: 8
allowed_tools: [Read, Glob, Grep, Edit, Write]
---

We've been calling ~/.cache/tally "the attic" all morning. Add a check to tally.py: if the attic isn't writable, stop with an error message instead of a traceback. Keep it small, no tests needed.
