# Project instructions

Applies to the entire repository.

- Work directly on `main` in focused commits, as requested by the user. Do not create branches or PRs unless later requested. Inspect the latest remote state and preserve other contributors' changes.
- Document every substantive research, code, test, configuration and workflow change in the same commit. Follow [docs/DOCUMENTATION_POLICY.md](docs/DOCUMENTATION_POLICY.md).
- Keep [docs/STATUS.md](docs/STATUS.md), [docs/ROADMAP.md](docs/ROADMAP.md), [docs/EVIDENCE_LOG.md](docs/EVIDENCE_LOG.md) and relevant usage/design documents accurate.
- Record objectives, decisions, sources, commands, actual results, limitations and next steps. Clearly separate planned, executed and independently verified work.
- Cite primary sources near semantic claims. Pin exact versions/commits for experiments. Never invent results or call a missing witness globally infeasible.
- Preserve the bounded criterion and counterexamples in [CODEX_HANDOFF.md](CODEX_HANDOFF.md). Local semantic coverage is distinct from root influence, validator execution coverage and certification.
- Run checks appropriate to the change and save reproducible evidence. Documentation-only updates require link/status checks; broader tests need a relevant reason.
- Close issues only when their acceptance evidence exists. Preserve issue history; do not delete records merely to reduce open counts.
