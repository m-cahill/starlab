"""Constants for V15-M01 training-scale asset registers (deterministic JSON)."""

from __future__ import annotations

from typing import Final

TRAINING_ASSET_REGISTERS_CONTRACT_VERSION: Final[str] = "starlab.v15.training_asset_registers.v1"
TRAINING_ASSET_REGISTERS_REPORT_VERSION: Final[str] = (
    "starlab.v15.training_asset_registers_report.v1"
)

TRAINING_ASSET_REGISTERS_FILENAME: Final[str] = "v15_training_asset_registers.json"
TRAINING_ASSET_REGISTERS_REPORT_FILENAME: Final[str] = "v15_training_asset_registers_report.json"

MILESTONE_ID_V15_M01: Final[str] = "V15-M01"

NON_CLAIMS_V15_M01: Final[tuple[str, ...]] = (
    "long_gpu_training_executed",
    "gpu_shakedown_executed",
    "environment_lock_completed",
    "checkpoint_lineage_runtime_implemented",
    "xai_evidence_contract_frozen",
    "strong_agent_benchmark_executed",
    "human_panel_benchmark_executed",
    "claim_critical_asset_registered_in_m01",
    "v2_opened",
    "px2_m04_opened",
    "px2_m05_opened",
)

ASSET_CLASSES_V1: Final[tuple[str, ...]] = (
    "code",
    "replay_corpus",
    "training_dataset",
    "label_set",
    "model_weight",
    "checkpoint",
    "benchmark_asset",
    "xai_evidence",
    "human_panel_record",
    "video_or_media",
    "map_pool",
    "environment_reference",
)

ASSET_ROW_REQUIRED_FIELDS_V1: Final[tuple[str, ...]] = (
    "asset_id",
    "asset_class",
    "asset_name",
    "register_id",
    "source_kind",
    "owner_or_steward",
    "storage_posture",
    "public_private_posture",
    "rights_posture",
    "redistribution_posture",
    "hash_policy",
    "sha256_or_hash_reference",
    "claim_use",
    "review_status",
    "governing_doc",
    "notes",
    "non_claims",
)

SOURCE_KIND_VOCABULARY_V1: Final[tuple[str, ...]] = (
    "first_party",
    "third_party",
    "generated",
    "operator_local",
    "human_provided",
    "unknown",
)

STORAGE_POSTURE_VOCABULARY_V1: Final[tuple[str, ...]] = (
    "repo_public",
    "repo_fixture",
    "docs_company_secrets",
    "local_out",
    "external_archive",
    "not_registered",
)

PUBLIC_PRIVATE_POSTURE_VOCABULARY_V1: Final[tuple[str, ...]] = (
    "public",
    "private",
    "local_only",
    "sanitized_public_reference",
    "forbidden_public",
)

RIGHTS_POSTURE_VOCABULARY_V1: Final[tuple[str, ...]] = (
    "first_party_owned",
    "third_party_terms_reviewed",
    "blizzard_terms_local_only",
    "human_private",
    "unclear_quarantined",
    "not_applicable",
)

REDISTRIBUTION_POSTURE_VOCABULARY_V1: Final[tuple[str, ...]] = (
    "redistributable",
    "reference_only",
    "local_only",
    "private_only",
    "forbidden",
    "unknown",
)

CLAIM_USE_VOCABULARY_V1: Final[tuple[str, ...]] = (
    "none",
    "readiness_only",
    "fixture_only",
    "training_candidate",
    "evaluation_candidate",
    "xai_candidate",
    "human_panel_candidate",
    "claim_critical",
)

REVIEW_STATUS_VOCABULARY_V1: Final[tuple[str, ...]] = (
    "not_reviewed",
    "eligible_for_canonical_review",
    "accepted_local_only",
    "accepted_public_reference",
    "accepted_private_reference",
    "quarantined",
    "rejected",
)
