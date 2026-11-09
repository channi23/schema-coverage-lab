# JSON Schema generation and coverage prior work

Research checked 2026-11-09. Primary-source review for the schema-coverage-lab manuscript. Source facts, project comparisons and unresolved novelty are separated. The review is targeted, not a systematic literature review. No comparator software was executed by this researcher.

## What formal foundations and witness-generation work already exist?

### Takeaway

Neither interpreting JSON Schema through accepted sets nor generating witnesses is a new contribution of this project. Existing formal work is much broader than pure-v1, while modern annotations and dynamic scope already have dedicated formal treatments.

### Cited Findings

- **Foundations.** Felipe Pezoa, Juan L. Reutter, Fernando Suárez, Martín Ugarte and Domagoj Vrgoč, *Foundations of JSON Schema*, WWW 2016, pp. 263–273, DOI `10.1145/2872427.2883029`. The proceedings paper formalizes syntax and semantics and studies validation; it concerns the contemporary, classical schema language, not an implementation of all later Draft 2020-12 evaluation behavior. The date displayed by a search crawler is not its publication year. — [Original WWW proceedings PDF](https://archives.iw3c2.org/www2016/WWW2016-Proceedings/proceedings/p263.pdf); [author-hosted PDF](https://jreutter.ing.uc.cl/www16.pdf).
- **Logical/data model.** Pierre Bourhis, Juan L. Reutter, Fernando Suárez and Domagoj Vrgoč, *JSON: data model, query languages and schema specification*, PODS 2017, pp. 123–135, DOI `10.1145/3034786.3056120`, arXiv `1701.02221`. It develops a formal JSON data model and a logic capturing the schema proposal and analyzes computational questions. This is historical foundational work, not evidence that arbitrary current extensions are covered. — [Author-submitted arXiv record](https://arxiv.org/abs/1701.02221); [publisher reference listing with PODS metadata](https://doi.org/10.1145/3460319.3464796).
- **Algebra and negation.** Mohamed-Amine Baazizi, Dario Colazzo, Giorgio Ghelli, Carlo Sartiani and Stefanie Scherzinger, *Not Elimination and Witness Generation for JSON Schema*, arXiv `2104.14828v2`, 7 May 2021. It introduces an algebraic characterization with additional operators to address interactions between schema keywords, then uses algebra for negation elimination and witness generation. Thus “JSON Schema needs more than detached independent keyword sets” is already part of its motivation. — [Original versioned arXiv record](https://arxiv.org/abs/2104.14828v2).
- **Constructive witnesses.** Lyes Attouche, Mohamed-Amine Baazizi, Dario Colazzo, Giorgio Ghelli, Carlo Sartiani and Stefanie Scherzinger, *Witness Generation for JSON Schema*, PVLDB 15(13), 4002–4014, 2022, DOI `10.14778/3565838.3565852`; arXiv `2202.12849v3`, 16 July 2022. The paper provides a direct witness-generation algorithm and experiments over several collections including real-world schemas. Its claimed language completeness excludes `uniqueItems`; it is a classical-schema result, not a claim that every 2020-12 feature is handled. Its algebra explicitly uses sets, intersection, union and complement. The artifact is DOI `10.5281/zenodo.7106749`. — [Original PVLDB paper](https://www.vldb.org/pvldb/vol15/p4002-sartiani.pdf); [versioned author submission](https://arxiv.org/abs/2202.12849v3); [authors' reproduction repository](https://github.com/sdbs-uni-p/JSONSchemaWitnessGeneration).
- **Modern semantics.** The same six authors, *Validation of Modern JSON Schema: Formalization and Complexity*, arXiv `2307.10034v2`, 1 February 2024 (initial submission 2023). It formalizes dynamic references and annotation-dependent validation. It proves PSPACE-completeness with respect to schema size even at a fixed instance, while validation is PTIME when the schema is fixed and only instance size varies. The source attributes the hardness to dynamic references rather than annotation dependence. A manuscript must retain that parameter qualification instead of saying every validation call is “PSPACE in the data.” — [Original record and abstract](https://arxiv.org/abs/2307.10034v2); [full author-submitted text](https://arxiv.org/html/2307.10034v2).
- **Annotation elimination.** Lyes Attouche, Mohamed-Amine Baazizi, Dario Colazzo, Giorgio Ghelli, Stefan Klessinger, Carlo Sartiani and Stefanie Scherzinger, *Elimination of annotation dependencies in validation for Modern JSON Schema*, Theoretical Computer Science 1063, article 115645, 2026, DOI `10.1016/j.tcs.2025.115645`; preprint arXiv `2503.11288` (2025). It establishes eliminability of annotation-dependent operators, an exponential worst-case succinctness cost, and a practical rewriting algorithm. This is crucial: a counterexample to unrestricted substitution of acceptance-equivalent fragments does not establish impossibility of compiling a whole modern schema into a richer/classical representation. — [Original publisher article](https://www.sciencedirect.com/science/article/pii/S0304397525005821); [author-submitted preprint](https://arxiv.org/abs/2503.11288).
- **Later journal version.** A 2026 journal publication titled *Witness Generation for Classical JSON Schema* is documented by the authors' institutional portal as ACM Transactions on Database Systems 51(4), article 22, DOI `10.1145/3799416`. The publisher DOI was inaccessible during this review, so detailed new-theorem claims should be based on the accessible earlier paper rather than assumed from the journal title. — [Author institution's publication record](https://researchportal.ip-paris.fr/fr/publications/witness-generation-for-classical-json-schema/); [publisher DOI](https://doi.org/10.1145/3799416).

### Inferences

- This project's defensible framing is a bounded, auditable adaptation of strict semantic unique-cause obligations, paired-evidence suite selection and reproducible experiments. Set semantics, JSON Schema formalization, witness generation, and annotation-sensitive semantics should be cited as foundations rather than claimed inventions.
- A complete witness solver could in principle populate the realizable truth cells needed by the project criterion. The present deterministic candidate generator is a bounded heuristic and must not be equated with the broader decision procedures above.
- A proposed witness relation asks for two concrete inputs in adjacent realizable cells, not simply one satisfying schema instance. That is a difference of objective from ordinary positive witness generation, not proof that nobody previously studied it.
- The project's annotation example is a useful explanatory counterexample about the inadequacy of a particular compositional abstraction. It is not a new impossibility result, and does not contradict elimination algorithms.

### Gaps

- No exhaustive search establishes that a JSON Schema-specific MC/DC analogue has never appeared. “First,” “novel mathematical foundation,” “first set-theoretic schema coverage,” or “only tool” would be unsupported.
- The complete 2026 TODS text could not be read through the available publisher route. Institutional and publisher-index dates differ (online-first versus issue dates); cite year/volume/article without asserting an exact publication day.
- A recent interactive-generation work is listed by the authors' institutional portal, but its year is inconsistent with the publisher's indexed online date: the institutional record gives 2027 although the event is ADBIS 2026 and the publisher's reference list gives September 2026. It is not needed for the core argument; omit or label bibliographic uncertainty rather than inventing a year. — [Institutional record](https://researchportal.ip-paris.fr/en/publications/an-interactive-framework-for-data-generation-from-json-schema/).

## What existing tools already generate data or measure schema coverage?

### Takeaway

There is an existing JSON Schema coverage tool, as well as mature generation and validator-comparison projects. The manuscript should compare observation models and supported objectives rather than treating all tools as interchangeable or claiming unsupported performance wins.

### Cited Findings

- **Hyperjump coverage.** `@hyperjump/json-schema-coverage` supplies test coverage for schema files, Vitest integration and lower-level collection APIs using Istanbul reports. Its README maps statements to keywords, branches to true/false keyword outcomes except nonbranching annotations, and functions to subschemas. Its evaluation plugin observes the Hyperjump validator's evaluation process. The README does not claim the project's strict pair-based semantic independence criterion. License: MIT. — [Official repository and README](https://github.com/hyperjump-io/json-schema-coverage/); [official generated API documentation](https://json-schema-coverage.hyperjump.io/modules.html).
- **Hypothesis generation.** `hypothesis-jsonschema` exposes `from_schema`, returning a Hypothesis strategy for allowed JSON values. The inspected official README states fully tested working support for drafts 04, 05 and 07 and support for nonrecursive references; it does not establish full Draft 2020-12 support. Its small strategy API and positive-data objective differ from paired independence evidence. The repository identifies MPL-2.0 licensing. — [Official repository](https://github.com/python-jsonschema/hypothesis-jsonschema).
- **Bowtie.** Bowtie coordinates other JSON Schema validators, collects their results and publishes comparison/compliance reports. It is a meta-validator rather than a generator for an independence-adequate test suite. The stable documentation observed in this review identifies version 2026.11.2; that moving URL should be pinned if used experimentally. — [Official Bowtie documentation](https://docs.bowtie.report/en/stable/).
- **Containment checking.** Andrew Habib, Avraham Shinnar, Martin Hirzel and Michael Pradel, *Finding Data Compatibility Bugs with JSON Subschema Checking*, ISSTA 2021, pp. 620–632, DOI `10.1145/3460319.3464796`. Their approach checks whether every value accepted by one schema is also accepted by another, addressing compatibility before particular runtime data appears. `jsonsubschema` is the associated official implementation; it is not a strict pair-coverage metric. — [Author-hosted paper](https://andrewhabib.org/publications/issta21-JSONSubschema.pdf); [author institution metadata](https://orbilu.uni.lu/handle/10993/50268); [IBM repository](https://github.com/IBM/jsonsubschema).
- **Official validation suite.** The JSON Schema Test Suite is a language-agnostic collection organized by specification release. It supplies expected instance-validity behavior; passing a selected subset measures the admitted implementation behavior on those cases, not test-suite adequacy or superiority of a coverage criterion. — [Official test-suite repository](https://github.com/json-schema-org/JSON-Schema-Test-Suite).

### Inferences

- Hyperjump is the closest directly relevant coverage comparator found. Its keyword/outcome/visited-subschema reports should be acknowledged explicitly. Our semantic evaluation of all admitted logical children differs from claiming that a validator executed those branches.
- `hypothesis-jsonschema` could be a later generation baseline after dialect restrictions, version pinning, budgets and validity checks are harmonized. It should not be described as an experimentally beaten baseline unless actually run. A simple in-project random selection baseline is not a benchmark of Hypothesis.
- Bowtie could provide a broader oracle comparison later; one pinned Python oracle plus a custom evaluator is not equivalent to many independent validator implementations.
- Existing classical witness-generation experiments over real schemas are stronger external-validity evidence for their own objective than our small constructed corpus. Our narrower experiment must not borrow their scale or findings.
- JSON inference tools and JSON-parser/library test generation are adjacent but different problems. GenSON inference and the LLM-based JSONTestGen paper about Fastjson2 should not be presented as direct semantic schema-coverage baselines without an explicit bridge.

### Gaps

- No listed comparator was installed or executed in this research subtask. No runtime, memory, bug-detection or coverage-superiority comparison is supported by this review.
- The inspected Hyperjump README is a moving source, not an immutable experimental version. If used only as related work, record access date 2026-11-09; if benchmarked, pin a commit and configuration.
- The targeted search found no directly verified MC/DC-specific JSON Schema tool, but this is not evidence of universal absence. The manuscript should say “we investigate” or “we implement,” not “we are first.”

## How should citations and novelty be written in the manuscript?

### Takeaway

Claim an explicit research question and a reproducible bounded artifact, then state the demonstrated result. Treat novelty as an evaluated relation to prior work rather than an adjective applied in advance.

### Cited Findings

- Classical set/algebra semantics and witness generation are directly present in the original 2021 and 2022 work; modern semantics and annotation elimination have separate primary treatments. — [Baazizi et al. 2021](https://arxiv.org/abs/2104.14828v2); [Attouche et al. 2022](https://www.vldb.org/pvldb/vol15/p4002-sartiani.pdf); [Attouche et al. modern validation](https://arxiv.org/abs/2307.10034v2); [annotation elimination](https://www.sciencedirect.com/science/article/pii/S0304397525005821).
- Keyword, true/false and subschema coverage already have a public implementation. — [Hyperjump official README](https://github.com/hyperjump-io/json-schema-coverage/).

### Inferences

- Suitable contribution statement: “We specify a strict semantic unique-cause criterion for declared local decisions in an annotation-free JSON Schema fragment, retain concrete paired evidence and domain-qualified uncertainty, and evaluate deterministic generation and paired suite selection in a reproducible bounded study.” This is a project description, not a priority claim.
- Suitable limitation statement: “The study is not a proof of full Draft 2020-12 support, global feasibility, current safety certification compliance, or practical fault-detection superiority. It does not benchmark external tools unless explicitly reported.”
- Suitable positioning: “Set-theoretic identities are established background. Our engineering question is how to retain realizability, occurrence identity, paired evidence and uncertainty in a coverage workflow.”
- Bibliography entries can use the verified author/title/year/venue/DOI metadata above. For mutable software pages use `@misc` or `@software`, organization as author, URL and `urldate={2026-11-09}`; do not invent a release version. For arXiv sources cite the explicit version when it matters.
- Repeated sources in these notes do not imply independent corroboration; the PVLDB article, arXiv preprint and authors' artifact belong to the same research line.

### Gaps

- This subtask did not audit broad active-clause or MC/DC literature; the parallel MC/DC researcher should assess whether the strict relation is an existing restricted-active-clause criterion under different terminology.
- The manuscript's final novelty and empirical contribution must be reconciled with the actual implementation/results. This review supplies related-work evidence, not peer review or a publication acceptance assessment.
