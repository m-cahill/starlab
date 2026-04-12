"""Tests for M43 hierarchical training pipeline."""

from __future__ import annotations

import ast
import json
import shutil
from pathlib import Path

from starlab.hierarchy.emit_hierarchical_training_run import main as emit_main
from starlab.hierarchy.hierarchical_training_models import (
    HIERARCHICAL_TRAINING_RUN_FILENAME,
    HIERARCHICAL_TRAINING_RUN_REPORT_FILENAME,
)
from starlab.hierarchy.hierarchical_training_pipeline import build_hierarchical_training_run
from starlab.runs.json_util import canonical_json_dumps, sha256_hex_of_canonical_json
from starlab.training.training_program_io import build_agent_training_program_contract

REPO_ROOT = Path(__file__).resolve().parents[1]
M14_FIX = REPO_ROOT / "tests" / "fixtures" / "m14"
M26_FIX = REPO_ROOT / "tests" / "fixtures" / "m26"

M43_HIERARCHY_MODULES = (
    "hierarchical_training_models.py",
    "hierarchical_training_io.py",
    "hierarchical_training_pipeline.py",
    "emit_hierarchical_training_run.py",
)


def materialize_m14_bundle_directory(dest: Path) -> None:
    """Build M14 bundle dir from shared fixture (same as M41 tests)."""

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


def test_hierarchical_training_run_deterministic_repeat(tmp_path: Path) -> None:
    materialize_m14_bundle_directory(tmp_path / "b1")
    ds = json.loads((M26_FIX / "replay_training_dataset.json").read_text(encoding="utf-8"))
    c = build_agent_training_program_contract()
    r1, rep1, _ = build_hierarchical_training_run(
        bundle_dirs=[tmp_path / "b1"],
        dataset=ds,
        emit_weights=False,
        output_dir=None,
        seed=42,
        training_program_contract=c,
    )
    r2, rep2, _ = build_hierarchical_training_run(
        bundle_dirs=[tmp_path / "b1"],
        dataset=ds,
        emit_weights=False,
        output_dir=None,
        seed=42,
        training_program_contract=c,
    )
    assert canonical_json_dumps(r1) == canonical_json_dumps(r2)
    assert canonical_json_dumps(rep1) == canonical_json_dumps(rep2)


def test_hierarchical_training_run_binds_m40_contract(tmp_path: Path) -> None:
    materialize_m14_bundle_directory(tmp_path / "b1")
    ds = json.loads((M26_FIX / "replay_training_dataset.json").read_text(encoding="utf-8"))
    c = build_agent_training_program_contract()
    run, _rep, _ = build_hierarchical_training_run(
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


def test_binds_m29_m30_delegate_policy(tmp_path: Path) -> None:
    materialize_m14_bundle_directory(tmp_path / "b1")
    ds = json.loads((M26_FIX / "replay_training_dataset.json").read_text(encoding="utf-8"))
    run, _rep, _ = build_hierarchical_training_run(
        bundle_dirs=[tmp_path / "b1"],
        dataset=ds,
        emit_weights=False,
        output_dir=None,
        seed=42,
    )
    assert run["delegate_policy_id"] == "starlab.m30.delegate.fixed_four_v1"
    assert run["interface_trace_schema_version"] == "starlab.hierarchical_agent_interface_trace.v1"


def test_delegate_coverage_fields(tmp_path: Path) -> None:
    materialize_m14_bundle_directory(tmp_path / "b1")
    ds = json.loads((M26_FIX / "replay_training_dataset.json").read_text(encoding="utf-8"))
    run, _rep, _ = build_hierarchical_training_run(
        bundle_dirs=[tmp_path / "b1"],
        dataset=ds,
        emit_weights=False,
        output_dir=None,
        seed=42,
    )
    cov = run["delegate_coverage"]
    assert isinstance(cov, list)
    assert len(cov) == 4
    for row in cov:
        assert "delegate_id" in row
        assert "counts_by_split" in row
        assert "trained_worker" in row
        assert "fallback_active" in row
        assert "fallback_reason" in row


def test_weights_sidecar_metadata_matches_file(tmp_path: Path) -> None:
    materialize_m14_bundle_directory(tmp_path / "b1")
    ds = json.loads((M26_FIX / "replay_training_dataset.json").read_text(encoding="utf-8"))
    c = build_agent_training_program_contract()
    out = tmp_path / "run_out"
    run, _rep, wp = build_hierarchical_training_run(
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
    assert (out / HIERARCHICAL_TRAINING_RUN_FILENAME).is_file()
    assert (out / HIERARCHICAL_TRAINING_RUN_REPORT_FILENAME).is_file()


def test_m43_hierarchy_modules_forbid_replays_sc2_s2protocol() -> None:
    h = REPO_ROOT / "starlab" / "hierarchy"
    forbidden = frozenset({"starlab.replays", "starlab.sc2", "s2protocol"})
    for fname in M43_HIERARCHY_MODULES:
        tree = ast.parse((h / fname).read_text(encoding="utf-8"))
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


def test_worker_fallback_zero_train_delegate(tmp_path: Path) -> None:
    """Synthetic dataset: one delegate absent from train — fallback, no error."""

    materialize_m14_bundle_directory(tmp_path / "b1")
    ds = json.loads((M26_FIX / "replay_training_dataset.json").read_text(encoding="utf-8"))
    # Force all train examples to production labels only
    for ex in ds["examples"]:
        if isinstance(ex, dict) and ex.get("split") == "train":
            ex["target_semantic_kind"] = "production_unit"
    run, _rep, _ = build_hierarchical_training_run(
        bundle_dirs=[tmp_path / "b1"],
        dataset=ds,
        emit_weights=False,
        output_dir=None,
        seed=42,
    )
    info = {row["delegate_id"]: row for row in run["delegate_coverage"]}
    assert info["information"]["fallback_active"] is True
    assert info["information"]["fallback_reason"] == "zero_train_examples"
