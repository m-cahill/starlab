# STARLAB v15 — SC2-backed T1 candidate training (governed contract)

**Contract ID:** `starlab.v15.sc2_backed_t1_candidate_training.v1`

**Milestone:** V15-M28 — *SC2-Backed T1 Candidate Training Attempt*

## Purpose

Consume a **sealed** V15-M27 SC2 rollout integration artifact (`starlab.v15.sc2_rollout_training_loop_integration.v1`), derive a **deterministic feature vector** from real rollout episode fields (actions, observations, tallies, timing, rollup binding metadata), and execute a **bounded** PyTorch training loop that is explicitly **conditioned on those features**.

This milestone is **not** a strength claim. Training is labeled **`sc2_rollout_feature_conditioned_training_smoke_not_strength_learning`** unless separately evidenced.

## Inputs

- **M27 JSON path** (`--m27-sc2-rollout-json`): must exist on disk.
- **Canonical seal:** `artifact_sha256` must equal `sha256_hex_of_canonical_json(body_without_artifact_sha256)` (same sealing rule as other STARLAB JSON artifacts).
- **Preferred upstream posture:** `m27_outcome == sc2_rollout_training_loop_integration_completed` (override with `--allow-partial-m27-outcome` only when explicitly permitted).

## Outputs (operator-local)

Under `--output-dir`:

- `v15_sc2_backed_t1_candidate_training.json` (sealed with `artifact_sha256`)
- `v15_sc2_backed_t1_candidate_training_report.json`
- `v15_sc2_backed_t1_candidate_training_checklist.md`
- Optional `checkpoints/candidate_checkpoint_step_<n>.pt` at `--checkpoint-cadence-updates` boundaries

Candidate checkpoints are **`not_promoted_candidate_only`** — never treated as promoted or benchmark-validated.

## Runner

```bash
python -m starlab.v15.run_v15_m28_sc2_backed_t1_candidate_training \
  --allow-operator-local-execution \
  --authorize-sc2-backed-t1-candidate-training \
  --m27-sc2-rollout-json out/v15_m27/sc2_rollout_integration_run1/v15_sc2_rollout_training_loop_integration.json \
  --max-wall-clock-minutes 30 \
  --output-dir out/v15_m28/sc2_backed_t1_candidate_training_run1
```

**CI / fixture mode (no upstream path on disk):**

```bash
python -m starlab.v15.run_v15_m28_sc2_backed_t1_candidate_training \
  --fixture-only \
  --output-dir out/v15_m28/sc2_backed_t1_fixture_ci
```

### Full-wall-clock mode (operator-only, opt-in)

Smoke runs may stop earlier (loss-floor early stop / update budgets). When a **≤30‑minute bounded** run is insufficient, governance may require explicitly **full-wall** training with **`--require-full-wall-clock`** (paired with **`--disable-loss-floor-early-stop`** and related flags). Default behavior unchanged without these flags.

**V15‑M29** wraps this path for governed full-wall-clock bundles (`python -m starlab.v15.run_v15_m29_full_30min_sc2_backed_t1_run`); closeout posture and seal index are recorded publicly in **`docs/starlab-v1.5.md`** **§V15-M29**.

## Guards

Operator-local execution requires **both** `--allow-operator-local-execution` and `--authorize-sc2-backed-t1-candidate-training`.

## Non-claims

Mirrors other V15 operator milestones: no strength evaluation, benchmark pass, checkpoint promotion, XAI execution, human-panel execution, showcase release, v2 authorization, or T2/T3 execution claims by default.

## M20 / M21 integration

Deferred unless trivial glue exists — recorded as `m20_m21_candidate_gate_integration_deferred_to_m30` on emitted artifacts (V15-M29 rechartered; full-wall-clock evidence gates precede downstream gate glue).
