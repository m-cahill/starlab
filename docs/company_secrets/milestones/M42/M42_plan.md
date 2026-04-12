# M42 Plan — Learned-Agent Comparison Harness v1

**Milestone:** M42  
**Phase:** VI — Governed Agent Training, Comparison, and Local Validation  
**Status:** In progress on branch `m42-learned-agent-comparison-harness-v1` until merged to `main` with authoritative CI.

---

## Objective

Deliver the first **deterministic, governed comparison layer** for learned candidates: compare the frozen **M27** replay-imitation baseline and one or more **M41** replay-imitation training-run candidates on the **same offline evaluation surface** as **M28**, and emit deterministic **`learned_agent_comparison.json`** / **`learned_agent_comparison_report.json`**.

This is a **comparison** milestone — **not** new training objectives, **not** benchmark-integrity proof, **not** live SC2, **not** M43+ work.

---

## Locked implementation defaults

| Topic | Choice |
| ----- | ------ |
| Metrics | Reuse M28: **accuracy**, **macro_f1**, **fallback_rate**, **example_count** |
| M41 path | **`TrainedRunPredictor`** loading local **`joblib`** sidecar per M41 run artifact |
| Ranking policy id | `starlab.m42.ranking.accuracy_macro_f1_candidate_id_v1` |
| Ranking order | accuracy ↓, macro_f1 ↓, candidate_id ↑ (fallback_rate **not** in ranking chain) |

---

## Deliverables

| Item | Path / artifact |
| ---- | ---------------- |
| Runtime contract | `docs/runtime/learned_agent_comparison_harness_v1.md` |
| Harness | `starlab/evaluation/learned_agent_comparison_*.py`, `emit_learned_agent_comparison.py` |
| Predictor | `starlab/imitation/trained_run_predictor.py` |
| Shared M28 eval | `evaluate_predictor_on_test_split` in `learned_agent_evaluation.py` |
| Tests | `tests/test_m42_learned_agent_comparison.py` |
| Ledger | `docs/starlab.md` (during implementation) |

---

## Out of scope

- New training objectives, hyperparameter search, benchmark-integrity upgrades  
- Replay↔execution equivalence or live-play claims  
- M43 hierarchical training, M44 live-play, M45 RL  
- Committed weights; GPU training or live SC2 in CI  

---

## Closeout (when merging)

Per workflow: `M42_summary.md`, `M42_audit.md`, PR/SHA/CI evidence in §18, tag **`v0.0.42-m42`**, do **not** add merge narrative until actually merged.
