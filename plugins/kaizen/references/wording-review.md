# Wording review

A second pass over text that other people will read, written by Alex (Alexander Clausen, GitHub sk1p), a colleague at ER-C, and folded into kaizen with his permission, with thanks. Its reason, in his words: labels, log messages and other text often had to be corrected by hand afterwards.

Who uses it: the agent, before it counts such text as done (the standing instructions carry it as one line); an independent review of a change, for the text the change shows people; a hallway test's tester, as one extra pass over the messages, help and documents of the subject. The standing line is the short form of the text below; the two must agree.

His text, as he wrote it:

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

A reviewer or tester reports each failing text with where it stands, which check it fails, and the reader it fails for.
