"""V15-M38 remediation & launch rehearsal tests."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from starlab.runs.json_util import canonical_json_dumps
from starlab.v15.emit_v15_m38_two_hour_run_remediation_launch_rehearsal import (
    main as emit_m38_main,
)
from starlab.v15.m37_two_hour_run_blocker_discovery_io import build_fixture_body, seal_m37_body
from starlab.v15.m38_two_hour_run_remediation_launch_rehearsal_io import (
    emit_m38_fixture,
    emit_m38_operator_preflight,
)
from starlab.v15.m38_two_hour_run_remediation_launch_rehearsal_models import (
    CONTRACT_ID_M38,
    FILENAME_MAIN_JSON,
    LAUNCH_COMMAND_FILENAME,
    PROFILE_FIXTURE_CI,
    STATUS_BLOCKED_CHECKPOINT,
    STATUS_BLOCKED_CRITICAL,
    STATUS_BLOCKED_NO_M37,
    STATUS_BLOCKED_RUNNER,
    STATUS_FIXTURE_SCHEMA_ONLY,
    STATUS_READY_M39,
    STOP_RESUME_CARD_FILENAME,
)

REPO_ROOT = Path(__file__).resolve().parents[1]

_EXPECTED_ARTIFACTS = (
    FILENAME_MAIN_JSON,
    "v15_two_hour_run_remediation_launch_rehearsal_report.json",
    "v15_two_hour_run_remediation_launch_rehearsal_checklist.md",
    "v15_m39_launch_runbook.md",
    LAUNCH_COMMAND_FILENAME,
    STOP_RESUME_CARD_FILENAME,
)


def _sealed_m37_from_fixture_body(
    *,
    blockers: list[dict[str, Any]] | None = None,
    critical: int = 0,
    high: int = 0,
) -> dict[str, Any]:
    body = build_fixture_body()
    if blockers is not None:
        body["blockers"] = blockers
    rs = body.get("readiness_summary")
    if isinstance(rs, dict):
        rs["critical_blocker_count"] = critical
        rs["high_blocker_count"] = high
    return seal_m37_body(body)


def test_m38_fixture_emits_all_artifacts(tmp_path: Path) -> None:
    sealed, *paths = emit_m38_fixture(tmp_path / "o", repo_root=REPO_ROOT)
    assert len(paths) == 6
    assert sealed["rehearsal_status"] == STATUS_FIXTURE_SCHEMA_ONLY
    assert {p.name for p in paths} == set(_EXPECTED_ARTIFACTS)


def test_m38_fixture_claim_flags_false(tmp_path: Path) -> None:
    sealed, *_ = emit_m38_fixture(tmp_path / "o", repo_root=REPO_ROOT)
    assert sealed["contract_id"] == CONTRACT_ID_M38
    for _k, v in sealed["claim_flags"].items():
        assert v is False


def test_m38_fixture_cli(tmp_path: Path) -> None:
    rc = emit_m38_main(["--fixture-ci", "--output-dir", str(tmp_path / "o")])
    assert rc == 0
    js = json.loads((tmp_path / "o" / FILENAME_MAIN_JSON).read_text())
    assert js["profile"] == PROFILE_FIXTURE_CI


def test_preflight_clean_m37_ready(tmp_path: Path) -> None:
    m37 = tmp_path / "m37.json"
    sealed37 = _sealed_m37_from_fixture_body()
    m37.write_text(canonical_json_dumps(sealed37), encoding="utf-8")
    sealed38, *_ = emit_m38_operator_preflight(
        tmp_path / "out38",
        repo_root=REPO_ROOT,
        m37_blocker_discovery_json=m37,
    )
    assert sealed38["rehearsal_status"] == STATUS_READY_M39
    assert sealed38["m39_launch_ready"] is True


def test_preflight_critical_blocker_blocks(tmp_path: Path) -> None:
    m37 = tmp_path / "m37.json"
    sealed37 = _sealed_m37_from_fixture_body(
        blockers=[
            {
                "blocker_id": "synthetic_critical_test",
                "category": "test",
                "severity": "critical",
                "status": "open",
                "evidence": "test",
                "m38_action": "test",
            },
        ],
        critical=1,
        high=0,
    )
    m37.write_text(canonical_json_dumps(sealed37), encoding="utf-8")
    sealed38, *_ = emit_m38_operator_preflight(
        tmp_path / "out38",
        repo_root=REPO_ROOT,
        m37_blocker_discovery_json=m37,
    )
    assert sealed38["rehearsal_status"] == STATUS_BLOCKED_CRITICAL
    assert sealed38["m39_launch_ready"] is False


def test_preflight_checkpoint_cadence_unresolved(tmp_path: Path) -> None:
    m37 = tmp_path / "m37.json"
    sealed37 = _sealed_m37_from_fixture_body(
        blockers=[
            {
                "blocker_id": "checkpoint_cadence_too_high",
                "category": "checkpoint_cadence_storage",
                "severity": "critical",
                "status": "open",
                "evidence": "test",
                "m38_action": "test",
            },
        ],
    )
    m37.write_text(canonical_json_dumps(sealed37), encoding="utf-8")
    fake_root = tmp_path / "fake_repo"
    (fake_root / "starlab" / "v15").mkdir(parents=True)
    (fake_root / "starlab" / "v15" / "sc2_backed_t1_training_execution.py").write_text(
        "pass\n",
        encoding="utf-8",
    )
    (fake_root / "starlab" / "v15" / "run_v15_m28_sc2_backed_t1_candidate_training.py").write_text(
        "pass\n",
        encoding="utf-8",
    )
    sealed38, *_ = emit_m38_operator_preflight(
        tmp_path / "out38",
        repo_root=fake_root,
        m37_blocker_discovery_json=m37,
    )
    assert sealed38["rehearsal_status"] == STATUS_BLOCKED_CHECKPOINT
    assert sealed38["m39_launch_ready"] is False


def test_preflight_retention_resolves_cadence_blocker(tmp_path: Path) -> None:
    m37 = tmp_path / "m37.json"
    sealed37 = _sealed_m37_from_fixture_body(
        blockers=[
            {
                "blocker_id": "checkpoint_cadence_too_high",
                "category": "checkpoint_cadence_storage",
                "severity": "critical",
                "status": "open",
                "evidence": "test",
                "m38_action": "test",
            },
        ],
    )
    m37.write_text(canonical_json_dumps(sealed37), encoding="utf-8")
    sealed38, *_ = emit_m38_operator_preflight(
        tmp_path / "out38",
        repo_root=REPO_ROOT,
        m37_blocker_discovery_json=m37,
    )
    assert sealed38["rehearsal_status"] == STATUS_READY_M39
    remediated = {r["blocker_id"]: r["status"] for r in sealed38["blocker_resolution_summary"]}
    assert remediated.get("checkpoint_cadence_too_high") == "remediated"


def test_preflight_runner_incompatible(tmp_path: Path) -> None:
    m37 = tmp_path / "m37.json"
    sealed37 = _sealed_m37_from_fixture_body(
        blockers=[
            {
                "blocker_id": "m29_wrapper_name_or_contract_too_30min_specific",
                "category": "runner_compatibility",
                "severity": "high",
                "status": "open",
                "evidence": "test",
                "m38_action": "test",
            },
        ],
    )
    m37.write_text(canonical_json_dumps(sealed37), encoding="utf-8")
    fake_root = tmp_path / "fake_repo"
    (fake_root / "starlab" / "v15").mkdir(parents=True)
    (fake_root / "starlab" / "v15" / "run_v15_m28_sc2_backed_t1_candidate_training.py").write_text(
        "# stub without wall clock flag\n",
        encoding="utf-8",
    )
    sealed38, *_ = emit_m38_operator_preflight(
        tmp_path / "out38",
        repo_root=fake_root,
        m37_blocker_discovery_json=m37,
    )
    assert sealed38["rehearsal_status"] == STATUS_BLOCKED_RUNNER
    assert sealed38["m39_launch_ready"] is False


def test_launch_command_emitted_not_executed(tmp_path: Path) -> None:
    _, *paths = emit_m38_fixture(tmp_path / "o", repo_root=REPO_ROOT)
    cmd_path = next(p for p in paths if p.name == LAUNCH_COMMAND_FILENAME)
    txt = cmd_path.read_text(encoding="utf-8")
    assert ".venv" in txt
    assert "120" in txt
    assert "max-retained-checkpoints" in txt


def test_stop_resume_card_emitted(tmp_path: Path) -> None:
    _, *paths = emit_m38_fixture(tmp_path / "o", repo_root=REPO_ROOT)
    card = next(p for p in paths if p.name == STOP_RESUME_CARD_FILENAME)
    assert "resume" in card.read_text(encoding="utf-8").lower()


def test_non_claims_in_checklist(tmp_path: Path) -> None:
    _, *paths = emit_m38_fixture(tmp_path / "o", repo_root=REPO_ROOT)
    chk = next(p for p in paths if p.name.endswith("_checklist.md"))
    low = chk.read_text(encoding="utf-8").lower()
    assert "not_two_hour_run" in low or "non_claims" in low


def test_invalid_m37_contract_blocked(tmp_path: Path) -> None:
    bad = tmp_path / "bad.json"
    bad.write_text(
        json.dumps({"contract_id": "wrong", "artifact_sha256": "a" * 64}), encoding="utf-8"
    )
    sealed38, *_ = emit_m38_operator_preflight(
        tmp_path / "o",
        repo_root=REPO_ROOT,
        m37_blocker_discovery_json=bad,
    )
    assert sealed38["rehearsal_status"] == STATUS_BLOCKED_NO_M37


def test_optional_md_enriched(tmp_path: Path) -> None:
    m37p = tmp_path / "m37.json"
    sealed37 = _sealed_m37_from_fixture_body()
    m37p.write_text(canonical_json_dumps(sealed37), encoding="utf-8")
    map_md = tmp_path / "map.md"
    map_md.write_text("# map\n", encoding="utf-8")
    sealed38, *_ = emit_m38_operator_preflight(
        tmp_path / "o",
        repo_root=REPO_ROOT,
        m37_blocker_discovery_json=m37p,
        m37_remediation_map_md=map_md,
    )
    ub = sealed38["upstream_bindings"]
    assert ub["m37_remediation_map_md"] == "enriched_when_supplied"
