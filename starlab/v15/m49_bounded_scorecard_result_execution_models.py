"""V15-M49 — bounded scorecard result execution surface.

Consumes sealed M48 preflight JSON only (no recursive M47–M39 re-adjudication).
"""

from __future__ import annotations

from typing import Final

CONTRACT_ID_M49_RESULT: Final[str] = "starlab.v15.bounded_scorecard_result_execution.v1"
PROFILE_M49_SURFACE: Final[str] = "starlab.v15.m49.bounded_scorecard_result_execution_surface.v1"

SCORECARD_RESULT_EVIDENCE_CONTRACT_ID: Final[str] = (
    "starlab.v15.bounded_scorecard_result_evidence.v1"
)

MILESTONE_LABEL_M49: Final[str] = "V15-M49"
EMITTER_MODULE_M49: Final[str] = "starlab.v15.emit_v15_m49_bounded_scorecard_result_execution"

FILENAME_MAIN_JSON: Final[str] = "v15_bounded_scorecard_result_execution.json"
REPORT_FILENAME: Final[str] = "v15_bounded_scorecard_result_execution_report.json"
BRIEF_FILENAME: Final[str] = "v15_bounded_scorecard_result_execution_brief.md"

SCHEMA_VERSION: Final[str] = "1.0"
DIGEST_FIELD: Final[str] = "artifact_sha256"

PROFILE_FIXTURE_CI: Final[str] = "fixture_ci"
PROFILE_OPERATOR_PREFLIGHT: Final[str] = "operator_preflight"
PROFILE_OPERATOR_DECLARED: Final[str] = "operator_declared"

STATUS_RESULT_COMPLETED: Final[str] = "bounded_scorecard_result_execution_completed"
STATUS_RESULT_COMPLETED_WARNINGS: Final[str] = (
    "bounded_scorecard_result_execution_completed_with_warnings"
)
STATUS_RESULT_REFUSED: Final[str] = "bounded_scorecard_result_execution_refused"

RESULT_MODE_FIXTURE: Final[str] = "fixture_synthetic_scorecard_result"
RESULT_MODE_OPERATOR_DECLARED: Final[str] = "operator_declared_scorecard_result"
RESULT_MODE_OPERATOR_BOUND: Final[str] = "operator_bound_scorecard_result"

INTERPRETATION_SCORECARD_ARTIFACT_ONLY: Final[str] = "scorecard_result_artifact_only"
INTERPRETATION_NOT_STRENGTH: Final[str] = "not_strength_evaluation"
INTERPRETATION_NOT_PROMOTION: Final[str] = "not_checkpoint_promotion"
INTERPRETATION_NOT_HUMAN_BENCHMARK: Final[str] = "not_human_benchmark_claim"
INTERPRETATION_NOT_SHOWCASE: Final[str] = "not_showcase_release"

INTERPRETATIONS_ARTIFACT: Final[tuple[str, ...]] = (
    INTERPRETATION_SCORECARD_ARTIFACT_ONLY,
    INTERPRETATION_NOT_STRENGTH,
    INTERPRETATION_NOT_PROMOTION,
    INTERPRETATION_NOT_HUMAN_BENCHMARK,
    INTERPRETATION_NOT_SHOWCASE,
)

M48_STATUS_READY: Final[str] = "bounded_scorecard_execution_preflight_ready"
M48_STATUS_READY_WARNINGS: Final[str] = "bounded_scorecard_execution_preflight_ready_with_warnings"

ROUTE_STATUS_RECOMMENDED_NOT_EXECUTED: Final[str] = "recommended_not_executed"
ROUTE_READOUT_PROMOTION_REFUSAL: Final[str] = (
    "route_to_scorecard_result_readout_and_promotion_refusal"
)
ROUTE_M48_REMEDIATION: Final[str] = "route_to_m48_remediation_or_reemit"
ROUTE_EVIDENCE_GAP: Final[str] = "route_to_scorecard_evidence_gap_remediation"

WARN_FORWARD_HINT_MISSING: Final[str] = "m49_forward_contract_profile_hints_missing_on_m48"
WARN_CANDIDATE_UPSTREAM_UNAVAILABLE: Final[str] = (
    "candidate_identity_upstream_not_available_for_cross_check"
)

REFUSED_MISSING_M48: Final[str] = "refused_missing_m48_preflight"
REFUSED_INVALID_M48: Final[str] = "refused_invalid_m48_preflight"
REFUSED_M48_NOT_READY: Final[str] = "refused_m48_preflight_not_ready"
REFUSED_M48_HONESTY: Final[str] = "refused_m48_honesty_flags_violation"
REFUSED_M48_ROUTE_EXECUTED: Final[str] = "refused_m48_route_executed"
REFUSED_M48_SCORECARD_ALREADY: Final[str] = "refused_m48_scorecard_execution_already_performed"
REFUSED_MISSING_RESULT_EVIDENCE: Final[str] = "refused_missing_scorecard_result_evidence"
REFUSED_INVALID_RESULT_EVIDENCE: Final[str] = "refused_invalid_scorecard_result_evidence"
REFUSED_CANDIDATE_MISMATCH: Final[str] = "refused_candidate_identity_mismatch"
REFUSED_MISSING_METRICS: Final[str] = "refused_missing_metric_results"
REFUSED_INVALID_METRICS: Final[str] = "refused_invalid_metric_results"
REFUSED_MISSING_THRESHOLD: Final[str] = "refused_missing_threshold_policy"
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
REFUSED_DECLARED_SHAPE: Final[str] = "refused_invalid_declared_m49_shape"

CLAIM_SCORECARD_REFUSED_EMIT: Final[str] = "scorecard_results_refused_not_emitted_in_m49"

CLAIM_SCORECARD_EMITTED_BOUNDED: Final[str] = "scorecard_results_emitted_bounded"
CLAIM_BENCHMARK_PENDING: Final[str] = "benchmark_pass_fail_refused_pending_threshold_readout"
CLAIM_STRENGTH_REFUSED: Final[str] = "strength_claim_refused_not_evaluated"
CLAIM_PROMOTION_PENDING: Final[str] = "promotion_refused_pending_scorecard_readout"
CLAIM_XAI_REFUSED: Final[str] = "xai_claim_refused_not_executed"
CLAIM_HUMAN_REFUSED: Final[str] = "human_panel_claim_refused_not_executed"
CLAIM_SHOWCASE_REFUSED: Final[str] = "showcase_claim_refused_not_released"
CLAIM_V2_REFUSED: Final[str] = "v2_claim_refused_not_authorized"
CLAIM_T2_T5_REFUSED: Final[str] = "t2_t5_claim_refused_not_executed"

FORBIDDEN_FLAG_CLAIM_BENCHMARK_PASS: Final[str] = "--claim-benchmark-pass"
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
    FORBIDDEN_FLAG_CLAIM_BENCHMARK_PASS,
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
    FORBIDDEN_FLAG_CLAIM_BENCHMARK_PASS: REFUSED_BENCHMARK_PASS_CLAIM,
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

INTERPRETATION_M48_BINDING: Final[str] = "evidence_preflight_only_not_scorecard_results"

NON_CLAIMS_M49: Final[tuple[str, ...]] = (
    "bounded_scorecard_result_artifact_fields_only",
    "not_benchmark_pass_fail_readout_in_m49",
    "not_strength_evaluation",
    "not_checkpoint_promotion",
    "not_torch_load",
    "not_checkpoint_blob_loaded",
    "not_live_sc2_execution",
    "not_xai_execution",
    "not_human_panel_execution",
    "not_showcase_release",
    "not_v2_authorization",
    "not_t2_t3_t4_t5_ladder_execution",
    "declared_or_fixture_evidence_only_not_gameplay_execution",
)

M49_SUCCESS_FALSE_KEYS: Final[tuple[str, ...]] = (
    "benchmark_passed",
    "benchmark_pass_fail_emitted",
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

M49_DECLARED_OVERCLAIM_KEYS: Final[tuple[str, ...]] = M49_SUCCESS_FALSE_KEYS + (
    "scorecard_execution_performed",
)

ALLOWED_CLAIM_DECISION_VALUES: Final[frozenset[str]] = frozenset(
    {
        CLAIM_SCORECARD_EMITTED_BOUNDED,
        CLAIM_SCORECARD_REFUSED_EMIT,
        CLAIM_BENCHMARK_PENDING,
        CLAIM_STRENGTH_REFUSED,
        CLAIM_PROMOTION_PENDING,
        CLAIM_XAI_REFUSED,
        CLAIM_HUMAN_REFUSED,
        CLAIM_SHOWCASE_REFUSED,
        CLAIM_V2_REFUSED,
        CLAIM_T2_T5_REFUSED,
    }
)

FIXTURE_ARTIFACT_SHA_PLACEHOLDER: Final[str] = (
    "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
)
