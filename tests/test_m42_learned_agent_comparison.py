"""Tests for M42 learned-agent comparison harness."""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path

import pytest
from starlab.evaluation.learned_agent_comparison_harness import (
    ComparisonCandidateSpec,
    build_learned_agent_comparison_artifacts,
)
from starlab.evaluation.learned_agent_comparison_models import RANKING_POLICY_ID
from starlab.imitation.replay_imitation_training_io import write_replay_imitation_training_artifacts
from starlab.imitation.replay_imitation_training_pipeline import build_replay_imitation_training_run
from starlab.runs.json_util import canonical_json_dumps
from starlab.training.training_program_io import (
    build_agent_training_program_contract,
    write_agent_training_program_contract,
)

REPO_ROOT = Path(__file__).resolve().parents[1]
M14_FIX = REPO_ROOT / "tests" / "fixtures" / "m14"
M26_FIX = REPO_ROOT / "tests" / "fixtures" / "m26"
M28_FIX = REPO_ROOT / "tests" / "fixtures" / "m28"
M27_FIX = REPO_ROOT / "tests" / "fixtures" / "m27"


def _materialize_m14_bundle_directory(dest: Path) -> None:
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


def test_m42_comparison_deterministic_and_ranking_policy(tmp_path: Path) -> None:
    _materialize_m14_bundle_directory(tmp_path / "b1")
    ds = json.loads((M26_FIX / "replay_training_dataset.json").read_text(encoding="utf-8"))
    contract = build_agent_training_program_contract()
    run, _rep, _wp = build_replay_imitation_training_run(
        bundle_dirs=[tmp_path / "b1"],
        dataset=ds,
        emit_weights=True,
        output_dir=tmp_path / "m41_out",
        seed=42,
        training_program_contract=contract,
    )
    baseline = json.loads((M27_FIX / "replay_imitation_baseline.json").read_text(encoding="utf-8"))
    bench = json.loads((M28_FIX / "benchmark_contract_m28.json").read_text(encoding="utf-8"))

    specs = [
        ComparisonCandidateSpec(
            candidate_id="m27_frozen_baseline",
            source_type="m27_frozen_baseline",
            source_artifact_path=str(M27_FIX / "replay_imitation_baseline.json"),
            baseline_body=baseline,
        ),
        ComparisonCandidateSpec(
            candidate_id="m41_run",
            source_type="m41_training_run",
            source_artifact_path=str(tmp_path / "m41_out" / "replay_imitation_training_run.json"),
            training_run_body=run,
            training_run_dir=tmp_path / "m41_out",
        ),
    ]

    c1, r1 = build_learned_agent_comparison_artifacts(
        benchmark_contract=bench,
        dataset=ds,
        bundle_dirs=[tmp_path / "b1"],
        evaluation_split="test",
        training_program_contract=contract,
        candidates=specs,
    )
    c2, r2 = build_learned_agent_comparison_artifacts(
        benchmark_contract=bench,
        dataset=ds,
        bundle_dirs=[tmp_path / "b1"],
        evaluation_split="test",
        training_program_contract=contract,
        candidates=specs,
    )

    assert c1["comparison_id"] == c2["comparison_id"]
    assert canonical_json_dumps(c1) == canonical_json_dumps(c2)
    assert c1["ranking_policy_id"] == RANKING_POLICY_ID
    assert "ranked_candidate_ids" in c1
    assert len(c1["candidate_rows"]) == 2
    assert c1["comparison_version"] == "starlab.learned_agent_comparison.v1"
    assert r1["report_version"] == "starlab.learned_agent_comparison_report.v1"
    nc = set(c1["non_claims"])
    assert "benchmark_integrity" in nc
    assert "replay_execution_equivalence" in nc


def test_m42_emit_cli_smoke(tmp_path: Path) -> None:
    _materialize_m14_bundle_directory(tmp_path / "b1")
    ds = json.loads((M26_FIX / "replay_training_dataset.json").read_text(encoding="utf-8"))
    contract = build_agent_training_program_contract()
    m41_out = tmp_path / "m41_out"
    run, rep, _wp = build_replay_imitation_training_run(
        bundle_dirs=[tmp_path / "b1"],
        dataset=ds,
        emit_weights=True,
        output_dir=m41_out,
        seed=42,
        training_program_contract=contract,
    )
    write_replay_imitation_training_artifacts(
        output_dir=m41_out,
        run_body=run,
        report_body=rep,
    )
    out = tmp_path / "cmp"
    cmd = [
        sys.executable,
        "-m",
        "starlab.evaluation.emit_learned_agent_comparison",
        "--contract",
        str(M28_FIX / "benchmark_contract_m28.json"),
        "--dataset",
        str(M26_FIX / "replay_training_dataset.json"),
        "--bundle",
        str(tmp_path / "b1"),
        "--baseline",
        str(M27_FIX / "replay_imitation_baseline.json"),
        "--m41",
        "m41_run",
        str(tmp_path / "m41_out" / "replay_imitation_training_run.json"),
        str(tmp_path / "m41_out"),
        "--output-dir",
        str(out),
    ]
    proc = subprocess.run(cmd, check=False, capture_output=True, text=True, cwd=str(REPO_ROOT))
    assert proc.returncode == 0, proc.stderr
    assert (out / "learned_agent_comparison.json").is_file()
    assert (out / "learned_agent_comparison_report.json").is_file()


def _m42_emit_cmd(
    tmp_path: Path,
    *,
    benchmark_flag: str,
    benchmark_path: Path,
) -> subprocess.CompletedProcess[str]:
    _materialize_m14_bundle_directory(tmp_path / "b1")
    ds = json.loads((M26_FIX / "replay_training_dataset.json").read_text(encoding="utf-8"))
    contract = build_agent_training_program_contract()
    m41_out = tmp_path / "m41_out"
    run, rep, _wp = build_replay_imitation_training_run(
        bundle_dirs=[tmp_path / "b1"],
        dataset=ds,
        emit_weights=True,
        output_dir=m41_out,
        seed=42,
        training_program_contract=contract,
    )
    write_replay_imitation_training_artifacts(
        output_dir=m41_out,
        run_body=run,
        report_body=rep,
    )
    out = tmp_path / "cmp"
    cmd = [
        sys.executable,
        "-m",
        "starlab.evaluation.emit_learned_agent_comparison",
        benchmark_flag,
        str(benchmark_path),
        "--dataset",
        str(M26_FIX / "replay_training_dataset.json"),
        "--bundle",
        str(tmp_path / "b1"),
        "--baseline",
        str(M27_FIX / "replay_imitation_baseline.json"),
        "--m41",
        "m41_run",
        str(tmp_path / "m41_out" / "replay_imitation_training_run.json"),
        str(tmp_path / "m41_out"),
        "--output-dir",
        str(out),
    ]
    return subprocess.run(cmd, check=False, capture_output=True, text=True, cwd=str(REPO_ROOT))


def test_m42_emit_cli_benchmark_contract_flag(tmp_path: Path) -> None:
    proc = _m42_emit_cmd(
        tmp_path,
        benchmark_flag="--benchmark-contract",
        benchmark_path=M28_FIX / "benchmark_contract_m28.json",
    )
    assert proc.returncode == 0, proc.stderr


def test_m42_emit_cli_contract_alias(tmp_path: Path) -> None:
    proc = _m42_emit_cmd(
        tmp_path,
        benchmark_flag="--contract",
        benchmark_path=M28_FIX / "benchmark_contract_m28.json",
    )
    assert proc.returncode == 0, proc.stderr


def test_m42_emit_cli_benchmark_and_contract_conflict(tmp_path: Path) -> None:
    _materialize_m14_bundle_directory(tmp_path / "b1")
    ds = json.loads((M26_FIX / "replay_training_dataset.json").read_text(encoding="utf-8"))
    contract = build_agent_training_program_contract()
    m41_out = tmp_path / "m41_out"
    run, rep, _wp = build_replay_imitation_training_run(
        bundle_dirs=[tmp_path / "b1"],
        dataset=ds,
        emit_weights=True,
        output_dir=m41_out,
        seed=42,
        training_program_contract=contract,
    )
    write_replay_imitation_training_artifacts(output_dir=m41_out, run_body=run, report_body=rep)
    p_other = tmp_path / "other_bench.json"
    p_other.write_text(
        json.dumps({"not": "a valid m28 bench for this test"}),
        encoding="utf-8",
    )
    cmd = [
        sys.executable,
        "-m",
        "starlab.evaluation.emit_learned_agent_comparison",
        "--benchmark-contract",
        str(M28_FIX / "benchmark_contract_m28.json"),
        "--contract",
        str(p_other),
        "--dataset",
        str(M26_FIX / "replay_training_dataset.json"),
        "--bundle",
        str(tmp_path / "b1"),
        "--baseline",
        str(M27_FIX / "replay_imitation_baseline.json"),
        "--m41",
        "m41_run",
        str(m41_out / "replay_imitation_training_run.json"),
        str(m41_out),
        "--output-dir",
        str(tmp_path / "cmp"),
    ]
    proc = subprocess.run(cmd, check=False, capture_output=True, text=True, cwd=str(REPO_ROOT))
    assert proc.returncode == 2
    assert "disagree" in proc.stderr.lower()


def test_m42_emit_cli_training_program_contract_from_disk(tmp_path: Path) -> None:
    _materialize_m14_bundle_directory(tmp_path / "b1")
    ds = json.loads((M26_FIX / "replay_training_dataset.json").read_text(encoding="utf-8"))
    tp_dir = tmp_path / "tp"
    write_agent_training_program_contract(tp_dir)
    tp_path = tp_dir / "agent_training_program_contract.json"
    contract = build_agent_training_program_contract()
    m41_out = tmp_path / "m41_out"
    run, rep, _wp = build_replay_imitation_training_run(
        bundle_dirs=[tmp_path / "b1"],
        dataset=ds,
        emit_weights=True,
        output_dir=m41_out,
        seed=42,
        training_program_contract=contract,
    )
    write_replay_imitation_training_artifacts(output_dir=m41_out, run_body=run, report_body=rep)
    out = tmp_path / "cmp"
    cmd = [
        sys.executable,
        "-m",
        "starlab.evaluation.emit_learned_agent_comparison",
        "--benchmark-contract",
        str(M28_FIX / "benchmark_contract_m28.json"),
        "--training-program-contract",
        str(tp_path),
        "--dataset",
        str(M26_FIX / "replay_training_dataset.json"),
        "--bundle",
        str(tmp_path / "b1"),
        "--baseline",
        str(M27_FIX / "replay_imitation_baseline.json"),
        "--m41",
        "m41_run",
        str(m41_out / "replay_imitation_training_run.json"),
        str(m41_out),
        "--output-dir",
        str(out),
    ]
    proc = subprocess.run(cmd, check=False, capture_output=True, text=True, cwd=str(REPO_ROOT))
    assert proc.returncode == 0, proc.stderr
    assert (out / "learned_agent_comparison.json").is_file()


def test_m42_m41_training_program_contract_mismatch_fails(tmp_path: Path) -> None:
    _materialize_m14_bundle_directory(tmp_path / "b1")
    ds = json.loads((M26_FIX / "replay_training_dataset.json").read_text(encoding="utf-8"))
    contract = build_agent_training_program_contract()
    m41_out = tmp_path / "m41_out"
    run, rep, _wp = build_replay_imitation_training_run(
        bundle_dirs=[tmp_path / "b1"],
        dataset=ds,
        emit_weights=True,
        output_dir=m41_out,
        seed=42,
        training_program_contract=contract,
    )
    run_bad = dict(run)
    sha = str(run_bad["training_program_contract_sha256"])
    run_bad["training_program_contract_sha256"] = "0" + sha[1:]
    write_replay_imitation_training_artifacts(output_dir=m41_out, run_body=run_bad, report_body=rep)

    baseline = json.loads((M27_FIX / "replay_imitation_baseline.json").read_text(encoding="utf-8"))
    bench = json.loads((M28_FIX / "benchmark_contract_m28.json").read_text(encoding="utf-8"))
    specs = [
        ComparisonCandidateSpec(
            candidate_id="m27_frozen_baseline",
            source_type="m27_frozen_baseline",
            source_artifact_path=str(M27_FIX / "replay_imitation_baseline.json"),
            baseline_body=baseline,
        ),
        ComparisonCandidateSpec(
            candidate_id="m41_run",
            source_type="m41_training_run",
            source_artifact_path=str(m41_out / "replay_imitation_training_run.json"),
            training_run_body=run_bad,
            training_run_dir=m41_out,
        ),
    ]
    with pytest.raises(ValueError, match="training_program_contract_sha256"):
        build_learned_agent_comparison_artifacts(
            benchmark_contract=bench,
            dataset=ds,
            bundle_dirs=[tmp_path / "b1"],
            evaluation_split="test",
            training_program_contract=contract,
            candidates=specs,
        )
