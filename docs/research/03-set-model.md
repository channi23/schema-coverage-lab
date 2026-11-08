# Set-theoretic semantic coverage for JSON Schema

Research date: 2026-11-08. This chapter distinguishes specification facts from project-derived definitions and proofs. The proposed criterion is **semantic unique-cause independence coverage**, not a certification claim or validator source-code MC/DC. All sources below were accessed on the research date.

## Which semantic algebra is justified?

### Takeaway

Sets faithfully describe acceptance under a fixed evaluation contract. Union alone is insufficient, and accepted sets alone cannot preserve every observable effect of Draft 2020-12 schema composition. The following formal definitions and proofs are project derivations, not claims that the JSON Schema specification defines a coverage metric.

### Cited findings

- Draft 2020-12 combines subschema assertion outcomes with logical applicators: `allOf` requires all, `anyOf` at least one, `oneOf` exactly one, and `not` failure of its child. Most assertions accept values outside their targeted primitive types. — [Core §§7.6.1, 10.2.1](https://json-schema.org/draft/2020-12/json-schema-core)
- `unevaluatedProperties` depends on evaluation annotations. All successful `anyOf` branches contribute when collecting annotations; unsuccessful schema objects discard annotations. Dynamic reference resolution can depend on evaluation scope. — [Core §§7.7.1.2, 8.2.3.2, 10.2.1.2, 11.3](https://json-schema.org/draft/2020-12/json-schema-core)
- Numeric assertions constrain numbers; `type` can independently require integers. — [Validation §§6.1.1, 6.2](https://json-schema.org/draft/2020-12/json-schema-validation)

### Inferences and project derivations

#### 1. Evaluation contract and universe

Let J be the universe of finite JSON values interpreted under the JSON Schema instance data model, not host-language object identity. Let E fix the dialect and vocabularies, resource registry and base URIs, supported formats and their assertion policy, numerical interpretation, and extension policy. At an evaluation occurrence also fix instance location, reference path and dynamic scope κ. Assume schema well-formedness, resources resolved, supported semantics, and terminating evaluation. Under those assumptions define:

`[[S]]_(E,κ) = {x ∈ J : validation of x against S at κ succeeds}`.

For a root schema with a fixed registry and ordinary initial scope, κ can be suppressed. This is extensional **acceptance** semantics. It does not encode annotation values, evaluated properties, branch visits, error messages, or implementation control flow. If evaluation errors or cannot be completed, the project must return an error/unsupported result rather than silently assigning false. An ill-formed schema is not the same object as Boolean schema `false`.

For whole-root acceptance, an extensional set exists whenever the contract yields a total Boolean function. That observation does not give a compositional implementation or a decision procedure for set emptiness. For context-sensitive occurrences, make the context part of the domain, e.g. `(x,κ)`, or retain an evaluator producing `(valid, evaluatedLocations, annotations, trace)`.

#### 2. Assertion projection for logical applicators

At a common instance location and compatible fixed context, let A_i be the accepted set of child occurrence i. The assertion result of the logical keyword, considered by itself, is:

| Keyword | Accepted region |
|---|---|
| Boolean `true` / `false` | J / ∅ |
| `allOf` | intersection over i of A_i |
| `anyOf` | union over i of A_i |
| `not` | J minus A_1 |
| `oneOf` | union over i of `(A_i minus union over j≠i of A_j)` |

Proof sketch: for each x, replace set membership by its 0/1 indicator. Intersection means all indicators are 1, union means at least one is 1, complement reverses the indicator, and the disjoint exclusive regions mean exactly one indicator is 1. This is a membership proof, independent of test generation.

Binary `oneOf` is symmetric difference. For three or more children, iterated symmetric difference is parity and differs from exactly-one. If all three child schemas are `true`, every x belongs to their iterated symmetric difference, but no x validates the `oneOf`. A union-only language is monotone in the component sets; `not` and exactly-one are not. For example increasing one branch of `oneOf` can turn a previously valid x invalid. Therefore union cannot express the complete algebra without additional operations or encodings.

For assertion-only `if` I with present `then` T and `else` F, the accepted region is `(I ∩ T) ∪ ((J\I) ∩ F)`. A missing selected branch imposes no assertion. This equation is a statement about assertion outcomes, not permission to evaluate an unselected branch or treat its annotations as active. When `if` is absent the sibling `then`/`else` are ignored, so do not introduce an artificial guard.

#### 3. Why simple intersection over detached keyword schemas fails

For pure independent assertions at one location, sibling constraints compose by intersection. But do not claim that extracting every keyword into a standalone schema preserves semantics. `properties`, `patternProperties`, `additionalProperties`, conditionals, references and unevaluated keywords have specified interactions or evaluation context.

Consider A=`{"properties":{"p":true}}` and B=`true`. As standalone schemas, both accept every JSON value. Put each in the context `{"allOf":[HOLE],"unevaluatedProperties":false}`. On `{"p":1}`, the context with A accepts; the context with B rejects. Thus acceptance equality is not a congruence for all schema contexts. A compositional full-draft model must retain evaluated-location effects. It is inaccurate to say that sets cannot model JSON Schema at all: sets of richer evaluation states or relations can do so, while plain accepted-value sets lose this information.

A second fixture is `{"anyOf":[{"properties":{"p":true}},{"properties":{"q":true}}],"unevaluatedProperties":false}`. The instance `{"p":1,"q":2}` validates because both successful branches contribute evaluated names. Treating `anyOf` as “take the first successful branch” preserves its isolated assertion but changes this parent result.

#### 4. Applicability is semantic, not a free Boolean input

For `{"minimum":18}`, A includes all nonnumeric values and all numeric values at least 18. It is not just the set of numbers ≥18. For `{"type":"integer","minimum":18,"maximum":60}`, the accepted root set is integers from 18 through 60. When considering the three assertions as conditions, a string makes `type` false while both numeric assertions hold; a numeric value 17 makes `minimum` false. These are semantic truth values, not evidence that a validator executed the same branches for the two values.

Likewise `{"properties":{"age":{"minimum":18}}}` accepts `{}`, `{"age":"x"}`, and nonobjects. Coverage of an applicability guard and coverage of an actual failing numeric constraint are different obligations.

### Gaps

No full denotational model of arbitrary custom vocabularies, arbitrary dynamic references, annotation-dependent contexts, recursion, or implementation-specific format checking is proved here. No general decidability or complexity claim follows from the existence of accepted sets. A complete full-draft feasibility solver is not part of the proposed first implementation.

## How can independence and semantic coverage be defined soundly?

### Takeaway

Independence is an edge between two **realizable** semantic cells whose selected decision changes. It is not a single instance in a set difference. The project should begin with a strict unique-cause definition; masking is a different criterion that needs its own formal treatment.

### Cited findings

- NASA's tutorial addresses MC/DC as structural coverage of program decisions and distinguishes unique-cause and masking approaches. Its treatment of independence pairs motivates, but does not standardize, this schema-level adaptation. — [NASA/TM-2001-210876, discussion of independence and masking](https://ntrs.nasa.gov/api/citations/20010057789/downloads/20010057789.pdf)

### Inferences and project derivations

#### 5. Fix the decomposition before scoring

Declare an ordered list of selected condition **occurrences** P_1…P_n and a decision function f. The conditions may be immediate subschema outcomes of one logical applicator, or explicitly chosen pure assertion leaves. A repeated schema occurrence remains a separate coordinate if the declared decomposition says so; merging coordinates changes the metric. Annotated logical children can be used to score their local logical assertion, but the resulting Boolean vector may be insufficient to reconstruct ancestor validity. A node's root-level effect is a separate analysis.

For each instance x define `v(x)=(1_A1(x),…,1_An(x))`. Require that the selected local decision actually satisfies `D(x)=f(v(x))`. If two instances have the same vector but different claimed D, the selected predicates are insufficient: reject the decomposition rather than report misleading coverage.

A Boolean cell is:

`R_b = intersection_i (A_i if b_i=1 else J\A_i)`, for `b∈{0,1}^n`.

The nonempty cells partition J. Proof: each x has one unique membership vector, so it lies in exactly one cell; distinct vectors differ in a coordinate and their cells are disjoint. Empty cells represent impossible combinations, not missing tests.

#### 6. Strict semantic unique-cause independence

For coordinate i, an eligible unordered witness pair `{x,y}` satisfies:

1. `v_i(x) ≠ v_i(y)`;
2. `v_j(x) = v_j(y)` for every j≠i;
3. `D(x) ≠ D(y)`;
4. both observations belong to the same declared decision occurrence/context class and have complete, valid evaluation records.

This holds other selected predicate outcomes fixed, not all JSON fields fixed. Many fields may change. It establishes independence relative to a declared abstraction; it does not establish causal independence of arbitrary physical inputs or source-code branches.

Equivalently, i is feasible precisely when there is a b such that `R_b≠∅`, `R_(b xor e_i)≠∅`, and `f(b)≠f(b xor e_i)`. Proof: a pair yields its two adjacent cells; conversely choose one member of each nonempty adjacent cell. This exact equivalence is the mathematical foundation. The cells may still be difficult to decide or populate.

A useful Boolean derivative is `δ_i f(u)=f(u with i=0) xor f(u with i=1)`. Nonzero derivative on an abstract Boolean vector is necessary but insufficient for semantic feasibility: **both associated cells must be realizable**.

For a test suite T, obligation i is covered iff an eligible pair has **both endpoints in T**. Define `C(T)={i : such a pair exists}`. Then `C(T)⊆C(T∪T')`; adding tests cannot reduce coverage for a fixed contract and obligation catalog. However `C(T∪T')` can strictly exceed `C(T)∪C(T')` because pairs may straddle the suites. This is an important limit of naive set-union bookkeeping. Retain per-test vectors or indexed partial evidence when combining runs.

#### 7. Specialized conjunction, union and exactly-one feasibility

For conjunction, let `P=intersection_j A_j` and `N_i=(intersection_(j≠i) A_j)\A_i`. Condition i has a strict pair iff P and N_i are both nonempty; witnesses come from P and N_i. A point of N_i alone only demonstrates a negative exclusive region, not a pair. If P is empty the decision never succeeds, so no condition has a decision-flipping pair.

For disjunction, let `Z=J\union_j A_j` and `U_i=A_i\union_(j≠i) A_j`. A strict pair exists iff Z and U_i are nonempty. An exclusive branch witness is insufficient if there is no negative decision witness anywhere.

For exactly-one, fix the other n−1 truth values and let k be their sum. Toggling i changes f only for k=0 or k=1. For k=0 it moves between zero matches and one; for k=1 it moves between one match and overlap. For k≥2 both outcomes are invalid. Each candidate pair still needs both associated cells nonempty.

#### 8. Coverage criteria worth reporting separately

- Decision-outcome coverage: observed true and false outcomes at a named decision.
- Predicate-outcome coverage: each selected predicate observed both true and false; does not imply independence.
- Realizable-cell coverage: observed nonempty membership cells. It is exhaustive only over a proven complete finite domain or a complete cell-feasibility classification; otherwise report observed vectors without a percent claiming exhaustiveness.
- Strict semantic unique-cause independence: eligible witness pairs per selected condition.
- Branch/applicability observations: selected guard outcomes and activated schema locations, with vacuous passes distinguishable from applied constraints.
- Domain-specific boundaries: declared bins or boundary examples for numbers, lengths, counts and required properties. There is no one universal boundary topology supplied by the Boolean abstraction.

“Masking” must not be used as a label for arbitrary pairs with multiple changing predicates. Defer a masking metric until a precise rule has been specified and tested; preserve traces if it will be studied later. Report logical outcomes as semantic evaluations, and runtime `not_evaluated` separately from false. Re-evaluating a skipped child analytically may produce a semantic value but cannot fabricate execution evidence.

#### 9. Counterexamples that the implementation must preserve

| Fixture | Consequence |
|---|---|
| `anyOf: [true, {type: integer}]` | Root always true. The integer branch has positive/negative instances but no decision-flipping pair; neither branch has a strict pair. |
| `anyOf: [{type: integer}, {type: integer}]` | Children are perfectly coupled; mixed membership cells are empty, so treating them as independently assignable creates false witnesses. |
| `allOf: [{minimum: 0}, {minimum: 10}]` | The weaker constraint's negative exclusive region is empty. Numbers in [0,10) can demonstrate the stronger constraint. Nonnumbers satisfy both. |
| `allOf: [{const: 0}, {const: 1}]` | No positive decision region, so no strict independence pair for either child. |
| `oneOf: [true,true,true]` | Always false, while three-way XOR is always true. |
| Boolean `A and B`, suite vectors `{00,11}` | Both decision outcomes and both condition outcomes occur; no strict pair exists. |
| Boolean `A and B`, suite vectors `{10,01}` | Both condition outcomes occur; decision remains false. |
| Root `allOf: [false, {anyOf: [{const: 0},{const: 1}]}]` | Local inner decision can change; root stays false. Local coverage must not be promoted to root influence. |
| `properties` with absent child | A child's false observation cannot be inferred from absence; record activation separately. |
| Annotation context from §3 | Acceptance-equivalent child replacement can change parent acceptance. |

### Gaps

This is a selected semantic coverage criterion, not proof of requirements correctness, complete validator conformance, mutation adequacy, fault detection, safety certification, or a universal definition of schema MC/DC. Broad statements that traditional MC/DC “cannot apply to JSON Schema” are too strong: it can be adapted to declared Boolean decisions; the limitations concern decomposition, feasibility, annotations, and the difference from implementation structural coverage.

## What can implementation and verification legitimately claim?

### Takeaway

A small, bounded analyzer can be sound about observed witnesses while remaining explicitly incomplete about unbounded feasibility. Suite minimization must respect paired evidence. Finite verification checks the proposed identities, not the whole JSON Schema draft.

### Cited findings

- Draft 2020-12 is defined by separate core and validation vocabularies, including format and content policies; scope has to be fixed before treating results from validators as interchangeable. — [Validation §§7–8](https://json-schema.org/draft/2020-12/json-schema-validation)

### Inferences and project derivations

#### 10. Evidence and feasibility statuses

Use statuses with explicit domains and proof artifacts:

- `covered`: validated eligible witness pair is in this suite, with both instance IDs, vectors, decision outcomes and evaluator contract.
- `feasible_uncovered`: a validated witness pair exists but is outside the selected suite.
- `proven_infeasible`: sound reasoning establishes no eligible pair in the stated universe; retain solver certificate or mathematical argument and its supported fragment.
- `unknown`: search did not find a pair and no proof exists, including timeout or incomplete symbolic reasoning.
- `unsupported`: semantics cannot be analyzed by the chosen implementation; give the keyword/path/context reason.

A complete enumeration may prove infeasibility **within a declared finite candidate domain X**. It does not prove infeasibility over J unless X is independently shown complete for the selected abstraction. Report `domain: candidate_pool` versus `domain: all_json` and avoid a misleading global `proven_infeasible`. Bounded-depth, bounded-length, or bounded-number searches require the same qualification.

For the complete obligation catalog O report `|covered|`, `|feasible_uncovered|`, `|proven_infeasible|`, `|unknown|`, and `|unsupported|`, plus declaration of whether every occurrence has been classified. A raw conservative score `|covered|/|O|` is interpretable if O is fixed. A feasibility-adjusted score `|covered|/(|O|-|proven_infeasible|)` must retain unknown and unsupported obligations in its denominator and display the counts; excluding every not-found obligation produces false 100% coverage. If only witnessed-feasible obligations form a separate denominator, label it “coverage of witnessed-feasible obligations” and never imply global adequacy. For zero denominator report N/A, not 100%.

#### 11. Pair-aware suite minimization

Let X be a finite candidate pool; for each obligation i compute eligible pairs E_i⊆{{x,y}:x,y∈X}. Select tests with variables y_x∈{0,1} and pair activations z_p∈{0,1}:

`minimize sum_(x∈X) y_x`

subject to `z_{x,y}≤y_x`, `z_{x,y}≤y_y`, and `sum_(p∈E_i) z_p≥1` for every required feasible obligation i.

For weighted tests minimize `sum cost_x*y_x`. Only cover obligations feasible within X; handle empty E_i separately. This binary formulation guarantees that each credited obligation has both witnesses selected. Plain set cover over individual tests is unsound if each endpoint is independently treated as covering independence. Set cover over pairs can find a covering family of pairs, but minimizing the number of pairs is generally a different objective from minimizing distinct tests because endpoints can be shared. A greedy heuristic is acceptable when it reports achieved coverage and actual distinct-test count without claiming optimality. An exact result is optimal only for the supplied finite candidate pool and declared obligations.

#### 12. Reproducible finite checks performed

The companion `research-checks/check_semantic_model.py` is dependency-free research verification, not production code and not a JSON Schema validator. Run with Python 3:

`python3 research-checks/check_semantic_model.py`

Observed result on 2026-11-08:

```text
PASS: 197314 finite identity assertions across 65808 function/realizability models
Scope: Boolean/set identities only; no JSON Schema conformance or unbounded feasibility proved.
```

The script checks exactly-one against disjoint exclusive regions for n≤4; conjunction, disjunction and exactly-one toggle characterizations for n≤4; the pair-versus-adjacent-cell equivalence for every Boolean function and every realizable-cell subset for n≤3; and the three-way XOR counterexample. The symbolic proof sketches above justify arbitrary finite n; these checks provide independent finite regression evidence. They do not validate annotation examples through a real validator, prove solver soundness, establish support for arbitrary schemas, or show practical fault-detection benefits. The repository stores the script under `research-checks/`; run the command above from the repository root.

#### 13. Handoff recommendations

Implement a declarative, annotation-free, acyclic supported fragment first: Boolean schemas; `type`, `const`, `enum`; selected numeric bounds; and `allOf`, `anyOf`, `oneOf`, `not`. Choose immediate-child outcomes as the first condition decomposition. Explicitly exclude custom vocabularies, reference-dependent contexts, annotation-sensitive parent influence, complex string/array/object constraints and formats from symbolic proof support until their semantics are implemented. An oracle may still validate larger schemas without the coverage analyzer claiming full support.

Keep the coverage engine separate from the validation oracle. Every generated witness must be checked independently against the relevant schemas using a pinned Draft 2020-12 validator with recorded configuration. Persist original schema URI/pointer, occurrence identity, schema digest, candidate domain, input IDs, selected vector, local decision, root result, status and evidence. Do not scrape error messages to infer successes, branch visitation, or full evaluation traces.

Test the region identities, pair detector, all listed counterexamples, unknown-vs-infeasible handling, zero denominators, pair-aware suite selection, stable identities under references, and unsupported-keyword behavior. Import a pinned official JSON Schema Test Suite subset with license retained; it measures validator behavior on those cases, not adequacy of the proposed coverage criterion. Compare decision coverage, predicate coverage, strict semantic independence, random selection and boundary-oriented baselines under equal budgets. Mutation experiments must distinguish killed mutants, equivalent/proven-equivalent mutants and unresolved equivalence; results should not presume the proposed metric is superior.

### Gaps

The experiment has not measured test generation scalability, solver completeness, mutation score, conformance against actual validators, or performance on real schemas. No empirical claim that set-based coverage is better than existing testing is established. Accepted-set semantics gives a rigorous research foundation; practical utility remains an explicit experimental question.
