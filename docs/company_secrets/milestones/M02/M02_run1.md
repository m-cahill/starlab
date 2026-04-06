# M02 — CI workflow analysis (PR-head run 1)

**Workflow:** `CI` (`.github/workflows/ci.yml`)  
**Authoritative run ID (current PR tip):** `24052112581`  
**URL:** https://github.com/m-cahill/starlab/actions/runs/24052112581  
**Trigger:** `pull_request`  
**Branch:** `m02-deterministic-match-execution-harness`  
**Head SHA (authoritative for merge gating at this revision):** `1bd98f181c8a65568f8ec4b7d8e6e1fa2bf3431f`  
**PR:** [#3 — M02: deterministic match execution harness](https://github.com/m-cahill/starlab/pull/3)  
**Conclusion:** **success**  
**Recorded:** 2026-04-06 (analysis)

**Earlier green PR-head run (superseded by tip update):** `24052043305` on `888407868cbdd00ca124e2b496f9ca14f909b0fc` (harness implementation only, before closeout-prep docs commit).

---

## 1. Workflow identity (inputs)

| Field | Value |
|-------|--------|
| Workflow name | CI |
| Run ID | 24052112581 |
| Trigger | PR against `main` |
| Commit | `1bd98f1…` (PR tip) |
| Milestone | M02 — Deterministic Match Execution Harness |
| Intent | Land harness + docs + tests; keep CI SC2-free |

**Baseline:** prior trusted green on `main` (M01 era); this run validates the M02 delta on the PR branch.

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
| Pytest | Yes | Tests (includes fake adapter; no SC2) | Pass |
| pip-audit | Yes | Supply chain | Pass |
| CycloneDX SBOM + upload | Yes | SBOM artifact | Pass |
| Gitleaks | Yes | Secret scan | Pass |
| Job summary | Informational | Markdown summary | Pass |

No `continue-on-error` on required checks.  
**Annotation (informational):** Node.js 20 deprecation notice for GitHub Actions — does not fail the job.

---

## 3. Step 2 — Signal integrity

### Tests

- **Tier:** unit / governance smoke + SC2 harness fake path + probe tests.
- **What CI proves:** Config parsing, artifact hashing, fake-adapter harness, map helpers, governance doc presence — all without a StarCraft II install.
- **What CI does not prove:** Real `burnysc2` execution against a live SC2 client, determinism of two real runs on a developer machine, replay binding, or benchmark validity.

### Static / policy gates

- Ruff + Mypy enforce current Python policy; aligned with M02 code changes.

### SC2 / runtime

- **CI remains SC2-free:** default install has no `burnysc2`; optional `sc2-harness` is not installed in CI.

---

## 4. Step 3 — Delta (M02 scope)

**Changed surface:** `starlab/sc2` harness modules, adapters, tests, runtime docs, ledger/README alignment, milestone secrets templates.

**Expected CI coupling:** New tests must pass under fake adapter only — satisfied.

---

## 5. Step 5 — Invariants

- Required checks remain enforced; none weakened for M02.
- No benchmark or replay-scope expansion in CI.
- Consumer contract for STARLAB remains: proof artifact and harness docs are milestone-scoped; non-claims preserved in docs.

---

## 6. Step 6 — Verdict

> **Verdict:** This PR-head run is **green** and is the **authoritative merge gate** for the current PR tip (`1bd98f1…`). It validates repository governance and the **CI-safe** portion of M02 (code + fake path). It does **not** certify local real-match execution or cross-host reproducibility.

**Merge from CI/governance:** ✅ **Merge approved** from a **CI signal** standpoint (all required checks passed on authoritative tip `1bd98f1…`).  
Final milestone **closeout** on `main` still requires **merge**, **post-merge `main` CI** (per project practice), and **local real-execution evidence** before claiming “controlled deterministic match execution” in the ledger.

---

## 7. Step 7 — Next actions

| Owner | Action |
|-------|--------|
| Human | Complete two local `burnysc2` runs + determinism docs (`M02_local_execution_note.md`, `M02_determinism_check.md`, redacted proof JSON). |
| Human | Merge PR #3 when ready; record post-merge `main` CI in §18 at closeout. |
| — | Do not treat CI green alone as M02 **fully closed** without local evidence per plan. |
