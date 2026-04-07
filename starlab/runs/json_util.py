"""Canonical JSON helpers for STARLAB run identity (M03)."""

from __future__ import annotations

import hashlib
import json
from typing import Any


def canonical_json_dumps(obj: Any) -> str:
    """Deterministic JSON: sorted keys, UTF-8, trailing newline."""

    dumped = json.dumps(
        obj,
        ensure_ascii=False,
        indent=2,
        sort_keys=True,
        separators=(",", ": "),
    )
    return dumped + "\n"


def sha256_hex_of_canonical_json(obj: Any) -> str:
    """SHA-256 (hex) of canonical JSON bytes (no trailing newline for hash)."""

    dumped = json.dumps(
        obj,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )
    return hashlib.sha256(dumped.encode("utf-8")).hexdigest()
