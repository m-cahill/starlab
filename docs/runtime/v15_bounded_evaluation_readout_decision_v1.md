# V15-M46 — Bounded evaluation readout decision v1 (`starlab.v15.bounded_evaluation_readout_decision.v1`)

**Milestone:** `V15-M46` — *Bounded Evaluation Readout / Promotion Refusal Decision*  
**Profile:** `starlab.v15.m46.bounded_evaluation_readout_promotion_refusal.v1`  
**Emitter:** `python -m starlab.v15.emit_v15_m46_bounded_evaluation_readout_decision`

## Purpose

1. **V15-M46 consumes sealed V15-M45 bounded execution JSON.** Upstream artifact: `v15_bounded_candidate_evaluation_execution.json` (`starlab.v15.bounded_candidate_evaluation_execution.v1` / `starlab.v15.m45.bounded_candidate_evaluation_execution_surface.v1`).

2. **M45 synthetic execution receipt is not benchmark execution.** `bounded_candidate_evaluation_execution_completed_synthetic` is bookkeeping only—not benchmark pass/fail.

3. **V15-M46 is a readout/refusal decision surface.** It emits deterministic classifications of what downstream claims may and may not be inferred from bounded execution bookkeeping—without executing benchmarks or loading checkpoints.

4. **V15-M46 refuses benchmark pass/fail claims.** Outputs keep `benchmark_passed` false and classify benchmark claims as refused.

5. **V15-M46 refuses scorecard result claims.** `scorecard_results_produced` remains false.

6. **V15-M46 refuses strength claims.** `strength_evaluated` remains false.

7. **V15-M46 refuses checkpoint promotion.** Default `promotion_refused_insufficient_evidence`; no promoted checkpoint semantics.

8. **V15-M46 does not use `torch.load`.**

9. **V15-M46 does not load checkpoint blobs.**

10. **V15-M46 does not run live StarCraft II.** `live_sc2_executed` remains false.

11. **V15-M46 does not run XAI, human-panel evaluation, showcase release, v2 authorization, or T2/T3/T4/T5 ladder execution.** Corresponding booleans remain false.

12. **Future real benchmark / scorecard / promotion surfaces require separately chartered milestones.** Route recommendations (`route_to_bounded_real_benchmark_design`, `route_to_m45_remediation_or_reemit`) are `recommended_not_executed` metadata only—M46 does not execute routed work.

## Eligible upstream M45 execution statuses

| M45 execution status                                           | M46 decision posture                                                                                                              |
| -------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------- |
| `bounded_candidate_evaluation_execution_surface_ready`          | Readout completed; synthetic-only routing warning omitted; benchmark/scorecard/promotion claims refused                             |
| `bounded_candidate_evaluation_completed_synthetic`              | Readout completed with synthetic-only warning in `warnings`; promotion refused; benchmark interpretation refused                    |
| `bounded_candidate_evaluation_execution_not_ready`, `refused_*` | Readout refused; route `route_to_m45_remediation_or_reemit`                                                                     |

## Artifacts

- `v15_bounded_evaluation_readout_decision.json` — sealed decision (`artifact_sha256`)
- `v15_bounded_evaluation_readout_decision_report.json` — report companion without digest duplicate semantics
- `v15_bounded_evaluation_readout_decision_brief.md` — machine-readable brief including required refusal footer

## Profiles

| Profile              | Inputs                                                                                                       | Behavior                                                                                   |
| -------------------- | ------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------ |
| `fixture_ci`         | synthesized M43→M44→M45 fixture                                                                              | Validates sealed upstream M46 path end-to-end in CI fixtures                               |
| `operator_preflight` | `--m45-execution-json` sealed M45                                                                          | Validates seal, honesty flags, statuses; deterministic readout                           |
| `operator_declared`  | `--declared-readout-json` (same contract/profile as M46, shape-constrained; includes `m45_binding` metadata) | Normalize/redact declared JSON; refuse overclaims; seal fresh deterministic output         |

Operator-local bounded execution guards are **not** part of `V15-M46`—there is **no** M46 execution surface beyond decision bookkeeping.

## Forbidden CLI flags (deterministic refusal)

All flags map to deterministic refusal vocabulary and preserve all claim booleans as false:

| Flag | Typical refusal |
| --- | --- |
| `--claim-benchmark-pass` | `refused_benchmark_pass_claim` |
| `--produce-scorecard-results` | `refused_scorecard_results_claim` |
| `--claim-strength` | `refused_strength_claim` |
| `--promote-checkpoint` | `refused_checkpoint_promotion_claim` |
| `--load-checkpoint` | `refused_checkpoint_load_request` |
| `--run-live-sc2` | `refused_live_sc2_request` |
| `--run-xai` | `refused_xai_claim` |
| `--run-human-panel` | `refused_human_panel_claim` |
| `--release-showcase` | `refused_showcase_release_claim` |
| `--authorize-v2` | `refused_v2_authorization_claim` |
| `--execute-t2` / `--execute-t3` / `--execute-t4` / `--execute-t5` | `refused_t2_t5_execution_claim` |
| `--interpret-m45-synthetic-as-benchmark-success` | `refused_m45_synthetic_receipt_overinterpreted` |

## Always-false booleans

Aligned with bounded governance posture:

```json
{
  "benchmark_passed": false,
  "benchmark_pass_fail_emitted": false,
  "scorecard_results_produced": false,
  "strength_evaluated": false,
  "checkpoint_promoted": false,
  "torch_load_invoked": false,
  "checkpoint_blob_loaded": false,
  "live_sc2_executed": false,
  "xai_executed": false,
  "human_panel_executed": false,
  "showcase_released": false,
  "v2_authorized": false,
  "t2_t3_t4_t5_executed": false
}
```

Upstream M45 booleans are preserved read-only under `m45_upstream_honesty_snapshot` for audit lineage.

## ensure all documentation is updated as necessary

At milestone implementation/closeout per program discipline: update authoritative `docs/starlab-v1.5.md` and minimal pointers in `docs/starlab.md` for V15 navigation.
