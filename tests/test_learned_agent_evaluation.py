"""Tests for learned-agent evaluation harness (M28)."""

from __future__ import annotations

import ast
import json
import shutil
from pathlib import Path
from typing import Any

import pytest
from starlab.evaluation.emit_learned_agent_evaluation import main as emit_main
from starlab.evaluation.learned_agent_evaluation import (
    build_learned_agent_evaluation_artifacts,
    index_bundle_directories_for_dataset,
)
from starlab.evaluation.learned_agent_metrics import accuracy, macro_f1
from starlab.imitation.baseline_models import MODEL_FAMILY
from starlab.runs.json_util import canonical_json_dumps

REPO_ROOT = Path(__file__).resolve().parents[1]
M26_FIX = REPO_ROOT / "tests" / "fixtures" / "m26"
M27_FIX = REPO_ROOT / "tests" / "fixtures" / "m27"
M28_FIX = REPO_ROOT / "tests" / "fixtures" / "m28"
M16_BUNDLE = REPO_ROOT / "tests" / "fixtures" / "m16" / "bundle"
M14_FIX = REPO_ROOT / "tests" / "fixtures" / "m14"

M28_EVALUATION_MODULES = (
    "learned_agent_evaluation.py",
    "learned_agent_metrics.py",
    "emit_learned_agent_evaluation.py",
    "learned_agent_models.py",
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


def _load_m28_contract() -> dict[str, Any]:
    raw: Any = json.loads((M28_FIX / "benchmark_contract_m28.json").read_text(encoding="utf-8"))
    assert isinstance(raw, dict)
    return raw


def test_e2e_golden_evaluation(tmp_path: Path) -> None:
    materialize_m14_bundle_directory(tmp_path / "b1")
    c = _load_m28_contract()
    b = json.loads((M27_FIX / "replay_imitation_baseline.json").read_text(encoding="utf-8"))
    d = json.loads((M26_FIX / "replay_training_dataset.json").read_text(encoding="utf-8"))
    ev, rep = build_learned_agent_evaluation_artifacts(
        benchmark_contract=c,
        baseline=b,
        dataset=d,
        bundle_dirs=[tmp_path / "b1"],
    )
    exp_ev = json.loads(
        (M28_FIX / "learned_agent_evaluation.json").read_text(encoding="utf-8"),
    )
    exp_rep = json.loads(
        (M28_FIX / "learned_agent_evaluation_report.json").read_text(encoding="utf-8"),
    )
    assert canonical_json_dumps(ev) == canonical_json_dumps(exp_ev)
    assert canonical_json_dumps(rep) == canonical_json_dumps(exp_rep)


def test_e2e_golden_uses_m16_bundle_fixture() -> None:
    """Fixture path used in golden generation (governed bundle on disk)."""

    c = _load_m28_contract()
    b = json.loads((M27_FIX / "replay_imitation_baseline.json").read_text(encoding="utf-8"))
    d = json.loads((M26_FIX / "replay_training_dataset.json").read_text(encoding="utf-8"))
    ev, rep = build_learned_agent_evaluation_artifacts(
        benchmark_contract=c,
        baseline=b,
        dataset=d,
        bundle_dirs=[M16_BUNDLE],
    )
    exp_ev = json.loads(
        (M28_FIX / "learned_agent_evaluation.json").read_text(encoding="utf-8"),
    )
    exp_rep = json.loads(
        (M28_FIX / "learned_agent_evaluation_report.json").read_text(encoding="utf-8"),
    )
    assert canonical_json_dumps(ev) == canonical_json_dumps(exp_ev)
    assert canonical_json_dumps(rep) == canonical_json_dumps(exp_rep)


def test_deterministic_repeat(tmp_path: Path) -> None:
    materialize_m14_bundle_directory(tmp_path / "b1")
    c = _load_m28_contract()
    b = json.loads((M27_FIX / "replay_imitation_baseline.json").read_text(encoding="utf-8"))
    d = json.loads((M26_FIX / "replay_training_dataset.json").read_text(encoding="utf-8"))
    a1, r1 = build_learned_agent_evaluation_artifacts(
        benchmark_contract=c,
        baseline=b,
        dataset=d,
        bundle_dirs=[tmp_path / "b1"],
    )
    a2, r2 = build_learned_agent_evaluation_artifacts(
        benchmark_contract=c,
        baseline=b,
        dataset=d,
        bundle_dirs=[tmp_path / "b1"],
    )
    assert a1["evaluation_sha256"] == a2["evaluation_sha256"]
    assert canonical_json_dumps(r1) == canonical_json_dumps(r2)


def test_cli_emit(tmp_path: Path) -> None:
    materialize_m14_bundle_directory(tmp_path / "b1")
    out = tmp_path / "out"
    rc = emit_main(
        [
            "--contract",
            str(M28_FIX / "benchmark_contract_m28.json"),
            "--baseline",
            str(M27_FIX / "replay_imitation_baseline.json"),
            "--dataset",
            str(M26_FIX / "replay_training_dataset.json"),
            "--bundle",
            str(tmp_path / "b1"),
            "--output-dir",
            str(out),
        ],
    )
    assert rc == 0
    assert (out / "learned_agent_evaluation.json").is_file()
    assert (out / "learned_agent_evaluation_report.json").is_file()


def test_training_dataset_sha256_mismatch_fails() -> None:
    c = _load_m28_contract()
    b = json.loads((M27_FIX / "replay_imitation_baseline.json").read_text(encoding="utf-8"))
    d = json.loads((M26_FIX / "replay_training_dataset.json").read_text(encoding="utf-8"))
    d["dataset_sha256"] = "0" * 64
    with pytest.raises(ValueError, match="training_dataset_sha256"):
        build_learned_agent_evaluation_artifacts(
            benchmark_contract=c,
            baseline=b,
            dataset=d,
            bundle_dirs=[M16_BUNDLE],
        )


def test_label_policy_mismatch_fails() -> None:
    c = _load_m28_contract()
    b = json.loads((M27_FIX / "replay_imitation_baseline.json").read_text(encoding="utf-8"))
    d = json.loads((M26_FIX / "replay_training_dataset.json").read_text(encoding="utf-8"))
    d["label_policy_id"] = "wrong.policy"
    with pytest.raises(ValueError, match="label_policy_id"):
        build_learned_agent_evaluation_artifacts(
            benchmark_contract=c,
            baseline=b,
            dataset=d,
            bundle_dirs=[M16_BUNDLE],
        )


def test_missing_bundle_dir_fails() -> None:
    c = _load_m28_contract()
    b = json.loads((M27_FIX / "replay_imitation_baseline.json").read_text(encoding="utf-8"))
    d = json.loads((M26_FIX / "replay_training_dataset.json").read_text(encoding="utf-8"))
    with pytest.raises(ValueError, match="replay_bundle_manifest|missing --bundle"):
        build_learned_agent_evaluation_artifacts(
            benchmark_contract=c,
            baseline=b,
            dataset=d,
            bundle_dirs=[REPO_ROOT / "nonexistent_bundle_path"],
        )


def test_extra_bundle_rejected(tmp_path: Path) -> None:
    materialize_m14_bundle_directory(tmp_path / "b1")
    materialize_m14_bundle_directory(tmp_path / "b2")
    c = _load_m28_contract()
    b = json.loads((M27_FIX / "replay_imitation_baseline.json").read_text(encoding="utf-8"))
    d = json.loads((M26_FIX / "replay_training_dataset.json").read_text(encoding="utf-8"))
    with pytest.raises(ValueError, match="duplicate --bundle|extra --bundle"):
        build_learned_agent_evaluation_artifacts(
            benchmark_contract=c,
            baseline=b,
            dataset=d,
            bundle_dirs=[tmp_path / "b1", tmp_path / "b2"],
        )


def test_empty_test_split_fails(tmp_path: Path) -> None:
    materialize_m14_bundle_directory(tmp_path / "b1")
    c = _load_m28_contract()
    b = json.loads((M27_FIX / "replay_imitation_baseline.json").read_text(encoding="utf-8"))
    d = json.loads((M26_FIX / "replay_training_dataset.json").read_text(encoding="utf-8"))
    for ex in d["examples"]:
        if ex.get("split") == "test":
            ex["split"] = "train"
    with pytest.raises(ValueError, match="no examples"):
        build_learned_agent_evaluation_artifacts(
            benchmark_contract=c,
            baseline=b,
            dataset=d,
            bundle_dirs=[tmp_path / "b1"],
        )


def test_invalid_benchmark_contract_fails() -> None:
    c = _load_m28_contract()
    c_bad = {**c, "measurement_surface": "runtime_execution"}
    b = json.loads((M27_FIX / "replay_imitation_baseline.json").read_text(encoding="utf-8"))
    d = json.loads((M26_FIX / "replay_training_dataset.json").read_text(encoding="utf-8"))
    with pytest.raises(ValueError, match="fixture_only"):
        build_learned_agent_evaluation_artifacts(
            benchmark_contract=c_bad,
            baseline=b,
            dataset=d,
            bundle_dirs=[M16_BUNDLE],
        )


def test_malformed_baseline_fails() -> None:
    c = _load_m28_contract()
    d = json.loads((M26_FIX / "replay_training_dataset.json").read_text(encoding="utf-8"))
    b = {
        "baseline_version": "nope",
        "training_dataset_sha256": d["dataset_sha256"],
        "label_policy_id": d["label_policy_id"],
        "model_family": MODEL_FAMILY,
    }
    with pytest.raises(ValueError, match="baseline_version"):
        build_learned_agent_evaluation_artifacts(
            benchmark_contract=c,
            baseline=b,
            dataset=d,
            bundle_dirs=[M16_BUNDLE],
        )


def test_unsupported_evaluation_split_fails() -> None:
    c = _load_m28_contract()
    b = json.loads((M27_FIX / "replay_imitation_baseline.json").read_text(encoding="utf-8"))
    d = json.loads((M26_FIX / "replay_training_dataset.json").read_text(encoding="utf-8"))
    with pytest.raises(ValueError, match="test"):
        build_learned_agent_evaluation_artifacts(
            benchmark_contract=c,
            baseline=b,
            dataset=d,
            bundle_dirs=[M16_BUNDLE],
            evaluation_split="validation",
        )


def test_metric_accuracy_and_macro_f1() -> None:
    y_true = ["a", "b", "a", "b"]
    y_pred = ["a", "b", "b", "b"]
    assert accuracy(y_true, y_pred) == 0.75
    labels = ["a", "b"]
    mf = macro_f1(y_true, y_pred, labels)
    assert abs(mf - (11.0 / 15.0)) < 1e-9


def test_index_bundle_directories_happy(tmp_path: Path) -> None:
    materialize_m14_bundle_directory(tmp_path / "b1")
    mpath = tmp_path / "b1" / "replay_bundle_manifest.json"
    bid = str(json.loads(mpath.read_text(encoding="utf-8"))["bundle_id"])
    idx = index_bundle_directories_for_dataset(
        bundle_dirs=[tmp_path / "b1"],
        required_bundle_ids={bid},
    )
    assert idx[bid] == (tmp_path / "b1").resolve()


def test_m28_evaluation_modules_forbid_replays_sc2_s2protocol() -> None:
    ev = REPO_ROOT / "starlab" / "evaluation"
    forbidden = frozenset({"starlab.replays", "starlab.sc2", "s2protocol"})
    for fname in M28_EVALUATION_MODULES:
        tree = ast.parse((ev / fname).read_text(encoding="utf-8"))
        found: set[str] = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    head = alias.name
                    base = alias.name.split(".", 1)[0]
                    if head in forbidden or base in {"s2protocol"}:
                        found.add(alias.name)
            elif isinstance(node, ast.ImportFrom):
                if node.module and node.module in forbidden:
                    found.add(node.module)
        assert not found, f"{fname}: forbidden imports {found}"


def test_cli_requires_at_least_one_bundle(tmp_path: Path) -> None:
    rc = emit_main(
        [
            "--contract",
            str(M28_FIX / "benchmark_contract_m28.json"),
            "--baseline",
            str(M27_FIX / "replay_imitation_baseline.json"),
            "--dataset",
            str(M26_FIX / "replay_training_dataset.json"),
            "--output-dir",
            str(tmp_path / "out"),
        ],
    )
    assert rc == 2
