# Research and implementation roadmap

Updated 2026-11-09 (Asia/Kolkata). The user authorized merging all completed research/planning PRs and requested future work directly on `main`. This supersedes the initial stacked-draft workflow.

| Stage | Issue | Current result | Evidence / next gate |
|---|---|---|---|
| 1: MC/DC foundations | [#1](https://github.com/channi23/schema-coverage-lab/issues/1) | Complete; PR #6 merged | Formal criterion, variants, coupling, tool qualifications and primary citations. |
| 2: Schema semantics | [#2](https://github.com/channi23/schema-coverage-lab/issues/2) | Complete as research; PR #7 merged into the stage 1 branch, then brought to main by #8 | Keyword inventory and specification-derived fixtures; oracle execution remains stage 5. |
| 3: Set model | [#3](https://github.com/channi23/schema-coverage-lab/issues/3) | Complete as research; PR #8 merged to main | Proof sketches and finite checker; no global feasibility or conformance claim. |
| 4: Codex handoff | [#4](https://github.com/channi23/schema-coverage-lab/issues/4) | Complete; PR #9 merged to main | Bounded scope, architecture, report contract and acceptance criteria. |
| 5: Prototype and testing | [#5](https://github.com/channi23/schema-coverage-lab/issues/5) | Bounded implementation and offline experiments complete; author-review manuscript follows | Follow [implementation plan](IMPLEMENTATION_PLAN.md), [usage](USAGE.md) and [handoff](../CODEX_HANDOFF.md). |

## Next implementation sequence

1. Completed: exact environment, validator versions, numeric policy and official-suite commit recorded in a hash lock and experiment manifest.
2. Completed: admitted pure-fragment evaluator and decision catalog; explicit unsupported diagnostics.
3. Completed: supplied-corpus observations, strict witness pairs and independent endpoint replay.
4. Completed: deterministic finite candidate generation and pair-aware suite selection; unknown/infeasible statuses preserve their domains.
5. Completed: reproducible tests and equal-budget comparisons, including the negative mutation result and explicit uncertainty.

All five bounded implementation steps have executed evidence in E-0003; full-draft expansion and stronger external validation remain research opportunities. Close issue #5 only when its full implementation/testing acceptance evidence exists. Every increment must update [status](STATUS.md) and [evidence](EVIDENCE_LOG.md) alongside code; follow the [documentation policy](DOCUMENTATION_POLICY.md). Documentation supports traceability but does not itself prove correctness. Milestone 1 results and limitations are recorded in [the evidence manifest](../results/milestone-1/manifest.json).
