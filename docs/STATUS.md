# Project status

Updated 2026-11-09 (Asia/Kolkata).

## Completed

- Research and handoff stages 1–4: MC/DC definitions/implementations, Draft 2020-12 inventory and counterexamples, qualified set model, sources, uncertainties and Codex handoff.
- All original PRs #6–#10 are merged. Stage 2 reached `main` through #8 after its earlier merge into the stage 1 branch.
- Stage 5 planning and its first corpus-analysis milestone are complete; the bounded generation/reduction/experiment continuation is now complete (see below).
- Finite-model research checker rerun: 197314 assertions across 65808 function/realizability models passed, exit 0.
- Repository-wide documentation policy and persistent project instructions added.
- Milestone 1: supplied-corpus analyzer, pure-v1 evaluator, support checker, local decision catalog, strict witness pairs, domain-qualified reports and independent oracle replay are implemented.
- Hash-locked dependencies installed into a fresh environment from local packages; no package retrieval during verification. Tested Python 3.14.2, macOS arm64.
- 86 pytest regressions, 295 admitted official-suite cases and all 43 research-oracle expectations passed. 52 official cases were explicitly excluded for unsupported schemas. The example replays two covered obligations.
- Usage, architecture and machine-readable source/environment/artifact evidence are available in [usage](USAGE.md), [architecture](ARCHITECTURE.md) and [verification manifest](../results/milestone-1/manifest.json).

## Open work

[Issue #5](https://github.com/channi23/schema-coverage-lab/issues/5) now meets its bounded implementation/testing acceptance conditions: deterministic generation, pair-aware reduction, replay and reproducible offline comparisons are implemented. It can be closed after publication verification. The manuscript is a draft for author review, not a peer-reviewed or submitted publication. No global feasibility solver, full-draft support, practical superiority result or release is claimed.

Follow the [implementation plan](IMPLEMENTATION_PLAN.md), [roadmap](ROADMAP.md) and [Codex handoff](../CODEX_HANDOFF.md). The original consolidation did not implement the prototype; the subsequent milestone recorded here does.

## Current workflow

Work directly on `main`, in focused commits with accompanying documentation and evidence. This user instruction supersedes the original stacked draft/no-merge process. Preserve historical PRs/issues; issues #1–#4 are complete and #5 has bounded acceptance evidence in E-0003. See [documentation policy](DOCUMENTATION_POLICY.md) and [evidence log](EVIDENCE_LOG.md).


## Completed continuation (version 0.2.0)

- Deterministic candidate generation with visible caps/reasons; pair-aware greedy reduction and bounded exact enumeration (<=16 candidates).
- Source/reduced report bundles are independently replayed; expanded artifacts must remain within loader limits.
- 105 regression tests; existing 295 admitted official cases and 43 original oracle fixtures remain passing.
- Frozen 32-subject / 2304-row offline study: 630 candidate inputs; 69 condition obligations, 50 witnessed in their pools and 19 pool-absent. Twenty-one target-bearing subjects reduced 451 inputs to 64, preserving all 50 witnessed obligations.
- 177 admitted mutants: 139 pool-distinguishable, 38 pool-indistinguishable; no global equivalence inference. At budget 8, pair-guided mutation coverage 76.63% trails random 77.59% and boundary-first 91.86%.
- Raw artifacts, source/environment hashes, per-case reduction evidence and a full budget/metric audit are saved under results/milestone-2 and results/audits.

Full-draft support, global solvers, representative real-schema validation and scholarly novelty remain outside these completed bounded claims. Publication materials and author-review requirements are recorded in docs/PUBLICATION_REVIEW.md.
