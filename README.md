# Schema Coverage Lab

Research into MC/DC-inspired semantic test coverage for JSON Schema Draft 2020-12.

The objective is to determine which schema decisions admit meaningful independence obligations, derive a qualified set-theoretic model, and test its practical usefulness without assuming that the hypothesis is true. The proposed metric is **semantic unique-cause independence coverage**. It is distinct from validator source-code MC/DC and carries no certification claim.

## Research and handoff

This navigation describes the complete staged stack. Files belonging to later stages appear only on their branches until reviewed and merged; links to those files are therefore intentionally pending on earlier branches.

| Stage | Deliverable | Tracking |
|---|---|---|
| 1 | [MC/DC definitions and implementations](docs/research/01-mcdc.md) | Issue #1; `research/01-mcdc-foundations` |
| 2 | [Draft 2020-12 semantics and counterexamples](docs/research/02-json-schema.md), [fixtures](research-fixtures/schema-semantics.json) | Issue #2; `research/02-schema-semantics` |
| 3 | [Set model and proof sketches](docs/research/03-set-model.md), [finite research checks](research-checks/check_semantic_model.py) | Issue #3; `research/03-set-model` |
| 4 | [Codex handoff](CODEX_HANDOFF.md), [research report](docs/research/REPORT.md), [sources](docs/research/SOURCES.md), [uncertainties](docs/research/04-uncertainties.md), [roadmap](docs/ROADMAP.md) | Issue #4; `handoff/04-codex-plan` |
| 5 | [Later implementation and testing plan](docs/IMPLEMENTATION_PLAN.md) | Issue #5; `plan/05-implementation-testing` |

Draft PRs are stacked in stage order. Each targets the preceding branch; stage 1 targets `main`. No automatic merges. Only a minimal bootstrap README was committed directly to the initially empty `main` so GitHub could accept PRs.

## What has been verified

Primary-source research, original derivations and counterexamples are documented as of 2026-11-08. A dependency-free mathematical check verifies finite Boolean/set identities:

```sh
python3 research-checks/check_semantic_model.py
```

Expected result: `PASS: 197314 finite identity assertions across 65808 function/realizability models`.

This is research verification, not a JSON Schema validator or production coverage engine. The JSON fixture expectations were derived from the specification and syntax-checked; they have not yet been run against an independent validator. Production implementation, validator conformance, generation scalability and comparative experiments remain later work.
