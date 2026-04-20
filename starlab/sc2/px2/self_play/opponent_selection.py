"""Deterministic opponent / snapshot selection rules (PX2-M03 opening)."""

from __future__ import annotations

from typing import Final

OPPONENT_SELECTION_SELF_SNAPSHOT: Final[str] = "starlab.px2.opponent_selection.self_snapshot.v1"
OPPONENT_SELECTION_ROUND_ROBIN: Final[str] = (
    "starlab.px2.opponent_selection.round_robin_snapshot.v1"
)
OPPONENT_SELECTION_FROZEN_SEED: Final[str] = (
    "starlab.px2.opponent_selection.frozen_seed_snapshot.v1"
)
OPPONENT_SELECTION_WEIGHTED_FROZEN_STUB: Final[str] = (
    "starlab.px2.opponent_selection.weighted_frozen_stub.v1"
)


def select_opponent_ref(
    *,
    step_index: int,
    rule_id: str,
    ref_ids: tuple[str, ...],
    weights: tuple[int, ...] | None = None,
) -> str:
    """Return the opponent snapshot ref for this step (deterministic).

    ``ref_ids`` must be non-empty. ``self_snapshot`` always picks index 0.
    ``frozen_seed`` always picks index 0. ``round_robin`` cycles through all ids.
    ``weighted_frozen_stub`` repeats each ref by integer weight then round-robins
    the expanded sequence (deterministic; governance bookkeeping, not gameplay).
    """

    if not ref_ids:
        msg = "ref_ids must be non-empty"
        raise ValueError(msg)
    if rule_id == OPPONENT_SELECTION_SELF_SNAPSHOT:
        return ref_ids[0]
    if rule_id == OPPONENT_SELECTION_FROZEN_SEED:
        return ref_ids[0]
    if rule_id == OPPONENT_SELECTION_ROUND_ROBIN:
        return ref_ids[step_index % len(ref_ids)]
    if rule_id == OPPONENT_SELECTION_WEIGHTED_FROZEN_STUB:
        if weights is None:
            msg = "weights required for weighted_frozen_stub"
            raise ValueError(msg)
        if len(weights) != len(ref_ids):
            msg = "weights length must match ref_ids"
            raise ValueError(msg)
        if any(w < 0 for w in weights):
            msg = "weights must be non-negative integers"
            raise ValueError(msg)
        expanded: list[str] = []
        for rid, w in zip(ref_ids, weights, strict=True):
            expanded.extend([rid] * w)
        if not expanded:
            msg = "weighted expansion is empty"
            raise ValueError(msg)
        return expanded[step_index % len(expanded)]
    msg = f"unknown opponent_selection_rule_id: {rule_id!r}"
    raise ValueError(msg)
