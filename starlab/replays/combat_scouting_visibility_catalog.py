"""M12-owned conservative entity → role mapping (combat / scouting / visibility plane)."""

from __future__ import annotations

from starlab.replays.build_order_economy_catalog import ENTITY_CATEGORY as M11_ENTITY_CATEGORY

# M11 macro categories -> M12 roles (reuse macro semantics).
_M11_TO_M12_ROLE: dict[str, str] = {
    "worker": "worker",
    "townhall": "townhall",
    "gas_structure": "gas_structure",
    "supply_provider": "supply_provider",
    "production_structure": "production_structure",
    "tech_structure": "tech_structure",
    "combat_or_other": "army",
}

# Explicit M12 extensions (narrow; unknowns reported separately).
ENTITY_ROLE: dict[str, str] = {}
for name, cat in M11_ENTITY_CATEGORY.items():
    ENTITY_ROLE[name] = _M11_TO_M12_ROLE.get(cat, "unknown")

# Scouting / combat-specific overrides and additions.
ENTITY_ROLE.update(
    {
        "Reaper": "scout",
        "Observer": "detector",
        "Overseer": "detector",
        "Raven": "detector",
    },
)

STRUCTURE_ROLES: frozenset[str] = frozenset(
    {
        "townhall",
        "gas_structure",
        "supply_provider",
        "production_structure",
        "tech_structure",
        "other_structure",
    },
)
