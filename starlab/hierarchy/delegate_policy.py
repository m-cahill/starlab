"""Fixed M30 delegate partition over M29/M26 coarse semantic labels (offline v1).

``DELEGATE_POLICY_ID`` is the single anchor for this checked-in mapping; echo it into
artifacts and reports for provenance.
"""

from __future__ import annotations

from typing import Final

from starlab.hierarchy.hierarchical_interface_models import COARSE_SEMANTIC_LABEL_ENUM

DELEGATE_POLICY_ID: Final[str] = "starlab.m30.delegate.fixed_four_v1"

# Stable catalog: exactly four delegates (sorted id order for deterministic JSON).
DELEGATE_IDS: Final[tuple[str, ...]] = ("combat", "economy", "information", "production")

# Deterministic coarse label → delegate (total over ``COARSE_SEMANTIC_LABEL_ENUM``).
COARSE_LABEL_TO_DELEGATE_ID: Final[dict[str, str]] = {
    "army_attack": "combat",
    "army_move": "combat",
    "economy_expand": "economy",
    "economy_worker": "economy",
    "other": "information",
    "production_structure": "production",
    "production_unit": "production",
    "research_upgrade": "production",
    "scout": "information",
}


def assert_delegate_mapping_total() -> None:
    """Raise if mapping is not a bijection from the M29 coarse enum to ``DELEGATE_IDS``."""

    labels = set(COARSE_SEMANTIC_LABEL_ENUM)
    mapped = set(COARSE_LABEL_TO_DELEGATE_ID.keys())
    if labels != mapped:
        msg = f"delegate map keys {sorted(mapped)} != coarse enum {sorted(labels)}"
        raise ValueError(msg)
    targets = set(COARSE_LABEL_TO_DELEGATE_ID.values())
    if targets != set(DELEGATE_IDS):
        msg = f"delegate map range {sorted(targets)} != catalog {list(DELEGATE_IDS)}"
        raise ValueError(msg)


def delegate_id_for_coarse_label(coarse_label: str) -> str:
    """Map one coarse semantic label to a delegate id."""

    if coarse_label not in COARSE_LABEL_TO_DELEGATE_ID:
        msg = f"unsupported coarse label for M30 delegate map: {coarse_label!r}"
        raise ValueError(msg)
    return COARSE_LABEL_TO_DELEGATE_ID[coarse_label]


def build_delegate_catalog_entries() -> list[dict[str, str]]:
    """Return ``delegates_catalog`` rows for M29 traces (``delegate_role`` = worker)."""

    return [{"delegate_id": did, "delegate_role": "worker"} for did in DELEGATE_IDS]
