"""Load/validate observation JSON; write emitted schema artifacts (M17)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from starlab._io import load_json_object
from starlab.observation.observation_surface_catalog import (
    ACTION_MASK_FAMILY_NAMES,
    NON_CLAIMS_V1,
    ORDERED_SCALAR_FEATURE_NAMES,
    UPSTREAM_LINEAGE_NOTES_V1,
)
from starlab.observation.observation_surface_models import (
    OBSERVATION_SURFACE_CONTRACT,
    OBSERVATION_SURFACE_PROFILE,
    OBSERVATION_SURFACE_REPORT_VERSION,
    OBSERVATION_SURFACE_SCHEMA_FILENAME,
    OBSERVATION_SURFACE_SCHEMA_REPORT_FILENAME,
)
from starlab.observation.observation_surface_schema import (
    build_observation_surface_json_schema,
    validate_observation_surface_frame,
)
from starlab.runs.json_util import canonical_json_dumps, sha256_hex_of_canonical_json


def build_observation_surface_schema_report(
    *,
    schema_obj: dict[str, Any],
    example_fixture_paths: dict[str, Path] | None = None,
) -> dict[str, Any]:
    """Build ``observation_surface_schema_report.json`` body."""

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
        "report_version": OBSERVATION_SURFACE_REPORT_VERSION,
        "contract": OBSERVATION_SURFACE_CONTRACT,
        "profile": OBSERVATION_SURFACE_PROFILE,
        "schema_sha256": schema_sha256,
        "ordered_scalar_feature_names": list(ORDERED_SCALAR_FEATURE_NAMES),
        "action_mask_family_names": list(ACTION_MASK_FAMILY_NAMES),
        "feature_families_summary": (
            "metadata; viewpoint; scalar_features (ordered); entity_rows; "
            "spatial_plane_family (structural shapes); action_mask_families (family-level masks)."
        ),
        "upstream_lineage_notes": list(UPSTREAM_LINEAGE_NOTES_V1),
        "non_claims": list(NON_CLAIMS_V1),
        "example_fixture_hashes": example_fixture_hashes,
    }


def write_observation_surface_schema_artifacts(
    output_dir: Path,
    *,
    example_fixture_paths: dict[str, Path] | None = None,
) -> tuple[Path, Path]:
    """Write ``observation_surface_schema.json`` and ``observation_surface_schema_report.json``."""

    output_dir.mkdir(parents=True, exist_ok=True)
    schema_obj = build_observation_surface_json_schema()
    report_obj = build_observation_surface_schema_report(
        schema_obj=schema_obj,
        example_fixture_paths=example_fixture_paths,
    )
    sp = output_dir / OBSERVATION_SURFACE_SCHEMA_FILENAME
    rp = output_dir / OBSERVATION_SURFACE_SCHEMA_REPORT_FILENAME
    sp.write_text(canonical_json_dumps(schema_obj), encoding="utf-8")
    rp.write_text(canonical_json_dumps(report_obj), encoding="utf-8")
    return sp, rp


def validate_observation_surface_file(path: Path) -> list[str]:
    """Load ``path`` and validate against the M17 JSON Schema."""

    obj, err = load_json_object(path)
    if err:
        return [err]
    assert obj is not None
    return validate_observation_surface_frame(obj)
