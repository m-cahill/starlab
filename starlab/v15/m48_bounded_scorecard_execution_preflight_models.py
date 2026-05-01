"""V15-M48 — bounded scorecard execution preflight / evidence gate.

Consumes sealed M47 upstream artifacts only (no recursive M46/M45 adjudication).
"""

from __future__ import annotations

from typing import Final

CONTRACT_ID_M48_PREFLIGHT: Final[str] = "starlab.v15.bounded_scorecard_execution_preflight.v1"
PROFILE_M48_EVIDENCE_GATE: Final[str] = (
    "starlab.v15.m48.bounded_scorecard_execution_preflight_evidence_requirements_gate.v1"
)

EVIDENCE_MANIFEST_CONTRACT_ID: Final[str] = (
    "starlab.v15.bounded_scorecard_execution_evidence_manifest.v1"
)

MILESTONE_LABEL_M48: Final[str] = "V15-M48"
EMITTER_MODULE_M48: Final[str] = "starlab.v15.emit_v15_m48_bounded_scorecard_execution_preflight"

FILENAME_MAIN_JSON: Final[str] = "v15_bounded_scorecard_execution_preflight.json"
REPORT_FILENAME: Final[str] = "v15_bounded_scorecard_execution_preflight_report.json"
BRIEF_FILENAME: Final[str] = "v15_bounded_scorecard_execution_preflight_brief.md"

SCHEMA_VERSION: Final[str] = "1.0"
DIGEST_FIELD: Final[str] = "artifact_sha256"

PROFILE_FIXTURE_CI: Final[str] = "fixture_ci"
PROFILE_OPERATOR_PREFLIGHT: Final[str] = "operator_preflight"
PROFILE_OPERATOR_DECLARED: Final[str] = "operator_declared"

STATUS_PREFLIGHT_READY: Final[str] = "bounded_scorecard_execution_preflight_ready"
STATUS_PREFLIGHT_READY_WARNINGS: Final[str] = (
    "bounded_scorecard_execution_preflight_ready_with_warnings"
)
STATUS_PREFLIGHT_REFUSED: Final[str] = "bounded_scorecard_execution_preflight_refused"

GATE_SATISFIED: Final[str] = "evidence_requirements_satisfied_for_future_preflight"
GATE_INCOMPLETE: Final[str] = "evidence_requirements_incomplete"
GATE_INVALID: Final[str] = "evidence_requirements_invalid"

CLAIM_SCORECARD_REFUSED: Final[str] = "scorecard_results_refused_not_executed"
CLAIM_BENCHMARK_REFUSED: Final[str] = "benchmark_pass_fail_refused_not_executed"
CLAIM_TOTAL_REFUSED: Final[str] = "scorecard_total_refused_not_computed"
CLAIM_STRENGTH_REFUSED: Final[str] = "strength_claim_refused_not_evaluated"
CLAIM_PROMOTION_REFUSED: Final[str] = "promotion_refused_no_scorecard_execution"

ROUTE_STATUS_RECOMMENDED_NOT_EXECUTED: Final[str] = "recommended_not_executed"
ROUTE_TO_SCORECARD_EXEC_SURFACE: Final[str] = "route_to_bounded_scorecard_execution_surface"
ROUTE_TO_M47_REMEDIATION: Final[str] = "route_to_m47_remediation_or_reemit"
ROUTE_TO_EVIDENCE_GAP: Final[str] = "route_to_evidence_gap_remediation"

REFUSED_MISSING_M47: Final[str] = "refused_missing_m47_surface_design"
REFUSED_INVALID_M47: Final[str] = "refused_invalid_m47_surface_design"
REFUSED_M47_NOT_READY: Final[str] = "refused_m47_design_not_ready"
REFUSED_M47_HONESTY: Final[str] = "refused_m47_honesty_flags_violation"
REFUSED_M47_ROUTE_EXECUTED: Final[str] = "refused_m47_route_executed"
REFUSED_M47_FUTURE_SURFACE_ALLOWED: Final[str] = "refused_m47_future_surface_allowed"
REFUSED_M47_FUTURE_SURFACE_NOT_SEPARATE: Final[str] = "refused_m47_future_surface_not_separate"
REFUSED_M47_SCORECARD_PRESENT: Final[str] = "refused_m47_scorecard_results_present"
REFUSED_REQUIRED_EVIDENCE_MISSING: Final[str] = "refused_required_evidence_missing"
REFUSED_REQUIRED_EVIDENCE_INVALID: Final[str] = "refused_required_evidence_invalid"
REFUSED_SCORECARD_RESULTS_CLAIM: Final[str] = "refused_scorecard_results_claim"
REFUSED_BENCHMARK_PASS_CLAIM: Final[str] = "refused_benchmark_pass_claim"
REFUSED_SCORECARD_TOTAL_CLAIM: Final[str] = "refused_scorecard_total_claim"
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
REFUSED_DECLARED_SHAPE: Final[str] = "refused_invalid_declared_preflight_shape"

FORBIDDEN_FLAG_EXECUTE_SCORECARD: Final[str] = "--execute-scorecard"
FORBIDDEN_FLAG_CLAIM_SCORECARD: Final[str] = "--claim-scorecard-results"
FORBIDDEN_FLAG_CLAIM_BENCHMARK_PASS: Final[str] = "--claim-benchmark-pass"
FORBIDDEN_FLAG_COMPUTE_SCORECARD_TOTAL: Final[str] = "--compute-scorecard-total"
FORBIDDEN_FLAG_COMPUTE_WIN_RATE: Final[str] = "--compute-win-rate"
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
    FORBIDDEN_FLAG_EXECUTE_SCORECARD,
    FORBIDDEN_FLAG_CLAIM_SCORECARD,
    FORBIDDEN_FLAG_CLAIM_BENCHMARK_PASS,
    FORBIDDEN_FLAG_COMPUTE_SCORECARD_TOTAL,
    FORBIDDEN_FLAG_COMPUTE_WIN_RATE,
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
    FORBIDDEN_FLAG_EXECUTE_SCORECARD: REFUSED_SCORECARD_RESULTS_CLAIM,
    FORBIDDEN_FLAG_CLAIM_SCORECARD: REFUSED_SCORECARD_RESULTS_CLAIM,
    FORBIDDEN_FLAG_CLAIM_BENCHMARK_PASS: REFUSED_BENCHMARK_PASS_CLAIM,
    FORBIDDEN_FLAG_COMPUTE_SCORECARD_TOTAL: REFUSED_SCORECARD_TOTAL_CLAIM,
    FORBIDDEN_FLAG_COMPUTE_WIN_RATE: REFUSED_SCORECARD_RESULTS_CLAIM,
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

# Mirrors sealed M47 honesty keys used for upstream snapshot / declared validation.
M47_BODY_BOOL_KEYS: Final[tuple[str, ...]] = (
    "benchmark_passed",
    "benchmark_pass_fail_emitted",
    "scorecard_results_produced",
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

M48_ALWAYS_FALSE_KEYS: Final[tuple[str, ...]] = (
    "scorecard_execution_performed",
    "scorecard_results_produced",
    "benchmark_passed",
    "benchmark_pass_fail_emitted",
    "scorecard_total_computed",
    "win_rate_computed",
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

NON_CLAIMS_M48: Final[tuple[str, ...]] = (
    "not_scorecard_execution_in_m48",
    "not_scorecard_results",
    "not_benchmark_pass_fail_evidence",
    "not_scorecard_total",
    "not_win_rate_computation",
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
    "preflight_evidence_gate_only_not_execution",
)

REQ_E0: Final[str] = "E0_artifact_integrity"
REQ_E1: Final[str] = "E1_candidate_identity"
REQ_E2: Final[str] = "E2_benchmark_protocol_binding"
REQ_E3: Final[str] = "E3_execution_receipt_binding"
REQ_E4: Final[str] = "E4_match_or_episode_evidence_bindings"
REQ_E5: Final[str] = "E5_scorecard_metric_schema"
REQ_E6: Final[str] = "E6_threshold_policy"
REQ_E7: Final[str] = "E7_public_private_boundary"
REQ_E8: Final[str] = "E8_failure_mode_schema"
REQ_E9: Final[str] = "E9_non_claims"

STATUS_REQUIRED_PRESENT: Final[str] = "required_present"
STATUS_REQUIRED_MISSING: Final[str] = "required_missing"
STATUS_REQUIRED_INVALID: Final[str] = "required_invalid"

SEMANTIC_SCOPE_REQ: Final[str] = "preflight_requirement_only_not_result_value"

EVIDENCE_MODE_FIXTURE: Final[str] = "fixture_structural_only_not_scorecard_execution"
EVIDENCE_MODE_OPERATOR_MANIFEST: Final[str] = (
    "operator_manifest_metadata_only_not_scorecard_execution"
)

INTERPRETATION_M47_BINDING: Final[str] = "scorecard_surface_design_only_not_scorecard_results"

FORBIDDEN_MANIFEST_KEYS: Final[frozenset[str]] = frozenset(
    {
        "scorecard_total",
        "win_rate",
        "benchmark_passed",
        "scorecard_results",
        "metric_results",
        "threshold_pass_fail",
        "strength_rating",
        "promotion_decision",
    }
)

ALLOWED_CLAIM_DECISION_VALUES: Final[frozenset[str]] = frozenset(
    {
        CLAIM_SCORECARD_REFUSED,
        CLAIM_BENCHMARK_REFUSED,
        CLAIM_TOTAL_REFUSED,
        CLAIM_STRENGTH_REFUSED,
        CLAIM_PROMOTION_REFUSED,
    }
)

FIXTURE_MANIFEST_SHA_PLACEHOLDER: Final[str] = (
    "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
)
