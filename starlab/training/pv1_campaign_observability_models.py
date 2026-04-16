"""Constants and version ids for PV1-M01 campaign observability / checkpoint receipts."""

from __future__ import annotations

from typing import Final

# Artifact versions
TRANCHE_CHECKPOINT_RECEIPT_VERSION: Final[str] = "starlab.tranche_checkpoint_receipt.v1"
TRANCHE_CHECKPOINT_RECEIPT_REPORT_VERSION: Final[str] = (
    "starlab.tranche_checkpoint_receipt_report.v1"
)

CAMPAIGN_OBSERVABILITY_INDEX_VERSION: Final[str] = "starlab.pv1_campaign_observability_index.v1"
CAMPAIGN_OBSERVABILITY_INDEX_REPORT_VERSION: Final[str] = (
    "starlab.pv1_campaign_observability_index_report.v1"
)

TRANCHE_CHECKPOINT_RECEIPT_FILENAME: Final[str] = "tranche_checkpoint_receipt.json"
TRANCHE_CHECKPOINT_RECEIPT_REPORT_FILENAME: Final[str] = "tranche_checkpoint_receipt_report.json"

CAMPAIGN_OBSERVABILITY_INDEX_FILENAME: Final[str] = "campaign_observability_index.json"
CAMPAIGN_OBSERVABILITY_INDEX_REPORT_FILENAME: Final[str] = (
    "campaign_observability_index_report.json"
)

# Locked, small posture vocabulary (deterministic enumeration strings).
EVIDENCE_STATUS_COMPLETE: Final[str] = "complete"
EVIDENCE_STATUS_INCOMPLETE: Final[str] = "incomplete"
EVIDENCE_STATUS_PAUSED: Final[str] = "paused"
EVIDENCE_STATUS_MISSING_REQUIRED_EVIDENCE: Final[str] = "missing_required_evidence"
EVIDENCE_STATUS_NOT_EVALUABLE: Final[str] = "not_evaluable"

ALL_EVIDENCE_STATUSES_V1: Final[tuple[str, ...]] = tuple(
    sorted(
        (
            EVIDENCE_STATUS_COMPLETE,
            EVIDENCE_STATUS_INCOMPLETE,
            EVIDENCE_STATUS_PAUSED,
            EVIDENCE_STATUS_MISSING_REQUIRED_EVIDENCE,
            EVIDENCE_STATUS_NOT_EVALUABLE,
        ),
    ),
)

# Sorted for deterministic JSON emission.
PV1_OBSERVABILITY_NON_CLAIMS_V1: Final[tuple[str, ...]] = (
    "starlab.pv1.obs.not_automatic_campaign_success",
    "starlab.pv1.obs.not_benchmark_integrity",
    "starlab.pv1.obs.not_fabricating_missing_files",
    "starlab.pv1.obs.not_healing_incomplete_evidence",
    "starlab.pv1.obs.not_live_sc2_in_ci",
    "starlab.pv1.obs.not_ladder_or_public_strength",
    "starlab.pv1.obs.not_proof_of_full_training_run_threshold",
    "starlab.pv1.obs.not_replay_execution_equivalence",
    "starlab.pv1.obs.not_substitute_for_operator_execution",
    "starlab.pv1.obs.reference_inspection_helpers_only",
)
