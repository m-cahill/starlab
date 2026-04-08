"""Catalogs, ordering, and non-claims for observation surface contract v1 (M17)."""

from __future__ import annotations

# Visibility policy for agent-facing observation (proxy / bounded — not FOW truth).
VISIBILITY_POLICY_VALUES: tuple[str, ...] = ("proxy_bounded",)

ROW_KIND_VALUES: tuple[str, ...] = (
    "aggregated_category",
    "unit_instance",
)

OWNER_VIEW_VALUES: tuple[str, ...] = ("self", "ally", "enemy", "neutral")

# Structural spatial contract only; not bound to M09 map dimensions.

COORDINATE_FRAME_VALUES: tuple[str, ...] = ("starlab.spatial.not_bound_to_replay_map",)

# Fixed family order for action_mask_families.families[].
ACTION_MASK_FAMILY_NAMES: tuple[str, ...] = (
    "no_op",
    "selection",
    "camera_or_view",
    "production",
    "build",
    "unit_command",
    "research_or_upgrade",
)

# Ordered scalar feature names (metadata + viewpoint-relative summaries).
ORDERED_SCALAR_FEATURE_NAMES: tuple[str, ...] = (
    "economy.resource_signal_category",
    "economy.structure_train_events_total",
    "economy.unit_train_events_total",
    "global.active_combat_window_count",
    "global.active_slice_count",
    "production.active_build_queue_count",
    "production.tech_upgrades_started_total",
    "race.actual",
    "result.known",
    "scouting.recent_scout_events_count",
    "visibility.proxy_level",
)

NON_CLAIMS_V1: tuple[str, ...] = (
    "Does not prove canonical-state→observation materialization or projection (M18+).",
    "Does not prove perceptual bridge, pixels, or image-space feature extraction.",
    "Does not prove full SC2 action coverage, mask legality, or dynamic mask generation.",
    "Does not prove exact banked resources or certified fog-of-war truth (inherits M11/M12/M16).",
    "Does not prove replay↔execution equivalence, benchmark integrity, or live SC2 in CI.",
    "Spatial plane shape metadata is structural only — not bound to M09 map dimensions.",
)

UPSTREAM_LINEAGE_NOTES_V1: tuple[str, ...] = (
    (
        "M15 canonical state schema: docs/runtime/canonical_state_schema_v1.md; "
        "artifact canonical_state_schema.json."
    ),
    (
        "M16 canonical state pipeline: docs/runtime/canonical_state_pipeline_v1.md; "
        "artifacts canonical_state.json, canonical_state_report.json."
    ),
    (
        "M17 binds observation contract semantics to M16 canonical state as upstream — "
        "not to raw replay bundles or replay_raw_parse.json."
    ),
)
