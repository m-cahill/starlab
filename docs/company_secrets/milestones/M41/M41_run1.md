# M41 — CI / workflow analysis (merge + main)

**Milestone:** M41 — Replay-Imitation Training Pipeline v1  
**PR:** [#52](https://github.com/m-cahill/starlab/pull/52) — `M41: add replay-imitation training pipeline v1`  
**Branch:** `m41-replay-imitation-training-pipeline-v1` (**retained** on `origin` after merge)

---

## 1. Workflow identity

| Field | Value |
| ----- | ----- |
| Workflow | `CI` (`.github/workflows/ci.yml`) |
| **Authoritative PR-head run** | [`24297208733`](https://github.com/m-cahill/starlab/actions/runs/24297208733) |
| Trigger | `pull_request` |
| Final PR head SHA | `7c092eda7fe6554a2168968ffddbe37e929159e4` |
| Conclusion | **success** |

| Field | Value |
| ----- | ----- |
| **Merge-boundary `main` run** | [`24297269820`](https://github.com/m-cahill/starlab/actions/runs/24297269820) |
| Trigger | `push` (merge of PR #52 to `main`) |
| Merge commit SHA | `5e0add12dd8f4b3a9b4dd31023319cc1999f826b` |
| Merge-boundary `main` head SHA | `5e0add12dd8f4b3a9b4dd31023319cc1999f826b` |
| Merged at (UTC) | **2026-04-12T02:58:11Z** |
| Conclusion | **success** |

---

## 2. Superseded / not merge authority (PR branch)

These runs were **green** on intermediate PR heads for `m41-replay-imitation-training-pipeline-v1` but are **not** merge authority for the final merged head `7c092eda7fe6554a2168968ffddbe37e929159e4`:

| Run | Head (short) | Result | Note |
| --- | ------------ | ------ | ---- |
| [`24297190190`](https://github.com/m-cahill/starlab/actions/runs/24297190190) | `4f85583…` | success | Prior PR head — **superseded** |
| [`24297168010`](https://github.com/m-cahill/starlab/actions/runs/24297168010) | `3155745…` | success | Intermediate — **superseded** |
| [`24297148773`](https://github.com/m-cahill/starlab/actions/runs/24297148773) | — | success | Intermediate — **superseded** |
| [`24297129471`](https://github.com/m-cahill/starlab/actions/runs/24297129471) | — | success | Intermediate — **superseded** |
| [`24297108516`](https://github.com/m-cahill/starlab/actions/runs/24297108516) | `67126bc…` | success | Earlier product push — **superseded** |

**Authoritative PR-head CI** for merge discipline is **`24297208733`** only (matches final PR head).

---

## 3. Required jobs — PR-head (`24297208733`)

| Job | Result |
| --- | ------ |
| `quality` | Pass |
| `smoke` | Pass |
| `tests` | Pass |
| `security` | Pass |
| `fieldtest` | Pass |
| `flagship` | Pass |
| `governance` | Pass |

**Annotations:** GitHub Actions Node.js 20 deprecation notices (informational; pre-existing posture).

---

## 4. Required jobs — merge-boundary `main` (`24297269820`)

| Job | Result |
| --- | ------ |
| `quality` | Pass |
| `smoke` | Pass |
| `tests` | Pass |
| `security` | Pass |
| `fieldtest` | Pass |
| `flagship` | Pass |
| `governance` | Pass |

---

## 5. Non-merge-boundary `main` runs

- **Prior `main` tip before M41 merge** (e.g. doc-only M40 closeout at `d9fd04c…`): CI [`24295373356`](https://github.com/m-cahill/starlab/actions/runs/24295373356) — **not** M41 merge-boundary authority.
- **Closeout / ledger documentation pushes** to `main` **after** merge commit `5e0add12…` (if any): treat as **non-merge-boundary** for M41 product merge — they validate hygiene only; **merge-boundary** for M41 remains **`24297269820`** on **`5e0add12…`**.

---

## 6. Local validation evidence (supplementary)

*Local-only; not a benchmark-integrity, superiority, or public quality claim.*

| Item | Result |
| ---- | ------ |
| Dataset | `tests/fixtures/m26/replay_training_dataset.json` |
| Bundle | Materialized M14 bundle under `out/training_runs/_m14_governed_bundle` (from `tests/fixtures/m14`) |
| JSON-only run (`--no-weights`) | **Success** — `weights_sidecar` null |
| Weights-enabled run | **Success** — local `joblib` under `weights/` |
| SHA-256 vs JSON | **Match** (local file vs recorded metadata) |

---

## 7. Verdict

M41 PR-head and merge-boundary `main` CI are **green** with required jobs passing. **Authoritative** evidence for merge discipline: PR-head **`24297208733`**, merge-boundary **`24297269820`**. Safe to record **M41** closed on `main` per closeout artifacts and tag **`v0.0.41-m41`** on merge commit `5e0add12…`.
