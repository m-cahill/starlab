"""V15-M45 — bounded candidate evaluation execution surface (consumes sealed M44 preflight)."""

from __future__ import annotations

from typing import Final

CONTRACT_ID_M45_EXECUTION: Final[str] = "starlab.v15.bounded_candidate_evaluation_execution.v1"
PROFILE_M45_EXECUTION: Final[str] = (
    "starlab.v15.m45.bounded_candidate_evaluation_execution_surface.v1"
)

MILESTONE_LABEL_M45: Final[str] = "V15-M45"
EMITTER_MODULE_M45: Final[str] = "starlab.v15.emit_v15_m45_bounded_candidate_evaluation_execution"

FILENAME_MAIN_JSON: Final[str] = "v15_bounded_candidate_evaluation_execution.json"
REPORT_FILENAME: Final[str] = "v15_bounded_candidate_evaluation_execution_report.json"
CHECKLIST_FILENAME: Final[str] = "v15_bounded_candidate_evaluation_execution_checklist.md"

SCHEMA_VERSION: Final[str] = "1.0"
DIGEST_FIELD: Final[str] = "artifact_sha256"

PROFILE_FIXTURE_CI: Final[str] = "fixture_ci"
PROFILE_OPERATOR_PREFLIGHT: Final[str] = "operator_preflight"
PROFILE_OPERATOR_LOCAL_BOUNDED_EXECUTION: Final[str] = "operator_local_bounded_execution"

STATUS_EXECUTION_SURFACE_READY: Final[str] = "bounded_candidate_evaluation_execution_surface_ready"
STATUS_EXECUTION_COMPLETED_SYNTHETIC: Final[str] = (
    "bounded_candidate_evaluation_execution_completed_synthetic"
)
STATUS_EXECUTION_NOT_READY: Final[str] = "bounded_candidate_evaluation_execution_not_ready"

CONTRACT_ID_M44_PREFLIGHT: Final[str] = "starlab.v15.bounded_evaluation_execution_preflight.v1"
PROFILE_M44_PREFLIGHT: Final[str] = "starlab.v15.m44.bounded_evaluation_execution_preflight.v1"

M44_STATUS_PREFLIGHT_READY: Final[str] = "bounded_evaluation_execution_preflight_ready"
M44_STATUS_PREFLIGHT_READY_WARNINGS: Final[str] = (
    "bounded_evaluation_execution_preflight_ready_with_warnings"
)

M44_DRY_RUN_PLAN_STATUS_EXPECTED: Final[str] = "constructed_not_executed"

REFUSED_MISSING_M44_PREFLIGHT: Final[str] = "refused_missing_m44_preflight"
REFUSED_INVALID_M44_PREFLIGHT: Final[str] = "refused_invalid_m44_preflight"
REFUSED_M44_PREFLIGHT_NOT_READY: Final[str] = "refused_m44_preflight_not_ready"
REFUSED_M44_HONESTY_FLAGS_VIOLATION: Final[str] = "refused_m44_honesty_flags_violation"
REFUSED_M44_DRY_RUN_PLAN_NOT_CONSTRUCTED: Final[str] = "refused_m44_dry_run_plan_not_constructed"
REFUSED_DISALLOWED_BENCHMARK_REQUEST: Final[str] = "refused_disallowed_benchmark_request"
REFUSED_SCORECARD_RESULTS_REQUEST: Final[str] = "refused_scorecard_results_request"
REFUSED_CHECKPOINT_LOAD_REQUEST: Final[str] = "refused_checkpoint_load_request"
REFUSED_LIVE_SC2_REQUEST: Final[str] = "refused_live_sc2_request"
REFUSED_PROMOTION_REQUEST: Final[str] = "refused_promotion_request"
REFUSED_XAI_REQUEST: Final[str] = "refused_xai_request"
REFUSED_HUMAN_PANEL_REQUEST: Final[str] = "refused_human_panel_request"
REFUSED_SHOWCASE_REQUEST: Final[str] = "refused_showcase_request"
REFUSED_V2_AUTHORIZATION_REQUEST: Final[str] = "refused_v2_authorization_request"
REFUSED_ROUTE_OUT_OF_SCOPE: Final[str] = "refused_route_out_of_scope"
REFUSED_OPERATOR_LOCAL_NOT_AUTHORIZED: Final[str] = "refused_operator_local_not_authorized"

FORBIDDEN_FLAG_CLAIM_BENCHMARK_PASS: Final[str] = "--claim-benchmark-pass"
FORBIDDEN_FLAG_PRODUCE_SCORECARD_RESULTS: Final[str] = "--produce-scorecard-results"
FORBIDDEN_FLAG_EVALUATE_STRENGTH: Final[str] = "--evaluate-strength"
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
    FORBIDDEN_FLAG_CLAIM_BENCHMARK_PASS,
    FORBIDDEN_FLAG_PRODUCE_SCORECARD_RESULTS,
    FORBIDDEN_FLAG_EVALUATE_STRENGTH,
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
    FORBIDDEN_FLAG_CLAIM_BENCHMARK_PASS: REFUSED_DISALLOWED_BENCHMARK_REQUEST,
    FORBIDDEN_FLAG_PRODUCE_SCORECARD_RESULTS: REFUSED_SCORECARD_RESULTS_REQUEST,
    FORBIDDEN_FLAG_EVALUATE_STRENGTH: REFUSED_DISALLOWED_BENCHMARK_REQUEST,
    FORBIDDEN_FLAG_PROMOTE_CHECKPOINT: REFUSED_PROMOTION_REQUEST,
    FORBIDDEN_FLAG_LOAD_CHECKPOINT: REFUSED_CHECKPOINT_LOAD_REQUEST,
    FORBIDDEN_FLAG_RUN_LIVE_SC2: REFUSED_LIVE_SC2_REQUEST,
    FORBIDDEN_FLAG_RUN_XAI: REFUSED_XAI_REQUEST,
    FORBIDDEN_FLAG_RUN_HUMAN_PANEL: REFUSED_HUMAN_PANEL_REQUEST,
    FORBIDDEN_FLAG_RELEASE_SHOWCASE: REFUSED_SHOWCASE_REQUEST,
    FORBIDDEN_FLAG_AUTHORIZE_V2: REFUSED_V2_AUTHORIZATION_REQUEST,
    FORBIDDEN_FLAG_EXECUTE_T2: REFUSED_ROUTE_OUT_OF_SCOPE,
    FORBIDDEN_FLAG_EXECUTE_T3: REFUSED_ROUTE_OUT_OF_SCOPE,
    FORBIDDEN_FLAG_EXECUTE_T4: REFUSED_ROUTE_OUT_OF_SCOPE,
    FORBIDDEN_FLAG_EXECUTE_T5: REFUSED_ROUTE_OUT_OF_SCOPE,
}

NON_CLAIMS_M45: Final[tuple[str, ...]] = (
    "not_benchmark_pass_fail",
    "not_benchmark_execution",
    "not_scorecard_results",
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
)

INTERPRETATION_PREFLIGHT_BOOKKEEPING_ONLY: Final[str] = (
    "preflight_bookkeeping_only_not_benchmark_success"
)

SYNTHETIC_EXECUTION_INTERPRETATION: Final[str] = (
    "synthetic_execution_receipt_only_not_benchmark_execution_not_scorecard_results_"
    "not_strength_evaluation_not_checkpoint_promotion"
)

NOT_INTERPRETED_AS_M44: Final[tuple[str, ...]] = (
    "benchmark_success",
    "benchmark_pass_fail",
    "evaluation_execution",
    "strength_evaluation",
    "checkpoint_promotion",
    "scorecard_results",
)

GUARD_FLAG_ALLOW_OPERATOR_LOCAL_EXECUTION: Final[str] = "--allow-operator-local-execution"
GUARD_FLAG_AUTHORIZE_BOUNDED_EVALUATION_EXECUTION: Final[str] = (
    "--authorize-bounded-evaluation-execution"
)
