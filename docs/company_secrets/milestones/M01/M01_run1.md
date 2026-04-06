# M01 — CI workflow analysis (run 1)

This file records PR-head CI for **M01** on [PR #2](https://github.com/m-cahill/starlab/pull/2). Two runs occurred on the branch: (1) implementation commit, (2) closeout documentation commit. **Merge-gating evidence for the current PR tip** is **Run B** below.

---

## Run B — authoritative (current PR head)

**Workflow:** CI (`ci.yml`)  
**Run ID:** `24048498203`  
**URL:** https://github.com/m-cahill/starlab/actions/runs/24048498203  
**Trigger:** `pull_request`  
**Branch:** `m01-sc2-runtime-surface-env-lock`  
**Head SHA:** `260c4e022db06a4e02f2827ec1efec8fa9b3c992`  
**PR:** [#2](https://github.com/m-cahill/starlab/pull/2) — *M01: SC2 runtime surface decision and environment lock*  
**Conclusion:** **success**  
**Analyzed:** 2026-04-06 (UTC)

**Milestone context:** M01 — SC2 runtime surface decision & environment lock, including closeout artifacts (`M01_run1.md`, `M01_summary.md`, `M01_audit.md`) and ledger updates for PR #2 / CI evidence.

**Baseline reference:** `origin/main` at `725250018bb09ce84e772ded0c7a184cc7d764ea`.

---

## Run A — prior tip (implementation only)

**Run ID:** `24048416111`  
**URL:** https://github.com/m-cahill/starlab/actions/runs/24048416111  
**Head SHA:** `378c86425b63b7b0c048a011644333058a548e80`  
**Conclusion:** **success**  
**Notes:** First push of M01 implementation; superseded by Run B after closeout docs commit.

---

## Workflow inventory (Run B — same structure as Run A)

| Job / Check | Required? | Purpose | Pass/Fail | Notes |
|-------------|-----------|---------|-----------|----------|
| `governance` job | Yes | Full governance pipeline | Pass | Merge-blocking |
| Checkout | Yes | Source at PR head | Pass | `actions/checkout@v4` |
| Set up Python 3.11 | Yes | Toolchain | Pass | |
| Install package (dev) | Yes | Editable install | Pass | |
| Ruff check | Yes | Lint | Pass | `ruff check starlab tests` |
| Ruff format check | Yes | Format | Pass | |
| Mypy | Yes | Types | Pass | |
| Pytest | Yes | Tests | Pass | |
| pip-audit | Yes | Supply chain | Pass | |
| CycloneDX SBOM + upload | Yes | SBOM | Pass | |
| Gitleaks | Yes | Secrets | Pass | |
| Job summary | Yes | Summary | Pass | “STARLAB CI summary” |

**Annotation (informational):** GitHub reported Node.js 20 deprecation notice for some actions — **not** a failure; track upstream action updates outside M01 scope.

---

## Signal integrity

- **Tests:** 32 passed on PR head `260c4e0…` (Run B).
- **Static gates:** Ruff, Mypy unchanged in behavior vs M00.
- **Coverage:** Not gated in CI (unchanged).

---

## Delta analysis

**Full PR diff (current tip vs `origin/main`):** `725250018bb09ce84e772ded0c7a184cc7d764ea...260c4e022db06a4e02f2827ec1efec8fa9b3c992` — 21 files, +1822 / −117 lines (per `git diff --stat origin/main...HEAD`).

Run B validates the same workflow on the expanded tree (implementation + closeout markdown).

---

## Verdict

> **Verdict (Run B):** **Green** on `260c4e022db06a4e02f2827ec1efec8fa9b3c992`. Required governance steps passed. Suitable as **authoritative PR-head CI** for merge gating at the current PR tip.

**Merge recommendation:** **Merge approved** from a **CI / governance** standpoint (subject to human content review).

---

## Next actions

| Action | Owner |
|--------|--------|
| Merge PR #2 when ready | Human |
| Record merge SHA + post-merge `main` CI in `docs/starlab.md` §18 | After merge |

---

*Structure aligned with `docs/company_secrets/prompts/workflowprompt.md`.*
