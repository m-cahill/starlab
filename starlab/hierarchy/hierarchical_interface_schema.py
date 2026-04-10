"""JSON Schema for hierarchical agent interface trace documents (M29)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

from starlab.hierarchy.hierarchical_interface_models import (
    COARSE_SEMANTIC_LABEL_ENUM,
    COARSE_SEMANTIC_LABEL_POLICY_ID,
    DELEGATE_ROLE_ENUM,
    HIERARCHICAL_AGENT_INTERFACE_JSON_SCHEMA_ID,
    TRACE_DOCUMENT_SCHEMA_VERSION,
)


def build_hierarchical_agent_interface_json_schema() -> dict[str, Any]:
    """Return the JSON Schema (draft 2020-12) for one trace document."""

    frame_ref = {
        "type": "object",
        "additionalProperties": False,
        "required": [
            "bundle_id",
            "lineage_root",
            "gameloop",
            "perspective_player_index",
        ],
        "properties": {
            "bundle_id": {"type": "string", "minLength": 1},
            "lineage_root": {"type": "string", "minLength": 1},
            "gameloop": {"type": "integer", "minimum": 0},
            "perspective_player_index": {"type": "integer", "minimum": 0},
        },
    }

    delegate_descriptor = {
        "type": "object",
        "additionalProperties": False,
        "required": ["delegate_id", "delegate_role"],
        "properties": {
            "delegate_id": {"type": "string", "minLength": 1},
            "delegate_role": {"type": "string", "enum": list(DELEGATE_ROLE_ENUM)},
        },
    }

    manager_request = {
        "type": "object",
        "additionalProperties": False,
        "required": ["frame_ref", "delegates_catalog"],
        "properties": {
            "frame_ref": {"$ref": "#/$defs/frame_ref"},
            "delegates_catalog": {
                "type": "array",
                "minItems": 1,
                "items": {"$ref": "#/$defs/delegate_descriptor"},
            },
        },
    }

    manager_response = {
        "type": "object",
        "additionalProperties": False,
        "required": ["selected_delegate_id"],
        "properties": {
            "selected_delegate_id": {"type": "string", "minLength": 1},
            "directive_kind": {"type": "string", "minLength": 1, "maxLength": 64},
            "option_id": {"type": "string", "minLength": 1, "maxLength": 64},
        },
    }

    worker_request = {
        "type": "object",
        "additionalProperties": False,
        "required": ["frame_ref", "manager_response", "delegate"],
        "properties": {
            "frame_ref": {"$ref": "#/$defs/frame_ref"},
            "manager_response": {"$ref": "#/$defs/manager_response"},
            "delegate": {"$ref": "#/$defs/delegate_descriptor"},
        },
    }

    worker_response = {
        "type": "object",
        "additionalProperties": False,
        "required": ["label_policy_id", "semantic_coarse_label"],
        "properties": {
            "label_policy_id": {"type": "string", "const": COARSE_SEMANTIC_LABEL_POLICY_ID},
            "semantic_coarse_label": {
                "type": "string",
                "enum": list(COARSE_SEMANTIC_LABEL_ENUM),
            },
            "confidence": {"type": "number", "minimum": 0.0, "maximum": 1.0},
        },
    }

    hierarchical_decision_trace = {
        "type": "object",
        "additionalProperties": False,
        "required": [
            "manager_request",
            "manager_response",
            "worker_request",
            "worker_response",
        ],
        "properties": {
            "manager_request": {"$ref": "#/$defs/manager_request"},
            "manager_response": {"$ref": "#/$defs/manager_response"},
            "worker_request": {"$ref": "#/$defs/worker_request"},
            "worker_response": {"$ref": "#/$defs/worker_response"},
        },
    }

    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": HIERARCHICAL_AGENT_INTERFACE_JSON_SCHEMA_ID,
        "title": "STARLAB hierarchical agent interface trace v1 (M29)",
        "description": (
            "Offline, frame-scoped two-level hierarchy (manager routing + worker semantic label). "
            "Does not assert live SC2 actions, benchmark integrity, or learned policies."
        ),
        "type": "object",
        "additionalProperties": False,
        "required": ["schema_version", "hierarchical_decision_trace"],
        "properties": {
            "schema_version": {"type": "string", "const": TRACE_DOCUMENT_SCHEMA_VERSION},
            "hierarchical_decision_trace": {"$ref": "#/$defs/hierarchical_decision_trace"},
        },
        "$defs": {
            "frame_ref": frame_ref,
            "delegate_descriptor": delegate_descriptor,
            "manager_request": manager_request,
            "manager_response": manager_response,
            "worker_request": worker_request,
            "worker_response": worker_response,
            "hierarchical_decision_trace": hierarchical_decision_trace,
        },
    }


def validate_hierarchical_trace_document(obj: dict[str, Any]) -> list[str]:
    """Validate ``obj`` against the M29 JSON Schema; return human-readable issues."""

    schema = build_hierarchical_agent_interface_json_schema()
    validator = Draft202012Validator(schema)
    errors: list[str] = []
    for err in validator.iter_errors(obj):
        errors.append(f"{err.json_path}: {err.message}")
    return errors


def validate_hierarchical_trace_file(path: Path) -> list[str]:
    """Load JSON from ``path`` and validate; return issues (empty if valid)."""

    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        return [str(exc)]
    if not isinstance(raw, dict):
        return ["JSON root must be an object"]
    return validate_hierarchical_trace_document(raw)


def assert_valid_hierarchical_trace_document(obj: dict[str, Any]) -> None:
    """Raise ``ValueError`` if validation fails."""

    errs = validate_hierarchical_trace_document(obj)
    if errs:
        msg = "; ".join(errs)
        raise ValueError(msg)


