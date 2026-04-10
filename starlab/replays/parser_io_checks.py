"""Check helpers and small I/O utilities for replay parse pipeline (M08 / M35)."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from starlab._io import load_json_object
from starlab.replays.parser_models import PARSE_CHECK_IDS, CheckResult, CheckSeverity, ParseStatus
from starlab.runs.replay_binding import load_replay_binding


def _sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_replay_opaque(replay_path: Path) -> tuple[str | None, int | None, str | None]:
    """Return ``(sha256_hex, size_bytes, read_error)``."""

    try:
        data = replay_path.read_bytes()
    except OSError as exc:
        return None, None, str(exc)
    return hashlib.sha256(data).hexdigest(), len(data), None


def load_optional_json(path: Path | None) -> tuple[dict[str, Any] | None, str | None]:
    if path is None:
        return None, None
    return load_json_object(path)


def _status_from_adapter_failure(kind: str) -> ParseStatus:
    if kind == "unsupported_protocol":
        return "unsupported_protocol"
    if kind == "parser_unavailable":
        return "parser_unavailable"
    return "parse_failed"


def finalize_checks(checks: list[CheckResult]) -> list[CheckResult]:
    """Emit checks in ``PARSE_CHECK_IDS`` order; fill gaps with ``not_evaluated``."""

    by_id = {c.check_id: c for c in checks}
    out: list[CheckResult] = []
    for cid in PARSE_CHECK_IDS:
        out.append(
            by_id.get(cid)
            or CheckResult(
                check_id=cid,
                detail=None,
                severity="required",
                status="not_evaluated",
            ),
        )
    return out


def _merge_checks(
    *,
    base: list[CheckResult],
    overrides: dict[str, tuple[str, CheckSeverity, str | None]],
) -> list[CheckResult]:
    out: list[CheckResult] = []
    for cid in PARSE_CHECK_IDS:
        if cid in overrides:
            st, sev, det = overrides[cid]
            out.append(CheckResult(check_id=cid, detail=det, severity=sev, status=st))  # type: ignore[arg-type]
        else:
            found = next((c for c in base if c.check_id == cid), None)
            if found is None:
                out.append(
                    CheckResult(
                        check_id=cid,
                        detail=None,
                        severity="required",
                        status="not_evaluated",
                    ),
                )
            else:
                out.append(found)
    return out


def load_optional_replay_binding(path: Path) -> tuple[dict[str, Any] | None, str | None]:
    try:
        return load_replay_binding(path), None
    except (OSError, UnicodeError, ValueError, json.JSONDecodeError) as exc:
        return None, str(exc)


__all__ = [
    "_merge_checks",
    "_sha256_file",
    "_status_from_adapter_failure",
    "finalize_checks",
    "load_optional_json",
    "load_optional_replay_binding",
    "read_replay_opaque",
]
