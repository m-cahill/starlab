"""V15-M20 — real candidate checkpoint production gate (constants)."""

from __future__ import annotations

from typing import Final

CONTRACT_ID_REAL_CANDIDATE_CHECKPOINT_PRODUCTION_GATE: Final[str] = (
    "starlab.v15.real_candidate_checkpoint_production_gate.v1"
)
MILESTONE_ID_V15_M20: Final[str] = "V15-M20"
EMITTER_MODULE_REAL_CANDIDATE_GATE: Final[str] = (
    "starlab.v15.emit_v15_real_candidate_checkpoint_production_gate"
)

RUNNER_MODULE_T1_GATE: Final[str] = "starlab.v15.run_v15_t1_30min_candidate_checkpoint_gate"

SCHEMA_VERSION: Final[str] = "1.0"
REPORT_VERSION: Final[str] = "1"
SEAL_KEY_ARTIFACT: Final[str] = "artifact_sha256"

FILENAME_GATE_JSON: Final[str] = "v15_real_candidate_checkpoint_production_gate.json"
REPORT_FILENAME_GATE_JSON: Final[str] = "v15_real_candidate_checkpoint_production_gate_report.json"
FILENAME_RUNBOOK_MD: Final[str] = "v15_real_candidate_checkpoint_production_runbook.md"

RUN_TIER_T1_30_MIN: Final[str] = "T1_30_MIN"

PROFILE_FIXTURE_DEFAULT: Final[str] = "fixture_default"
PROFILE_OPERATOR_PREFLIGHT: Final[str] = "operator_preflight"

# Gate statuses (machine vocabulary)
STATUS_FIXTURE_NO_OPERATOR_RUN: Final[str] = "fixture_no_operator_run"
STATUS_OPERATOR_PREFLIGHT_BLOCKED: Final[str] = "operator_preflight_blocked"
STATUS_T1_NOT_STARTED: Final[str] = "t1_30min_run_not_started"
STATUS_T1_RUN_FAILED: Final[str] = "t1_30min_run_failed"
STATUS_T1_INSUFFICIENT_TRAINING_WORKLOAD: Final[str] = (
    "t1_30min_run_failed_insufficient_training_workload"
)
STATUS_T1_COMPLETED_NO_CHECKPOINT: Final[str] = "t1_30min_run_completed_no_checkpoint"
STATUS_T1_PACKAGE_BLOCKED: Final[str] = "t1_30min_checkpoint_produced_package_blocked"
STATUS_T1_PACKAGE_READY: Final[str] = "t1_30min_checkpoint_produced_package_ready"

NON_CLAIMS_V15_M20: Final[tuple[str, ...]] = (
    "not_strength_evaluation",
    "not_checkpoint_promotion",
    "not_benchmark_pass",
    "not_xai_execution",
    "not_human_benchmark_execution",
    "not_showcase_release",
    "not_v2_authorization",
    "not_2_hour_run",
    "not_12_hour_run",
)

DEFAULT_BLOCKED_REASON_MISSING_M16: Final[str] = (
    "missing_operator_local_m16_short_gpu_environment_evidence"
)
DEFAULT_BLOCKED_REASON_M16_NOT_PROBE_SUCCESS: Final[str] = (
    "m16_environment_evidence_not_operator_local"
)

T1_MIN_OPERATOR_TRAINING_WORKLOAD_SECONDS: Final[float] = 300.0

RECOMMENDED_NEXT_FORK_FIELD: Final[str] = "real_candidate_checkpoint_production_gate"

DEFAULT_CLAIM_FLAGS: Final[dict[str, bool]] = {
    "strength_evaluated": False,
    "checkpoint_promoted": False,
    "benchmark_passed": False,
    "xai_claim_authorized": False,
    "human_benchmark_claim_authorized": False,
    "showcase_release_authorized": False,
    "v2_authorized": False,
}

STRONGEST_ALLOWED_CLAIM_M20: Final[str] = (
    "STARLAB completed a bounded 30-minute operator-local GPU checkpoint-production run and "
    "produced a structurally governed candidate package for future evaluation."
)
