"""V15-M06 human panel benchmark protocol tests (fixture + operator; no human execution)."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from starlab.runs.json_util import sha256_hex_of_canonical_json
from starlab.v15.human_panel_benchmark_io import (
    build_human_panel_benchmark_body_fixture,
    build_human_panel_benchmark_body_operator,
    build_human_panel_benchmark_report,
    emit_v15_human_panel_benchmark,
    merge_operator_protocol,
    parse_protocol_json,
    redact_path_and_contact_in_value,
    seal_human_panel_benchmark_body,
)
from starlab.v15.human_panel_benchmark_models import (
    ALLOWED_FUTURE_CLAIM_BOUNDARY,
    CONTRACT_ID_HUMAN_PANEL_BENCHMARK,
    EVIDENCE_REQUIREMENT_CLASS_IDS,
    FILENAME_HUMAN_PANEL_BENCHMARK,
    PARTICIPANT_TIER_IDS,
    PRIVACY_POSTURE_IDS,
    PROFILE_OPERATOR_DECLARED,
    PROTOCOL_PROFILE_ID_HUMAN_PANEL,
    REPORT_FILENAME_HUMAN_PANEL_BENCHMARK,
    SEAL_KEY_HUMAN_PANEL,
    THRESHOLD_OPTION_IDS,
)

REPO_ROOT = Path(__file__).resolve().parents[1]
Z = "0" * 64


def _privacy_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for pid in PRIVACY_POSTURE_IDS:
        rows.append(
            {
                "posture_id": pid,
                "enforcement": "required",
                "protocol_status": "defined",
                "notes": "n",
            }
        )
    return rows


def _tier_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for tid in PARTICIPANT_TIER_IDS:
        rows.append(
            {
                "tier_id": tid,
                "description": f"d:{tid}",
                "protocol_status": "defined",
                "notes": "",
            }
        )
    return rows


def _threshold_rows() -> list[dict[str, str]]:
    out: list[dict[str, str]] = []
    for oid in THRESHOLD_OPTION_IDS:
        out.append(
            {
                "option_id": oid,
                "description": f"t:{oid}",
                "protocol_status": "defined",
                "notes": "",
            }
        )
    return out


def _evidence_rows() -> list[dict[str, object]]:
    out: list[dict[str, object]] = []
    for eid in EVIDENCE_REQUIREMENT_CLASS_IDS:
        out.append(
            {
                "evidence_class_id": eid,
                "required": True,
                "storage_posture": "declared",
                "protocol_status": "defined",
                "notes": "",
            }
        )
    return out


def _minimal_complete_operator_protocol() -> dict[str, object]:
    return {
        "profile": "operator_declared",
        "protocol_profile_id": PROTOCOL_PROFILE_ID_HUMAN_PANEL,
        "benchmark_id": "op.human.1",
        "benchmark_name": "Operator test human panel protocol",
        "participant_privacy_profile": _privacy_rows(),
        "participant_tiers": _tier_rows(),
        "eligibility_rules": [{"rule_id": "e1", "text": "eligible", "protocol_status": "defined"}],
        "consent_requirements": [
            {"requirement_id": "c1", "text": "consent", "protocol_status": "defined"}
        ],
        "session_rules": {"session_format": "declared", "execution_status": "not_executed"},
        "match_rules": {
            "race": "Terran_first",
            "mode": "1v1",
            "execution_status": "not_executed",
        },
        "map_pool_policy": {"map_pool_id": "m1", "execution_status": "not_executed"},
        "agent_identity_requirements": {"checkpoint_id_binding": "required"},
        "checkpoint_binding_requirements": {"lineage_or_sha_ref": "required"},
        "replay_capture_requirements": {"replay_capture": "required"},
        "result_policy": {"result_recording": "predeclared"},
        "threshold_policy": _threshold_rows(),
        "evidence_requirements": _evidence_rows(),
        "claim_boundary": {
            "allowed_shape": ALLOWED_FUTURE_CLAIM_BOUNDARY,
            "disallowed_shapes": ["beats all humans"],
        },
        "non_claims": ["operator extra non-claim"],
        "redaction_policy": {"notes": "redact paths"},
        "operator_notes": "",
        "extension_flags": [],
    }


def test_fixture_determinism() -> None:
    a = build_human_panel_benchmark_body_fixture()
    b = build_human_panel_benchmark_body_fixture()
    assert a == b
    sa = sha256_hex_of_canonical_json(a)
    sb = sha256_hex_of_canonical_json(b)
    assert sa == sb


def test_fixture_required_fields() -> None:
    body = build_human_panel_benchmark_body_fixture()
    assert body["contract_id"] == CONTRACT_ID_HUMAN_PANEL_BENCHMARK
    assert body["protocol_profile_id"] == PROTOCOL_PROFILE_ID_HUMAN_PANEL
    for k in (
        "benchmark_execution_performed",
        "human_panel_execution_performed",
        "human_benchmark_claim_authorized",
        "strong_agent_claim_authorized",
        "long_gpu_run_authorized",
    ):
        assert body[k] is False
    assert "human_panel_benchmark_sha256" not in body
    for tid in PARTICIPANT_TIER_IDS:
        found = [r for r in body["participant_tiers"] if r["tier_id"] == tid]
        assert len(found) == 1
    opts = {r["option_id"] for r in body["threshold_policy"]}
    assert "majority_threshold_gt_50" in opts
    assert "supermajority_threshold_gte_65" in opts
    ev_ids = {r["evidence_class_id"] for r in body["evidence_requirements"]}
    for req in EVIDENCE_REQUIREMENT_CLASS_IDS:
        assert req in ev_ids
    ncl = "\n".join(body["non_claims"])
    assert "ladder" in ncl.lower() or "GPU" in ncl
    assert "v2" in ncl.lower() or "PX2" in ncl
    s = json.dumps(body)
    assert "@" not in s
    assert "discord" not in s.lower()
    assert "battletag" not in s.lower()


def test_seal_and_report_match() -> None:
    body = build_human_panel_benchmark_body_fixture()
    sealed = seal_human_panel_benchmark_body(body)
    assert SEAL_KEY_HUMAN_PANEL in sealed
    rep = build_human_panel_benchmark_report(sealed, redaction_count=0)
    assert rep["artifact_sha256"] == sealed[SEAL_KEY_HUMAN_PANEL]
    assert rep["redaction_count"] == 0
    assert rep["claim_authorized"] is False
    assert rep["execution_performed"] is False


def test_emit_cli_fixture_writes_files(tmp_path: Path) -> None:
    out = tmp_path / "out"
    cmd = [
        sys.executable,
        "-m",
        "starlab.v15.emit_v15_human_panel_benchmark",
        "--output-dir",
        str(out),
    ]
    subprocess.run(cmd, check=True, cwd=REPO_ROOT)
    c = out / FILENAME_HUMAN_PANEL_BENCHMARK
    r = out / REPORT_FILENAME_HUMAN_PANEL_BENCHMARK
    assert c.is_file() and r.is_file()
    raw = json.loads(c.read_text(encoding="utf-8"))
    assert raw["contract_id"] == CONTRACT_ID_HUMAN_PANEL_BENCHMARK


def test_operator_minimal_valid_protocol(tmp_path: Path) -> None:
    proto = tmp_path / "p.json"
    proto.write_text(
        json.dumps(_minimal_complete_operator_protocol(), sort_keys=True), encoding="utf-8"
    )
    data = parse_protocol_json(proto)
    body = build_human_panel_benchmark_body_operator(
        data,
        optional_bindings={
            "environment_lock": None,
            "checkpoint_lineage": None,
            "strong_agent_scorecard": None,
            "xai_evidence": None,
        },
    )
    for k in (
        "benchmark_execution_performed",
        "human_panel_execution_performed",
        "human_benchmark_claim_authorized",
        "strong_agent_claim_authorized",
        "long_gpu_run_authorized",
    ):
        assert body[k] is False


def test_operator_redacts_absolute_paths_and_contact(tmp_path: Path) -> None:
    p = _minimal_complete_operator_protocol()
    p["operator_notes"] = r"Contact: user@example.com and C:\Users\o\sc2\Maps"
    proto = tmp_path / "p2.json"
    proto.write_text(json.dumps(p, sort_keys=True), encoding="utf-8")
    out = tmp_path / "out2"
    _, _, red_c, c_path, _ = emit_v15_human_panel_benchmark(
        out,
        profile=PROFILE_OPERATOR_DECLARED,
        protocol_path=proto,
    )
    text = c_path.read_text(encoding="utf-8")
    assert "user@example.com" not in text
    assert r"C:\Users" not in text
    assert "REDACTED" in text
    assert red_c >= 1


def test_invalid_protocol_unknown_key_fails(tmp_path: Path) -> None:
    bad = tmp_path / "bad.json"
    d = _minimal_complete_operator_protocol()
    d["not_a_key"] = 1
    bad.write_text(json.dumps(d), encoding="utf-8")
    try:
        parse_protocol_json(bad)
    except ValueError as e:
        assert "unknown" in str(e).lower()
    else:
        raise AssertionError("expected ValueError")


def test_invalid_protocol_not_object_fails(tmp_path: Path) -> None:
    bad = tmp_path / "arr.json"
    bad.write_text("[1,2,3]", encoding="utf-8")
    try:
        parse_protocol_json(bad)
    except ValueError:
        return
    raise AssertionError("expected ValueError")


def test_optional_binding_hashes_only(tmp_path: Path) -> None:
    m02 = tmp_path / "e.json"
    m02.write_text(json.dumps({"a": 1, "b": 2}, sort_keys=True), encoding="utf-8")
    proto = tmp_path / "p3.json"
    proto.write_text(
        json.dumps(_minimal_complete_operator_protocol(), sort_keys=True), encoding="utf-8"
    )
    out = tmp_path / "out3"
    _, rep, _rc, c_path, _ = emit_v15_human_panel_benchmark(
        out,
        profile=PROFILE_OPERATOR_DECLARED,
        protocol_path=proto,
        environment_lock_path=m02,
    )
    raw = json.loads(c_path.read_text(encoding="utf-8"))
    sh = raw["optional_bindings"]["environment_lock_json_canonical_sha256"]
    assert sh and len(sh) == 64
    keys_joined = " ".join(rep["optional_binding_keys"]).lower()
    assert "environment" in keys_joined


def test_redact_spy_on_email_key() -> None:
    o = redact_path_and_contact_in_value({"email": "x@y.com", "a": 1})
    assert o["email"] == "<REDACTED_PII>" or "<REDACTED" in str(o["email"])


def test_merge_operator_protocol() -> None:
    m = merge_operator_protocol({"benchmark_id": "x", "benchmark_name": "n"})
    assert m["benchmark_id"] == "x"
