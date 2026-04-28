# V15-M27 — SC2 rollout duration and training-loop integration (v1)

**Contract:** `starlab.v15.sc2_rollout_training_loop_integration.v1`  
**Milestone:** `V15-M27`  
**Runner:** `python -m starlab.v15.run_v15_m27_sc2_rollout_training_loop_integration`

## Purpose

Close the **M26** gap where **synthetic CUDA** checkpoint plumbing worked but the **SC2** rollout path remained **bounded smoke** (`_HarnessBot`, **action_count** **0**). This milestone proves **governed, nontrivial** SC2 rollout **observability** (nonzero actions, observations, bounded horizon) and connects **rollup features** to the **training loop** via an explicit **integration-smoke** step and optional **M49 preflight** consumption.

## Policy

- **policy_id:** `v15_m27_nontrivial_macro_smoke_policy_v1`
- **BurnySc2** `burnysc2_policy` string: `v15_m27_nontrivial_macro_smoke_policy_v1` (maps to the **PX1 watchability** macro/scout Terran scaffold — **not** a new learned policy).

## Commands

**Fixture (CI-safe — no live SC2):**

```powershell
.\.venv\Scripts\python.exe -m starlab.v15.run_v15_m27_sc2_rollout_training_loop_integration `
  --fixture-only `
  --policy-id v15_m27_nontrivial_macro_smoke_policy_v1 `
  --episodes 3 `
  --game-step 8 `
  --max-game-steps 2048 `
  --output-dir out/v15_m27/sc2_rollout_integration_run1
```

**Operator-local real SC2 (dual guards):**

```powershell
.\.venv\Scripts\python.exe -m starlab.v15.run_v15_m27_sc2_rollout_training_loop_integration `
  --allow-operator-local-execution `
  --authorize-sc2-rollout `
  --policy-id v15_m27_nontrivial_macro_smoke_policy_v1 `
  --episodes 3 `
  --game-step 8 `
  --max-game-steps 2048 `
  --output-dir out/v15_m27/sc2_rollout_integration_run1
```

Optional **`--match-config-json`** for a custom BurnySc2 JSON (per-episode **seed** offset).

## Training-loop binding

1. Rollout artifact lists per-episode **action_count**, **observation_count**, **bounded_exit**, **wall_clock_seconds**, and optional **action_types** tallies.
2. **Rollup features** are hashed; one **PyTorch** SGD step runs when **torch** is installed — labeled **`integration_smoke_not_meaningful_learning`** in metadata.
3. **M49 preflight** may consume the integration JSON:

```powershell
python -m starlab.training.emit_full_local_training_campaign_preflight `
  --campaign-contract <path> `
  --output-dir <dir> `
  --m27-sc2-rollout-json <path\to\v15_sc2_rollout_training_loop_integration.json>
```

## Non-claims

See **`docs/starlab-v1.5.md`** **M27 non-claims block**: not strength, not benchmark pass, not checkpoint promotion, not XAI, not human panel, not v2. Fixture mode is **not** live SC2 evidence.
