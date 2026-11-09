# Running the bounded prototype

Milestone 1, 2026-11-09. The implemented tool analyzes a supplied finite corpus and independently replays strict semantic independence pairs. It does not generate tests or minimize a suite. Run commands from the repository root.

## Install and verify

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --require-hashes -r requirements.lock
python tools/verify.py
```

Tested with Python 3.14.2 on macOS arm64. The project declares Python >=3.11, but other Python/platform combinations have not been tested. The lock fixes all ten direct/transitive runtime and test package versions and includes release-artifact hashes for other platforms. Dependency installation needs package access; analysis, replay and vendored tests require no network retrieval. The module runs from the repository; package publishing and an installed console command are outside this milestone.

`tools/verify.py` runs pytest, the finite mathematics check, both research catalogs, the admitted official subset and an example analysis/replay. It writes actual outputs and an environment/source/artifact manifest to `results/milestone-1/`. A subsequent run replaces those artifacts; commit a new evidence entry when recording a new experiment.

## Analyze and replay

```sh
python -m schema_coverage_lab analyze \
  --schema examples/conjunction.schema.json \
  --corpus examples/conjunction.instances.json \
  --output results/example.json
python -m schema_coverage_lab replay --report results/example.json
```

The output directory must already exist. Without `--output`, commands print JSON. Exit codes: 0 for supported success, 2 for input/evaluation/replay failure, 3 for unsupported analysis. Error diagnostics go to stderr. Unsupported analysis still produces a diagnostic report, with no percentage or partial complete catalog. An unsupported replay confirms only that diagnostic report and exits 3, not a coverage success.

Corpus format:

```json
{
  "instances": [
    {"id": "adult", "value": 18},
    {"id": "minor", "value": 17},
    {"id": "text", "value": "x"}
  ],
  "suite_ids": ["adult", "minor", "text"]
}
```

IDs must be unique nonempty strings. `suite_ids` is an optional unique subset; omitted means select every candidate. A pair found among candidates but absent from the selected suite is `feasible_uncovered`. Input order does not affect the report; IDs determine deterministic ordering and tie-breaking.

Default `--domain all_json` treats missing pairs as `unknown`. This is intentionally incomplete for the all-JSON universe. Use `--domain candidate_pool` only when scoring the exact supplied finite pool: exhaustive pair absence is then `proven_infeasible` **in that pool**. It is not a global proof. No symbolic global infeasibility solver is provided.

The example has two covered obligations: integer vs noninteger while minimum holds, and minimum vs below-minimum while integer holds. Both endpoints are included and replayed. These are local logical obligations, not source-code execution coverage.

## Supported schemas and numbers

Admitted: Boolean schemas, `{}`, `type` including arrays of type names, `const`, `enum`, four inclusive/exclusive numeric bounds, and nested `allOf`/`anyOf`/`oneOf`/`not`. `$schema` must name Draft 2020-12 if present. `title`, `description` and `$comment` are inert. Other keywords are explicitly unsupported, including structural object/array/string constraints, conditionals, references, `multipleOf`, formats and annotation-sensitive applicators.

Schemas are meta-schema-checked before support checking. Malformed JSON, duplicate keys, nonfinite values, invalid schemas and resource-limit failures are errors, never synthetic validation false or infeasibility.

JSON decimal tokens are parsed exactly. Integers and integer-valued decimals are numerically equal; booleans are not numbers; object key order does not affect equality. The oracle receives exact integers for integral decimals and exact Decimal values otherwise, avoiding the stock oracle's Decimal integer-type mismatch without changing its validation algorithms. The Python API accepts JSON values with `Decimal`, not native floats. Public analysis entry points are `coverage.analyze` and `coverage.replay`; the low-level evaluator assumes its schema was already admitted.

Limits are included in each report: 16 MiB input/report size, JSON depth 64 and 100000 nodes; admitted schema/value depth 32; 1000 numeric digits and absolute exponent/adjusted exponent <=1000; 10000 corpus entries; 64 children per logical decision; 100000 schema-occurrence/corpus evaluation cells. The expanded report must also fit the strict loader node/depth/byte limits so every emitted analysis report remains replayable. Exceeding limits fails explicitly. These are engineering admission limits, not JSON Schema semantic limits.

## Read the report

- `schema`, `corpus`, digests and configuration retain the evidence inputs. Schema identity is based on project canonical JSON, not the original file bytes. Experiment manifests additionally hash exact source/input files.
- `decisions` identifies each logical occurrence and its immediate-child decomposition. Atomic sibling keywords affect validity but do not become invented conditions.
- `observations` records every candidate's vector, local result, root result and independent replay status. This is semantic evaluation, not evidence that the oracle executed every branch.
- `obligations` includes condition identity, status, domain, proof/search description and concrete witness endpoints when available.
- `scores` uses exact numerator/denominator records. A zero denominator is JSON null (N/A). Unknown/unsupported obligations are never silently removed from an all-JSON denominator. An unsupported schema has no complete catalog or scores.

Replay recomputes the entire report, including independent oracle validation. Changed evidence, omitted records, configuration or environment produce an error. Replay is a consistency check, not a cryptographic signature or proof of historical provenance. It currently requires the same recorded Python/platform/package environment; cross-environment replay is a future compatibility decision.

## Other checks

```sh
python -m pytest -q
python research-checks/check_semantic_model.py
python -m schema_coverage_lab check-fixtures --input research-fixtures/schema-semantics.json
python -m schema_coverage_lab check-fixtures --input research-fixtures/semantic-counterexamples.json
python -m schema_coverage_lab check-official
```

The oracle checks all original research examples, including deferred features, while the analyzer must explicitly reject unsupported examples. The official-subset command verifies pinned file hashes and reports each excluded group. Passing that subset is not a full-draft conformance claim.
