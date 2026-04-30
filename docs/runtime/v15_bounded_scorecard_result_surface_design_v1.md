# V15-M47 — Bounded scorecard result surface design v1 (`starlab.v15.bounded_scorecard_result_surface_design.v1`)

**Milestone:** `V15-M47` — *Bounded Scorecard Result Surface Design / Refusal Gate*  
**Profile:** `starlab.v15.m47.bounded_scorecard_result_refusal_gate.v1`  
**Emitter:** `python -m starlab.v15.emit_v15_m47_bounded_scorecard_result_surface_design`

## Purpose

1. **V15-M47 consumes sealed V15-M46 readout JSON.** Upstream artifact: `v15_bounded_evaluation_readout_decision.json` (`starlab.v15.bounded_evaluation_readout_decision.v1` / `starlab.v15.m46.bounded_evaluation_readout_promotion_refusal.v1`).

2. **M46 readout completion is not scorecard results.** `bounded_evaluation_readout_completed` and `bounded_evaluation_readout_completed_with_synthetic_only_warning` are readout/refusal bookkeeping only — not benchmark pass/fail or scorecard execution evidence.

3. **V15-M47 defines a future scorecard result surface but does not execute it.** `scorecard_surface_design.future_result_surface_allowed_in_m47` is **`false`** — M47 may recommend a future route but does not run scorecard execution.

4. **V15-M47 refuses scorecard result claims.** Outputs keep `scorecard_results_produced` false and classify scorecard-result claims as refused.

5. **V15-M47 refuses benchmark pass/fail claims.** `benchmark_passed` and `benchmark_pass_fail_emitted` remain false.

6. **V15-M47 refuses strength claims.** `strength_evaluated` remains false.

7. **V15-M47 refuses checkpoint promotion.** No promotion semantics; binding reflects M46 promotion refusal posture only.

8. **V15-M47 does not use `torch.load`.**

9. **V15-M47 does not load checkpoint blobs.**

10. **V15-M47 does not run live StarCraft II.** `live_sc2_executed` remains false.

11. **V15-M47 does not run XAI, human-panel evaluation, showcase release, v2 authorization, or T2/T3/T4/T5 ladder execution.** Corresponding booleans remain false.

12. **Future scorecard result production requires a separately chartered milestone** (e.g. proposed `starlab.v15.bounded_scorecard_result_execution.v1`). Route `route_to_bounded_scorecard_execution_preflight` is `recommended_not_executed` metadata only — M47 does not execute routed work.

## Upstream M46 handling

| M46 decision status | M47 design status |
| --- | --- |
| `bounded_evaluation_readout_completed` | `bounded_scorecard_result_surface_design_ready` |
| `bounded_evaluation_readout_completed_with_synthetic_only_warning` | `bounded_scorecard_result_surface_design_ready_with_warnings` |
| `bounded_evaluation_readout_refused` / `refused_*` / not eligible | `bounded_scorecard_result_surface_design_refused` |

M47 validates that M46 `route_recommendation.route_status` is `recommended_not_executed` and that M46 promotion status is one of the refusal postures (`promotion_refused_insufficient_evidence` or `promotion_not_considered_no_scorecard_results`).

## Artifacts

- `v15_bounded_scorecard_result_surface_design.json` — sealed decision (`artifact_sha256`)
- `v15_bounded_scorecard_result_surface_design_report.json` — report companion
- `v15_bounded_scorecard_result_surface_design_brief.md` — machine-readable brief including required footer

## Profiles

| Profile | Inputs | Behavior |
| --- | --- | --- |
| `fixture_ci` | (none) | Reuses existing **M46** `fixture_ci` chain; consumes sealed synthetic M46 through normal M47 validation |
| `operator_preflight` | `--m46-readout-json` sealed M46 | Seal, contract, honesty, route, and promotion checks |
| `operator_declared` | `--declared-scorecard-surface-json` | Normalize/redact declared M47 JSON; validate binding; refuse overclaims; seal fresh output |

No operator-local execution profile in M47.

## Forbidden CLI flags (deterministic refusal)

M47 maintains an **independent** forbidden-flag set (not inherited from M46). All flags map to deterministic refusal vocabulary; all claim booleans remain false:

| Flag | Typical refusal |
| --- | --- |
| `--claim-scorecard-results` | `refused_scorecard_results_claim` |
| `--claim-benchmark-pass` | `refused_benchmark_pass_claim` |
| `--compute-scorecard-total` | `refused_scorecard_results_claim` |
| `--claim-strength` | `refused_strength_claim` |
| `--promote-checkpoint` | `refused_checkpoint_promotion_claim` |
| `--load-checkpoint` | `refused_checkpoint_load_request` |
| `--run-live-sc2` | `refused_live_sc2_request` |
| `--run-xai` | `refused_xai_claim` |
| `--run-human-panel` | `refused_human_panel_claim` |
| `--release-showcase` | `refused_showcase_release_claim` |
| `--authorize-v2` | `refused_v2_authorization_claim` |
| `--execute-t2` … `--execute-t5` | `refused_t2_t5_execution_claim` |

## Always-false booleans (M47 artifact)

```json
{
  "scorecard_results_produced": false,
  "benchmark_passed": false,
  "benchmark_pass_fail_emitted": false,
  "scorecard_total_computed": false,
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

Upstream M46 honesty fields are preserved read-only under `m46_upstream_honesty_snapshot`.

## ensure all documentation is updated as necessary

At milestone implementation/closeout per program discipline: update authoritative `docs/starlab-v1.5.md` and minimal pointers in `docs/starlab.md` for V15 navigation.
