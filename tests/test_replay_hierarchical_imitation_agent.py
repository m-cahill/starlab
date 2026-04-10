"""Tests for replay hierarchical imitation agent (M30)."""

from __future__ import annotations

import ast
import json
import shutil
import subprocess
import sys
from pathlib import Path

import pytest
from starlab.hierarchy.delegate_policy import (
    DELEGATE_IDS,
    DELEGATE_POLICY_ID,
    assert_delegate_mapping_total,
    delegate_id_for_coarse_label,
)
from starlab.hierarchy.emit_replay_hierarchical_imitation_agent import main as emit_main
from starlab.hierarchy.hierarchical_agent_fit import (
    build_replay_hierarchical_imitation_agent_artifacts,
    select_proof_trace_examples,
)
from starlab.hierarchy.hierarchical_agent_predictor import FrozenHierarchicalImitationPredictor
from starlab.hierarchy.hierarchical_interface_schema import validate_hierarchical_trace_document
from starlab.runs.json_util import canonical_json_dumps

REPO_ROOT = Path(__file__).resolve().parents[1]
M14_FIX = REPO_ROOT / "tests" / "fixtures" / "m14"
M26_FIX = REPO_ROOT / "tests" / "fixtures" / "m26"
M30_FIX = REPO_ROOT / "tests" / "fixtures" / "m30"

M30_HIERARCHY_MODULES = (
    "delegate_policy.py",
    "hierarchical_agent_models.py",
    "hierarchical_agent_fit.py",
    "hierarchical_agent_predictor.py",
    "emit_replay_hierarchical_imitation_agent.py",
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


def test_delegate_mapping_total_over_m29_enum() -> None:
    assert_delegate_mapping_total()
    assert len(DELEGATE_IDS) == 4
    assert delegate_id_for_coarse_label("production_unit") == "production"
    assert delegate_id_for_coarse_label("scout") == "information"


def test_happy_path_matches_golden(tmp_path: Path) -> None:
    materialize_m14_bundle_directory(tmp_path / "b1")
    ds = json.loads((M26_FIX / "replay_training_dataset.json").read_text(encoding="utf-8"))
    agent, rep = build_replay_hierarchical_imitation_agent_artifacts(
        dataset=ds,
        bundle_dirs=[tmp_path / "b1"],
    )
    exp_a = json.loads(
        (M30_FIX / "replay_hierarchical_imitation_agent.json").read_text(encoding="utf-8")
    )
    exp_r = json.loads(
        (M30_FIX / "replay_hierarchical_imitation_agent_report.json").read_text(encoding="utf-8")
    )
    assert canonical_json_dumps(agent) == canonical_json_dumps(exp_a)
    assert canonical_json_dumps(rep) == canonical_json_dumps(exp_r)


def test_byte_stable_repeated_emit(tmp_path: Path) -> None:
    materialize_m14_bundle_directory(tmp_path / "b1")
    ds = json.loads((M26_FIX / "replay_training_dataset.json").read_text(encoding="utf-8"))
    a1, r1 = build_replay_hierarchical_imitation_agent_artifacts(
        dataset=ds, bundle_dirs=[tmp_path / "b1"]
    )
    a2, r2 = build_replay_hierarchical_imitation_agent_artifacts(
        dataset=ds, bundle_dirs=[tmp_path / "b1"]
    )
    assert canonical_json_dumps(a1) == canonical_json_dumps(a2)
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
    assert (out / "replay_hierarchical_imitation_agent.json").is_file()
    assert (out / "replay_hierarchical_imitation_agent_report.json").is_file()


def test_missing_bundle_dir_fails(tmp_path: Path) -> None:
    ds = json.loads((M26_FIX / "replay_training_dataset.json").read_text(encoding="utf-8"))
    with pytest.raises(ValueError, match="replay_bundle_manifest"):
        build_replay_hierarchical_imitation_agent_artifacts(
            dataset=ds,
            bundle_dirs=[tmp_path / "nonexistent"],
        )


def test_dataset_version_mismatch_fails(tmp_path: Path) -> None:
    materialize_m14_bundle_directory(tmp_path / "b1")
    ds = json.loads((M26_FIX / "replay_training_dataset.json").read_text(encoding="utf-8"))
    ds["dataset_version"] = "bogus"
    with pytest.raises(ValueError, match="unsupported dataset_version"):
        build_replay_hierarchical_imitation_agent_artifacts(
            dataset=ds, bundle_dirs=[tmp_path / "b1"]
        )


def test_unsupported_label_fails(tmp_path: Path) -> None:
    materialize_m14_bundle_directory(tmp_path / "b1")
    ds = json.loads((M26_FIX / "replay_training_dataset.json").read_text(encoding="utf-8"))
    ds["examples"][0]["target_semantic_kind"] = "not_a_real_label"
    with pytest.raises(ValueError, match="unsupported target_semantic_kind"):
        build_replay_hierarchical_imitation_agent_artifacts(
            dataset=ds, bundle_dirs=[tmp_path / "b1"]
        )


def test_empty_train_split_fails(tmp_path: Path) -> None:
    materialize_m14_bundle_directory(tmp_path / "b1")
    ds = json.loads((M26_FIX / "replay_training_dataset.json").read_text(encoding="utf-8"))
    for ex in ds["examples"]:
        if ex.get("split") == "train":
            ex["split"] = "validation"
    with pytest.raises(ValueError, match="no training split"):
        build_replay_hierarchical_imitation_agent_artifacts(
            dataset=ds, bundle_dirs=[tmp_path / "b1"]
        )


def test_malformed_agent_body_predictor_fails() -> None:
    with pytest.raises(ValueError, match="agent_version"):
        FrozenHierarchicalImitationPredictor.from_agent_body({"agent_version": "bogus"})


def test_proof_traces_validate_m29_schema(tmp_path: Path) -> None:
    materialize_m14_bundle_directory(tmp_path / "b1")
    ds = json.loads((M26_FIX / "replay_training_dataset.json").read_text(encoding="utf-8"))
    agent, _rep = build_replay_hierarchical_imitation_agent_artifacts(
        dataset=ds,
        bundle_dirs=[tmp_path / "b1"],
    )
    traces = select_proof_trace_examples(
        dataset=ds,
        bundle_dirs=[tmp_path / "b1"],
        agent=agent,
    )
    assert len(traces) >= 1
    for tr in traces:
        errs = validate_hierarchical_trace_document(tr)
        assert errs == [], errs


def test_invalid_trace_extra_property_fails_schema(tmp_path: Path) -> None:
    materialize_m14_bundle_directory(tmp_path / "b1")
    ds = json.loads((M26_FIX / "replay_training_dataset.json").read_text(encoding="utf-8"))
    agent, _ = build_replay_hierarchical_imitation_agent_artifacts(
        dataset=ds,
        bundle_dirs=[tmp_path / "b1"],
    )
    trs = select_proof_trace_examples(dataset=ds, bundle_dirs=[tmp_path / "b1"], agent=agent)
    bad = dict(trs[0])
    bad["extra_top"] = 1
    errs = validate_hierarchical_trace_document(bad)
    assert errs


def test_module_ast_import_guard() -> None:
    """M30 hierarchy modules must not depend on replay/SC2/parser stacks."""

    pkg = REPO_ROOT / "starlab" / "hierarchy"
    forbidden = ("starlab.replays", "starlab.sc2", "s2protocol")
    for name in M30_HIERARCHY_MODULES:
        path = pkg / name
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        found: list[str] = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.name in forbidden or any(
                        alias.name == f or alias.name.startswith(f + ".") for f in forbidden
                    ):
                        found.append(alias.name)
            elif isinstance(node, ast.ImportFrom):
                if node.module is None:
                    continue
                mod = node.module
                if mod in forbidden or any(mod == f or mod.startswith(f + ".") for f in forbidden):
                    found.append(mod)
        assert not found, f"{name} forbidden imports: {found}"


def test_python_m_emit_entrypoint(tmp_path: Path) -> None:
    materialize_m14_bundle_directory(tmp_path / "b1")
    out = tmp_path / "emit_out"
    proc = subprocess.run(
        [
            sys.executable,
            "-m",
            "starlab.hierarchy.emit_replay_hierarchical_imitation_agent",
            "--dataset",
            str(M26_FIX / "replay_training_dataset.json"),
            "--bundle",
            str(tmp_path / "b1"),
            "--output-dir",
            str(out),
        ],
        cwd=str(REPO_ROOT),
        check=False,
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0, proc.stderr
    assert (out / "replay_hierarchical_imitation_agent.json").is_file()


def test_delegate_policy_id_echoed_in_artifact_and_report(tmp_path: Path) -> None:
    materialize_m14_bundle_directory(tmp_path / "b1")
    ds = json.loads((M26_FIX / "replay_training_dataset.json").read_text(encoding="utf-8"))
    agent, report = build_replay_hierarchical_imitation_agent_artifacts(
        dataset=ds,
        bundle_dirs=[tmp_path / "b1"],
    )
    assert agent["delegate_policy_id"] == DELEGATE_POLICY_ID
    assert report["delegate_policy_id"] == DELEGATE_POLICY_ID


def test_manager_majority_on_tiny_synthetic_tables() -> None:
    """Direct predictor sanity: known signature maps."""

    pred = FrozenHierarchicalImitationPredictor(
        signature_to_delegate={"sig_a": "production"},
        pair_to_label={("production", "sig_a"): "production_unit"},
        manager_fallback_delegate="information",
        worker_fallback_by_delegate={"production": "other"},
        global_worker_fallback_label="other",
    )
    d, lab, mf, wf = pred.predict("sig_a")
    assert (d, lab, mf, wf) == ("production", "production_unit", False, False)


def test_worker_fallback_when_pair_missing() -> None:
    pred = FrozenHierarchicalImitationPredictor(
        signature_to_delegate={"sig_a": "production"},
        pair_to_label={},
        manager_fallback_delegate="information",
        worker_fallback_by_delegate={"production": "production_structure"},
        global_worker_fallback_label="other",
    )
    _d, lab, _mf, wf = pred.predict("sig_a")
    assert wf
    assert lab == "production_structure"
