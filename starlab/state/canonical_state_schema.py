"""JSON Schema for canonical state frame v1 + subset validator (M15)."""

from __future__ import annotations

from typing import Any

from starlab.state.canonical_state_catalog import (
    FRAME_KIND_VALUES,
    RACE_ACTUAL_VALUES,
    RESULT_VALUES,
)
from starlab.state.canonical_state_models import (
    CANONICAL_STATE_FRAME_SCHEMA_VERSION,
    CANONICAL_STATE_JSON_SCHEMA_ID,
)


def build_canonical_state_json_schema() -> dict[str, Any]:
    """Return the JSON Schema (draft 2020-12) for a single canonical state frame."""

    # Inline sub-schemas (no $ref) for deterministic emission and simple validation.
    economy_summary = {
        "type": "object",
        "additionalProperties": False,
        "properties": {
            "unit_train_events_total": {"type": "integer", "minimum": 0},
            "structure_train_events_total": {"type": "integer", "minimum": 0},
            "resource_signal_category": {
                "type": ["string", "null"],
                "enum": ["low", "medium", "high", None],
            },
        },
    }
    production_summary = {
        "type": "object",
        "additionalProperties": False,
        "properties": {
            "active_build_queue_count": {"type": "integer", "minimum": 0},
            "tech_upgrades_started_total": {"type": "integer", "minimum": 0},
        },
    }
    army_summary = {
        "type": "object",
        "additionalProperties": False,
        "properties": {
            "army_unit_category_counts": {
                "type": "object",
                "additionalProperties": {"type": "integer", "minimum": 0},
            },
        },
    }
    combat_context = {
        "type": "object",
        "additionalProperties": False,
        "properties": {
            "active_combat_window_ids": {
                "type": "array",
                "items": {"type": "string"},
            },
        },
    }
    scouting_context = {
        "type": "object",
        "additionalProperties": False,
        "properties": {
            "recent_scout_events_count": {"type": "integer", "minimum": 0},
        },
    }
    visibility_context = {
        "type": "object",
        "additionalProperties": False,
        "properties": {
            "visibility_signal_non_truth_disclaimer": {
                "type": "string",
                "const": "starlab.visibility_proxy_not_fog_of_war_truth",
            },
            "visibility_proxy_level": {
                "type": ["string", "null"],
                "enum": ["low", "medium", "high", None],
            },
        },
    }
    player = {
        "type": "object",
        "additionalProperties": False,
        "required": [
            "player_index",
            "race_actual",
            "economy_summary",
            "production_summary",
            "army_summary",
        ],
        "properties": {
            "player_index": {"type": "integer", "minimum": 0},
            "race_actual": {"type": "string", "enum": list(RACE_ACTUAL_VALUES)},
            "result": {"type": "string", "enum": list(RESULT_VALUES)},
            "economy_summary": economy_summary,
            "production_summary": production_summary,
            "army_summary": army_summary,
            "combat_context": combat_context,
            "scouting_context": scouting_context,
            "visibility_context": visibility_context,
        },
    }
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": CANONICAL_STATE_JSON_SCHEMA_ID,
        "title": "STARLAB canonical state frame v1 (M15 profile)",
        "description": (
            "Single replay-derived state frame at one gameloop. Bounded to M09–M14 replay planes; "
            "no extraction pipeline proof."
        ),
        "type": "object",
        "additionalProperties": False,
        "required": [
            "schema_version",
            "frame_kind",
            "source",
            "gameloop",
            "players",
            "global_context",
            "provenance",
        ],
        "properties": {
            "schema_version": {
                "type": "string",
                "const": CANONICAL_STATE_FRAME_SCHEMA_VERSION,
            },
            "frame_kind": {"type": "string", "enum": list(FRAME_KIND_VALUES)},
            "source": {
                "type": "object",
                "additionalProperties": False,
                "properties": {
                    "source_bundle_id": {"type": "string"},
                    "source_lineage_root": {"type": "string"},
                    "source_replay_identity": {"type": "string"},
                },
            },
            "gameloop": {"type": "integer", "minimum": 0},
            "players": {"type": "array", "minItems": 1, "items": player},
            "global_context": {
                "type": "object",
                "additionalProperties": False,
                "properties": {
                    "map_name": {"type": "string"},
                    "active_slice_ids": {
                        "type": "array",
                        "items": {"type": "string"},
                    },
                    "active_combat_window_ids": {
                        "type": "array",
                        "items": {"type": "string"},
                    },
                },
            },
            "provenance": {
                "type": "object",
                "additionalProperties": False,
                "required": [
                    "uses_metadata_plane",
                    "uses_timeline_plane",
                    "uses_build_order_economy_plane",
                    "uses_combat_scouting_visibility_plane",
                    "uses_slice_plane",
                    "uses_replay_bundle_plane",
                ],
                "properties": {
                    "uses_metadata_plane": {"type": "boolean"},
                    "uses_timeline_plane": {"type": "boolean"},
                    "uses_build_order_economy_plane": {"type": "boolean"},
                    "uses_combat_scouting_visibility_plane": {"type": "boolean"},
                    "uses_slice_plane": {"type": "boolean"},
                    "uses_replay_bundle_plane": {"type": "boolean"},
                },
            },
        },
    }


def _schema_types(schema: dict[str, Any]) -> list[str]:
    t = schema.get("type")
    if t is None:
        return []
    return t if isinstance(t, list) else [t]


def _matches_json_type(instance: Any, json_type: str) -> bool:
    if json_type == "null":
        return instance is None
    if json_type == "boolean":
        return isinstance(instance, bool)
    if json_type == "string":
        return isinstance(instance, str)
    if json_type == "integer":
        return isinstance(instance, int) and not isinstance(instance, bool)
    if json_type == "number":
        return isinstance(instance, (int, float)) and not isinstance(instance, bool)
    if json_type == "array":
        return isinstance(instance, list)
    if json_type == "object":
        return isinstance(instance, dict)
    return False


def validate_json_schema_subset(
    instance: Any,
    schema: dict[str, Any],
    path: str = "$",
) -> list[str]:
    """Validate ``instance`` against a **subset** of JSON Schema used by M15 (no $ref)."""

    errors: list[str] = []

    if "const" in schema:
        if instance != schema["const"]:
            errors.append(f"{path}: expected const {schema['const']!r}, got {instance!r}")
        return errors

    if "enum" in schema:
        if instance not in schema["enum"]:
            errors.append(f"{path}: must be one of {schema['enum']!r}")
        return errors

    type_list = _schema_types(schema)
    if type_list:
        if not any(_matches_json_type(instance, t) for t in type_list):
            errors.append(f"{path}: type must be {type_list!r}, got {type(instance).__name__}")
            return errors

    if "object" in type_list and isinstance(instance, dict):
        req = schema.get("required") or []
        for key in req:
            if key not in instance:
                errors.append(f"{path}: missing required property {key!r}")
        props = schema.get("properties") or {}
        extra_keys = set(instance) - set(props)
        ap = schema.get("additionalProperties", True)
        if ap is False and extra_keys:
            errors.append(f"{path}: additional properties not allowed: {sorted(extra_keys)!r}")
        elif isinstance(ap, dict):
            for key in extra_keys:
                errors.extend(
                    validate_json_schema_subset(instance[key], ap, f"{path}.{key}"),
                )
        for key, sub in props.items():
            if key not in instance:
                continue
            errors.extend(validate_json_schema_subset(instance[key], sub, f"{path}.{key}"))
        return errors

    if "array" in type_list and isinstance(instance, list):
        min_items = schema.get("minItems")
        if isinstance(min_items, int) and len(instance) < min_items:
            errors.append(f"{path}: array shorter than minItems {min_items}")
        items_schema = schema.get("items")
        if isinstance(items_schema, dict):
            for i, item in enumerate(instance):
                errors.extend(
                    validate_json_schema_subset(item, items_schema, f"{path}[{i}]"),
                )
        return errors

    if "integer" in type_list and isinstance(instance, int) and not isinstance(instance, bool):
        if "minimum" in schema and instance < schema["minimum"]:
            errors.append(f"{path}: must be >= {schema['minimum']}")
        return errors

    if (
        "number" in type_list
        and isinstance(instance, (int, float))
        and not isinstance(
            instance,
            bool,
        )
    ):
        if "minimum" in schema and instance < schema["minimum"]:
            errors.append(f"{path}: must be >= {schema['minimum']}")
        return errors

    return errors


def validate_canonical_state_frame(instance: Any) -> list[str]:
    """Validate a parsed state frame object against the M15 JSON Schema."""

    schema = build_canonical_state_json_schema()
    return validate_json_schema_subset(instance, schema)
