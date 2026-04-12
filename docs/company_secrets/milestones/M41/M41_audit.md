# M41 — Delta audit (unified template v2)

* **Milestone:** M41 — Replay-Imitation Training Pipeline v1  
* **Mode:** DELTA AUDIT  
* **Range:** `d9fd04cd823098d6cc064f242a759c8c2d647508` (pre-M41 `main` tip) → `5e0add12dd8f4b3a9b4dd31023319cc1999f826b` (merge commit of PR #52)  
* **CI Status:** Green (authoritative PR-head [`24297208733`](https://github.com/m-cahill/starlab/actions/runs/24297208733); merge-boundary `main` [`24297269820`](https://github.com/m-cahill/starlab/actions/runs/24297269820))  
* **Audit Verdict:** 🟢 — First **governed replay-imitation training pipeline** delivered with explicit **non-claims**; **not** benchmark integrity, **not** live-play proof, **not** M42 product.

---

## Executive summary

**Improvements:** Deterministic **`replay_imitation_training_run.json`** / **`replay_imitation_training_run_report.json`**; sklearn logistic regression over M27 **context_signature** one-hot features; **M40** contract binding + feature schema; **CI** fixture-only path; **`scikit-learn`** pinned in `pyproject.toml`.

**Risks:** Low — no live SC2; weights **not** in repo. **Superseded** intermediate green PR-head runs on the M41 branch are **not** merge authority for final head `7c092ed…`; authoritative PR-head is **`24297208733`** only.

**Residual:** GitHub Actions **Node 20** deprecation annotations (informational).

---

## Delta map & blast radius

* **Changed:** `starlab/imitation/*` (training pipeline, emit CLI), `baseline_fit.py`, `pyproject.toml`, docs, tests.  
* **Risk zones:** `starlab.imitation` training path; sklearn dependency. No auth, no deployment.

---

## Architecture & modularity

### Keep

* Local-first `out/training_runs/` posture; CI exercises minimal fixture path only.

### Fix now

* None blocking post-merge.

### Defer

* M42 comparison harness; optional Actions Node 24 migration.

---

## CI/CD & workflow integrity

* Required jobs on **24297208733** and **24297269820**: **quality**, **smoke**, **tests**, **security**, **fieldtest**, **flagship**, **governance** — all success.  
* **Superseded** (not merge authority for final PR head): [`24297190190`](https://github.com/m-cahill/starlab/actions/runs/24297190190), [`24297168010`](https://github.com/m-cahill/starlab/actions/runs/24297168010), [`24297148773`](https://github.com/m-cahill/starlab/actions/runs/24297148773), [`24297129471`](https://github.com/m-cahill/starlab/actions/runs/24297129471), [`24297108516`](https://github.com/m-cahill/starlab/actions/runs/24297108516) — see `M41_run1.md`.

---

## Tests & coverage

* Full suite + M41 fixture tests; **`fail_under` 78.0** unchanged.

---

## Security & supply chain

* **scikit-learn** added within pinned range; pip-audit / SBOM / Gitleaks green on merge-boundary `main`.

---

## Top issues (max 7)

| ID | Category | Severity | Observation | Recommendation | Guardrail |
| --- | --- | --- | --- | --- | --- |
| — | — | — | No blocking issues | — | — |

---

## PR-sized action plan

| ID | Task | Acceptance |
| --- | --- | --- |
| A1 | None blocking post-M41 | N/A |

---

## Deferred issues registry (append)

| ID | Issue | Discovered | Deferred To | Reason | Blocker? | Exit |
| --- | --- | --- | --- | --- | --- | --- |
| D1 | GitHub Actions Node 20 deprecation | Pre-M41 | TBD | Upstream runner | No | Pin bump when available |

---

## Score trend (placeholder)

| Milestone | Overall |
| --- | --- |
| M41 | Maintained — first governed replay-imitation training pipeline (bounded) |

---

## Flake & regression log

| Item | Status |
| --- | --- |
| M41 PR / merge-boundary main CI | Green |

---

## Local validation (evidence only)

*Dataset:* `tests/fixtures/m26/replay_training_dataset.json`. *Bundle:* materialized under `out/training_runs/_m14_governed_bundle`. JSON-only and weights runs succeeded locally; SHA match for weights file vs JSON — **local-only**, **not** a benchmark-integrity or superiority claim.

---

## Machine-readable appendix

```json
{
  "milestone": "M41",
  "mode": "delta",
  "merge_commit": "5e0add12dd8f4b3a9b4dd31023319cc1999f826b",
  "pr_head": "7c092eda7fe6554a2168968ffddbe37e929159e4",
  "verdict": "green",
  "milestone_kind": "first_governed_replay_imitation_training_pipeline_not_benchmark_or_live_play",
  "quality_gates": {
    "ci_pr_head": "24297208733",
    "ci_main_merge_boundary": "24297269820",
    "superseded_not_authority": [
      "24297190190",
      "24297168010",
      "24297148773",
      "24297129471",
      "24297108516"
    ]
  },
  "non_claims": [
    "no_benchmark_integrity",
    "no_replay_execution_equivalence",
    "no_live_sc2_ci",
    "no_weights_in_repo",
    "no_m42_product_in_m41"
  ]
}
```
