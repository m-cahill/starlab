"""V15-M47 — bounded scorecard result surface design / refusal gate (consumes sealed M46)."""

from __future__ import annotations

from typing import Final

CONTRACT_ID_M47_SURFACE: Final[str] = "starlab.v15.bounded_scorecard_result_surface_design.v1"
PROFILE_M47_REFUSAL_GATE: Final[str] = "starlab.v15.m47.bounded_scorecard_result_refusal_gate.v1"

MILESTONE_LABEL_M47: Final[str] = "V15-M47"
EMITTER_MODULE_M47: Final[str] = "starlab.v15.emit_v15_m47_bounded_scorecard_result_surface_design"

FILENAME_MAIN_JSON: Final[str] = "v15_bounded_scorecard_result_surface_design.json"
REPORT_FILENAME: Final[str] = "v15_bounded_scorecard_result_surface_design_report.json"
BRIEF_FILENAME: Final[str] = "v15_bounded_scorecard_result_surface_design_brief.md"

SCHEMA_VERSION: Final[str] = "1.0"
DIGEST_FIELD: Final[str] = "artifact_sha256"

PROFILE_FIXTURE_CI: Final[str] = "fixture_ci"
PROFILE_OPERATOR_PREFLIGHT: Final[str] = "operator_preflight"
PROFILE_OPERATOR_DECLARED: Final[str] = "operator_declared"

STATUS_DESIGN_READY: Final[str] = "bounded_scorecard_result_surface_design_ready"
STATUS_DESIGN_READY_WARNINGS: Final[str] = (
    "bounded_scorecard_result_surface_design_ready_with_warnings"
)
STATUS_DESIGN_REFUSED: Final[str] = "bounded_scorecard_result_surface_design_refused"

CLAIM_SCORECARD_REFUSED: Final[str] = "scorecard_results_refused_not_produced"
CLAIM_BENCHMARK_REFUSED: Final[str] = "benchmark_pass_fail_refused_not_produced"
CLAIM_STRENGTH_REFUSED: Final[str] = "strength_claim_refused_not_evaluated"
CLAIM_PROMOTION_REFUSED: Final[str] = "promotion_refused_no_scorecard_results"
CLAIM_XAI_REFUSED: Final[str] = "xai_claim_refused_not_executed"
CLAIM_HUMAN_PANEL_REFUSED: Final[str] = "human_panel_claim_refused_not_executed"
CLAIM_SHOWCASE_REFUSED: Final[str] = "showcase_claim_refused_not_released"
CLAIM_V2_REFUSED: Final[str] = "v2_claim_refused_not_authorized"
CLAIM_T2_T5_REFUSED: Final[str] = "t2_t5_claim_refused_not_executed"

ROUTE_STATUS_RECOMMENDED_NOT_EXECUTED: Final[str] = "recommended_not_executed"
ROUTE_TO_SCORECARD_EXEC_PREFLIGHT: Final[str] = "route_to_bounded_scorecard_execution_preflight"
ROUTE_TO_M46_REMEDIATION: Final[str] = "route_to_m46_remediation_or_reemit"

INTERPRETATION_M46_BINDING: Final[str] = "readout_refusal_only_not_scorecard_results"

REFUSED_MISSING_M46: Final[str] = "refused_missing_m46_readout"
REFUSED_INVALID_M46: Final[str] = "refused_invalid_m46_readout"
REFUSED_M46_NOT_COMPLETED: Final[str] = "refused_m46_readout_not_completed"
REFUSED_M46_HONESTY: Final[str] = "refused_m46_honesty_flags_violation"
REFUSED_M46_ROUTE_EXECUTED: Final[str] = "refused_m46_route_executed"
REFUSED_M46_PROMOTION_NOT_REFUSED: Final[str] = "refused_m46_promotion_not_refused"
REFUSED_M46_SCORECARD_PRESENT: Final[str] = "refused_m46_scorecard_results_present"
REFUSED_SCORECARD_RESULTS_CLAIM: Final[str] = "refused_scorecard_results_claim"
REFUSED_BENCHMARK_PASS_CLAIM: Final[str] = "refused_benchmark_pass_claim"
REFUSED_STRENGTH_CLAIM: Final[str] = "refused_strength_claim"
REFUSED_PROMOTION_CLAIM: Final[str] = "refused_checkpoint_promotion_claim"
REFUSED_CHECKPOINT_LOAD: Final[str] = "refused_checkpoint_load_request"
REFUSED_LIVE_SC2: Final[str] = "refused_live_sc2_request"
REFUSED_XAI_CLAIM: Final[str] = "refused_xai_claim"
REFUSED_HUMAN_PANEL_CLAIM: Final[str] = "refused_human_panel_claim"
REFUSED_SHOWCASE_CLAIM: Final[str] = "refused_showcase_release_claim"
REFUSED_V2_CLAIM: Final[str] = "refused_v2_authorization_claim"
REFUSED_T2_T5_CLAIM: Final[str] = "refused_t2_t5_execution_claim"
REFUSED_ROUTE_OUT_OF_SCOPE: Final[str] = "refused_route_out_of_scope"
REFUSED_DECLARED_SHAPE: Final[str] = "refused_invalid_declared_scorecard_surface_shape"

FORBIDDEN_FLAG_CLAIM_SCORECARD: Final[str] = "--claim-scorecard-results"
FORBIDDEN_FLAG_CLAIM_BENCHMARK_PASS: Final[str] = "--claim-benchmark-pass"
FORBIDDEN_FLAG_COMPUTE_SCORECARD_TOTAL: Final[str] = "--compute-scorecard-total"
FORBIDDEN_FLAG_CLAIM_STRENGTH: Final[str] = "--claim-strength"
FORBIDDEN_FLAG_PROMOTE_CHECKPOINT: Final[str] = "--promote-checkpoint"
FORBIDDEN_FLAG_LOAD_CHECKPOINT: Final[str] = "--load-checkpoint"
FORBIDDEN_FLAG_RUN_LIVE_SC2: Final[str] = "--run-live-sc2"
FORBIDDEN_FLAG_RUN_XAI: Final[str] = "--run-xai"
FORBIDDEN_FLAG_RUN_HUMAN_PANEL: Final[str] = "--run-human-panel"
FORBIDDEN_FLAG_RELEASE_SHOWCASE: Final[str] = "--release-showcase"
FORBIDDEN_FLAG_AUTHORIZE_V2: Final[str] = "--authorize-v2"
FORBIDDEN_FLAG_EXECUTE_T2: Final[str] = "--execute-t2"
FORBIDDEN_FLAG_EXECUTE_T3: Final[str] = "--execute-t3"
FORBIDDEN_FLAG_EXECUTE_T4: Final[str] = "--execute-t4"
FORBIDDEN_FLAG_EXECUTE_T5: Final[str] = "--execute-t5"

FORBIDDEN_CLI_FLAGS: Final[tuple[str, ...]] = (
    FORBIDDEN_FLAG_CLAIM_SCORECARD,
    FORBIDDEN_FLAG_CLAIM_BENCHMARK_PASS,
    FORBIDDEN_FLAG_COMPUTE_SCORECARD_TOTAL,
    FORBIDDEN_FLAG_CLAIM_STRENGTH,
    FORBIDDEN_FLAG_PROMOTE_CHECKPOINT,
    FORBIDDEN_FLAG_LOAD_CHECKPOINT,
    FORBIDDEN_FLAG_RUN_LIVE_SC2,
    FORBIDDEN_FLAG_RUN_XAI,
    FORBIDDEN_FLAG_RUN_HUMAN_PANEL,
    FORBIDDEN_FLAG_RELEASE_SHOWCASE,
    FORBIDDEN_FLAG_AUTHORIZE_V2,
    FORBIDDEN_FLAG_EXECUTE_T2,
    FORBIDDEN_FLAG_EXECUTE_T3,
    FORBIDDEN_FLAG_EXECUTE_T4,
    FORBIDDEN_FLAG_EXECUTE_T5,
)

FORBIDDEN_FLAG_TO_REFUSAL: Final[dict[str, str]] = {
    FORBIDDEN_FLAG_CLAIM_SCORECARD: REFUSED_SCORECARD_RESULTS_CLAIM,
    FORBIDDEN_FLAG_CLAIM_BENCHMARK_PASS: REFUSED_BENCHMARK_PASS_CLAIM,
    FORBIDDEN_FLAG_COMPUTE_SCORECARD_TOTAL: REFUSED_SCORECARD_RESULTS_CLAIM,
    FORBIDDEN_FLAG_CLAIM_STRENGTH: REFUSED_STRENGTH_CLAIM,
    FORBIDDEN_FLAG_PROMOTE_CHECKPOINT: REFUSED_PROMOTION_CLAIM,
    FORBIDDEN_FLAG_LOAD_CHECKPOINT: REFUSED_CHECKPOINT_LOAD,
    FORBIDDEN_FLAG_RUN_LIVE_SC2: REFUSED_LIVE_SC2,
    FORBIDDEN_FLAG_RUN_XAI: REFUSED_XAI_CLAIM,
    FORBIDDEN_FLAG_RUN_HUMAN_PANEL: REFUSED_HUMAN_PANEL_CLAIM,
    FORBIDDEN_FLAG_RELEASE_SHOWCASE: REFUSED_SHOWCASE_CLAIM,
    FORBIDDEN_FLAG_AUTHORIZE_V2: REFUSED_V2_CLAIM,
    FORBIDDEN_FLAG_EXECUTE_T2: REFUSED_T2_T5_CLAIM,
    FORBIDDEN_FLAG_EXECUTE_T3: REFUSED_T2_T5_CLAIM,
    FORBIDDEN_FLAG_EXECUTE_T4: REFUSED_T2_T5_CLAIM,
    FORBIDDEN_FLAG_EXECUTE_T5: REFUSED_T2_T5_CLAIM,
}

# M46 honesty keys — validated on upstream M46 JSON (matches M46 sealed body).
M46_BODY_BOOL_KEYS: Final[tuple[str, ...]] = (
    "benchmark_passed",
    "benchmark_pass_fail_emitted",
    "scorecard_results_produced",
    "strength_evaluated",
    "checkpoint_promoted",
    "torch_load_invoked",
    "checkpoint_blob_loaded",
    "live_sc2_executed",
    "xai_executed",
    "human_panel_executed",
    "showcase_released",
    "v2_authorized",
    "t2_t3_t4_t5_executed",
)

# M47 artifact always-false block (includes scorecard_total_computed).
M47_ALWAYS_FALSE_KEYS: Final[tuple[str, ...]] = (
    "scorecard_results_produced",
    "benchmark_passed",
    "benchmark_pass_fail_emitted",
    "scorecard_total_computed",
    "strength_evaluated",
    "checkpoint_promoted",
    "torch_load_invoked",
    "checkpoint_blob_loaded",
    "live_sc2_executed",
    "xai_executed",
    "human_panel_executed",
    "showcase_released",
    "v2_authorized",
    "t2_t3_t4_t5_executed",
)

NON_CLAIMS_M47: Final[tuple[str, ...]] = (
    "not_scorecard_results_in_m47",
    "not_benchmark_pass_fail_evidence",
    "not_scorecard_total",
    "not_strength_evaluation",
    "not_checkpoint_promotion",
    "not_torch_load",
    "not_checkpoint_blob_loaded",
    "not_live_sc2",
    "not_xai",
    "not_human_panel",
    "not_showcase",
    "not_v2_authorization",
    "not_t2_t3_t4_t5_ladder_execution",
    "surface_design_only_not_execution",
)

ALLOWED_CLAIM_DECISION_VALUES: Final[frozenset[str]] = frozenset(
    {
        CLAIM_SCORECARD_REFUSED,
        CLAIM_BENCHMARK_REFUSED,
        CLAIM_STRENGTH_REFUSED,
        CLAIM_PROMOTION_REFUSED,
        CLAIM_XAI_REFUSED,
        CLAIM_HUMAN_PANEL_REFUSED,
        CLAIM_SHOWCASE_REFUSED,
        CLAIM_V2_REFUSED,
        CLAIM_T2_T5_REFUSED,
    }
)
