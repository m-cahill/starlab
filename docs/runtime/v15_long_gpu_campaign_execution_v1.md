# V15-M08 — Long GPU Campaign Execution (runtime v1)

**Document type:** Operator runbook / governance narrative  
**Project:** STARLAB v1.5 (V15)  
**Milestone:** `V15-M08` — *Long GPU Campaign Execution*  
**Status:** Implementation surfaces (`starlab.v15.*`) may ship before any operator-local long run completes; **fixture CI** proves schema and guards only.

## Purpose

Define the **governed long GPU campaign** layer: frozen `campaign_plan.json`, preflight gates **A–G**, canonical SHA bindings, `v15_long_gpu_training_manifest.json` + report, optional `v15_long_gpu_campaign_receipt.json` scaffolding, and a **double-guard** wrapper around the existing **M49–M51** `execute_full_local_training_campaign` entrypoint.

## Relationship to M00–M07 gates

Gates **A–G** (governance, environment, data, checkpoints, evaluation, XAI, operator) are recorded in `gate_statuses` on the manifest. **Long campaign execution** requires **pass** on A–D and **G**, and **pass** or **warning** on E–F, unless an explicit **M07 shakedown governance override** is used (rare; must be recorded in operator notes).

**M07** (`starlab.v15.training_run_receipt.v1`, short GPU shakedown) is **not** the long campaign. By default, **gate G** requires a valid **operator-local M07** receipt with **`gpu_shakedown_performed: true`** (CUDA shakedown). Fixture M07 receipts **block** gate G.

## Relationship to M09 (checkpoint promotion)

M08 may produce **candidate** checkpoints and hashes. **Promotion** and benchmark-gated selection are **V15-M09**.

## Relationship to M10 (XAI) and M11 (human benchmark)

M08 may bind **M04** / **M05** / **M06** contracts by SHA only. It does **not** run XAI review, human-panel matches, or authorize claims.

## Run classes and profiles

| Profile | Purpose |
| --- | --- |
| `fixture_ci` | Default CI: deterministic manifest + receipt stub; **no** GPU, **no** PyTorch requirement, **no** `out/` campaign tree. |
| `operator_preflight` | Validates `campaign_plan.json` and binding JSONs; emits manifest + `campaign_plan.json` copy; **does not** run training. |
| `operator_declared` | Normalizes/redacts an operator-supplied manifest JSON. |
| `operator_local_long_gpu` | **Runner only** (`run_v15_long_gpu_campaign`): requires `--allow-operator-local-execution` and `--authorize-long-gpu-campaign`; invokes M50 when preflight is green. |

## Required campaign plan

See `CAMPAIGN_PLAN_REQUIRED_KEYS` in `starlab/v15/long_gpu_training_manifest_models.py`. Required fields include campaign identity, duration/step caps, interval steps, policy blobs, `non_claims`, and **`m49_full_local_training_campaign_contract_path`** (path to `full_local_training_campaign_contract.json`). Optional: **`m49_campaign_root`** (defaults to parent of contract path).

**Example values (not authorization):**

```json
{
  "target_duration_hours": 8,
  "minimum_duration_hours": 2,
  "max_wall_clock_hours": 12,
  "checkpoint_interval_steps": 1000,
  "evaluation_interval_steps": 1000,
  "xai_sample_interval_steps": 5000
}
```

**Fixture / CI test values** may use zeros and interval `1`.

## Operator-local execution guardrails

- Never commit `out/`, weights, raw replays, or `docs/company_secrets/**`.
- Runner refuses to start without both guard flags.
- Use `--dry-run` to validate manifest/plan SHA and gates without calling M50.

## Campaign output tree (suggested)

Under `out/v15_m08_campaigns/<campaign_id>/`: `campaign_plan.json`, manifest + reports, `receipts/`, `checkpoints/`, `lineage/`, `eval/`, `logs/`, `archive/` — **local-only**; see milestone plan for layout details.

## Training engine

**Primary:** `python -m starlab.training.execute_full_local_training_campaign` (M50/M51).  
**Wrapper:** `python -m starlab.v15.run_v15_long_gpu_campaign` forwards to that module after V15 preflight.

## CLI reference

**Emit manifest (fixture):**

```bash
python -m starlab.v15.emit_v15_long_gpu_training_manifest --output-dir <dir> [--profile fixture_ci]
```

**Preflight:**

```bash
python -m starlab.v15.emit_v15_long_gpu_training_manifest \
  --profile operator_preflight \
  --output-dir <dir> \
  --campaign-plan-json <campaign_plan.json> \
  --environment-lock-json <v15_long_gpu_environment_lock.json> \
  --checkpoint-lineage-json <v15_checkpoint_lineage_manifest.json> \
  --m07-training-run-receipt-json <v15_training_run_receipt.json> \
  --training-config-json <training_config.json> \
  --dataset-manifest-json <dataset_manifest.json> \
  --rights-manifest-json <rights_manifest.json>
```

**Declared normalization:**

```bash
python -m starlab.v15.emit_v15_long_gpu_training_manifest \
  --profile operator_declared \
  --output-dir <dir> \
  --manifest-json <path>
```

**Runner (operator-local, after green preflight):**

```bash
python -m starlab.v15.run_v15_long_gpu_campaign \
  --campaign-manifest-json <v15_long_gpu_training_manifest.json> \
  --campaign-plan-json <campaign_plan.json> \
  --output-root out/v15_m08_campaigns/<campaign_id> \
  --allow-operator-local-execution \
  --authorize-long-gpu-campaign
```

Optional: `--dry-run`, `--governance-override-m07-shakedown`, `--post-bootstrap-protocol-phases`.

## Emitted artifacts

- `v15_long_gpu_training_manifest.json` / `v15_long_gpu_training_manifest_report.json`
- `v15_long_gpu_campaign_receipt.json` / report (fixture: not-executed stub)
- `campaign_plan.json` (copy, operator_preflight)

## Non-claims (summary)

M08 does **not** promote checkpoints, pass benchmarks, run human panels, perform XAI review, authorize strong-agent or human-benchmark claims, open v2 or PX2-M04/05, or prove global/ladder claims. A completed long campaign is **training evidence**, not a strong-agent certification.

## Closeout

Public closeout may record `closed — long campaign completed within declared scope`, `blocked`, or `failed with receipts` — **not** “completed” without a real receipt. Implementation-only PRs may remain `implementation_ready_preflight_blocked` or `implementation_ready_waiting_for_operator_run`.

### Implementation PR (2026-04-25)

**[PR #133](https://github.com/m-cahill/starlab/pull/133)** merged the **M08 implementation surface** to `main` (merge `33b277383d3383ada607039b7a7586859a5925a8`). **Authoritative PR-head CI:** [`24940027890`](https://github.com/m-cahill/starlab/actions/runs/24940027890); **merge-boundary `main` CI:** [`24940102671`](https://github.com/m-cahill/starlab/actions/runs/24940102671). **Recorded public status:** **`implementation_ready_waiting_for_operator_run`**. **No** operator-local long GPU campaign was executed for this merge; **`long_gpu_run_authorized`** remains **false** on fixture/default paths. **V15-M09** is **not started** publicly.
