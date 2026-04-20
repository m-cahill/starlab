"""Opponent rotation trace helpers — audit bookkeeping for PX2-M03 (not gameplay diversity)."""

from __future__ import annotations

from typing import Any


def build_opponent_rotation_trace(
    *,
    step_index: int,
    rule_id: str,
    ref_ids: tuple[str, ...],
    selected_ref: str,
    weights: tuple[int, ...] | None = None,
) -> dict[str, Any]:
    """Deterministic per-step record of which opponent ref was selected."""

    return {
        "opponent_selection_rule_id": rule_id,
        "step_index_zero_based": step_index,
        "candidate_ref_ids": list(ref_ids),
        "weights": list(weights) if weights is not None else None,
        "selected_opponent_ref": selected_ref,
    }
