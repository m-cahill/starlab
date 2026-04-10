"""IO for replay explorer artifacts (M31)."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from starlab.runs.json_util import canonical_json_dumps


def write_replay_explorer_surface(output_dir: Path, surface: dict[str, Any]) -> Path:
    path = output_dir / "replay_explorer_surface.json"
    path.write_text(canonical_json_dumps(surface), encoding="utf-8")
    return path


def write_replay_explorer_report(output_dir: Path, report: dict[str, Any]) -> Path:
    path = output_dir / "replay_explorer_surface_report.json"
    path.write_text(canonical_json_dumps(report), encoding="utf-8")
    return path
