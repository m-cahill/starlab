"""V15-M39 two-hour operator run attempt tests."""

from __future__ import annotations

import json
import os
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
    build_checkpoint_inventory,
    classify_run_outcome,
    emit_m39_fixture,
    emit_m39_operator_preflight,
    validate_launch_command_text,
)
from starlab.v15.m39_two_hour_operator_run_attempt_models import (
    CONTRACT_ID_M39,
    FILENAME_MAIN_JSON,
    M39_OUTPUT_ROOT_TOKEN,
    PROFILE_FIXTURE_CI,
    STATUS_FIXTURE_ONLY,
    STATUS_PREFLIGHT_BLOCKED_M38_NOT_READY,
    STATUS_PREFLIGHT_BLOCKED_NO_M38,
    STATUS_PREFLIGHT_BLOCKED_RETENTION,
    STATUS_PREFLIGHT_READY,
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
