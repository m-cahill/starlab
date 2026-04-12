# M41 — CI / workflow analysis (Run 1)

**Workflow:** `CI`  
**Run ID (authoritative, final PR head):** [`24297148773`](https://github.com/m-cahill/starlab/actions/runs/24297148773)  
**Trigger:** `pull_request`  
**Branch:** `m41-replay-imitation-training-pipeline-v1`  
**PR:** [#52](https://github.com/m-cahill/starlab/pull/52) — **M41: add replay-imitation training pipeline v1**  
**Final PR head SHA (under review):** `d2ddcc777a36c1cd7332e3a876cfc9cee72bee9d`  
**Branch on origin before this pass:** **No** — branch was created locally and pushed as new (`git ls-remote` was empty before push).

**Authoritative PR-head CI:** **`24297148773`** — **success** (all required jobs below passed).

**Superseded / non-authority (intermediate PR heads, not merge authority for final):**  
- [`24297129471`](https://github.com/m-cahill/starlab/actions/runs/24297129471) on `ffbcf72…` (initial `M41_run1.md` commit)  
- [`24297108516`](https://github.com/m-cahill/starlab/actions/runs/24297108516) on `67126bc…` (M41 product-only commit)  
(Other historical runs, e.g. M40 PR `24295030115` Ruff failure, are **not** merge authority for M41.)

---

## Step 1 — Workflow inventory

| Job / Check | Required (merge gate) | Purpose | Pass/Fail | Notes |
| ----------- | --------------------- | ------- | --------- | ----- |
| `quality` | Yes | Ruff check, Ruff format, Mypy | **Pass** | |
| `smoke` | Yes | Fast pytest smoke subset + JUnit | **Pass** | |
| `tests` | Yes | Full pytest + coverage gate + JUnit | **Pass** | |
| `security` | Yes | pip-audit, CycloneDX SBOM, Gitleaks | **Pass** | |
| `fieldtest` | Yes | Fixture-only M31 explorer + artifact | **Pass** | |
| `flagship` | Yes | M39 proof pack emit + verify + artifact | **Pass** | |
| `governance` | Yes | Aggregate success | **Pass** | |

No `continue-on-error` merge bypass observed.

---

## Step 2 — Signal integrity (brief)

- **Tests:** Full suite + smoke; M41 adds `tests/test_m41_replay_imitation_training_pipeline.py` (fixture-only, CPU).
- **Coverage:** Branch-aware gate unchanged (`fail_under` in `pyproject.toml`).
- **Static:** Ruff + Mypy green on PR head.
- **Security:** pip-audit / SBOM / Gitleaks as configured.

---

## Step 3 — Delta vs baseline

- Adds `scikit-learn` dependency + `starlab.imitation` M41 pipeline modules; governance/docs/tests aligned.
- No CI topology change; no gate weakening.

---

## Step 4 — Failures

- **None** on authoritative run `24297148773`.

---

## Step 5 — Invariants

- Required checks enforced; no muted merge gates identified for this run.

---

## Step 6 — Verdict

**Verdict:** This PR-head CI run is **green** with all required jobs passing. It is appropriate to treat **`24297148773`** as **authoritative PR-head CI** for merge decision (subject to human approval). **Merge-boundary `main` CI** is **not** in scope until after merge.

**Status:** ✅ Merge approved *from a CI-signal perspective* — **human merge approval still required** per program gates.

---

## Step 7 — Next actions

- **Human:** Decide merge vs. request changes.
- **Post-merge (only when explicitly authorized):** merge-boundary `main` CI, tag `v0.0.41-m41`, closeout docs — **not** started here.

---

## Local validation evidence (supplementary)

*This is **local** evidence only; not a benchmark-integrity or superiority claim.*

| Item | Result |
| ---- | ------ |
| Dataset | `tests/fixtures/m26/replay_training_dataset.json` |
| Bundle | Materialized M14 bundle at `out/training_runs/_m14_governed_bundle` (from `tests/fixtures/m14`, same layout as M27/M41 tests) |
| JSON-only run (`--no-weights`) | **Success** — `weights_sidecar: null`; run/report linkage OK |
| Weights-enabled run | **Success** — `weights/replay_imitation_sklearn_bundle.joblib` present |
| SHA-256 vs JSON | **Match** — `artifact_sha256` matched on-disk file (local verification) |

---

## Annotations / warnings (non-blocking)

- **Node.js 20 deprecation** annotations on GitHub Actions (informational; pre-existing across jobs).
