# M42 — Delta audit (unified template v2)

* **Milestone:** M42 — Learned-Agent Comparison Harness v1  
* **Mode:** DELTA AUDIT  
* **Range:** `22f464a144ad37626c62a7e754a8fd93d0427972` (pre-M42 `main` tip) → `3eb091aba832cb0a66066d6fca6db091eb53c8f5` (merge commit of PR #53)  
* **CI Status:** Green (authoritative PR-head [`24298501553`](https://github.com/m-cahill/starlab/actions/runs/24298501553); merge-boundary `main` [`24300065842`](https://github.com/m-cahill/starlab/actions/runs/24300065842))  
* **Audit Verdict:** 🟢 — First **governed learned-agent comparison harness** delivered with explicit **non-claims**; **not** benchmark integrity, **not** live-play proof, **not** M43 product.

---

## Executive summary

**Improvements:** Deterministic **`learned_agent_comparison.json`** / **`learned_agent_comparison_report.json`**; M28 metric surface reuse via extracted `evaluate_predictor_on_test_split`; **`TrainedRunPredictor`** for M41 `joblib` sidecar loading; **ranking policy** `starlab.m42.ranking.accuracy_macro_f1_candidate_id_v1`; pairwise metric deltas; **CI** fixture-only comparison path; CLI `python -m starlab.evaluation.emit_learned_agent_comparison`.

**Risks:** Low — no live SC2; weights **not** in repo. No superseded PR-head runs; authoritative PR-head is **`24298501553`** (sole run on final head).

**Residual:** GitHub Actions **Node 20** deprecation annotations (informational).

---

## Delta map & blast radius

* **Changed:** `starlab/evaluation/*` (comparison harness, models, IO, CLI), `starlab/imitation/trained_run_predictor.py`, `starlab/evaluation/learned_agent_evaluation.py` (refactor), docs, tests.  
* **Risk zones:** `starlab.evaluation` comparison path; `starlab.imitation` predictor loading. No auth, no deployment, no persistence changes.

---

## Architecture & modularity

### Keep

* M28 metric surface reuse via extracted `evaluate_predictor_on_test_split` — clean separation.
* `TrainedRunPredictor` parallel to `FrozenImitationPredictor` — consistent predictor interface.
* Local-first `out/comparisons/` posture; CI exercises minimal fixture path only.

### Fix now

* None blocking post-merge.

### Defer

* M43 hierarchical training pipeline; optional Actions Node 24 migration.

---

## CI/CD & workflow integrity

* Required jobs on **24298501553** and **24300065842**: **quality**, **smoke**, **tests**, **security**, **fieldtest**, **flagship**, **governance** — all success.  
* **Superseded** (not merge authority for final PR head): none — sole run on `191a955…`.

---

## Tests & coverage

* Full suite + M42 fixture tests; **`fail_under` 78.0** unchanged.
* M42-specific: `test_m42_comparison_deterministic_and_ranking_policy`, `test_m42_emit_cli_smoke`, `test_m42_comparison_modules_exist`.

---

## Security & supply chain

* No new dependencies added by M42; pip-audit / SBOM / Gitleaks green on merge-boundary `main`.

---

## Top issues (max 7)

| ID | Category | Severity | Observation | Recommendation | Guardrail |
| --- | --- | --- | --- | --- | --- |
| — | — | — | No blocking issues | — | — |

---

## PR-sized action plan

| ID | Task | Acceptance |
| --- | --- | --- |
| A1 | None blocking post-M42 | N/A |

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
| M42 | Maintained — first governed learned-agent comparison harness (bounded) |

---

## Flake & regression log

| Item | Status |
| --- | --- |
| M42 PR / merge-boundary main CI | Green |

---

## Machine-readable appendix

```json
{
  "milestone": "M42",
  "mode": "delta",
  "merge_commit": "3eb091aba832cb0a66066d6fca6db091eb53c8f5",
  "pr_head": "191a95511a7428b0c12c79edc978070c406ad736",
  "verdict": "green",
  "milestone_kind": "first_governed_learned_agent_comparison_harness_not_benchmark_or_live_play",
  "quality_gates": {
    "ci_pr_head": "24298501553",
    "ci_main_merge_boundary": "24300065842",
    "superseded_not_authority": []
  },
  "non_claims": [
    "no_benchmark_integrity",
    "no_replay_execution_equivalence",
    "no_live_sc2_ci",
    "no_weights_in_repo",
    "no_m43_product_in_m42",
    "no_statistical_significance",
    "no_leaderboard_claims"
  ]
}
```
