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
