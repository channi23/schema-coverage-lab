# Schema Coverage Lab

**Read the complete study:** [9-page manuscript](paper/manuscript.pdf), [editable source and reading guide](paper/README.md), and [publication review](docs/PUBLICATION_REVIEW.md).

Research into MC/DC-inspired semantic test coverage for JSON Schema Draft 2020-12.

The objective is to determine which schema decisions admit meaningful independence obligations, derive a qualified set-theoretic model, and test its practical usefulness without assuming that the hypothesis is true. The proposed metric is **semantic unique-cause independence coverage**. It is distinct from validator source-code MC/DC and carries no certification claim.

## Research and handoff

All research and planning stages are consolidated on `main`. Stages 1–4 are complete as research/handoff deliverables; stage 5 now has the completed bounded generator, analyzer, reducer and reproducible offline study.

| Stage | Deliverable | Tracking |
|---|---|---|
| 1 | [MC/DC definitions and implementations](docs/research/01-mcdc.md) | Issue #1; `research/01-mcdc-foundations` |
| 2 | [Draft 2020-12 semantics and counterexamples](docs/research/02-json-schema.md), [fixtures](research-fixtures/schema-semantics.json) | Issue #2; `research/02-schema-semantics` |
| 3 | [Set model and proof sketches](docs/research/03-set-model.md), [finite research checks](research-checks/check_semantic_model.py) | Issue #3; `research/03-set-model` |
| 4 | [Codex handoff](CODEX_HANDOFF.md), [research report](docs/research/REPORT.md), [sources](docs/research/SOURCES.md), [uncertainties](docs/research/04-uncertainties.md), [roadmap](docs/ROADMAP.md) | Issue #4; `handoff/04-codex-plan` |
| 5 | [Later implementation and testing plan](docs/IMPLEMENTATION_PLAN.md) | Issue #5; `plan/05-implementation-testing` |

PRs #6–#10 are merged. Stage 2 originally merged into the stage 1 branch and reached `main` through PR #8. Per the user's subsequent instruction, new work goes directly to `main` in focused, documented commits. The original staged branches remain historical references.

## Current work and evidence

- [Project status](docs/STATUS.md): completed deliverables, remaining work, and issue links.
- [Roadmap](docs/ROADMAP.md): the implementation sequence and acceptance gates.
- [Documentation policy](docs/DOCUMENTATION_POLICY.md): required records for every change and experiment.
- [Evidence log](docs/EVIDENCE_LOG.md): actions taken, commands, results, source revisions, and limitations.
- [Codex project instructions](AGENTS.md): persistent workflow and documentation requirements.

Issues #1–#4 are complete. Issue #5 is closed with bounded acceptance evidence: generation, analysis, reduction/replay and a reproducible study. Full-draft support and scholarly publication claims remain outside that completed scope.

## Run the prototype

From the repository root:

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --require-hashes -r requirements.lock
python tools/verify.py
python -m schema_coverage_lab analyze --schema examples/conjunction.schema.json --corpus examples/conjunction.instances.json --output results/example.json
python -m schema_coverage_lab replay --report results/example.json
```

See [usage](docs/USAGE.md), [architecture](docs/ARCHITECTURE.md), and the [recorded verification manifest](results/milestone-1/manifest.json). Tested runtime: Python 3.14.2, macOS arm64. Analysis/replay run offline after dependency installation.

## What has been verified

Primary-source research, original derivations and counterexamples are documented as of 2026-11-08. A dependency-free mathematical check verifies finite Boolean/set identities:

```sh
python3 research-checks/check_semantic_model.py
```

Expected result: `PASS: 197314 finite identity assertions across 65808 function/realizability models`.

The finite script is research verification, separate from the implemented bounded coverage engine. Milestone 1 passed 86 regression tests, 295 admitted official-suite tests (52 explicitly excluded), and all 43 research-fixture expectations through an independent pinned validator. The example covers two obligations and replays successfully. These are subset/observed-witness results, not full-draft conformance, unbounded feasibility or demonstrated practical superiority. Generation, reduction and comparative experiments remain later work.


## Completed bounded study

Version 0.2.0 adds deterministic generation, pair-aware greedy/exact-small-pool reduction and replayable reduction bundles. 105 regression tests pass. A frozen 32-subject study produced 2304 equal-budget rows. On 21 subjects with witnessed independence targets, reduction retained all 50 targets while selecting 64 tests from 451 candidates. This does not establish a minimum or superior fault detection: at budget 8, pair-guided mutation coverage was 76.63%, below random 77.59% and boundary-first 91.86% on the declared probe.

Run `python tools/run_experiments.py`, then `python tools/audit_artifacts.py` after a recorded verification run. See [protocol](benchmarks/README.md), [raw summary](results/milestone-2/summary.json), [usage](docs/USAGE.md) and [publication review](docs/PUBLICATION_REVIEW.md). The compiled manuscript and editable source package are under paper/. It is an author-review draft, not a submitted or peer-reviewed publication.
