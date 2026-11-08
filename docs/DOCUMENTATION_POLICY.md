# Documentation and research evidence policy

Effective 2026-11-08, by explicit user instruction. This policy applies to research, implementation, tests, experiments, configuration, releases and repository maintenance.

## Record each substantive change

Use a focused commit directly on `main`. Include the documentation with the change rather than leaving it for the end. Before editing, inspect current repository state. If another contributor changes the branch, refresh and reconcile; do not overwrite their work.

For each change record:
- Objective and acceptance conditions: what question or behavior is being addressed.
- Changes and rationale: what changed, why, and relevant alternatives or assumptions.
- Evidence: exact command, input/schema/corpus identity, configuration, output, exit status, and source revision where relevant.
- Interpretation: what the result supports, its domain, and what remains uncertain.
- Next action and related issue/commit.

Update the evidence log for substantive work and the status/roadmap when milestones or plans change. Update relevant design, usage, API/report and test documentation when behavior changes. A small wording fix can use one short evidence entry; do not create repetitive reports.

## Research claims

Cite primary sources beside claims, with section and access date. Distinguish source semantics from project proposals, proof sketches, finite checks and empirical measurements. Preserve counterexamples and failed hypotheses. Record amendments rather than rewriting historical failures as successes.

A finite search proves absence only in its stated finite domain. Separate unknown, unsupported, malformed input and evaluator failure from ordinary invalidity. Document all metric denominators and zero-obligation handling.

## Experiments and tests

Before execution record exact Python/tool/package versions, locked dependency resolution, validator class/options, numeric and format policies, test-suite commit/paths, schema/corpus digests, seeds, bounds and budgets. Save command output and compact machine-readable results when available. Avoid secrets and personal data in artifacts.

Use an evidence ID such as `E-0002`; reference a stable revision or content digest. If an artifact is produced by a commit, name the producing revision in the next record or use a file digest to avoid circular self-references. Never mark a proposed command as executed. Record failures, oracle disagreements, exclusions and negative findings.

## Evidence entry template

```text
ID / date / objective:
Related issue / source revision:
Changes / rationale:
Inputs / versions / configuration:
Command / action:
Observed result / exit status:
Interpretation / limitations:
Artifacts / next step:
```

## Completion and publication

Close issues when their stated deliverables and evidence are complete. A merged plan does not complete its implementation. Keep historical issues/PRs available for traceability. Before a future release, document version, supported fragment, usage, breaking changes, verification and known limitations; no product release is claimed by research consolidation.
