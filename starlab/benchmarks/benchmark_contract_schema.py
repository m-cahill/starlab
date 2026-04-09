"""JSON Schema for benchmark contract document v1 (M20).

Validation via jsonschema (Draft 2020-12).
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator
from jsonschema.exceptions import ValidationError

from starlab.benchmarks.benchmark_contract_models import (
    AGGREGATION_METHOD_VALUES,
    AGGREGATION_POLICY_KIND_VALUES,
    BENCHMARK_CONTRACT_DOCUMENT_SCHEMA_VERSION,
    BENCHMARK_CONTRACT_JSON_SCHEMA_ID,
    COMPARABILITY_STATUS_VALUES,
    EVALUATION_POSTURE_VALUES,
    GATING_RULE_SEVERITY_VALUES,
    MEASUREMENT_SURFACE_VALUES,
    OPTIMIZATION_DIRECTION_VALUES,
    SCORING_ROLE_VALUES,
    SCORING_STATUS_VALUES,
    SUBJECT_KINDS_ALLOWED_VALUES,
)
from starlab.runs.json_util import sha256_hex_of_canonical_json


def build_benchmark_contract_json_schema() -> dict[str, Any]:
    """Return the JSON Schema (draft 2020-12) for one benchmark contract document."""

    metric_definition = {
        "type": "object",
        "additionalProperties": False,
        "required": [
            "metric_id",
            "display_name",
            "unit",
            "optimization_direction",
            "aggregation_method",
            "scoring_role",
        ],
        "properties": {
            "metric_id": {"type": "string", "minLength": 1},
            "display_name": {"type": "string", "minLength": 1},
            "unit": {"type": "string", "minLength": 1},
            "optimization_direction": {
                "type": "string",
                "enum": list(OPTIMIZATION_DIRECTION_VALUES),
            },
            "aggregation_method": {"type": "string", "enum": list(AGGREGATION_METHOD_VALUES)},
            "scoring_role": {"type": "string", "enum": list(SCORING_ROLE_VALUES)},
        },
    }

    gating_rule = {
        "type": "object",
        "additionalProperties": False,
        "required": ["rule_id", "description", "severity"],
        "properties": {
            "rule_id": {"type": "string", "minLength": 1},
            "description": {"type": "string", "minLength": 1},
            "severity": {"type": "string", "enum": list(GATING_RULE_SEVERITY_VALUES)},
        },
    }

    input_requirements = {
        "type": "object",
        "additionalProperties": False,
        "required": ["required_inputs"],
        "properties": {
            "required_inputs": {
                "type": "array",
                "items": {"type": "string", "minLength": 1},
            },
            "notes": {"type": ["string", "null"]},
        },
    }

    aggregation_policy = {
        "type": "object",
        "additionalProperties": False,
        "required": ["policy_kind"],
        "properties": {
            "policy_kind": {"type": "string", "enum": list(AGGREGATION_POLICY_KIND_VALUES)},
            "notes": {"type": ["string", "null"]},
        },
    }

    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": BENCHMARK_CONTRACT_JSON_SCHEMA_ID,
        "title": "STARLAB benchmark contract v1 (M20 profile)",
        "description": (
            "One benchmark definition document. Schema + validation only; does not assert "
            "benchmark integrity or replay equivalence."
        ),
        "type": "object",
        "additionalProperties": False,
        "required": [
            "schema_version",
            "benchmark_id",
            "benchmark_version",
            "benchmark_name",
            "subject_kinds_allowed",
            "measurement_surface",
            "input_requirements",
            "metric_definitions",
            "gating_rules",
            "aggregation_policy",
            "scorecard_schema_ref",
            "non_claims",
        ],
        "properties": {
            "schema_version": {
                "type": "string",
                "const": BENCHMARK_CONTRACT_DOCUMENT_SCHEMA_VERSION,
            },
            "benchmark_id": {"type": "string", "minLength": 1},
            "benchmark_version": {"type": "string", "minLength": 1},
            "benchmark_name": {"type": "string", "minLength": 1},
            "subject_kinds_allowed": {
                "type": "array",
                "minItems": 1,
                "uniqueItems": True,
                "items": {"type": "string", "enum": list(SUBJECT_KINDS_ALLOWED_VALUES)},
            },
            "measurement_surface": {
                "type": "string",
                "enum": list(MEASUREMENT_SURFACE_VALUES),
            },
            "input_requirements": input_requirements,
            "metric_definitions": {
                "type": "array",
                "minItems": 1,
                "items": metric_definition,
            },
            "gating_rules": {
                "type": "array",
                "items": gating_rule,
            },
            "aggregation_policy": aggregation_policy,
            "scorecard_schema_ref": {"type": "string", "minLength": 1},
            "non_claims": {
                "type": "array",
                "items": {"type": "string", "minLength": 1},
                "uniqueItems": True,
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


def _is_sorted_lex(strings: list[str]) -> bool:
    return strings == sorted(strings)


def validate_benchmark_contract(instance: Any) -> list[str]:
    """Validate a benchmark contract object against the M20 JSON Schema and ordering rules."""

    schema = build_benchmark_contract_json_schema()
    validator = Draft202012Validator(schema)
    errors = [_format_validation_error(e) for e in validator.iter_errors(instance)]
    if errors:
        return sorted(errors)

    assert isinstance(instance, dict)
    nc = instance.get("non_claims")
    if isinstance(nc, list) and all(isinstance(x, str) for x in nc):
        if not _is_sorted_lex(list(nc)):
            return ["non_claims: must be sorted lexicographically"]

    return []


def build_benchmark_contract_schema_report(
    *,
    schema_obj: dict[str, Any],
    example_fixture_paths: dict[str, Path] | None = None,
) -> dict[str, Any]:
    """Build ``benchmark_contract_schema_report.json`` body."""

    from starlab.benchmarks.benchmark_contract_models import (
        BENCHMARK_CONTRACT_CONTRACT,
        BENCHMARK_CONTRACT_PROFILE,
        BENCHMARK_CONTRACT_REPORT_NON_CLAIMS_V1,
        ORDERED_BENCHMARK_CONTRACT_TOP_LEVEL_KEYS,
    )

    schema_sha256 = sha256_hex_of_canonical_json(schema_obj)
    example_fixture_hashes: dict[str, str] = {}
    if example_fixture_paths:
        for label, p in sorted(example_fixture_paths.items()):
            if not p.is_file():
                msg = f"missing fixture for report hash: {p}"
                raise FileNotFoundError(msg)
            raw_obj: Any = json.loads(p.read_text(encoding="utf-8"))
            example_fixture_hashes[label] = sha256_hex_of_canonical_json(raw_obj)

    return {
        "contract": BENCHMARK_CONTRACT_CONTRACT,
        "profile": BENCHMARK_CONTRACT_PROFILE,
        "schema_sha256": schema_sha256,
        "schema_id": schema_obj.get("$id", ""),
        "deterministic_key_order_benchmark_instance": list(
            ORDERED_BENCHMARK_CONTRACT_TOP_LEVEL_KEYS,
        ),
        "vocabularies": {
            "comparability_status": list(COMPARABILITY_STATUS_VALUES),
            "evaluation_posture": list(EVALUATION_POSTURE_VALUES),
            "measurement_surface": list(MEASUREMENT_SURFACE_VALUES),
            "scoring_status": list(SCORING_STATUS_VALUES),
            "subject_kinds_allowed": list(SUBJECT_KINDS_ALLOWED_VALUES),
        },
        "non_claims": list(BENCHMARK_CONTRACT_REPORT_NON_CLAIMS_V1),
        "example_fixture_hashes": example_fixture_hashes,
    }
