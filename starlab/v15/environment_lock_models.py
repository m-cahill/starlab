"""Constants and vocabulary for V15-M02 long GPU environment lock (deterministic JSON)."""

from __future__ import annotations

from typing import Final

CONTRACT_ID_LONG_GPU_ENV: Final[str] = "starlab.v15.long_gpu_environment_lock.v1"
REPORT_VERSION_LONG_GPU_ENV: Final[str] = "starlab.v15.long_gpu_environment_lock_report.v1"
FILENAME_LONG_GPU_ENV: Final[str] = "v15_long_gpu_environment_lock.json"
REPORT_FILENAME_LONG_GPU_ENV: Final[str] = "v15_long_gpu_environment_lock_report.json"

MILESTONE_ID_V15_M02: Final[str] = "V15-M02"

EMITTER_MODULE: Final[str] = "starlab.v15.emit_v15_long_gpu_environment_lock"

PROFILE_FIXTURE_CI: Final[str] = "fixture_ci"
PROFILE_OPERATOR_LOCAL: Final[str] = "operator_local"

# environment_lock_status
STATUS_FIXTURE_ONLY: Final[str] = "fixture_only"
STATUS_OPERATOR_LOCAL_READY: Final[str] = "operator_local_ready"
STATUS_OPERATOR_LOCAL_INCOMPLETE: Final[str] = "operator_local_incomplete"
STATUS_BLOCKED: Final[str] = "blocked"
STATUS_NOT_EVALUATED: Final[str] = "not_evaluated"

# check_status
CHECK_PASS: Final[str] = "pass"
CHECK_FAIL: Final[str] = "fail"
CHECK_WARNING: Final[str] = "warning"
CHECK_NOT_APPLICABLE: Final[str] = "not_applicable"
CHECK_NOT_EVALUATED: Final[str] = "not_evaluated"
CHECK_FIXTURE: Final[str] = "fixture"

# path_disclosure
PATH_PUBLIC_SAFE: Final[str] = "public_safe"
PATH_REDACTED: Final[str] = "redacted"
PATH_LOGICAL_REFERENCE: Final[str] = "logical_reference_only"
PATH_PRIVATE_LOCAL: Final[str] = "private_local_only"
PATH_FORBIDDEN_PUBLIC: Final[str] = "forbidden_public"

# evidence_scope
EVIDENCE_CI_FIXTURE: Final[str] = "ci_fixture"
EVIDENCE_OPERATOR_PROBE: Final[str] = "operator_local_probe"
EVIDENCE_OPERATOR_DECLARED: Final[str] = "operator_declared"
EVIDENCE_NOT_EVALUATED: Final[str] = "not_evaluated"

STATUS_VOCABULARY: Final[dict[str, tuple[str, ...]]] = {
    "environment_lock_status": (
        STATUS_FIXTURE_ONLY,
        STATUS_OPERATOR_LOCAL_READY,
        STATUS_OPERATOR_LOCAL_INCOMPLETE,
        STATUS_BLOCKED,
        STATUS_NOT_EVALUATED,
    ),
    "check_status": (
        CHECK_PASS,
        CHECK_FAIL,
        CHECK_WARNING,
        CHECK_NOT_APPLICABLE,
        CHECK_NOT_EVALUATED,
        CHECK_FIXTURE,
    ),
    "path_disclosure": (
        PATH_PUBLIC_SAFE,
        PATH_REDACTED,
        PATH_LOGICAL_REFERENCE,
        PATH_PRIVATE_LOCAL,
        PATH_FORBIDDEN_PUBLIC,
    ),
    "evidence_scope": (
        EVIDENCE_CI_FIXTURE,
        EVIDENCE_OPERATOR_PROBE,
        EVIDENCE_OPERATOR_DECLARED,
        EVIDENCE_NOT_EVALUATED,
    ),
}

NON_CLAIMS_V15_M02: Final[tuple[str, ...]] = (
    "long_gpu_training_executed",
    "gpu_shakedown_executed_m07",
    "m02_authorizes_long_gpu_run",
    "m02_proves_portable_globally",
    "checkpoint_lineage_runtime_implemented_m03",
    "xai_evidence_contract_frozen_m04",
    "strong_agent_benchmark_executed_m05",
    "human_panel_benchmark_executed_m06",
    "claim_critical_dataset_or_weights_approved",
    "v2_opened",
    "px2_m04_opened",
    "px2_m05_opened",
)

PROBE_TOP_LEVEL_KEYS: Final[tuple[str, ...]] = (
    "evidence_scope",
    "repo_identity",
    "python_environment",
    "dependency_environment",
    "cuda_environment",
    "pytorch_environment",
    "gpu_environment",
    "sc2_environment",
    "map_pool_environment",
    "disk_environment",
    "operator_notes",
    "path_disclosure_policy",
)

# Keys allowed on probe root beyond environment sections
PROBE_OPTIONAL_ROOT_KEYS: Final[set[str]] = set(PROBE_TOP_LEVEL_KEYS)
