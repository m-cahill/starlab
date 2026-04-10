"""Constants for replay hierarchical imitation agent artifacts (M30)."""

from __future__ import annotations

from typing import Final

from starlab.hierarchy.hierarchical_interface_models import TRACE_DOCUMENT_SCHEMA_VERSION

AGENT_VERSION: Final[str] = "starlab.replay_hierarchical_imitation_agent.v1"
REPORT_VERSION: Final[str] = "starlab.replay_hierarchical_imitation_agent_report.v1"

MANAGER_MODEL_FAMILY: Final[str] = "starlab.m30.model.manager_signature_delegate_majority_v1"
WORKER_MODEL_FAMILY: Final[str] = "starlab.m30.model.worker_delegate_signature_label_majority_v1"

FEATURE_POLICY_ID: Final[str] = "starlab.m27.feature.observation_signature_v1"

REPLAY_HIERARCHICAL_IMITATION_AGENT_FILENAME: Final[str] = (
    "replay_hierarchical_imitation_agent.json"
)
REPLAY_HIERARCHICAL_IMITATION_AGENT_REPORT_FILENAME: Final[str] = (
    "replay_hierarchical_imitation_agent_report.json"
)

NON_CLAIMS_V1: Final[tuple[str, ...]] = (
    "benchmark_integrity",
    "first_flagship_proof_pack",
    "hierarchical_policy_optimality",
    "leaderboard_validity",
    "live_sc2_execution",
    "m31_replay_explorer_product",
    "raw_sc2_action_legality",
    "replay_execution_equivalence",
    "replay_parser_in_m30_modules",
    "strong_imitation_quality_beyond_internal_smoke",
)

# Same field as M29 trace documents; explicit anchor for hierarchical traces.
INTERFACE_TRACE_SCHEMA_VERSION: Final[str] = TRACE_DOCUMENT_SCHEMA_VERSION
