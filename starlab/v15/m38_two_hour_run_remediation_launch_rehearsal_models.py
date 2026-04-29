"""V15-M38 two-hour run remediation & launch rehearsal — constants."""

from __future__ import annotations

from typing import Final

CONTRACT_ID_M38: Final[str] = "starlab.v15.two_hour_run_remediation_launch_rehearsal.v1"
PROFILE_M38: Final[str] = "starlab.v15.m38.two_hour_run_remediation_launch_rehearsal.v1"

MILESTONE_LABEL_M38: Final[str] = "V15-M38"

EMITTER_MODULE_M38: Final[str] = (
    "starlab.v15.emit_v15_m38_two_hour_run_remediation_launch_rehearsal"
)

FILENAME_MAIN_JSON: Final[str] = "v15_two_hour_run_remediation_launch_rehearsal.json"
REPORT_FILENAME: Final[str] = "v15_two_hour_run_remediation_launch_rehearsal_report.json"
CHECKLIST_FILENAME: Final[str] = "v15_two_hour_run_remediation_launch_rehearsal_checklist.md"
RUNBOOK_FILENAME: Final[str] = "v15_m39_launch_runbook.md"
LAUNCH_COMMAND_FILENAME: Final[str] = "v15_m39_launch_command.txt"
STOP_RESUME_CARD_FILENAME: Final[str] = "v15_m39_operator_stop_resume_card.md"

SCHEMA_VERSION: Final[str] = "1.0"
GATE_ARTIFACT_DIGEST_FIELD: Final[str] = "artifact_sha256"

PROFILE_FIXTURE_CI: Final[str] = "fixture_ci"
PROFILE_OPERATOR_PREFLIGHT: Final[str] = "operator_preflight"
PROFILE_OPERATOR_REHEARSAL: Final[str] = "operator_local_rehearsal"

STATUS_FIXTURE_SCHEMA_ONLY: Final[str] = "fixture_schema_only_no_operator_rehearsal"
STATUS_BLOCKED_NO_M37: Final[str] = "launch_rehearsal_blocked_missing_m37_audit"
STATUS_BLOCKED_CRITICAL: Final[str] = "launch_rehearsal_blocked_open_critical_blockers"
STATUS_BLOCKED_CHECKPOINT: Final[str] = "launch_rehearsal_blocked_checkpoint_cadence_unresolved"
STATUS_BLOCKED_RUNNER: Final[str] = "launch_rehearsal_blocked_runner_7200s_incompatible"
STATUS_BLOCKED_STORAGE: Final[str] = "launch_rehearsal_blocked_storage_or_output_policy"
STATUS_COMPLETED_DEFERRED: Final[str] = "launch_rehearsal_completed_with_deferred_noncritical_items"
STATUS_READY_M39: Final[str] = "launch_rehearsal_completed_ready_for_m39"

OPTIONAL_NOT_SUPPLIED: Final[str] = "optional_not_supplied"
OPTIONAL_ENRICHED: Final[str] = "enriched_when_supplied"

M39_TARGET_WALL_CLOCK_SECONDS: Final[float] = 7200.0
M39_MAX_WALL_CLOCK_MINUTES: Final[float] = 120.0

RECOMMENDED_NEXT: Final[str] = "V15-M39_two_hour_sc2_backed_t1_operator_attempt"

NON_CLAIMS_M38: Final[tuple[str, ...]] = (
    "not_two_hour_run_executed",
    "not_t2_t3",
    "not_benchmark_pass",
    "not_strength_evaluation",
    "not_checkpoint_promotion",
    "not_scorecard_results",
    "not_xai",
    "not_human_panel",
    "not_showcase",
    "not_v2",
    "not_live_sc2_claim_unless_labeled_rehearsal_only",
)
