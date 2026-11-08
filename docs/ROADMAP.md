# Research and implementation roadmap

Updated 2026-11-08 (Asia/Kolkata). The user authorized merging all completed research/planning PRs and requested future work directly on `main`. This supersedes the initial stacked-draft workflow.

| Stage | Issue | Current result | Evidence / next gate |
|---|---|---|---|
| 1: MC/DC foundations | [#1](https://github.com/channi23/schema-coverage-lab/issues/1) | Complete; PR #6 merged | Formal criterion, variants, coupling, tool qualifications and primary citations. |
| 2: Schema semantics | [#2](https://github.com/channi23/schema-coverage-lab/issues/2) | Complete as research; PR #7 merged into the stage 1 branch, then brought to main by #8 | Keyword inventory and specification-derived fixtures; oracle execution remains stage 5. |
| 3: Set model | [#3](https://github.com/channi23/schema-coverage-lab/issues/3) | Complete as research; PR #8 merged to main | Proof sketches and finite checker; no global feasibility or conformance claim. |
| 4: Codex handoff | [#4](https://github.com/channi23/schema-coverage-lab/issues/4) | Complete; PR #9 merged to main | Bounded scope, architecture, report contract and acceptance criteria. |
| 5: Prototype and testing | [#5](https://github.com/channi23/schema-coverage-lab/issues/5) | Plan merged via #10; implementation outstanding | Follow [implementation plan](IMPLEMENTATION_PLAN.md) and [handoff](../CODEX_HANDOFF.md). |

## Next implementation sequence

1. Freeze the exact environment, validator versions, numeric policy and official-suite commit. Save a lockfile, source revisions and experiment manifest.
2. Implement the admitted pure-fragment evaluator and decision catalog. Reject unsupported semantics explicitly.
3. Analyze corpora, retain observations, identify strict witness pairs, and replay endpoints through an independent oracle.
4. Add deterministic finite candidate generation and pair-aware suite selection. Preserve domain-qualified unknown/infeasible statuses.
5. Run reproducible tests and equal-budget comparisons. Report negative findings and uncertainty as well as successes.

These are planned tasks, not completed results. Close issue #5 only when its implementation and testing acceptance evidence exists. Every increment must update [status](STATUS.md) and [evidence](EVIDENCE_LOG.md) alongside code; follow the [documentation policy](DOCUMENTATION_POLICY.md). Documentation supports traceability but does not itself prove correctness.
