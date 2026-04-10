"""Constants and helpers for replay explorer surface (M31)."""

from __future__ import annotations

SURFACE_VERSION = "starlab.replay_explorer_surface.v1"
SELECTION_POLICY_ID = "starlab.m31.selection.slice_anchor_v1"
REPORT_VERSION = "starlab.replay_explorer_surface_report.v1"

# Fixed excerpt caps (must match docs/runtime/replay_explorer_surface_v1.md)
TIMELINE_EXCERPT_MAX = 8
ECONOMY_EXCERPT_MAX = 6
COMBAT_SCOUTING_EXCERPT_MAX = 6
OBSERVATION_SCALAR_ENTRIES_MAX = 12

DEFAULT_MAX_PANELS = 5

DEFAULT_NON_CLAIMS: tuple[str, ...] = (
    "benchmark_integrity_not_claimed",
    "leaderboard_validity_not_claimed",
    "live_sc2_execution_not_claimed",
    "replay_execution_equivalence_not_claimed",
    "raw_sc2_action_legality_not_claimed",
    "full_replay_coverage_not_claimed_hosted_ui_not_claimed",
    "m32_flagship_proof_pack_not_claimed",
    "deployment_readiness_not_claimed",
)
