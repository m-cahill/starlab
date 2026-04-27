"""V15-M19 — candidate checkpoint evaluation package assembly (constants)."""

from __future__ import annotations

from enum import StrEnum
from typing import Final

CONTRACT_ID_CANDIDATE_CHECKPOINT_EVALUATION_PACKAGE: Final[str] = (
    "starlab.v15.candidate_checkpoint_evaluation_package.v1"
)
MILESTONE_ID_V15_M19: Final[str] = "V15-M19"
EMITTER_MODULE: Final[str] = "starlab.v15.emit_v15_candidate_checkpoint_evaluation_package"

SCHEMA_VERSION: Final[str] = "1.0"
REPORT_VERSION: Final[str] = "1"
SEAL_KEY_ARTIFACT: Final[str] = "artifact_sha256"

FILENAME_PACKAGE: Final[str] = "v15_candidate_checkpoint_evaluation_package.json"
REPORT_FILENAME: Final[str] = "v15_candidate_checkpoint_evaluation_package_report.json"
CHECKLIST_FILENAME: Final[str] = "v15_candidate_checkpoint_evaluation_package_checklist.md"

PROFILE_FIXTURE_DEFAULT: Final[str] = "fixture_default"
PROFILE_OPERATOR_PREFLIGHT: Final[str] = "operator_preflight"
PROFILE_OPERATOR_DECLARED: Final[str] = "operator_declared"


class PackageStatus(StrEnum):
    """M19 package assembly status (machine vocabulary)."""

    BLOCKED_MISSING_CANDIDATE_CHECKPOINT_EVIDENCE = "blocked_missing_candidate_checkpoint_evidence"
    BLOCKED_INCOMPLETE_EVALUATION_PACKAGE_INPUTS = "blocked_incomplete_evaluation_package_inputs"
    BLOCKED_INVALID_CANDIDATE_PACKAGE = "blocked_invalid_candidate_package"
    EVALUATION_PACKAGE_READY = "evaluation_package_ready"


REQUIRED_INPUT_LIST: Final[tuple[str, ...]] = (
    "m18_readiness_json",
    "candidate_checkpoint_manifest",
    "candidate_checkpoint_sha256",
    "completed_m08_campaign_receipt",
    "checkpoint_lineage_manifest",
    "environment_manifest",
    "dataset_manifest",
    "evaluation_protocol",
)

NON_CLAIMS_V15_M19: Final[tuple[str, ...]] = (
    "not_checkpoint_evaluation",
    "not_strength_evaluation",
    "not_checkpoint_promotion",
    "not_benchmark_pass",
    "not_xai_claim",
    "not_human_benchmark_claim",
    "not_showcase_release",
    "not_v2_authorization",
)

STRONGEST_ALLOWED_CLAIM_M19: Final[str] = (
    "STARLAB can deterministically assemble, bind, and audit a candidate checkpoint "
    "evaluation-input package, or refuse with a precise missing-input inventory."
)

READY_SEMANTICS_M19: Final[str] = (
    "evaluation_package_ready means ready_for_future_checkpoint_evaluation only. "
    "It is not a strength, promotion, or benchmark result."
)

REASON_INVALID_M18_CONTRACT: Final[str] = "invalid_m18_readiness_contract_id"
REASON_JOBLIB: Final[str] = "sklearn_joblib_not_promoted_pytorch_checkpoint"
REASON_NOT_EXECUTED: Final[str] = "campaign_receipt_not_executed_or_empty_checkpoints"
REASON_HASH_MISMATCH: Final[str] = "cross_artifact_checkpoint_or_binding_hash_mismatch"
REASON_SCORECARD_CONTRACT: Final[str] = "strong_agent_scorecard_contract_or_protocol_mismatch"
REASON_ENV_CONTRACT: Final[str] = "environment_lock_contract_mismatch"
REASON_M18_REFUSAL: Final[str] = "m18_readiness_posture_blocks_package"

# Deterministic M20 fork recommendations
M20_FORK_READY_ID: Final[str] = "candidate_checkpoint_evaluation_scorecard_v1"
M20_FORK_READY_TITLE: Final[str] = "V15-M20 — Candidate Checkpoint Evaluation & Scorecard v1"

M20_FORK_MISSING_ID: Final[str] = "real_candidate_checkpoint_production_gate"
M20_FORK_MISSING_TITLE: Final[str] = "V15-M20 — Real Candidate Checkpoint Production Gate"

M20_FORK_INCOMPLETE_ID: Final[str] = "candidate_evidence_remediation_ii"
M20_FORK_INCOMPLETE_TITLE: Final[str] = "V15-M20 — Candidate Evidence Remediation II"

M20_FORK_INVALID_ID: Final[str] = "candidate_rejection_replacement_gate"
M20_FORK_INVALID_TITLE: Final[str] = "V15-M20 — Candidate Rejection / Replacement Gate"
