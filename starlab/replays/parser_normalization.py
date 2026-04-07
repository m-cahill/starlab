"""Deterministic lowering of parser-native Python values to JSON-safe STARLAB data (M08)."""

from __future__ import annotations

import math
from enum import Enum
from typing import Any


class NormalizationError(ValueError):
    """Raised when a value cannot be lowered deterministically."""


def normalize_value(value: Any) -> Any:
    """Recursively normalize a value for canonical JSON emission.

    Rules:
    - ``dict``: keys sorted lexicographically; values normalized recursively.
    - ``list`` / ``tuple``: normalized to list, elements normalized.
    - ``bytes`` / ``bytearray``: lowercase hex string (no ``0x`` prefix).
    - ``str``, ``bool``, ``int``: returned as-is.
    - ``float``: rejected if not finite (no NaN / Infinity).
    - ``Enum``: string of ``name`` (stable across runs).
    - ``None``: null.
    - Other types: ``NormalizationError``.
    """

    if value is None:
        return None
    if isinstance(value, bool):
        return value
    if isinstance(value, int) and not isinstance(value, bool):
        return value
    if isinstance(value, float):
        if not math.isfinite(value):
            msg = "non-finite float is not JSON-safe for STARLAB normalization"
            raise NormalizationError(msg)
        return value
    if isinstance(value, str):
        return value
    if isinstance(value, bytes):
        return value.hex()
    if isinstance(value, bytearray):
        return bytes(value).hex()
    if isinstance(value, tuple):
        return [normalize_value(v) for v in value]
    if isinstance(value, list):
        return [normalize_value(v) for v in value]
    if isinstance(value, dict):
        out: dict[str, Any] = {}
        for k in sorted(value.keys(), key=lambda x: str(x)):
            if not isinstance(k, str):
                msg = f"dict keys must be str after lowering, got {type(k).__name__}"
                raise NormalizationError(msg)
            out[k] = normalize_value(value[k])
        return out
    if isinstance(value, Enum):
        return str(value.name)
    msg = f"unsupported type for normalization: {type(value).__name__}"
    raise NormalizationError(msg)


def normalize_mapping_tree(root: Any) -> Any:
    """Normalize a tree; if root is not a mapping, normalize as a single value."""

    return normalize_value(root)
