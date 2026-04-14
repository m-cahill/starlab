# Learned-agent comparison harness (M42)

**Version:** `starlab.learned_agent_comparison.v1`  
**Ledger:** `docs/starlab.md` §6–§8, §11  
**Emitter:**

```bash
python -m starlab.evaluation.emit_learned_agent_comparison \
  --benchmark-contract <M20 benchmark_contract.json> \
  [--training-program-contract <M40 agent_training_program_contract.json>] \
  --dataset <M26 replay_training_dataset.json> \
  --bundle <M14_bundle_dir> ... \
  --baseline <replay_imitation_baseline.json> \
  [--m41 <id> <replay_imitation_training_run.json> <run_output_dir> ...] \
  --output-dir out/comparisons/<comparison_id>/
```

**Compatibility:** `--contract` remains an alias for `--benchmark-contract` (same M20 file). If both `--benchmark-contract` and `--contract` are passed, they must refer to the **same** path.

Repeat `--m41` for multiple M41 candidates (each id, run JSON, and directory containing `weights/`).

## Two contract surfaces (do not confuse)

| Surface | Milestone | CLI flag | Role in M42 |
| ------- | --------- | -------- | ----------- |
| **M20 benchmark contract** | M20 / M28 metric binding | **`--benchmark-contract`** (or **`--contract`**) | Defines the offline evaluation / benchmark semantics used for M28-style metrics on the test split. Loaded from disk. |
| **M40 training-program charter** | M40 program posture | **`--training-program-contract`** (optional) | Governed training-program JSON (`agent_training_program_contract.json`). If omitted, the harness uses the in-process default from `build_agent_training_program_contract()`. |

**M48 alignment:** When **`--m41`** candidates are present, the harness **fails** (strict) if any M41 run’s `training_program_contract_sha256` or `training_program_contract_version` does not match the **active** M40 charter (loaded or default). This ties comparison-time charter identity to each candidate run’s recorded identity — **auditability**, not benchmark-math changes.

## Purpose

M42 is the first **governed deterministic comparison** milestone: it evaluates **frozen M27** and **M41 training-run** candidates on the **same offline surface** as **M28** (accuracy, macro-F1, fallback rate, example count on the held-out `test` split), then emits **pairwise metric deltas**, a **stable ranking** under `starlab.m42.ranking.accuracy_macro_f1_candidate_id_v1`, and explicit **non-claims**.

M42 does **not** define a new benchmark surface, **not** prove benchmark integrity, **not** live SC2 in CI, **not** replay↔execution equivalence, and **not** M43+ training work.

## Outputs

| File | Role |
| ---- | ---- |
| `learned_agent_comparison.json` | Full comparison: contract binding, dataset identity, candidate rows, metrics, pairwise deltas, `ranked_candidate_ids`, `ranking_policy_id`, `comparison_id` |
| `learned_agent_comparison_report.json` | Compact summary linked by `comparison_id` |

Default layout:

```text
out/comparisons/<comparison_id>/
  learned_agent_comparison.json
  learned_agent_comparison_report.json
```

## Candidate sources

| Type | Loader |
| ---- | ------ |
| `m27_frozen_baseline` | `FrozenImitationPredictor` from `replay_imitation_baseline.json` |
| `m41_training_run` | `TrainedRunPredictor` from local `joblib` sidecar (`weights_sidecar` in run JSON) |

## Ranking (v1)

1. **accuracy** descending  
2. **macro_f1** descending  
3. **candidate_id** ascending  

`fallback_rate` is recorded but **not** used in ranking.

## Local vs CI

- **Training** remains **local-first** (`out/training_runs/`).  
- **CI:** fixture-only, CPU, **no** GPU training, **no** live SC2 — tests synthesize tiny M41 runs + weights in temp space (`tests/test_m42_learned_agent_comparison.py`).

## Non-claims

See `non_claims` in the emitted comparison JSON and `docs/starlab.md` §11.

## Out of scope (M42 / M48)

**Not** benchmark integrity proofs, **not** changing M20 schema families, **not** M41 training semantics beyond charter identity checks for comparison.
