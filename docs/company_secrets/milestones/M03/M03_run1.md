# M03 — CI workflow analysis (PR-head + post-merge `main`)

## A) Final PR-head CI (merge gate — merged PR #4)

**Workflow:** `CI` (`.github/workflows/ci.yml`)  
**Authoritative run ID (final PR head before merge):** `24059095399`  
**URL:** https://github.com/m-cahill/starlab/actions/runs/24059095399  
**Trigger:** `pull_request`  
**Branch:** `m03-run-identity-lineage-seed` (merged; remote branch **deleted** after merge)  
**Head SHA (merged tip):** `884055c34b78f182c704df5a10a9eced5515fa78`  
**PR:** [#4 — M03: run identity and lineage seed](https://github.com/m-cahill/starlab/pull/4) (**merged**)  
**Conclusion:** **success**  
**Recorded:** 2026-04-07

**Superseded / historical PR-head runs (older tips):** includes `24058918126` on `72aff7050f6ae0807b875993d577cb6d6eeeded6` — **success** (implementation-focused tree); earlier green runs on older SHAs superseded by later PR tips before the final merge head above.

**What this run proves:** `pull_request` CI **success** on the **exact** Git commit that was merged as the PR tip (`884055c…`). Required checks were **green** before merge.

---

## B) Merge to `main`

**Merge commit:** `6bfe6a7b32a004f62a491bf31573e12cd211118a`  
**Merged at (UTC):** `2026-04-07T01:10:32Z`  
**Merge method:** **Merge commit** (GitHub “Create a merge commit” — message: `Merge pull request #4 from m-cahill/m03-run-identity-lineage-seed`).  
**Remote branch after merge:** `m03-run-identity-lineage-seed` **deleted** on origin.

---

## C) Authoritative post-merge `main` CI (push on merge commit)

**Workflow:** `CI`  
**Run ID:** `24059246337`  
**URL:** https://github.com/m-cahill/starlab/actions/runs/24059246337  
**Trigger:** `push` to `main`  
**Head SHA:** `6bfe6a7b32a004f62a491bf31573e12cd211118a` (merge commit)  
**Conclusion:** **success**

*Follow-up documentation-only pushes to `main` after closeout may produce additional green `push` runs; distinguish them in `docs/starlab.md` §23.*

---

## 1. Workflow identity

| Field | Value |
|-------|--------|
| Workflow name | CI |
| Merge gate (PR) | Run `24059095399` on `884055c…` |
| Post-merge (`main`) | Run `24059246337` on `6bfe6a7…` |
| Milestone | M03 — Run Identity & Lineage Seed |

---

## 2. Step 1 — Workflow inventory (PR-head and `main` use same job)

Single job: **`governance`**.

| Step / check | Merge-blocking | Purpose | Result (PR-head run) |
|--------------|----------------|---------|------------------------|
| Checkout | Yes | Reproducible source | Pass |
| Python 3.11 | Yes | Version lock | Pass |
| `pip install -e ".[dev]"` | Yes | Dev deps only | Pass |
| Ruff check | Yes | Lint | Pass |
| Ruff format --check | Yes | Format | Pass |
| Mypy | Yes | Types | Pass |
| Pytest | Yes | Tests (61); fixture-driven M03 + SC2 tests | Pass |
| pip-audit | Yes | Supply chain | Pass |
| CycloneDX SBOM + upload | Yes | SBOM artifact | Pass |
| Gitleaks | Yes | Secret scan | Pass |
| Job summary | Informational | Markdown summary | Pass |

**Annotation (informational):** Node.js 20 deprecation notice for GitHub Actions may appear — does not fail the job.

---

## 3. Step 2 — Signal integrity

### Tests

- **Tier:** unit / governance + M03 identity/lineage/CLI + existing SC2 harness fake path + probe tests.
- **What CI proves:** Deterministic identity/lineage derivation, stable JSON writers, CLI wiring, governance doc presence — **without** a StarCraft II install and **without** replay binding or canonical run artifacts.
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

> **Verdict:** PR-head run **`24059095399`** on **`884055c…`** was **green**; merge to `main` completed at **`6bfe6a7…`**; post-merge `main` CI run **`24059246337`** on that merge commit — **success**. M03 scope remains **fixture/proof-driven**; **not** replay binding; **not** canonical run artifact v0.

**Merge from CI/governance:** ✅ **Green** PR-head before merge; ✅ **Green** post-merge `main` CI on the merge commit.

---

## 7. Next actions

- **M04** — Replay binding to run identity: plan only until authorized; **no** implementation without milestone plan update.
