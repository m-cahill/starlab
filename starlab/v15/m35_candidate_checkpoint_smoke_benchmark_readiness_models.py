"""V15-M35 candidate checkpoint smoke benchmark readiness constants."""

from __future__ import annotations

from typing import Final

CONTRACT_ID_M35_READINESS: Final[str] = (
    "starlab.v15.candidate_checkpoint_smoke_benchmark_readiness.v1"
)
PROFILE_M35_READINESS: Final[str] = (
    "starlab.v15.m35.candidate_checkpoint_smoke_benchmark_readiness.v1"
)

MILESTONE_LABEL_M35: Final[str] = "V15-M35"

EMITTER_MODULE_M35: Final[str] = (
    "starlab.v15.emit_v15_m35_candidate_checkpoint_smoke_benchmark_readiness"
)

FILENAME_MAIN_JSON: Final[str] = "v15_candidate_checkpoint_smoke_benchmark_readiness.json"
REPORT_FILENAME: Final[str] = "v15_candidate_checkpoint_smoke_benchmark_readiness_report.json"
CHECKLIST_FILENAME: Final[str] = "v15_candidate_checkpoint_smoke_benchmark_readiness_checklist.md"

SCHEMA_VERSION: Final[str] = "1.0"
GATE_ARTIFACT_DIGEST_FIELD: Final[str] = "artifact_sha256"

READINESS_SCOPE: Final[str] = "ready_for_future_smoke_benchmark_execution_only"

STATUS_FIXTURE_ONLY: Final[str] = "fixture_schema_only_no_benchmark_execution"
STATUS_BLOCKED_MISSING_M33: Final[str] = "smoke_benchmark_readiness_blocked_missing_m33_probe"
STATUS_BLOCKED_INVALID_M33: Final[str] = "smoke_benchmark_readiness_blocked_invalid_m33_probe"
STATUS_BLOCKED_SHA_MISMATCH: Final[str] = "smoke_benchmark_readiness_blocked_candidate_sha_mismatch"
STATUS_BLOCKED_NOT_CUDA: Final[str] = "smoke_benchmark_readiness_blocked_probe_not_cuda"
STATUS_BLOCKED_M05: Final[str] = "smoke_benchmark_readiness_blocked_invalid_scorecard_protocol_json"
STATUS_READY: Final[str] = "smoke_benchmark_ready_for_future_execution"

PROFILE_FIXTURE_CI: Final[str] = "fixture_ci"
PROFILE_OPERATOR_PREFLIGHT: Final[str] = "operator_preflight"

RECOMMENDED_NEXT_SUCCESS: Final[str] = "V15-M36_smoke_benchmark_execution_surface"

NON_CLAIMS_M35: Final[tuple[str, ...]] = (
    "not_checkpoint_promotion",
    "not_benchmark_execution",
    "not_benchmark_pass",
    "not_strength_evaluation",
    "not_scorecard_execution",
    "not_72_hour_campaign",
    "not_live_sc2_evaluation_outcome",
    "not_xai_execution",
    "not_human_panel_execution",
    "not_showcase_release",
    "not_v2_authorization",
    "not_t2_t3_authorization",
)

EXPECTED_PUBLIC_CANDIDATE_SHA256: Final[str] = (
    "eac6fc1f37aa958279a80209822765ecfa6aa2525ed64a8bee88c0ac2be13d26"
)
