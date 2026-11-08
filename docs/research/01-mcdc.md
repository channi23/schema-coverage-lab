# MC/DC definitions and implementations

Research checked 2026-11-08. This chapter separates source-backed facts from project definitions and mathematical deductions. MC/DC is a coverage criterion, not one software package. Public descriptions and open-source implementations exist; this work makes no certification claim.

## What does independence mean mathematically?

### Takeaway

Use an explicit unique-cause pair relation for the initial schema experiment. Record condition identity and feasible instances; do not assume all truth vectors can occur. Masking is a distinct criterion requiring a separate algorithm and evidence.

### Cited Findings

- NASA/TM-2001-210876, Hayhurst, Veerhusen, Chilenski and Rierson (May 2001), §2.3.5, §2.5, and Appendix B distinguish unique cause from masking. Unique cause fixes other condition outcomes; masking permits other changes only with logical justification that they do not account for the decision change. Repeated occurrences can make unique-cause obligations infeasible. The tutorial describes structural analysis as complementing requirements-based tests, and cautions against equating coverage with defect detection. This is historical DO-178B guidance, not a verified statement of current certification requirements. [NASA tutorial](https://ntrs.nasa.gov/api/citations/20010057789/downloads/20010057789.pdf)
- NIST's glossary lists condition outcomes, independent influence, and invoked entry/exit points in its MC/DC definition. [NIST glossary](https://csrc.nist.gov/glossary/term/Modified_condition_decision_coverage)
- The GCC implementation author's paper explicitly distinguishes unique-cause and masking and uses the latter for its analysis. [Kvalsvik 2025, §1](https://arxiv.org/html/2501.02133v1#S1)

### Inferences

The following is the project's mathematical formalization of the independence component, not a quotation from a standard.

Let a decision have condition occurrences indexed by I={1,...,n}; let F:{0,1}^n→{0,1}. Let X be the feasible input domain and c:X→{0,1}^n the vector of actual semantic condition outcomes. Define d(x)=F(c(x)). For each i, the unique-cause witness relation is

    W_i = {(x,y)∈X×X : c_i(x)≠c_i(y),
           d(x)≠d(y), and ∀j≠i, c_j(x)=c_j(y)}.

A suite T witnesses i iff W_i∩(T×T) is nonempty. This condition guarantees both outcomes for the target condition and the decision in that pair. It does not incorporate program entry/exit coverage. A schema experiment must therefore call its result semantic independence coverage or explicitly qualified MC/DC-style coverage, rather than certified program MC/DC.

For an unrestricted truth-vector domain, Boolean sensitivity is

    ∂_i F(v) = F(v) XOR F(v with bit i flipped).

A feasible witness requires two realizable endpoints; a sensitive abstract vector alone is insufficient. The data x and y may differ in many fields, provided the selected *other predicate outcomes* remain equal. Conversely, changing just one JSON property does not establish independence if it changes several selected predicates.

For D=A AND B, rows 11,01,10 suffice: 11/01 witnesses A and 11/10 witnesses B. The abstract three-row argument becomes a concrete test argument only after actual JSON instances realize those rows.

Masking example (deduced): Z=(A OR B) AND (C OR D). Vectors (0,0,0,1) and (1,0,1,0) flip the overall decision while flipping A,C,D. The second subexpression remains true, so its changes are masked relative to A's demonstration. This is not a unique-cause pair. Implementing masking by simply accepting arbitrary multiple-bit changes would be unsound. The initial prototype should avoid claiming masking support.

The n+1 claim needs scope. If n independent coordinates each have a unique-cause witness, select one edge for each coordinate in the n-cube. These n edges have distinct coordinate labels and contain no cycle: a cube cycle flips every used coordinate an even number of times. A forest with n edges has at least n+1 vertices. Thus n+1 is a lower bound on distinct vectors under this model. An n-way conjunction attains it with the all-true vector and n single-false vectors. This argument neither promises attainability for arbitrary constrained domains nor concerns masking.

For example, let X be the integers, A(x)=(x≥0) and B(x)=(x≥0) as separately indexed occurrences; D=A AND B. Only rows 00 and 11 occur. No W_A or W_B pair exists, although the decision has both outcomes. Removing duplication would change the criterion's decomposition and its denominator. Report that change; do not silently collapse occurrences.

Condition and decision coverage alone are weaker. For D=A AND B, suite {00,11} gives both outcomes to both predicates and the decision but has no unique-cause pair. A useful report should show the missing pair, not only a percentage.

### Gaps

- No current RTCA standard text was obtained or analyzed; NASA's public tutorial is a historical primary source, not a substitute for current regulatory interpretation.
- Masking variants and short-circuit conventions are not interchangeable. This research does not prescribe a single formal masking relation for JSON Schema.
- The n+1 forest argument assumes total Boolean outcomes for the selected predicates, distinct coordinates, and pair-based unique cause. Not applicable to operational traces with unknown/skipped values without further definition.

## What open-source implementations can be inspected?

### Takeaway

LLVM/Clang and GCC implement program coverage and are useful algorithm references or optional comparison instruments. Neither is itself a JSON Schema coverage engine.

### Cited Findings

- Clang documents compilation with `-fprofile-instr-generate -fcoverage-mapping -fcoverage-mcdc`, profile merging, and `llvm-cov show --show-mcdc`. Its instrumentation-limit section documents condition/test-vector limits and exclusion warnings. Raw profile compatibility is not guaranteed. The same page retains older six-condition wording in the reporting section, so installed-version behavior must be checked. Its interpretation section also says all execution paths are tested; this should not be adopted as a general mathematical definition of MC/DC. [Clang source-based coverage, workflow, interpretation, compatibility, instrumentation limits](https://clang.llvm.org/docs/SourceBasedCodeCoverage.html)
- LLVM 19.1.0 `CoverageMapping.cpp`, `MCDCRecordProcessor::findIndependencePairs`, pairs opposite-decision executed vectors and accepts one differing condition while ignoring don't-care positions. It retains test-vector and condition-location information. The file header states Apache-2.0 WITH LLVM-exception. [Pinned LLVM 19.1.0 implementation](https://raw.githubusercontent.com/llvm/llvm-project/llvmorg-19.1.0/llvm/lib/ProfileData/Coverage/CoverageMapping.cpp)
- GCC documents `-fcondition-coverage` instrumentation, read using `gcov --conditions`. [GCC instrumentation options](https://gcc.gnu.org/onlinedocs/gcc/Instrumentation-Options.html)
- Gcov explicitly describes its criterion as masking MC/DC and reports condition outcomes, including uncovered true/false outcomes. [Gcov manual, --conditions](https://gcc.gnu.org/onlinedocs/gcc/Invoking-Gcov.html)
- Kvalsvik's author report describes GCC 14's CFG/BDD approach and compact bitwise runtime recording, introduced in 2024. [Kvalsvik 2025, abstract and §§1–4](https://arxiv.org/html/2501.02133v1)
- GCC's `tree-profile.cc` has condition-mask discovery, `instrument_decisions`, true/false/mask accumulators, and flushing of unmasked observations. Its header specifies GPL version 3 or later. The release branch URL is moving, rather than an immutable commit pin. [GCC 14 release-branch source](https://raw.githubusercontent.com/gcc-mirror/gcc/releases/gcc-14/gcc/tree-profile.cc)
- LLVM's project policy describes Apache 2.0 with LLVM exceptions, with legacy material and exceptions needing file-specific review. [LLVM licensing policy](https://llvm.org/docs/DeveloperPolicy.html#license)

### Inferences

Use the tools as reference implementations, not as an oracle for schema semantics. A validator written in C/C++ may have program MC/DC measurements; a schema interpreted by it has a separate set of semantic obligations. A schema compiler could preserve schema-to-code mapping, but any such approach would require proof that generated code decisions correspond to the chosen schema criterion.

Recommended optional comparison recipe after research review:

1. Choose a small C decision that mirrors an annotation-free supported schema expression.
2. Pin compiler, coverage tools, command lines, target, optimization settings and source hash.
3. Run the exact concrete instances through schema predicates and an equivalent C fixture.
4. Compare explicit vectors and pairs, not percentage labels; explain differences caused by short circuiting and masking.
5. Save raw artifacts with compatible tool versions and also export a stable project report.

Do not copy third-party implementation code into this repository without recording its license and obligations. Studying their algorithms and independently expressing the project's own pair relation avoids an unnecessary dependency. This is an engineering recommendation, not legal advice or a license-compatibility determination.

### Gaps

- No compiler was built or executed during this research phase. Support flags and reporting behavior have been read, not experimentally confirmed locally.
- Current online manuals are mutable; the later experiment must capture exact release manuals or source commits. LLVM source above is tag-pinned; GCC release source remains branch-pinned.
- This research did not audit the whole implementation or prove its correctness. It identifies relevant code, not an independent compiler qualification.
