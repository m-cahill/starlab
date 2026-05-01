"""V15-M53 — twelve-hour operator run attempt constants."""

from __future__ import annotations

from typing import Final

CONTRACT_ID_M53: Final[str] = "starlab.v15.twelve_hour_operator_run_attempt.v1"
PROFILE_M53: Final[str] = "starlab.v15.m53.twelve_hour_operator_run_attempt.v1"

MILESTONE_LABEL_M53: Final[str] = "V15-M53"

EMITTER_MODULE_M53: Final[str] = "starlab.v15.emit_v15_m53_twelve_hour_operator_run_attempt"
RUNNER_MODULE_M53: Final[str] = "starlab.v15.run_v15_m53_twelve_hour_operator_run_attempt"

FILENAME_MAIN_JSON: Final[str] = "v15_twelve_hour_operator_run_attempt.json"
REPORT_FILENAME: Final[str] = "v15_twelve_hour_operator_run_attempt_report.json"
CHECKLIST_FILENAME: Final[str] = "v15_twelve_hour_operator_run_attempt_checklist.md"
TRANSCRIPT_FILENAME: Final[str] = "v15_m53_operator_transcript.txt"
TELEMETRY_SUMMARY_FILENAME: Final[str] = "v15_m53_telemetry_summary.json"
CHECKPOINT_INVENTORY_FILENAME: Final[str] = "v15_m53_checkpoint_inventory.json"

SCHEMA_VERSION: Final[str] = "1.0"
GATE_ARTIFACT_DIGEST_FIELD: Final[str] = "artifact_sha256"

PROFILE_FIXTURE_CI: Final[str] = "fixture_ci"
PROFILE_OPERATOR_PREFLIGHT: Final[str] = "operator_preflight"
PROFILE_OPERATOR_CANDIDATE_WATCH_SMOKE: Final[str] = "operator_candidate_watch_smoke"
PROFILE_OPERATOR_12H_RUN: Final[str] = "operator_local_12hour_run"

STATUS_FIXTURE_ONLY: Final[str] = "fixture_schema_only_no_operator_run"
STATUS_PREFLIGHT_READY: Final[str] = "operator_preflight_ready_for_12hour_attempt"

PHASE_A_COMPLETED: Final[str] = "candidate_watch_smoke_completed"
PHASE_A_COMPLETED_WARNINGS: Final[str] = "candidate_watch_smoke_completed_with_warnings"
PHASE_A_BLOCKED: Final[str] = "candidate_watch_smoke_blocked"
PHASE_A_FAILED: Final[str] = "candidate_watch_smoke_failed"
PHASE_A_NOT_PERFORMED: Final[str] = "candidate_watch_smoke_not_performed"
PHASE_A_SKIPPED_ACK: Final[str] = "candidate_watch_smoke_skipped_with_operator_acknowledgment"

STATUS_12H_COMPLETED_CKPT: Final[str] = (
    "twelve_hour_operator_run_completed_with_candidate_checkpoint"
)
STATUS_12H_COMPLETED_NO_CKPT: Final[str] = "twelve_hour_operator_run_completed_no_checkpoint"
STATUS_12H_COMPLETED_WARNINGS: Final[str] = "twelve_hour_operator_run_completed_with_warnings"
STATUS_12H_INTERRUPTED_RESUME: Final[str] = (
    "twelve_hour_operator_run_interrupted_with_resume_available"
)
STATUS_12H_INTERRUPTED_NO_RESUME: Final[str] = "twelve_hour_operator_run_interrupted_no_resume"
STATUS_12H_BLOCKED: Final[str] = "twelve_hour_operator_run_blocked"
STATUS_12H_FAILED: Final[str] = "twelve_hour_operator_run_failed"

GUARD_ALLOW_OPERATOR_LOCAL: Final[str] = "--allow-operator-local-execution"
GUARD_AUTHORIZE_12H: Final[str] = "--authorize-12-hour-operator-run"
GUARD_AUTHORIZE_SMOKE: Final[str] = "--authorize-candidate-watch-smoke"
ACK_SKIP_PHASE_A: Final[str] = "--acknowledge-skip-candidate-watch-smoke"

TARGET_WALL_CLOCK_SECONDS_DEFAULT: Final[int] = 43200

RUN_SCOPE: Final[str] = (
    "operator_local_43200_second_sc2_backed_t1_candidate_training_m53_governed_attempt"
)

NON_CLAIMS_M53: Final[tuple[str, ...]] = (
    "not_benchmark_pass_fail",
    "not_strength_evaluation",
    "not_checkpoint_promotion",
    "not_xai",
    "not_human_panel",
    "not_showcase_release",
    "not_v2_authorization",
    "not_t2_t3_t4_t5_execution",
    "training_execution_evidence_only",
)

RECOMMENDED_NEXT_SUCCESS: Final[str] = "V15-M54_12_hour_run_package_evaluation_readiness"
RECOMMENDED_NEXT_REMEDIATION: Final[str] = "V15-M54_12_hour_run_remediation_gate"

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
)

M52B_FILENAME: Final[str] = "v15_twelve_hour_launch_rehearsal.json"
M52A_FILENAME: Final[str] = "v15_candidate_live_adapter_spike.json"

M52A_CONTRACT_ID: Final[str] = "starlab.v15.candidate_live_adapter_spike.v1"
