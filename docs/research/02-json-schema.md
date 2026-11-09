# JSON Schema Draft 2020-12 semantics and coverage applicability

Implementation follow-up, 2026-11-09: the bounded corpus analyzer and independent witness replay are now implemented. Both original research catalogs passed all 43 oracle expectations; 295 admitted official cases passed and 52 were explicitly excluded. The research-phase statements below about unexecuted examples describe the earlier baseline. See [current status](../STATUS.md) and [evidence](../EVIDENCE_LOG.md) for current scope and artifacts. Global feasibility, full-draft coverage and practical superiority remain unproved.

Research date: 2026-11-08. Scope: the fixed Draft 2020-12 dialect, not an assertion about a newer dialect. Primary sources are linked at point of use. Counterexamples and coverage proposals below are original deductions, not claims that the specification defines MC/DC.

## What semantic information must coverage retain?

### Takeaway

Accepted-instance sets describe whole-schema validity, but do not preserve every observation needed when a schema is composed. Coverage needs a declared observation model: root validity, local predicate outcomes, applicability, annotation contribution, reference context, or implementation execution.

### Cited Findings

- The core specification distinguishes assertions, annotations and applicators. Type-specific assertions succeed outside their applicable primitive types. Boolean schemas are constant outcomes. Annotation collection examines applicable schemas; failing schemas contribute no annotations. `$ref` permits siblings. `$dynamicRef` can resolve through dynamic scope. References need not trigger network access. Infinite recursive nesting has undefined behavior and must not cause an infinite loop. `additionalProperties` depends on adjacent `properties`/`patternProperties`; `items` depends on adjacent `prefixItems`. `unevaluated*` uses successful evaluations. See [Core §§4.3.2, 7.6.1, 7.7.1, 8.2.3, 9.4, 10–11](https://json-schema.org/draft/2020-12/json-schema-core).
- Validation covers general equality/type assertions; numeric, string, array and object constraints. `integer` includes numbers with zero fractional part. Numbers have no specified precision bounds. Patterns are not implicitly anchored. `minContains`/`maxContains` do nothing without adjacent `contains`; omitted `minContains` acts as one. The standard format behavior is annotation, with assertion evaluation disabled by default; a separate assertion vocabulary exists. Content keywords are annotations. Basic metadata includes `title`, `description`, `default`, `deprecated`, `readOnly`, `writeOnly` and `examples`. See [Validation §§4, 6–9](https://json-schema.org/draft/2020-12/json-schema-validation).
- The official test suite is language agnostic and tests prescribed behavior rather than schema writing style. Its draft-specific directories distinguish versions. It is a useful oracle corpus, not a proof of complete implementation correctness. Pin its exact commit before experiments; record attribution and MIT license if copying cases. [Official test suite README and license](https://github.com/json-schema-org/JSON-Schema-Test-Suite).

### Inferences

The following is a proposed coverage-design inventory. Rows name the complete standard keyword families and recommend observations; they do not prescribe implementation execution order.

| Family / keywords | Proposed observations and scope decision |
|---|---|
| `true`, `false`, `{}` | Constant decision; zero condition obligations, outcome reachability distinguished from missing tests. |
| `$schema`, `$vocabulary` | Record dialect and vocabulary policy in every report. Reject unsupported required vocabularies as unsupported analysis. |
| `$id`, `$anchor`, `$dynamicAnchor` | Record resource identity; do not count identifiers as Boolean conditions. |
| `$ref`, `$dynamicRef` | Record resolved target and evaluation path. Initial prototype: reject references or support only an explicitly bounded, acyclic subset. |
| `$defs`, `$comment` | Storage/comment locations; no independent pass/fail obligation merely for existing in source. |
| `allOf`, `anyOf`, `oneOf`, `not` | Local decisions with child truth-vector obligations; also distinguish overlaps and infeasible vectors. |
| `if`, `then`, `else` | Branch selection plus selected branch outcome. Inactive branch is not an observed false predicate. |
| `dependentSchemas` | Trigger absent/present and triggered whole-instance outcome. |
| `properties`, `patternProperties`, `additionalProperties`, `propertyNames` | Presence, matching partition and child outcome; retain path and overlapping-pattern context. |
| `prefixItems`, `items`, `contains` | Empty/nonempty, index regime, matching-count partition, all matching indices when needed. |
| `unevaluatedProperties`, `unevaluatedItems` | Evaluated-location provenance and successful/failed contributors; defer until a richer semantics exists. |
| `type`, `enum`, `const` | Equality/type partitions with exact JSON value semantics. |
| `multipleOf`, `maximum`, `exclusiveMaximum`, `minimum`, `exclusiveMinimum` | Applicability, bound/equality regions, exact arithmetic; reject unmodeled numeric semantics. |
| `maxLength`, `minLength`, `pattern` | Unicode length and match partitions; defer unsupported regex features. |
| `maxItems`, `minItems`, `uniqueItems`, `maxContains`, `minContains` | Cardinality/uniqueness and match counts; do not invent independent free truth bits. |
| `maxProperties`, `minProperties`, `required`, `dependentRequired` | Cardinality, required-name and trigger partitions. |
| `format` | Report vocabulary plus option policy; no silent mixing of annotation-only and assertion modes. |
| `contentEncoding`, `contentMediaType`, `contentSchema` | Separate optional content processing observations from ordinary acceptance. |
| `title`, `description`, `default`, `deprecated`, `readOnly`, `writeOnly`, `examples` | Annotation coverage, if requested; do not claim validation independence. |

Model evaluation as an observation relation `Eval(S, x, context) -> (validity, annotations, trace/status)`. This is a project modeling proposal. `context` includes dialect, resource registry, reference path/dynamic scope and relevant evaluated-location information. A flat accepted set is the projection onto validity after fixing that context. Such a projection is useful, but loss of information prevents unrestricted substitution inside annotation-sensitive contexts.

### Gaps

- A local Python `jsonschema` package was unavailable during research. The examples below were reasoned from the primary sources; no execution-based validation is claimed.
- No universal termination or completeness theorem is established here. Undefined cyclic cases, unresolved references, invalid schemas, unsupported vocabularies and resource limits must be separate statuses, never a synthetic validation failure.
- An instrumentation API that reliably exposes all successful evaluations is not selected. Error lists alone are insufficient evidence of all predicate outcomes.

## Which concrete counterexamples prevent a universal Boolean reduction?

### Takeaway

Logical truth functions can be modeled exactly in a fixed pure fragment. Treating arbitrary keyword occurrences as freely assignable Boolean variables loses realizability, applicability and annotation information.

### Cited Findings

- The official [conditional cases](https://raw.githubusercontent.com/json-schema-org/JSON-Schema-Test-Suite/main/tests/draft2020-12/if-then-else.json) exercise lone `if`, lone `then`/`else`, selected branches and non-interference across composed schemas.
- The official [unevaluated-properties cases](https://raw.githubusercontent.com/json-schema-org/JSON-Schema-Test-Suite/main/tests/draft2020-12/unevaluatedProperties.json) exercise adjacent keywords, composition and successful evaluation. The [unevaluated-items cases](https://raw.githubusercontent.com/json-schema-org/JSON-Schema-Test-Suite/main/tests/draft2020-12/unevaluatedItems.json) cover array-location bookkeeping.
- The official [`$ref` cases](https://raw.githubusercontent.com/json-schema-org/JSON-Schema-Test-Suite/main/tests/draft2020-12/ref.json) include recursion, escaped pointer fragments and sibling keywords. The [`$dynamicRef` cases](https://raw.githubusercontent.com/json-schema-org/JSON-Schema-Test-Suite/main/tests/draft2020-12/dynamicRef.json) distinguish ordinary anchors, dynamic anchors and dynamic scope resolution.

### Inferences

All following examples are original project deductions. They are small acceptance fixtures for a later implementation PR; this research stage does not claim they have been run.

**E1 — Applicability and presence are distinct observations.**

```json
{"properties":{"age":{"minimum":18}}}
```

`{}`, `{"age":"young"}` and `{"age":18}` pass; `{"age":17}` fails. A minimum observation cannot mean “the property exists and is an adult.” Add `required` for presence and `type` for numeric typing. The empty object makes a property obligation vacuously true without evaluating its child instance.

**E2 — A stronger constraint can make a condition redundant.**

```json
{"allOf":[{"minimum":0},{"minimum":10}]}
```

For numeric inputs, the vector `(false,true)` is impossible. For nonnumbers both predicates pass, so they do not restore that vector. The first minimum cannot independently affect this conjunction. Searching more samples cannot fix that infeasibility. Report a proof of redundancy only when justified over the declared universe; finite sample absence is weaker.

**E3 — `oneOf` is exactly one, not odd parity.**

```json
{"oneOf":[true,true,true]}
```

Every instance fails. An iterated binary symmetric difference of three universal sets instead accepts every instance. Therefore binary XOR generalization is incorrect for three or more alternatives. Use the disjoint exclusive regions `A_i \ union(j != i) A_j`, then union those regions.

**E4 — Same accepted set, different behavior in a context.**

Let `P = {"properties":{"a":true}}` and `T = true`. Both accept every JSON value. Compare:

```json
{"allOf":[{"properties":{"a":true}}],"unevaluatedProperties":false}
```

with:

```json
{"allOf":[true],"unevaluatedProperties":false}
```

At `{"a":1}`, the first passes and the second fails. Equal accepted sets are therefore insufficient for context-preserving schema replacement. This refutes unrestricted compositional semantics based solely on acceptance sets; it does not refute whole-schema denotations.

**E5 — All successful `anyOf` branches can matter.**

```json
{"anyOf":[{"properties":{"a":true}},{"properties":{"b":true}}],"unevaluatedProperties":false}
```

`{"a":1,"b":2}` passes because both successful branches contribute evaluated names. Stopping after a first successful branch and using only its annotations incorrectly rejects the other name. A truth-only union is adequate for the isolated `anyOf` acceptance projection but inadequate as the entire compositional result.

**E6 — Failed branches do not supply evaluated-name credit.**

```json
{"anyOf":[{"properties":{"a":{"type":"integer"}}},{"properties":{"b":true}}],"unevaluatedProperties":false}
```

`{"a":"bad","b":2}` fails: the branch involving `a` fails, so the successful `b` branch leaves `a` unevaluated. Merely visiting a property in a failed branch does not cover it as successfully evaluated.

**E7 — Match counting is richer than a single existential bit.**

```json
{"contains":{"type":"integer"},"minContains":1,"maxContains":1,"unevaluatedItems":false}
```

`[1]` passes, `[1,2]` fails the count bound, and `[1,"x"]` fails the unevaluated-item constraint. These arrays all contain an integer. A single “contains true” bit cannot reconstruct root validity. Removing `contains` would make the count bounds inert rather than ordinary standalone numeric tests.

**E8 — A conditional is selection rather than conjunction.**

```json
{"if":{"type":"integer"},"then":{"minimum":0},"else":{"type":"string"}}
```

`0` and `"x"` pass; `-1` and `null` fail. `null` makes `if` false but still evaluates `else`; `"x"` makes `if` false without forcing root failure. A pure validity expression is `(I ∩ T) ∪ ((J \ I) ∩ E)` once branch acceptance sets are defined in a fixed context; inactive-branch truth is counterfactual, not observed execution coverage.

**E9 — Additional and unevaluated properties have different contexts.**

```json
{"allOf":[{"properties":{"a":true}}],"additionalProperties":false}
```

`{"a":1}` fails because the root `additionalProperties` has no adjacent root `properties` allowing `a`. Replacing `additionalProperties` with `unevaluatedProperties` makes it pass. Flattening these keywords into one catch-all “extra field condition” is unsound.

**E10 — Reference siblings cannot be discarded.**

```json
{"$defs":{"n":{"type":"integer"}},"$ref":"#/$defs/n","minimum":5}
```

`4` fails, `5` passes. Replacing the schema object with only its `$ref` target wrongly accepts `4`. A future loader must distinguish resource identity from document pointer traversal.

### Gaps

- These cases establish limitations and regression targets; they do not exhaust the semantics.
- Dynamic-scope fixtures should be adapted from a pinned official suite rather than invented as a simple textual `$dynamicRef` replacement.
- The suite's moving `main` URLs above identify research sources, not reproducibility pins. Implementation must record a commit SHA and exact test path.

## What is the defensible implementation boundary?

### Takeaway

Begin with a finite, explicit corpus over a small pure fragment and an independent validator oracle. Expand only when the evaluator and obligation definitions account for the new observations.

### Cited Findings

- The specification documents applicability and keyword interactions, and provides flag and richer outputs; it does not define a JSON Schema MC/DC metric. [Core §§7, 10–12](https://json-schema.org/draft/2020-12/json-schema-core).
- Content processing is separate from ordinary validation and metadata is annotation-oriented. [Validation §§8–9](https://json-schema.org/draft/2020-12/json-schema-validation).

### Inferences

Recommended initial contract:

1. Parse valid JSON with an explicit mathematical-number representation; avoid Python's `bool`/`int` subclass confusion or JavaScript floating-point artifacts when defining JSON equality.
2. Validate schemas against the declared meta-schema, then check the analyzer's own allowlist. A meta-schema-valid schema can still be unsupported by this analyzer.
3. Support Boolean schemas, `type`, `const`, `enum`, selected numeric assertions, and `allOf`/`anyOf`/`oneOf`/`not` only when their subtrees remain pure. Unknown keywords should be reported, not silently removed before analysis. Reject unmodeled nested assertions conservatively.
4. Treat each local logical decision separately. Stable condition IDs include schema location and branch index. Report both local and root-sensitive results if both are implemented, never under one ambiguous percentage.
5. Record the domain/corpus and each truth vector with concrete witnesses. Enumerated finite-domain completeness is only completeness for that declared domain.
6. Separate covered, uncovered-with-known-witness, proved-infeasible, unknown, unsupported and not-applicable. No percentage should conceal unknown obligations or exclude them without displaying counts.
7. Use E1–E10 as staged fixtures. E4–E7 and E9 are explicit deferred-feature rejection tests in the first prototype. Add full semantics only in later PRs.
8. Freeze dialect, validator version, format mode, registry contents, random seeds and limits in every report. Use the official suite plus original adversarial cases; neither replaces a proof of the proposed coverage criterion.

### Gaps

- No performance, usability, mutation score or generator completeness results exist yet.
- Full Draft 2020-12 support, solver decidability and useful real-world coverage improvement remain open work; the initial contract must not advertise them as achieved.
