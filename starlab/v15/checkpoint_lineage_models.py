"""Constants and vocabulary for V15-M03 checkpoint lineage manifest (deterministic JSON)."""

from __future__ import annotations

from typing import Final

CONTRACT_ID_CHECKPOINT_LINEAGE: Final[str] = "starlab.v15.checkpoint_lineage_manifest.v1"
REPORT_VERSION_CHECKPOINT_LINEAGE: Final[str] = "starlab.v15.checkpoint_lineage_manifest_report.v1"
FILENAME_CHECKPOINT_LINEAGE: Final[str] = "v15_checkpoint_lineage_manifest.json"
REPORT_FILENAME_CHECKPOINT_LINEAGE: Final[str] = "v15_checkpoint_lineage_manifest_report.json"

MILESTONE_ID_V15_M03: Final[str] = "V15-M03"

EMITTER_MODULE_CHECKPOINT_LINEAGE: Final[str] = "starlab.v15.emit_v15_checkpoint_lineage_manifest"

PROFILE_FIXTURE_CI: Final[str] = "fixture_ci"
PROFILE_OPERATOR_DECLARED: Final[str] = "operator_declared"

# lineage_manifest_status
LINEAGE_STATUS_FIXTURE_ONLY: Final[str] = "fixture_only"
LINEAGE_STATUS_OP_COMPLETE: Final[str] = "operator_declared_complete"
LINEAGE_STATUS_OP_INCOMPLETE: Final[str] = "operator_declared_incomplete"
LINEAGE_STATUS_BLOCKED: Final[str] = "blocked"
LINEAGE_STATUS_NOT_EVALUATED: Final[str] = "not_evaluated"

# evidence_scope
EVIDENCE_CI_FIXTURE: Final[str] = "ci_fixture"
EVIDENCE_OPERATOR_DECLARED: Final[str] = "operator_declared"
EVIDENCE_OPERATOR_LOCAL_METADATA: Final[str] = "operator_local_metadata"
EVIDENCE_NOT_EVALUATED: Final[str] = "not_evaluated"

# check_status
CHECK_PASS: Final[str] = "pass"
CHECK_FAIL: Final[str] = "fail"
CHECK_WARNING: Final[str] = "warning"
CHECK_NOT_APPLICABLE: Final[str] = "not_applicable"
CHECK_FIXTURE: Final[str] = "fixture"

STATUS_VOCABULARY: Final[dict[str, tuple[str, ...]]] = {
    "lineage_manifest_status": (
        LINEAGE_STATUS_FIXTURE_ONLY,
        LINEAGE_STATUS_OP_COMPLETE,
        LINEAGE_STATUS_OP_INCOMPLETE,
        LINEAGE_STATUS_BLOCKED,
        LINEAGE_STATUS_NOT_EVALUATED,
    ),
    "checkpoint_role": (
        "initial",
        "candidate",
        "promoted",
        "rejected",
        "rollback_target",
        "archived",
        "fixture",
    ),
    "promotion_status": (
        "not_evaluated",
        "candidate",
        "promoted",
        "rejected",
        "archived",
        "fixture_only",
    ),
    "hash_verification_status": (
        "fixture",
        "declared_only",
        "verified_external",
        "missing",
        "mismatch",
        "not_evaluated",
    ),
    "resume_verification_status": (
        "fixture",
        "declared_only",
        "not_executed",
        "verified_external",
        "failed",
        "not_evaluated",
    ),
    "rollback_verification_status": (
        "fixture",
        "declared_only",
        "not_executed",
        "verified_external",
        "failed",
        "not_evaluated",
    ),
    "checkpoint_storage_posture": (
        "repo_fixture",
        "local_out",
        "external_archive",
        "private_local_only",
        "not_committed",
        "unknown",
    ),
    "checkpoint_path_disclosure": (
        "public_safe",
        "redacted",
        "logical_reference_only",
        "private_local_only",
        "forbidden_public",
    ),
    "evidence_scope": (
        EVIDENCE_CI_FIXTURE,
        EVIDENCE_OPERATOR_DECLARED,
        EVIDENCE_OPERATOR_LOCAL_METADATA,
        EVIDENCE_NOT_EVALUATED,
    ),
    "receipt_status": (
        "fixture",
        "declared_only",
        "verified_external",
        "not_evaluated",
    ),
    "check_status": (CHECK_PASS, CHECK_FAIL, CHECK_WARNING, CHECK_NOT_APPLICABLE, CHECK_FIXTURE),
}

NON_CLAIMS_V15_M03: Final[tuple[str, ...]] = (
    "m03_creates_checkpoint_blobs",
    "m03_verifies_checkpoint_bytes_by_default",
    "m03_executes_trainer_resume",
    "m03_executes_rollback",
    "m03_promotes_strong_checkpoint",
    "m03_runs_evaluation",
    "m03_executes_gpu_training",
    "m03_executes_gpu_shakedown",
    "m03_authorizes_long_gpu_run",
    "m03_approves_claim_critical_real_assets",
    "v2_opened",
    "px2_m04_opened",
    "px2_m05_opened",
    "m03_independently_verifies_verified_external_fields",
)

LINEAGE_JSON_TOP_LEVEL_KEYS: Final[tuple[str, ...]] = (
    "profile",
    "training_run_id",
    "environment_lock_reference",
    "dataset_reference",
    "model_config_reference",
    "checkpoints",
    "interruption_receipts",
    "resume_receipts",
    "rollback_receipts",
    "operator_notes",
)

CHECKPOINT_ROW_REQUIRED_FIELDS: Final[tuple[str, ...]] = (
    "checkpoint_id",
    "checkpoint_role",
    "checkpoint_storage_posture",
    "checkpoint_path_disclosure",
    "checkpoint_uri_or_reference",
    "checkpoint_sha256",
    "hash_verification_status",
    "parent_checkpoint_id",
    "training_run_id",
    "environment_lock_sha256",
    "dataset_manifest_sha256",
    "model_config_sha256",
    "step",
    "episode",
    "wall_clock_elapsed",
    "promotion_status",
    "created_by_event",
    "non_claims",
)

INTERRUPTION_RECEIPT_REQUIRED_FIELDS: Final[tuple[str, ...]] = (
    "interruption_id",
    "training_run_id",
    "checkpoint_id",
    "reason",
    "interruption_step",
    "interruption_episode",
    "operator_declared_at",
    "receipt_status",
    "notes",
)

RESUME_RECEIPT_REQUIRED_FIELDS: Final[tuple[str, ...]] = (
    "resume_id",
    "training_run_id",
    "from_checkpoint_id",
    "resume_step",
    "resume_episode",
    "resume_policy",
    "resume_verification_status",
    "notes",
)

ROLLBACK_RECEIPT_REQUIRED_FIELDS: Final[tuple[str, ...]] = (
    "rollback_id",
    "training_run_id",
    "from_checkpoint_id",
    "to_checkpoint_id",
    "rollback_reason",
    "rollback_policy",
    "rollback_verification_status",
    "notes",
)

CONTRACT_ID_M02_ENV_LOCK: Final[str] = "starlab.v15.long_gpu_environment_lock.v1"
