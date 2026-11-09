# Defensible experimental methods for bounded schema coverage

Research date and access date: 2026-11-09. These notes concern experimental design and interpretation, not a claim that experiments have already been performed. The root agent is implementing and executing them; results must be taken from recorded artifacts rather than this design. The author's manuscript details supplied by the user are Sri Hari Haran Sharma, hariharansharma588@gmail.com; no affiliation was supplied.

## What can the experiments establish without circular evaluation?

### Takeaway

Separate correctness and finite-pool adequacy from practical fault-discovery utility. Preserving the criterion being optimized validates the reducer, but cannot itself demonstrate that the criterion is a superior testing method.

### Cited Findings

- Inozemtseva and Holmes measured coverage, size and mutation effectiveness for large Java subjects and explicitly controlled test-suite size. They found that stronger coverage did not automatically give better effectiveness prediction in their setting. Their domains and metrics are not JSON Schema. — [Inozemtseva and Holmes, ICSE 2014, abstract and §§3–6](https://www.cs.ubc.ca/~rtholmes/papers/icse_2014_inozemtseva.pdf).
- Gligoric and colleagues distinguish comparing coverage-adequate suites from evaluating coverage as a predictor over non-adequate suites. Their work studies multiple criteria and measures, and discusses confounding from suite size and computational effort. — [Gligoric et al., author-hosted journal manuscript, §§1 and 5](https://mir.cs.illinois.edu/marinov/publications/GligoricETAL15CoCoJournal.pdf); verified final journal metadata: [Marinov publication list, entry 78](https://mir.cs.illinois.edu/marinov/publications/).
- Whalen and colleagues propose Observable MC/DC because exercising an internal condition need not propagate a fault effect to the monitored output. Their scope is program/model testing, not JSON Schema. — [Whalen et al., ICSE 2013, abstract and §§I–III](https://greg4cr.github.io/pdf/13omcdc.pdf).

### Inferences

The project's core algebra supports a **finite-pool witness soundness** question: does every reported covered coordinate have two retained inputs whose other selected outcomes agree, whose target changes, and whose local decision flips? This can be checked by recomputation and independent oracle replay. A distinct **coverage-preserving reduction** question asks how many distinct inputs remain while preserving the pool's witnessed obligations. A third, empirical **mutation differential** question asks whether selected inputs distinguish a schema from declared schema mutations at the root. These are different outcomes and should have separate tables.

Recommended manuscript research questions:

1. RQ1, correctness: do admitted instances/decisions agree with the pinned independent validator and do selected witness endpoints replay? This is observed agreement under a supported fragment, not a proof of full-draft conformance.
2. RQ2, reduction: how much can deterministic pair-aware selection reduce each supplied/generated pool while retaining its witnessed independence obligations? On a bounded small subset, does exact enumeration confirm the greedy result or reveal a gap?
3. RQ3, fair-budget comparison: at the same number of distinct inputs from the same frozen pool, what decision outcomes, predicate outcomes, strict independence and root mutation discrepancies do random, boundary, decision-guided, predicate-guided and pair-guided choices achieve?
4. RQ4, limitations: which obligations have no witness in the declared pool, which schemas/cases are unsupported, and which mutants cannot be distinguished on that pool? Do coupled or constant decisions expose denominator problems?

Do not use RQ2 as evidence for RQ3. A selector deliberately maximizing pair coverage will often score well on pair coverage. Its benefit to a separate outcome, such as root mutation discrepancy, remains empirical and can be absent. Similarly, local coverage inside a schema rooted in an always-false conjunction may contribute zero observable root changes; that is an important negative case rather than a result to remove.

### Gaps

The current artifact has no real fault corpus, user study, industrial schema corpus, or evidence that a schema mutation operator distribution resembles actual authoring errors. It therefore cannot establish superiority at finding real defects. A pilot paper can legitimately report a bounded, reproducible implementation and exploratory evaluation, but should not call the method universally effective or first-ever novel.

## How should pools, budgets, baselines and reduction be specified?

### Takeaway

Freeze one pool per schema before running selectors, compare equal distinct-input budgets, and expose generation/selection costs. Random seeds create repeated samples within one schema, not additional independent schema subjects.

### Cited Findings

- The ICSE 2014 study creates fixed-size random suites by sampling without replacement, explicitly to investigate coverage/effectiveness while controlling size. It also records the representational meaning of suite size. — [Inozemtseva and Holmes, §3.4](https://www.cs.ubc.ca/~rtholmes/papers/icse_2014_inozemtseva.pdf).
- The CoCo study explicitly addresses the practical problem of comparing non-adequate suites instead of assuming every criterion can be fully satisfied. — [Gligoric et al., original ISSTA 2013 paper](https://users.ece.utexas.edu/~gligoric/papers/GligoricETAL13CoCo.pdf).
- ACM SIGSOFT's empirical standards provide general, benchmarking, experiment and optimization-study guidance and emphasize explicit research questions, methods and evidence. This is methodological guidance rather than a criterion-specific algorithm. — [SIGSOFT Empirical Standards](https://www2.sigsoft.org/EmpiricalStandards/docs/standards).

### Inferences

**Pool provenance.** Save each schema, pool, source URI/official-suite path, generation configuration, exact values, stable IDs and SHA-256 digests. Deduplicate JSON instances using the exact JSON equality/canonical serialization contract; distinguish numeric equality from booleans. One schema/pool pair is one experimental unit. Official schemas are developer-authored conformance cases, not a representative random sample of deployed schemas. If combining original official test data with generated values, report each source and the merge/deduplication rule.

**Deterministic generation.** For pure-v1, a transparent heuristic may use type representatives, `const`/`enum` literals, numeric bounds and values just below/at/above bounds. Decimal offsets must be stated exactly; arbitrary epsilon is not mathematically universal. If a cap is reached, report truncation and the deterministic priority rule. Absence after a capped heuristic remains unknown over all JSON. Schema-derived boundary generation gives favorable representation to the same constraint families that generated the pool; acknowledge that bias.

**Subject composition.** Include authored synthetic cases with explicit categories: independent conjunction/disjunction, nested decisions, contradictory constraints, redundant bounds, duplicated predicates, exactly-one overlap, root-masked local decisions and zero-obligation/constant schemas. Add a predeclared subset of supported official schemas. Show counts by provenance and category, not just a grand total. Preserve zero-obligation cases in the inventory; report independence as N/A rather than granting them 100%.

**Equal budgets.** For each schema, use common distinct-input budgets such as 1, 2, 3, 4 and min(8, pool size), deduplicating repeated budgets. Random selection samples without replacement under explicitly stored seeds 0–19. A boundary baseline must use a documented schema-derived ordering and deterministic tie-breaking; do not quietly use mutation or coverage knowledge to rank it. If a method terminates early because its own target is saturated, either report its actual lower cost separately or apply one common documented fill rule to reach the same comparison budget. Never compare two tests from one method against twenty from another and attribute the difference solely to criterion quality.

**Guided selectors.** Decision-guided and predicate-guided selection may use standard greedy newly-covered singleton obligations. Pair coverage is different: an empty suite can have zero marginal gain for every individual input even when adding a pair would cover a condition. A pair-aware heuristic should consider adding both missing endpoints together, normalize gain by the number of *new distinct* inputs, and respect the budget. Record deterministic tie-breaking. Do not award coverage to a single endpoint.

**Reduction.** For coverage-preserving reduction, start with all pool-witnessed obligations as the target and verify that the final suite retains the target. Greedy reduction guarantees achieved adequacy only if replay checks it; it has no global cardinality-optimality guarantee. On pools small enough for enumeration, search subsets in increasing cardinality and verify every candidate to obtain a genuine finite-pool optimum. Record a pool-size/search cap and mark larger instances as heuristic. Minimizing pair count is not the same as minimizing distinct-input count because endpoints can be shared.

**Costs.** A selector that consults full-pool observations is performing offline selection from pre-executed candidates. Record generation time, custom/oracle evaluation counts, preprocessing time, selection time, replay time and final suite size separately. Random/boundary ranking does not require the same coverage preprocessing. Equal final-suite budgets support an offline selection comparison, not an end-to-end test-generation efficiency claim. Timing from one host is descriptive; do not generalize across machines or call noisy submillisecond differences significant.

**Variation and aggregation.** Save every per-schema/budget/seed result. Summarize the random baseline within schema with mean/median and min/max or quantiles, then aggregate schemas with equal weight when giving macro summaries. Do not treat 20 seeds as 20 independent schema subjects; avoid a p-value computed over all schema-seed rows as though independent. If using paired confidence intervals, resample schema units, preserving nested seed measurements. For a small pilot, transparent per-schema and descriptive summaries may be more defensible than significance claims. Define handling of N/A denominators explicitly; show eligible counts for each aggregate.

### Gaps

No universal numerical boundary step or universal random distribution over all finite JSON exists in this design. No power analysis justifies twenty random seeds as sufficient for a general effectiveness conclusion; they provide a reproducible variability sample. Only a future larger independent corpus and additional environments can address external validity.

## How can mutation evidence be reported honestly?

### Takeaway

Use schema mutations as an explicitly declared exploratory proxy. A mutant not distinguished by a finite pool is not thereby globally equivalent; retain the distinction in counts and denominators.

### Cited Findings

- Just and colleagues study whether mutant detection correlates with real-fault detection and explicitly consider coverage as a confounder. Their evidence comes from Java application faults, not schema errors. — [Just et al., FSE 2014 author publication page and paper](https://homes.cs.washington.edu/~mernst/pubs/mutation-effectiveness-fse2014-abstract.html).
- Inozemtseva and Holmes discuss the threat introduced by treating master-suite-surviving mutants as equivalent: this can overestimate equivalence and reflect existing test biases. — [ICSE 2014, §§3.3 and 6.1](https://www.cs.ubc.ca/~rtholmes/papers/icse_2014_inozemtseva.pdf).
- Observable MC/DC's motivation is that local activation and observable output failure are different properties. — [Whalen et al., ICSE 2013](https://greg4cr.github.io/pdf/13omcdc.pdf).

### Inferences

Predeclare mutation operators before running selectors. Reasonable pure-v1 examples include replacing a logical applicator, deleting one logical child when meta-schema-valid, changing inclusive/exclusive bounds, shifting a numeric bound by a documented amount, changing a type assertion, or removing `not`. Every mutant must be meta-schema-valid and admitted to the same supported fragment before evaluation. Save original schema digest, mutant digest, operator and occurrence path; deduplicate identical mutant schemas and count invalid/rejected attempts separately.

At root instance x, define a mutant discrepancy as original validity differing from mutant validity. Precompute the discrepancy set K_m in the frozen candidate pool using the independent oracle. A selected suite kills m when it intersects K_m. A mutant with K_m empty is **pool-indistinguishable**, not proved equivalent; do not quietly remove it and present a global mutation score. Report total unique admitted mutants, pool-distinguishable mutants, pool-indistinguishable mutants and per-suite killed counts.

If a normalized score is helpful, label it exactly **pool-distinguishable mutant coverage**, with denominator number of mutants whose K_m is nonempty in this pool. Also show killed / all admitted mutants and raw counts. Zero denominators are N/A. Do not call unseen mutants globally equivalent, do not discard cases that lower the score, and do not let mutation outcomes influence selection for methods intended to optimize coverage only. A mutation-guided oracle baseline, if added, must be explicitly labeled as using extra knowledge.

Deduplicating syntactically identical mutations does not remove semantically redundant mutants. Several different mutant schemas may have identical root behavior over the pool, over-weighting one fault pattern. Report optional behavior-signature deduplication as a sensitivity analysis rather than silently changing the primary denominator. Persist signatures or discrepancy sets so another researcher can reproduce the chosen treatment.

The manuscript should say: observed gains concern this finite pool and this mutation operator set. If pair-guided suites outperform random in pair coverage but fail to improve mutation detection, report the negative result prominently. If they improve mutation detection on boundary-heavy authored subjects, do not extrapolate to real faults, structural keywords, references, annotation-sensitive validity, or deployed API schemas.

### Gaps

This design does not prove global mutant equivalence or establish that these operators represent developer mistakes. There is no evidence yet of real-fault coupling for JSON Schema mutants. No comparative result may be fabricated from this methodological recommendation; all figures must be generated from the executed artifact records.

## Which primary references should the manuscript cite?

### Takeaway

Use these as methodological context rather than claiming their program-testing findings transfer automatically to schema testing. The detailed semantic criterion belongs alongside established active-clause/MC/DC literature handled by another researcher.

### Cited Findings

- Laura Inozemtseva and Reid Holmes. *Coverage Is Not Strongly Correlated with Test Suite Effectiveness*. ICSE 2014, pp. 435–445. DOI 10.1145/2568225.2568271. Author-hosted PDF: https://www.cs.ubc.ca/~rtholmes/papers/icse_2014_inozemtseva.pdf. Full text inspected, especially abstract and §§3–6.
- Milos Gligoric, Alex Groce, Chaoqiang Zhang, Rohan Sharma, Mohammad Amin Alipour and Darko Marinov. *Guidelines for Coverage-Based Comparisons of Non-Adequate Test Suites*. ACM TOSEM 24(4), article 22, pp. 22:1–22:33, 2015. Author publication list confirms venue/pages: https://mir.cs.illinois.edu/marinov/publications/. Author-hosted accepted manuscript: https://mir.cs.illinois.edu/marinov/publications/GligoricETAL15CoCoJournal.pdf. The PDF retains placeholder publication headers, so use the author publication list for final bibliographic details.
- Milos Gligoric, Alex Groce, Chaoqiang Zhang, Rohan Sharma, Mohammad Amin Alipour and Darko Marinov. *Comparing Non-adequate Test Suites using Coverage Criteria*. ISSTA 2013, pp. 302–313. DOI 10.1145/2483760.2483769. Author-hosted PDF: https://users.ece.utexas.edu/~gligoric/papers/GligoricETAL13CoCo.pdf. Prefer journal version for the main citation, unless tracing original chronology.
- Michael W. Whalen, Gregory Gay, Dongjiang You, Mats P. E. Heimdahl and Matt Staats. *Observable Modified Condition/Decision Coverage*. ICSE 2013, pp. 102–111. DOI 10.1109/ICSE.2013.6606556. Author-hosted PDF: https://greg4cr.github.io/pdf/13omcdc.pdf. Metadata corroborated by the institutional record: https://publications.uni.lu/handle/10993/10970.
- René Just, Darioush Jalali, Laura Inozemtseva, Michael D. Ernst, Reid Holmes and Gordon Fraser. *Are mutants a valid substitute for real faults in software testing?* FSE 2014, pp. 654–665. Author-provided BibTeX and paper: https://homes.cs.washington.edu/~mernst/pubs/mutation-effectiveness-fse2014-abstract.html. Use the author's Darioush spelling from their BibTeX; the extracted PDF text/search variant sometimes differs.
- ACM SIGSOFT Empirical Standards. https://www2.sigsoft.org/EmpiricalStandards/docs/standards. Accessed 2026-11-09. Consulted as living methodological guidance; no claim of formal compliance certification is made.

### Inferences

Useful safe contribution phrasing: “We present an explicit, auditable adaptation of unique-cause semantic independence to a bounded JSON Schema fragment, together with counterexamples to unrestricted accepted-set composition and a reproducible pilot artifact.” Avoid “the first MC/DC approach,” “a new set algebra,” “full JSON Schema coverage,” “proved superior,” or “arXiv publication accepted.” arXiv-style preparation is not peer review, submission, endorsement or acceptance.

### Gaps

This is a targeted source review, not a systematic review with exhaustive database coverage. Its failure to find an exact earlier artifact does not establish novelty. Formal novelty and publishability require author review and broader independent scholarly assessment.
