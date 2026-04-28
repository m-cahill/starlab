# V15-M20 — Real Candidate Checkpoint Production Gate (runtime)

**Contract id:** `starlab.v15.real_candidate_checkpoint_production_gate.v1`  
**Milestone:** `V15-M20`  
**Emitter:** `python -m starlab.v15.emit_v15_real_candidate_checkpoint_production_gate`  
**Operator orchestrator:** `python -m starlab.v15.run_v15_t1_30min_candidate_checkpoint_gate`

## Purpose

V15-M20 is the first **real candidate checkpoint production gate** after M19 closed with default **`blocked_missing_candidate_checkpoint_evidence`**. It targets a bounded **30-minute** operator-local GPU run (`T1_30_MIN`) using the existing **M08** campaign runner (`run_v15_long_gpu_campaign`) with forwarded wall-clock limits — **no** separate training stack.

The milestone **permits** an honest operator-local path when preflight passes; it **closes honestly** when the operator run is not performed (`t1_30min_run_not_started`, `operator_preflight_blocked`, or fixture **`fixture_no_operator_run`**).

M20 **does not** evaluate strength or promote checkpoints.

## Relationship to prior milestones

| Milestone | Role |
| --- | --- |
| **M16** | Operator-local short GPU evidence (`starlab.v15.short_gpu_environment_evidence.v1`) — **required** profile `operator_local_short_gpu_probe` + success posture for **real** GPU gate — fixture-only paths **must not** authorize execution |
| **M08** | Long GPU campaign runner — reused with **`--max-wall-clock-minutes 30`** and **`--run-tier T1_30_MIN`** |
| **M15** | Operator evidence collection preflight (`starlab.v15.operator_evidence_collection_preflight.v1`) |
| **M18** | Checkpoint evaluation readiness (`starlab.v15.checkpoint_evaluation_readiness.v1`) — rerun after a candidate checkpoint manifest exists |
| **M19** | Candidate checkpoint evaluation package (`starlab.v15.candidate_checkpoint_evaluation_package.v1`) — rerun after M18 |

## Run-tier ladder (execute **only** T1 in M20)

| Tier | Duration | Milestone posture |
| --- | ---: | --- |
| `T1_30_MIN` | 30 minutes | **V15-M20 target** |
| `T2_2_HOUR` | 2 hours | Forward-gated — **not** M20 |
| `T3_12_HOUR` | 12 hours | Forward-gated — **not** M20 |

## Required inputs (operator orchestrator)

- `--m16-short-gpu-environment-json` — governed M16 evidence JSON  
- `--m08-long-gpu-manifest-json` — sealed M08 training manifest JSON  
- `--m15-preflight-json` — M15 preflight JSON  
- `--campaign-plan-json` — if omitted, `campaign_plan.json` beside the manifest must exist  
- `--checkpoint-lineage-json`, `--environment-manifest-json`, `--dataset-manifest-json`, `--evaluation-protocol-json` — M18/M19 bindings  

## Guards

Dual guards are mandatory:

- `--allow-operator-local-execution`  
- `--authorize-t1-30min-gpu-run`  

Optional **`--dry-run-preflight-only`** validates inputs without invoking M08 training.

## Fixture / CI

Default emitter profile **`fixture_default`** emits **`fixture_no_operator_run`**. CI does **not** execute GPU training.

## Artifacts

Emit:

- `v15_real_candidate_checkpoint_production_gate.json`  
- `v15_real_candidate_checkpoint_production_gate_report.json`  
- `v15_real_candidate_checkpoint_production_runbook.md`  

Operator-local layout under `out/…/<run_id>/` typically includes **`m08/`**, **`candidate/`**, **`m18/`**, **`m19/`** as wired by **`run_v15_t1_30min_candidate_checkpoint_gate`**.

## Candidate checkpoint evidence

Accept **only** real PyTorch artifacts **`.pt`** / **`.pth`** as candidate checkpoint evidence — **not** **`.joblib`**.

Success **does not** mean “checkpoint production gate succeeded” unless a **real** packaged checkpoint (.pt/.pth) is produced and referenced by governed manifests.

## Non-claims (always false on gate outputs unless explicitly noted elsewhere)

These remain **false** in honest public outputs:

`strength_evaluated`, `checkpoint_promoted`, `benchmark_passed`, `xai_claim_authorized`, `human_benchmark_claim_authorized`, `showcase_release_authorized`, `v2_authorized`.

## Public / private boundary

Sanitized refs appear in public artifacts; raw absolute paths stay operator-local.

## Forward fork

When blocked or after an honest no-run posture, follow **`recommended_m20_fork`** / **`docs/starlab-v1.5.md`** (e.g. remediation before retry; longer tiers forward-gated).
