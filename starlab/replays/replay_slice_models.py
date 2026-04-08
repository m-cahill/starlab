"""Schema constants for replay slice artifacts (M13)."""

from __future__ import annotations

REPLAY_SLICES_CONTRACT_VERSION = "starlab.replay_slices_contract.v1"
REPLAY_SLICES_PROFILE = "starlab.replay_slices.m13.v1"
REPLAY_SLICES_SCHEMA_VERSION = "starlab.replay_slices.v1"
REPLAY_SLICES_REPORT_SCHEMA_VERSION = "starlab.replay_slices_report.v1"

SLICE_PADDING_PRE_LOOPS = 160
SLICE_PADDING_POST_LOOPS = 160

SliceKind = str  # "combat_window" | "scouting_observation"

SLICE_KIND_COMBAT = "combat_window"
SLICE_KIND_SCOUTING = "scouting_observation"
