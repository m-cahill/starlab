"""JSON Schema for observation surface frame v1 (M17); validation via jsonschema (Draft 2020-12)."""

from __future__ import annotations

from typing import Any

from jsonschema import Draft202012Validator
from jsonschema.exceptions import ValidationError

from starlab.observation.observation_surface_catalog import (
    ACTION_MASK_FAMILY_NAMES,
    COORDINATE_FRAME_VALUES,
    ORDERED_SCALAR_FEATURE_NAMES,
    OWNER_VIEW_VALUES,
    ROW_KIND_VALUES,
    VISIBILITY_POLICY_VALUES,
)
from starlab.observation.observation_surface_models import (
    OBSERVATION_FRAME_SCHEMA_VERSION,
    OBSERVATION_SURFACE_CONTRACT,
    OBSERVATION_SURFACE_JSON_SCHEMA_ID,
)


def _scalar_entry_schema(name: str) -> dict[str, Any]:
    return {
        "type": "object",
        "additionalProperties": False,
        "required": ["name", "value"],
        "properties": {
            "name": {"type": "string", "const": name},
            "value": {
                "type": ["string", "number", "boolean", "null"],
            },
        },
    }


def _action_family_schema(family_name: str) -> dict[str, Any]:
    return {
        "type": "object",
        "additionalProperties": False,
        "required": ["family_name", "ordered_mask_values"],
        "properties": {
            "family_name": {"type": "string", "const": family_name},
            "ordered_mask_values": {
                "type": "array",
                "minItems": 1,
                "items": {"type": "integer", "enum": [0, 1]},
            },
        },
    }


def build_observation_surface_json_schema() -> dict[str, Any]:
    """Return the JSON Schema (draft 2020-12) for a single observation frame."""

    metadata_props: dict[str, Any] = {
        "observation_contract_version": {"type": "string", "const": "1"},
        "source_canonical_state_sha256": {
            "type": "string",
            "pattern": "^[0-9a-f]{64}$",
        },
        "gameloop": {"type": "integer", "minimum": 0},
        "perspective_player_index": {"type": "integer", "minimum": 0},
        "source_bundle_id": {"type": "string"},
        "source_lineage_root": {"type": "string"},
        "source_replay_identity": {"type": "string"},
    }
    metadata_required = [
        "observation_contract_version",
        "source_canonical_state_sha256",
        "gameloop",
        "perspective_player_index",
    ]

    position_schema: dict[str, Any] = {
        "type": "object",
        "additionalProperties": False,
        "properties": {
            "x": {"type": ["number", "null"]},
            "y": {"type": ["number", "null"]},
        },
    }

    entity_row = {
        "type": "object",
        "additionalProperties": False,
        "required": ["row_kind", "owner_view", "category"],
        "properties": {
            "row_kind": {"type": "string", "enum": list(ROW_KIND_VALUES)},
            "owner_view": {"type": "string", "enum": list(OWNER_VIEW_VALUES)},
            "category": {"type": "string"},
            "count": {"type": "integer", "minimum": 0},
            "position": {"oneOf": [{"type": "null"}, position_schema]},
            "health": {"type": ["number", "null"]},
            "shield": {"type": ["number", "null"]},
            "energy": {"type": ["number", "null"]},
            "unit_tag": {"type": ["string", "null"]},
            "is_visible": {"type": ["boolean", "null"]},
        },
    }

    plane = {
        "type": "object",
        "additionalProperties": False,
        "required": [
            "plane_id",
            "grid_height",
            "grid_width",
            "channel_count",
            "channel_order",
        ],
        "properties": {
            "plane_id": {"type": "string", "minLength": 1},
            "grid_height": {"type": "integer", "minimum": 0},
            "grid_width": {"type": "integer", "minimum": 0},
            "channel_count": {"type": "integer", "minimum": 0},
            "channel_order": {
                "type": "array",
                "items": {"type": "string"},
            },
            "coordinate_frame": {
                "type": "string",
                "enum": list(COORDINATE_FRAME_VALUES),
            },
        },
    }

    scalar_prefix = [_scalar_entry_schema(n) for n in ORDERED_SCALAR_FEATURE_NAMES]
    family_prefix = [_action_family_schema(n) for n in ACTION_MASK_FAMILY_NAMES]

    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": OBSERVATION_SURFACE_JSON_SCHEMA_ID,
        "title": "STARLAB observation surface frame v1 (M17 profile)",
        "description": (
            "Single player-relative observation frame at one gameloop; "
            "upstream: M16 canonical state. Contract-only — no materialization proof."
        ),
        "type": "object",
        "additionalProperties": False,
        "required": [
            "schema_version",
            "contract_id",
            "metadata",
            "viewpoint",
            "scalar_features",
            "entity_rows",
            "spatial_plane_family",
            "action_mask_families",
        ],
        "properties": {
            "schema_version": {
                "type": "string",
                "const": OBSERVATION_FRAME_SCHEMA_VERSION,
            },
            "contract_id": {
                "type": "string",
                "const": OBSERVATION_SURFACE_CONTRACT,
            },
            "metadata": {
                "type": "object",
                "additionalProperties": False,
                "required": metadata_required,
                "properties": metadata_props,
            },
            "viewpoint": {
                "type": "object",
                "additionalProperties": False,
                "required": [
                    "player_index",
                    "visibility_policy",
                    "single_player_relative_viewpoint",
                ],
                "properties": {
                    "player_index": {"type": "integer", "minimum": 0},
                    "visibility_policy": {
                        "type": "string",
                        "enum": list(VISIBILITY_POLICY_VALUES),
                    },
                    "single_player_relative_viewpoint": {"type": "boolean", "const": True},
                },
            },
            "scalar_features": {
                "type": "object",
                "additionalProperties": False,
                "required": ["ordered_entries"],
                "properties": {
                    "ordered_entries": {
                        "type": "array",
                        "minItems": len(ORDERED_SCALAR_FEATURE_NAMES),
                        "maxItems": len(ORDERED_SCALAR_FEATURE_NAMES),
                        "prefixItems": scalar_prefix,
                        "items": False,
                    },
                },
            },
            "entity_rows": {
                "type": "object",
                "additionalProperties": False,
                "required": ["rows"],
                "properties": {
                    "rows": {
                        "type": "array",
                        "items": entity_row,
                    },
                },
            },
            "spatial_plane_family": {
                "type": "object",
                "additionalProperties": False,
                "required": ["planes"],
                "properties": {
                    "planes": {
                        "type": "array",
                        "items": plane,
                    },
                },
            },
            "action_mask_families": {
                "type": "object",
                "additionalProperties": False,
                "required": ["families"],
                "properties": {
                    "families": {
                        "type": "array",
                        "minItems": len(ACTION_MASK_FAMILY_NAMES),
                        "maxItems": len(ACTION_MASK_FAMILY_NAMES),
                        "prefixItems": family_prefix,
                        "items": False,
                    },
                },
            },
        },
    }


def _instance_location(err: ValidationError) -> str:
    parts = [str(p) for p in err.absolute_path]
    if not parts:
        return "$"
    return "$." + ".".join(parts)


def _format_validation_error(err: ValidationError) -> str:
    return f"{_instance_location(err)}: {err.message}"


def validate_observation_surface_frame(instance: Any) -> list[str]:
    """Validate a parsed observation frame object against the M17 JSON Schema."""

    schema = build_observation_surface_json_schema()
    validator = Draft202012Validator(schema)
    errors = [_format_validation_error(e) for e in validator.iter_errors(instance)]
    return sorted(errors)
