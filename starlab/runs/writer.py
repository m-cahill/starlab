"""Deterministic JSON writers for M03 run artifacts."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from starlab.runs.json_util import canonical_json_dumps


def write_json_record(path: Path, record: dict[str, Any]) -> None:
    """Write canonical JSON with trailing newline."""

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(canonical_json_dumps(record), encoding="utf-8")


def run_identity_to_json(record: dict[str, Any]) -> str:
    """Serialize run identity mapping (sorted keys)."""

    return canonical_json_dumps(record)


def lineage_seed_to_json(record: dict[str, Any]) -> str:
    """Serialize lineage seed mapping (sorted keys)."""

    return canonical_json_dumps(record)
