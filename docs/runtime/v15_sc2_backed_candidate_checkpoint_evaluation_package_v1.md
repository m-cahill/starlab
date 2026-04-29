# V15-M30 — SC2-backed candidate checkpoint evaluation package (runtime)

**Milestone:** `V15-M30`  
**Contract family:** `starlab.v15.candidate_checkpoint_evaluation_package.v1`  
**M30 profile:** `starlab.v15.m30.sc2_backed_candidate_checkpoint_evaluation_package.v1`

## Role

**V15-M30** wraps sealed **M27** → **M28** → **M29** operator JSON receipts into the same candidate checkpoint evaluation **contract family** introduced in **V15-M19**, without reusing M19’s M18/M08/M03-oriented CLI shape.

M30 **does not** load checkpoint blobs, **does not** run benchmark matches, **does not** measure strength, **does not** execute XAI or human-panel evaluation, **does not** authorize v2, **does not** authorize **T2/T3**, and **does not** promote checkpoints.

It validates canonical JSON seals, cross-checks SHA bindings across the three milestones, and emits:

- `v15_candidate_checkpoint_evaluation_package.json`
- `v15_candidate_checkpoint_evaluation_package_report.json`
- `v15_candidate_checkpoint_evaluation_package_checklist.md`

When validation passes, **`evaluation_package_ready`** is **`true`** and **`package_status`** is **`ready_for_future_checkpoint_evaluation`** — assembly/consistency only.

## Inputs

| Input | Role |
| --- | --- |
| `--m27-sc2-rollout-json` | Sealed **`starlab.v15.sc2_rollout_training_loop_integration.v1`** (`v15_sc2_rollout_training_loop_integration.json`) |
| `--m28-sc2-backed-training-json` | Sealed **`starlab.v15.sc2_backed_t1_candidate_training.v1`** (`v15_sc2_backed_t1_candidate_training.json`) |
| `--m29-full-30min-run-json` | Sealed **`starlab.v15.full_30min_sc2_backed_t1_run.v1`** (`v15_full_30min_sc2_backed_t1_run.json`) |
| `--m05-scorecard-json` (optional) | **`starlab.v15.strong_agent_scorecard.v1`** — protocol binding only when supplied and valid |

## Outputs

Emitted under `--output-dir`:

- **`v15_candidate_checkpoint_evaluation_package.json`** — sealed primary artifact (`artifact_sha256`)
- **`v15_candidate_checkpoint_evaluation_package_report.json`** — digest/report companion
- **`v15_candidate_checkpoint_evaluation_package_checklist.md`** — gates G1–G6

## CLI

```powershell
.\.venv\Scripts\python.exe -m starlab.v15.emit_v15_m30_sc2_backed_candidate_checkpoint_evaluation_package `
  --m27-sc2-rollout-json out\v15_m27\sc2_rollout_integration_run1\v15_sc2_rollout_training_loop_integration.json `
  --m28-sc2-backed-training-json out\v15_m29\full_30min_sc2_backed_t1_run1\v15_sc2_backed_t1_candidate_training.json `
  --m29-full-30min-run-json out\v15_m29\full_30min_sc2_backed_t1_run1\v15_full_30min_sc2_backed_t1_run.json `
  --output-dir out\v15_m30\sc2_backed_candidate_checkpoint_evaluation_package_run1
```

Optional scorecard (protocol bind only):

```powershell
.\.venv\Scripts\python.exe -m starlab.v15.emit_v15_m30_sc2_backed_candidate_checkpoint_evaluation_package `
  ... `
  --m05-scorecard-json <path\to\v15_strong_agent_scorecard.json> `
  --output-dir out\v15_m30\sc2_backed_candidate_checkpoint_evaluation_package_run1
```

## Gates / blockers

Machine-readable blocker codes include (sorted when multiple apply):

- Missing inputs (CLI enforces paths exist before parsing)
- `blocked_invalid_m27_contract`, `blocked_invalid_m28_contract`, `blocked_invalid_m29_contract`
- `blocked_m29_full_wall_clock_not_satisfied`
- `blocked_m29_not_candidate_checkpoint_outcome`
- `blocked_m28_m29_artifact_sha_mismatch`
- `blocked_m27_m28_m29_artifact_sha_mismatch`
- `blocked_candidate_checkpoint_sha_mismatch`
- `blocked_candidate_checkpoint_not_produced`
- `blocked_candidate_checkpoint_not_candidate_only`
- `blocked_invalid_scorecard_protocol_json` (only when `--m05-scorecard-json` is supplied but fails contract checks)

**M05 is optional:** omission does **not** block readiness.

## Non-claims

Emitted **`non_claims`** enumerate assembly-only posture (no strength, benchmark pass, promotion, XAI, human-panel, showcase, v2, or T2/T3 authorization).

## Public/private boundary

Raw **`upstream_m27_rollout.resolved_path`** from M28 may contain operator-local absolute paths. Public-facing package JSON carries **`upstream_m27_rollout_public_digest`** with **`resolved_path_status`** **`redacted_operator_local_path`** — not raw absolute paths.

Keep **`out/**`** and operator transcripts untracked.

## See also

- `docs/runtime/v15_candidate_checkpoint_evaluation_package_v1.md` (M19 contract family)  
- `docs/runtime/v15_full_30min_sc2_backed_t1_run_v1.md` (M29)  
- `docs/starlab-v1.5.md` — **§V15-M30**
