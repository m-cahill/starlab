# M28 Plan — Learned-Agent Evaluation Harness

**Milestone:** M28 — Learned-Agent Evaluation Harness  
**Tag target:** `v0.0.28-m28`  
**Recommended branch:** `m28-learned-agent-evaluation-harness`  
**Recommended PR title:** `M28: learned-agent evaluation harness`

## Objective

Prove the **first deterministic, offline evaluation harness for a frozen learned subject** in STARLAB.

M28 consumes:

- one governed **M20** `fixture_only` benchmark contract  
- one governed **M27** `replay_imitation_baseline.json`  
- the matching governed **M26** `replay_training_dataset.json`  
- the supplied governed **M14** replay bundle directories referenced by that dataset  

M28 emits:

- `learned_agent_evaluation.json`  
- `learned_agent_evaluation_report.json`  

This milestone is **evaluation only**. It does **not** train a new model, prove benchmark integrity, run live SC2, or introduce hierarchy.

## Scope defaults (locked)

- **Exactly one learned subject in v1:** one frozen M27 baseline artifact.  
- **Exactly one benchmark contract in v1:** one M20-validated `fixture_only` contract.  
- **Default evaluation split in v1:** `test` only (governed M26 `split` assignments; **held-out** = `split == "test"`).  
- **Reuse M20 scorecard structure**; no new schema family for benchmark contracts.  
- **Reuse M27’s in-process materialization seam** (`replay_observation_materialization`); no shell-outs to M16/M18 CLIs.  
- **No tournament (M23), no M24/M25 surfaces** in M28.  
- **CLI `--bundle`:** exact set of bundles referenced by the dataset; **extra** bundle directories are **rejected** (duplicate `bundle_id` from two paths is also rejected).

## Primary artifact contract

### `learned_agent_evaluation.json`

- `evaluation_version` = `starlab.learned_agent_evaluation.v1`  
- `evaluation_sha256`, `benchmark_contract_sha256`, `baseline_sha256`, `training_dataset_sha256`  
- `subject_kind` = `imitation`, `model_family`, `feature_policy_id`, `label_policy_id`  
- `evaluation_split`, `example_count`, embedded **`scorecard`** (M20-validated), `metric_values`, `fallback_count`, `fallback_rate`, `warnings`, `non_claims`  

### `learned_agent_evaluation_report.json`

- `report_version` = `starlab.learned_agent_evaluation_report.v1`  
- Cross-hashes, `evaluation_split`, `example_count`, `label_counts` (true / predicted), `metric_summary`, `fallback_count`, `fallback_rate`, `materialization_warnings`, `non_claims`  

### Benchmark contract (v1 metrics)

`accuracy` (primary), `macro_f1` (secondary), `fallback_rate` (secondary), `example_count` (informational).

### Scorecard `subject_ref`

Identifies the **frozen M27 baseline** (`subject_kind` = `imitation`, `subject_id` = `baseline_sha256`).

## Explicit non-claims

No benchmark integrity, leaderboard validity, live SC2, replay↔execution equivalence, replay parsing in M28 product modules, M23 tournament, M24/M25, retraining, hierarchical agents, or M29+ product surfaces.

**Import guard:** no `starlab.replays`, `starlab.sc2`, `s2protocol` in listed M28 `starlab/evaluation/` product modules.

## Product layout (implemented)

- `docs/runtime/learned_agent_evaluation_harness_v1.md`  
- `starlab/evaluation/learned_agent_evaluation.py`  
- `starlab/evaluation/learned_agent_metrics.py`  
- `starlab/evaluation/learned_agent_models.py`  
- `starlab/evaluation/emit_learned_agent_evaluation.py`  
- `starlab/imitation/replay_imitation_predictor.py` (frozen prediction rule; **M27** `baseline_fit` refactored to use it)  
- `tests/test_learned_agent_evaluation.py`, `tests/fixtures/m28/`  

## Phases (implementation checklist)

1. Runtime contract + M20 fixture benchmark contract (`benchmark_contract_m28.json`).  
2. Harness core: load/validate, compatibility, test split, materialize, predict, metrics.  
3. Deterministic emitters + CLI.  
4. Tests, goldens, AST import guard, governance updates.  
5. Closeout: `docs/starlab.md`, `M28_run1.md`, `M28_summary.md`, `M28_audit.md`, **M29** stub only (no M29 product code).

## Acceptance criteria

Deterministic artifacts; embedded scorecard validates against M20 scorecard schema; governed offline inputs only; fixture E2E green; CI green; ledger honest; M29 remains stub-only after closeout.

---

**Status:** Product implementation complete in-repo; **merge to `main` + authoritative CI** + closeout artifacts (`M28_run1` / summary / audit) **pending** merge gate.
