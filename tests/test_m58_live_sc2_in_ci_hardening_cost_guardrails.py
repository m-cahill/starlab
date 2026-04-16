"""M58 live SC2-in-CI hardening & cost guardrails."""

from __future__ import annotations

import json
import multiprocessing as mp
import shutil
import time
from pathlib import Path

from starlab.hierarchy.hierarchical_training_models import HIERARCHICAL_TRAINING_RUN_FILENAME
from starlab.hierarchy.hierarchical_training_pipeline import build_hierarchical_training_run
from starlab.runs.json_util import canonical_json_dumps, sha256_hex_of_canonical_json
from starlab.sc2.emit_live_sc2_in_ci_guardrails import (
    write_live_sc2_in_ci_hardening_guardrails_artifacts,
)
from starlab.sc2.emit_live_sc2_in_ci_preflight import main as preflight_main
from starlab.sc2.live_sc2_ci_guardrails import (
    build_live_sc2_in_ci_hardening_guardrails_artifact,
)
from starlab.sc2.live_sc2_ci_models import (
    LIVE_SC2_IN_CI_HARDENING_GUARDRAILS_CONTRACT_ID,
    LIVE_SC2_IN_CI_PREFLIGHT_RECEIPT_CONTRACT_ID,
    M57_RUNNER_PROFILE_M44_SINGLE_VALIDATION_V1,
    M58_GUARDRAIL_PROFILE_M57_SINGLE_VALIDATION_COST_GUARDRAILS_V1,
    M58_MAX_ARTIFACT_RETENTION_DAYS,
    M58_MAX_TIMEOUT_MINUTES,
)
from starlab.sc2.live_sc2_ci_preflight import evaluate_live_sc2_in_ci_preflight
from starlab.sc2.live_sc2_ci_preflight_lock import (
    release_m58_live_sc2_preflight_lock,
    try_acquire_m58_live_sc2_preflight_lock,
)
from starlab.training.training_program_io import build_agent_training_program_contract

REPO_ROOT = Path(__file__).resolve().parents[1]
M14_FIX = REPO_ROOT / "tests" / "fixtures" / "m14"
M26_FIX = REPO_ROOT / "tests" / "fixtures" / "m26"
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


def test_emit_guardrails_is_deterministic(tmp_path: Path) -> None:
    a = write_live_sc2_in_ci_hardening_guardrails_artifacts(tmp_path / "a")
    b = write_live_sc2_in_ci_hardening_guardrails_artifacts(tmp_path / "b")
    assert a[0].read_text(encoding="utf-8") == b[0].read_text(encoding="utf-8")
    assert a[1].read_text(encoding="utf-8") == b[1].read_text(encoding="utf-8")


def test_guardrails_contract_and_exactly_one_profile() -> None:
    obj = build_live_sc2_in_ci_hardening_guardrails_artifact()
    assert obj["contract_id"] == LIVE_SC2_IN_CI_HARDENING_GUARDRAILS_CONTRACT_ID
    assert len(obj["guardrail_profiles"]) == 1
    assert (
        obj["guardrail_profiles"][0]["guardrail_profile_id"]
        == M58_GUARDRAIL_PROFILE_M57_SINGLE_VALIDATION_COST_GUARDRAILS_V1
    )
    assert (
        obj["guardrail_profiles"][0]["runner_profile_id"]
        == M57_RUNNER_PROFILE_M44_SINGLE_VALIDATION_V1
    )


def test_guardrails_report_sha256(tmp_path: Path) -> None:
    write_live_sc2_in_ci_hardening_guardrails_artifacts(tmp_path)
    g = json.loads(
        (tmp_path / "live_sc2_in_ci_hardening_guardrails.json").read_text(encoding="utf-8")
    )
    r = json.loads(
        (tmp_path / "live_sc2_in_ci_hardening_guardrails_report.json").read_text(encoding="utf-8")
    )
    assert r["guardrails_canonical_sha256"] == sha256_hex_of_canonical_json(g)


def test_preflight_fixture_clears(tmp_path: Path) -> None:
    m43 = _build_m43_run_dir(tmp_path)
    wpath = next(m43.rglob("*.joblib"))
    shutil.copy(MATCH_FAKE, tmp_path / "match.json")

    ok, rec, rep, _ = evaluate_live_sc2_in_ci_preflight(
        m43_run_dir=m43,
        weights_path=wpath,
        match_config=tmp_path / "match.json",
        runtime_mode="fixture_stub_ci",
        workflow_trigger="workflow_dispatch",
        runner_labels_csv="Windows,self-hosted,starlab-sc2",
        timeout_minutes=M58_MAX_TIMEOUT_MINUTES,
        artifact_retention_days=M58_MAX_ARTIFACT_RETENTION_DAYS,
        live_sc2_confirmed=False,
    )
    assert ok
    assert rec["preflight_status"] == "cleared"
    assert rec["contract_id"] == LIVE_SC2_IN_CI_PREFLIGHT_RECEIPT_CONTRACT_ID
    assert rec["sc2_probe_status"] == "not_applicable"
    assert rep["receipt_canonical_sha256"] == sha256_hex_of_canonical_json(rec)


def test_preflight_live_without_confirmation_fails(tmp_path: Path) -> None:
    m43 = _build_m43_run_dir(tmp_path)
    wpath = next(m43.rglob("*.joblib"))
    shutil.copy(MATCH_FAKE, tmp_path / "match.json")

    ok, rec, _, _ = evaluate_live_sc2_in_ci_preflight(
        m43_run_dir=m43,
        weights_path=wpath,
        match_config=tmp_path / "match.json",
        runtime_mode="local_live_sc2",
        workflow_trigger="workflow_dispatch",
        runner_labels_csv="Linux,self-hosted,starlab-sc2",
        timeout_minutes=M58_MAX_TIMEOUT_MINUTES,
        artifact_retention_days=M58_MAX_ARTIFACT_RETENTION_DAYS,
        live_sc2_confirmed=False,
    )
    assert not ok
    assert rec["preflight_status"] == "failed_preconditions"


def test_preflight_timeout_over_max_fails(tmp_path: Path) -> None:
    m43 = _build_m43_run_dir(tmp_path)
    wpath = next(m43.rglob("*.joblib"))
    shutil.copy(MATCH_FAKE, tmp_path / "match.json")

    ok, rec, _, _ = evaluate_live_sc2_in_ci_preflight(
        m43_run_dir=m43,
        weights_path=wpath,
        match_config=tmp_path / "match.json",
        runtime_mode="fixture_stub_ci",
        workflow_trigger="workflow_dispatch",
        runner_labels_csv="Linux,self-hosted,starlab-sc2",
        timeout_minutes=31,
        artifact_retention_days=M58_MAX_ARTIFACT_RETENTION_DAYS,
        live_sc2_confirmed=False,
    )
    assert not ok
    assert any("timeout" in x for x in rec["failure_reasons"])


def test_preflight_retention_over_max_fails(tmp_path: Path) -> None:
    m43 = _build_m43_run_dir(tmp_path)
    wpath = next(m43.rglob("*.joblib"))
    shutil.copy(MATCH_FAKE, tmp_path / "match.json")

    ok, rec, _, _ = evaluate_live_sc2_in_ci_preflight(
        m43_run_dir=m43,
        weights_path=wpath,
        match_config=tmp_path / "match.json",
        runtime_mode="fixture_stub_ci",
        workflow_trigger="workflow_dispatch",
        runner_labels_csv="Linux,self-hosted,starlab-sc2",
        timeout_minutes=M58_MAX_TIMEOUT_MINUTES,
        artifact_retention_days=8,
        live_sc2_confirmed=False,
    )
    assert not ok


def _child_hold_lock(out: str, q: mp.Queue[tuple[bool, str, str]]) -> None:
    p = Path(out)
    ok, lp, msg = try_acquire_m58_live_sc2_preflight_lock(output_dir=p)
    q.put((ok, str(lp), msg))
    if ok:
        time.sleep(3)
        release_m58_live_sc2_preflight_lock(Path(lp))


def test_lock_denied_when_other_process_holds_lock(tmp_path: Path) -> None:
    out = str(tmp_path / "shared")
    q: mp.Queue[tuple[bool, str, str]] = mp.Queue()
    proc = mp.Process(target=_child_hold_lock, args=(out, q))
    proc.start()
    try:
        got_ok, lp_s, _msg = q.get(timeout=5)
        assert got_ok is True
        ok2, _lp2, _ = try_acquire_m58_live_sc2_preflight_lock(output_dir=Path(out))
        assert ok2 is False
    finally:
        proc.join(timeout=10)
        if proc.is_alive():
            proc.terminate()


def test_workflow_manual_dispatch_and_hardening() -> None:
    wf = REPO_ROOT / ".github" / "workflows" / "live-sc2-controlled-runner.yml"
    yml = wf.read_text(encoding="utf-8")
    assert "workflow_dispatch:" in yml
    assert "pull_request:" not in yml
    assert "push:" not in yml
    assert "permissions:" in yml and "contents: read" in yml
    assert "concurrency:" in yml
    assert "timeout-minutes: 30" in yml
    assert "retention-days: 7" in yml
    assert "strategy:" not in yml
    assert "retry:" not in yml


def test_governance_ledger_m58_m57_m59() -> None:
    text = (REPO_ROOT / "docs" / "starlab.md").read_text(encoding="utf-8")
    assert "### M58" in text
    assert "### M57" in text
    assert "### M59" in text
    sec11 = text.split("## 11. Current milestone")[1].split("## 12")[0]
    assert "m58" in sec11.lower() and "closed" in sec11.lower()
    assert "m57" in sec11.lower() and "closed" in sec11.lower()
    assert "m59" in sec11.lower() and ("stub" in sec11.lower() or "planned" in sec11.lower())
    assert "live_sc2_in_ci" in text.lower() or "live sc2" in text.lower()
    assert "merge" in text.lower() and "live" in text.lower()


def test_ledger_live_sc2_guardrail_profile_table() -> None:
    text = (REPO_ROOT / "docs" / "starlab.md").read_text(encoding="utf-8")
    assert "Phase VII bounded live-SC2-in-CI guardrail profiles" in text
    assert M58_GUARDRAIL_PROFILE_M57_SINGLE_VALIDATION_COST_GUARDRAILS_V1 in text


def test_preflight_cli_writes_files(tmp_path: Path) -> None:
    m43 = _build_m43_run_dir(tmp_path)
    wpath = next(m43.rglob("*.joblib"))
    shutil.copy(MATCH_FAKE, tmp_path / "match.json")
    out = tmp_path / "pf"
    code = preflight_main(
        [
            "--m43-run",
            str(m43),
            "--weights",
            str(wpath),
            "--match-config",
            str(tmp_path / "match.json"),
            "--runtime-mode",
            "fixture_stub_ci",
            "--workflow-trigger",
            "workflow_dispatch",
            "--runner-labels",
            "Windows,self-hosted,starlab-sc2",
            "--timeout-minutes",
            str(M58_MAX_TIMEOUT_MINUTES),
            "--artifact-retention-days",
            str(M58_MAX_ARTIFACT_RETENTION_DAYS),
            "--live-sc2-confirmed",
            "false",
            "--output-dir",
            str(out),
            "--skip-advisory-lock",
        ],
    )
    assert code == 0
    assert (out / "live_sc2_in_ci_preflight_receipt.json").is_file()


def test_m58_sc2_modules_no_replays_import() -> None:
    forbidden = ("starlab.replays", "s2protocol")
    for name in (
        "live_sc2_ci_guardrails.py",
        "emit_live_sc2_in_ci_guardrails.py",
        "live_sc2_ci_preflight.py",
        "emit_live_sc2_in_ci_preflight.py",
        "live_sc2_ci_preflight_lock.py",
    ):
        p = REPO_ROOT / "starlab" / "sc2" / name
        text = p.read_text(encoding="utf-8")
        for sub in forbidden:
            assert sub not in text, f"{name} must not reference {sub}"
