# V15-M45 — Bounded candidate evaluation execution surface v1 (`starlab.v15.bounded_candidate_evaluation_execution.v1`)

**Milestone:** `V15-M45` — *Bounded Candidate Evaluation Execution Surface*  
**Profile:** `starlab.v15.m45.bounded_candidate_evaluation_execution_surface.v1`  
**Emitter:** `python -m starlab.v15.emit_v15_m45_bounded_candidate_evaluation_execution`

## Purpose

1. **V15-M45 consumes sealed V15-M44 preflight JSON.** Upstream artifact: `v15_bounded_evaluation_execution_preflight.json` (`starlab.v15.bounded_evaluation_execution_preflight.v1` / `starlab.v15.m44.bounded_evaluation_execution_preflight.v1`).

2. **V15-M45 is bounded execution/refusal bookkeeping.** It validates that the bounded execution surface can execute or refuse according to its chartered constraints without producing benchmark results.

3. **M45 trusts the sealed M44 artifact as the immediate upstream authority.** It validates M44's contract, seal, preflight status, `dry_run_plan.plan_status`, and honesty flags. M45 does **not** recursively re-adjudicate M43/M42/M41/M39.

4. **`bounded_evaluation_execution_preflight_ready` from M44 is future preflight bookkeeping only, not benchmark success.** M45 carries this interpretation forward—any "ready" status from M44 is eligibility routing, not benchmark outcome.

5. **V15-M45 does not produce benchmark pass/fail.** `benchmark_passed`, `benchmark_pass_fail_emitted`, and related booleans remain `false`.

6. **V15-M45 does not produce scorecard results.** `scorecard_results_produced` remains `false`.

7. **V15-M45 does not evaluate strength.** `strength_evaluated` remains `false`.

8. **V15-M45 does not promote checkpoints.** `checkpoint_promoted` remains `false`.

9. **V15-M45 does not use `torch.load`.** `torch_load_invoked` remains `false`.

10. **V15-M45 does not load checkpoint blobs.** `checkpoint_blob_loaded` remains `false`.

11. **V15-M45 does not run live StarCraft II by default.** `live_sc2_executed` remains `false`.

12. **V15-M45 does not run XAI, human-panel, showcase, v2 authorization, or T2–T5 ladder execution.** All corresponding booleans remain `false`.

13. **Future benchmark pass/fail, promotion, and XAI review require later milestones.** M45 does not open those surfaces by itself.

## Artifacts

- `v15_bounded_candidate_evaluation_execution.json` — sealed execution/refusal record (`artifact_sha256`)
- `v15_bounded_candidate_evaluation_execution_report.json` — report companion over the sealed body minus `artifact_sha256`
- `v15_bounded_candidate_evaluation_execution_checklist.md` — machine-generated checklist (not benchmark execution evidence)

## Profiles

| Profile | `v15_bounded_evaluation_execution_preflight.json` | Guards required | Behavior |
| --- | :---: | :---: | --- |
| `fixture_ci` | synthesized via upstream M43→M44 fixture chain | none | Deterministic fixture emission; no real execution |
| `operator_preflight` | **required** | none | Validates M44; does not execute; emits `execution_surface_ready` |
| `operator_local_bounded_execution` | **required** | `--allow-operator-local-execution` AND `--authorize-bounded-evaluation-execution` | Emits synthetic execution receipt; no `torch.load`, no blobs, no live SC2 |

**Strict profiles:** `fixture_ci` and `operator_preflight` accept only **clean** M44 `bounded_evaluation_execution_preflight_ready`. **`bounded_evaluation_execution_preflight_ready_with_warnings`** may yield the execution surface only under **`operator_local_bounded_execution`** with explicit warning carry-forward—never silently upgraded.

## Execution receipt semantics

The `execution_receipt` block describes bounded execution posture:

| Field | Meaning |
| --- | --- |
| `receipt_status` | `not_executed_or_synthetic_only` (fixture/preflight) or `synthetic_execution_receipt_emitted` (operator-local) |
| `execution_mode` | `fixture_or_preflight_metadata_only` or `operator_local_synthetic_bounded` |
| `scorecard_mode` | Always `none` |
| `benchmark_mode` | Always `none` |
| `checkpoint_mode` | Always `metadata_only_no_blob_load` |
| `sc2_mode` | Always `not_run` |

**`bounded_candidate_evaluation_execution_completed_synthetic`** means: synthetic execution receipt only—**not** benchmark execution, **not** scorecard results, **not** strength evaluation, **not** checkpoint promotion.

## Forbidden CLI flags

Never execute; emit deterministic refusal rows and keep all execution booleans `false`:

| Flag | Refusal |
| --- | --- |
| `--claim-benchmark-pass` | `refused_disallowed_benchmark_request` |
| `--produce-scorecard-results` | `refused_scorecard_results_request` |
| `--evaluate-strength` | `refused_disallowed_benchmark_request` |
| `--promote-checkpoint` | `refused_promotion_request` |
| `--load-checkpoint` | `refused_checkpoint_load_request` |
| `--run-live-sc2` | `refused_live_sc2_request` |
| `--run-xai` | `refused_xai_request` |
| `--run-human-panel` | `refused_human_panel_request` |
| `--release-showcase` | `refused_showcase_request` |
| `--authorize-v2` | `refused_v2_authorization_request` |
| `--execute-t2` / `--execute-t3` / `--execute-t4` / `--execute-t5` | `refused_route_out_of_scope` |

## Always-false booleans

These remain `false` in all profiles:

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

For `operator_local_bounded_execution` only:

```json
{
  "bounded_execution_surface_invoked": true,
  "synthetic_execution_receipt_emitted": true
}
```

For `fixture_ci` and `operator_preflight`, keep `bounded_execution_surface_invoked` and `synthetic_execution_receipt_emitted` as `false`.

## Non-claims

M45 does **not**:

- Produce benchmark pass/fail
- Claim benchmark success
- Produce scorecard results
- Evaluate strength
- Promote checkpoints
- Train checkpoints
- Invoke `torch.load`
- Load checkpoint blobs
- Run live SC2 (unless a later explicit operator-local execution milestone charters it)
- Run XAI
- Run human-panel evaluation
- Release a showcase agent
- Authorize v2
- Execute T2/T3/T4/T5 ladder stages
- Reinterpret M44 preflight readiness as execution success
- Reinterpret M43 gate readiness as benchmark success

## M44 eligibility rules

M45 can proceed only if M44 is sealed, valid, and has:

| M44 status | `fixture_ci` | `operator_preflight` | `operator_local_bounded_execution` |
| --- | :---: | :---: | :---: |
| `bounded_evaluation_execution_preflight_ready` | allow | allow | allow |
| `bounded_evaluation_execution_preflight_ready_with_warnings` | refuse | refuse | allow (with explicit warning carry-forward) |
| `bounded_evaluation_execution_preflight_not_ready` | refuse | refuse | refuse |
| any `refused_*` | refuse | refuse | refuse |

M45 must preserve and re-state M44's interpretation:

```text
bounded_evaluation_execution_preflight_ready is future preflight bookkeeping only, not benchmark success.
```

## ensure all documentation is updated as necessary

At milestone closeout, update the V15 ledger (`docs/starlab-v1.5.md`) and minimal pointers in `docs/starlab.md` per program discipline.
