"""Write learned-agent comparison JSON artifacts (M42)."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from starlab.evaluation.learned_agent_comparison_models import (
    LEARNED_AGENT_COMPARISON_FILENAME,
    LEARNED_AGENT_COMPARISON_REPORT_FILENAME,
)
from starlab.runs.json_util import canonical_json_dumps, sha256_hex_of_canonical_json


def seal_comparison_body(body_without_id: dict[str, Any]) -> dict[str, Any]:
    """Attach deterministic ``comparison_id`` (SHA-256 of canonical JSON without that field)."""

    digest = sha256_hex_of_canonical_json(body_without_id)
    return {**body_without_id, "comparison_id": digest}


def write_learned_agent_comparison_artifacts(
    *,
    comparison_body: dict[str, Any],
    report_body: dict[str, Any],
    output_dir: Path,
) -> tuple[Path, Path]:
    """Write ``learned_agent_comparison.json`` + report under ``output_dir``."""

    output_dir.mkdir(parents=True, exist_ok=True)
    cp = output_dir / LEARNED_AGENT_COMPARISON_FILENAME
    rp = output_dir / LEARNED_AGENT_COMPARISON_REPORT_FILENAME
    cp.write_text(canonical_json_dumps(comparison_body), encoding="utf-8")
    rp.write_text(canonical_json_dumps(report_body), encoding="utf-8")
    return cp, rp
