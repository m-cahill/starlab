"""V15-M36 smoke benchmark execution/refusal constants."""

from __future__ import annotations

from typing import Final

CONTRACT_ID_M36_EXECUTION: Final[str] = "starlab.v15.smoke_benchmark_execution.v1"
PROFILE_M36_SURFACE: Final[str] = "starlab.v15.m36.smoke_benchmark_execution_surface.v1"

MILESTONE_LABEL_M36: Final[str] = "V15-M36"

EMITTER_MODULE_M36: Final[str] = "starlab.v15.emit_v15_m36_smoke_benchmark_execution"

FILENAME_MAIN_JSON: Final[str] = "v15_smoke_benchmark_execution.json"
REPORT_FILENAME: Final[str] = "v15_smoke_benchmark_execution_report.json"
CHECKLIST_FILENAME: Final[str] = "v15_smoke_benchmark_execution_checklist.md"

SCHEMA_VERSION: Final[str] = "1.0"
GATE_ARTIFACT_DIGEST_FIELD: Final[str] = "artifact_sha256"

EXECUTION_SCOPE: Final[str] = "tiny_smoke_execution_surface_only"

PROFILE_FIXTURE_CI: Final[str] = "fixture_ci"
PROFILE_OPERATOR_PREFLIGHT: Final[str] = "operator_preflight"
PROFILE_OPERATOR_BOUNDED_SMOKE: Final[str] = "operator_local_bounded_smoke"

STATUS_FIXTURE_ONLY: Final[str] = "fixture_schema_only_no_candidate_execution"

STATUS_BLOCKED_MISSING_M35: Final[str] = "smoke_benchmark_execution_blocked_missing_m35_readiness"
STATUS_BLOCKED_INVALID_M35: Final[str] = "smoke_benchmark_execution_blocked_invalid_m35_readiness"
STATUS_BLOCKED_NOT_READY: Final[str] = "smoke_benchmark_execution_blocked_candidate_not_ready"
STATUS_BLOCKED_SHA_MISMATCH: Final[str] = "smoke_benchmark_execution_blocked_candidate_sha_mismatch"

STATUS_READY_BUT_NOT_RUN: Final[str] = "smoke_benchmark_execution_ready_but_not_run"
STATUS_COMPLETED_SYNTHETIC: Final[str] = "smoke_benchmark_execution_completed"

SMOKE_POLICY_PREFLIGHT_ONLY: Final[str] = "starlab.v15.m36.smoke_execution_none_preflight_only"
SMOKE_POLICY_SYNTHETIC_BOUNDED: Final[str] = (
    "starlab.v15.m36.synthetic_bounded_smoke_bookkeeping_only.v1"
)

RECOMMENDED_NEXT_SUCCESS: Final[str] = "V15-M37_bounded_operator_smoke_benchmark_attempt"

NON_CLAIMS_M36: Final[tuple[str, ...]] = (
    "not_benchmark_pass",
    "not_strength_evaluation",
    "not_checkpoint_promotion",
    "not_scorecard_result",
    "not_benchmark_execution_claim",
    "not_2_hour_run",
    "not_t2_t3",
    "not_xai",
    "not_human_panel",
    "not_showcase",
    "not_v2",
    "not_live_sc2_evaluation_outcome",
)
