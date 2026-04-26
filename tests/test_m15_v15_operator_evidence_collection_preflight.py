"""V15-M15 operator evidence collection preflight — emit, bindings, and governance text."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest
from starlab.runs.json_util import sha256_hex_of_canonical_json
from starlab.v15.evidence_remediation_models import (
    ALL_GAP_IDS,
    ALL_REMEDIATION_GATE_IDS,
    CONTRACT_ID_EVIDENCE_REMEDIATION_PLAN,
    SEAL_KEY_EVIDENCE_REMEDIATION_PLAN,
    STATUS_OPERATOR_EVIDENCE_NOT_COLLECTED,
    default_m14_authorization_flags,
)
from starlab.v15.operator_evidence_preflight_io import (
    emit_v15_operator_evidence_collection_preflight,
    parse_m14_remediation_plan,
    seal_operator_evidence_preflight_body,
)
from starlab.v15.operator_evidence_preflight_models import (
    ALL_PREFLIGHT_GATE_IDS,
    ALL_SEQUENCE_IDS,
    CONTRACT_ID_OPERATOR_EVIDENCE_COLLECTION_PREFLIGHT,
    FILENAME_OPERATOR_EVIDENCE_COLLECTION_CHECKLIST_MD,
    FILENAME_OPERATOR_EVIDENCE_COLLECTION_PREFLIGHT,
    REPORT_FILENAME_OPERATOR_EVIDENCE_COLLECTION_PREFLIGHT,
    SEAL_KEY_ARTIFACT,
)
from starlab.v15.v2_decision_io import emit_v15_v2_go_no_go_decision_fixture

REPO_ROOT = Path(__file__).resolve().parents[1]


def _json(obj: object) -> str:
    return json.dumps(obj, ensure_ascii=True, sort_keys=True, separators=(",", ":"))


def _minimal_m14_for_binding() -> dict[str, object]:
    from starlab.v15.evidence_remediation_io import build_evidence_remediation_body_fixture

    body = build_evidence_remediation_body_fixture()
    return {
        "contract_id": body["contract_id"],
        "remediation_status_primary": body["remediation_status_primary"],
        "remediation_status_secondary": body["remediation_status_secondary"],
        "evidence_gap_inventory": body["evidence_gap_inventory"],
        "remediation_gates": body["remediation_gates"],
        "authorization_flags": body["authorization_flags"],
    }


def test_default_emission_three_files(tmp_path: Path) -> None:
    emit_v15_operator_evidence_collection_preflight(tmp_path)
    assert (tmp_path / FILENAME_OPERATOR_EVIDENCE_COLLECTION_PREFLIGHT).is_file()
    assert (tmp_path / REPORT_FILENAME_OPERATOR_EVIDENCE_COLLECTION_PREFLIGHT).is_file()
    assert (tmp_path / FILENAME_OPERATOR_EVIDENCE_COLLECTION_CHECKLIST_MD).is_file()


def test_json_deterministic_emit(tmp_path: Path) -> None:
    emit_v15_operator_evidence_collection_preflight(tmp_path)
    a = (tmp_path / FILENAME_OPERATOR_EVIDENCE_COLLECTION_PREFLIGHT).read_text(encoding="utf-8")
    emit_v15_operator_evidence_collection_preflight(tmp_path)
    b = (tmp_path / FILENAME_OPERATOR_EVIDENCE_COLLECTION_PREFLIGHT).read_text(encoding="utf-8")
    assert a == b


def test_contract_and_defaults(tmp_path: Path) -> None:
    sealed, _, _, _, _ = emit_v15_operator_evidence_collection_preflight(tmp_path)
    assert sealed.get("contract_id") == CONTRACT_ID_OPERATOR_EVIDENCE_COLLECTION_PREFLIGHT
    assert sealed.get("operator_evidence_collection_status") == "not_started"
    assert sealed.get("v2_authorized") is False
    assert sealed.get("v2_recharter_authorized") is False
    base = {k: v for k, v in sealed.items() if k != SEAL_KEY_ARTIFACT}
    assert sealed[SEAL_KEY_ARTIFACT] == sha256_hex_of_canonical_json(base)


def test_future_milestone_map_m16_m21(tmp_path: Path) -> None:
    sealed, _, _, _, _ = emit_v15_operator_evidence_collection_preflight(tmp_path)
    mp = sealed.get("future_milestone_map")
    assert isinstance(mp, list)
    ids = {x.get("milestone") for x in mp if isinstance(x, dict)}
    for m in (f"V15-M{i}" for i in range(16, 22)):
        assert m in ids


def test_evidence_sequence_s0_s10(tmp_path: Path) -> None:
    sealed, _, _, _, _ = emit_v15_operator_evidence_collection_preflight(tmp_path)
    seq = sealed.get("evidence_sequence")
    assert isinstance(seq, list)
    got = [x.get("sequence_id") for x in seq if isinstance(x, dict)]
    assert got == list(ALL_SEQUENCE_IDS)


def test_preflight_gates_p0_p14(tmp_path: Path) -> None:
    sealed, _, _, _, _ = emit_v15_operator_evidence_collection_preflight(tmp_path)
    gates = sealed.get("preflight_gates")
    assert isinstance(gates, list)
    got = [g.get("gate_id") for g in gates if isinstance(g, dict)]
    assert got == list(ALL_PREFLIGHT_GATE_IDS)


def test_register_touchpoints(tmp_path: Path) -> None:
    sealed, _, _, _, _ = emit_v15_operator_evidence_collection_preflight(tmp_path)
    reg = sealed.get("register_touchpoints")
    assert isinstance(reg, list)
    paths = {x.get("register_doc") for x in reg if isinstance(x, dict)}
    assert "docs/rights_register.md" in paths
    assert "docs/human_benchmark_register.md" in paths


def test_public_private_boundary_excludes_raw_private_artifacts(
    tmp_path: Path,
) -> None:
    sealed, _, _, _, _ = emit_v15_operator_evidence_collection_preflight(tmp_path)
    b = sealed.get("public_private_boundary")
    assert isinstance(b, dict)
    priv = b.get("private_local_only", [])
    assert isinstance(priv, list)
    low = " ".join(str(x) for x in priv).lower()
    for needle in (
        "model_weights",
        "checkpoint",
        "replay",
        "saliency",
    ):
        assert needle in low
    safe = b.get("public_safe", [])
    assert "non_claims" in " ".join(str(x) for x in safe).lower()


def test_m13_binding_with_fixture_m13(tmp_path: Path) -> None:
    m13_dir = tmp_path / "m13"
    m13_dir.mkdir()
    emit_v15_v2_go_no_go_decision_fixture(m13_dir)
    p13 = m13_dir / "v15_v2_go_no_go_decision.json"
    out = tmp_path / "out1"
    sealed, _, _, _, _ = emit_v15_operator_evidence_collection_preflight(out, m13_path=p13)
    b = sealed.get("m13_binding")
    assert isinstance(b, dict) and b.get("binding_mode") == "file_bound"
    assert b.get("m13_v2_decision_json_canonical_sha256") not in ("0" * 64, None, "")


def test_m14_binding_with_minimal_m14_json(tmp_path: Path) -> None:
    p14 = tmp_path / "m14.json"
    p14.write_text(_json(_minimal_m14_for_binding()) + "\n", encoding="utf-8")
    out = tmp_path / "o2"
    sealed, _, _, _, _ = emit_v15_operator_evidence_collection_preflight(out, m14_path=p14)
    b = sealed.get("m14_binding")
    assert isinstance(b, dict) and b.get("binding_mode") == "file_bound"
    assert b.get("m14_remediation_plan_json_canonical_sha256") not in (
        "0" * 64,
        None,
        "",
    )
    # Contract JSON must be valid for parser
    parse_m14_remediation_plan(p14)


def test_malformed_m13_fails(tmp_path: Path) -> None:
    bad = tmp_path / "badm13.json"
    bad.write_text(
        _json(
            {
                "contract_id": "wrong",
                "v2_decision_id": "x",
            }
        )
        + "\n",
        encoding="utf-8",
    )
    p = subprocess.run(
        [
            sys.executable,
            "-m",
            "starlab.v15.emit_v15_operator_evidence_collection_preflight",
            "--output-dir",
            str(tmp_path / "ox"),
            "--m13-v2-decision-json",
            str(bad),
        ],
        cwd=str(REPO_ROOT),
        check=False,
        capture_output=True,
        text=True,
    )
    assert p.returncode != 0


def test_malformed_m14_fails(tmp_path: Path) -> None:
    bad = tmp_path / "badm14.json"
    bad.write_text(
        _json(
            {
                "contract_id": "wrong",
            }
        )
        + "\n",
        encoding="utf-8",
    )
    p = subprocess.run(
        [
            sys.executable,
            "-m",
            "starlab.v15.emit_v15_operator_evidence_collection_preflight",
            "--output-dir",
            str(tmp_path / "oy"),
            "--m14-remediation-plan-json",
            str(bad),
        ],
        cwd=str(REPO_ROOT),
        check=False,
        capture_output=True,
        text=True,
    )
    assert p.returncode != 0


def test_seal_tamper_detected() -> None:
    from starlab.v15.operator_evidence_preflight_io import build_operator_evidence_preflight_body

    body = build_operator_evidence_preflight_body(m13_path=None, m14_path=None)
    sealed = seal_operator_evidence_preflight_body(body)
    sealed2 = dict(sealed)
    sealed2["v2_authorized"] = True
    base2 = {k: v for k, v in sealed2.items() if k != SEAL_KEY_ARTIFACT}
    assert sha256_hex_of_canonical_json(base2) != sealed.get(SEAL_KEY_ARTIFACT)


def test_cli_fixture_mode(tmp_path: Path) -> None:
    out = tmp_path / "cli"
    res = subprocess.run(
        [
            sys.executable,
            "-m",
            "starlab.v15.emit_v15_operator_evidence_collection_preflight",
            "--output-dir",
            str(out),
        ],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
        check=False,
    )
    assert res.returncode == 0, res.stderr
    j = json.loads(
        (out / FILENAME_OPERATOR_EVIDENCE_COLLECTION_PREFLIGHT).read_text(encoding="utf-8")
    )
    assert j[SEAL_KEY_ARTIFACT]
    jpop = {k: v for k, v in j.items() if k != SEAL_KEY_ARTIFACT}
    assert j[SEAL_KEY_ARTIFACT] == sha256_hex_of_canonical_json(jpop)


def test_runtime_doc_mentions_checklist() -> None:
    rt = REPO_ROOT / "docs" / "runtime" / "v15_operator_evidence_collection_preflight_v1.md"
    t = rt.read_text(encoding="utf-8")
    assert "V15-M15" in t
    assert CONTRACT_ID_OPERATOR_EVIDENCE_COLLECTION_PREFLIGHT in t
    assert "v15_operator_evidence_collection_checklist.md" in t
    assert "non-claims" in t.lower() or "Non-claims" in t


def test_starlab_v15_mentions_m15() -> None:
    v15 = (REPO_ROOT / "docs" / "starlab-v1.5.md").read_text(encoding="utf-8")
    assert "V15-M15" in v15
    assert CONTRACT_ID_OPERATOR_EVIDENCE_COLLECTION_PREFLIGHT in v15


def test_rights_register_m15() -> None:
    r = (REPO_ROOT / "docs" / "rights_register.md").read_text(encoding="utf-8")
    assert "V15-M15" in r
    assert "preflight" in r.lower()


def test_output_no_collection_claims(tmp_path: Path) -> None:
    sealed, _, _, _, _ = emit_v15_operator_evidence_collection_preflight(tmp_path)
    assert sealed.get("operator_evidence_collection_status") == "not_started"
    no_seal = {k: v for k, v in sealed.items() if k != SEAL_KEY_ARTIFACT}
    assert no_seal.get("v2_authorized") is False
    blob = _json(no_seal).lower()
    assert "operator_evidence_collected" not in blob
    assert "evidence collection completed" not in blob


def test_m14_parse_requires_all_gaps(tmp_path: Path) -> None:
    body = _minimal_m14_for_binding()
    inv_raw = body.get("evidence_gap_inventory", [])
    assert isinstance(inv_raw, list)
    inv = list(inv_raw)
    if inv:
        inv.pop(0)
    body["evidence_gap_inventory"] = inv
    p = tmp_path / "incomplete14.json"
    p.write_text(_json(body) + "\n", encoding="utf-8")
    with pytest.raises(ValueError, match="gap_id"):
        parse_m14_remediation_plan(p)


def test_m14_rejects_v2_authorized_in_auth_flags(tmp_path: Path) -> None:
    body = _minimal_m14_for_binding()
    af = dict(default_m14_authorization_flags())
    af["v2_authorized"] = True
    body["authorization_flags"] = af
    p = tmp_path / "v14.json"
    p.write_text(_json(body) + "\n", encoding="utf-8")
    with pytest.raises(ValueError, match="v2_authorized"):
        parse_m14_remediation_plan(p)


def test_m14_fixture_same_contract_as_emit(tmp_path: Path) -> None:
    """M14 body from fixture build matches parser surface."""
    p = tmp_path / "em14.json"
    p.write_text(
        _json(
            {
                "contract_id": CONTRACT_ID_EVIDENCE_REMEDIATION_PLAN,
                "remediation_status_primary": "evidence_gap_inventory_only",
                "remediation_status_secondary": [
                    STATUS_OPERATOR_EVIDENCE_NOT_COLLECTED,
                    "remediation_plan_ready",
                ],
                "evidence_gap_inventory": [
                    {"gap_id": gid, "status": "open"} for gid in ALL_GAP_IDS
                ],
                "remediation_gates": [
                    {"gate_id": gid, "status": "pass", "notes": "x"}
                    for gid in ALL_REMEDIATION_GATE_IDS
                ],
                "authorization_flags": {
                    "v2_authorized": False,
                },
            }
        )
        + "\n",
        encoding="utf-8",
    )
    parse_m14_remediation_plan(p)
    out = tmp_path / "b14"
    emit_v15_operator_evidence_collection_preflight(out, m14_path=p)
    s = json.loads(
        (out / FILENAME_OPERATOR_EVIDENCE_COLLECTION_PREFLIGHT).read_text(encoding="utf-8")
    )
    # Must not have other contract seal keys mixed in
    assert SEAL_KEY_EVIDENCE_REMEDIATION_PLAN not in s
