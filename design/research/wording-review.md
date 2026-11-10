# A wording pass for text other people read

Source: a snippet by ales (GitHub sk1p), a colleague of the principal, shared on 2026-11-10 with permission to fold it into kaizen as appropriate and to be named. Kept here verbatim until it has its place (ledger row 297).

> ## Review the wording of text that other people will read
>
> Text written for users, developers or administrators gets a second pass
> before I count it as done. That includes error and log messages, CLI help,
> UI strings, docs and READMEs, docstrings, config comments, commit messages,
> and PR or issue text. Reread it as the person it's for, who hasn't seen our
> conversation, and fix whatever fails these checks:
>
> - It's correct, and it says what happened or what the reader should do next.
> - It doesn't depend on context the reader lacks, such as terms coined during
>   the session, internal names or "as discussed".
> - It's as short as it can be without losing meaning. No filler, no hedging.
> - It uses one term for each thing, consistent with the rest of the codebase.
> - The spelling, grammar and tone suit the audience.
>
> Why: labels, log messages and other text often had to be corrected by hand
> afterwards.
