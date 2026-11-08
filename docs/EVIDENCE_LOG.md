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
