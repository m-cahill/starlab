"""V15-M37 two-hour run blocker discovery / operator readiness audit constants."""

from __future__ import annotations

from typing import Final

CONTRACT_ID_M37_DISCOVERY: Final[str] = "starlab.v15.two_hour_run_blocker_discovery.v1"
PROFILE_M37_OPERATOR_READINESS: Final[str] = (
    "starlab.v15.m37.two_hour_run_operator_readiness_audit.v1"
)

MILESTONE_LABEL_M37: Final[str] = "V15-M37"

EMITTER_MODULE_M37: Final[str] = "starlab.v15.emit_v15_m37_two_hour_run_blocker_discovery"

FILENAME_MAIN_JSON: Final[str] = "v15_two_hour_run_blocker_discovery.json"
REPORT_FILENAME: Final[str] = "v15_two_hour_run_blocker_discovery_report.json"
CHECKLIST_FILENAME: Final[str] = "v15_two_hour_run_blocker_discovery_checklist.md"
REMEDIATION_MAP_FILENAME: Final[str] = "v15_m38_remediation_map.md"
RUNBOOK_DRAFT_FILENAME: Final[str] = "v15_m39_candidate_runbook_draft.md"

SCHEMA_VERSION: Final[str] = "1.0"
GATE_ARTIFACT_DIGEST_FIELD: Final[str] = "artifact_sha256"

PROFILE_FIXTURE_CI: Final[str] = "fixture_ci"
PROFILE_OPERATOR_AUDIT: Final[str] = "operator_audit"

STATUS_FIXTURE_SCHEMA_ONLY: Final[str] = "fixture_schema_only_no_operator_audit"

STATUS_BLOCKED_MISSING_REQUIRED_INPUTS: Final[str] = (
    "operator_audit_blocked_missing_required_inputs"
)
STATUS_BLOCKED_ENVIRONMENT: Final[str] = "operator_audit_blocked_environment_not_ready"
STATUS_BLOCKED_LINEAGE: Final[str] = "operator_audit_blocked_candidate_lineage_inconsistent"
STATUS_BLOCKED_STORAGE: Final[str] = "operator_audit_blocked_storage_risk"
STATUS_BLOCKED_RUN_CONTROL: Final[str] = "operator_audit_blocked_run_control_risk"

STATUS_COMPLETED_MATERIAL_BLOCKERS: Final[str] = "operator_audit_completed_material_blockers_found"
STATUS_COMPLETED_NO_MATERIAL_BLOCKERS: Final[str] = "operator_audit_completed_no_material_blockers"
STATUS_COMPLETED_READY_M38: Final[str] = "operator_audit_completed_ready_for_m38_remediation"

DEFAULT_OPERATOR_OUTCOME_STATUS: Final[str] = STATUS_COMPLETED_READY_M38

RECOMMENDED_NEXT: Final[str] = "V15-M38_two_hour_run_remediation_and_launch_rehearsal"

# Public ledger / handoff fallbacks when M29 JSON fields are absent (see M37 plan).
PUBLIC_LEDGER_M29_OBSERVED_WALL_CLOCK_SECONDS: Final[float] = 1800.0
PUBLIC_LEDGER_M29_CHECKPOINT_COUNT: Final[int] = 49537
PUBLIC_LEDGER_M29_TRAINING_UPDATE_COUNT: Final[int] = 2476886

# Optional seal anchor — M27 rollout (M28/M29); cross-checked when M29 JSON lists it.
ANCHOR_UPSTREAM_M27_ARTIFACT_SHA256: Final[str] = (
    "f9c2ca5aca7a3b15df0567358c1f207f99e112cd8d816f5ac1a1c6ff04022227"
)

DEFAULT_TARGET_WALL_CLOCK_SECONDS: Final[float] = 7200.0
DEFAULT_MIN_FREE_DISK_GB: Final[float] = 100.0

EXPECTED_PUBLIC_CANDIDATE_SHA256: Final[str] = (
    "eac6fc1f37aa958279a80209822765ecfa6aa2525ed64a8bee88c0ac2be13d26"
)

NON_CLAIMS_M37: Final[tuple[str, ...]] = (
    "not_two_hour_run",
    "not_t2_t3",
    "not_benchmark_pass",
    "not_benchmark_execution_claim",
    "not_strength_evaluation",
    "not_checkpoint_promotion",
    "not_scorecard_results",
    "not_xai",
    "not_human_panel",
    "not_showcase",
    "not_v2",
    "not_live_sc2_benchmark_run",
)

STORAGE_RISK_CRITICAL: Final[str] = "critical_storage_risk_estimated_checkpoint_volume"
STORAGE_RISK_HIGH: Final[str] = "high_storage_risk_estimated_checkpoint_volume"
STORAGE_RISK_MEDIUM: Final[str] = "medium_storage_risk_checkpoint_cadence_review_recommended"

M36_BINDING_OPTIONAL_NOT_SUPPLIED: Final[str] = "optional_not_supplied"
M36_BINDING_ENRICHED: Final[str] = "enriched_when_supplied_valid"
