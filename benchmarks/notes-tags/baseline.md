# Baseline: 2026-11-05

Plugin: kaizen as of commit `b50c1df` (0.4 before the comparison's proposals and the independent review). OpenSpec 1.16.0. The three condition agents ran Opus 5.5; in condition A, the agent chose Sonnet 5.5 for its implementer and its hallway tester (so K9 was found by a Sonnet tester); C's hallway tester inherited Opus. One run per condition. Graded by the orchestrating session from the three reports, not blind: the next run should use a blind grader (see README). "Not reported" means the report does not mention it, not that the run missed it for sure.

| Key | A: kaizen alone | B: OpenSpec alone | C: both |
|---|---|---|---|
| K1 need behind tags | found (requirements: need before solution) | missed: "tags" became a capability; named only in the agent's critique afterwards | found (requirements, walk-through) |
| K2 lost updates | found, measured (walk against the running tool) | found, measured (agent's own initiative) | found, measured (walk) |
| K3 torn file | found, measured (walk) | found, measured | found, measured (walk) |
| K4 ID reuse | found (walk; made "IDs never reused" a requirement) | missed by the process: the validated design accepted it; named only in the critique | found (walk) |
| K5 group drive | found (open question that conditions the build) | not reported | found (decided the design) |
| K6 symlink replaced | not reported | not implemented | found by the hallway test, outside all ten scenarios |
| K7 mode and owner reset | not reported | not implemented | found by the hallway test |
| K8 unquoted tag | found (developer hat) | not reported | not reported |
| K9 duplicate IDs | found by the hallway test, outside the implementer's 12 green tests | not implemented | not reported |
| K10 old clients | found (measured that the old version keeps unknown keys) | not reported | not reported |

Process measures:

- **Invented decisions:** A's implementer, working from the kaizen documents alone, listed 21 decisions no document settled (interface, data format, constants, search semantics, scope). B and C had a specification step (OpenSpec's design and specs).
- **Size:** C wrote 34 KB of records for a 4 KB tool; A about 4,400 words of design for a 35-line tool. B 12.7 KB.
- **Wrong findings:** A's tester claimed a stale lock blocks forever; the main session refuted it (the tester had waited 10 s, the takeover is at 60 s).
- **Validation:** `openspec validate --strict` passed every change, and also a one-line proposal with an untestable scenario (checked separately).
- **Cost**, output tokens from `usage.py`, counted once per API message, each condition agent plus its nested agents: A 56 k (35 k Opus, 10 k implementer and 10 k tester on Sonnet); B 24 k, no implementation; C 52 k (42 k, plus 10 k for the hallway tester). The harness's own per-agent totals at completion were A 118 k, B 104 k, C 157 k; they measure more than output and are not comparable with `usage.py`.

What this one run suggests, not shows (one run per condition, graded by the orchestrator, see Limits in the README): the content findings (K1, K4, K5) came from the requirements and walk-through habits; OpenSpec added structure and a home for decisions; the hallway tests found implementation defects (K6, K7, K9) that the scenarios and green tests missed. The changes made in response (decision record, one list of examples with IDs, small-change path, OpenSpec hand-off) are in `design/kaizen.md`, proposals 22 to 29; the next run shows whether they hold.
