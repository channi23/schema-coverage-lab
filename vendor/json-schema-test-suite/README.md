# Vendored official JSON Schema cases

Source: https://github.com/json-schema-org/JSON-Schema-Test-Suite

Immutable source commit: `245a45abc90190c0bff04d97e6d2b541b4bb9f12` (retrieved 2026-11-09).

The upstream MIT [LICENSE](LICENSE) is preserved. These JSON files are exact upstream text, not project-authored fixtures. [manifest.json](manifest.json) records SHA-256 digests and paths.

Selection: Draft 2020-12 `boolean_schema`, `type`, `const`, `enum`, `minimum`, `maximum`, `exclusiveMinimum`, `exclusiveMaximum`, `allOf`, `anyOf`, `oneOf`, `not`. Other files were not imported in this milestone. Within selected files, schemas outside pure-v1 are excluded by the analyzer support checker and reported with reasons. The recorded run admitted 295 tests and excluded 52 tests; see results/milestone-1/official-subset.json in the repository.

Run `python -m schema_coverage_lab check-official` from the repository root. The checker verifies file hashes before execution. This subset does not represent full-draft conformance.
