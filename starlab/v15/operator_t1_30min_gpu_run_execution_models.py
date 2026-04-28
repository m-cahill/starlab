"""V15-M21 — operator T1 30-minute GPU run execution / evidence capture (constants)."""

from __future__ import annotations

from typing import Final

CONTRACT_ID_OPERATOR_T1_30MIN_GPU_RUN_EXECUTION: Final[str] = (
    "starlab.v15.operator_t1_30min_gpu_run_execution.v1"
)
MILESTONE_ID_V15_M21: Final[str] = "V15-M21"
EMITTER_MODULE_OPERATOR_T1_EXECUTION: Final[str] = (
    "starlab.v15.emit_v15_operator_t1_30min_gpu_run_execution"
)
RUNNER_MODULE_M21_OPERATOR_T1: Final[str] = "starlab.v15.run_v15_m21_t1_30min_gpu_run_execution"

UPSTREAM_M20_CONTRACT_REFERENCE: Final[str] = (
    "starlab.v15.real_candidate_checkpoint_production_gate.v1"
)
RUNNER_MODULE_M20_T1_GATE: Final[str] = "starlab.v15.run_v15_t1_30min_candidate_checkpoint_gate"

SCHEMA_VERSION: Final[str] = "1.0"
REPORT_VERSION: Final[str] = "1"
SEAL_KEY_ARTIFACT: Final[str] = "artifact_sha256"

FILENAME_EXECUTION_JSON: Final[str] = "v15_operator_t1_30min_gpu_run_execution.json"
REPORT_FILENAME_EXECUTION_JSON: Final[str] = "v15_operator_t1_30min_gpu_run_execution_report.json"
FILENAME_RUNBOOK_MD: Final[str] = "v15_operator_t1_30min_gpu_run_execution_runbook.md"

RUN_TIER_T1_30_MIN: Final[str] = "T1_30_MIN"

PROFILE_FIXTURE_DEFAULT: Final[str] = "fixture_default"
PROFILE_OPERATOR_PREFLIGHT: Final[str] = "operator_preflight"

# Execution statuses (aligned with V15-M21 vocabulary)
STATUS_OPERATOR_PREFLIGHT_BLOCKED: Final[str] = "operator_preflight_blocked"
STATUS_T1_NOT_STARTED: Final[str] = "t1_30min_run_not_started"
STATUS_T1_RUN_FAILED: Final[str] = "t1_30min_run_failed"
STATUS_T1_COMPLETED_NO_CHECKPOINT: Final[str] = "t1_30min_run_completed_no_checkpoint"
STATUS_T1_PACKAGE_BLOCKED: Final[str] = "t1_30min_checkpoint_produced_package_blocked"
STATUS_T1_PACKAGE_READY: Final[str] = "t1_30min_checkpoint_produced_package_ready"

NON_CLAIMS_V15_M21: Final[tuple[str, ...]] = (
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

DEFAULT_CLAIM_FLAGS: Final[dict[str, bool]] = {
    "strength_evaluated": False,
    "checkpoint_promoted": False,
    "benchmark_passed": False,
    "xai_claim_authorized": False,
    "human_benchmark_claim_authorized": False,
    "showcase_release_authorized": False,
    "v2_authorized": False,
}

STRONGEST_ALLOWED_CLAIM_M21: Final[str] = (
    "STARLAB completed the governed T1 30-minute operator-local GPU run and captured "
    "checkpoint-production evidence, or recorded an honest preflight/run blocker."
)

DRY_RUN_STATUS_PASSED: Final[str] = "passed"
DRY_RUN_STATUS_FAILED: Final[str] = "failed"
DRY_RUN_STATUS_NOT_APPLICABLE: Final[str] = "not_applicable"
