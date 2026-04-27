"""V15-M18 — checkpoint evaluation readiness / refusal contract (constants)."""

from __future__ import annotations

from enum import StrEnum
from typing import Final

CONTRACT_ID_CHECKPOINT_EVALUATION_READINESS: Final[str] = (
    "starlab.v15.checkpoint_evaluation_readiness.v1"
)
CONTRACT_ID_CANDIDATE_CHECKPOINT_MANIFEST: Final[str] = (
    "starlab.v15.candidate_checkpoint_manifest.v1"
)
MILESTONE_ID_V15_M18: Final[str] = "V15-M18"
EMITTER_MODULE_CHECKPOINT_EVALUATION_READINESS: Final[str] = (
    "starlab.v15.emit_v15_checkpoint_evaluation_readiness"
)

SCHEMA_VERSION: Final[str] = "1.0"
REPORT_VERSION: Final[str] = "1"
SEAL_KEY_ARTIFACT: Final[str] = "artifact_sha256"

FILENAME_CHECKPOINT_EVALUATION_READINESS: Final[str] = "v15_checkpoint_evaluation_readiness.json"
REPORT_FILENAME_CHECKPOINT_EVALUATION_READINESS: Final[str] = (
    "v15_checkpoint_evaluation_readiness_report.json"
)

PROFILE_FIXTURE_DEFAULT: Final[str] = "fixture_default"
PROFILE_OPERATOR_EXPLICIT_INPUTS: Final[str] = "operator_explicit_inputs"

PLACEHOLDER_SHA256: Final[str] = "0" * 64


class CandidateReadinessStatus(StrEnum):
    """M18 readiness / refusal classification (machine vocabulary)."""

    NO_CANDIDATE_REFUSAL = "no_candidate_refusal"
    CANDIDATE_EVIDENCE_INCOMPLETE = "candidate_evidence_incomplete"
    CANDIDATE_READY_FOR_EVALUATION = "candidate_ready_for_evaluation"
    INVALID_OR_UNSUPPORTED_CANDIDATE = "invalid_or_unsupported_candidate"


class CandidateKind(StrEnum):
    """Candidate artifact classification for M18 (not strength)."""

    NONE = "none"
    PYTORCH_CHECKPOINT = "pytorch_checkpoint"
    SKLEARN_BUNDLE = "sklearn_bundle"
    UNKNOWN_ARTIFACT = "unknown_artifact"


REQUIRED_INPUT_KEYS: Final[tuple[str, ...]] = (
    "candidate_checkpoint_manifest",
    "candidate_checkpoint_sha256",
    "campaign_receipt",
    "training_completion_status",
    "checkpoint_lineage_manifest",
    "environment_manifest",
    "dataset_manifest",
    "evaluation_protocol",
)

REFUSAL_NO_MANIFEST: Final[str] = "no_candidate_checkpoint_manifest_provided"
REFUSAL_WATCHABILITY_ONLY: Final[str] = "watchability_evidence_is_not_candidate_checkpoint_evidence"
REFUSAL_NOT_EXECUTED: Final[str] = "campaign_receipt_not_executed"
REFUSAL_CHECKPOINT_COUNT_ZERO: Final[str] = "campaign_receipt_checkpoint_count_zero"
REFUSAL_JOBLIB_ONLY: Final[str] = "sklearn_joblib_not_promoted_pytorch_checkpoint"
REFUSAL_HASH_MISMATCH: Final[str] = "candidate_checkpoint_hash_mismatch_lineage_or_receipt"
REFUSAL_INVALID_SHA: Final[str] = "candidate_checkpoint_sha256_invalid_or_placeholder"
REFUSAL_MISSING_LINEAGE: Final[str] = "checkpoint_lineage_manifest_missing_or_no_matching_row"
REFUSAL_MISSING_GOVERNED_RECEIPT: Final[str] = "governed_m08_campaign_receipt_missing_or_incomplete"
REFUSAL_MISSING_MANIFEST_FIELDS: Final[str] = (
    "candidate_manifest_missing_environment_dataset_or_evaluation_bindings"
)

NON_CLAIMS_V15_M18: Final[tuple[str, ...]] = (
    "not_strength_evaluation",
    "not_checkpoint_promotion",
    "not_benchmark_pass",
    "not_human_panel_claim",
    "not_xai_claim",
    "not_v2_authorization",
    "not_long_gpu_campaign_completed_claim",
)

STRONGEST_ALLOWED_CLAIM_M18: Final[str] = (
    "STARLAB can deterministically classify whether candidate-checkpoint evidence is sufficient "
    "to begin a future evaluation milestone (inputs only; not strength)."
)

REPORT_SEMANTICS_READY: Final[str] = (
    "This status means the input evidence package is structurally ready for a future evaluation "
    "milestone (ready_for_future_evaluation). It is not a strength result."
)
