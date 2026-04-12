"""Tests for M41 replay-imitation training pipeline."""

from __future__ import annotations

import ast
import json
import shutil
from pathlib import Path

import pytest
from starlab.imitation.emit_replay_imitation_training_run import main as emit_main
from starlab.imitation.replay_imitation_training_models import (
    REPLAY_IMITATION_TRAINING_RUN_FILENAME,
    REPLAY_IMITATION_TRAINING_RUN_REPORT_FILENAME,
)
from starlab.imitation.replay_imitation_training_pipeline import build_replay_imitation_training_run
from starlab.runs.json_util import canonical_json_dumps, sha256_hex_of_canonical_json
from starlab.training.training_program_io import build_agent_training_program_contract

REPO_ROOT = Path(__file__).resolve().parents[1]
M14_FIX = REPO_ROOT / "tests" / "fixtures" / "m14"
M26_FIX = REPO_ROOT / "tests" / "fixtures" / "m26"

M41_IMITATION_MODULES = (
    "replay_imitation_training_models.py",
    "replay_imitation_training_io.py",
    "replay_imitation_training_pipeline.py",
    "emit_replay_imitation_training_run.py",
)


def materialize_m14_bundle_directory(dest: Path) -> None:
    """Build M14 bundle dir from shared fixture (same as M27 tests)."""

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


def test_training_run_deterministic_repeat(tmp_path: Path) -> None:
    materialize_m14_bundle_directory(tmp_path / "b1")
    ds = json.loads((M26_FIX / "replay_training_dataset.json").read_text(encoding="utf-8"))
    c = build_agent_training_program_contract()
    r1, rep1, _ = build_replay_imitation_training_run(
        bundle_dirs=[tmp_path / "b1"],
        dataset=ds,
        emit_weights=False,
        output_dir=None,
        seed=42,
        training_program_contract=c,
    )
    r2, rep2, _ = build_replay_imitation_training_run(
        bundle_dirs=[tmp_path / "b1"],
        dataset=ds,
        emit_weights=False,
        output_dir=None,
        seed=42,
        training_program_contract=c,
    )
    assert canonical_json_dumps(r1) == canonical_json_dumps(r2)
    assert canonical_json_dumps(rep1) == canonical_json_dumps(rep2)


def test_training_run_binds_m40_contract(tmp_path: Path) -> None:
    materialize_m14_bundle_directory(tmp_path / "b1")
    ds = json.loads((M26_FIX / "replay_training_dataset.json").read_text(encoding="utf-8"))
    c = build_agent_training_program_contract()
    run, _rep, _ = build_replay_imitation_training_run(
        bundle_dirs=[tmp_path / "b1"],
        dataset=ds,
        emit_weights=False,
        output_dir=None,
        seed=7,
        training_program_contract=c,
    )
    assert run["training_program_contract_sha256"] == c["contract_sha256"]
    assert run["training_program_contract_version"] == c["program_version"]
    stripped = {k: v for k, v in run.items() if k != "training_run_sha256"}
    assert sha256_hex_of_canonical_json(stripped) == run["training_run_sha256"]


def test_weights_sidecar_metadata_matches_file(tmp_path: Path) -> None:
    materialize_m14_bundle_directory(tmp_path / "b1")
    ds = json.loads((M26_FIX / "replay_training_dataset.json").read_text(encoding="utf-8"))
    c = build_agent_training_program_contract()
    out = tmp_path / "run_out"
    run, _rep, wp = build_replay_imitation_training_run(
        bundle_dirs=[tmp_path / "b1"],
        dataset=ds,
        emit_weights=True,
        output_dir=out,
        seed=42,
        training_program_contract=c,
    )
    assert wp is not None
    ws = run.get("weights_sidecar")
    assert isinstance(ws, dict)
    assert ws["format"] == "joblib"
    rel = Path(ws["relative_path"])
    assert (out / rel).is_file()
    assert ws["byte_size"] == (out / rel).stat().st_size


def test_run_id_override(tmp_path: Path) -> None:
    materialize_m14_bundle_directory(tmp_path / "b1")
    ds = json.loads((M26_FIX / "replay_training_dataset.json").read_text(encoding="utf-8"))
    c = build_agent_training_program_contract()
    run, _rep, _ = build_replay_imitation_training_run(
        bundle_dirs=[tmp_path / "b1"],
        dataset=ds,
        emit_weights=False,
        output_dir=None,
        run_id_override="custom_run_id_test",
        seed=42,
        training_program_contract=c,
    )
    assert run["run_id"] == "custom_run_id_test"
    assert run["run_id_derivation"] == "operator_override"
    assert len(run["deterministic_run_id"]) == 64


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
            "--seed",
            "42",
        ],
    )
    assert rc == 0
    assert (out / REPLAY_IMITATION_TRAINING_RUN_FILENAME).is_file()
    assert (out / REPLAY_IMITATION_TRAINING_RUN_REPORT_FILENAME).is_file()


def test_feature_schema_fields(tmp_path: Path) -> None:
    materialize_m14_bundle_directory(tmp_path / "b1")
    ds = json.loads((M26_FIX / "replay_training_dataset.json").read_text(encoding="utf-8"))
    run, _rep, _ = build_replay_imitation_training_run(
        bundle_dirs=[tmp_path / "b1"],
        dataset=ds,
        emit_weights=False,
        output_dir=None,
        seed=42,
    )
    fs = run["feature_schema"]
    assert fs["encoding_policy_id"] == "starlab.m41.encoding.context_signature_onehot_v1"
    assert isinstance(fs["ordered_feature_names"], list)
    assert isinstance(fs["label_vocabulary"], list)
    assert len(fs["label_vocabulary"]) >= 2


def test_m41_imitation_modules_forbid_replays_sc2_s2protocol() -> None:
    im = REPO_ROOT / "starlab" / "imitation"
    forbidden = frozenset({"starlab.replays", "starlab.sc2", "s2protocol"})
    for fname in M41_IMITATION_MODULES:
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


def test_single_class_train_split_errors(tmp_path: Path) -> None:
    materialize_m14_bundle_directory(tmp_path / "b1")
    ds = json.loads((M26_FIX / "replay_training_dataset.json").read_text(encoding="utf-8"))
    for ex in ds["examples"]:
        if ex.get("split") == "train":
            ex["target_semantic_kind"] = "production_unit"
    with pytest.raises(ValueError, match="at least two distinct labels"):
        build_replay_imitation_training_run(
            bundle_dirs=[tmp_path / "b1"],
            dataset=ds,
            emit_weights=False,
            output_dir=None,
            seed=42,
        )
