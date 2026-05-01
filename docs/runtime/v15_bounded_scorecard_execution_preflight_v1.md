# V15-M48 — Bounded scorecard execution preflight v1 (`starlab.v15.bounded_scorecard_execution_preflight.v1`)

**Milestone:** `V15-M48` — *Bounded Scorecard Execution Preflight / Evidence Requirements Gate*  
**Profile:** `starlab.v15.m48.bounded_scorecard_execution_preflight_evidence_requirements_gate.v1`  
**Emitter:** `python -m starlab.v15.emit_v15_m48_bounded_scorecard_execution_preflight`

## Purpose

1. **V15-M48 consumes sealed V15-M47 surface-design JSON.** Upstream artifact: `v15_bounded_scorecard_result_surface_design.json` (`starlab.v15.bounded_scorecard_result_surface_design.v1` / `starlab.v15.m47.bounded_scorecard_result_refusal_gate.v1`).

2. **M47 design readiness is not scorecard results.** Surface-design-ready statuses are **design / refusal bookkeeping only**.

3. **M48 validates evidence requirements for future scorecard execution.** Expected manifest input contract (not a separately emitted artifact family): `starlab.v15.bounded_scorecard_execution_evidence_manifest.v1`, modeled inside M48.

4. **M48 does not execute scorecard evaluation.** `scorecard_execution_allowed_in_m48` remains **`false`**; `scorecard_execution_performed` remains **`false`**.

5. **M48 refuses scorecard result claims.** Outputs keep result booleans **false** and classify execution/result claims as refused where applicable.

6. **M48 refuses benchmark pass/fail claims.** `benchmark_passed` and `benchmark_pass_fail_emitted` remain **false**.

7. **M48 refuses scorecard total / win-rate computation claims.** `scorecard_total_computed` and `win_rate_computed` remain **false**.

8. **M48 refuses strength claims.** `strength_evaluated` remains **false**.

9. **M48 refuses checkpoint promotion.** `checkpoint_promoted` remains **false**.

10. **M48 does not use `torch.load`.**

11. **M48 does not load checkpoint blobs.**

12. **M48 does not run live StarCraft II.** `live_sc2_executed` remains **false**.

13. **M48 does not run XAI, human-panel evaluation, showcase release, v2 authorization, or T2/T3/T4/T5 ladder execution.** Corresponding booleans remain **false**.

14. **Future scorecard result production requires a separately chartered milestone** (e.g. proposed `starlab.v15.bounded_scorecard_result_execution.v1`). Routes such as `route_to_bounded_scorecard_execution_surface` are **`recommended_not_executed`** metadata only — M48 does not execute routed work.

## Upstream M47 handling

| M47 design status | M48 preflight status |
| --- | --- |
| `bounded_scorecard_result_surface_design_ready` | `bounded_scorecard_execution_preflight_ready` |
| `bounded_scorecard_result_surface_design_ready_with_warnings` | `bounded_scorecard_execution_preflight_ready_with_warnings` |
| `bounded_scorecard_result_surface_design_refused` / `refused_*` / not eligible | `bounded_scorecard_execution_preflight_refused` |

M48 validates sealed M47 canonical seal (when consuming sealed artifacts), `route_recommendation.route_status == recommended_not_executed`, `scorecard_surface_design.surface_status == designed_not_executed`, `future_result_surface_allowed_in_m47 == false`, `future_result_surface_requires_separate_milestone == true`, and upstream honesty booleans remain **false**.

## Artifacts

- `v15_bounded_scorecard_execution_preflight.json` — sealed decision (`artifact_sha256`)
- `v15_bounded_scorecard_execution_preflight_report.json` — report companion
- `v15_bounded_scorecard_execution_preflight_brief.md` — machine-readable brief including required footer

## Profiles

| Profile | Inputs | Behavior |
| --- | --- | --- |
| `fixture_ci` | (none) | Calls **`emit_m47_fixture_ci()`**, consumes sealed synthetic M47 + deterministic synthetic evidence manifest |
| `operator_preflight` | **`--m47-surface-design-json`** (required), **`--evidence-manifest-json`** (required) | Validates sealed M47 + manifest structure |
| `operator_declared` | `--declared-preflight-json` | Normalize/redact declared M48 JSON; validate binding / refuse overclaims; seal fresh output |

No operator-local execution profile in M48.

## Forbidden CLI flags (deterministic refusal)

| Flag | Typical refusal |
| --- | --- |
| `--execute-scorecard` | `refused_scorecard_results_claim` |
| `--claim-scorecard-results` | `refused_scorecard_results_claim` |
| `--claim-benchmark-pass` | `refused_benchmark_pass_claim` |
| `--compute-scorecard-total` | `refused_scorecard_total_claim` |
| `--compute-win-rate` | `refused_scorecard_results_claim` |
| `--claim-strength` | `refused_strength_claim` |
| `--promote-checkpoint` | `refused_checkpoint_promotion_claim` |
| `--load-checkpoint` | `refused_checkpoint_load_request` |
| `--run-live-sc2` | `refused_live_sc2_request` |
| `--run-xai` | `refused_xai_claim` |
| `--run-human-panel` | `refused_human_panel_claim` |
| `--release-showcase` | `refused_showcase_release_claim` |
| `--authorize-v2` | `refused_v2_authorization_claim` |
| `--execute-t2` … `--execute-t5` | `refused_t2_t5_execution_claim` |

## Always-false booleans (M48 artifact)

```json
{
  "scorecard_execution_performed": false,
  "scorecard_results_produced": false,
  "benchmark_passed": false,
  "benchmark_pass_fail_emitted": false,
  "scorecard_total_computed": false,
  "win_rate_computed": false,
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

Upstream M47 honesty fields are preserved read-only under `m47_upstream_honesty_snapshot`.

## Gate vocabulary

- `evidence_requirements_satisfied_for_future_preflight`
- `evidence_requirements_incomplete`
- `evidence_requirements_invalid`

## ensure all documentation is updated as necessary

At milestone implementation/closeout per program discipline: update authoritative `docs/starlab-v1.5.md` and minimal pointers in `docs/starlab.md` for V15 navigation.
