# V15-M21 — Operator T1 30-Minute GPU Run Execution (`starlab.v15.operator_t1_30min_gpu_run_execution.v1`)

**Contract id:** `starlab.v15.operator_t1_30min_gpu_run_execution.v1`  
**Milestone:** `V15-M21`  
**Emitter:** `python -m starlab.v15.emit_v15_operator_t1_30min_gpu_run_execution`  
**Thin wrapper runner:** `python -m starlab.v15.run_v15_m21_t1_30min_gpu_run_execution`

## Purpose

V15-M21 is the first milestone intended to execute the **real** governed **T1 30-minute** operator-local GPU run **or** record an honest **preflight/run blocker**. It does **not** evaluate strength.

It emits execution/evidence artifacts (`v15_operator_t1_30min_gpu_run_execution.json`) **distinct** from **V15-M20** gate artifacts (`v15_real_candidate_checkpoint_production_gate.json`).

If preflight blocks, M21 closes as **preflight/evidence remediation** rather than forcing GPU execution.

A **package-ready** checkpoint after **M21** is eligible for **future evaluation**, **not** promoted strength.

## Relationship to V15-M20

**M20** delivered the candidate checkpoint production **gate**, orchestrator wiring, and CI-safe **`fixture_no_operator_run`** posture; merge CI **did not** perform the full **T1** GPU run.

**M21** delegates training orchestration to **`python -m starlab.v15.run_v15_t1_30min_candidate_checkpoint_gate`** (dual guards required). **M21** owns contract identity, artifact naming, execution framing, **`recommended_m22_fork`**, and public/private semantics — **not** a second training implementation.

## Required operator inputs

Pass explicit paths — **never** rely on hardcoded **`out/**`** paths in public code:

- `--m16-short-gpu-environment-json` — governed **M16** JSON (`operator_local_short_gpu_probe`, probe success where applicable)  
- `--m08-long-gpu-manifest-json` — **M08** training manifest JSON  
- `--m15-preflight-json` — **M15** operator evidence collection preflight JSON  
- `--checkpoint-lineage-json`, `--environment-manifest-json`, `--dataset-manifest-json`, `--evaluation-protocol-json` — **M18/M19** bindings  
- **`campaign_plan.json`** beside the manifest **or** `--campaign-plan-json <path>`  

## Guards

Forwarded to **M20**:

- `--allow-operator-local-execution`  
- `--authorize-t1-30min-gpu-run`  

## Commands

### Dry-run preflight only (no training subprocess inside **M08** path)

```bash
python -m starlab.v15.run_v15_m21_t1_30min_gpu_run_execution \
  --allow-operator-local-execution \
  --authorize-t1-30min-gpu-run \
  --dry-run-preflight-only \
  --m16-short-gpu-environment-json <PRIVATE_M16_JSON> \
  --m08-long-gpu-manifest-json <PRIVATE_M08_MANIFEST_JSON> \
  --m15-preflight-json <PRIVATE_M15_PREFLIGHT_JSON> \
  --checkpoint-lineage-json <PRIVATE_M03_LINEAGE_JSON> \
  --environment-manifest-json <PRIVATE_M02_ENV_JSON> \
  --dataset-manifest-json <PRIVATE_DATASET_MANIFEST_JSON> \
  --evaluation-protocol-json <PRIVATE_M05_SCORECARD_JSON> \
  --output-dir out/v15_m21_operator_t1_30min_gpu_run/t1_preflight
```

### Real T1 run

```bash
python -m starlab.v15.run_v15_m21_t1_30min_gpu_run_execution \
  --allow-operator-local-execution \
  --authorize-t1-30min-gpu-run \
  --m16-short-gpu-environment-json <PRIVATE_M16_JSON> \
  --m08-long-gpu-manifest-json <PRIVATE_M08_MANIFEST_JSON> \
  --m15-preflight-json <PRIVATE_M15_PREFLIGHT_JSON> \
  --checkpoint-lineage-json <PRIVATE_M03_LINEAGE_JSON> \
  --environment-manifest-json <PRIVATE_M02_ENV_JSON> \
  --dataset-manifest-json <PRIVATE_DATASET_MANIFEST_JSON> \
  --evaluation-protocol-json <PRIVATE_M05_SCORECARD_JSON> \
  --max-wall-clock-minutes 30 \
  --output-dir out/v15_m21_operator_t1_30min_gpu_run/t1_001
```

## Run tier

**`T1_30_MIN` only** — **30-minute** wall-clock budget forwarded to **M08**. **T2**/**T3** tiers remain **forward-gated** — **not** executed in **M21**.

## Output layout (operator-local)

Typical subtree after orchestration:

```text
out/v15_m21_operator_t1_30min_gpu_run/t1_001/
  v15_operator_t1_30min_gpu_run_execution.json
  v15_operator_t1_30min_gpu_run_execution_report.json
  v15_operator_t1_30min_gpu_run_execution_runbook.md
  v15_real_candidate_checkpoint_production_gate.json   # upstream M20 gate mirror
  m08/
  candidate/
  m18/
  m19/
```

Do **not** commit **`out/**`** contents.

## Execution status vocabulary

| Status | Meaning |
| --- | --- |
| `operator_preflight_blocked` | Operator inputs invalid / fixture-only / unsafe |
| `t1_30min_run_not_started` | Full training path not entered (incl. dry-run-only posture mapped honestly) |
| `t1_30min_run_failed` | Runner failed before candidate checkpoint |
| `t1_30min_run_completed_no_checkpoint` | Completed without `.pt`/`.pth` |
| `t1_30min_checkpoint_produced_package_blocked` | Checkpoint exists but **M18/M19** blocked |
| `t1_30min_checkpoint_produced_package_ready` | Checkpoint + **M18/M19** structurally aligned |

## Post-run chain

Inspect **M08** receipt → candidate **`.pt`/`.pth`** only (**ignore `.joblib`**) → **M18** readiness → **M19** package assembly → seal **M21** execution JSON.

## Public / private boundary

Sanitized hashes/refs may appear in public artifacts; raw blobs, logs, absolute paths remain **`out/**`** / **`docs/company_secrets/**`** — **not** committed.

## Non-claims

`strength_evaluated`, `checkpoint_promoted`, `benchmark_passed`, `xai_claim_authorized`, `human_benchmark_claim_authorized`, `showcase_release_authorized`, `v2_authorized` remain **false** on honest paths.

## V15-M22 fork decision table

| M21 outcome | Suggested **V15-M22** theme |
| --- | --- |
| `t1_30min_checkpoint_produced_package_ready` | Candidate evaluation **or** 2-hour scale-up gate |
| `t1_30min_checkpoint_produced_package_blocked` | Candidate package remediation |
| `t1_30min_run_completed_no_checkpoint` | Checkpoint emission remediation |
| `t1_30min_run_failed` | Operator GPU run failure remediation |
| `operator_preflight_blocked` | Operator preflight remediation |
| `t1_30min_run_not_started` | Operator scheduling / authorization follow-up |

Planning vocabulary only — **not** v2 authorization.
