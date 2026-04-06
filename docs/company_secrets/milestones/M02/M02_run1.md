# M02 — CI workflow analysis (PR-head run 1)

**Workflow:** `CI` (`.github/workflows/ci.yml`)  
**Authoritative run ID (current PR tip):** `24054586191`  
**URL:** https://github.com/m-cahill/starlab/actions/runs/24054586191  
**Trigger:** `pull_request`  
**Branch:** `m02-deterministic-match-execution-harness`  
**Head SHA (authoritative for merge gating at this revision):** `c03691b61b8d11aafda55f866232f6d623c70628`  
**PR:** [#3 — M02: deterministic match execution harness](https://github.com/m-cahill/starlab/pull/3)  
**Conclusion:** **success**  
**Recorded:** 2026-04-06 (analysis)

**Earlier green PR-head runs (superseded by tip update):** `24054529734` on `5ec0ccb17c15f6b549da12719369ce1478e31212` (local evidence commit); `24053526611` on `061c2126cc59b3ce4d662c58240216343c21f71a` (prior tip before local-evidence commit); `24053475644` on `bfab038a8f7a4908a5a909131b402ba7909463da` (ledger alignment commit prior to latest tip); `24053430560` on `3952c4071d82a77e633b0cd428da19caac2720ff` (ledger alignment commit prior to that); `24053381609` on `08fb582fa8fe969a02de82257d64dedfea2ff35f` (ledger witness commit prior to that); `24053317502` on `10a2b13ba8115e50037948c014facaa502da6978` (ledger witness commit prior to that); `24053264747` on `22b2b57654c9bc5124059227f363b27ccc63ed6f` (ledger witness commit prior to that); `24053218335` on `d80ae12322c3d2c45c754bb298ac895a8cbe7335` (ledger bump prior to that); `24052325999` on `f457cf54bb9e49a991de7605bc0c2c87b97c9c6a` (doc alignment commit prior to that); `24052230417` on `5f5c8a52684b7bc29642b8d52ba5758d21f28f20` (ledger row prior to that); `24052291273` on `79b341aa53a7102b17db102c8e402d89d04875d4`; `24052172714` on `59dcf15e9912c5f6c1920a495150ff03a5a5af7d` (CI reference alignment); `24052112581` on `1bd98f181c8a65568f8ec4b7d8e6e1fa2bf3431f` (closeout-prep docs); `24052043305` on `888407868cbdd00ca124e2b496f9ca14f909b0fc` (harness implementation only).

---

## 1. Workflow identity (inputs)

| Field | Value |
|-------|--------|
| Workflow name | CI |
| Run ID | 24054586191 |
| Trigger | PR against `main` |
| Commit | `c03691b…` (PR tip) |
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

> **Verdict:** This PR-head run is **green** and is the **authoritative merge gate** for the current PR tip (`c03691b…`). It validates repository governance and the **CI-safe** portion of M02 (code + fake path). It does **not** certify local real-match execution or cross-host reproducibility.

**Merge from CI/governance:** ✅ **Merge approved** from a **CI signal** standpoint (all required checks passed on authoritative tip `c03691b…`).  
Final milestone **closeout** on `main` still requires **merge**, **post-merge `main` CI** (per project practice), and **two successful** local burny runs with a recorded hash outcome before claiming “controlled deterministic match execution” in the ledger (2026-04-06 session documented a **blocked** attempt — no proof hashes).

---

## 7. Step 7 — Next actions

| Owner | Action |
|-------|--------|
| Human | Obtain a valid `.SC2Map` path; repeat two successful `burnysc2` runs; update determinism docs with real `artifact_hash` values (or document mismatch). |
| Human | Merge PR #3 when ready; record post-merge `main` CI in §18 at closeout. |
| — | Do not treat CI green alone as M02 **fully closed** without local evidence per plan. |
