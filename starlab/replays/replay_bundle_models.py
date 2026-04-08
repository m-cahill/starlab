"""Schema constants for replay bundle + lineage artifacts (M14)."""

from __future__ import annotations

REPLAY_BUNDLE_CONTRACT_VERSION = "starlab.replay_bundle_contract.v1"
REPLAY_BUNDLE_PROFILE = "starlab.replay_bundle.m14.v1"
REPLAY_BUNDLE_MANIFEST_SCHEMA_VERSION = "starlab.replay_bundle_manifest.v1"
REPLAY_BUNDLE_LINEAGE_SCHEMA_VERSION = "starlab.replay_bundle_lineage.v1"
REPLAY_BUNDLE_CONTENTS_SCHEMA_VERSION = "starlab.replay_bundle_contents.v1"

PRIMARY_ARTIFACT_FILENAMES: tuple[str, ...] = (
    "replay_metadata.json",
    "replay_timeline.json",
    "replay_build_order_economy.json",
    "replay_combat_scouting_visibility.json",
    "replay_slices.json",
)

SECONDARY_REPORT_FILENAMES: tuple[str, ...] = (
    "replay_metadata_report.json",
    "replay_timeline_report.json",
    "replay_build_order_economy_report.json",
    "replay_combat_scouting_visibility_report.json",
    "replay_slices_report.json",
)
