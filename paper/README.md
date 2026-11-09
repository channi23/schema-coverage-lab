# Start here: the complete research manuscript

**Semantic Independence Coverage for JSON Schema: A Bounded Reproducible Study**

Sri Hari Haran Sharma — hariharansharma588@gmail.com. Author-review manuscript, November 2026. No affiliation was supplied. No arXiv upload, peer review or acceptance is claimed.

Read [manuscript.pdf](manuscript.pdf) for the complete 9-page explanation. The matching [Markdown](manuscript.md), [LaTeX](main.tex), [bibliography](refs.bib) and vector [figure](figures/results.pdf) are editable/source artifacts. The paper contains background, formal definitions and qualified proofs, counterexamples, architecture, algorithms, methodology, results, threats, worked examples, reproduction commands and project history.

## What was achieved

The project moved from a question about MC/DC and sets to a bounded, independently checked JSON Schema testing artifact. It generates finite candidate pools, measures local semantic independence, reduces suites while preserving witnessed pairs, and replays the source/selected evidence. The completed pilot includes 32 selected schemas, 2304 common-budget rows, 105 regression tests and a full raw-evidence audit. On 21 target-bearing subjects, 451 pool inputs reduced to 64 tests while retaining 50 witnessed obligations.

That adequacy result is different from effectiveness. At an eight-test budget, pair-guided selection reached 100% mean pair coverage but only 76.63% mean pool-distinguishable mutation coverage; boundary-first achieved 91.86% and random 77.59%. The paper preserves this negative result and does not claim a new universal coverage criterion, first-ever schema coverage, full-draft support or practical superiority.

## How to read

1. Read the abstract and Section 1 for the question and result.
2. Read Sections 3–4 and Appendix A for schema semantics, sets, witness pairs and examples.
3. Read Sections 5–7 for the implemented algorithms and actual study.
4. Read Sections 8–9 for limitations and conclusions, then Appendix B for reproduction and Appendix C for project history.
5. Use [publication review](../docs/PUBLICATION_REVIEW.md) before making submission or novelty claims. Read [the evidence log](../docs/EVIDENCE_LOG.md), [usage](../docs/USAGE.md) and raw artifacts when auditing the work.

## Stable artifact and compilation

The tested implementation/results revision is `f9b84dc6adf5a085f8014e4619cf0eb02a74cc6d`. Its manifests record exact source, input and output digests. The manuscript is published separately so it can cite that immutable revision without a circular self-commit claim.

The standalone LaTeX uses an inline bibliography; refs.bib is also supplied for editing. From this directory, compile with `pdflatex main.tex` twice, or `tectonic main.tex`. Compilation was verified with Tectonic 0.17.0; the current version uses ACM-style sigconf/nonacm two-column formatting and cached compilation. Nonfatal font-selection/underfull diagnostics remain; visual checks found no clipping. TeX resources may need network access on a new installation. `python build_manuscript.py` regenerates main.tex from manuscript.md; no external Python package is required for that conversion. It was checked to regenerate the reviewed TeX source exactly.

`python build_figure.py` can regenerate the plot from the repository root data when ReportLab 4.4.9 is installed in a separate optional paper-build environment. The SVG rebuild was checked byte-for-byte against the reviewed vector source. The vector figure was produced from results/milestone-2/summary.json with ReportLab 4.4.9; no source illustration or plot was copied from another paper. The [build manifest](build-manifest.json) records source/PDF digests, compiler identity and visual checks. These records support traceability, not a guarantee of bit-identical PDF metadata across other compiler installations.

The separate source ZIP is a convenience package, not confirmation that all current arXiv administrative requirements have been met. The author must review claims and citations, confirm authorship and rights/licensing, and choose any submission venue/license. No project or paper license was invented on the author's behalf.


## Reference-matched layout (2026-11-10)

The user supplied 2503.02770v2.pdf as a visual reference. The paper now uses the standard acmart class in sigconf/nonacm mode: two columns, compact approximately 9-point Libertine body text, full-width title and author block, numbered academic section labels, numeric citations, wide results floats and compact references. The provided reference was used only for layout; no reference-paper prose or result was copied. No affiliation, publication venue or arXiv identifier was invented.

Section labels were shortened to conventional academic headings. All non-heading Markdown text and all scientific sources/results retain their prior hashes. Narrow-column equations were line-broken without changing their mathematics. The archived earlier revision remains available through Git history; this version supersedes the single-column PDF for reading.
