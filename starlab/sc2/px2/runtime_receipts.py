"""Deterministic receipts for PX2 compile / legality (tests and audit)."""

from __future__ import annotations

import hashlib
import json
from typing import Any

from starlab.sc2.px2.action_compiler import Px2InternalCommand, compile_terran_action
from starlab.sc2.px2.terran_action_schema import TerranAction
from starlab.sc2.px2.terran_legality import GameStateSnapshot, legality_for

PX2_COMPILE_RECEIPT_CONTRACT: str = "starlab.px2.compile_receipt.v1"


def build_compile_receipt(
    *,
    action: TerranAction,
    state: GameStateSnapshot | None,
    include_legality: bool = True,
) -> dict[str, Any]:
    """Build a JSON-serializable receipt for a compile step."""

    legality_json: dict[str, Any] | None = None
    if include_legality and state is not None:
        lr = legality_for(state, action)
        legality_json = lr.to_json_dict()

    cmd: Px2InternalCommand | None = None
    error: str | None = None
    try:
        cmd = compile_terran_action(action, state)
    except ValueError as e:
        error = str(e)

    receipt: dict[str, Any] = {
        "contract_id": PX2_COMPILE_RECEIPT_CONTRACT,
        "action": action.to_json_dict(),
        "legality": legality_json,
        "compiled": cmd.to_json_dict() if cmd is not None else None,
        "error": error,
    }
    return receipt


def receipt_sha256(receipt: dict[str, Any]) -> str:
    """Stable hash for fixture comparison (sorted JSON)."""

    blob = json.dumps(receipt, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(blob).hexdigest()
