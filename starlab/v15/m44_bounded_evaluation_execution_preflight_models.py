"""V15-M44 — bounded evaluation execution preflight (consumes sealed M43 gate JSON)."""

from __future__ import annotations

from typing import Final

CONTRACT_ID_M44_PREFLIGHT: Final[str] = "starlab.v15.bounded_evaluation_execution_preflight.v1"
PROFILE_M44_PREFLIGHT: Final[str] = "starlab.v15.m44.bounded_evaluation_execution_preflight.v1"

MILESTONE_LABEL_M44: Final[str] = "V15-M44"
EMITTER_MODULE_M44: Final[str] = "starlab.v15.emit_v15_m44_bounded_evaluation_execution_preflight"

FILENAME_MAIN_JSON: Final[str] = "v15_bounded_evaluation_execution_preflight.json"
REPORT_FILENAME: Final[str] = "v15_bounded_evaluation_execution_preflight_report.json"
CHECKLIST_FILENAME: Final[str] = "v15_bounded_evaluation_execution_preflight_checklist.md"

SCHEMA_VERSION: Final[str] = "1.0"
DIGEST_FIELD: Final[str] = "artifact_sha256"

PROFILE_FIXTURE_CI: Final[str] = "fixture_ci"
PROFILE_OPERATOR_PREFLIGHT: Final[str] = "operator_preflight"
PROFILE_OPERATOR_DECLARED: Final[str] = "operator_declared"

STATUS_PREFLIGHT_READY: Final[str] = "bounded_evaluation_execution_preflight_ready"
STATUS_PREFLIGHT_READY_WARNINGS: Final[str] = (
    "bounded_evaluation_execution_preflight_ready_with_warnings"
)
STATUS_PREFLIGHT_NOT_READY: Final[str] = "bounded_evaluation_execution_preflight_not_ready"

CONTRACT_ID_M43_GATE: Final[str] = "starlab.v15.bounded_evaluation_gate.v1"
PROFILE_M43_GATE: Final[str] = "starlab.v15.m43.bounded_evaluation_gate.v1"

M43_STATUS_READY: Final[str] = "bounded_evaluation_gate_ready"
M43_STATUS_READY_WARNINGS: Final[str] = "bounded_evaluation_gate_ready_with_warnings"

PLAN_STATUS_CONSTRUCTED: Final[str] = "constructed_not_executed"
PLAN_ID_EXPECTED: Final[str] = "starlab.v15.m44.plan.bounded_candidate_eval_preflight_v1"

REFUSED_MISSING_M43_GATE: Final[str] = "refused_missing_m43_gate"
REFUSED_INVALID_M43_GATE: Final[str] = "refused_invalid_m43_gate"
REFUSED_M43_GATE_NOT_READY: Final[str] = "refused_m43_gate_not_ready"
REFUSED_M43_HONESTY_VIOLATION: Final[str] = "refused_m43_honesty_flags_violation"
REFUSED_M43_ROUTE_NOT_DECLARED: Final[str] = "refused_m43_route_not_declared"
REFUSED_DRY_RUN_PLAN_MISSING: Final[str] = "refused_dry_run_plan_missing"
REFUSED_DRY_RUN_PLAN_INVALID: Final[str] = "refused_dry_run_plan_invalid"
REFUSED_ENV_MANIFEST_MISSING: Final[str] = "refused_environment_manifest_missing"
REFUSED_ENV_MANIFEST_INVALID: Final[str] = "refused_environment_manifest_invalid"
REFUSED_CANDIDATE_IDENTITY_MISSING: Final[str] = "refused_candidate_identity_missing"
REFUSED_SCORECARD_PROTOCOL_MISSING: Final[str] = "refused_scorecard_protocol_missing"
REFUSED_SCORECARD_PROTOCOL_INVALID: Final[str] = "refused_scorecard_protocol_invalid"
REFUSED_DISALLOWED_EXECUTION: Final[str] = "refused_disallowed_execution_request"
REFUSED_CHECKPOINT_LOAD: Final[str] = "refused_checkpoint_load_request"
REFUSED_LIVE_SC2: Final[str] = "refused_live_sc2_request"
REFUSED_ROUTE_OUT_OF_SCOPE: Final[str] = "refused_route_out_of_scope"


FORBIDDEN_FLAG_CHECKPOINT_LOAD: Final[str] = "--load-checkpoint"
FORBIDDEN_FLAG_LIVE_SC2: Final[str] = "--run-live-sc2"
FORBIDDEN_CLI_FLAGS_GENERAL: Final[tuple[str, ...]] = (
    "--run-benchmark",
    "--execute-evaluation",
    "--promote-checkpoint",
    "--produce-scorecard-results",
    "--run-xai",
    "--run-human-panel",
    "--release-showcase",
    "--authorize-v2",
)
FORBIDDEN_CLI_FLAGS: Final[tuple[str, ...]] = (
    FORBIDDEN_FLAG_CHECKPOINT_LOAD,
    FORBIDDEN_FLAG_LIVE_SC2,
) + FORBIDDEN_CLI_FLAGS_GENERAL


NON_CLAIMS_M44: Final[tuple[str, ...]] = (
    "not_benchmark_execution",
    "not_evaluation_execution_surface",
    "not_scorecard_results",
    "not_strength_evaluation",
    "not_checkpoint_load",
    "not_torch_load",
    "not_live_sc2",
    "not_checkpoint_promotion",
    "not_xai",
    "not_human_panel",
    "not_showcase",
    "not_v2_authorization",
    "not_t2_t3_t4_t5_ladder_execution",
)

INTERPRETATION_ROUTING_ONLY: Final[str] = "routing_eligibility_only"

NOT_INTERPRETED_AS_M43: Final[tuple[str, ...]] = (
    "benchmark_success",
    "evaluation_execution",
    "strength_evaluation",
    "checkpoint_promotion",
    "scorecard_results",
)
