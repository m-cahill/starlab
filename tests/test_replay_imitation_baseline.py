"""Tests for replay imitation baseline emission (M27)."""

from __future__ import annotations

import ast
import json
import shutil
from pathlib import Path
from unittest.mock import patch

import pytest
from starlab.imitation.baseline_fit import build_replay_imitation_baseline_artifacts
from starlab.imitation.emit_replay_imitation_baseline import main as emit_main
from starlab.imitation.replay_observation_materialization import resolve_bundle_directory
from starlab.runs.json_util import canonical_json_dumps

REPO_ROOT = Path(__file__).resolve().parents[1]
M14_FIX = REPO_ROOT / "tests" / "fixtures" / "m14"
M26_FIX = REPO_ROOT / "tests" / "fixtures" / "m26"
M27_FIX = REPO_ROOT / "tests" / "fixtures" / "m27"

FIXTURE_LINEAGE_ROOT = "fdd37af019f2cd23f3dce5a1c6d129a7741f81e0502528f325141d7e0b56f457"
FIXTURE_BUNDLE_ID = "844b7c08271e81f1444585004d23c26c52d77e009168f6ca22066b4cf6c071a1"

M27_IMITATION_MODULES = (
    "baseline_models.py",
    "baseline_features.py",
    "baseline_fit.py",
    "emit_replay_imitation_baseline.py",
    "replay_observation_materialization.py",
)


def materialize_m14_bundle_directory(dest: Path) -> None:
    """Build M14 bundle dir from shared fixture + expected bundle JSON."""

    dest.mkdir(parents=True, exist_ok=True)
    for name in (
        "replay_metadata.json",
        "replay_timeline.json",
        "replay_build_order_economy.json",
        "replay_combat_scouting_visibility.json",
        "replay_slices.json",
        "replay_metadata_report.json",
        "replay_slices_report.json",
    ):
        shutil.copy(M14_FIX / name, dest / name)
    shutil.copy(
        M14_FIX / "expected_replay_bundle_manifest.json",
        dest / "replay_bundle_manifest.json",
    )
    shutil.copy(
        M14_FIX / "expected_replay_bundle_lineage.json",
        dest / "replay_bundle_lineage.json",
    )
    shutil.copy(
        M14_FIX / "expected_replay_bundle_contents.json",
        dest / "replay_bundle_contents.json",
    )


def test_happy_path_matches_golden(tmp_path: Path) -> None:
    materialize_m14_bundle_directory(tmp_path / "b1")
    ds = json.loads((M26_FIX / "replay_training_dataset.json").read_text(encoding="utf-8"))
    bl, rep = build_replay_imitation_baseline_artifacts(
        dataset=ds,
        bundle_dirs=[tmp_path / "b1"],
    )
    exp_bl = json.loads(
        (M27_FIX / "replay_imitation_baseline.json").read_text(encoding="utf-8"),
    )
    exp_rep = json.loads(
        (M27_FIX / "replay_imitation_baseline_report.json").read_text(encoding="utf-8"),
    )
    assert canonical_json_dumps(bl) == canonical_json_dumps(exp_bl)
    assert canonical_json_dumps(rep) == canonical_json_dumps(exp_rep)


def test_byte_stable_repeated_emit(tmp_path: Path) -> None:
    materialize_m14_bundle_directory(tmp_path / "b1")
    ds = json.loads((M26_FIX / "replay_training_dataset.json").read_text(encoding="utf-8"))
    bl1, r1 = build_replay_imitation_baseline_artifacts(dataset=ds, bundle_dirs=[tmp_path / "b1"])
    bl2, r2 = build_replay_imitation_baseline_artifacts(dataset=ds, bundle_dirs=[tmp_path / "b1"])
    assert canonical_json_dumps(bl1) == canonical_json_dumps(bl2)
    assert canonical_json_dumps(r1) == canonical_json_dumps(r2)


def test_cli_emits(tmp_path: Path) -> None:
    materialize_m14_bundle_directory(tmp_path / "b1")
    out = tmp_path / "out"
    rc = emit_main(
        [
            "--dataset",
            str(M26_FIX / "replay_training_dataset.json"),
            "--bundle",
            str(tmp_path / "b1"),
            "--output-dir",
            str(out),
        ],
    )
    assert rc == 0
    assert (out / "replay_imitation_baseline.json").is_file()
    assert (out / "replay_imitation_baseline_report.json").is_file()


def test_observation_request_bundle_id_mismatch_fails(tmp_path: Path) -> None:
    materialize_m14_bundle_directory(tmp_path / "b1")
    ds = json.loads((M26_FIX / "replay_training_dataset.json").read_text(encoding="utf-8"))
    ds["examples"][0]["observation_request"]["bundle_id"] = "0" * 64
    with pytest.raises(ValueError, match="bundle_id mismatch"):
        build_replay_imitation_baseline_artifacts(dataset=ds, bundle_dirs=[tmp_path / "b1"])


def test_missing_bundle_dir_fails(tmp_path: Path) -> None:
    ds = json.loads((M26_FIX / "replay_training_dataset.json").read_text(encoding="utf-8"))
    with pytest.raises(ValueError, match="replay_bundle_manifest"):
        build_replay_imitation_baseline_artifacts(
            dataset=ds,
            bundle_dirs=[tmp_path / "nonexistent"],
        )


def test_resolve_bundle_directory(tmp_path: Path) -> None:
    materialize_m14_bundle_directory(tmp_path / "b1")
    mpath = tmp_path / "b1" / "replay_bundle_manifest.json"
    manifest = json.loads(mpath.read_text(encoding="utf-8"))
    bid = str(manifest["bundle_id"])
    p = resolve_bundle_directory(bundle_id=bid, bundle_dirs=[tmp_path / "b1"])
    assert p.resolve() == (tmp_path / "b1").resolve()


def test_majority_tie_break_lexicographic(tmp_path: Path) -> None:
    """Two labels same count → lexicographically smallest label wins."""

    ds = {
        "dataset_sha256": "a" * 64,
        "dataset_version": "starlab.replay_training_dataset.v1",
        "examples": [
            {
                "bundle_id": FIXTURE_BUNDLE_ID,
                "example_id": "e1",
                "lineage_root": FIXTURE_LINEAGE_ROOT,
                "observation_request": {
                    "bundle_id": FIXTURE_BUNDLE_ID,
                    "gameloop": 100,
                    "lineage_root": FIXTURE_LINEAGE_ROOT,
                    "perspective_player_index": 0,
                },
                "perspective_player_index": 0,
                "split": "train",
                "target_semantic_kind": "zebra",
            },
            {
                "bundle_id": FIXTURE_BUNDLE_ID,
                "example_id": "e2",
                "lineage_root": FIXTURE_LINEAGE_ROOT,
                "observation_request": {
                    "bundle_id": FIXTURE_BUNDLE_ID,
                    "gameloop": 100,
                    "lineage_root": FIXTURE_LINEAGE_ROOT,
                    "perspective_player_index": 0,
                },
                "perspective_player_index": 0,
                "split": "train",
                "target_semantic_kind": "apple",
            },
        ],
        "label_policy_id": "starlab.m26.label.coarse_action_v1",
        "warnings": [],
    }

    def fake_sig(**_kwargs: object) -> str:
        return "same_sig"

    bdir = tmp_path / "b1"
    materialize_m14_bundle_directory(bdir)
    with patch("starlab.imitation.baseline_fit.build_context_signature", fake_sig):
        bl, _rep = build_replay_imitation_baseline_artifacts(dataset=ds, bundle_dirs=[bdir])
    row = next(r for r in bl["signature_table"] if r["context_signature"] == "same_sig")
    assert row["predicted_label"] == "apple"
    assert bl["fallback_label"] == "apple"


def test_m27_imitation_modules_forbid_replays_sc2_s2protocol() -> None:
    im = REPO_ROOT / "starlab" / "imitation"
    forbidden = frozenset({"starlab.replays", "starlab.sc2", "s2protocol"})
    for fname in M27_IMITATION_MODULES:
        tree = ast.parse((im / fname).read_text(encoding="utf-8"))
        found: set[str] = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    base = alias.name.split(".", 1)[0]
                    head = alias.name
                    if head in forbidden or base in {"s2protocol"}:
                        found.add(alias.name)
            elif isinstance(node, ast.ImportFrom):
                if node.module and node.module in forbidden:
                    found.add(node.module)
        assert not found, f"{fname}: forbidden imports {found}"


def test_end_to_end_m26_dataset_to_m27_baseline(tmp_path: Path) -> None:
    """Governed M14 bundle → M26 dataset fixture → M27 baseline artifact chain."""

    materialize_m14_bundle_directory(tmp_path / "b1")
    from starlab.imitation.dataset_views import build_replay_training_dataset_artifacts

    ds, _rep = build_replay_training_dataset_artifacts(bundle_dirs=[tmp_path / "b1"])
    assert ds["dataset_version"] == "starlab.replay_training_dataset.v1"
    bl, bl_rep = build_replay_imitation_baseline_artifacts(
        dataset=ds,
        bundle_dirs=[tmp_path / "b1"],
    )
    assert bl["baseline_version"] == "starlab.replay_imitation_baseline.v1"
    assert bl["model_family"] == "starlab.m27.model.observation_signature_majority_v1"
    assert bl_rep["report_version"] == "starlab.replay_imitation_baseline_report.v1"
    assert bl_rep["baseline_sha256"] == bl["baseline_sha256"]
    assert "agreement_by_split" in bl_rep
