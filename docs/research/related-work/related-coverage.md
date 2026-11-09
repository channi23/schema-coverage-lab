# MC/DC, active clauses and pair-aware reduction

Research date: 2026-11-09. Primary-source review for a cautious manuscript; this is not a current aviation-certification interpretation. Source URLs below identify original papers or their authors' institutional records. Search-index publication timestamps were ignored when they conflicted with the papers' actual dates.

## How does the proposed semantic criterion relate to existing logic coverage?

### Takeaway

The project's strict schema witness relation belongs to the established unique-cause MC/DC / Restricted Active Clause Coverage (RACC) family. Re-expressing the relation with accepted sets or adjacent realizable cells is a useful semantic adaptation, but is not evidence of a new Boolean coverage criterion.

### Cited Findings

- NASA's original report is Kelly J. Hayhurst, Dan S. Veerhusen, John J. Chilenski and Leanna K. Rierson, *A Practical Tutorial on Modified Condition/Decision Coverage*, NASA/TM-2001-210876, May 2001. Its public record confirms authors, report number and historical DO-178B scope. The earlier project chapter inspected §2.5 and Appendix B on unique cause and masking; this review verified the official record, while the PDF download timed out. — [NASA original report record](https://ntrs.nasa.gov/citations/20010057789), [official PDF](https://ntrs.nasa.gov/api/citations/20010057789/downloads/20010057789.pdf).
- John Joseph Chilenski and Steven P. Miller's original article, *Applicability of modified condition/decision coverage to software testing*, describes independent condition influence and properties of MC/DC. The historical publication is *Software Engineering Journal* 9(5):193–200, September 1994, DOI 10.1049/sej.1994.0025. The original indexed paper was discoverable, but full download access failed in this session; use NASA for inspected details rather than overclaiming review of this article. — [original paper copy](https://citeseerx.ist.psu.edu/document?doi=78518767bf708510475b04cbae3ee055ca4bf9ec&repid=rep1&type=pdf), [publisher DOI locator](https://doi.org/10.1049/sej.1994.0025).
- Paul Ammann, Jeff Offutt and Hong Huang, *Coverage Criteria for Logical Expressions*, ISSRE 2003, pp.99–107, formalizes logic criteria independently of whether expressions arise from code, specifications or state machines. The original indexed text contains determination, RACC/CACC distinctions and Boolean derivatives. Offutt's own CV verifies authors, conference, pages and November 2003. The indexed paper explicitly contrasts keeping the other clauses fixed for RACC with permitting different minor-clause choices for CACC. Direct original-PDF retrieval was blocked, so this is inspected indexed original text plus author metadata, not a complete full-text review. — [original indexed paper](https://citeseerx.ist.psu.edu/document?doi=abab7a61723c961acd6ff35ffea5ef6a0c701685&repid=rep1&type=pdf), [author CV, publication 153](https://www.albany.edu/faculty/offutt/resume.pdf). DOI locator: https://doi.org/10.1109/ISSRE.2003.1251034 (resolver unavailable here).
- Gordon Fraser and Angelo Gargantini's original paper, *An Evaluation of Specification Based Test Generation Techniques using Model Checkers*, §2.3, defines predicate/condition coverage, GACC, CACC and RACC within one framework. RACC requires identical minor-clause values across the two target-clause values, with an opposite predicate result. Equations (12)–(13) retain cross-test constraints using helper values. The paper compares specification-based criteria and explicitly reports no universally preferable single criterion; its results concern its own model-checking subjects. — [author-hosted original PDF, §§2.3, 4–5](https://cs.unibg.it/gargantini/research/papers/taicpart09.pdf). The filename and context identify TAIC PART 2009, but this review did not independently verify full proceedings pagination/DOI; avoid inventing them.

### Inferences

- For declared total predicates c_i(x), the project's pair relation c_i(x)≠c_i(y), c_j(x)=c_j(y) for all j≠i, and f(c(x))≠f(c(y)) is exactly the restricted same-minor-values condition over feasible concrete observations. Naming it semantic unique-cause coverage is appropriately descriptive; claiming invention of the independence principle is not.
- Realizable cells R_b qualify the abstract criterion by concrete schema inputs. Their adjacency characterization is a direct membership reformulation: a pair yields adjacent cells, and two nonempty adjacent cells yield a pair. Boolean sensitivity is established machinery; do not call this a novel Boolean derivative.
- The contribution can instead be an explicit, executable JSON Schema semantic contract: local occurrence identities; concrete input witnesses; annotation-context counterexamples; exact numeric handling; independent oracle replay; and conservative unknown/unsupported/finite-domain reporting. Whether that combination is publishably novel remains a literature-review question, not something a bounded implementation demonstrates.
- Separate condition occurrences from logical variables. AOH's indexed derivative discussion replaces all occurrences of a clause variable together; the project intentionally preserves distinct schema child occurrences and lets identical predicates be coupled through realizability. The manuscript must state this difference rather than call all occurrence/variable interpretations interchangeable.

### Gaps

- No current RTCA standard was obtained. The paper must not claim certification compliance.
- Full AOH and Chilenski/Miller downloads were inaccessible; exact quotation or detailed attributions beyond inspected portions should be avoided.
- We have not proved a formal equivalence to every operational MC/DC or short-circuit convention. The model is total semantic evaluation, not runtime execution coverage.

## What prior work already addresses pair-aware test-suite reduction?

### Takeaway

Pair-aware MC/DC reduction is longstanding prior art. The project should describe its reducer as a bounded implementation of the correct paired-evidence objective, not as the discovery that MC/DC requires both endpoints.

### Cited Findings

- James A. Jones and Mary Jean Harrold, *Test-Suite Reduction and Prioritization for Modified Condition/Decision Coverage*, *IEEE Transactions on Software Engineering* 29(3):195–209, March 2003, §§2–4, distinguishes paired MC/DC requirements from single-entity coverage. It explains that covering opposite condition truth values can still miss a compatible pair and presents build-up/break-down reduction and prioritization approaches. The original PDF's title, author line, volume, issue, pages and date were inspected. — [original TSE paper, §§2–4](https://bowringj.people.charleston.edu/docs/tse03-mcdc.pdf).
- The same authors published an earlier conference version under the same title in ICSM 2001. The authors' research-group record identifies that venue, November 2001 and a case-study scope; its DOI link resolves to identifier 10.1109/ICSM.2001.972715, although the resolver itself could not be fetched. Do not confuse the 2001 conference paper with the inspected 2003 journal extension. — [author research-group record](https://spideruci.org/publication/jones-test-suite-2001/).
- Robin Lee and Youngho Nam, *EQ-Robin: Constraint-Resilient Generation of Multiple Minimal Unique-Cause MC/DC Test Suites*, arXiv:2509.26458v2, revised 9 February 2026, studies alternative minimal suites under feasibility constraints for Singular Boolean Expressions. The abstract restricts its guarantees to that Boolean setting; it is an author preprint, not a JSON Schema/full-dialect solver or a proof that arbitrary decisions admit N+1 concrete tests. — [author preprint record, version 2](https://arxiv.org/abs/2509.26458v2).

### Inferences

- Given finite candidates X and eligible pair sets E_i, selecting tests y_x and pair activations z_{xy} with z_{xy}≤y_x, z_{xy}≤y_y and Σ_{p∈E_i}z_p≥1 is a transparent binary encoding of established paired requirements. It is reasonable to include as a derivation for the reader; no novelty claim for the general formulation was established here.
- Minimizing distinct tests and minimizing selected pairs are different objectives because endpoints may be shared. Ordinary set cover over individual tests is unsound if a single endpoint is credited as complete independence. Set cover over pairs preserves coverage but generally optimizes pair count, not distinct tests.
- C(T∪U) can exceed C(T)∪C(U) when a compatible pair straddles two suites. This is a direct consequence of paired requirements already emphasized by Jones/Harrold. It is a useful implementation/aggregation warning, not persuasive standalone novelty.
- A build-up greedy reducer should consider paired additions or already selected mates, because from the empty suite every single test has zero completed independence contribution. A break-down reducer can begin with a covering pool and remove only tests whose deletion preserves all desired obligations. Both require deterministic tie-breaking and replay of the resulting suite.
- Any exact algorithm's optimality statement must name the supplied finite pool, fixed criterion/catalog and completed search budget. A timeout or node budget yields an incumbent or unknown optimality, never a global minimum claim.

### Gaps

- This search did not establish that the exact binary formulation above is unpublished; it should be treated as standard logical modeling, not a novel theorem.
- Neither classical MC/DC reduction results nor EQ-Robin's restricted Boolean setting establish performance or fault-detection superiority for JSON Schema. Those require the project's own fair experiments and may yield negative findings.

## Which manuscript claims and experimental interpretations are defensible?

### Takeaway

Position the paper as a carefully scoped semantic adaptation and reproducible research artifact. Distinguish formal reformulation, engineering evidence and empirical effectiveness; do not announce a universal or first-ever new coverage method.

### Cited Findings

- The inspected Fraser/Gargantini experiment combines coverage techniques, reports infeasible requirements and cautions against a single universally preferable criterion. Its §3 separates complete generation, post-generation minimization and monitoring of already covered requirements. — [original paper, §§3–5](https://cs.unibg.it/gargantini/research/papers/taicpart09.pdf).
- NASA's report presents structural analysis as part of a wider verification process, while Jones/Harrold studies reduction that preserves its declared criterion. Neither source equates coverage preservation with complete correctness. — [NASA record and tutorial](https://ntrs.nasa.gov/citations/20010057789), [Jones/Harrold original paper](https://bowringj.people.charleston.edu/docs/tse03-mcdc.pdf).

### Inferences

- Recommended contribution wording: “We operationalize a strict unique-cause semantic criterion for a declared JSON Schema fragment, make feasibility and context limitations explicit, and evaluate generated/reduced suites with replayable evidence.” Prefer “operationalize/adapt” to “invent/first/universal.”
- Report equal candidate pools and distinct-test budgets for decision, condition, semantic-pair, random and boundary baselines. Separate selector coverage targets from fault-detection evaluation, and retain timing/memory/candidate costs.
- Repetition seeds and per-subject results matter. A global mean can conceal constant/contradictory schemas, coupled conditions, zero obligations and local effects masked at the root. State exact denominators and classify these subjects rather than silently dropping them.
- If mutation experiments use the same pool for mutant classification and evaluation, call non-distinguished mutants pool-equivalent or unresolved, not globally equivalent. If a held-out universe is available, separate selection and evaluation evidence.
- Full-draft annotation-sensitive schemas may serve as oracle-checked counterexamples while remaining analyzer-unsupported; this is deliberate scoped evidence rather than implementation conformance failure.

### Gaps

- This is a targeted primary-source review, not an exhaustive systematic literature review. No first-ever claim has been established.
- arXiv acceptance, peer review, current submission policies, author responsibility and final publication decisions were not investigated by this subtask; the manuscript should remain an author-review draft.

Bibliographic core for the writer: Hayhurst et al. (NASA/TM-2001-210876, 2001); Chilenski and Miller (Software Engineering Journal 9(5):193–200, 1994); Ammann, Offutt and Huang (ISSRE 2003:99–107); Jones and Harrold (IEEE TSE 29(3):195–209, 2003; distinct earlier ICSM 2001 version); Fraser and Gargantini (author-hosted TAIC PART 2009 paper, metadata beyond title/authors/year to verify); Lee and Nam (arXiv:2509.26458v2, 2026 revision).
