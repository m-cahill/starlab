"""Load M16 canonical state JSON and optional pipeline report for M18 materialization."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from starlab.runs.json_util import sha256_hex_of_canonical_json


def load_json_object(path: Path) -> tuple[dict[str, Any] | None, str | None]:
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        return None, str(exc)
    if not isinstance(raw, dict):
        return None, "JSON root must be an object"
    return raw, None


def load_canonical_state(path: Path) -> tuple[dict[str, Any] | None, str | None]:
    """Load ``canonical_state.json`` (M16)."""

    return load_json_object(path)


def load_canonical_state_report(path: Path) -> tuple[dict[str, Any] | None, str | None]:
    """Load ``canonical_state_report.json`` (M16 pipeline report)."""

    return load_json_object(path)


def canonical_state_sha256(state: dict[str, Any]) -> str:
    """SHA-256 (hex) of canonical JSON for ``state`` (no trailing newline)."""

    return sha256_hex_of_canonical_json(state)


def provenance_report_matches_state(
    *,
    state: dict[str, Any],
    report: dict[str, Any],
) -> str | None:
    """Return an error string if ``report``'s state hash disagrees with ``state``; else ``None``."""

    reported = report.get("canonical_state_sha256")
    if not isinstance(reported, str) or len(reported) != 64:
        return (
            "canonical_state_report.json: canonical_state_sha256 missing "
            "or not a 64-char hex string"
        )
    got = canonical_state_sha256(state).lower()
    if got != reported.lower():
        return (
            "canonical state hash mismatch: recomputed from canonical_state.json vs "
            "canonical_state_report.json canonical_state_sha256"
        )
    return None
