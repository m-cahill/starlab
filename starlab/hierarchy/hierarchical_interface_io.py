"""Emit hierarchical agent interface JSON Schema + report artifacts (M29)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from starlab.hierarchy.hierarchical_interface_models import (
    COARSE_SEMANTIC_LABEL_ENUM,
    COARSE_SEMANTIC_LABEL_POLICY_ID,
    HIERARCHICAL_AGENT_INTERFACE_CONTRACT,
    HIERARCHICAL_AGENT_INTERFACE_PROFILE,
    HIERARCHICAL_AGENT_INTERFACE_SCHEMA_FILENAME,
    HIERARCHICAL_AGENT_INTERFACE_SCHEMA_REPORT_FILENAME,
    HIERARCHICAL_AGENT_INTERFACE_SCHEMA_REPORT_VERSION,
    NON_CLAIMS_V1,
)
from starlab.hierarchy.hierarchical_interface_schema import (
    build_hierarchical_agent_interface_json_schema,
)
from starlab.runs.json_util import canonical_json_dumps, sha256_hex_of_canonical_json


def build_hierarchical_agent_interface_schema_report(
    *,
    schema_obj: dict[str, Any],
    example_fixture_paths: dict[str, Path] | None = None,
) -> dict[str, Any]:
    """Build ``hierarchical_agent_interface_schema_report.json`` body."""

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
        "report_version": HIERARCHICAL_AGENT_INTERFACE_SCHEMA_REPORT_VERSION,
        "contract": HIERARCHICAL_AGENT_INTERFACE_CONTRACT,
        "profile": HIERARCHICAL_AGENT_INTERFACE_PROFILE,
        "schema_sha256": schema_sha256,
        "coarse_semantic_label_policy_id": COARSE_SEMANTIC_LABEL_POLICY_ID,
        "coarse_semantic_label_enum": list(COARSE_SEMANTIC_LABEL_ENUM),
        "non_claims": list(NON_CLAIMS_V1),
        "example_fixture_hashes": example_fixture_hashes,
    }


def write_hierarchical_agent_interface_schema_artifacts(
    output_dir: Path,
    *,
    example_fixture_paths: dict[str, Path] | None = None,
) -> tuple[Path, Path]:
    """Write schema + report JSON under ``output_dir``."""

    output_dir.mkdir(parents=True, exist_ok=True)
    schema_obj = build_hierarchical_agent_interface_json_schema()
    report_obj = build_hierarchical_agent_interface_schema_report(
        schema_obj=schema_obj,
        example_fixture_paths=example_fixture_paths,
    )
    sp = output_dir / HIERARCHICAL_AGENT_INTERFACE_SCHEMA_FILENAME
    rp = output_dir / HIERARCHICAL_AGENT_INTERFACE_SCHEMA_REPORT_FILENAME
    sp.write_text(canonical_json_dumps(schema_obj), encoding="utf-8")
    rp.write_text(canonical_json_dumps(report_obj), encoding="utf-8")
    return sp, rp
