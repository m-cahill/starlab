"""V15-M43 — bounded evaluation gate constants (upstream: V15-M42 package)."""

from __future__ import annotations

from typing import Final

CONTRACT_ID_BOUNDED_EVAL_GATE: Final[str] = "starlab.v15.bounded_evaluation_gate.v1"

PROFILE_GATE: Final[str] = "starlab.v15.m43.bounded_evaluation_gate.v1"

MILESTONE_LABEL_M43: Final[str] = "V15-M43"

EMITTER_MODULE_M43: Final[str] = "starlab.v15.emit_v15_m43_bounded_evaluation_gate"

FILENAME_MAIN_JSON: Final[str] = "v15_bounded_evaluation_gate.json"
REPORT_FILENAME: Final[str] = "v15_bounded_evaluation_gate_report.json"

SCHEMA_VERSION: Final[str] = "1.0"
GATE_ARTIFACT_DIGEST_FIELD: Final[str] = "artifact_sha256"

PROFILE_FIXTURE_CI: Final[str] = "fixture_ci"
PROFILE_OPERATOR_PREFLIGHT: Final[str] = "operator_preflight"
PROFILE_OPERATOR_DECLARED: Final[str] = "operator_declared"

STATUS_GATE_READY: Final[str] = "bounded_evaluation_gate_ready"
STATUS_GATE_READY_WITH_WARNINGS: Final[str] = "bounded_evaluation_gate_ready_with_warnings"
STATUS_GATE_NOT_READY: Final[str] = "bounded_evaluation_gate_not_ready"

ROUTE_ID_FUTURE_BOUNDED: Final[str] = "starlab.v15.m43.route.future_bounded_candidate_eval_v1"
ROUTE_STATUS_DECLARED_NOT_EXECUTED: Final[str] = "declared_not_executed"

REFUSED_MISSING_M42_PACKAGE: Final[str] = "refused_missing_m42_package"
REFUSED_INVALID_M42_PACKAGE: Final[str] = "refused_invalid_m42_package"
REFUSED_M42_PACKAGE_NOT_READY: Final[str] = "refused_m42_package_not_ready"
REFUSED_CANDIDATE_NOT_CANDIDATE_ONLY: Final[str] = "refused_candidate_not_candidate_only"
REFUSED_CHECKPOINT_IDENTITY_MISSING: Final[str] = "refused_checkpoint_identity_missing"
REFUSED_BENCHMARK_PROTOCOL_MISSING: Final[str] = "refused_benchmark_protocol_missing"
REFUSED_BENCHMARK_PROTOCOL_NOT_ALLOWED: Final[str] = "refused_benchmark_protocol_not_allowed"
REFUSED_ENVIRONMENT_PREREQUISITE_MISSING: Final[str] = "refused_environment_prerequisite_missing"
REFUSED_ARTIFACT_PREREQUISITE_MISSING: Final[str] = "refused_artifact_prerequisite_missing"
REFUSED_DISALLOWED_EXECUTION_REQUEST: Final[str] = "refused_disallowed_execution_request"
REFUSED_ROUTE_OUT_OF_SCOPE: Final[str] = "refused_route_out_of_scope"

FORBIDDEN_CLI_FLAGS: Final[tuple[str, ...]] = (
    "--run-benchmark",
    "--execute-evaluation",
    "--load-checkpoint",
    "--promote-checkpoint",
)

NON_CLAIMS_M43: Final[tuple[str, ...]] = (
    "not_benchmark_execution",
    "not_benchmark_pass_fail",
    "not_strength_evaluation",
    "not_checkpoint_promotion",
    "not_scorecard_results",
    "not_torch_load",
    "not_checkpoint_blob_load",
    "not_live_sc2",
    "not_xai",
    "not_human_panel",
    "not_showcase",
    "not_v2_authorization",
    "not_t2_t3_t4_t5_execution",
)


M42_FILENAME_MAIN_CANONICAL: Final[str] = (
    "v15_m42_two_hour_candidate_checkpoint_evaluation_package.json"
)
