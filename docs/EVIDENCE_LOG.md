# Evidence and activity log

This log records completed actions and their limits. Dates use Asia/Kolkata. Earlier research evidence is preserved in the research chapters, source register and finite-check output.

## E-0001 — Research consolidation and workflow change — 2026-11-08

**Objective:** bring all completed research/planning deliverables to `main`, reconcile issue status, and persist the user's requirement to document all future work.

**Authorization and decision:** the user explicitly requested merging all existing PRs, closing completed issues, working directly on `main` going forward, and documenting activities for research traceability. This supersedes the initial no-merge draft workflow. No deletion of research history is needed.

**Observed starting state:** PR #6 was merged into `main`; #7 was merged into the stage 1 branch. PRs #8–#10 were open and already ready for review when inspected. Their reported combined statuses contained CodeRabbit success. That status is not treated as proof of semantic correctness or a substitute for tests.

**Actions and merge results:**

| PR | Action | Merge commit |
|---|---|---|
| #8 | Retargeted to main; consolidated stage 2 files plus stage 3 | `18a6c062bc5657abbe40ab761a8aa84151806d40` |
| #9 | Retargeted to main after #8; merged research synthesis/handoff | `21247df0fcec2eba6eef680b0ea64e980d80b857` |
| #10 | Retargeted to main after #9; merged implementation/testing plan | `373497fe76c200fe76e7d282f0681707e2c95477` |

Merge calls used the inspected expected head SHAs and merge commits, preserving ancestry. Comparing the full stage 5 branch to consolidated `main` reported no file differences, behind_by=0; all research/planning files were included.

**Check rerun:**

```sh
python3 work/publish/research-checks/check_semantic_model.py
```

The local publication copy corresponds to repository `research-checks/check_semantic_model.py`; source revision: stage 3 `7c3df08131cd11f812e50adb00ff53eb4e7bf6aa`. Observed exit status: 0.

```text
PASS: 197314 finite identity assertions across 65808 function/realizability models
Scope: Boolean/set identities only; no JSON Schema conformance or unbounded feasibility proved.
```

**Documentation changes:** README, roadmap, handoff, implementation plan and synthesis workflow text updated; documentation policy, project status, this log and persistent instructions added. Original mathematical claims and limits remain unchanged.

**Issue disposition:** stages 1–4 meet their research/handoff deliverables; close #1–#4 as completed. Keep #5 open for actual implementation, validator replay and comparative experiments. Do not delete issues or claim implementation complete.

**Limitations:** no production analyzer was built and no independent validator run or experiment was performed in this consolidation. Syntax checks and finite identities are research evidence only. No release was published.

**Next:** pin the implementation environment and oracle/test-suite revisions, then follow the bounded handoff. Record future commands and results under successive evidence IDs. Final remote documentation, link and issue/PR-state checks are recorded in the task completion evidence after execution.

**Documentation check before commit:** all repository-local Markdown links in the 19-file complete documentation/research tree resolved; no missing targets. The commit is based on the consolidated main tree and preserves existing research artifacts.

**Completion verification:** after documentation commit `5d8b204a8cafb8e950044d381ac98852aacaf84d`, all 19 repository files were fetched from `main` and matched the intended research/documentation contents. GitHub metadata confirmed PRs #6–#10 merged, issues #1–#4 closed, and issue #5 open. Local Markdown targets resolved in the complete tree. This final entry records those completed checks; it does not claim execution of the outstanding prototype or validator tests.

## E-0002 — Corpus-analysis prototype and independent witness replay — 2026-11-09

**Objective:** implement the first bounded milestone of issue #5 in this chat, on main, with code, tests and accompanying documentation. Stop at supplied-corpus analysis/replay; defer test generation, pair-aware reduction and utility experiments.

**Starting revision:** `0d3411da47df952bbc1bd678db25cf658343c7a4`. The repository was inspected through GitHub and materialized as a local execution snapshot; no implementation code existed. Existing instructions required direct work on main, preserved occurrence identities and documented evidence.

**Implemented:** strict exact-number JSON parsing and structural equality, meta-schema/support checks, pure-v1 evaluation and local catalog, deterministic candidate/suite observations, strict unique-cause pairs, domain-qualified statuses/scores, independent root/child/applicator oracle comparisons, full-report replay and offline CLI. Added usage/architecture documents, a reproducible verification entry point, pinned dependencies and a licensed official-suite subset. No compiler code was copied.

**Decision:** use exact Decimal parsing and normalize integral decimals to integers only at the stock oracle boundary. This avoids Decimal integer classification mismatch without replacing oracle algorithms. Report identity uses documented exact canonical JSON, while the experiment manifest hashes raw source/input files. Unknown all-JSON feasibility is never inferred from finite absence. Unsupported schemas receive no fabricated complete catalog/percentage.

**Environment and provenance:** Python 3.14.2, macOS/Darwin arm64; jsonschema 4.26.0 with Draft202012Validator, format assertion disabled, network reference retrieval denied. `requirements.lock` pins all ten transitive runtime/test packages and PyPI release-artifact hashes. Official suite commit: `245a45abc90190c0bff04d97e6d2b541b4bb9f12`; twelve selected files, original MIT license and exact source bytes retained. Package/API sources are linked in [architecture](ARCHITECTURE.md).

**Installation checks executed:** initial restricted-network package lookup could not resolve the package host. After approved dependency download, `python3 -m venv work/verified-venv` and `work/verified-venv/bin/python -m pip install --disable-pip-version-check --no-index --find-links work/wheels --require-hashes -r work/repo/requirements.lock` completed, exit 0. This is a fresh environment with hash verification from local packages, not an unpinned global install. The final verification used that environment; package installation is the only required network step for a fresh user environment.

**Verification executed:** from the repository execution snapshot, `../verified-venv/bin/python tools/verify.py`, exit 0. It invoked the following recorded commands using that same Python:

```sh
python -m pytest -q
python research-checks/check_semantic_model.py
python -m schema_coverage_lab check-fixtures --input research-fixtures/schema-semantics.json
python -m schema_coverage_lab check-fixtures --input research-fixtures/semantic-counterexamples.json
python -m schema_coverage_lab check-official
python -m schema_coverage_lab analyze --schema examples/conjunction.schema.json --corpus examples/conjunction.instances.json
python -m schema_coverage_lab replay --report results/milestone-1/example-report.json
```

**Observed results:** 86 pytest cases passed; 197314 finite Boolean/set assertions across 65808 models passed; both research catalogs passed all 23 + 20 oracle expectations; 295 admitted official cases passed and 52 were excluded explicitly for unsupported schemas. The example reported two covered obligations, three local observations and verified replay. All seven verification commands exited 0. The regression suite also tests malformed/duplicate-key inputs, exact numeric equality, unsupported/infeasible/unknown distinctions, local-vs-root influence, coupled predicates, pair endpoints split across suites, deterministic order, CLI exit codes and rejection of altered report evidence. No semantic/oracle disagreement was observed in these cases. Final review identified that expanded observation reports could outgrow the strict replay loader even when inputs fit; an explicit output admission check and regression were added. The final rerun includes that correction.

**Saved artifacts:** [verification manifest](../results/milestone-1/manifest.json), actual pytest and finite-check outputs, both fixture results, official selected/excluded results, example report and replay. The manifest records commands, statuses, environment and hashes of all executed code, test inputs and outputs. Verified source-set digest: `f7f8a552a00272767323987b38e6dc95ce6b0a73bd1e63c2025ef42e5955fca2`.

**Interpretation and limits:** these results establish observed behavior of the admitted subset under one tested environment, not full-draft conformance, a global feasibility solver, compiler execution MC/DC, formal proof of engine correctness, optimal test sets or practical superiority. The oracle supports some deferred fixture semantics that the analyzer deliberately rejects. Replay checks full consistency under the same recorded environment; it is not a signature or cross-version compatibility guarantee. No generated corpus, optimizer, comparative or mutation experiment, product release or multi-platform test was performed.

**Next:** keep issue #5 open for deterministic candidate generation, pair-aware suite reduction and comparative experiments. Historical research-phase statements are preserved with dated implementation follow-ups. Final publication checks should match remote file contents against this reviewed snapshot and preserve other contributors' changes.

**Publication verification:** implementation commit [82cefa9fe24d143bc542e08b2c50b0e6b6559499](https://github.com/channi23/schema-coverage-lab/commit/82cefa9fe24d143bc542e08b2c50b0e6b6559499) was advanced directly to main without force. All 60 repository files were fetched at that revision and matched the reviewed local snapshot. Local documentation links and every recorded source/artifact SHA-256 were checked successfully. Issue #5 was updated with completed milestone items and retained open for generation, reduction and comparative experiments. This entry records completed publication checks; it does not add new scientific claims or change executed source inputs.

## E-0003 — Generation, pair-aware reduction and frozen offline study — 2026-11-09

**Authorization and scope:** the user requested continuing all remaining bounded work and a publication-style document explaining the entire project. Implemented directly on main, preserving prior research and milestone-1 evidence. Starting revision: `c48fbe4ec1aa49f0b4bd2b8eb0797944981034fa`. This completes the bounded issue #5 contract, not full Draft 2020-12 analysis or scholarly novelty.

**Implemented:** deterministic literal/boundary/primitive generation (cap, priority, reasons, truncation/rejection metadata); pair-aware greedy reduction and bounded exact minimization (<=16 candidates); source/reduced bundles with independently recomputed replay; common-budget decision/predicate/pair-guided, boundary-first and random offline selectors; declared schema mutations and root discrepancy sets; a reproducible experiment and raw-evidence audit. Engine/package version 0.2.0. Heuristics make no all-JSON completeness or general optimum claim.

**Protocol frozen before the first experiment:**32 selected subjects (20 authored diagnostic schemas, 12 official-derived), generated-pool cap 48, distinct-input budgets 2/4/8, random seeds 0..19, mutant cap 32. Exact source/provenance and methodology: benchmarks/study.json and benchmarks/README.md. Random repetitions are nested within schemas, not additional independent subjects. All methods share the same frozen pool; full-pool preprocessing and final-suite costs are reported separately.

**Commands executed, exit 0:** `python tools/run_experiments.py`; `python tools/verify.py --output results/milestone-2/verification --evidence-id E-0003 --base-commit c48fbe4ec1aa49f0b4bd2b8eb0797944981034fa`; `python tools/audit_artifacts.py`. Actual execution used the hash-locked work/verified-venv Python 3.14.2 on macOS arm64. Oracle, format/network and numeric policies remain recorded in each report. No new runtime dependencies were added. The experiment manifest, separate verification manifest and audit file retain exact source/artifact hashes and statuses.

**Integration findings corrected before the final run:** exact canonical JSON can parse an integer-valued exponent token (seed 10 encoded as 1e1) as Decimal, so RNG control seeds are explicitly converted to int. Expanded generated/reduction artifacts now share strict output admission with replay, preventing successful emission of an unreadable oversized bundle. Experiment and verification manifests have separate artifact boundaries so a new verification run cannot invalidate experiment-output hashes. A failed experiment removes an old pass manifest before starting. The final source and all 2304 raw metric/budget rows passed audit.

**Observed verification:**105 pytest regressions passed; 295 admitted official-suite cases passed with 52 explicit unsupported exclusions; 43 original research expectations passed the independent oracle; 197314 finite mathematical assertions across 65808 models passed. All 32 reduced bundles replayed. The audit recomputed all 2304 rows' budgets and metric numerators and matched source/artifact hashes.

**Observed study:** generated 630 per-subject candidate tests (pool sizes 16–32), with no truncations or rejected numeric representations. Catalogued 69 condition obligations: 50 witnessed in their pools, 19 absent in those finite pools. On 21 target-bearing subjects, pair-aware reduction selected 64 tests from 451, preserving all 50 witnessed obligations (85.81% fewer distinct inputs in that finite-pool aggregate). This is not a minimum-size or effectiveness claim. Four atomic and seven other no-witness controls remain visible.

**Separate mutation result:**177 unique admitted mutants, 139 pool-distinguishable and 38 pool-indistinguishable; no invalid/truncated proposals in this run. At budget 8, pair-guided selection achieved 100% mean independence coverage over 21 eligible schemas, while its mean pool-distinguishable mutation coverage over 31 eligible schemas was 76.63%, below random 77.59% and boundary-first 91.86%. These different denominators and operator biases are explicit; no real-fault, population significance, global-equivalence or end-to-end superiority claim follows. At budget 4, one greedy budgeted subject missed a target despite a four-test adequate reduction existing, exposing heuristic myopia.

**Artifacts:** results/milestone-2 contains 32 case directories with corpora, oracle-agreed pool observations, admitted mutants/root discrepancy sets, reduction bundles and replay results; observations.json contains 2304 budget/seed rows; subjects.json includes timings and traced Python memory; summary.json contains macro-per-schema descriptive summaries. Verification outputs are under results/milestone-2/verification; consistency audit is results/audits/milestone-2.json. Source-set digest: `747e895d6f0b434387545990e2aa88bf589b20b646852cbea0b7d588c54a31e1`. Study input digest: `fb8958b9681d95228a2c3f0c0886825dc45aafb545ffb80873d8e5e35a666ddc`.

**Prior-work and manuscript boundary:** a targeted primary-source review found established MC/DC/RACC and paired reduction, formal JSON Schema algebra/witness generation, modern annotation elimination, and existing schema coverage tools. The paper is therefore an author-review artifact study of a bounded adaptation, not a first-ever coverage/set-theory claim. It retains the negative mutation result. Scholarly novelty, authorship review, stronger external validity, manuscript/code licensing and actual submission remain separate author decisions. No arXiv upload, endorsement, peer review or acceptance is claimed.

**Next action:** publish and verify the bounded code/results on main, close issue #5 once its acceptance artifacts are present, then finish the compiled manuscript/source package and PDF visual QA. Record that publication check as a follow-up entry. Future full-draft/industrial evaluation is beyond the completed bounded contract.


## E-0004 — Comprehensive manuscript and publication artifacts — 2026-11-09

**Deliverable:** a self-contained author-review manuscript, approximately 7090 words and 15 compiled pages, explaining the question, related work, formal model, algorithms, actual results, threats, worked examples, reproduction and project history. Author name/contact were supplied explicitly: Sri Hari Haran Sharma, hariharansharma588@gmail.com. No affiliation was supplied or invented.

**Research scope:** three focused primary-source reviews covered schema generation/coverage, MC/DC/RACC and paired reduction, and experimental methodology. Their original notes are preserved under docs/research/related-work. The manuscript has 20 references, credits established work, distinguishes finite-pool adaptation from universal coverage, and preserves the negative mutation finding. The review is targeted rather than systematic and establishes no first-ever novelty claim.

**Stable experiment identity:** implementation/results commit f9b84dc6adf5a085f8014e4619cf0eb02a74cc6d; study digest fb8958b9681d95228a2c3f0c0886825dc45aafb545ffb80873d8e5e35a666ddc; source-set digest 747e895d6f0b434387545990e2aa88bf589b20b646852cbea0b7d588c54a31e1. The manuscript cites this revision, enabling publication documentation to be committed separately without circular provenance.

**Compilation and layout:** the built-in compile request did not complete within the working wait and was stopped; the official Tectonic 0.17.0 release archive was downloaded and matched its published SHA-256 a3f1cac7c5678f01661a92212f58480ae3b0634115d880dbc59e2953ded45667. Resources were cached inside the task workspace. Final command: tectonic --only-cached --untrusted --keep-logs main.tex, exit 0, no warnings. Long code/hash strings were made breakable and bibliography layout repaired. PDF metadata reports 15 letter-size pages. All pages were rendered and visually inspected in a contact sheet; pages 1,5,9,10,13,15 were inspected at full size. Text checks found expected author/results and no unresolved placeholders; page-character bounds checks found no out-of-page content.

**Figure and editable source:** the two-panel vector plot was created with ReportLab 4.4.9 from the saved summary, not copied from a source. Its SVG matched the portable figure-builder output exactly. The portable Markdown-to-LaTeX builder regenerated the reviewed main.tex exactly. paper/build-manifest.json records compiler identity, source/PDF hashes and QA. Source and outputs include main.tex, manuscript.md, refs.bib, figures/results.pdf and results.svg, source builders, reading guide and compiled manuscript.pdf. A complete research-package ZIP will include the code/results/documentation alongside the paper.

**Repository verification already completed:** all 243 files at the implementation/results revision matched expected Git blob hashes. Issue #5 was closed as completed after the 32-subject, 2304-row study and 105-test acceptance evidence was published. Historical issue/PR records remain intact. The paper revision will receive its own remote file-hash check after publication.

**Author review, not automatic publication:** docs/PUBLICATION_REVIEW.md identifies scholarly novelty, citations, authorship/accountability, rights/licensing, external validity and current submission-process checks for the author. AI assistance is disclosed. No arXiv account action, upload, endorsement, peer review, acceptance or publication was performed. No project/manuscript license was invented. These review considerations do not negate completion of the bounded software and document deliverables.

**Final publication verification:** paper/source revision fc4062a4b585899c26e6726af605f4bcb23c3d40 was published on main. All 256 files, including compiled manuscript and vector figure, matched expected Git blob hashes. All five original issues are closed. The separately downloadable research package contains the complete reviewed repository snapshot, manuscript and a per-file SHA-256 index; its ZIP integrity is checked before delivery. The runtime experiment revision remains f9b84dc6adf5a085f8014e4619cf0eb02a74cc6d, and all paper/scientific hashes are preserved in their respective manifests.

## E-0005 — Reference-matched two-column paper layout — 2026-11-10

**Request:** the author supplied 2503.02770v2.pdf and requested that the paper use its arXiv-style appearance. The supplied PDF is typeset with acmart; visual inspection and font measurements identified a two-column US-letter layout, approximately 9-point Libertine body text, a wide title/author block, numbered academic headings, numeric citations and compact references. Reference SHA-256: 85ca2cff0e103612e4215b4badcea7912386f5e856ddc2240454bc21b0346ad9. It was used only as a layout reference, without copying its prose, results, authors, affiliation or arXiv identifier.

**Changes:** switched the portable paper builder to the standard acmart sigconf/nonacm template. Preserved the supplied author/email without inventing an affiliation or publication venue. Shortened section labels to conventional academic headings. Broke long display equations for narrow columns, used wide results table/figure floats and numeric compressed citations, and kept the full bibliography and all appendices. Removed a redundant amssymb import that conflicts with acmart's own math stack. Generated compiler intermediates are excluded from version control.

**Content preservation:** only Markdown section labels changed. SHA-256 of the complete non-heading Markdown text is 32ce4807f8f9e181b3389236205ed2385ce99b7d1c94a9c6b7cfc14db4ee788e, unchanged before/after restyling. The scientific summary retains SHA-256 65d46ea7ef00db0d2050fc238e17811ed1e6a160612022d025b7c263b92e52ac. All recorded runtime/test/scientific-source hashes still match. No implementation behavior, benchmark input, experimental outcome or claim was changed; no new experimental run is represented by this formatting update.

**Compilation and QA:** Tectonic 0.17.0 compiled the acmart source; final pass used --only-cached --untrusted --keep-logs, exit 0. Font-selection and underfull-box diagnostics remain; there are no overfull boxes or undefined references. Rendering confirms the intended fonts and layout. The revised paper is 9 pages instead of 15, entirely due to denser two-column formatting. All 9 pages were reviewed in a contact sheet, and pages 1,2,3,6,9 at full size. Character bounds, expected author/results text and template-placeholder checks passed. Text extraction required whitespace normalization for the font encoding; the rendered author line was also checked visually.

**Artifacts:** paper/manuscript.pdf, main.tex, manuscript.md, build_manuscript.py, build-manifest.json and current reading guides are updated together. The reference document itself is not copied into the repository or deliverable archive. The downloadable PDF, editable Markdown and full research ZIP will be refreshed from this reviewed snapshot. Prior single-column revisions remain available through Git history. The original source/study commit and scientific content hashes remain unchanged.

**Formatting publication verification:** revision 47b827cf6f60e2a82bda884902004e2838df14ce is on main. All 257 repository files matched expected Git blob hashes, including the revised nine-page PDF, portable source and build manifest. The final deliverable/package refresh uses this checked formatting revision; unchanged scientific source and result hashes are retained.
