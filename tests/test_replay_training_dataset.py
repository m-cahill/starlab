"""Tests for replay training dataset emission (M26)."""

from __future__ import annotations

import ast
import json
import shutil
from pathlib import Path

import pytest
from starlab.imitation.dataset_models import APPROVED_TARGET_SEMANTIC_KINDS
from starlab.imitation.dataset_views import (
    build_replay_training_dataset_artifacts,
    load_json_object,
    map_timeline_to_coarse_label,
    split_mod100_from_example_id,
)
from starlab.imitation.emit_replay_training_dataset import write_replay_training_dataset_artifacts
from starlab.runs.json_util import canonical_json_dumps

REPO_ROOT = Path(__file__).resolve().parents[1]
M14_FIX = REPO_ROOT / "tests" / "fixtures" / "m14"
M26_FIX = REPO_ROOT / "tests" / "fixtures" / "m26"


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
    ds, rep = build_replay_training_dataset_artifacts(bundle_dirs=[tmp_path / "b1"])
    exp_ds = load_json_object(M26_FIX / "replay_training_dataset.json")
    exp_rep = load_json_object(M26_FIX / "replay_training_dataset_report.json")
    assert canonical_json_dumps(ds) == canonical_json_dumps(exp_ds)
    assert canonical_json_dumps(rep) == canonical_json_dumps(exp_rep)


def test_byte_stable_repeated_emit(tmp_path: Path) -> None:
    materialize_m14_bundle_directory(tmp_path / "b1")
    p1 = tmp_path / "out1"
    p2 = tmp_path / "out2"
    write_replay_training_dataset_artifacts(bundle_dirs=[tmp_path / "b1"], output_dir=p1)
    write_replay_training_dataset_artifacts(bundle_dirs=[tmp_path / "b1"], output_dir=p2)
    assert (p1 / "replay_training_dataset.json").read_bytes() == (
        p2 / "replay_training_dataset.json"
    ).read_bytes()
    assert (p1 / "replay_training_dataset_report.json").read_bytes() == (
        p2 / "replay_training_dataset_report.json"
    ).read_bytes()


def test_example_ordering_stable(tmp_path: Path) -> None:
    materialize_m14_bundle_directory(tmp_path / "b1")
    ds1, _ = build_replay_training_dataset_artifacts(bundle_dirs=[tmp_path / "b1"])
    ds2, _ = build_replay_training_dataset_artifacts(bundle_dirs=[tmp_path / "b1"])
    assert [e["example_id"] for e in ds1["examples"]] == [e["example_id"] for e in ds2["examples"]]


def test_split_mod100_locked_vectors() -> None:
    ex1 = (
        "starlab.m26.example.v1:fdd37af019f2cd23f3dce5a1c6d129a7741f81e0502528f325141d7e0b56f457:"
        "844b7c08271e81f1444585004d23c26c52d77e009168f6ca22066b4cf6c071a1:0:100:0:production_structure"
    )
    assert split_mod100_from_example_id(ex1) == "validation"


def test_duplicate_bundle_id_rejected(tmp_path: Path) -> None:
    materialize_m14_bundle_directory(tmp_path / "a")
    materialize_m14_bundle_directory(tmp_path / "b")
    with pytest.raises(ValueError, match="duplicate bundle_id"):
        build_replay_training_dataset_artifacts(bundle_dirs=[tmp_path / "a", tmp_path / "b"])


def test_manifest_hash_mismatch_rejected(tmp_path: Path) -> None:
    materialize_m14_bundle_directory(tmp_path / "bad")
    mpath = tmp_path / "bad" / "replay_bundle_manifest.json"
    m = json.loads(mpath.read_text(encoding="utf-8"))
    m["artifact_hashes"]["replay_metadata.json"] = "0" * 64
    mpath.write_text(json.dumps(m, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    with pytest.raises(ValueError, match="hash mismatch"):
        build_replay_training_dataset_artifacts(bundle_dirs=[tmp_path / "bad"])


def test_lineage_bundle_id_mismatch_rejected(tmp_path: Path) -> None:
    materialize_m14_bundle_directory(tmp_path / "bad")
    lpath = tmp_path / "bad" / "replay_bundle_lineage.json"
    l_obj = json.loads(lpath.read_text(encoding="utf-8"))
    l_obj["bundle_id"] = "0" * 64
    lpath.write_text(json.dumps(l_obj, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    with pytest.raises(ValueError, match="bundle_id"):
        build_replay_training_dataset_artifacts(bundle_dirs=[tmp_path / "bad"])


def test_quarantined_intake_rejected(tmp_path: Path) -> None:
    materialize_m14_bundle_directory(tmp_path / "b1")
    shutil.copy(
        M26_FIX / "replay_intake_receipt_quarantined.json",
        tmp_path / "b1" / "replay_intake_receipt.json",
    )
    with pytest.raises(ValueError, match="quarantined"):
        build_replay_training_dataset_artifacts(bundle_dirs=[tmp_path / "b1"])


def test_labels_bounded(tmp_path: Path) -> None:
    materialize_m14_bundle_directory(tmp_path / "b1")
    ds, _ = build_replay_training_dataset_artifacts(bundle_dirs=[tmp_path / "b1"])
    for ex in ds["examples"]:
        assert ex["target_semantic_kind"] in APPROVED_TARGET_SEMANTIC_KINDS


def test_map_unknown_semantic_falls_back_to_other() -> None:
    assert (
        map_timeline_to_coarse_label(semantic_kind="unknown_xyz", source_stream="tracker")
        == "other"
    )


def test_m26_imitation_modules_have_no_forbidden_imports() -> None:
    root = REPO_ROOT / "starlab" / "imitation"
    forbidden = ("starlab.replays", "starlab.sc2", "s2protocol")
    for path in sorted(root.glob("*.py")):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    assert not any(alias.name.startswith(prefix) for prefix in forbidden), (
                        f"{path.name}: forbidden import {alias.name}"
                    )
            elif isinstance(node, ast.ImportFrom):
                assert node.module is not None
                assert not any(
                    node.module == prefix or node.module.startswith(prefix + ".")
                    for prefix in forbidden
                ), f"{path.name}: forbidden import from {node.module}"


def test_end_to_end_m14_chain(tmp_path: Path) -> None:
    """Governed M14 fixture inputs → M26 dataset output."""

    materialize_m14_bundle_directory(tmp_path / "bundle")
    ds, rep = build_replay_training_dataset_artifacts(bundle_dirs=[tmp_path / "bundle"])
    assert ds["dataset_version"] == "starlab.replay_training_dataset.v1"
    assert rep["report_version"] == "starlab.replay_training_dataset_report.v1"
    assert rep["source_bundle_count"] == 1
    assert rep["example_count"] == len(ds["examples"])
