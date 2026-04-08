"""M14 replay bundle generation tests (fixture JSON; no s2protocol, no raw parse)."""

from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path
from typing import Any, cast

from starlab.replays.replay_bundle_generation import (
    build_replay_bundle_envelope,
    compute_bundle_id,
    compute_lineage_root,
)
from starlab.replays.replay_bundle_io import extract_replay_bundle_from_paths
from starlab.runs.json_util import canonical_json_dumps, sha256_hex_of_canonical_json

FIX = Path(__file__).resolve().parent / "fixtures" / "m14"


def _load(name: str) -> dict[str, Any]:
    data: Any = json.loads((FIX / name).read_text(encoding="utf-8"))
    assert isinstance(data, dict)
    return data


def test_golden_replay_bundle_deterministic() -> None:
    primary = {
        "replay_metadata.json": _load("replay_metadata.json"),
        "replay_timeline.json": _load("replay_timeline.json"),
        "replay_build_order_economy.json": _load("replay_build_order_economy.json"),
        "replay_combat_scouting_visibility.json": _load("replay_combat_scouting_visibility.json"),
        "replay_slices.json": _load("replay_slices.json"),
    }
    secondary: dict[str, dict[str, Any]] = {}
    if (FIX / "replay_metadata_report.json").is_file():
        secondary["replay_metadata_report.json"] = _load("replay_metadata_report.json")
    if (FIX / "replay_slices_report.json").is_file():
        secondary["replay_slices_report.json"] = _load("replay_slices_report.json")

    status, err, manifest, lineage, contents = build_replay_bundle_envelope(
        bundle_created_from="tests/fixtures/m14",
        primary_objects=primary,
        secondary_reports=secondary,
    )
    assert err is None
    assert status == "completed"

    exp_m = json.loads((FIX / "expected_replay_bundle_manifest.json").read_text(encoding="utf-8"))
    exp_l = json.loads((FIX / "expected_replay_bundle_lineage.json").read_text(encoding="utf-8"))
    exp_c = json.loads((FIX / "expected_replay_bundle_contents.json").read_text(encoding="utf-8"))
    assert json.loads(canonical_json_dumps(manifest)) == exp_m
    assert json.loads(canonical_json_dumps(lineage)) == exp_l
    assert json.loads(canonical_json_dumps(contents)) == exp_c


def test_lineage_mismatch_fails() -> None:
    primary = {
        "replay_metadata.json": _load("replay_metadata.json"),
        "replay_timeline.json": _load("replay_timeline.json"),
        "replay_build_order_economy.json": _load("replay_build_order_economy.json"),
        "replay_combat_scouting_visibility.json": _load("replay_combat_scouting_visibility.json"),
        "replay_slices.json": _load("replay_slices.json"),
    }
    boe = deepcopy(primary["replay_build_order_economy.json"])
    boe["source_timeline_sha256"] = "0" * 64
    primary["replay_build_order_economy.json"] = boe
    status, err, _m, _l, _c = build_replay_bundle_envelope(
        bundle_created_from="test",
        primary_objects=primary,
        secondary_reports={},
    )
    assert status == "lineage_failed"
    assert err is not None
    assert "timeline" in err.lower()


def test_missing_primary_fails() -> None:
    partial: dict[str, Any] = {
        "replay_metadata.json": _load("replay_metadata.json"),
        "replay_timeline.json": _load("replay_timeline.json"),
        "replay_build_order_economy.json": _load("replay_build_order_economy.json"),
        "replay_combat_scouting_visibility.json": _load("replay_combat_scouting_visibility.json"),
    }
    status, err, _m, _l, _c = build_replay_bundle_envelope(
        bundle_created_from="test",
        primary_objects=cast(dict[str, dict[str, Any]], partial),
        secondary_reports={},
    )
    assert status == "load_failed"
    assert "missing primary" in (err or "").lower()


def test_bundle_id_and_lineage_root_stable() -> None:
    primary = {
        "replay_metadata.json": _load("replay_metadata.json"),
        "replay_timeline.json": _load("replay_timeline.json"),
        "replay_build_order_economy.json": _load("replay_build_order_economy.json"),
        "replay_combat_scouting_visibility.json": _load("replay_combat_scouting_visibility.json"),
        "replay_slices.json": _load("replay_slices.json"),
    }
    ph = {k: sha256_hex_of_canonical_json(primary[k]) for k in sorted(primary)}
    lr = compute_lineage_root(primary_hashes=ph)
    bid = compute_bundle_id(
        lineage_root=lr,
        generation_parameters={"replay_bundle_catalog": "starlab.replay_bundle_catalog.m14.v1"},
    )
    assert len(lr) == 64
    assert len(bid) == 64
    assert lr == compute_lineage_root(primary_hashes=ph)


def test_extract_from_paths_matches_golden(tmp_path: Path) -> None:
    out = tmp_path / "bundle_out"
    status, err, _m, _l, _c = extract_replay_bundle_from_paths(
        bundle_created_from="tests/fixtures/m14",
        input_dir=FIX,
        output_dir=out,
    )
    assert status == "completed"
    assert err is None
    exp_m = (FIX / "expected_replay_bundle_manifest.json").read_text(encoding="utf-8")
    assert (out / "replay_bundle_manifest.json").read_text(encoding="utf-8") == exp_m
