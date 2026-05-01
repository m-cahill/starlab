"""V15-M52B twelve-hour launch rehearsal models (no 12-hour execution)."""

from __future__ import annotations

from typing import Final

CONTRACT_ID_M52B: Final[str] = "starlab.v15.twelve_hour_blocker_discovery_launch_rehearsal.v1"

PROFILE_M52B_SURFACE: Final[str] = (
    "starlab.v15.m52.twelve_hour_blocker_discovery_launch_rehearsal.v1"
)

PROFILE_ID_FIXTURE_CI: Final[str] = "starlab.v15.m52b.profile.fixture_ci.v1"
PROFILE_ID_OPERATOR_PREFLIGHT: Final[str] = "starlab.v15.m52b.profile.operator_preflight.v1"
PROFILE_ID_OPERATOR_DECLARED: Final[str] = "starlab.v15.m52b.profile.operator_declared.v1"

MILESTONE_LABEL_M52B: Final[str] = "V15-M52B"
EMITTER_MODULE_M52B: Final[str] = "starlab.v15.emit_v15_m52_twelve_hour_launch_rehearsal"

FILENAME_MAIN_JSON: Final[str] = "v15_twelve_hour_launch_rehearsal.json"
REPORT_FILENAME: Final[str] = "v15_twelve_hour_launch_rehearsal_report.json"
CHECKLIST_FILENAME: Final[str] = "v15_twelve_hour_launch_rehearsal_checklist.md"
LAUNCH_CMD_FILENAME: Final[str] = "v15_m53_launch_command.txt"
RUNBOOK_FILENAME: Final[str] = "v15_m53_launch_runbook.md"
STOP_RESUME_FILENAME: Final[str] = "v15_m53_operator_stop_resume_card.md"

DIGEST_FIELD: Final[str] = "artifact_sha256"
SCHEMA_VERSION: Final[str] = "1.0"

PROFILE_FIXTURE_CI: Final[str] = "fixture_ci"
PROFILE_OPERATOR_PREFLIGHT: Final[str] = "operator_preflight"
PROFILE_OPERATOR_DECLARED: Final[str] = "operator_declared"

STATUS_FIXTURE_ONLY: Final[str] = "fixture_schema_only_no_12hour_rehearsal"
STATUS_READY: Final[str] = "twelve_hour_launch_rehearsal_ready"
STATUS_READY_WARNINGS: Final[str] = "twelve_hour_launch_rehearsal_ready_with_warnings"
STATUS_BLOCKED: Final[str] = "twelve_hour_launch_rehearsal_blocked"
STATUS_REFUSED: Final[str] = "twelve_hour_launch_rehearsal_refused"

DISK_FIXTURE_NOT_INSPECTED: Final[str] = "fixture_not_inspected"

ROUTE_STATUS_RECOMMENDED_NOT_EXECUTED: Final[str] = "recommended_not_executed"

BLOCKED_MISSING_M52A: Final[str] = "blocked_missing_m52a_adapter_spike"
BLOCKED_M52A_NOT_READY: Final[str] = "blocked_m52a_adapter_not_ready"
BLOCKED_CANDIDATE_NOT_WATCHABLE: Final[str] = "blocked_candidate_not_watchable"
BLOCKED_MISSING_CKPT: Final[str] = "blocked_missing_candidate_checkpoint"
BLOCKED_CKPT_SHA: Final[str] = "blocked_candidate_checkpoint_sha_mismatch"
BLOCKED_SC2: Final[str] = "blocked_missing_sc2_root"
BLOCKED_MAP: Final[str] = "blocked_missing_map"
BLOCKED_DISK_UNKNOWN: Final[str] = "blocked_disk_budget_unknown"
BLOCKED_DISK_INSUFFICIENT: Final[str] = "blocked_disk_budget_insufficient"
BLOCKED_RETENTION: Final[str] = "blocked_checkpoint_retention_unset"
BLOCKED_STOP_RESUME: Final[str] = "blocked_stop_resume_plan_missing"
BLOCKED_LAUNCH_CMD: Final[str] = "blocked_launch_command_not_frozen"
BLOCKED_OPERATOR_AUTH: Final[str] = "blocked_operator_authorization_missing"
BLOCKED_PUBLIC_PRIVATE: Final[str] = "blocked_public_private_boundary_risk"

REFUSED_FORBIDDEN: Final[str] = "refused_forbidden_execution_flag"
REFUSED_M52A_SHA: Final[str] = "refused_m52a_sha_mismatch"
REFUSED_CONTRACT: Final[str] = "refused_m52b_contract_invalid"

FORBIDDEN_FLAG_12H: Final[str] = "--execute-12-hour-run"
FORBIDDEN_FLAG_CLAIM_BENCHMARK: Final[str] = "--claim-benchmark-pass"
FORBIDDEN_FLAG_CLAIM_STRENGTH: Final[str] = "--claim-strength"
FORBIDDEN_FLAG_PROMOTE: Final[str] = "--promote-checkpoint"
FORBIDDEN_FLAG_RUN_BENCHMARK: Final[str] = "--run-benchmark"
FORBIDDEN_FLAG_HUMAN_PANEL: Final[str] = "--run-human-panel"
FORBIDDEN_FLAG_XAI: Final[str] = "--run-xai"
FORBIDDEN_FLAG_SHOWCASE: Final[str] = "--release-showcase"
FORBIDDEN_FLAG_V2: Final[str] = "--authorize-v2"
FORBIDDEN_FLAG_T2: Final[str] = "--execute-t2"
FORBIDDEN_FLAG_T3: Final[str] = "--execute-t3"
FORBIDDEN_FLAG_T4: Final[str] = "--execute-t4"
FORBIDDEN_FLAG_T5: Final[str] = "--execute-t5"

FORBIDDEN_CLI_FLAGS: Final[tuple[str, ...]] = (
    FORBIDDEN_FLAG_CLAIM_BENCHMARK,
    FORBIDDEN_FLAG_CLAIM_STRENGTH,
    FORBIDDEN_FLAG_PROMOTE,
    FORBIDDEN_FLAG_RUN_BENCHMARK,
    FORBIDDEN_FLAG_HUMAN_PANEL,
    FORBIDDEN_FLAG_XAI,
    FORBIDDEN_FLAG_SHOWCASE,
    FORBIDDEN_FLAG_V2,
    FORBIDDEN_FLAG_T2,
    FORBIDDEN_FLAG_T3,
    FORBIDDEN_FLAG_T4,
    FORBIDDEN_FLAG_T5,
    FORBIDDEN_FLAG_12H,
)

DOMAIN_KEYS: Final[tuple[str, ...]] = (
    "environment",
    "sc2_runtime",
    "map_pool",
    "candidate_checkpoint",
    "candidate_live_adapter",
    "launch_command",
    "disk_budget",
    "checkpoint_retention",
    "telemetry_capture",
    "stop_resume",
    "operator_authorization",
    "public_private_boundary",
)

NON_CLAIMS_M52B: Final[tuple[str, ...]] = (
    "not_twelve_hour_execution",
    "not_benchmark",
    "not_strength",
    "not_promotion",
    "not_xai",
    "not_human_panel",
    "not_showcase",
    "not_v2",
    "not_t2_t5",
    "not_candidate_skill_claim",
    "rehearsal_freezes_m53_command_only",
)

CONTRACT_ID_M52A_UPSTREAM: Final[str] = "starlab.v15.candidate_live_adapter_spike.v1"
