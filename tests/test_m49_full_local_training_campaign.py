"""M49 full local training campaign contract + preflight."""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path

import pytest
from starlab.hierarchy.hierarchical_training_models import HIERARCHICAL_TRAINING_RUN_FILENAME
from starlab.hierarchy.hierarchical_training_pipeline import build_hierarchical_training_run
from starlab.runs.json_util import canonical_json_dumps
from starlab.training.emit_full_local_training_campaign_contract import (
    main as emit_campaign_main,
)
from starlab.training.emit_full_local_training_campaign_preflight import (
    main as preflight_main,
)
from starlab.training.full_local_training_campaign_io import emit_full_local_training_campaign
from starlab.training.full_local_training_campaign_models import (
    FULL_LOCAL_TRAINING_CAMPAIGN_VERSION,
)
from starlab.training.full_local_training_campaign_preflight import run_campaign_preflight
from starlab.training.training_program_io import build_agent_training_program_contract
from starlab.v15.run_v15_m27_sc2_rollout_training_loop_integration import (
    main as m27_integration_main,
)

REPO_ROOT = Path(__file__).resolve().parents[1]
M14_FIX = REPO_ROOT / "tests" / "fixtures" / "m14"
M26_FIX = REPO_ROOT / "tests" / "fixtures" / "m26"
M28_FIX = REPO_ROOT / "tests" / "fixtures" / "m28"
MATCH_FAKE = REPO_ROOT / "tests" / "fixtures" / "match_fake_m02.json"


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


def _build_m43_run_dir(tmp_path: Path) -> tuple[Path, Path]:
    bundle = tmp_path / "b1"
    _materialize_m14_bundle_directory(bundle)
    ds = json.loads((M26_FIX / "replay_training_dataset.json").read_text(encoding="utf-8"))
    c = build_agent_training_program_contract()
    out = tmp_path / "m43_run"
    out.mkdir(parents=True, exist_ok=True)
    run, _rep, _wp = build_hierarchical_training_run(
        bundle_dirs=[bundle],
        dataset=ds,
        emit_weights=True,
        output_dir=out,
        seed=42,
        training_program_contract=c,
    )
    (out / HIERARCHICAL_TRAINING_RUN_FILENAME).write_text(
        canonical_json_dumps(run),
        encoding="utf-8",
    )
    return out, bundle


def test_m49_campaign_emit_and_preflight_fixture_mode(tmp_path: Path) -> None:
    m43_dir, _bundle = _build_m43_run_dir(tmp_path)
    shutil.copy(MATCH_FAKE, tmp_path / "match.json")
    bench = M28_FIX / "benchmark_contract_m28.json"
    out = tmp_path / "campaign"
    c, _r, _cp, _rp = emit_full_local_training_campaign(
        benchmark_contract_path=bench,
        campaign_id="test_campaign_a",
        hierarchical_training_run_dir=m43_dir,
        match_config_path=tmp_path / "match.json",
        output_dir=out,
        planned_weighted_refit=False,
        runtime_mode="fixture_stub_ci",
        training_program_contract_path=None,
    )
    assert c["campaign_version"] == FULL_LOCAL_TRAINING_CAMPAIGN_VERSION
    assert "campaign_sha256" in c
    assert c["authorization_posture"]["status"] == "planned_charter_only"

    ok, receipt = run_campaign_preflight(
        contract_path=out / "full_local_training_campaign_contract.json"
    )
    assert ok
    assert receipt["preflight_ok"] is True
    assert all(x["ok"] for x in receipt["checks"])


def test_m49_preflight_accepts_optional_m27_rollout_json(tmp_path: Path) -> None:
    """V15-M27 rollout artifact binds into M49 preflight checks when supplied."""

    m43_dir, _bundle = _build_m43_run_dir(tmp_path)
    shutil.copy(MATCH_FAKE, tmp_path / "match.json")
    bench = M28_FIX / "benchmark_contract_m28.json"
    out = tmp_path / "campaign"
    emit_full_local_training_campaign(
        benchmark_contract_path=bench,
        campaign_id="with_m27",
        hierarchical_training_run_dir=m43_dir,
        match_config_path=tmp_path / "match.json",
        output_dir=out,
        planned_weighted_refit=False,
        runtime_mode="fixture_stub_ci",
        training_program_contract_path=None,
    )
    m27_dir = tmp_path / "m27"
    assert m27_integration_main(["--fixture-only", "--output-dir", str(m27_dir)]) == 0
    m27_p = m27_dir / "v15_sc2_rollout_training_loop_integration.json"
    ok, receipt = run_campaign_preflight(
        contract_path=out / "full_local_training_campaign_contract.json",
        m27_sc2_rollout_json=m27_p,
    )
    assert ok
    chk = next(
        (x for x in receipt["checks"] if x.get("check_id") == "m27_sc2_rollout_integration"),
        None,
    )
    assert chk is not None
    assert chk.get("ok") is True


def test_m49_campaign_deterministic_same_paths(tmp_path: Path) -> None:
    """Same inputs and same output_dir produce identical campaign_sha256 (re-emission)."""

    m43_dir, _bundle = _build_m43_run_dir(tmp_path)
    shutil.copy(MATCH_FAKE, tmp_path / "match.json")
    bench = M28_FIX / "benchmark_contract_m28.json"
    out = tmp_path / "campaign"
    a, _, _, _ = emit_full_local_training_campaign(
        benchmark_contract_path=bench,
        campaign_id="same",
        hierarchical_training_run_dir=m43_dir,
        match_config_path=tmp_path / "match.json",
        output_dir=out,
        planned_weighted_refit=False,
        runtime_mode="fixture_stub_ci",
        training_program_contract_path=None,
    )
    b, _, _, _ = emit_full_local_training_campaign(
        benchmark_contract_path=bench,
        campaign_id="same",
        hierarchical_training_run_dir=m43_dir,
        match_config_path=tmp_path / "match.json",
        output_dir=out,
        planned_weighted_refit=False,
        runtime_mode="fixture_stub_ci",
        training_program_contract_path=None,
    )
    assert a["campaign_sha256"] == b["campaign_sha256"]


def test_m49_preflight_fails_missing_weights(tmp_path: Path) -> None:
    m43_dir, _bundle = _build_m43_run_dir(tmp_path)
    shutil.copy(MATCH_FAKE, tmp_path / "match.json")
    bench = M28_FIX / "benchmark_contract_m28.json"
    out = tmp_path / "campaign"
    emit_full_local_training_campaign(
        benchmark_contract_path=bench,
        campaign_id="broken_weights",
        hierarchical_training_run_dir=m43_dir,
        match_config_path=tmp_path / "match.json",
        output_dir=out,
        planned_weighted_refit=False,
        runtime_mode="fixture_stub_ci",
        training_program_contract_path=None,
    )
    wpath = m43_dir / "weights" / "hierarchical_training_sklearn_bundle.joblib"
    wpath.unlink()
    ok, receipt = run_campaign_preflight(
        contract_path=out / "full_local_training_campaign_contract.json"
    )
    assert not ok
    assert receipt["preflight_ok"] is False


def test_m49_cli_contract_module_smoke(tmp_path: Path) -> None:
    m43_dir, _bundle = _build_m43_run_dir(tmp_path)
    shutil.copy(MATCH_FAKE, tmp_path / "match.json")
    bench = M28_FIX / "benchmark_contract_m28.json"
    out = tmp_path / "campaign"
    code = emit_campaign_main(
        [
            "--campaign-id",
            "cli_smoke",
            "--output-dir",
            str(out),
            "--hierarchical-training-run-dir",
            str(m43_dir),
            "--benchmark-contract",
            str(bench),
            "--match-config",
            str(tmp_path / "match.json"),
            "--runtime-mode",
            "fixture_stub_ci",
        ],
    )
    assert code == 0
    assert (out / "full_local_training_campaign_contract.json").is_file()


def test_m49_cli_preflight_module_smoke(tmp_path: Path) -> None:
    m43_dir, _bundle = _build_m43_run_dir(tmp_path)
    shutil.copy(MATCH_FAKE, tmp_path / "match.json")
    bench = M28_FIX / "benchmark_contract_m28.json"
    out = tmp_path / "campaign"
    emit_campaign_main(
        [
            "--campaign-id",
            "pf_smoke",
            "--output-dir",
            str(out),
            "--hierarchical-training-run-dir",
            str(m43_dir),
            "--benchmark-contract",
            str(bench),
            "--match-config",
            str(tmp_path / "match.json"),
            "--runtime-mode",
            "fixture_stub_ci",
        ],
    )
    code = preflight_main(
        [
            "--campaign-contract",
            str(out / "full_local_training_campaign_contract.json"),
            "--output-dir",
            str(out),
        ],
    )
    assert code == 0
    assert (out / "campaign_preflight_receipt.json").is_file()


@pytest.mark.parametrize(
    "module",
    (
        "starlab.training.emit_full_local_training_campaign_contract",
        "starlab.training.emit_full_local_training_campaign_preflight",
    ),
)
def test_m49_cli_module_invocation(module: str) -> None:
    r = subprocess.run(
        [sys.executable, "-m", module, "--help"],
        check=False,
        capture_output=True,
        text=True,
        cwd=REPO_ROOT,
    )
    assert r.returncode == 0
    assert "usage" in (r.stdout + r.stderr).lower()
