"""Milestone / role labels for replay bundle lineage (M14)."""

from __future__ import annotations

from typing import Any

# Primary artifact filename -> (milestone id, node id suffix, human label)
PRIMARY_NODE_INFO: dict[str, tuple[str, str, str]] = {
    "replay_metadata.json": ("M09", "m09_metadata", "Replay metadata (M09)"),
    "replay_timeline.json": ("M10", "m10_timeline", "Replay timeline (M10)"),
    "replay_build_order_economy.json": (
        "M11",
        "m11_build_order_economy",
        "Build-order / economy (M11)",
    ),
    "replay_combat_scouting_visibility.json": (
        "M12",
        "m12_combat_scouting_visibility",
        "Combat / scouting / visibility (M12)",
    ),
    "replay_slices.json": ("M13", "m13_replay_slices", "Replay slice definitions (M13)"),
}

SECONDARY_REPORT_NODE_INFO: dict[str, tuple[str, str, str]] = {
    "replay_metadata_report.json": (
        "M09",
        "m09_metadata_report",
        "Replay metadata report (M09)",
    ),
    "replay_timeline_report.json": (
        "M10",
        "m10_timeline_report",
        "Replay timeline report (M10)",
    ),
    "replay_build_order_economy_report.json": (
        "M11",
        "m11_build_order_economy_report",
        "Build-order / economy report (M11)",
    ),
    "replay_combat_scouting_visibility_report.json": (
        "M12",
        "m12_combat_scouting_visibility_report",
        "Combat / scouting / visibility report (M12)",
    ),
    "replay_slices_report.json": ("M13", "m13_replay_slices_report", "Replay slices report (M13)"),
}


def optional_contextual_ancestry_note() -> str:
    """Explicit non-claim for optional M07/M08 lineage nodes."""

    return (
        "Optional M07 intake and M08 parser-substrate lineage nodes (when present) are "
        "contextual ancestry only; they are not part of the required M14 proof surface."
    )


def included_milestones_primary() -> list[str]:
    return ["M09", "M10", "M11", "M12", "M13"]


def exclusions_policy_v1() -> list[str]:
    return sorted(
        [
            "raw_replay_bytes_sc2replay",
            "replay_raw_parse_json",
            "parser_owned_binary_blobs",
            "clipped_sub_replays",
            "videos_images_unless_future_milestone",
            "archive_compression_not_required_in_v1",
        ],
    )


def determinism_notes_v1() -> str:
    return (
        "Manifest and lineage are emitted from canonical JSON hashes of governed inputs; "
        "ordering is deterministic; no wall-clock timestamps or local filesystem paths."
    )


def bundle_node_id() -> str:
    return "m14_replay_bundle"


def bundle_node_label() -> str:
    return "Replay bundle packaging (M14)"


def node_record(
    *,
    node_id: str,
    milestone: str,
    label: str,
    artifact_filename: str | None,
    content_sha256: str | None,
    proof_surface_required: bool,
    contextual_ancestry: bool,
) -> dict[str, Any]:
    row: dict[str, Any] = {
        "contextual_ancestry": contextual_ancestry,
        "label": label,
        "milestone": milestone,
        "node_id": node_id,
        "proof_surface_required": proof_surface_required,
    }
    if artifact_filename is not None:
        row["artifact_filename"] = artifact_filename
    if content_sha256 is not None:
        row["content_sha256"] = content_sha256
    return row
