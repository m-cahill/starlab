# V15-M49 — Bounded scorecard result execution surface v1 (`starlab.v15.bounded_scorecard_result_execution.v1`)

**Milestone:** `V15-M49` — *Bounded Scorecard Result Execution Surface*  
**Profile:** `starlab.v15.m49.bounded_scorecard_result_execution_surface.v1`  
**Emitter:** `python -m starlab.v15.emit_v15_m49_bounded_scorecard_result_execution`

## Purpose

1. **V15-M49 consumes sealed V15-M48 preflight JSON.** Upstream artifact: `v15_bounded_scorecard_execution_preflight.json` (`starlab.v15.bounded_scorecard_execution_preflight.v1` / `starlab.v15.m48.bounded_scorecard_execution_preflight_evidence_requirements_gate.v1`).

2. **M48 evidence preflight readiness is not scorecard execution or scorecard results.** M48 `bounded_scorecard_execution_preflight_ready` is routing for declared evidence only — **not** authorization to claim benchmark pass/fail or strength.

3. **M49 emits bounded scorecard result artifacts from fixture or declared evidence** (`starlab.v15.bounded_scorecard_result_evidence.v1` is an **input contract** modeled in M49 only — not a separate emitted artifact family).

4. **M49 may produce scorecard result values, scorecard total, and win-rate values** only as **bounded** fields on the M49 artifact — classified as **operator_declared** / **fixture_synthetic** / **operator_preflight_bound** semantics via `result_mode`.

5. **M49 does not emit benchmark pass/fail.** `benchmark_passed` and `benchmark_pass_fail_emitted` remain **false**; `pass_fail_interpretation` remains **`not_emitted_in_m49`**.

6. **M49 does not evaluate strength.** `strength_evaluated` remains **false**.

7. **M49 does not promote checkpoints.** `checkpoint_promoted` remains **false**.

8. **M49 does not use `torch.load`.** `torch_load_invoked` remains **false**.

9. **M49 does not load checkpoint blobs.** `checkpoint_blob_loaded` remains **false**.

10. **M49 does not run live StarCraft II.** `live_sc2_executed` remains **false**.

11. **M49 does not run XAI, human-panel evaluation, showcase release, v2 authorization, or T2/T3/T4/T5 ladder execution.** Corresponding booleans remain **false**.

12. **Future pass/fail readout and promotion refusal** require a **separately chartered** milestone (e.g. proposed V15-M50).

## Upstream M48 handling

M49 validates sealed M48 canonical seal (operator paths), contract/profile, `preflight_status` in {`bounded_scorecard_execution_preflight_ready`, `bounded_scorecard_execution_preflight_ready_with_warnings`}, `scorecard_execution_preflight.preflight_surface_status == ready_not_executed`, honesty keys per M48 (no `True` on refused-capable fields), `route_recommendation.route_status == recommended_not_executed`, and `scorecard_execution_performed == false`. When `future_contract_id` / `future_profile_id` are **both absent**, M49 may emit **`bounded_scorecard_result_execution_completed_with_warnings`** (forward-hint warning). When **present**, they must match this milestone’s contract/profile. **Conflicting** forward hints → `refused_route_out_of_scope`.

| M48 preflight status | Typical M49 outcome |
| --- | --- |
| `bounded_scorecard_execution_preflight_ready` | `bounded_scorecard_result_execution_completed` (if evidence validates) |
| `bounded_scorecard_execution_preflight_ready_with_warnings` | `bounded_scorecard_result_execution_completed_with_warnings` |
| `bounded_scorecard_execution_preflight_refused` / not eligible | `bounded_scorecard_result_execution_refused` |

## Typical refusal / evidence codes (operator paths)

Examples recorded on refusal outcomes include **`refused_m48_preflight_not_ready`**, **`refused_invalid_scorecard_result_evidence`**, **`refused_candidate_identity_mismatch`**, and **`refused_missing_metric_results`** (non-exhaustive — see emitter for the full set).

## Artifacts

- `v15_bounded_scorecard_result_execution.json` — sealed decision (`artifact_sha256`)
- `v15_bounded_scorecard_result_execution_report.json` — report companion
- `v15_bounded_scorecard_result_execution_brief.md` — machine brief including required footer

## Profiles

| Profile | Inputs | Behavior |
| --- | --- | --- |
| `fixture_ci` | (none) | `emit_m48_fixture_ci()` chain, synthetic result evidence, full M49 validation |
| `operator_preflight` | `--m48-preflight-json`, `--scorecard-result-evidence-json` | Validates sealed M48 + evidence |
| `operator_declared` | `--declared-result-json` | Normalize / redact declared M49-shaped JSON; refuse overclaims; seal |

## Forbidden CLI flags (deterministic refusal)

Includes `--claim-benchmark-pass`, `--claim-strength`, `--promote-checkpoint`, `--load-checkpoint`, `--run-live-sc2`, `--run-xai`, `--run-human-panel`, `--release-showcase`, `--authorize-v2`, `--execute-t2` … `--execute-t5`. **`--execute-scorecard` is not forbidden** in M49 — bounded emission is from declared evidence, not live gameplay execution.

## Artifact honesty (success path)

When **`bounded_scorecard_result_execution_completed`** or **`bounded_scorecard_result_execution_completed_with_warnings`**: **`scorecard_results_produced`**, **`scorecard_total_computed`**, **`win_rate_computed`** may be **true**; **`claim_decisions.scorecard_results`** may be **`scorecard_results_emitted_bounded`** (bounded artifact emission only). Pending readout labels include **`benchmark_pass_fail_refused_pending_threshold_readout`** and **`promotion_refused_pending_scorecard_readout`**. **`benchmark_passed`**, **`benchmark_pass_fail_emitted`**, **`strength_evaluated`**, **`checkpoint_promoted`**, **`torch_load_invoked`**, **`checkpoint_blob_loaded`**, **`live_sc2_executed`** remain **false**.

## Non-claims

No M49 benchmark pass/fail, strength evaluation, checkpoint promotion, `torch.load`, checkpoint blob loading, live SC2, XAI, human-panel, showcase, v2, or T2–T5 execution is claimed. Scorecard result fields, if emitted, are bounded artifact fields only.
