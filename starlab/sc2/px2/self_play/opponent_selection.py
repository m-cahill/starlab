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


def select_opponent_ref(
    *,
    step_index: int,
    rule_id: str,
    ref_ids: tuple[str, ...],
) -> str:
    """Return the opponent snapshot ref for this step (deterministic).

    ``ref_ids`` must be non-empty. ``self_snapshot`` always picks index 0.
    ``frozen_seed`` always picks index 0. ``round_robin`` cycles through all ids.
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
    msg = f"unknown opponent_selection_rule_id: {rule_id!r}"
    raise ValueError(msg)
