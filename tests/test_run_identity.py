"""M03 run spec and execution identity derivation."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from starlab.runs.identity import (
    compute_config_hash,
    compute_execution_id,
    compute_run_spec_id,
    normalize_match_config_for_identity,
)
from starlab.sc2.artifacts import parse_execution_proof_mapping
from starlab.sc2.match_config import load_match_config, match_config_from_mapping

FIXTURE_DIR = Path(__file__).resolve().parent / "fixtures"


@pytest.mark.smoke
def test_normalize_match_config_stable() -> None:
    cfg = load_match_config(FIXTURE_DIR / "m02_match_config.json")
    a = normalize_match_config_for_identity(cfg)
    b = normalize_match_config_for_identity(cfg)
    assert a == b


@pytest.mark.smoke
def test_same_inputs_same_ids() -> None:
    cfg = load_match_config(FIXTURE_DIR / "m02_match_config.json")
    boundary = "s2client_proto_sc2api"
    rs1 = compute_run_spec_id(cfg, boundary)
    rs2 = compute_run_spec_id(cfg, boundary)
    assert rs1 == rs2
    h = "d8e2fcb2e227c7c3e7e908c0df140586572f7c8c25fb67db1be823f445062774"
    e1 = compute_execution_id(h)
    e2 = compute_execution_id(h)
    assert e1 == e2


def test_changed_config_changes_run_spec_id() -> None:
    raw = json.loads((FIXTURE_DIR / "m02_match_config.json").read_text(encoding="utf-8"))
    base = match_config_from_mapping(raw)
    boundary = "s2client_proto_sc2api"
    rs_base = compute_run_spec_id(base, boundary)
    other = match_config_from_mapping({**raw, "seed": 9999})
    rs_other = compute_run_spec_id(other, boundary)
    assert rs_base != rs_other


def test_changed_artifact_hash_changes_execution_id() -> None:
    h0 = "d8e2fcb2e227c7c3e7e908c0df140586572f7c8c25fb67db1be823f445062774"
    h1 = "0" * 64
    assert compute_execution_id(h0) != compute_execution_id(h1)


def test_config_hash_changes_with_map_mode() -> None:
    base = load_match_config(FIXTURE_DIR / "m02_match_config.json")
    ch0 = compute_config_hash(base)
    alt = match_config_from_mapping(
        {
            "adapter": "fake",
            "bounded_horizon": {"game_step": 1, "max_game_steps": 10},
            "interface": {
                "feature_layer_interface": False,
                "raw_interface": True,
                "rendered_interface": False,
                "score_interface": True,
            },
            "map": {"battle_net_map_name": "LadderTest"},
            "schema_version": "1",
            "seed": 4242,
        },
    )
    assert compute_config_hash(alt) != ch0


def test_proof_parse_aligns_with_fixture_config() -> None:
    raw = (FIXTURE_DIR / "m02_match_execution_proof.json").read_text(encoding="utf-8")
    data = json.loads(raw)
    if not isinstance(data, dict):
        pytest.fail("expected dict")
    rec = parse_execution_proof_mapping(data)
    cfg = load_match_config(FIXTURE_DIR / "m02_match_config.json")
    assert cfg.adapter == rec.adapter_name
    assert cfg.seed == rec.seed
