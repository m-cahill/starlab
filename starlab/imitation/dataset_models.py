"""Typed constants for replay training dataset artifacts (M26)."""

from __future__ import annotations

from typing import Final

REPLAY_TRAINING_DATASET_VERSION: Final[str] = "starlab.replay_training_dataset.v1"
REPLAY_TRAINING_DATASET_REPORT_VERSION: Final[str] = "starlab.replay_training_dataset_report.v1"

SELECTION_POLICY_ID: Final[str] = "starlab.m26.selection.timeline_entries_v1"
SPLIT_POLICY_ID: Final[str] = "starlab.m26.split.sha256_mod100_v1"
LABEL_POLICY_ID: Final[str] = "starlab.m26.label.coarse_action_v1"

APPROVED_TARGET_SEMANTIC_KINDS: frozenset[str] = frozenset(
    {
        "economy_expand",
        "economy_worker",
        "production_unit",
        "production_structure",
        "research_upgrade",
        "army_move",
        "army_attack",
        "scout",
        "other",
    },
)

REPLAY_TRAINING_DATASET_FILENAME: Final[str] = "replay_training_dataset.json"
REPLAY_TRAINING_DATASET_REPORT_FILENAME: Final[str] = "replay_training_dataset_report.json"

NON_CLAIMS_V1: Final[tuple[str, ...]] = (
    "benchmark_integrity",
    "imitation_quality",
    "live_sc2_execution",
    "m27_imitation_baseline_training",
    "m28_plus_product_claims",
    "model_training",
    "raw_replay_packaging",
    "replay_execution_equivalence",
    "replay_parser_correctness",
    "full_action_legality",
)

UNSAFE_INTAKE_STATUSES: Final[frozenset[str]] = frozenset({"quarantined", "rejected"})
