# Later implementation and reproducible testing

Continuation complete, 2026-11-09: increments A–D meet the bounded contract. 105 regressions pass; deterministic generation, pair-aware reduction/replay, a 32-subject / 2304-row frozen offline study and raw-evidence audit are complete. See results/milestone-2, docs/STATUS.md and E-0003. The milestone 1 update below is retained as historical context.

Milestone 1 update, 2026-11-09: increments A and B are implemented for pure-v1, with 86 regression tests, 295 admitted official tests and 43 independent-oracle research expectations passing. Increment C is limited to supplied-corpus finite-domain analysis; generation and suite reduction remain. Increment D is unstarted. See [current status](STATUS.md), [usage](USAGE.md) and [evidence](EVIDENCE_LOG.md).

Issue #5. This stage is a planning deliverable. The original planning delivery contained no implementation. The current corpus-analysis/replay milestone is recorded above; the broader generator and experiments remain open. The research and handoff are now consolidated on `main`. Follow [CODEX_HANDOFF.md](../CODEX_HANDOFF.md) and implement directly on `main` under the [documentation policy](DOCUMENTATION_POLICY.md).

## Proposed implementation increments

| Increment | Deliverable | Acceptance evidence |
|---|---|---|
| A: contract and evaluator | Pinned environment, strict parser/meta-schema/support checks, pure-fragment evaluator and local decision catalog. | JSON equality/numeric applicability checks; admitted official-suite subset at exact SHA; explicit unsupported diagnostics. |
| B: observations and pairs | Corpus analysis, vectors, strict-pair detection, status/denominator report and replay. | Known pairs and coupled/infeasible examples; unknown and N/A handling; oracle agreement for every endpoint. |
| C: generation and selection | Deterministic candidate recipes, finite-domain mode, pair-aware suite reduction. | Stable output under fixed seed/input; domain-qualified infeasibility; pair replay after selection; distinct-test counts. |
| D: experiments | Reproducible coverage/cost comparisons and optional mutations. | Equal-budget baselines, frozen corpus, raw reports, confidence/variation reporting, negative findings and limits. |

Keep increments reviewable through focused commits on `main`, each accompanied by its documentation and evidence. A–C establish bounded tool behavior; D examines practical utility. Neither establishes full Draft 2020-12 support.

## Reproducibility record

Before execution freeze Python and package versions, dependency lock/hashes, operating system, validator class/options, format policy, strict numeric model, schema/corpus digests, test-suite commit and paths, seeds, generation limits and runtime budgets. Store commands and raw reports with timestamps. Choose immutable source commits; moving manual and suite URLs in the research are source locators, not experimental pins.

Use the handoff's planned CLI contract and make its final version executable. Run the dependency-free research check separately. Execute both fixture catalogs with the oracle; for deferred features require analyzer rejection. Track failures by schema/instance IDs and retain the smallest reproducer. Do not infer branch successes by scraping validation errors.

## Compare utility without assuming success

Compare decision outcomes, predicate outcomes, strict semantic independence, random selection and declared boundary-based selection under the same candidate pools and budgets. Report suite size, unique witnesses, generation time, memory, unknown/unsupported counts, raw/adjusted denominator definitions and achieved coverage. For stochastic baselines, predeclare seeds/repetitions and show variation. Separate oracle conformance checks from coverage-metric experiments.

Optional mutation experiments must describe mutation operators, preserve schema well-formedness where intended, separate invalid mutants, killed mutants, equivalent/proven-equivalent mutants and unresolved equivalence, and distinguish validation-changing faults from annotation or extension behavior outside scope. Do not remove unresolved mutants or infeasible obligations merely to improve scores. Any superiority claim needs empirical evidence; currently there is none.

## Expansion gates

Add object/array/string assertions, conditionals, references, dynamic scope or annotation-sensitive keywords only after specifying their observation model and regression cases. Full support requires richer evaluation state and context identities. Treat custom vocabularies and undefined recursion behavior explicitly. A larger validator oracle can validate schemas that the coverage analyzer still rejects; label that distinction.
