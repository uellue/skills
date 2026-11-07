# Rule ablation: leave one rule out

Does a given rule of a skill change what the agent does, and can its effect be told in advance? Ledger 204 (needs 3 and 4: the expected effect of a change, and removal instead of addition), 214 (the eval suite it runs) and 215 (expected effects written before the run).

## Method

1. A variant in `variants.json` names one exact text of the plugin to remove and the eval case it bears on.
2. The expected effect is written into the variant and committed **before** the run; the commit's time shows it came first. The agent's and the principal's expected effects are kept apart, to compare them.
3. `ablate.py` copies the plugin without that text into a new directory, and the case runs there with the plugin only (no baseline), three runs.
4. The observed grader counts go into `observed`; the baseline is the with-arm of the first comparison (`plugins/kaizen/evals/README.md`), every grader 3 of 3.

## Run

    python3 benchmarks/rule-ablation/ablate.py --list
    python3 benchmarks/rule-ablation/ablate.py no-blocks /tmp/ablation/no-blocks
    # then the eval command it prints

The copy is outside this repository, so the first eval run in it asks to trust the directory. About $0.45 for a variant of `asks-for-persona`, $1 for `walks-confirmed-persona` (three runs each, by the first comparison's costs).

## Limits

Three runs per variant: an effect of one run in three is noise. One situation per rule: a rule that changes nothing here may act elsewhere (the parameter space). The graders see only what they check; a removal can shift behaviour no grader looks at.
