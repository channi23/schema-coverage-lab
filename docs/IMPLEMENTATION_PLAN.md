# Later implementation and reproducible testing

Issue #5. This stage is a planning deliverable. No production analyzer, generator, validator integration, conformance run or comparative experiment is implemented by this draft. Follow [CODEX_HANDOFF.md](../CODEX_HANDOFF.md) after review of stages 1–4. Leave all PRs unmerged.

## Proposed implementation increments

| Increment | Deliverable | Acceptance evidence |
|---|---|---|
| A: contract and evaluator | Pinned environment, strict parser/meta-schema/support checks, pure-fragment evaluator and local decision catalog. | JSON equality/numeric applicability checks; admitted official-suite subset at exact SHA; explicit unsupported diagnostics. |
| B: observations and pairs | Corpus analysis, vectors, strict-pair detection, status/denominator report and replay. | Known pairs and coupled/infeasible examples; unknown and N/A handling; oracle agreement for every endpoint. |
| C: generation and selection | Deterministic candidate recipes, finite-domain mode, pair-aware suite reduction. | Stable output under fixed seed/input; domain-qualified infeasibility; pair replay after selection; distinct-test counts. |
| D: experiments | Reproducible coverage/cost comparisons and optional mutations. | Equal-budget baselines, frozen corpus, raw reports, confidence/variation reporting, negative findings and limits. |

Keep increments reviewable in later draft PRs or focused commits, with no automatic merge. A–C establish bounded tool behavior; D examines practical utility. Neither establishes full Draft 2020-12 support.

## Reproducibility record

Before execution freeze Python and package versions, dependency lock/hashes, operating system, validator class/options, format policy, strict numeric model, schema/corpus digests, test-suite commit and paths, seeds, generation limits and runtime budgets. Store commands and raw reports with timestamps. Choose immutable source commits; moving manual and suite URLs in the research are source locators, not experimental pins.

Use the handoff's planned CLI contract and make its final version executable. Run the dependency-free research check separately. Execute both fixture catalogs with the oracle; for deferred features require analyzer rejection. Track failures by schema/instance IDs and retain the smallest reproducer. Do not infer branch successes by scraping validation errors.

## Compare utility without assuming success

Compare decision outcomes, predicate outcomes, strict semantic independence, random selection and declared boundary-based selection under the same candidate pools and budgets. Report suite size, unique witnesses, generation time, memory, unknown/unsupported counts, raw/adjusted denominator definitions and achieved coverage. For stochastic baselines, predeclare seeds/repetitions and show variation. Separate oracle conformance checks from coverage-metric experiments.

Optional mutation experiments must describe mutation operators, preserve schema well-formedness where intended, separate invalid mutants, killed mutants, equivalent/proven-equivalent mutants and unresolved equivalence, and distinguish validation-changing faults from annotation or extension behavior outside scope. Do not remove unresolved mutants or infeasible obligations merely to improve scores. Any superiority claim needs empirical evidence; currently there is none.

## Expansion gates

Add object/array/string assertions, conditionals, references, dynamic scope or annotation-sensitive keywords only after specifying their observation model and regression cases. Full support requires richer evaluation state and context identities. Treat custom vocabularies and undefined recursion behavior explicitly. A larger validator oracle can validate schemas that the coverage analyzer still rejects; label that distinction.
