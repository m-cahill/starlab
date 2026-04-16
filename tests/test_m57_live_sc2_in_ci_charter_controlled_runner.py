"""M57 live SC2-in-CI charter & controlled runner."""

from __future__ import annotations

import json
import shutil
from pathlib import Path

import pytest
from starlab.hierarchy.hierarchical_training_models import HIERARCHICAL_TRAINING_RUN_FILENAME
from starlab.hierarchy.hierarchical_training_pipeline import build_hierarchical_training_run
from starlab.runs.json_util import canonical_json_dumps, sha256_hex_of_canonical_json
from starlab.sc2.emit_live_sc2_in_ci_charter import write_live_sc2_in_ci_charter_artifacts
from starlab.sc2.live_sc2_ci_charter import (
    build_live_sc2_in_ci_charter_artifact,
    build_live_sc2_in_ci_charter_report,
)
from starlab.sc2.live_sc2_ci_controlled_runner import (
    assert_m43_candidate_or_raise,
    assert_no_local_live_stub_fallback_or_raise,
    run_m57_controlled_runner,
)
from starlab.sc2.live_sc2_ci_models import (
    LIVE_SC2_IN_CI_CHARTER_CONTRACT_ID,
    LIVE_SC2_IN_CI_CONTROLLED_RUNNER_RECEIPT_CONTRACT_ID,
    M44_STUB_REPLAY_WARNING,
    M57_RUNNER_PROFILE_M44_SINGLE_VALIDATION_V1,
)
from starlab.sc2.run_live_sc2_in_ci_controlled_runner import main as runner_cli_main
from starlab.training.training_program_io import build_agent_training_program_contract

REPO_ROOT = Path(__file__).resolve().parents[1]
M14_FIX = REPO_ROOT / "tests" / "fixtures" / "m14"
M26_FIX = REPO_ROOT / "tests" / "fixtures" / "m26"
MATCH_FAKE = REPO_ROOT / "tests" / "fixtures" / "match_fake_m02.json"

M57_SC2_MODULES = (
    "live_sc2_ci_models.py",
    "live_sc2_ci_charter.py",
    "emit_live_sc2_in_ci_charter.py",
    "live_sc2_ci_controlled_runner.py",
    "run_live_sc2_in_ci_controlled_runner.py",
)


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


def _build_m43_run_dir(tmp_path: Path) -> Path:
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
    return out


def test_emit_live_sc2_in_ci_charter_is_deterministic(tmp_path: Path) -> None:
    p1 = write_live_sc2_in_ci_charter_artifacts(tmp_path / "a")
    p2 = write_live_sc2_in_ci_charter_artifacts(tmp_path / "b")
    assert p1[0].read_text(encoding="utf-8") == p2[0].read_text(encoding="utf-8")
    assert p1[1].read_text(encoding="utf-8") == p2[1].read_text(encoding="utf-8")


def test_charter_contract_and_single_runner_profile() -> None:
    obj = build_live_sc2_in_ci_charter_artifact()
    assert obj["contract_id"] == LIVE_SC2_IN_CI_CHARTER_CONTRACT_ID
    assert obj["bounded_runner_profile_id"] == M57_RUNNER_PROFILE_M44_SINGLE_VALIDATION_V1
    assert obj["milestone"] == "M57"


def test_charter_report_sha256_matches() -> None:
    charter = build_live_sc2_in_ci_charter_artifact()
    report = build_live_sc2_in_ci_charter_report(charter_obj=charter)
    assert report["charter_canonical_sha256"] == sha256_hex_of_canonical_json(charter)


def test_controlled_runner_fixture_mode_receipt_deterministic(tmp_path: Path) -> None:
    m43_dir = _build_m43_run_dir(tmp_path)
    out = tmp_path / "m57_out"
    shutil.copy(MATCH_FAKE, tmp_path / "match.json")

    r1 = run_m57_controlled_runner(
        match_config=tmp_path / "match.json",
        m43_run_dir=m43_dir,
        output_dir=out,
        runtime_mode="fixture_stub_ci",
    )
    r2 = run_m57_controlled_runner(
        match_config=tmp_path / "match.json",
        m43_run_dir=m43_dir,
        output_dir=tmp_path / "m57_out2",
        runtime_mode="fixture_stub_ci",
    )
    assert r1.receipt["execution_status"] == "executed_fixture_stub"
    assert r1.receipt["contract_id"] == LIVE_SC2_IN_CI_CONTROLLED_RUNNER_RECEIPT_CONTRACT_ID
    assert r1.receipt["runner_profile_id"] == M57_RUNNER_PROFILE_M44_SINGLE_VALIDATION_V1
    assert r1.receipt["requested_runtime_mode"] == "fixture_stub_ci"
    assert r1.receipt["resolved_runtime_mode"] == "fixture_stub_ci"
    assert r1.receipt["m44_validation_run_sha256"] == r2.receipt["m44_validation_run_sha256"]


def test_receipt_report_sha256_matches_receipt(tmp_path: Path) -> None:
    m43_dir = _build_m43_run_dir(tmp_path)
    out = tmp_path / "m57_out"
    shutil.copy(MATCH_FAKE, tmp_path / "match.json")

    r = run_m57_controlled_runner(
        match_config=tmp_path / "match.json",
        m43_run_dir=m43_dir,
        output_dir=out,
        runtime_mode="fixture_stub_ci",
    )
    assert r.report["receipt_canonical_sha256"] == sha256_hex_of_canonical_json(r.receipt)


def test_runner_rejects_non_m43_candidate(tmp_path: Path) -> None:
    bad = tmp_path / "bad_m43"
    bad.mkdir(parents=True, exist_ok=True)
    (bad / HIERARCHICAL_TRAINING_RUN_FILENAME).write_text(
        json.dumps(
            {
                "training_run_sha256": "a" * 64,
                "training_run_version": "starlab.replay_imitation_training_run.v1",
            },
        ),
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="M43 hierarchical"):
        assert_m43_candidate_or_raise(hierarchical_training_run_dir=bad)


def test_no_silent_fallback_raises_on_stub_warning() -> None:
    with pytest.raises(RuntimeError, match="M57 policy"):
        assert_no_local_live_stub_fallback_or_raise(
            validation_run={
                "warnings": [M44_STUB_REPLAY_WARNING],
            },
        )


def test_local_live_skip_by_policy_emits_skipped_receipt(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    m43_dir = _build_m43_run_dir(tmp_path)
    out = tmp_path / "m57_skip"
    shutil.copy(MATCH_FAKE, tmp_path / "match.json")

    import starlab.sc2.live_sc2_ci_controlled_runner as cr

    def _probe_fail() -> tuple[bool, list[str]]:
        return False, ["no binary"]

    monkeypatch.setattr(cr, "live_sc2_binary_available_for_bounded_run", _probe_fail)

    r = run_m57_controlled_runner(
        match_config=tmp_path / "match.json",
        m43_run_dir=m43_dir,
        output_dir=out,
        runtime_mode="local_live_sc2",
        skip_live_when_prereqs_missing=True,
    )
    assert r.m44_output_dir is None
    assert r.receipt["execution_status"] == "skipped_by_policy"
    assert r.receipt["skip_reason"] == "live_sc2_prerequisites_not_satisfied_skip_by_policy"


def test_local_live_without_prereqs_raises_without_skip(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    m43_dir = _build_m43_run_dir(tmp_path)
    out = tmp_path / "m57_fail"
    shutil.copy(MATCH_FAKE, tmp_path / "match.json")

    import starlab.sc2.live_sc2_ci_controlled_runner as cr

    def _probe_fail() -> tuple[bool, list[str]]:
        return False, ["no binary"]

    monkeypatch.setattr(cr, "live_sc2_binary_available_for_bounded_run", _probe_fail)

    with pytest.raises(RuntimeError, match="SC2 binary prerequisites"):
        run_m57_controlled_runner(
            match_config=tmp_path / "match.json",
            m43_run_dir=m43_dir,
            output_dir=out,
            runtime_mode="local_live_sc2",
            skip_live_when_prereqs_missing=False,
        )


def test_runner_cli_writes_receipt_files(tmp_path: Path) -> None:
    m43_dir = _build_m43_run_dir(tmp_path)
    out = tmp_path / "m57_cli"
    shutil.copy(MATCH_FAKE, tmp_path / "match.json")

    code = runner_cli_main(
        [
            "--m43-run",
            str(m43_dir),
            "--match-config",
            str(tmp_path / "match.json"),
            "--output-dir",
            str(out),
            "--runtime-mode",
            "fixture_stub_ci",
        ],
    )
    assert code == 0
    assert (out / "live_sc2_in_ci_controlled_runner_receipt.json").is_file()
    assert (out / "live_sc2_in_ci_controlled_runner_receipt_report.json").is_file()


def test_workflow_live_sc2_is_manual_dispatch_only() -> None:
    text = (REPO_ROOT / ".github" / "workflows" / "live-sc2-controlled-runner.yml").read_text(
        encoding="utf-8",
    )
    assert "workflow_dispatch:" in text
    assert "pull_request:" not in text
    assert "push:" not in text


def test_m57_sc2_modules_do_not_import_replays_or_s2protocol() -> None:
    forbidden_substrings = ("starlab.replays", "s2protocol")
    for module in M57_SC2_MODULES:
        p = REPO_ROOT / "starlab" / "sc2" / module
        text = p.read_text(encoding="utf-8")
        for sub in forbidden_substrings:
            assert sub not in text, f"{module} must not reference {sub}"


def test_ledger_m57_m58_m56_governance() -> None:
    text = (REPO_ROOT / "docs" / "starlab.md").read_text(encoding="utf-8")
    assert "### M57" in text
    assert "### M58" in text
    assert "### M56" in text
    assert "M56" in text and "closed" in text.lower()
    assert "M58" in text and "closed" in text.lower()
    assert "live_sc2_in_ci" in text or "live SC2" in text
    assert "not yet proved" in text.lower() or "not proved" in text.lower()
    assert "merge" in text.lower() and "live" in text.lower()
    sec11 = text.split("## 11. Current milestone")[1].split("## 12")[0]
    assert "m57" in sec11.lower() and "m56" in sec11.lower() and "closed" in sec11.lower()
    assert "m58" in sec11.lower() and "closed" in sec11.lower()
    assert "m59" in sec11.lower()


def test_ledger_phase_vii_live_sc2_runner_profile_table() -> None:
    text = (REPO_ROOT / "docs" / "starlab.md").read_text(encoding="utf-8")
    assert "#### Phase VII bounded live-SC2-in-CI runner profiles" in text
    assert M57_RUNNER_PROFILE_M44_SINGLE_VALIDATION_V1 in text
