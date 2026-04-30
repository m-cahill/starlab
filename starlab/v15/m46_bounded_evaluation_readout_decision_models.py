"""V15-M46 — bounded evaluation readout / promotion-refusal decision (consumes sealed M45)."""

from __future__ import annotations

from typing import Final

CONTRACT_ID_M46_READOUT: Final[str] = "starlab.v15.bounded_evaluation_readout_decision.v1"
PROFILE_M46_READOUT: Final[str] = "starlab.v15.m46.bounded_evaluation_readout_promotion_refusal.v1"

MILESTONE_LABEL_M46: Final[str] = "V15-M46"
EMITTER_MODULE_M46: Final[str] = "starlab.v15.emit_v15_m46_bounded_evaluation_readout_decision"

FILENAME_MAIN_JSON: Final[str] = "v15_bounded_evaluation_readout_decision.json"
REPORT_FILENAME: Final[str] = "v15_bounded_evaluation_readout_decision_report.json"
BRIEF_FILENAME: Final[str] = "v15_bounded_evaluation_readout_decision_brief.md"

SCHEMA_VERSION: Final[str] = "1.0"
DIGEST_FIELD: Final[str] = "artifact_sha256"

PROFILE_FIXTURE_CI: Final[str] = "fixture_ci"
PROFILE_OPERATOR_PREFLIGHT: Final[str] = "operator_preflight"
PROFILE_OPERATOR_DECLARED: Final[str] = "operator_declared"

STATUS_READOUT_COMPLETED: Final[str] = "bounded_evaluation_readout_completed"
STATUS_READOUT_COMPLETED_SYNTH_WARNING: Final[str] = (
    "bounded_evaluation_readout_completed_with_synthetic_only_warning"
)
STATUS_READOUT_REFUSED: Final[str] = "bounded_evaluation_readout_refused"

CONTRACT_ID_M45_EXECUTION: Final[str] = "starlab.v15.bounded_candidate_evaluation_execution.v1"
PROFILE_M45_EXECUTION: Final[str] = (
    "starlab.v15.m45.bounded_candidate_evaluation_execution_surface.v1"
)

M45_STATUS_SURFACE_READY: Final[str] = "bounded_candidate_evaluation_execution_surface_ready"
M45_STATUS_COMPLETED_SYNTHETIC: Final[str] = (
    "bounded_candidate_evaluation_execution_completed_synthetic"
)
M45_STATUS_NOT_READY: Final[str] = "bounded_candidate_evaluation_execution_not_ready"

CLAIM_BENCHMARK_REFUSED: Final[str] = "benchmark_claim_refused"
CLAIM_SCORECARD_REFUSED: Final[str] = "scorecard_results_refused"
CLAIM_STRENGTH_REFUSED: Final[str] = "strength_claim_refused"
CLAIM_PROMOTION_REFUSED: Final[str] = "promotion_refused"
CLAIM_XAI_REFUSED: Final[str] = "xai_claim_refused"
CLAIM_HUMAN_PANEL_REFUSED: Final[str] = "human_panel_claim_refused"
CLAIM_SHOWCASE_REFUSED: Final[str] = "showcase_claim_refused"
CLAIM_V2_REFUSED: Final[str] = "v2_claim_refused"
CLAIM_T2_T5_REFUSED: Final[str] = "t2_t5_claim_refused"

PROMOTION_REFUSED_INSUFFICIENT: Final[str] = "promotion_refused_insufficient_evidence"
PROMOTION_NOT_CONSIDERED: Final[str] = "promotion_not_considered_no_scorecard_results"

ROUTE_TO_BENCHMARK_DESIGN: Final[str] = "route_to_bounded_real_benchmark_design"
ROUTE_TO_M45_REMEDIATION: Final[str] = "route_to_m45_remediation_or_reemit"
ROUTE_STATUS_RECOMMENDED_NOT_EXECUTED: Final[str] = "recommended_not_executed"

INTERPRETATION_M45_BINDING: Final[str] = "bounded_execution_bookkeeping_only_not_benchmark_success"

REFUSED_MISSING_M45: Final[str] = "refused_missing_m45_execution"
REFUSED_INVALID_M45: Final[str] = "refused_invalid_m45_execution"
REFUSED_M45_NOT_READY: Final[str] = "refused_m45_execution_not_ready"
REFUSED_M45_HONESTY: Final[str] = "refused_m45_honesty_flags_violation"
REFUSED_M45_SYNTHETIC_OVERINTERPRET: Final[str] = "refused_m45_synthetic_receipt_overinterpreted"
REFUSED_BENCHMARK_PASS_CLAIM: Final[str] = "refused_benchmark_pass_claim"
REFUSED_SCORECARD_RESULTS_CLAIM: Final[str] = "refused_scorecard_results_claim"
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
REFUSED_DECLARED_SHAPE: Final[str] = "refused_invalid_declared_readout_shape"

FORBIDDEN_FLAG_CLAIM_BENCHMARK_PASS: Final[str] = "--claim-benchmark-pass"
FORBIDDEN_FLAG_PRODUCE_SCORECARD: Final[str] = "--produce-scorecard-results"
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
FORBIDDEN_FLAG_INTERPRET_SYNTHETIC: Final[str] = "--interpret-m45-synthetic-as-benchmark-success"

FORBIDDEN_CLI_FLAGS: Final[tuple[str, ...]] = (
    FORBIDDEN_FLAG_CLAIM_BENCHMARK_PASS,
    FORBIDDEN_FLAG_PRODUCE_SCORECARD,
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
    FORBIDDEN_FLAG_INTERPRET_SYNTHETIC,
)

FORBIDDEN_FLAG_TO_REFUSAL: Final[dict[str, str]] = {
    FORBIDDEN_FLAG_CLAIM_BENCHMARK_PASS: REFUSED_BENCHMARK_PASS_CLAIM,
    FORBIDDEN_FLAG_PRODUCE_SCORECARD: REFUSED_SCORECARD_RESULTS_CLAIM,
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
    FORBIDDEN_FLAG_INTERPRET_SYNTHETIC: REFUSED_M45_SYNTHETIC_OVERINTERPRET,
}

M45_HONESTY_BOOL_KEYS: Final[tuple[str, ...]] = (
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

NON_CLAIMS_M46: Final[tuple[str, ...]] = (
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

PROMOTION_REFUSAL_REASON_DEFAULT: Final[str] = (
    "M45 bounded execution bookkeeping and synthetic execution receipts are not sufficient for "
    "checkpoint promotion, because no benchmark pass/fail, scorecard results, strength "
    "evaluation, live SC2 evaluation, or checkpoint-load evaluation was performed."
)

ALLOWED_CLAIM_DECISION_VALUES: Final[frozenset[str]] = frozenset(
    {
        CLAIM_BENCHMARK_REFUSED,
        CLAIM_SCORECARD_REFUSED,
        CLAIM_STRENGTH_REFUSED,
        CLAIM_PROMOTION_REFUSED,
        CLAIM_XAI_REFUSED,
        CLAIM_HUMAN_PANEL_REFUSED,
        CLAIM_SHOWCASE_REFUSED,
        CLAIM_V2_REFUSED,
        CLAIM_T2_T5_REFUSED,
    }
)
