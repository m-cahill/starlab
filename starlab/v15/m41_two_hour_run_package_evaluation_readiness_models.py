"""V15-M41 — two-hour run package & evaluation readiness constants."""

from __future__ import annotations

from typing import Final

CONTRACT_ID_M41: Final[str] = "starlab.v15.two_hour_run_package_evaluation_readiness.v1"
PROFILE_M41: Final[str] = "starlab.v15.m41.two_hour_run_package_evaluation_readiness.v1"

MILESTONE_LABEL_M41: Final[str] = "V15-M41"

EMITTER_MODULE_M41: Final[str] = (
    "starlab.v15.emit_v15_m41_two_hour_run_package_evaluation_readiness"
)

FILENAME_MAIN_JSON: Final[str] = "v15_two_hour_run_package_evaluation_readiness.json"
REPORT_FILENAME: Final[str] = "v15_two_hour_run_package_evaluation_readiness_report.json"
CHECKLIST_FILENAME: Final[str] = "v15_two_hour_run_package_evaluation_readiness_checklist.md"
PACKET_FILENAME: Final[str] = "v15_m41_evaluation_readiness_packet.md"
CANDIDATE_INDEX_FILENAME: Final[str] = "v15_m41_candidate_checkpoint_index.json"

SCHEMA_VERSION: Final[str] = "1.0"
GATE_ARTIFACT_DIGEST_FIELD: Final[str] = "artifact_sha256"

PROFILE_FIXTURE_CI: Final[str] = "fixture_ci"
PROFILE_OPERATOR_PREFLIGHT: Final[str] = "operator_preflight"

STATUS_FIXTURE_ONLY: Final[str] = "fixture_schema_only_no_operator_package"
STATUS_BLOCKED_MISSING_M39: Final[str] = "package_blocked_missing_m39_receipt"
STATUS_BLOCKED_INVALID_M39: Final[str] = "package_blocked_invalid_m39_receipt"
STATUS_BLOCKED_M39_NOT_COMPLETED: Final[str] = "package_blocked_m39_not_completed"
STATUS_BLOCKED_MISSING_INVENTORY: Final[str] = (
    "package_blocked_missing_candidate_checkpoint_inventory"
)
STATUS_BLOCKED_MISSING_TELEMETRY: Final[str] = "package_blocked_missing_telemetry_summary"
STATUS_BLOCKED_MISSING_TRANSCRIPT: Final[str] = "package_blocked_missing_transcript"
STATUS_BLOCKED_CANDIDATE_SHA_MISMATCH: Final[str] = "package_blocked_candidate_sha_mismatch"
STATUS_READY: Final[str] = "package_ready_for_future_evaluation"
STATUS_READY_WARNINGS: Final[str] = "package_ready_with_noncritical_warnings"

# Public ledger anchors (Phase B completion — docs / operator record)
ANCHOR_M39_RECEIPT_SHA256: Final[str] = (
    "675ae631ff2fa8a9f71f2c03a93f3abbffbfe0c45fcb49a59c933920330b010c"
)
ANCHOR_FINAL_CANDIDATE_SHA256: Final[str] = (
    "51cea94ed5324087863b246b7b31a21021eba286924aea4609aa09466430a943"
)
SOURCE_CANDIDATE_LINEAGE_SHA256: Final[str] = (
    "eac6fc1f37aa958279a80209822765ecfa6aa2525ed64a8bee88c0ac2be13d26"
)

RECOMMENDED_NEXT_SUCCESS: Final[str] = (
    "V15-M42_candidate_checkpoint_evaluation_package_from_two_hour_run"
)
RECOMMENDED_NEXT_REMEDIATION: Final[str] = "V15-M42_2Hour_Run_Package_Remediation"

NON_CLAIMS_M41: Final[tuple[str, ...]] = (
    "not_benchmark_pass",
    "not_strength_evaluation",
    "not_checkpoint_promotion",
    "not_scorecard_results",
    "not_t2_t3",
    "not_xai",
    "not_human_panel",
    "not_showcase",
    "not_v2",
)

M39_CLAIM_KEYS_MUST_REMAIN_FALSE: Final[tuple[str, ...]] = (
    "benchmark_passed",
    "scorecard_results_produced",
    "strength_evaluated",
    "checkpoint_promoted",
    "xai_execution_performed",
    "human_panel_execution_performed",
    "showcase_release_authorized",
    "v2_authorized",
    "t2_authorized",
    "t3_authorized",
)
