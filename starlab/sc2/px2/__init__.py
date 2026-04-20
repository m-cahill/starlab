"""PX2 — Autonomous full-game skill development runtime (Terran-first; versioned surfaces)."""

from __future__ import annotations

from starlab.sc2.px2.action_compiler import (
    PX2_INTERNAL_COMMAND_CONTRACT,
    Px2InternalCommand,
    compile_terran_action,
)
from starlab.sc2.px2.burny_bridge import internal_command_to_semantic_hint
from starlab.sc2.px2.placement_targets import (
    BuildSlotId,
    EnemyClusterHandle,
    ExpansionSlotId,
    PlacementRequest,
    RegionSlotId,
)
from starlab.sc2.px2.runtime_receipts import (
    PX2_COMPILE_RECEIPT_CONTRACT,
    build_compile_receipt,
    receipt_sha256,
)
from starlab.sc2.px2.terran_action_schema import (
    PX2_ACTION_SCHEMA_CONTRACT_ID,
    PX2_TERRAN_CORE_SURFACE_VERSION,
    ActionFamily,
    TerranAction,
    terran_action_from_json_dict,
    terran_action_json_dumps,
)
from starlab.sc2.px2.terran_legality import (
    GameStateSnapshot,
    LegalityResult,
    legal_mask,
    legality_for,
)

__all__ = [
    "PX2_ACTION_SCHEMA_CONTRACT_ID",
    "PX2_COMPILE_RECEIPT_CONTRACT",
    "PX2_INTERNAL_COMMAND_CONTRACT",
    "PX2_TERRAN_CORE_SURFACE_VERSION",
    "ActionFamily",
    "BuildSlotId",
    "EnemyClusterHandle",
    "ExpansionSlotId",
    "GameStateSnapshot",
    "LegalityResult",
    "PlacementRequest",
    "Px2InternalCommand",
    "RegionSlotId",
    "TerranAction",
    "build_compile_receipt",
    "compile_terran_action",
    "internal_command_to_semantic_hint",
    "legal_mask",
    "legality_for",
    "receipt_sha256",
    "terran_action_from_json_dict",
    "terran_action_json_dumps",
]
