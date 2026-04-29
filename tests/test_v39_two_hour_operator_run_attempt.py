"""V15-M39 two-hour operator run attempt tests."""

from __future__ import annotations

import json
import os
import subprocess
import time
from pathlib import Path
from typing import Any

import pytest
from starlab.runs.json_util import canonical_json_dumps
from starlab.v15 import run_v15_m39_two_hour_operator_run_attempt as run_m39
from starlab.v15.emit_v15_m39_two_hour_operator_run_attempt import (
    main as emit_m39_main,
)
from starlab.v15.m37_two_hour_run_blocker_discovery_io import build_fixture_body, seal_m37_body
from starlab.v15.m37_two_hour_run_blocker_discovery_models import EXPECTED_PUBLIC_CANDIDATE_SHA256
from starlab.v15.m38_two_hour_run_remediation_launch_rehearsal_io import (
    emit_m38_fixture,
    emit_m38_operator_preflight,
    seal_m38_body,
)
from starlab.v15.m38_two_hour_run_remediation_launch_rehearsal_models import (
    CONTRACT_ID_M38,
    EMITTER_MODULE_M38,
    LAUNCH_COMMAND_FILENAME,
    MILESTONE_LABEL_M38,
    PROFILE_M38,
    SCHEMA_VERSION,
    STATUS_READY_M39,
)
from starlab.v15.m39_two_hour_operator_run_attempt_io import (
    PreflightOutcome,
    build_checkpoint_inventory,
    build_m39_checklist_md,
    build_m39_report,
    classify_run_outcome,
    emit_m39_fixture,
    emit_m39_operator_preflight,
    emit_m39_operator_run_receipt,
    evaluate_operator_preflight,
    frozen_launch_command_to_cmdexe_line,
    merge_telemetry_from_m28_artifact,
    validate_launch_command_text,
)
from starlab.v15.m39_two_hour_operator_run_attempt_models import (
    CONTRACT_ID_M39,
    FILENAME_MAIN_JSON,
    M39_OUTPUT_ROOT_TOKEN,
    PROFILE_FIXTURE_CI,
    STATUS_FIXTURE_ONLY,
    STATUS_PREFLIGHT_BLOCKED_ENV,
    STATUS_PREFLIGHT_BLOCKED_LINEAGE,
    STATUS_PREFLIGHT_BLOCKED_M38_NOT_READY,
    STATUS_PREFLIGHT_BLOCKED_NO_M38,
    STATUS_PREFLIGHT_BLOCKED_RETENTION,
    STATUS_PREFLIGHT_READY,
    STATUS_RUN_BLOCKED_PREFLIGHT,
    STATUS_RUN_COMPLETED_NO_CKPT,
    STATUS_RUN_COMPLETED_WITH_CKPT,
    STATUS_RUN_FAILED,
    STATUS_RUN_INTERRUPTED,
)

REPO_ROOT = Path(__file__).resolve().parents[1]

M38_REHEARSAL_JSON = "v15_two_hour_run_remediation_launch_rehearsal.json"

_EXPECTED_NAMES = {
    FILENAME_MAIN_JSON,
    "v15_two_hour_operator_run_attempt_report.json",
    "v15_two_hour_operator_run_attempt_checklist.md",
    "v15_m39_operator_transcript.txt",
    "v15_m39_telemetry_summary.json",
    "v15_m39_checkpoint_inventory.json",
}


def _sealed_m37_clean(tmp_path: Path) -> Path:
    m37 = tmp_path / "m37.json"
    sealed37 = seal_m37_body(build_fixture_body())
    m37.write_text(canonical_json_dumps(sealed37), encoding="utf-8")
    return m37


def test_m39_fixture_emits_all_artifacts(tmp_path: Path) -> None:
    sealed, paths = emit_m39_fixture(tmp_path / "o", repo_root=REPO_ROOT)
    assert {p.name for p in paths} == _EXPECTED_NAMES
    assert sealed["run_status"] == STATUS_FIXTURE_ONLY
    assert sealed["contract_id"] == CONTRACT_ID_M39


def test_m39_fixture_claim_flags_false(tmp_path: Path) -> None:
    sealed, _ = emit_m39_fixture(tmp_path / "o", repo_root=REPO_ROOT)
    for _k, v in sealed["claim_flags"].items():
        assert v is False


def test_m39_fixture_cli(tmp_path: Path) -> None:
    rc = emit_m39_main(["--fixture-ci", "--output-dir", str(tmp_path / "o")])
    assert rc == 0
    js = json.loads((tmp_path / "o" / FILENAME_MAIN_JSON).read_text())
    assert js["profile"] == PROFILE_FIXTURE_CI


def test_preflight_missing_m38_json(tmp_path: Path) -> None:
    missing = tmp_path / "nope.json"
    fake_cmd = tmp_path / "cmd.txt"
    fake_cmd.write_text(
        "\n".join(
            [
                r".\.venv\Scripts\python.exe -m starlab.v15."
                r"run_v15_m28_sc2_backed_t1_candidate_training ^",
                "  --max-wall-clock-minutes 120 ^",
                r"  --output-dir out\v15_m39_2hour_operator_run\x\ ^",
                "  --max-retained-checkpoints 8\r\n",
            ],
        ),
        encoding="utf-8",
    )
    sealed, _ = emit_m39_operator_preflight(
        tmp_path / "o",
        repo_root=REPO_ROOT,
        m38_launch_rehearsal_json=missing,
        m39_launch_command=fake_cmd,
        expected_candidate_sha256=EXPECTED_PUBLIC_CANDIDATE_SHA256,
        skip_cuda_sc2=True,
    )
    assert sealed["run_status"] == STATUS_PREFLIGHT_BLOCKED_NO_M38


def test_preflight_m38_not_ready(tmp_path: Path) -> None:
    body = {
        "schema_version": SCHEMA_VERSION,
        "contract_id": CONTRACT_ID_M38,
        "profile_id": PROFILE_M38,
        "profile": "operator_preflight",
        "milestone": MILESTONE_LABEL_M38,
        "emitter_module": EMITTER_MODULE_M38,
        "rehearsal_status": STATUS_READY_M39,
        "m39_launch_ready": False,
        "upstream_bindings": {},
        "claim_flags": {},
        "non_claims": [],
    }
    sealed38 = seal_m38_body(body)
    p38 = tmp_path / "m38.json"
    p38.write_text(canonical_json_dumps(sealed38), encoding="utf-8")
    _sf, *m38_paths = emit_m38_fixture(tmp_path / "m38bundle", repo_root=REPO_ROOT)
    cmd_src = next(p for p in m38_paths if p.name == LAUNCH_COMMAND_FILENAME)
    fake_cmd = tmp_path / "cmd.txt"
    fake_cmd.write_text(cmd_src.read_text(encoding="utf-8"), encoding="utf-8")

    sealed39, _ = emit_m39_operator_preflight(
        tmp_path / "o",
        repo_root=REPO_ROOT,
        m38_launch_rehearsal_json=p38,
        m39_launch_command=fake_cmd,
        expected_candidate_sha256=EXPECTED_PUBLIC_CANDIDATE_SHA256,
        skip_cuda_sc2=True,
    )
    assert sealed39["run_status"] == STATUS_PREFLIGHT_BLOCKED_M38_NOT_READY


def test_preflight_launch_command_missing_retention(tmp_path: Path) -> None:
    m37p = _sealed_m37_clean(tmp_path)
    _hdr, *m38_paths = emit_m38_operator_preflight(
        tmp_path / "m38out",
        repo_root=REPO_ROOT,
        m37_blocker_discovery_json=m37p,
    )
    p38 = next(p for p in m38_paths if p.name == M38_REHEARSAL_JSON)
    bad_cmd = tmp_path / "bad_cmd.txt"
    bad_cmd.write_text(
        "# no retention\n"
        r".\.venv\Scripts\python.exe -m starlab.v15.run_v15_m28 ^"
        "\n--max-wall-clock-minutes 120\n"
        rf"--output-dir out\{M39_OUTPUT_ROOT_TOKEN}\x\\\n",
        encoding="utf-8",
    )
    sealed39, _ = emit_m39_operator_preflight(
        tmp_path / "o",
        repo_root=REPO_ROOT,
        m38_launch_rehearsal_json=p38,
        m39_launch_command=bad_cmd,
        expected_candidate_sha256=EXPECTED_PUBLIC_CANDIDATE_SHA256,
        skip_cuda_sc2=True,
    )
    assert sealed39["run_status"] == STATUS_PREFLIGHT_BLOCKED_RETENTION


def test_preflight_accepts_m38_bundle(tmp_path: Path) -> None:
    m37p = _sealed_m37_clean(tmp_path)
    _hdr, *m38_paths = emit_m38_operator_preflight(
        tmp_path / "m38out",
        repo_root=REPO_ROOT,
        m37_blocker_discovery_json=m37p,
    )
    p38 = next(p for p in m38_paths if p.name == M38_REHEARSAL_JSON)
    p_cmd = next(p for p in m38_paths if p.name == LAUNCH_COMMAND_FILENAME)
    sealed39, _ = emit_m39_operator_preflight(
        tmp_path / "m39out",
        repo_root=REPO_ROOT,
        m38_launch_rehearsal_json=p38,
        m39_launch_command=p_cmd,
        expected_candidate_sha256=EXPECTED_PUBLIC_CANDIDATE_SHA256,
        skip_cuda_sc2=True,
    )
    assert sealed39["run_status"] == STATUS_PREFLIGHT_READY


def test_checkpoint_inventory_prefers_newest(tmp_path: Path) -> None:
    root = tmp_path / "run"
    (root / "a").mkdir(parents=True)
    p1 = root / "a" / "old.pt"
    p2 = root / "new.pt"
    p1.write_bytes(b"a")
    p2.write_bytes(b"bb")
    os.utime(p1, (time.time(), time.time() - 100))
    inv = build_checkpoint_inventory(root)
    assert inv["final_checkpoint_guess_relative"] == "new.pt"


def test_classify_interrupted_partial(tmp_path: Path) -> None:
    inv = build_checkpoint_inventory(tmp_path / "e")
    st = classify_run_outcome(
        return_code=0,
        observed_seconds=7200.0,
        target_seconds=7200.0,
        interrupted=True,
        inventory=inv,
        sc2_backed_features_used_guess=True,
        retention_max_retained=256,
        _checkpoints_written=1,
        _checkpoints_pruned=0,
        final_persisted=True,
    )
    assert st == STATUS_RUN_INTERRUPTED


def test_classify_failed_nonzero_rc(tmp_path: Path) -> None:
    inv: dict[str, Any] = {"checkpoint_files": [{"x": 1}]}
    st = classify_run_outcome(
        return_code=1,
        observed_seconds=100.0,
        target_seconds=7200.0,
        interrupted=False,
        inventory=inv,
        sc2_backed_features_used_guess=True,
        retention_max_retained=256,
        _checkpoints_written=1,
        _checkpoints_pruned=0,
        final_persisted=True,
    )
    assert st == STATUS_RUN_FAILED


def test_completed_strong_claim_flags_remain_false(tmp_path: Path) -> None:
    inv: dict[str, Any] = {"checkpoint_files": [{"sha256": "a" * 64}]}
    st = classify_run_outcome(
        return_code=0,
        observed_seconds=7200.0,
        target_seconds=7200.0,
        interrupted=False,
        inventory=inv,
        sc2_backed_features_used_guess=True,
        retention_max_retained=256,
        _checkpoints_written=3,
        _checkpoints_pruned=0,
        final_persisted=True,
    )
    assert st == STATUS_RUN_COMPLETED_WITH_CKPT
    body: dict[str, Any] = {
        "schema_version": "1.0",
        "contract_id": CONTRACT_ID_M39,
        "profile_id": "starlab.v15.m39.two_hour_operator_run_attempt.v1",
        "run_status": st,
        "claim_flags": {
            "two_hour_run_executed": True,
            "two_hour_run_completed": True,
            "benchmark_passed": False,
            "strength_evaluated": False,
            "checkpoint_promoted": False,
            "scorecard_results_produced": False,
            "xai_execution_performed": False,
            "human_panel_execution_performed": False,
            "showcase_release_authorized": False,
            "v2_authorized": False,
            "t2_authorized": False,
            "t3_authorized": False,
        },
    }
    assert body["claim_flags"]["benchmark_passed"] is False


def test_public_json_has_no_absolute_transcript_path(tmp_path: Path) -> None:
    sealed, _ = emit_m39_fixture(tmp_path / "o", repo_root=REPO_ROOT)
    dumped = canonical_json_dumps(sealed)
    assert sealed["execution_telemetry"]["transcript_absolute_path_redacted"] is True
    assert "artifact_sha256" in dumped


@pytest.mark.parametrize("iteration", range(2))
def test_fixture_seal_deterministic(tmp_path: Path, iteration: int) -> None:
    _ = iteration
    sub = tmp_path / f"emit_{iteration}"
    a, _ = emit_m39_fixture(sub / "a", repo_root=REPO_ROOT)
    b, _ = emit_m39_fixture(sub / "b", repo_root=REPO_ROOT)
    assert str(a["artifact_sha256"]) == str(b["artifact_sha256"])


def test_validate_launch_command_ok() -> None:
    ok, _why = validate_launch_command_text(
        r".\.venv\X\python.exe -m mod "
        "--max-wall-clock-minutes 120 --max-retained-checkpoints 2 "
        rf"out\x\{M39_OUTPUT_ROOT_TOKEN}\y ",
    )
    assert ok


def test_run_requires_dual_guards(tmp_path: Path) -> None:
    m37p = _sealed_m37_clean(tmp_path)
    _hdr, *m38_paths = emit_m38_operator_preflight(
        tmp_path / "m38out",
        repo_root=REPO_ROOT,
        m37_blocker_discovery_json=m37p,
    )
    p38 = next(p for p in m38_paths if p.name == M38_REHEARSAL_JSON)
    p_cmd = next(p for p in m38_paths if p.name == LAUNCH_COMMAND_FILENAME)
    rc = run_m39.main(
        [
            "--m38-launch-rehearsal-json",
            str(p38),
            "--m39-launch-command",
            str(p_cmd),
            "--output-dir",
            str(tmp_path / "outrun"),
        ],
    )
    assert rc == 2


def test_validate_launch_command_rejects_missing_horizon() -> None:
    ok, why = validate_launch_command_text(
        r".\.venv\Scripts\python.exe -m mod --max-retained-checkpoints 2 "
        rf"out\x\{M39_OUTPUT_ROOT_TOKEN}\y ",
    )
    assert not ok
    assert why == "missing_7200s_or_120min_horizon"


def test_validate_launch_command_rejects_missing_venv_hint() -> None:
    ok, why = validate_launch_command_text(
        "python -m mod --max-wall-clock-minutes 120 --max-retained-checkpoints 2 "
        rf"out/{M39_OUTPUT_ROOT_TOKEN}/",
    )
    assert not ok
    assert why == "missing_venv_python_hint"


def test_evaluate_preflight_invalid_expected_sha_hex(tmp_path: Path) -> None:
    out = evaluate_operator_preflight(
        repo_root=REPO_ROOT,
        m38_launch_rehearsal_json=None,
        m39_launch_command=None,
        expected_candidate_sha256="not_hex",
        skip_cuda_sc2=True,
        min_free_bytes=1_000_000,
        output_dir=tmp_path / "o",
    )
    assert out.status == STATUS_PREFLIGHT_BLOCKED_ENV


def test_evaluate_preflight_lineage_mismatch(tmp_path: Path) -> None:
    out = evaluate_operator_preflight(
        repo_root=REPO_ROOT,
        m38_launch_rehearsal_json=None,
        m39_launch_command=None,
        expected_candidate_sha256="a" * 64,
        skip_cuda_sc2=True,
        min_free_bytes=1_000_000,
        output_dir=tmp_path / "o",
    )
    assert out.status == STATUS_PREFLIGHT_BLOCKED_LINEAGE


def test_evaluate_preflight_m38_json_not_object(tmp_path: Path) -> None:
    p38 = tmp_path / "arr.json"
    p38.write_text("[1]", encoding="utf-8")
    p_cmd = tmp_path / "c.txt"
    p_cmd.write_text(
        r".\.venv\Scripts\python.exe -m m --max-wall-clock-minutes 120 "
        r"--max-retained-checkpoints 1 out\v15_m39_2hour_operator_run\\\n",
        encoding="utf-8",
    )
    out = evaluate_operator_preflight(
        repo_root=REPO_ROOT,
        m38_launch_rehearsal_json=p38,
        m39_launch_command=p_cmd,
        expected_candidate_sha256=EXPECTED_PUBLIC_CANDIDATE_SHA256,
        skip_cuda_sc2=True,
        min_free_bytes=1_000_000,
        output_dir=tmp_path / "pre",
    )
    assert out.status == STATUS_PREFLIGHT_BLOCKED_NO_M38
    assert "must be an object" in out.detail or "unreadable" in out.detail


def test_preflight_m38_seal_mismatch(tmp_path: Path) -> None:
    m37p = _sealed_m37_clean(tmp_path)
    _hdr, *m38_paths = emit_m38_operator_preflight(
        tmp_path / "m38out",
        repo_root=REPO_ROOT,
        m37_blocker_discovery_json=m37p,
    )
    p38_good = next(p for p in m38_paths if p.name == M38_REHEARSAL_JSON)
    obj = json.loads(p38_good.read_text(encoding="utf-8"))
    obj["rehearsal_notes"] = "tamper_without_reseal"
    p_bad = tmp_path / "tampered.json"
    p_bad.write_text(canonical_json_dumps(obj), encoding="utf-8")
    p_cmd = next(p for p in m38_paths if p.name == LAUNCH_COMMAND_FILENAME)
    sealed39, _ = emit_m39_operator_preflight(
        tmp_path / "o",
        repo_root=REPO_ROOT,
        m38_launch_rehearsal_json=p_bad,
        m39_launch_command=p_cmd,
        expected_candidate_sha256=EXPECTED_PUBLIC_CANDIDATE_SHA256,
        skip_cuda_sc2=True,
    )
    assert sealed39["run_status"] == STATUS_PREFLIGHT_BLOCKED_M38_NOT_READY


def test_preflight_launch_missing_horizon_status(tmp_path: Path) -> None:
    m37p = _sealed_m37_clean(tmp_path)
    _hdr, *m38_paths = emit_m38_operator_preflight(
        tmp_path / "m38out2",
        repo_root=REPO_ROOT,
        m37_blocker_discovery_json=m37p,
    )
    p38 = next(p for p in m38_paths if p.name == M38_REHEARSAL_JSON)
    bad_cmd = tmp_path / "bad_horizon.txt"
    bad_cmd.write_text(
        r".\.venv\Scripts\python.exe -m starlab.v15.run_v15_m28 "
        r"--max-retained-checkpoints 2 ^"
        "\n"
        rf"  --output-dir out\{M39_OUTPUT_ROOT_TOKEN}\n",
        encoding="utf-8",
    )
    out = evaluate_operator_preflight(
        repo_root=REPO_ROOT,
        m38_launch_rehearsal_json=p38,
        m39_launch_command=bad_cmd,
        expected_candidate_sha256=EXPECTED_PUBLIC_CANDIDATE_SHA256,
        skip_cuda_sc2=True,
        min_free_bytes=1_000_000,
        output_dir=tmp_path / "prehorizon",
    )
    assert out.status == STATUS_PREFLIGHT_BLOCKED_ENV


def test_emit_run_receipt_blocked_preflight_cached_outcome(tmp_path: Path) -> None:
    out_dir = tmp_path / "recv_block"
    dummy_m38 = tmp_path / "m38.json"
    dummy_m38.write_text("{}", encoding="utf-8")
    dummy_cmd = tmp_path / "cmd.txt"
    dummy_cmd.write_text("noop", encoding="utf-8")
    pre = PreflightOutcome(
        STATUS_PREFLIGHT_BLOCKED_NO_M38,
        "missing_m38_json_path",
        m38_obj=None,
    )
    sealed, paths = emit_m39_operator_run_receipt(
        out_dir,
        repo_root=REPO_ROOT,
        m38_launch_rehearsal_json=dummy_m38,
        m39_launch_command=dummy_cmd,
        expected_candidate_sha256=EXPECTED_PUBLIC_CANDIDATE_SHA256,
        max_retained_checkpoints=8,
        target_wall_clock_seconds=7200.0,
        skip_cuda_sc2=True,
        min_free_disk_gb=0.001,
        subprocess_result=None,
        observed_wall_seconds=0.0,
        interrupted=False,
        launch_command_delta_detected=False,
        transcript_text="",
        preflight_outcome=pre,
    )
    assert sealed["run_status"] == STATUS_RUN_BLOCKED_PREFLIGHT
    assert len(paths) == 6


def test_emit_run_receipt_post_preflight_completed_no_ckpt(tmp_path: Path) -> None:
    m37p = _sealed_m37_clean(tmp_path)
    _hdr, *m38_paths = emit_m38_operator_preflight(
        tmp_path / "m38recv",
        repo_root=REPO_ROOT,
        m37_blocker_discovery_json=m37p,
    )
    p38 = next(p for p in m38_paths if p.name == M38_REHEARSAL_JSON)
    p_cmd = next(p for p in m38_paths if p.name == LAUNCH_COMMAND_FILENAME)
    m38_obj = json.loads(p38.read_text(encoding="utf-8"))
    out_dir = tmp_path / "recv_ok"
    pre = PreflightOutcome(STATUS_PREFLIGHT_READY, "ok", m38_obj=m38_obj)
    cp = subprocess.CompletedProcess(args="cmd-line", returncode=0, stdout="x", stderr="")
    sealed, _paths = emit_m39_operator_run_receipt(
        out_dir,
        repo_root=REPO_ROOT,
        m38_launch_rehearsal_json=p38,
        m39_launch_command=p_cmd,
        expected_candidate_sha256=EXPECTED_PUBLIC_CANDIDATE_SHA256,
        max_retained_checkpoints=8,
        target_wall_clock_seconds=7200.0,
        skip_cuda_sc2=True,
        min_free_disk_gb=0.001,
        subprocess_result=cp,
        observed_wall_seconds=7200.0,
        interrupted=False,
        launch_command_delta_detected=False,
        transcript_text="trainer finished\n",
        preflight_outcome=pre,
    )
    assert sealed["run_status"] == STATUS_RUN_COMPLETED_NO_CKPT
    assert sealed["claim_flags"]["two_hour_run_executed"] is True


def test_emit_run_receipt_with_m28_hints_and_checkpoint(tmp_path: Path) -> None:
    m37p = _sealed_m37_clean(tmp_path)
    _hdr, *m38_paths = emit_m38_operator_preflight(
        tmp_path / "m38recv2",
        repo_root=REPO_ROOT,
        m37_blocker_discovery_json=m37p,
    )
    p38 = next(p for p in m38_paths if p.name == M38_REHEARSAL_JSON)
    p_cmd = next(p for p in m38_paths if p.name == LAUNCH_COMMAND_FILENAME)
    m38_obj = json.loads(p38.read_text(encoding="utf-8"))
    out_dir = tmp_path / "recv_ckpt"
    deep = out_dir / "nested"
    deep.mkdir(parents=True)
    m28_path = deep / "v15_sc2_backed_t1_candidate_training.json"
    m28_body = {
        "training_attempt": {
            "training_update_count": 3,
            "wall_clock_seconds": 100.0,
            "checkpoint_count": 1,
            "checkpoints_written_total": 2,
            "checkpoints_pruned_total": 0,
            "checkpoint_retention_max_retained": 8,
            "sc2_backed_features_used": True,
        },
    }
    m28_path.write_text(canonical_json_dumps(m28_body), encoding="utf-8")
    (out_dir / "final.ckpt.pt").write_bytes(b"x")
    pre = PreflightOutcome(STATUS_PREFLIGHT_READY, "ok", m38_obj=m38_obj)
    cp = subprocess.CompletedProcess(args="cmd", returncode=0, stdout="", stderr="")
    sealed, _paths = emit_m39_operator_run_receipt(
        out_dir,
        repo_root=REPO_ROOT,
        m38_launch_rehearsal_json=p38,
        m39_launch_command=p_cmd,
        expected_candidate_sha256=EXPECTED_PUBLIC_CANDIDATE_SHA256,
        max_retained_checkpoints=8,
        target_wall_clock_seconds=7200.0,
        skip_cuda_sc2=True,
        min_free_disk_gb=0.001,
        subprocess_result=cp,
        observed_wall_seconds=7200.0,
        interrupted=False,
        launch_command_delta_detected=False,
        transcript_text="ok\n",
        preflight_outcome=pre,
    )
    assert sealed["run_status"] == STATUS_RUN_COMPLETED_WITH_CKPT
    assert sealed["execution_telemetry"]["training_update_count"] == 3


def test_merge_m28_telemetry_roundtrip(tmp_path: Path) -> None:
    d = tmp_path / "tree"
    sub = d / "a" / "b"
    sub.mkdir(parents=True)
    m28_path = sub / "v15_sc2_backed_t1_candidate_training.json"
    m28_path.write_text(
        canonical_json_dumps(
            {"training_attempt": {"training_update_count": 5, "sc2_backed_features_used": True}},
        ),
        encoding="utf-8",
    )
    hints = merge_telemetry_from_m28_artifact(d)
    assert hints.get("training_update_count") == 5
    assert hints.get("sc2_backed_features_used") is True


def test_merge_m28_telemetry_malformed_returns_empty(tmp_path: Path) -> None:
    d = tmp_path / "empty_m28"
    d.mkdir()
    assert merge_telemetry_from_m28_artifact(d) == {}
    bad = d / "v15_sc2_backed_t1_candidate_training.json"
    bad.write_text("[]", encoding="utf-8")
    assert merge_telemetry_from_m28_artifact(d) == {}


def test_build_m39_report_and_checklist(tmp_path: Path) -> None:
    sealed, _ = emit_m39_fixture(tmp_path / "o", repo_root=REPO_ROOT)
    rep = build_m39_report(sealed)
    assert rep["report_kind"] == "v15_two_hour_operator_run_attempt_report"
    assert rep["run_status"] == STATUS_FIXTURE_ONLY
    md = build_m39_checklist_md(sealed)
    assert CONTRACT_ID_M39 in md or "V15-M39" in md


def test_frozen_launch_strips_comments_and_wraps_spaced_repo(tmp_path: Path) -> None:
    spaced = tmp_path / "repo root"
    spaced.mkdir()
    lf = spaced / "launch.txt"
    lf.write_text(
        "# header comment\n"
        "// also\n"
        r"  .\.venv\Scripts\python.exe -m demo  ",
        encoding="utf-8",
    )
    line = frozen_launch_command_to_cmdexe_line(lf, repo_root=spaced)
    assert "cmd.exe" in line
    assert "header" not in line
    assert "demo" in line
    assert "repo root" in line.replace('"', "")


def test_frozen_launch_empty_raises(tmp_path: Path) -> None:
    lf = tmp_path / "empty.txt"
    lf.write_text("# only comments\n// none\n", encoding="utf-8")
    with pytest.raises(ValueError, match="empty_launch_command"):
        frozen_launch_command_to_cmdexe_line(lf, repo_root=tmp_path / "rr")


def test_classify_short_wall_clock_interrupt_style(tmp_path: Path) -> None:
    inv = build_checkpoint_inventory(tmp_path / "e")
    st = classify_run_outcome(
        return_code=0,
        observed_seconds=100.0,
        target_seconds=7200.0,
        interrupted=False,
        inventory=inv,
        sc2_backed_features_used_guess=True,
        retention_max_retained=256,
        _checkpoints_written=1,
        _checkpoints_pruned=0,
        final_persisted=True,
    )
    assert st == STATUS_RUN_INTERRUPTED


def test_checkpoint_inventory_extra_glob_root(tmp_path: Path) -> None:
    root = tmp_path / "m39out"
    ext = tmp_path / "extra"
    root.mkdir()
    ext.mkdir()
    (ext / "side.pt").write_bytes(b"z")
    inv = build_checkpoint_inventory(root, extra_glob_roots=[ext])
    names = [r["path_relative_to_m39_output_dir"] for r in inv["checkpoint_files"]]
    assert "side.pt" in names
