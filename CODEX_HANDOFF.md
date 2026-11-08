# Codex handoff: implement a bounded semantic coverage experiment

Prepared 2026-11-08. Read [the research report](docs/research/REPORT.md), chapters [1](docs/research/01-mcdc.md), [2](docs/research/02-json-schema.md), [3](docs/research/03-set-model.md), [uncertainties](docs/research/04-uncertainties.md) and [roadmap](docs/ROADMAP.md) before implementation. Issue #4 tracks this handoff; issue #5 tracks later implementation and experiments. No PR may be merged automatically.

## Objective and stop condition

Build a reproducible prototype that reports **semantic unique-cause independence coverage** for explicitly selected local schema decisions and concrete JSON instances. Generate and replay witness pairs within a declared finite candidate domain. Establish sound observed evidence and expose incompleteness. Do not advertise full Draft 2020-12 coverage, masking MC/DC, validator code coverage, certification, guaranteed minimal suites, or demonstrated fault-detection superiority.

Initial completion means the supported-fragment engine, independent oracle checks, deterministic report contract, rejection behavior and required regression cases pass in a reproducible environment. Broader schema support is a later stage, not grounds to delay or silently widen this contract.

## Freeze the implementation contract first

Use Python for the initial prototype unless repository review selects another language. Before adding dependencies, record the exact Python version, package versions with lockfile/hashes, OS/architecture and numerical representation. Select a maintained validator exposing Draft 2020-12 validation (a candidate is Python `jsonschema` with an explicitly selected `Draft202012Validator`), then pin its exact version and transitive resolution. No version is prescribed as already tested by this research. Pin the JSON Schema Test Suite to an immutable commit SHA, retain its license/attribution if copying cases, and record selected paths and exclusions. Record schema and corpus digests, seeds, resource limits, format policy and registry policy in every result. Do not execute remote schema retrieval implicitly.

Validate input schemas against the declared meta-schema, then run a separate analyzer allowlist check. Meta-schema-valid does not imply analyzer-supported. Reject duplicate JSON object keys, nonfinite numbers and invalid JSON before semantic analysis. Define JSON equality structurally with numeric equality under the instance data model: booleans are not numbers, `1` and `1.0` represent integer-valued numbers, and object key order is irrelevant. Avoid host-language equality shortcuts. Use exact decimal/rational handling for admitted numeric values or reject values that cannot be represented faithfully by the chosen evaluator/oracle contract.

## MVP supported fragment

Support Boolean schemas; empty objects; `type` (including allowed type arrays), `const`, `enum`; `minimum`, `maximum`, `exclusiveMinimum`, `exclusiveMaximum`; and recursive `allOf`, `anyOf`, `oneOf`, `not` when all subtrees stay within this fragment. A `type` assertion can inspect any JSON value, including arrays and objects; this does not imply support for their structural keywords. `const`/`enum` require correct recursive JSON equality. `multipleOf` is deferred until exact arithmetic and oracle parity are demonstrated.

Recognize the Draft 2020-12 `$schema` declaration. Permit documented, inert metadata (`title`, `description`, `$comment`) without creating condition obligations. Treat all other keywords as unsupported for analysis in the MVP, including `$ref`, `$dynamicRef`, `$id`, `$defs`, custom vocabularies, `if`/`then`/`else`, object/array/string structural keywords, `format`, content keywords and `unevaluated*`. This conservative analyzer policy is stricter than general JSON Schema's extension behavior. Return explicit keyword paths/reasons; do not silently strip unknown keywords, treat them as false, or claim whole-schema support from a supported subtree.

No symbolic all-JSON feasibility solver is required in the MVP. Candidate-pool infeasibility is allowed only with its domain visibly attached. Keep global feasibility unknown unless a separately reviewed proof rule applies.

## Architecture and data flow

1. **Loader/contract:** strict JSON parsing, meta-schema validation, dialect/configuration and SHA-256 digests. Return input errors separately from coverage results.
2. **Support checker:** recursive keyword allowlist and semantic configuration checks, returning path-specific reasons. Do this before generating a report advertised as supported.
3. **Local evaluator:** independently implement the admitted pure semantics with total Boolean outcomes for admitted inputs. Use numeric applicability correctly: numeric assertions pass on nonnumbers. Preserve source locations; do not deduplicate identical occurrences.
4. **Decision catalog:** create one local decision for each `allOf`, `anyOf`, `oneOf` and `not` occurrence. Its ordered conditions are immediate child assertion outcomes (`not` has one). Atomic schemas contribute validity observations but no invented leaf-independence obligations. Multiple keywords at a schema object remain sibling conjunction for validity; the MVP does not flatten them into additional condition coordinates. This catalog choice deliberately limits the metric and must appear in reports.
5. **Observation collector:** evaluate every selected pure child semantically, even if an oracle internally short-circuits. Mark this as semantic evaluation, never evidence of validator execution. Persist child vector, local logical result and complete root result for each concrete input.
6. **Pair engine:** group compatible observations by decision ID, contract and domain; find pairs that differ in exactly the target coordinate and flip the local decision. Deterministic vector indexing is preferable to repeated all-pairs scanning. Retain both concrete endpoints.
7. **Candidate generator:** begin with user-supplied finite corpus and deterministic literal/boundary candidates. Derive candidates from `const`/`enum`, numeric bounds, relevant type representatives and schema literals; record generation recipe and limits. This heuristic is incomplete. An explicit finite-domain mode enumerates exactly the declared domain.
8. **Suite selector:** initially retain the supplied suite or use a deterministic pair-aware greedy reduction. Credit an obligation only after both endpoints are selected. Report achieved coverage and distinct-test count; do not claim optimality. An optional exact finite-pool optimizer must state its objective and pool bound.
9. **Oracle adapter/replay:** independently validate each root and relevant child schema on each reported endpoint using the pinned oracle/configuration. The MVP has no contextual child dependencies, so standalone child validation is legitimate here. Compare full vectors and logical outputs, not error-message strings. Oracle disagreement is an analysis failure requiring investigation.
10. **Reporter/CLI:** stable JSON output plus concise human summary, deterministic ordering, and reproducible artifacts. Keep generator, coverage engine and validation oracle separate so shared errors are easier to detect.

Suggested package boundaries are `model`, `loader`, `support`, `evaluate`, `catalog`, `observe`, `pairs`, `generate`, `select`, `oracle`, and `report`; these are responsibilities rather than a demand for ten separate files. Reuse existing repository structure if later work adds one.

## Identity and result contract

A decision identity includes schema digest, canonical schema resource identity, JSON Pointer to the logical keyword, occurrence path, criterion/catalog version and evaluation-context class. A condition adds its immediate-child index. The MVP uses the root instance location and no references; future work must add instance location and reference/dynamic-scope paths rather than grouping incompatible evaluations. Do not infer identity only from schema text or `$id` strings. Persist concrete instances with stable IDs and content digests; define canonical serialization explicitly rather than assuming host serialization is universal.

Each report includes `report_version`, dialect, supported-fragment version, criterion name, decomposition, evaluator/oracle versions, configuration, original schema digest, domain kind and description, generation/search limits, suite IDs, candidate IDs, completeness scope, and status counts. Each obligation includes decision/condition IDs, local function, status, proof/search scope, evidence, and any unsupported reason. Each observation includes input ID, vector, local result, root result and evaluation status. Each witness includes both IDs, target index, vectors, local outcomes and replay result. Do not claim root independence from a local pair; root validity is supplemental information.

Obligation statuses are mutually exclusive:

| Status | Evidence required |
|---|---|
| `covered` | An eligible, oracle-replayed pair with both endpoints in selected suite. |
| `feasible_uncovered` | A validated pair exists in the candidate pool/evidence store, but is absent from selected suite. |
| `proven_infeasible` | Proof of no eligible pair in the stated domain; retain proof kind and scope. Complete finite enumeration proves only candidate-domain infeasibility. |
| `unknown` | No pair/proof; search incomplete, exhausted its budget or timed out. |
| `unsupported` | Analyzer cannot interpret the semantics needed for this occurrence; preserve path/reason. |

Invalid schemas, unresolved resources, input errors and evaluator failures are report-level failures rather than valid=false observations or proven infeasibility. If analysis is unsupported before a complete catalog can be built, return `analysis_status: unsupported`, report diagnostic locations, and mark catalog completeness false; give no misleading global percentage. A constant schema has zero condition obligations and N/A independence coverage, although its observed validity is still useful. Absence/inactivity and runtime skipped states must never be encoded as semantic false in future richer fragments.

For a complete fixed catalog O, show all five counts, catalog completeness and scope. Raw coverage is `covered/|O|`. A separate feasibility-adjusted score can exclude only obligations proved infeasible **in the score's stated universe**; retain unknown and unsupported in its denominator. Candidate-pool proofs cannot reduce an all-JSON denominator. A witnessed-feasible-only ratio must be labeled exactly that and cannot imply global adequacy. Every zero denominator is N/A. Keep a fixed contract/catalog when comparing suites. Adding tests cannot reduce pair coverage; combining run percentages or just unioning already-covered obligation IDs can lose pairs whose endpoints came from different runs.

## Mandatory regression cases

Use both original fixture catalogs, preserving their status as research-derived expectations until oracle execution. Duplicate overlap cases across catalogs are intentional semantic cross-checks. For unsupported schemas test explicit rejection rather than pretending MVP supports them.

| Case | Required check |
|---|---|
| `allOf` of integer and minimum | Realizable strict pairs; numeric applicability including nonnumbers. |
| `anyOf` duplicate integer children | Both conditions coupled; no unique-cause pair. |
| `allOf` minima 0 and 10 | Weaker bound cannot independently flip result; stronger has witnesses. |
| Contradictory `const` conjuncts | Root always false; no strict pair despite child outcomes. |
| `anyOf` with `true` | Root always true; branch observation alone is insufficient. |
| `oneOf` three `true` children | Exactly-one differs from odd parity; always false. |
| Vectors `{00,11}` for conjunction | Predicate and decision outcomes occur without independence. |
| Split suites with opposite endpoints | Combined suite acquires pair absent from each suite separately. |
| Inner decision under outer `false` | Local coverage never labeled root influence. |
| Empty catalog, unknown search, unsupported input | N/A, preserved counts and failure/status distinctions. |
| Pair reduction | Selected suite contains both endpoints for every credited obligation. |
| Annotation, conditional, references fixtures | Oracle validates expectations; MVP analyzer explicitly rejects unsupported semantics. |

## Verification commands and evidence

Already executed research check, from repository root after stage 3:

```sh
python3 research-checks/check_semantic_model.py
```

It reports 197314 finite identity assertions across 65808 function/realizability models. It is not a validator, prototype, or proof of unbounded feasibility.

Planned command contract for the implementation PR (these commands do not exist yet):

```sh
python -m pytest
python -m schema_coverage_lab check-fixtures --input research-fixtures/schema-semantics.json
python -m schema_coverage_lab check-fixtures --input research-fixtures/semantic-counterexamples.json
python -m schema_coverage_lab analyze --schema examples/conjunction.schema.json --corpus examples/conjunction.instances.json --output results/conjunction.json
python -m schema_coverage_lab replay --report results/conjunction.json
```

The implementation may adjust interface names once, documenting the final commands. Add a single reproducible test entry point that creates no unsupported network side effects. Pin dependencies and suite SHA before running conformance checks. Run admitted official-suite cases and document exclusions; passing a subset is evidence for that subset, not full conformance. Oracle fixtures for deferred features test expectations independently of analyzer support.

## Stage gates

First review research and handoff in the stacked drafts. Later implementation PRs should provide focused code and recorded command output for the admitted fragment, then witness generation/reporting, then comparative experiments. Include deterministic rerun evidence and limits, not only screenshots or percentages. Keep drafts open and unmerged for the user. If a proof or hypothesis fails, add the smallest counterexample and amend the research conclusion. Stop at the bounded contract before expanding to annotation-sensitive full-draft semantics.
