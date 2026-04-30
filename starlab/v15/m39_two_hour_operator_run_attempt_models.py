"""V15-M39 — 2-hour operator run attempt constants."""

from __future__ import annotations

from typing import Final

CONTRACT_ID_M39: Final[str] = "starlab.v15.two_hour_operator_run_attempt.v1"
PROFILE_M39: Final[str] = "starlab.v15.m39.two_hour_operator_run_attempt.v1"

MILESTONE_LABEL_M39: Final[str] = "V15-M39"

EMITTER_MODULE_M39: Final[str] = "starlab.v15.emit_v15_m39_two_hour_operator_run_attempt"
RUNNER_MODULE_M39: Final[str] = "starlab.v15.run_v15_m39_two_hour_operator_run_attempt"

FILENAME_MAIN_JSON: Final[str] = "v15_two_hour_operator_run_attempt.json"
REPORT_FILENAME: Final[str] = "v15_two_hour_operator_run_attempt_report.json"
CHECKLIST_FILENAME: Final[str] = "v15_two_hour_operator_run_attempt_checklist.md"
TRANSCRIPT_FILENAME: Final[str] = "v15_m39_operator_transcript.txt"
TELEMETRY_SUMMARY_FILENAME: Final[str] = "v15_m39_telemetry_summary.json"
CHECKPOINT_INVENTORY_FILENAME: Final[str] = "v15_m39_checkpoint_inventory.json"

SCHEMA_VERSION: Final[str] = "1.0"
GATE_ARTIFACT_DIGEST_FIELD: Final[str] = "artifact_sha256"

PROFILE_FIXTURE_CI: Final[str] = "fixture_ci"
PROFILE_OPERATOR_PREFLIGHT: Final[str] = "operator_preflight"
PROFILE_OPERATOR_RUN: Final[str] = "operator_local_two_hour_run"

STATUS_FIXTURE_ONLY: Final[str] = "fixture_schema_only_no_operator_run"
STATUS_PREFLIGHT_READY: Final[str] = "operator_preflight_ready_for_2hour_attempt"
STATUS_PREFLIGHT_BLOCKED_NO_M38: Final[str] = "operator_preflight_blocked_missing_m38_rehearsal"
STATUS_PREFLIGHT_BLOCKED_M38_NOT_READY: Final[str] = "operator_preflight_blocked_m38_not_ready"
STATUS_PREFLIGHT_BLOCKED_NO_LAUNCH_CMD: Final[str] = (
    "operator_preflight_blocked_missing_launch_command"
)
STATUS_PREFLIGHT_BLOCKED_RETENTION: Final[str] = (
    "operator_preflight_blocked_checkpoint_retention_not_configured"
)
STATUS_PREFLIGHT_BLOCKED_CUDA: Final[str] = "operator_preflight_blocked_cuda_unavailable"
STATUS_PREFLIGHT_BLOCKED_SC2: Final[str] = "operator_preflight_blocked_sc2_surface_unavailable"
STATUS_PREFLIGHT_BLOCKED_DISK: Final[str] = "operator_preflight_blocked_disk_or_output_policy"
STATUS_PREFLIGHT_BLOCKED_ENV: Final[str] = "operator_preflight_blocked_environment"
STATUS_PREFLIGHT_BLOCKED_LINEAGE: Final[str] = (
    "operator_preflight_blocked_candidate_lineage_mismatch"
)

STATUS_RUN_STARTED: Final[str] = "two_hour_operator_run_started"
STATUS_RUN_COMPLETED_WITH_CKPT: Final[str] = (
    "two_hour_operator_run_completed_with_candidate_checkpoint"
)
STATUS_RUN_COMPLETED_NO_CKPT: Final[str] = (
    "two_hour_operator_run_completed_without_candidate_checkpoint"
)
STATUS_RUN_INTERRUPTED: Final[str] = "two_hour_operator_run_interrupted_partial_receipt"
STATUS_RUN_FAILED: Final[str] = "two_hour_operator_run_failed"
STATUS_RUN_BLOCKED_PREFLIGHT: Final[str] = "two_hour_operator_run_blocked_preflight"

RUN_SCOPE: Final[str] = "operator_local_7200_second_sc2_backed_t1_continuation_candidate_training"

TARGET_WALL_CLOCK_SECONDS: Final[float] = 7200.0

# Public ledger reference: sealed M29 artifact SHA (docs/starlab-v1.5.md).
PUBLIC_LEDGER_M29_ARTIFACT_SHA256: Final[str] = (
    "87d7d00b0fd19bb9f9d85180af9a0245957449ef0160575de146a71dd2ee4ea0"
)

RECOMMENDED_NEXT_SUCCESS: Final[str] = "V15-M40_two_hour_run_package_and_evaluation_readiness"
RECOMMENDED_NEXT_REMEDIATION: Final[str] = "V15-M40_two_hour_run_remediation_retry_gate"

NON_CLAIMS_M39: Final[tuple[str, ...]] = (
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

M39_OUTPUT_ROOT_TOKEN: Final[str] = "v15_m39_2hour_operator_run"
