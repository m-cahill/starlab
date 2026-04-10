"""Shared JSON object loading for STARLAB file-boundary I/O (M34 / DIR-003).

This module is internal; it is not a general data-access layer. Call sites that
need raise-on-error semantics should wrap :func:`load_json_object` or
:func:`parse_json_object_text` locally without duplicating parse logic.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

JSON_ROOT_MUST_BE_OBJECT = "JSON root must be an object"


def parse_json_object_text(raw: str) -> tuple[dict[str, Any] | None, str | None]:
    """Parse UTF-8 text as a single JSON object.

    Returns ``(dict, None)`` on success, or ``(None, error_message)`` on failure.
    """

    try:
        obj: Any = json.loads(raw)
    except json.JSONDecodeError as exc:
        return None, str(exc)
    if not isinstance(obj, dict):
        return None, JSON_ROOT_MUST_BE_OBJECT
    return obj, None


def load_json_object(path: Path) -> tuple[dict[str, Any] | None, str | None]:
    """Read ``path`` and parse its contents as a single JSON object.

    Returns ``(dict, None)`` on success, or ``(None, error_message)`` on failure.
    Read errors, decode errors, and non-object JSON roots are reported via the
    error string (same contract as pre-M34 duplicated helpers).
    """

    try:
        raw = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        return None, str(exc)
    return parse_json_object_text(raw)


def load_json_object_strict(path: Path) -> dict[str, Any]:
    """Read ``path`` and return a single JSON object, or raise :exc:`ValueError`.

    Single contract for strict callers (M35): :exc:`ValueError` on read failure,
    invalid JSON, or a non-object JSON root.
    """

    try:
        raw = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        msg = f"{path}: {exc}"
        raise ValueError(msg) from exc
    obj, err = parse_json_object_text(raw)
    if err is None:
        assert obj is not None
        return obj
    if err == JSON_ROOT_MUST_BE_OBJECT:
        msg = f"{path}: JSON root must be an object"
        raise ValueError(msg)
    try:
        json.loads(raw)
    except json.JSONDecodeError as exc:
        msg = f"invalid JSON in {path}: {exc}"
        raise ValueError(msg) from exc
    raise RuntimeError("unreachable")
