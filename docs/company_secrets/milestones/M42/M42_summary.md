# Milestone Summary — M42: Learned-Agent Comparison Harness v1

**Project:** STARLAB  
**Phase:** VI — Governed Agent Training, Comparison, and Local Validation  
**Milestone:** M42 — Learned-Agent Comparison Harness v1  
**Timeframe:** 2026-04-11 (implementation) → 2026-04-12 (merge to `main`)  
**Status:** Closed  

---

## 1. Milestone Objective

STARLAB needed a **governed, deterministic comparison layer** to evaluate learned candidates on a shared offline metric surface. Without M42, the program would have a training-program charter (**M40**) and a training pipeline (**M41**) but no governed way to **compare** candidate agents (M27 frozen baseline vs M41 training-run candidates) on the same evaluation surface with stable, auditable ranking.

> Without M42, Phase VI would lack a first **deterministic learned-agent comparison harness** — candidates could be trained but not formally compared under governance.

---

## 2. Scope Definition

### In Scope

- `starlab.evaluation`: `learned_agent_comparison_harness.py`, `learned_agent_comparison_models.py`, `learned_agent_comparison_io.py`, `emit_learned_agent_comparison.py`.
- Refactor: `evaluate_predictor_on_test_split` extracted from `learned_agent_evaluation.py` (M28 metric surface reuse).
- `starlab.imitation`: `trained_run_predictor.py` (`TrainedRunPredictor` for M41 `joblib` sidecar loading).
- Artifacts: `learned_agent_comparison.json`, `learned_agent_comparison_report.json`; deterministic `comparison_id` (SHA-256 seal); pairwise metric deltas; ranked candidate ordering.
- Candidate types: `m27_frozen_baseline`, `m41_training_run`.
- Ranking policy: `starlab.m42.ranking.accuracy_macro_f1_candidate_id_v1` (accuracy desc, macro_f1 desc, candidate_id asc; fallback_rate recorded but not used in ranking).
- Metric surface: M28 shared (accuracy, macro_f1, fallback_rate, example_count).
- Runtime: `docs/runtime/learned_agent_comparison_harness_v1.md`.
- Tests: `tests/test_m42_learned_agent_comparison.py`; governance/doc alignment updates.
- Ledger/README/architecture updates on branch; closeout on `main` post-merge.

### Out of Scope

- Benchmark-integrity or replay↔execution equivalence claims.
- Live SC2 in CI; GPU training in CI; weights in repository.
- Statistical significance or leaderboard claims.
- **M43** hierarchical training pipeline product implementation.
- Ladder / live-play superiority claims.

---

## 3. Work Executed

- **[PR #53](https://github.com/m-cahill/starlab/pull/53)** merged to `main` (merge commit `3eb091aba832cb0a66066d6fca6db091eb53c8f5`; final PR head `191a95511a7428b0c12c79edc978070c406ad736`).
- Deterministic comparison harness evaluating M27 `FrozenImitationPredictor` and M41 `TrainedRunPredictor` on the shared M28 metric surface via extracted `evaluate_predictor_on_test_split`.
- Pairwise metric deltas between all candidate pairs; stable ranked ordering with lexicographic tie-breaks.
- CLI: `python -m starlab.evaluation.emit_learned_agent_comparison`.
- 16 files changed (+1093 / −111 lines).

---

## 4. Validation & Evidence

- **Authoritative PR-head CI:** [`24298501553`](https://github.com/m-cahill/starlab/actions/runs/24298501553) — success (all 7 required jobs).
- **Superseded** PR-head runs: none — sole run on final head.
- **Merge-boundary `main` CI:** [`24300065842`](https://github.com/m-cahill/starlab/actions/runs/24300065842) on merge commit `3eb091a…` — success.
- **Local validation:** Ruff check clean, Ruff format clean, Mypy clean, 716 tests passed; working tree clean.
- **Test coverage:** `test_m42_comparison_deterministic_and_ranking_policy` (deterministic repeat + ranking policy + non-claims); `test_m42_emit_cli_smoke` (CLI end-to-end + artifact existence).

---

## 5. CI / Automation Impact

- No new CI jobs; M42 validated via existing **`tests`** lane (fixture-only CPU path).
- No gate weakening; `fail_under` unchanged at **78.0**.

---

## 6. Issues & Exceptions

- **Node 20** deprecation annotations on Actions — informational (pre-existing).

> No new issues were introduced during this milestone.

---

## 7. Deferred Work

- **M43**–**M45** product milestones — stub until each closes on `main`.
- Optional Actions Node 24 migration — outside M42.

---

## 8. Governance Outcomes

- **First governed learned-agent comparison harness** on `main`: deterministic comparison artifacts, explicit ranking policy, bounded non-claims, no weights in repo.
- M28 metric surface reused without modification; `TrainedRunPredictor` parallel to existing `FrozenImitationPredictor`.
- Ranking policy recorded in artifacts with explicit ID `starlab.m42.ranking.accuracy_macro_f1_candidate_id_v1`.

---

## 9. Exit Criteria Evaluation

| Criterion | Met / Partial / Not | Evidence |
| --- | --- | --- |
| Deterministic comparison + report emission | Met | Code + tests + runtime doc |
| M28 metric surface reuse | Met | `evaluate_predictor_on_test_split` extraction |
| M27 + M41 candidate evaluation | Met | `FrozenImitationPredictor` + `TrainedRunPredictor` |
| Ranking policy with explicit ID | Met | Artifacts + tests |
| Fixture-only CI validation | Met | Tests synthesize temp artifacts |
| CI green at merge | Met | `24298501553`, `24300065842` |
| No benchmark-integrity / live-play claims | Met | Docs + artifacts |

---

## 10. Final Verdict

Milestone objectives met. **M42** is closed on `main` with authoritative CI and bounded non-claims. Safe to proceed to **M43** planning only (no M43 product work implied).

---

## 11. Authorized Next Step

- **M43** — Hierarchical Training Pipeline v1 — **stub / planned** until implemented and closed on `main` with its own CI evidence.

---

## 12. Canonical References

- Merge commit: `3eb091aba832cb0a66066d6fca6db091eb53c8f5`
- PR: [#53](https://github.com/m-cahill/starlab/pull/53)
- PR-head CI: [`24298501553`](https://github.com/m-cahill/starlab/actions/runs/24298501553)
- Merge-boundary `main` CI: [`24300065842`](https://github.com/m-cahill/starlab/actions/runs/24300065842)
- Documents: `docs/runtime/learned_agent_comparison_harness_v1.md`, `docs/company_secrets/milestones/M42/M42_plan.md`, `M42_run1.md`, `M42_audit.md`
- Tag: **`v0.0.42-m42`** on merge commit `3eb091a…`
