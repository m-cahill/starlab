"""Load/validate canonical state JSON; write emitted schema artifacts (M15)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from starlab.runs.json_util import canonical_json_dumps, sha256_hex_of_canonical_json
from starlab.state.canonical_state_catalog import (
    NON_CLAIMS_V1,
    OMISSION_RULES_V1,
    OPTIONAL_SECTIONS,
    REQUIRED_PLAYER_FIELDS,
    REQUIRED_TOP_LEVEL_FIELDS,
)
from starlab.state.canonical_state_models import (
    CANONICAL_STATE_CONTRACT,
    CANONICAL_STATE_PROFILE,
    CANONICAL_STATE_SCHEMA_FILENAME,
    CANONICAL_STATE_SCHEMA_REPORT_FILENAME,
)
from starlab.state.canonical_state_schema import (
    build_canonical_state_json_schema,
    validate_canonical_state_frame,
)


def load_json_object(path: Path) -> tuple[dict[str, Any] | None, str | None]:
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        return None, str(exc)
    if not isinstance(raw, dict):
        return None, "JSON root must be an object"
    return raw, None


def build_canonical_state_schema_report(
    *,
    schema_obj: dict[str, Any],
    example_fixture_paths: dict[str, Path] | None = None,
) -> dict[str, Any]:
    """Build ``canonical_state_schema_report.json`` body."""

    schema_sha256 = sha256_hex_of_canonical_json(schema_obj)
    example_fixture_hashes: dict[str, str] = {}
    if example_fixture_paths:
        for label, p in sorted(example_fixture_paths.items()):
            if not p.is_file():
                msg = f"missing fixture for report hash: {p}"
                raise FileNotFoundError(msg)
            raw = json.loads(p.read_text(encoding="utf-8"))
            example_fixture_hashes[label] = sha256_hex_of_canonical_json(raw)

    return {
        "contract": CANONICAL_STATE_CONTRACT,
        "profile": CANONICAL_STATE_PROFILE,
        "schema_sha256": schema_sha256,
        "required_top_level_fields": list(REQUIRED_TOP_LEVEL_FIELDS),
        "required_player_fields": list(REQUIRED_PLAYER_FIELDS),
        "optional_sections": list(OPTIONAL_SECTIONS),
        "omission_rules": list(OMISSION_RULES_V1),
        "non_claims": list(NON_CLAIMS_V1),
        "example_fixture_hashes": example_fixture_hashes,
    }


def write_canonical_state_schema_artifacts(
    output_dir: Path,
    *,
    example_fixture_paths: dict[str, Path] | None = None,
) -> tuple[Path, Path]:
    """Write ``canonical_state_schema.json`` and ``canonical_state_schema_report.json``."""

    output_dir.mkdir(parents=True, exist_ok=True)
    schema_obj = build_canonical_state_json_schema()
    report_obj = build_canonical_state_schema_report(
        schema_obj=schema_obj,
        example_fixture_paths=example_fixture_paths,
    )
    sp = output_dir / CANONICAL_STATE_SCHEMA_FILENAME
    rp = output_dir / CANONICAL_STATE_SCHEMA_REPORT_FILENAME
    sp.write_text(canonical_json_dumps(schema_obj), encoding="utf-8")
    rp.write_text(canonical_json_dumps(report_obj), encoding="utf-8")
    return sp, rp


def validate_canonical_state_file(path: Path) -> list[str]:
    """Load ``path`` and validate against the M15 JSON Schema."""

    obj, err = load_json_object(path)
    if err:
        return [err]
    assert obj is not None
    return validate_canonical_state_frame(obj)
