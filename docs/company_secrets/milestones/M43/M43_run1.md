# M43 — CI / workflow analysis (run 1)

**Milestone:** M43 — Hierarchical Training Pipeline v1  
**Purpose:** Authoritative PR-head CI evidence for merge gating (pre-merge; **not** merge-boundary `main` CI — that is recorded at closeout after merge).

---

## Inputs (mandatory)

### Workflow identity

| Field | Value |
| ----- | ----- |
| Workflow | `CI` |
| **Authoritative PR-head run ID** | [`24300836922`](https://github.com/m-cahill/starlab/actions/runs/24300836922) |
| Trigger | `pull_request` |
| Branch | `m43-hierarchical-training-pipeline-v1` |
| **Final PR head SHA** | `71677446c22214f9485841bf5c9c403de90005c2` |
| PR | [#54](https://github.com/m-cahill/starlab/pull/54) — **M43: add hierarchical training pipeline v1** |

**Final PR head (verified):** `7167744` — M43 implementation + `M43_run1.md` (including authoritative CI table aligned to this tip).

**Superseded (not merge authority for final head):** [`24300809086`](https://github.com/m-cahill/starlab/actions/runs/24300809086) on `2f46bb6…`; [`24300781928`](https://github.com/m-cahill/starlab/actions/runs/24300781928) on `719929d…`; [`24300750817`](https://github.com/m-cahill/starlab/actions/runs/24300750817) on `e0df26c…`.

### Change context

- **Milestone / objective:** M43 — first governed hierarchical training run surface (`hierarchical_training_run.json` / report; optional local `joblib`; fixture-only tests).
- **Intent:** Add `starlab.hierarchy` training pipeline, runtime doc, ledger alignment, **no** benchmark-integrity / live-SC2 / M42-integration / M44–M45 product claims.
- **Run character:** Release-related / milestone PR validation on final PR head.

### Baseline reference

- **Trusted green (prior):** `main` at M42 merge (e.g. merge commit `3eb091a…` per ledger); this run validates the M43 delta only.
- **Invariants:** Required CI jobs unchanged; `fail_under` and gates not weakened by this PR.

### Branch provenance

- **`m43-hierarchical-training-pipeline-v1` did not exist on `origin` before this push** — first push created the remote branch; then PR #54 opened.

### Superseded / non-authoritative runs

- **Authoritative PR-head CI** for final head `71677446c22214f9485841bf5c9c403de90005c2`: **[`24300836922`](https://github.com/m-cahill/starlab/actions/runs/24300836922)** — **success**, all required jobs passed.
- **Superseded** — [`24300809086`](https://github.com/m-cahill/starlab/actions/runs/24300809086), [`24300781928`](https://github.com/m-cahill/starlab/actions/runs/24300781928), [`24300750817`](https://github.com/m-cahill/starlab/actions/runs/24300750817) — earlier PR heads; **not** merge authority for tip `7167744…`.

---

## Step 1 — Workflow inventory

| Job / Check | Required (merge-blocking) | Purpose | Pass/Fail | Notes |
| ----------- | ------------------------- | ------- | --------- | ----- |
| `quality` | Yes | Ruff + Mypy | **Pass** | |
| `smoke` | Yes | Fast pytest subset | **Pass** | |
| `tests` | Yes | Full pytest + coverage gate | **Pass** | |
| `security` | Yes | Gitleaks, SBOM, pip-audit | **Pass** | |
| `fieldtest` | Yes | Fixture explorer artifact | **Pass** | |
| `flagship` | Yes | M39 proof pack | **Pass** | |
| `governance` | Yes | Aggregate (no duplicate test execution) | **Pass** | |

**Conclusion:** All listed jobs are merge-blocking per repo CI design; **`governance`** succeeds when prior jobs succeed.

---

## Step 2 — Signal integrity (summary)

- **Tests:** Full suite exercised in `tests` job; M43 adds `test_m43_hierarchical_training_pipeline.py` (determinism, contract binding, CLI, import discipline, delegate fallback).
- **Coverage:** Line/branch gate enforced in `tests` job (unchanged policy).
- **Static gates:** `quality` — Ruff + Mypy green on `starlab` + `tests`.
- **Security:** `security` — informational SARIF + audit artifacts; job **passed**.

---

## Step 3 — Delta analysis

- **Changed surface:** `starlab.hierarchy` training modules, runtime doc, ledger/README/architecture, `.gitignore`, governance test tweak, M43 tests.
- **CI signals affected:** Standard lanes; no workflow edits in PR — no CI config drift.

---

## Step 4 — Failures

- **None.** Workflow conclusion: **`success`**.

---

## Step 5 — Invariants & guardrails

- Required checks remained enforced and **all passed** for run `24300836922`.
- No evidence of gate weakening in this PR.
- M43 non-claims remain documentation-level; no benchmark-integrity inflation.

---

## Step 6 — Verdict

> **Verdict:** PR-head CI run [`24300836922`](https://github.com/m-cahill/starlab/actions/runs/24300836922) completed **successfully** on `71677446c22214f9485841bf5c9c403de90005c2`. All required jobs passed. This run is suitable as **authoritative PR-head CI** for M43 merge review. **Merge-boundary `main` CI** is **not** claimed here — record that only after merge if/when closeout is approved.

**Status:** ✅ Merge approved *from a CI-signal perspective* — human still owns merge button and program gates.

---

## Step 7 — Next actions (minimal)

| Owner | Action |
| ----- | ------ |
| Human | Decide merge vs. follow-up |
| Post-merge (closeout only) | Merge-boundary `main` CI run ID, tag `v0.0.43-m43`, summary/audit, ledger update |

---

## Annotations / warnings (non-blocking)

- **Node.js 20 deprecation** annotations on Actions (GitHub platform; pre-existing pattern). **Not** a failing check.

---

## Local validation (pre-push)

| Check | Result |
| ----- | ------ |
| `git status` | Clean |
| `ruff check starlab tests` | Pass |
| `mypy starlab tests` | Pass |
| `pytest` | 724 passed; 1 DeprecationWarning from `s2protocol` (third-party) |
