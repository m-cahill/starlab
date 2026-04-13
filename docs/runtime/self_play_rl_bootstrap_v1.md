# Self-play / RL bootstrap run contract (M45)

**Version:** `starlab.self_play_rl_bootstrap_run.v1`  
**Report version:** `starlab.self_play_rl_bootstrap_run_report.v1`

## Role

M45 is the **first governed self-play / RL bootstrap surface** for STARLAB. It consumes a **governed M43** hierarchical training candidate (plus local `joblib` weights), drives **bounded rollout collection** through the **M44** local live-play validation harness, records rollout and reward metadata, optionally performs **one conservative weighted re-fit** over the existing sklearn logistic-regression family, and emits **deterministic JSON artifacts** for audit.

This milestone is **bootstrap-only**. It does **not** prove benchmark integrity, replay↔execution equivalence, live SC2 in CI, ladder performance, or a full RL program.

## Output layout

Recommended root:

`out/rl_bootstrap_runs/<run_id>/`

```text
out/rl_bootstrap_runs/<run_id>/
  self_play_rl_bootstrap_run.json
  self_play_rl_bootstrap_run_report.json
  bootstrap_dataset.json
  episodes/
    episode_manifest.json
    e000/
      local_live_play_validation_run.json
      ...
  updated_policy/
    rl_bootstrap_candidate_bundle.joblib   # optional, local-only
```

## CLI

```bash
python -m starlab.training.emit_self_play_rl_bootstrap_run \
  --hierarchical-training-run-dir <M43_DIR> \
  --match-config <M02_MATCH_JSON> \
  --output-dir out/rl_bootstrap_runs/<run_id>/ \
  --runtime-mode fixture_stub_ci \
  [--episodes N] \
  [--seed 42] \
  [--emit-updated-bundle --dataset <M26_DATASET.json> --bundle-dir <M14_BUNDLE_DIR> ...]
```

**Episode defaults:** if `--episodes` is omitted, **1** for `fixture_stub_ci` and **5** for `local_live_sc2`.

**Weighted re-fit:** requires `--emit-updated-bundle`, `--dataset` (must match `hierarchical_training_run.source_dataset.dataset_sha256`), and at least one `--bundle-dir` (same M14 bundles used to build the M43 run).

## `bootstrap_mode` (bounded enum)

| Value | Meaning |
| ----- | ------- |
| `single_candidate_fixture_stub` | Single M43 candidate; M44 `fixture_stub_ci` |
| `single_candidate_local_live` | Single M43 candidate; M44 `local_live_sc2` (operator machine) |
| `mirror_self_play_local` | Reserved; **not** implemented in M45 v1 |

## Policy IDs (v1)

| Field | Default ID |
| ----- | ------------ |
| `reward_policy_id` | `starlab.m45.reward.validation_outcome_v1` |
| `update_policy_id` | `starlab.m45.update.weighted_logistic_refit_v1` |

**Reward (v1):** primary signal from M44 `match_execution.final_status` (`ok` → 1.0; otherwise 0.0) plus a small deterministic step-count shaping term (capped). For **bounded burnysc2** runs, `final_status` is **`ok`** when the M44 harness completed the step cap (validation contract success); the literal SC2 `Result` is **not** used for reward — see `sc2_game_result` on the M44 proof if needed for forensics. **Not** victory, **not** ladder performance.

## Binding and non-claims

Runs must record:

- **M40:** `training_program_contract_sha256` / `training_program_contract_version` (via M43 candidate)
- **M43:** hierarchical training run path + SHA-256; weights path + SHA-256; `interface_trace_schema_version`; `delegate_policy_id`
- **M44:** `runtime_mode`; substrate reference to `starlab.local_live_play_validation_run.v1` and `starlab.m44.semantic_live_action_adapter.v1`

Explicit **non-claims** are listed in the artifact (`non_claims`) and mirror the ledger: no benchmark integrity, no replay↔execution equivalence, no live SC2 in CI, no ladder claims, no weights in repo, no implication of a full RL product beyond this bounded bootstrap.

## Bootstrap dataset summary

`bootstrap_dataset.json` holds a compact manifest pointer (`bootstrap_dataset_version`), episode manifest reference, and `rows_ingested_for_refit` when rollouts produced steps.
