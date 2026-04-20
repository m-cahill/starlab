"""PX2-M01 Terran runtime — fixture tests (offline)."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from starlab.sc2.px2 import (
    GameStateSnapshot,
    TerranAction,
    build_compile_receipt,
    compile_terran_action,
    legal_mask,
    legality_for,
    receipt_sha256,
    terran_action_from_json_dict,
)
from starlab.sc2.px2.terran_action_schema import (
    ALL_TERRAN_CORE_V1_ACTION_IDS,
    PX2_TERRAN_CORE_SURFACE_VERSION,
)

FIXTURE_DIR = Path(__file__).resolve().parent / "fixtures" / "px2_m01"


def test_surface_version_constant() -> None:
    assert PX2_TERRAN_CORE_SURFACE_VERSION == "starlab.px2.terran_core.v1"


def test_action_registry_nonempty() -> None:
    assert len(ALL_TERRAN_CORE_V1_ACTION_IDS) >= 20


def test_train_marine_legal_with_prereqs() -> None:
    state = GameStateSnapshot(
        minerals=200,
        vespene=0,
        supply_used=10,
        supply_cap=27,
        structures=frozenset({"command_center", "barracks"}),
    )
    action = TerranAction("train_marine", {"producer_key": "barracks_0"})
    assert legality_for(state, action).legal
    cmd = compile_terran_action(action, state)
    assert cmd.command_kind == "train_unit"
    assert cmd.burny_bridge_hint is not None
    assert cmd.burny_bridge_hint["semantic_coarse_label"] == "production_unit"


def test_train_marine_illegal_without_barracks() -> None:
    state = GameStateSnapshot(
        minerals=200,
        vespene=0,
        supply_used=5,
        supply_cap=15,
        structures=frozenset({"command_center"}),
    )
    action = TerranAction("train_marine", {"producer_key": "barracks_0"})
    assert not legality_for(state, action).legal


def test_compile_raises_when_illegal() -> None:
    state = GameStateSnapshot(
        minerals=0,
        vespene=0,
        supply_used=5,
        supply_cap=15,
        structures=frozenset({"command_center", "barracks"}),
    )
    action = TerranAction("train_marine", {"producer_key": "barracks_0"})
    with pytest.raises(ValueError, match="illegal"):
        compile_terran_action(action, state)


def test_fixture_roundtrip() -> None:
    raw = json.loads((FIXTURE_DIR / "sample_train_marine.json").read_text(encoding="utf-8"))
    action = terran_action_from_json_dict(
        {"action_id": raw["action_id"], "arguments": raw["arguments"]},
    )
    assert action.action_id == "train_marine"


def test_compile_receipt_deterministic() -> None:
    state = GameStateSnapshot(
        minerals=500,
        vespene=200,
        supply_used=20,
        supply_cap=35,
        structures=frozenset({"command_center", "barracks", "factory", "starport"}),
    )
    action = TerranAction("train_medivac", {"producer_key": "starport_0"})
    r1 = build_compile_receipt(action=action, state=state, include_legality=True)
    r2 = build_compile_receipt(action=action, state=state, include_legality=True)
    assert receipt_sha256(r1) == receipt_sha256(r2)


def test_legal_mask_keys() -> None:
    state = GameStateSnapshot(400, 0, 5, 11, frozenset({"command_center"}))
    mask = legal_mask(state)
    assert mask["produce_scv"] is True
    assert len(mask) == len(ALL_TERRAN_CORE_V1_ACTION_IDS)
