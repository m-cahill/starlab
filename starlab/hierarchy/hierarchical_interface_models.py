"""Constants for the hierarchical agent interface layer (M29).

Coarse semantic labels are owned by this milestone's JSON Schema enum and are kept
1:1 aligned with ``starlab.m26.label.coarse_action_v1`` / ``APPROVED_TARGET_SEMANTIC_KINDS``
(``starlab.imitation.dataset_models``) without importing training artifacts at validation time.
"""

from __future__ import annotations

from typing import Final

HIERARCHICAL_AGENT_INTERFACE_SCHEMA_VERSION: Final[str] = (
    "starlab.hierarchical_agent_interface_schema.v1"
)
HIERARCHICAL_AGENT_INTERFACE_SCHEMA_REPORT_VERSION: Final[str] = (
    "starlab.hierarchical_agent_interface_schema_report.v1"
)
TRACE_DOCUMENT_SCHEMA_VERSION: Final[str] = "starlab.hierarchical_agent_interface_trace.v1"

HIERARCHICAL_AGENT_INTERFACE_CONTRACT: Final[str] = "starlab.hierarchical_agent_interface.v1"
HIERARCHICAL_AGENT_INTERFACE_PROFILE: Final[str] = "two_level_manager_worker_offline_v1"

HIERARCHICAL_AGENT_INTERFACE_JSON_SCHEMA_ID: Final[str] = (
    "https://starlab.dev/schemas/hierarchical_agent_interface_schema.v1.json"
)

HIERARCHICAL_AGENT_INTERFACE_SCHEMA_FILENAME: Final[str] = (
    "hierarchical_agent_interface_schema.json"
)
HIERARCHICAL_AGENT_INTERFACE_SCHEMA_REPORT_FILENAME: Final[str] = (
    "hierarchical_agent_interface_schema_report.json"
)

# Same policy id as M26/M27/M28 coarse label surface; M29 schema enum is the bounded vocabulary.
COARSE_SEMANTIC_LABEL_POLICY_ID: Final[str] = "starlab.m26.label.coarse_action_v1"

# Sorted unique strings; must match M26 approved kinds exactly (1:1).
COARSE_SEMANTIC_LABEL_ENUM: tuple[str, ...] = (
    "army_attack",
    "army_move",
    "economy_expand",
    "economy_worker",
    "other",
    "production_structure",
    "production_unit",
    "research_upgrade",
    "scout",
)

DELEGATE_ROLE_ENUM: tuple[str, ...] = ("worker",)

NON_CLAIMS_V1: Final[tuple[str, ...]] = (
    "benchmark_integrity",
    "first_learned_hierarchical_agent",
    "hierarchical_policy_optimality",
    "leaderboard_validity",
    "live_sc2_execution",
    "m30_plus_learned_hierarchy_claims",
    "multi_level_hierarchy_beyond_two",
    "multi_worker_routing",
    "raw_sc2_action_legality",
    "replay_execution_equivalence",
    "replay_parser_in_m29_modules",
    "training_or_fitting",
)
