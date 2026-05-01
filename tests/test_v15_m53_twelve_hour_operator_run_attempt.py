"""Tests for V15-M53 twelve-hour operator run attempt (fixture + governance paths)."""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path
from unittest.mock import MagicMock

import pytest
from starlab.v15.m52_candidate_live_adapter_spike_io import seal_m52a_body
from starlab.v15.m52_candidate_live_adapter_spike_models import (
    CONTRACT_ID_M52A,
    STATUS_SPIKE_COMPLETED,
)
from starlab.v15.m52_twelve_hour_launch_rehearsal_io import seal_m52b_body
from starlab.v15.m52_twelve_hour_launch_rehearsal_models import (
    CONTRACT_ID_M52B,
    STATUS_FIXTURE_ONLY,
    STATUS_READY,
)
from starlab.v15.m52_twelve_hour_launch_rehearsal_models import (
    FILENAME_MAIN_JSON as M52B_MAIN,
)
from starlab.v15.m53_twelve_hour_operator_run_attempt_io import (
    BLOCKED_M52_NOT_READY,
    BLOCKED_M52_SHA,
    BLOCKED_PHASE_A_MISSING,
    emit_m53_fixture_ci,
    emit_m53_forbidden_refusal,
    emit_m53_phase_b_operator_receipt,
    evaluate_m53_operator_preflight,
    load_m52a_phase_gate,
    validate_m53_training_launch_command_text,
)
from starlab.v15.m53_twelve_hour_operator_run_attempt_models import (
    CONTRACT_ID_M53,
    EMITTER_MODULE_M53,
    FILENAME_MAIN_JSON,
    FORBIDDEN_FLAG_CLAIM_BENCHMARK,
    NON_CLAIMS_M53,
    RUNNER_MODULE_M53,
    STATUS_12H_COMPLETED_CKPT,
    STATUS_12H_INTERRUPTED_RESUME,
)
from starlab.v15.m53_twelve_hour_operator_run_attempt_models import (
    STATUS_FIXTURE_ONLY as M53_FIXTURE,
)


def _sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _write_minimal_m52_ready(tmp_path: Path) -> Path:
    body = {
        "schema_version": "1.0",
        "contract_id": CONTRACT_ID_M52B,
        "profile_id": "starlab.v15.m52.twelve_hour_blocker_discovery_launch_rehearsal.v1",
        "rehearsal_status": STATUS_READY,
        "stop_resume_plan_frozen": True,
        "blockers": [],
        "checkpoint_retention": {"max_retained_checkpoints": 256},
    }
    sealed = seal_m52b_body(body)
    p = tmp_path / M52B_MAIN
    p.write_text(json.dumps(sealed, indent=2), encoding="utf-8")
    return p


def _write_minimal_m52a_completed(tmp_path: Path) -> tuple[Path, str]:
    core = {
        "schema_version": "1.0",
        "contract_id": CONTRACT_ID_M52A,
        "adapter_status": STATUS_SPIKE_COMPLETED,
    }
    sealed = seal_m52a_body(core)
    p = tmp_path / "v15_candidate_live_adapter_spike.json"
    p.write_text(json.dumps(sealed, indent=2), encoding="utf-8")
    digest = str(sealed.get("artifact_sha256") or "").lower()
    return p, digest


def _training_launch_good(tmp_path: Path) -> Path:
    txt = (
        ".venv\\Scripts\\python.exe -m starlab.v15.run_v15_m28_sc2_backed_t1_candidate_training "
        "--max-wall-clock-minutes 720 --max-retained-checkpoints 256\n"
    )
    p = tmp_path / "train.txt"
    p.write_text(txt, encoding="utf-8")
    return p


@pytest.fixture
def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def test_m53_fixture_ci_no_live(tmp_path: Path) -> None:
    sealed, _paths = emit_m53_fixture_ci(tmp_path / "out")
    assert sealed["contract_id"] == CONTRACT_ID_M53
    assert sealed["run_status"] == M53_FIXTURE
    assert sealed["honesty"]["benchmark_passed"] is False
    assert sealed["phase_b_12hour_run"]["twelve_hour_run_executed"] is False
    assert NON_CLAIMS_M53[0] in sealed["non_claims"]


def test_m53_emit_cli(tmp_path: Path, repo_root: Path) -> None:
    out = tmp_path / "cli"
    res = subprocess.run(
        [
            sys.executable,
            "-m",
            EMITTER_MODULE_M53,
            "--profile",
            "fixture_ci",
            "--output-dir",
            str(out),
        ],
        cwd=str(repo_root),
        capture_output=True,
        text=True,
    )
    assert res.returncode == 0
    assert (out / FILENAME_MAIN_JSON).is_file()


def test_m52_binding_sha_mismatch(tmp_path: Path) -> None:
    m52 = _write_minimal_m52_ready(tmp_path)
    pre = evaluate_m53_operator_preflight(
        m52_launch_rehearsal_json=m52,
        expected_m52_sha256="f" * 64,
        m52a_adapter_spike_json=None,
        expected_m52a_sha256=None,
        candidate_checkpoint_path=None,
        expected_candidate_sha256=None,
        sc2_root=None,
        map_path=None,
        disk_root=None,
        estimated_checkpoint_mb=None,
        max_retained_checkpoints=None,
        skip_disk_strict=True,
    )
    assert not pre.ok
    assert BLOCKED_M52_SHA in pre.blockers


def test_m52_not_ready_blocks(tmp_path: Path) -> None:
    body = {
        "schema_version": "1.0",
        "contract_id": CONTRACT_ID_M52B,
        "profile_id": "x",
        "rehearsal_status": STATUS_FIXTURE_ONLY,
        "stop_resume_plan_frozen": True,
        "blockers": [],
        "checkpoint_retention": {"max_retained_checkpoints": 256},
    }
    sealed = seal_m52b_body(body)
    p = tmp_path / M52B_MAIN
    p.write_text(json.dumps(sealed), encoding="utf-8")
    pre = evaluate_m53_operator_preflight(
        m52_launch_rehearsal_json=p,
        expected_m52_sha256=None,
        m52a_adapter_spike_json=None,
        expected_m52a_sha256=None,
        candidate_checkpoint_path=None,
        expected_candidate_sha256=None,
        sc2_root=None,
        map_path=None,
        disk_root=None,
        estimated_checkpoint_mb=None,
        max_retained_checkpoints=None,
        skip_disk_strict=True,
    )
    assert not pre.ok
    assert BLOCKED_M52_NOT_READY in pre.blockers


def test_phase_a_gate_missing_m52a() -> None:
    st, bl, obj = load_m52a_phase_gate(None, expected_sha256=None, skip_acknowledged=False)
    assert obj is None
    assert BLOCKED_PHASE_A_MISSING in bl


def test_phase_a_skipped_ack() -> None:
    st, bl, obj = load_m52a_phase_gate(None, expected_sha256=None, skip_acknowledged=True)
    assert st == "candidate_watch_smoke_skipped_with_operator_acknowledgment"
    assert not bl


def test_training_launch_validation() -> None:
    ok, _ = validate_m53_training_launch_command_text(
        ".venv\\Scripts\\python.exe -m starlab.v15.run_v15_m28_sc2_backed_t1_candidate_training "
        "--max-wall-clock-minutes 720 --max-retained-checkpoints 256",
    )
    assert ok


def test_forbidden_flag_refusal(tmp_path: Path) -> None:
    sealed, _ = emit_m53_forbidden_refusal(
        tmp_path / "o",
        flags=[FORBIDDEN_FLAG_CLAIM_BENCHMARK],
    )
    assert sealed["run_status"] == "twelve_hour_operator_run_blocked"
    assert FORBIDDEN_FLAG_CLAIM_BENCHMARK in sealed["blockers"]


def test_emit_forbidden_cli(tmp_path: Path, repo_root: Path) -> None:
    out = tmp_path / "f"
    res = subprocess.run(
        [
            sys.executable,
            "-m",
            EMITTER_MODULE_M53,
            "--profile",
            "fixture_ci",
            "--output-dir",
            str(out),
            FORBIDDEN_FLAG_CLAIM_BENCHMARK,
        ],
        cwd=str(repo_root),
        capture_output=True,
        text=True,
    )
    assert res.returncode == 0
    sealed = json.loads((out / FILENAME_MAIN_JSON).read_text(encoding="utf-8"))
    assert sealed["run_status"] == "twelve_hour_operator_run_blocked"


def test_phase_b_mock_subprocess_completed(tmp_path: Path, repo_root: Path) -> None:
    m52_path = _write_minimal_m52_ready(tmp_path)
    m52a_path, m52a_digest = _write_minimal_m52a_completed(tmp_path)
    ck = tmp_path / "c.pt"
    ck.write_bytes(b"ck")
    ck_sha = _sha256_bytes(b"ck")
    map_p = tmp_path / "m.SC2Map"
    map_p.write_bytes(b"map")

    pre = evaluate_m53_operator_preflight(
        m52_launch_rehearsal_json=m52_path,
        expected_m52_sha256=None,
        m52a_adapter_spike_json=m52a_path,
        expected_m52a_sha256=m52a_digest,
        candidate_checkpoint_path=ck,
        expected_candidate_sha256=ck_sha,
        sc2_root=repo_root,
        map_path=map_p,
        disk_root=tmp_path,
        estimated_checkpoint_mb=1.0,
        max_retained_checkpoints=256,
        skip_disk_strict=True,
    )
    assert pre.ok

    phase_a_status, phase_a_blockers, _ = load_m52a_phase_gate(
        m52a_path,
        expected_sha256=m52a_digest,
        skip_acknowledged=False,
    )
    assert not phase_a_blockers

    launch = _training_launch_good(tmp_path)
    proc = MagicMock()
    proc.returncode = 0
    proc.stdout = "ok"
    outd = tmp_path / "m53out"
    outd.mkdir()
    (outd / "subdir" / "deep").mkdir(parents=True)
    (outd / "subdir" / "deep" / "v15_sc2_backed_t1_candidate_training.json").write_text(
        json.dumps(
            {
                "training_attempt": {
                    "training_update_count": 10,
                    "wall_clock_seconds": 43200.0,
                    "checkpoints_written_total": 2,
                    "checkpoints_pruned_total": 0,
                    "checkpoint_retention_max_retained": 256,
                    "sc2_backed_features_used": True,
                },
            },
        ),
        encoding="utf-8",
    )
    (outd / "subdir" / "deep" / "x.pt").write_bytes(b"pt")

    sealed, _paths = emit_m53_phase_b_operator_receipt(
        outd,
        repo_root=repo_root,
        pre=pre,
        phase_a_status=phase_a_status,
        phase_a_blockers=phase_a_blockers,
        phase_a_m52a_sha=m52a_digest,
        candidate_sha256=ck_sha,
        training_launch_file=launch,
        target_wall_clock_seconds=43200.0,
        max_retained_checkpoints=256,
        subprocess_result=proc,
        observed_wall_seconds=43201.0,
        interrupted=False,
        transcript_text="log\n",
        resume_from=None,
        skip_phase_a_ack=False,
    )
    assert sealed["run_status"] == STATUS_12H_COMPLETED_CKPT


def test_phase_b_interrupted_status(tmp_path: Path, repo_root: Path) -> None:
    m52_path = _write_minimal_m52_ready(tmp_path)
    m52a_path, m52a_digest = _write_minimal_m52a_completed(tmp_path)
    ck = tmp_path / "c.pt"
    ck.write_bytes(b"ck2")
    ck_sha = _sha256_bytes(b"ck2")
    map_p = tmp_path / "m2.SC2Map"
    map_p.write_bytes(b"m")
    launch = _training_launch_good(tmp_path)

    pre = evaluate_m53_operator_preflight(
        m52_launch_rehearsal_json=m52_path,
        expected_m52_sha256=None,
        m52a_adapter_spike_json=m52a_path,
        expected_m52a_sha256=m52a_digest,
        candidate_checkpoint_path=ck,
        expected_candidate_sha256=ck_sha,
        sc2_root=repo_root,
        map_path=map_p,
        disk_root=tmp_path,
        estimated_checkpoint_mb=1.0,
        max_retained_checkpoints=256,
        skip_disk_strict=True,
    )
    assert pre.ok
    st_a, bl_a, _ = load_m52a_phase_gate(
        m52a_path,
        expected_sha256=m52a_digest,
        skip_acknowledged=False,
    )
    assert not bl_a
    proc = MagicMock(returncode=-1, stdout="")
    sealed, _ = emit_m53_phase_b_operator_receipt(
        tmp_path / "outi",
        repo_root=repo_root,
        pre=pre,
        phase_a_status=st_a,
        phase_a_blockers=bl_a,
        phase_a_m52a_sha=m52a_digest,
        candidate_sha256=ck_sha,
        training_launch_file=launch,
        target_wall_clock_seconds=43200.0,
        max_retained_checkpoints=256,
        subprocess_result=proc,
        observed_wall_seconds=100.0,
        interrupted=True,
        transcript_text="partial\n",
        resume_from=None,
        skip_phase_a_ack=False,
    )
    assert sealed["run_status"] == STATUS_12H_INTERRUPTED_RESUME


def test_runner_phase_b_forbidden(tmp_path: Path, repo_root: Path) -> None:
    ck = tmp_path / "c.pt"
    ck.write_bytes(b"x")
    hx = _sha256_bytes(b"x")
    mp = tmp_path / "m.SC2Map"
    mp.write_bytes(b"m")
    res = subprocess.run(
        [
            sys.executable,
            "-m",
            RUNNER_MODULE_M53,
            "--phase",
            "full-12hour",
            "--m52-launch-rehearsal-json",
            str(_write_minimal_m52_ready(tmp_path)),
            "--candidate-checkpoint-path",
            str(ck),
            "--expected-candidate-checkpoint-sha256",
            hx,
            "--sc2-root",
            str(repo_root),
            "--map-path",
            str(mp),
            "--output-dir",
            str(tmp_path / "o"),
            FORBIDDEN_FLAG_CLAIM_BENCHMARK,
        ],
        cwd=str(repo_root),
        capture_output=True,
        text=True,
    )
    assert res.returncode == 0
