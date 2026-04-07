# M03 — CI workflow analysis (PR-head only; pre-merge)

## A) Authoritative PR-head CI (current PR tip — merge gate candidate)

**Workflow:** `CI` (`.github/workflows/ci.yml`)  
**Authoritative run ID (PR head at analysis time):** `24058833260`  
**URL:** https://github.com/m-cahill/starlab/actions/runs/24058833260  
**Trigger:** `pull_request`  
**Branch:** `m03-run-identity-lineage-seed`  
**Head SHA (merge gate candidate):** `8634da377fedf61c436f8b3678648b35e45067c3`  
**PR:** [#4 — M03: run identity and lineage seed](https://github.com/m-cahill/starlab/pull/4) (**open** at analysis time)  
**Conclusion:** **success**  
**Recorded:** 2026-04-07

**Superseded PR-head runs (older tips, not the merge gate):** `24058700007` on `4dbd9ba7fd57aaf835592024ee0577352a918c9e` — **success**; `24058752461` on `3e78e71a872086a787fe59c16fe6caa3ef6dbd99` — **success**; `24058791683` on `1ab53f287ece4d862e0ac752208ba8d1e817b491` — **success** (intermediate doc batches).

**Authoritative for merge gating:** **Yes** — this run is the latest `pull_request` CI on the current PR tip (`8634da3…`) and completed **success**; treat it as the merge gate signal until a newer commit invalidates it.

---

## B) Merge / post-merge `main` CI

**Not applicable in this document.** M03 is **not** merged to `main` in this milestone step. **Do not** record a merge commit SHA or post-merge workflow run here until after an actual merge and closeout.

---

## 1. Workflow identity (PR-head inputs)

| Field | Value |
|-------|--------|
| Workflow name | CI |
| Run ID | 24058833260 |
| Trigger | PR against `main` |
| Commit | `8634da377fedf61c436f8b3678648b35e45067c3` |
| Milestone | M03 — Run Identity & Lineage Seed |
| Intent | Land `starlab/runs/`, runtime contract, tests/fixtures, ledger/README alignment; keep CI SC2-free |

---

## 2. Step 1 — Workflow inventory

Single job: **`governance`**.

| Step / check | Merge-blocking | Purpose | Result |
|--------------|----------------|---------|--------|
| Checkout | Yes | Reproducible source | Pass |
| Python 3.11 | Yes | Version lock | Pass |
| `pip install -e ".[dev]"` | Yes | Dev deps only (no `sc2-harness`) | Pass |
| Ruff check | Yes | Lint | Pass |
| Ruff format --check | Yes | Format | Pass |
| Mypy | Yes | Types | Pass |
| Pytest | Yes | Tests (61); fixture-driven M03 + existing SC2 tests | Pass |
| pip-audit | Yes | Supply chain | Pass |
| CycloneDX SBOM + upload | Yes | SBOM artifact | Pass |
| Gitleaks | Yes | Secret scan | Pass |
| Job summary | Informational | Markdown summary | Pass |

No `continue-on-error` on required checks.  
**Annotation (informational):** Node.js 20 deprecation notice for GitHub Actions may appear — does not fail the job.

---

## 3. Step 2 — Signal integrity

### Tests

- **Tier:** unit / governance + M03 identity/lineage/CLI + existing SC2 harness fake path + probe tests.
- **What CI proves:** Deterministic identity/lineage derivation, stable JSON writers, CLI wiring, governance doc presence — all **without** a StarCraft II install and **without** replay binding or canonical run artifacts.
- **What CI does not prove:** Live `burnysc2` execution; replay file binding; canonical run artifact v0; benchmark validity; cross-host reproducibility.

### M03 boundary (fixture-driven)

- M03 operates on **JSON proof + config fixtures** under `tests/fixtures/` and the **same contracts** as M02 `match_execution_proof` + match config.
- **No new SC2 execution proof** is produced in CI.

---

## 4. Step 3 — Delta (M03 scope)

**Changed surface:** `starlab/runs/*`, `docs/runtime/run_identity_lineage_seed.md`, fixtures, tests, ledger/README updates, milestone docs under `docs/company_secrets/milestones/M03/`.

---

## 5. Invariants

- Required checks remain enforced; none weakened for M03.
- No replay-scope expansion; no canonical-run packaging in CI.

---

## 6. Verdict

> **Verdict:** PR-head run **`24058833260`** on **`8634da3…`** is **green** and is the **authoritative merge gate** for the current PR tip. **Merge to `main` has not occurred** in this step; post-merge `main` CI is **out of scope** until merge.

**Merge from CI/governance:** ✅ **CI green** — from an automation/governance standpoint, the PR is **eligible to merge** on the basis of required checks; **final merge** remains a human / permissioned action per project rules.

---

## 7. Next actions (post–PR merge, when authorized)

- Record merge commit + post-merge `main` CI in `docs/starlab.md` §18 (closeout).
- **Do not** start M04 implementation without a new milestone plan.
