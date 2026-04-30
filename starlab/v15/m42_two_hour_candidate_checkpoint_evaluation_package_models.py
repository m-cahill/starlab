"""V15-M42 — two-hour-run candidate checkpoint evaluation package constants."""

from __future__ import annotations

from typing import Final

CONTRACT_ID_EVAL_PACKAGE_FAMILY: Final[str] = (
    "starlab.v15.candidate_checkpoint_evaluation_package.v1"
)
PROFILE_M42: Final[str] = "starlab.v15.m42.two_hour_run_candidate_checkpoint_evaluation_package.v1"

MILESTONE_LABEL_M42: Final[str] = "V15-M42"

EMITTER_MODULE_M42: Final[str] = (
    "starlab.v15.emit_v15_m42_two_hour_candidate_checkpoint_evaluation_package"
)

FILENAME_MAIN_JSON: Final[str] = "v15_m42_two_hour_candidate_checkpoint_evaluation_package.json"
REPORT_FILENAME: Final[str] = "v15_m42_two_hour_candidate_checkpoint_evaluation_package_report.json"
CHECKLIST_FILENAME: Final[str] = (
    "v15_m42_two_hour_candidate_checkpoint_evaluation_package_checklist.md"
)
ROUTING_PACKET_FILENAME: Final[str] = "v15_m42_candidate_evaluation_routing_packet.md"
BINDINGS_INDEX_FILENAME: Final[str] = "v15_m42_candidate_bindings_index.json"

SCHEMA_VERSION: Final[str] = "1.0"
GATE_ARTIFACT_DIGEST_FIELD: Final[str] = "artifact_sha256"

PROFILE_FIXTURE_CI: Final[str] = "fixture_ci"
PROFILE_OPERATOR_PREFLIGHT: Final[str] = "operator_preflight"

STATUS_FIXTURE_ONLY: Final[str] = "fixture_schema_only_no_operator_package"
STATUS_BLOCKED_MISSING_M41: Final[str] = "package_blocked_missing_m41_package"
STATUS_BLOCKED_INVALID_M41: Final[str] = "package_blocked_invalid_m41_package"
STATUS_BLOCKED_M41_NOT_READY: Final[str] = "package_blocked_m41_not_ready"
STATUS_BLOCKED_M39_RECEIPT_MISMATCH: Final[str] = "package_blocked_m39_receipt_mismatch"
STATUS_BLOCKED_SOURCE_MISMATCH: Final[str] = "package_blocked_source_candidate_mismatch"
STATUS_BLOCKED_FINAL_MISMATCH: Final[str] = "package_blocked_final_candidate_mismatch"
STATUS_BLOCKED_MISSING_FINAL_INDEX: Final[str] = "package_blocked_missing_final_candidate_index"
STATUS_READY: Final[str] = "package_ready_for_future_candidate_evaluation"
STATUS_READY_WARNINGS: Final[str] = "package_ready_with_noncritical_warnings"
STATUS_BLOCKED_INVALID_M05: Final[str] = (
    "package_blocked_invalid_m05_protocol"  # operator supplied invalid JSON / contract mismatch
)

EXPECTED_M41_SHA_OPTIONAL_NOT_SUPPLIED: Final[str] = "optional_not_supplied"
EXPECTED_M41_SHA_VERIFIED_MATCH: Final[str] = "verified_match"
EXPECTED_M41_SHA_CLI_MISMATCH: Final[str] = "cli_expected_mismatch"

ANCHOR_M39_RECEIPT_SHA256: Final[str] = (
    "675ae631ff2fa8a9f71f2c03a93f3abbffbfe0c45fcb49a59c933920330b010c"
)
ANCHOR_FINAL_CANDIDATE_SHA256: Final[str] = (
    "51cea94ed5324087863b246b7b31a21021eba286924aea4609aa09466430a943"
)
SOURCE_CANDIDATE_LINEAGE_SHA256: Final[str] = (
    "eac6fc1f37aa958279a80209822765ecfa6aa2525ed64a8bee88c0ac2be13d26"
)

RUN_STATUS_EXPECTED_M39: Final[str] = "two_hour_operator_run_completed_with_candidate_checkpoint"

RECOMMENDED_NEXT_SUCCESS: Final[str] = "V15-M43_bounded_evaluation_gate_for_two_hour_candidate"
RECOMMENDED_NEXT_REMEDIATION: Final[str] = "V15-M43_2Hour_Candidate_Evaluation_Package_Remediation"

NON_CLAIMS_M42: Final[tuple[str, ...]] = (
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

M41_READY_STATUSES: Final[frozenset[str]] = frozenset(
    {
        "package_ready_for_future_evaluation",
        "package_ready_with_noncritical_warnings",
    }
)
