# V15 — Training smoke and short GPU shakedown (M07)

**Document type:** Runtime narrative / operator orientation  
**Project:** STARLAB v1.5 (V15)  
**Milestone:** `V15-M07` — *Training Smoke and Short GPU Shakedown*  
**Status:** Governs receipt emission and **bounded** shakedown only — **not** the long GPU campaign (V15-M08)

## Purpose

Define the **governed training run receipt** for short training smoke, optional **operator-local** GPU or CPU shakedown, and **CI-safe fixture** output. M07 produces **`starlab.v15.training_run_receipt.v1`** with profile **`starlab.v15.training_smoke_short_gpu_shakedown.v1`**, files `v15_training_run_receipt.json` and `v15_training_run_receipt_report.json`.

## Relationship to V15-M02 (environment lock)

M07 may **bind** prior environmental evidence by **canonical JSON SHA-256** of a `v15_long_gpu_environment_lock.json` file. That binding is **not** a substitute for Gate B proof and does not set `long_gpu_run_authorized` to true.

## Relationship to V15-M03 (checkpoint lineage)

M07 may bind **`v15_checkpoint_lineage_manifest.json`** (and other prior contracts) by SHA-256 only. M07 may **write** a small **synthetic** checkpoint under the operator `output` directory and record its **SHA-256** — **not** claim-critical promotion.

## Relationship to V15-M08 (long GPU campaign)

**V15-M08** runs the **long** GPU **campaign**. M07 is **shorter by design** and may only prove **receipts**, **wiring**, and **optional** bounded operator shakedown. A short shakedown receipt is **not** evidence that the long campaign has completed or that a strong agent exists.

## Run classes (posture)

| Class | When | `long_gpu_run_authorized` |
| --- | --- | --- |
| `fixture_smoke` | Default merge CI, no PyTorch, no SC2 | false |
| `operator_declared` | Validates / redacts declared metadata | false |
| `operator_local_short_gpu` | Optional local run with explicit guard + PyTorch | false |

## Profiles

- **`fixture_ci`** (default) — `python -m starlab.v15.emit_v15_training_run_receipt --output-dir <path>`
- **`operator_declared`** — `--profile operator_declared --receipt-json <path> --output-dir <dir>` (optional M02/M03/… JSON bindings)
- **`operator_local_short_gpu`** — requires `--allow-operator-local-execution`; may import **PyTorch** lazily; `--device cuda` **fails** if CUDA is unavailable (no fake GPU evidence)

## Contract fields (summary)

Top-level: `contract_id` (`starlab.v15.training_run_receipt.v1`), `profile_id` (`starlab.v15.training_smoke_short_gpu_shakedown.v1`), `milestone` (`V15-M07`), `run_id`, `run_class`, `profile`, `execution_scope`, `repo_identity`, `environment_binding`, `training_config_binding`, `dataset_binding`, `rights_binding`, `checkpoint_lineage_binding`, `prior_protocol_bindings`, `device_probe`, `sc2_probe`, `disk_probe`, `trainer_identity`, `training_smoke`, `checkpoint_write_receipt`, `resume_receipt`, `rollback_receipt`, `artifact_integrity`, `provenance_gaps`, `redaction_policy`, `optional_bindings`, `operator_notes`, `non_claims`, `authorization_flags`, and seal field `training_run_receipt_sha256`.

**Authorization flags** (subset): `operator_local_execution_performed`, `gpu_shakedown_performed`, `short_training_run_performed`, `checkpoint_write_verified`, `resume_execution_verified`, `rollback_execution_verified`, `long_gpu_run_authorized`, `strong_agent_claim_authorized`, `human_benchmark_claim_authorized`, `benchmark_execution_performed`, `human_panel_execution_performed`, `xai_review_performed`, `v2_authorized`. Program-level claim flags remain **false** in M07.

## Operator-local execution guardrails

- **Must** pass `--allow-operator-local-execution` for `operator_local_short_gpu`.
- **Must** not commit `out/`, `*.pt`, or private **company_secrets** paths.
- **Should** use output under a local `out/…` run root; large artifacts **gitignored**.

## Checkpoint and artifact rules

Operator-local shakedown writes a small `m07_synthetic_shakedown.pt` in the run directory. **Do not** commit weight blobs. Public narrative may list logical ids and hashes only (sanitized).

## Public / private boundary

Redact **absolute paths**, **secrets**, and **PII** in emitted JSON. Keep operator-only hardware detail in private notes. Public registers add **no** new claim-critical rows by default in M07.

## CLI reference

```bash
python -m starlab.v15.emit_v15_training_run_receipt --output-dir <dir> [--profile fixture_ci]

python -m starlab.v15.emit_v15_training_run_receipt --profile operator_declared \
  --receipt-json <path> --output-dir <dir> \
  [--environment-lock-json <m02.json> ...]

python -m starlab.v15.emit_v15_training_run_receipt --profile operator_local_short_gpu \
  --allow-operator-local-execution --output-dir out/v15_m07_shakedown/<run_id> \
  --max-steps 10 --device cuda
```

## Emitted artifacts

- `v15_training_run_receipt.json` — sealed contract (includes `training_run_receipt_sha256`)
- `v15_training_run_receipt_report.json` — summary + `artifact_sha256` matching the seal
- (operator local only) `m07_synthetic_shakedown.pt` — small synthetic checkpoint, **not** for commits

## Non-claims (M07)

V15-M07 defines the training smoke / short GPU shakedown receipt and may run a bounded **isolated synthetic** shakedown only when explicitly invoked. It does not execute the V15-M08 long GPU campaign; does not authorize a long run; does not promote a checkpoint; does not run a strong-agent benchmark; does not run human-panel matches; does not perform XAI review; does not authorize human-benchmark or strong-agent claims; does not approve real public register rows for claim-critical use; does not commit model weights or checkpoint blobs; and does not open v2 or PX2-M04/PX2-M05. A short GPU shakedown receipt is not evidence that the long GPU campaign has completed or that a strong agent exists.
