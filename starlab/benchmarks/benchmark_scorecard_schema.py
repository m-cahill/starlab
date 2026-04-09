"""JSON Schema for benchmark scorecard document v1 (M20).

Validation via jsonschema (Draft 2020-12).
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator
from jsonschema.exceptions import ValidationError

from starlab.benchmarks.benchmark_contract_models import (
    BENCHMARK_SCORECARD_DOCUMENT_SCHEMA_VERSION,
    BENCHMARK_SCORECARD_JSON_SCHEMA_ID,
    COMPARABILITY_STATUS_VALUES,
    EVALUATION_POSTURE_VALUES,
    SCORING_STATUS_VALUES,
    SUBJECT_KINDS_ALLOWED_VALUES,
)
from starlab.runs.json_util import sha256_hex_of_canonical_json


def build_benchmark_scorecard_json_schema() -> dict[str, Any]:
    """Return the JSON Schema (draft 2020-12) for one benchmark scorecard document."""

    subject_ref = {
        "type": "object",
        "additionalProperties": False,
        "required": ["subject_kind", "subject_id"],
        "properties": {
            "subject_kind": {"type": "string", "enum": list(SUBJECT_KINDS_ALLOWED_VALUES)},
            "subject_id": {"type": "string", "minLength": 1},
        },
    }

    metric_row = {
        "type": "object",
        "additionalProperties": False,
        "required": ["metric_id", "value", "unit"],
        "properties": {
            "metric_id": {"type": "string", "minLength": 1},
            "value": {"type": ["number", "null"]},
            "unit": {"type": "string", "minLength": 1},
        },
    }

    aggregate_score = {
        "type": "object",
        "additionalProperties": False,
        "required": ["aggregate_id", "value", "unit"],
        "properties": {
            "aggregate_id": {"type": "string", "minLength": 1},
            "value": {"type": ["number", "null"]},
            "unit": {"type": "string", "minLength": 1},
        },
    }

    gating_outcome = {
        "type": "object",
        "additionalProperties": False,
        "required": ["rule_id", "passed"],
        "properties": {
            "rule_id": {"type": "string", "minLength": 1},
            "passed": {"type": "boolean"},
            "detail": {"type": ["string", "null"]},
        },
    }

    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": BENCHMARK_SCORECARD_JSON_SCHEMA_ID,
        "title": "STARLAB benchmark scorecard v1 (M20 profile)",
        "description": (
            "One benchmark result / scorecard surface. Schema + validation only; does not assert "
            "benchmark integrity, comparability truth, or run validity."
        ),
        "type": "object",
        "additionalProperties": False,
        "required": [
            "schema_version",
            "benchmark_id",
            "benchmark_version",
            "benchmark_contract_sha256",
            "subject_ref",
            "evaluation_posture",
            "scoring_status",
            "comparability_status",
            "metric_rows",
            "aggregate_scores",
            "gating_outcomes",
            "warnings",
            "non_claims",
        ],
        "properties": {
            "schema_version": {
                "type": "string",
                "const": BENCHMARK_SCORECARD_DOCUMENT_SCHEMA_VERSION,
            },
            "benchmark_id": {"type": "string", "minLength": 1},
            "benchmark_version": {"type": "string", "minLength": 1},
            "benchmark_contract_sha256": {
                "type": "string",
                "pattern": "^[0-9a-f]{64}$",
            },
            "subject_ref": subject_ref,
            "evaluation_posture": {"type": "string", "enum": list(EVALUATION_POSTURE_VALUES)},
            "scoring_status": {"type": "string", "enum": list(SCORING_STATUS_VALUES)},
            "comparability_status": {
                "type": "string",
                "enum": list(COMPARABILITY_STATUS_VALUES),
            },
            "metric_rows": {
                "type": "array",
                "items": metric_row,
            },
            "aggregate_scores": {
                "type": "array",
                "items": aggregate_score,
            },
            "gating_outcomes": {
                "type": "array",
                "items": gating_outcome,
            },
            "warnings": {
                "type": "array",
                "items": {"type": "string", "minLength": 1},
            },
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


def validate_benchmark_scorecard(instance: Any) -> list[str]:
    """Validate a scorecard object against the M20 JSON Schema and ordering rules."""

    schema = build_benchmark_scorecard_json_schema()
    validator = Draft202012Validator(schema)
    errors = [_format_validation_error(e) for e in validator.iter_errors(instance)]
    if errors:
        return sorted(errors)

    assert isinstance(instance, dict)
    for key in ("warnings", "non_claims"):
        seq = instance.get(key)
        if isinstance(seq, list) and all(isinstance(x, str) for x in seq):
            if not _is_sorted_lex(list(seq)):
                return [f"{key}: must be sorted lexicographically"]

    return []


def build_benchmark_scorecard_schema_report(
    *,
    schema_obj: dict[str, Any],
    example_fixture_paths: dict[str, Path] | None = None,
) -> dict[str, Any]:
    """Build ``benchmark_scorecard_schema_report.json`` body."""

    from starlab.benchmarks.benchmark_contract_models import (
        BENCHMARK_SCORECARD_CONTRACT,
        BENCHMARK_SCORECARD_PROFILE,
        BENCHMARK_SCORECARD_REPORT_NON_CLAIMS_V1,
        ORDERED_SCORECARD_TOP_LEVEL_KEYS,
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
        "contract": BENCHMARK_SCORECARD_CONTRACT,
        "profile": BENCHMARK_SCORECARD_PROFILE,
        "schema_sha256": schema_sha256,
        "schema_id": schema_obj.get("$id", ""),
        "deterministic_key_order_scorecard_instance": list(ORDERED_SCORECARD_TOP_LEVEL_KEYS),
        "vocabularies": {
            "comparability_status": list(COMPARABILITY_STATUS_VALUES),
            "evaluation_posture": list(EVALUATION_POSTURE_VALUES),
            "scoring_status": list(SCORING_STATUS_VALUES),
        },
        "non_claims": list(BENCHMARK_SCORECARD_REPORT_NON_CLAIMS_V1),
        "example_fixture_hashes": example_fixture_hashes,
    }
