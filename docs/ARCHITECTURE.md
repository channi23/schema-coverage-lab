# Bounded corpus-analysis architecture

Implemented milestone 1, 2026-11-09. This is an independent implementation of the research criterion, not a copied compiler MC/DC algorithm. Requirements and exclusions originate in [the handoff](../CODEX_HANDOFF.md).

## Data flow and ownership

1. `jsonio` owns strict parsing, admitted JSON types/limits, exact numeric equality, canonical serialization and SHA-256 content identity.
2. `oracle` owns Draft202012Validator schema checking, offline resource policy and exact integral-decimal normalization. It does not use the custom evaluator or pair engine.
3. `semantics` owns the pure-fragment allowlist, local decision catalog and custom validity evaluation. All logical children are semantically evaluated, including children an optimizing validator could skip. Source occurrence paths are retained.
4. `coverage` validates the corpus and selected IDs, records local/root observations, compares each root/child/local applicator against the oracle, and indexes truth vectors to find strict pairs. A pair differs in exactly one target coordinate and flips the local decision.
5. `checks` executes original research expectations and an explicitly filtered official subset. Deferred semantics can be checked by the oracle without being admitted to coverage analysis.
6. `__main__` supplies the CLI, machine-readable errors and distinct unsupported exit status. `tools/verify.py` saves actual checks and content hashes.

There is no generator, suite optimizer, web service, database, global solver or runtime remote-reference retrieval. The supplied candidate pool is complete only as a finite domain explicitly named by the user.

## Semantic boundaries

Every logical keyword occurrence gets its own identity and immediate child coordinates; duplicate text remains separate. The same schema object can have several local logical decisions plus atomic sibling constraints. Root validity is the sibling conjunction, while each local decision is scored separately. Root influence is not inferred from a local flip.

All admitted applicators evaluate the same root instance location. A content-addressed `urn:sha256:` resource, JSON Pointer, criterion version and condition index identify the occurrence. The report also records fragment/catalog configuration. References and structural child instance locations are excluded; extending them requires a new context/identity design.

`allOf` is all-child truth, `anyOf` any-child truth, `oneOf` exactly one (not parity), and `not` one reversed child. Numeric constraints succeed outside numeric types. JSON equality is recursive; booleans are distinguished before numeric comparison. No evaluator state from an error list is used to infer successful evaluations.

## Exact input and identity contract

Project canonical JSON v1 sorts object keys, escapes strings as ASCII, and expresses numbers with a coefficient/exponent after exact removal of trailing zero digits. It neither rounds through the Decimal arithmetic context nor claims RFC 8785 compatibility. Numerically equal JSON representations have equal canonical digests; original text/whitespace differences are captured separately by experiment file hashes. Duplicate object keys are rejected before a digest is made.

The oracle adapter converts integral Decimal values to Python integers exactly and leaves nonintegral Decimal numbers exact. This accommodates the stock validator's integer checker. It does not modify the oracle's assertions, equality, applicability or applicator algorithms. Admission limits bound representation size and recursion; they do not redefine the unrestricted JSON Schema specification.

## Evidence and scoring

Pair selection uses deterministic vector-index lookup and stable input IDs. A selected-suite pair takes priority over a candidate-only pair. Every credited endpoint has an independently agreed vector, local applicator result and root result. Absent pairs yield unknown over all JSON, or finite-domain infeasibility under explicit candidate-pool scope. There are no global proof rules in this milestone.

The raw score is covered / all catalogued obligations. The adjusted score removes only infeasibility proved in the chosen scoring domain; zero denominator is N/A. Unsupported semantics prevent a complete catalog and suppress global scores. Input/evaluation failures abort analysis rather than becoming coverage observations.

Replay reconstructs the report from its embedded inputs, domain and suite, reruns independent oracle comparisons, and compares all report fields with JSON-aware equality. This detects inconsistent or omitted evidence, but is not an authenticated signature. Exact environment matching is deliberate in v1; compatibility across runtime versions is not yet established.

## Sources and verification scope

Draft semantics are cited in [the research chapters](research/02-json-schema.md). Implementation API decisions were checked against primary [jsonschema validation documentation](https://python-jsonschema.readthedocs.io/en/stable/validate/) and [referencing documentation](https://python-jsonschema.readthedocs.io/en/stable/referencing/) on 2026-11-09. These explain explicit validator selection, schema checking, format policy and registry configuration. Installed oracle version: 4.26.0.

The [vendored manifest](../vendor/json-schema-test-suite/manifest.json) pins the official suite to `245a45abc90190c0bff04d97e6d2b541b4bb9f12`; the upstream MIT license is retained. Twelve keyword files were selected. Within those files the checker executes admitted schemas and explicitly excludes unsupported groups. This measures the implemented subset, not full Draft 2020-12 conformance or practical testing superiority.

See [saved verification](../results/milestone-1/manifest.json), [usage](USAGE.md) and [evidence log](EVIDENCE_LOG.md). Evidence includes 86 regression tests, 295 admitted official cases, 52 excluded cases, 43 oracle-checked research expectations and 197314 finite algebra assertions. These counts describe this recorded run and its code/input hashes.


## Version 0.2 continuation

`generate` supplies deterministic, incomplete literal/boundary/primitive recipes and content-addressed candidates. `select` indexes frozen oracle-agreed observations, distinguishes singleton outcome features from paired obligations, greedily adds both missing endpoints, and reverse-deletes redundant selected tests. Bounded exact enumeration independently establishes minima only for pools <=16. Reduction bundles retain source and selected reports and recompute selection on replay.

`mutate` defines an explicit exploratory schema-mutation family; `tools/run_experiments.py` executes the frozen 32-subject offline study. It saves root discrepancy sets, finite-pool indistinguishability and per-schema/per-seed results. Mutation kills never guide the coverage-only selectors. `tools/audit_artifacts.py` checks raw metrics, exact distinct budgets, replay and all source/artifact hashes.

See [protocol](../benchmarks/README.md) and [study summary](../results/milestone-2/summary.json). The study reduced target-bearing pools from 451 to 64 tests preserving 50 witnessed obligations, but pair guidance did not lead the separate mutation probe. Earlier background claims about first-ever novelty are not supported: set semantics, schema coverage/witness generation, RACC and paired MC/DC reduction have substantial prior work discussed in the manuscript.
