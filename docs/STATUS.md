# Project status

Updated 2026-11-09 (Asia/Kolkata).

## Completed

- Research and handoff stages 1–4: MC/DC definitions/implementations, Draft 2020-12 inventory and counterexamples, qualified set model, sources, uncertainties and Codex handoff.
- All original PRs #6–#10 are merged. Stage 2 reached `main` through #8 after its earlier merge into the stage 1 branch.
- Stage 5 planning and its first corpus-analysis milestone are complete; generation, reduction and experiments remain outstanding.
- Finite-model research checker rerun: 197314 assertions across 65808 function/realizability models passed, exit 0.
- Repository-wide documentation policy and persistent project instructions added.
- Milestone 1: supplied-corpus analyzer, pure-v1 evaluator, support checker, local decision catalog, strict witness pairs, domain-qualified reports and independent oracle replay are implemented.
- Hash-locked dependencies installed into a fresh environment from local packages; no package retrieval during verification. Tested Python 3.14.2, macOS arm64.
- 86 pytest regressions, 295 admitted official-suite cases and all 43 research-oracle expectations passed. 52 official cases were explicitly excluded for unsupported schemas. The example replays two covered obligations.
- Usage, architecture and machine-readable source/environment/artifact evidence are available in [usage](USAGE.md), [architecture](ARCHITECTURE.md) and [verification manifest](../results/milestone-1/manifest.json).

## Open work

[Issue #5](https://github.com/channi23/schema-coverage-lab/issues/5) remains open for candidate generation, pair-aware suite reduction and comparative experiments. The admitted corpus analyzer and oracle integration are complete for this milestone. No global feasibility solver, full-draft support, practical superiority result or release is claimed.

Follow the [implementation plan](IMPLEMENTATION_PLAN.md), [roadmap](ROADMAP.md) and [Codex handoff](../CODEX_HANDOFF.md). The original consolidation did not implement the prototype; the subsequent milestone recorded here does.

## Current workflow

Work directly on `main`, in focused commits with accompanying documentation and evidence. This user instruction supersedes the original stacked draft/no-merge process. Preserve historical PRs/issues; close completed issues #1–#4 and keep #5 open until acceptance evidence exists. See [documentation policy](DOCUMENTATION_POLICY.md) and [evidence log](EVIDENCE_LOG.md).
