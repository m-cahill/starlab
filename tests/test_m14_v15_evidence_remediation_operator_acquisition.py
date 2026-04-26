"""V15-M14 evidence remediation plan — deterministic emit and M13 binding.

Note: this is V15 namespace M14 (evidence remediation), not v1 milestone M14 (replay bundle).
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest
from starlab.v15.evidence_remediation_io import (
    emit_v15_evidence_remediation_plan_fixture,
    emit_v15_evidence_remediation_plan_with_m13,
    parse_m13_v2_decision,
)
from starlab.v15.evidence_remediation_models import (
    ALL_GAP_IDS,
    ALL_REMEDIATION_GATE_IDS,
    CONTRACT_ID_EVIDENCE_REMEDIATION_PLAN,
    FILENAME_EVIDENCE_REMEDIATION_PLAN,
    FILENAME_OPERATOR_RUNBOOK_MD,
    REPORT_FILENAME_EVIDENCE_REMEDIATION_PLAN,
    SEAL_KEY_EVIDENCE_REMEDIATION_PLAN,
    default_m14_authorization_flags,
)
from starlab.v15.v2_decision_io import emit_v15_v2_go_no_go_decision_fixture

REPO_ROOT = Path(__file__).resolve().parents[1]


def test_default_fixture_emits_three_files(tmp_path: Path) -> None:
    emit_v15_evidence_remediation_plan_fixture(tmp_path)
    assert (tmp_path / FILENAME_EVIDENCE_REMEDIATION_PLAN).is_file()
    assert (tmp_path / REPORT_FILENAME_EVIDENCE_REMEDIATION_PLAN).is_file()
    assert (tmp_path / FILENAME_OPERATOR_RUNBOOK_MD).is_file()


def test_fixture_honest_status_and_flags(tmp_path: Path) -> None:
    sealed, _r, _, _, _ = emit_v15_evidence_remediation_plan_fixture(tmp_path)
    assert sealed.get("remediation_status_primary") == "evidence_gap_inventory_only"
    assert "operator_evidence_not_collected" in (sealed.get("remediation_status_secondary") or [])
    for k, v in default_m14_authorization_flags().items():
        assert sealed.get("authorization_flags", {}).get(k) is v


def test_gap_inventory_complete(tmp_path: Path) -> None:
    sealed, _, _, _, _ = emit_v15_evidence_remediation_plan_fixture(tmp_path)
    inv = sealed.get("evidence_gap_inventory")
    assert isinstance(inv, list)
    got = {g["gap_id"] for g in inv if isinstance(g, dict)}
    assert got == set(ALL_GAP_IDS)


def test_gate_coverage(tmp_path: Path) -> None:
    sealed, _, _, _, _ = emit_v15_evidence_remediation_plan_fixture(tmp_path)
    gates = sealed.get("remediation_gates")
    assert isinstance(gates, list)
    gids = [g.get("gate_id") for g in gates if isinstance(g, dict)]
    assert gids == list(ALL_REMEDIATION_GATE_IDS)
    for g in gates:
        if isinstance(g, dict):
            assert g.get("status") in {
                "pass",
                "warning",
                "fail",
                "blocked",
                "not_evaluated",
                "not_applicable",
            }


def test_proposed_roadmap_m15_m21(tmp_path: Path) -> None:
    sealed, _, _, _, _ = emit_v15_evidence_remediation_plan_fixture(tmp_path)
    road = sealed.get("proposed_roadmap_m15_m21")
    assert isinstance(road, list)
    assert len(road) == 7
    for row in road:
        if isinstance(row, dict):
            assert "proposed" in str(row.get("status", "")).lower()


def test_markdown_runbook_determinism_and_nonclaim(tmp_path: Path) -> None:
    emit_v15_evidence_remediation_plan_fixture(tmp_path)
    a = (tmp_path / FILENAME_OPERATOR_RUNBOOK_MD).read_text(encoding="utf-8")
    emit_v15_evidence_remediation_plan_fixture(tmp_path)
    b = (tmp_path / FILENAME_OPERATOR_RUNBOOK_MD).read_text(encoding="utf-8")
    assert a == b
    assert "does not execute" in a.lower() or "does not" in a.lower()
    for bad in (
        "v2 is authorized",
        "the agent is strong",
        "the checkpoint is promoted",
    ):
        assert bad not in a.lower()


def test_m13_binding_round_trip(tmp_path: Path) -> None:
    m13_dir = tmp_path / "m13"
    m13_dir.mkdir()
    emit_v15_v2_go_no_go_decision_fixture(m13_dir)
    p = m13_dir / "v15_v2_go_no_go_decision.json"
    parse_m13_v2_decision(p)
    out = tmp_path / "m14"
    sealed, _, _, _, _ = emit_v15_evidence_remediation_plan_with_m13(out, p)
    assert sealed.get("m13_v2_decision_json_canonical_sha256") != "0" * 64
    ctx = sealed.get("m13_decision_context")
    assert isinstance(ctx, dict) and ctx.get("m13_file_bound") is True
    assert sealed.get("contract_id") == CONTRACT_ID_EVIDENCE_REMEDIATION_PLAN


def test_m13_wrong_contract_fails(tmp_path: Path) -> None:
    bad = tmp_path / "bad.json"
    bad.write_text(json.dumps({"contract_id": "wrong", "v2_decision_id": "x"}), encoding="utf-8")
    with pytest.raises(ValueError, match="contract_id"):
        parse_m13_v2_decision(bad)


def test_cli_module_runs(tmp_path: Path) -> None:
    out = tmp_path / "cli_out"
    proc = subprocess.run(
        [
            sys.executable,
            "-m",
            "starlab.v15.emit_v15_evidence_remediation_plan",
            "--output-dir",
            str(out),
        ],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 0, proc.stderr
    assert (out / FILENAME_EVIDENCE_REMEDIATION_PLAN).is_file()
    j = json.loads((out / FILENAME_EVIDENCE_REMEDIATION_PLAN).read_text(encoding="utf-8"))
    assert j.get(SEAL_KEY_EVIDENCE_REMEDIATION_PLAN)
    jpop = {k: v for k, v in j.items() if k != SEAL_KEY_EVIDENCE_REMEDIATION_PLAN}
    from starlab.runs.json_util import sha256_hex_of_canonical_json

    assert j[SEAL_KEY_EVIDENCE_REMEDIATION_PLAN] == sha256_hex_of_canonical_json(jpop)


def test_governance_doc_mentions_m14() -> None:
    v15 = (REPO_ROOT / "docs" / "starlab-v1.5.md").read_text(encoding="utf-8")
    assert "V15-M14" in v15
    assert "starlab.v15.evidence_remediation_plan.v1" in v15
