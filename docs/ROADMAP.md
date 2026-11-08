# Staged review roadmap

Research date: 2026-11-08. No stage is permission to merge automatically. The five open issues track deliverables, not claims that later implementation has already happened.

| Stage | Issue | Branch | Draft PR base | Review gate |
|---|---|---|---|---|
| 1: MC/DC foundations | #1 | `research/01-mcdc-foundations` | `main` | Check formal criterion, variants, feasible domains and tool qualifications. |
| 2: Schema semantics | #2 | `research/02-schema-semantics` | stage 1 branch | Check keyword inventory and counterexample expectations against Draft 2020-12. |
| 3: Set model | #3 | `research/03-set-model` | stage 2 branch | Review proofs, pair feasibility, reporting denominator and finite evidence. |
| 4: Codex handoff | #4 | `handoff/04-codex-plan` | stage 3 branch | Agree initial fragment, output contract and acceptance tests. |
| 5: Later implementation/testing plan | #5 | `plan/05-implementation-testing` | stage 4 branch | Review plan; implementation and empirical results are still outstanding. |

The full research is visible cumulatively on stages 4 and 5. Review individual diffs in order. If the user later merges an earlier stage, retarget the next PR to `main` and inspect its diff before review; preserve ancestry or rebase carefully rather than force-moving shared branches without checking their heads. Do not merge or close dependent work automatically.

Stage 5 initially contains planning only. Follow-up implementation commits should be split into supported-fragment analysis, witness generation/reporting, then reproducible testing/experiments. Research questions that fail should be recorded as negative results rather than changing denominators to improve a score.
