"""Deterministic slice → panel selection (M31)."""

from __future__ import annotations

from typing import Any


def slice_anchor_gameloop(start_gameloop: int, end_gameloop: int) -> int:
    """Integer midpoint of ``[start_gameloop, end_gameloop]``."""

    return (start_gameloop + end_gameloop) // 2


def _slice_sort_key(s: dict[str, Any]) -> tuple[int, str]:
    return (int(s.get("start_gameloop", -1)), str(s.get("slice_id", "")))


def ordered_slices_for_explorer(
    slices_json: dict[str, Any],
    *,
    slice_id_filter: str | None,
    max_panels: int,
) -> list[dict[str, Any]]:
    """Return up to ``max_panels`` slice dicts in deterministic order."""

    raw = slices_json.get("slices")
    if not isinstance(raw, list):
        return []
    items: list[dict[str, Any]] = [s for s in raw if isinstance(s, dict)]
    if slice_id_filter is not None:
        items = [s for s in items if str(s.get("slice_id", "")) == slice_id_filter]
    items.sort(key=_slice_sort_key)
    return items[: max(0, max_panels)]
