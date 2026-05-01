"""V15-M50 — scorecard readout / benchmark pass-fail refusal (consumes sealed M49)."""

from __future__ import annotations

from typing import Final

from starlab.v15.m49_bounded_scorecard_result_execution_models import (
    CONTRACT_ID_M49_RESULT,
    FORBIDDEN_CLI_FLAGS,
    PROFILE_M49_SURFACE,
)

CONTRACT_ID_M50_READOUT: Final[str] = "starlab.v15.scorecard_result_readout_decision.v1"
PROFILE_M50_SURFACE: Final[str] = (
    "starlab.v15.m50.scorecard_result_readout_benchmark_pass_fail_refusal.v1"
)

MILESTONE_LABEL_M50: Final[str] = "V15-M50"
EMITTER_MODULE_M50: Final[str] = "starlab.v15.emit_v15_m50_scorecard_result_readout_decision"

FILENAME_MAIN_JSON: Final[str] = "v15_scorecard_result_readout_decision.json"
REPORT_FILENAME: Final[str] = "v15_scorecard_result_readout_decision_report.json"
BRIEF_FILENAME: Final[str] = "v15_scorecard_result_readout_decision_brief.md"

SCHEMA_VERSION: Final[str] = "1.0"
DIGEST_FIELD: Final[str] = "artifact_sha256"

PROFILE_FIXTURE_CI: Final[str] = "fixture_ci"
PROFILE_OPERATOR_PREFLIGHT: Final[str] = "operator_preflight"
PROFILE_OPERATOR_DECLARED: Final[str] = "operator_declared"

STATUS_READOUT_COMPLETED: Final[str] = "scorecard_result_readout_completed"
STATUS_READOUT_COMPLETED_WARNINGS: Final[str] = "scorecard_result_readout_completed_with_warnings"
STATUS_READOUT_REFUSED: Final[str] = "scorecard_result_readout_refused"

M49_STATUS_COMPLETED: Final[str] = "bounded_scorecard_result_execution_completed"
M49_STATUS_COMPLETED_WARNINGS: Final[str] = (
    "bounded_scorecard_result_execution_completed_with_warnings"
)
M49_STATUS_REFUSED: Final[str] = "bounded_scorecard_result_execution_refused"

BENCHMARK_PASS_FAIL_REFUSED_PENDING_AUTHORITY: Final[str] = (
    "benchmark_pass_fail_refused_pending_authoritative_threshold"
)
BENCHMARK_PASS_FAIL_REFUSED_M49_BOUNDED_ONLY: Final[str] = (
    "benchmark_pass_fail_refused_m49_bounded_only"
)
BENCHMARK_PASS_FAIL_REFUSED_MISSING_SCORECARD: Final[str] = (
    "benchmark_pass_fail_refused_missing_scorecard_results"
)

PROMOTION_REFUSED_PENDING_PASS_FAIL: Final[str] = "promotion_refused_pending_benchmark_pass_fail"
PROMOTION_REFUSED_M50_READOUT_ONLY: Final[str] = "promotion_refused_m50_readout_only"

ROUTE_TO_M51_WATCHABILITY: Final[str] = "route_to_live_candidate_watchability_harness"
ROUTE_M49_REMEDIATION: Final[str] = "route_to_m49_remediation_or_reemit"
ROUTE_STATUS_RECOMMENDED_NOT_EXECUTED: Final[str] = "recommended_not_executed"

INTERPRETATION_M49_BINDING: Final[str] = (
    "bounded_scorecard_result_execution_artifact_only_not_benchmark_authority"
)

REFUSED_MISSING_M49: Final[str] = "refused_missing_m49_scorecard_result_execution_json"
REFUSED_M49_CONTRACT_INVALID: Final[str] = "refused_m49_contract_invalid"
REFUSED_M49_SHA_MISMATCH: Final[str] = "refused_m49_sha_mismatch"
REFUSED_M49_RESULT_REFUSED: Final[str] = "refused_m49_result_refused"
REFUSED_M49_RESULT_NOT_READY: Final[str] = "refused_m49_result_not_ready"
REFUSED_MISSING_SCORECARD_FIELDS: Final[str] = "refused_missing_scorecard_result_fields"
REFUSED_BENCHMARK_PASS_CLAIM: Final[str] = "refused_benchmark_pass_claim"
REFUSED_STRENGTH_CLAIM: Final[str] = "refused_strength_claim"
REFUSED_PROMOTION_CLAIM: Final[str] = "refused_promotion_claim"
REFUSED_CHECKPOINT_LOAD: Final[str] = "refused_checkpoint_load_request"
REFUSED_LIVE_SC2: Final[str] = "refused_live_sc2_request"
REFUSED_XAI_CLAIM: Final[str] = "refused_xai_claim"
REFUSED_HUMAN_PANEL_CLAIM: Final[str] = "refused_human_panel_claim"
REFUSED_SHOWCASE_CLAIM: Final[str] = "refused_showcase_release_claim"
REFUSED_V2_CLAIM: Final[str] = "refused_v2_authorization_claim"
REFUSED_T2_T5_CLAIM: Final[str] = "refused_t2_t5_execution_claim"
REFUSED_DECLARED_SHAPE: Final[str] = "refused_invalid_declared_m50_shape"
REFUSED_UPSTREAM_HONESTY: Final[str] = "refused_m49_upstream_overclaim_or_honesty_violation"

FORBIDDEN_FLAG_TO_REFUSAL: Final[dict[str, str]] = {
    "--claim-benchmark-pass": REFUSED_BENCHMARK_PASS_CLAIM,
    "--claim-strength": REFUSED_STRENGTH_CLAIM,
    "--promote-checkpoint": REFUSED_PROMOTION_CLAIM,
    "--load-checkpoint": REFUSED_CHECKPOINT_LOAD,
    "--run-live-sc2": REFUSED_LIVE_SC2,
    "--run-xai": REFUSED_XAI_CLAIM,
    "--run-human-panel": REFUSED_HUMAN_PANEL_CLAIM,
    "--release-showcase": REFUSED_SHOWCASE_CLAIM,
    "--authorize-v2": REFUSED_V2_CLAIM,
    "--execute-t2": REFUSED_T2_T5_CLAIM,
    "--execute-t3": REFUSED_T2_T5_CLAIM,
    "--execute-t4": REFUSED_T2_T5_CLAIM,
    "--execute-t5": REFUSED_T2_T5_CLAIM,
}

NON_CLAIMS_M50: Final[tuple[str, ...]] = (
    "scorecard_readout_bounded_fields_only_not_benchmark_pass_fail",
    "not_benchmark_execution",
    "not_benchmark_pass_fail_authority",
    "not_strength_evaluation",
    "not_checkpoint_promotion_or_rejection_as_strength",
    "not_torch_load",
    "not_checkpoint_blob_loaded",
    "not_live_sc2_execution",
    "not_xai_execution",
    "not_human_panel_benchmark_evidence",
    "not_showcase_release",
    "not_v2_authorization",
    "not_t2_t3_t4_t5_execution",
    "route_recommendation_advisory_only_recommended_not_executed",
)

M50_HONESTY_FALSE_KEYS: Final[tuple[str, ...]] = (
    "benchmark_passed",
    "benchmark_failed",
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

M50_DECLARED_OVERCLAIM_KEYS: Final[tuple[str, ...]] = M50_HONESTY_FALSE_KEYS

ALLOWED_BENCHMARK_DECISIONS: Final[frozenset[str]] = frozenset(
    {
        BENCHMARK_PASS_FAIL_REFUSED_PENDING_AUTHORITY,
        BENCHMARK_PASS_FAIL_REFUSED_M49_BOUNDED_ONLY,
        BENCHMARK_PASS_FAIL_REFUSED_MISSING_SCORECARD,
    }
)

ALLOWED_PROMOTION_DECISIONS: Final[frozenset[str]] = frozenset(
    {
        PROMOTION_REFUSED_PENDING_PASS_FAIL,
        PROMOTION_REFUSED_M50_READOUT_ONLY,
    }
)

# Re-export for CLI
M49_CONTRACT_FOR_BINDING: Final[str] = CONTRACT_ID_M49_RESULT
M49_PROFILE_FOR_BINDING: Final[str] = PROFILE_M49_SURFACE
FORBIDDEN_CLI_FLAGS_M50: Final[tuple[str, ...]] = FORBIDDEN_CLI_FLAGS
