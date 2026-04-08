"""Field lists, omission rules, and non-claims for canonical state schema v1 (M15)."""

from __future__ import annotations

REQUIRED_TOP_LEVEL_FIELDS: tuple[str, ...] = (
    "schema_version",
    "frame_kind",
    "source",
    "gameloop",
    "players",
    "global_context",
    "provenance",
)

REQUIRED_PLAYER_FIELDS: tuple[str, ...] = (
    "player_index",
    "race_actual",
    "economy_summary",
    "production_summary",
    "army_summary",
)

OPTIONAL_SECTIONS: tuple[str, ...] = (
    "source.source_bundle_id",
    "source.source_lineage_root",
    "source.source_replay_identity",
    "players[].result",
    "players[].combat_context",
    "players[].scouting_context",
    "players[].visibility_context",
    "global_context.map_name",
    "global_context.active_slice_ids",
    "global_context.active_combat_window_ids",
)

OMISSION_RULES_V1: tuple[str, ...] = (
    "Optional fields are omitted when not derivable from governed replay planes (M09–M14).",
    (
        "Use JSON null only when a field is applicable but intentionally unresolved; "
        "do not invent defaults."
    ),
    "Do not include player display names, chat text, or other PII in public contract documents.",
    (
        "Economy and resource fields are summaries or categories only — not exact banked "
        "minerals/gas (M11 non-claim)."
    ),
    (
        "Visibility-related fields are proxy signals only — not certified fog-of-war truth "
        "(M12 non-claim)."
    ),
)

NON_CLAIMS_V1: tuple[str, ...] = (
    "Does not prove replay-to-state extraction from bundles (M16).",
    "Does not prove observation surface semantics (M17) or perceptual bridge behavior (M18).",
    "Does not prove replay↔execution equivalence, benchmark integrity, or live SC2 in CI.",
    "Does not certify omniscient or hidden game truth; bounded to replay-derived artifacts only.",
)

FRAME_KIND_VALUES: tuple[str, ...] = ("replay_snapshot", "replay_derived")

RACE_ACTUAL_VALUES: tuple[str, ...] = ("Terran", "Protoss", "Zerg", "Random")

RESULT_VALUES: tuple[str, ...] = ("win", "loss", "tie", "unknown")
