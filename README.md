# Schema Coverage Lab

Research into MC/DC-inspired semantic test coverage for JSON Schema Draft 2020-12.

The objective is to determine which schema decisions admit meaningful independence obligations, derive a qualified set-theoretic model, and test its practical usefulness without assuming that the hypothesis is true. The proposed metric is **semantic unique-cause independence coverage**. It is distinct from validator source-code MC/DC and carries no certification claim.

## Research and handoff

All research and planning stages are consolidated on `main`. Stages 1–4 are complete as research/handoff deliverables; stage 5 has a completed plan but its implementation and experiments remain outstanding.

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

Issues #1–#4 are complete. Issue #5 remains the implementation/testing backlog; merging its planning document does not complete the prototype.

## What has been verified

Primary-source research, original derivations and counterexamples are documented as of 2026-11-08. A dependency-free mathematical check verifies finite Boolean/set identities:

```sh
python3 research-checks/check_semantic_model.py
```

Expected result: `PASS: 197314 finite identity assertions across 65808 function/realizability models`.

This is research verification, not a JSON Schema validator or production coverage engine. The JSON fixture expectations were derived from the specification and syntax-checked; they have not yet been run against an independent validator. Production implementation, validator conformance, generation scalability and comparative experiments remain later work.
