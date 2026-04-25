"""V15-M05 strong-agent scorecard / benchmark protocol tests (fixture + operator; no matches)."""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

from starlab.runs.json_util import sha256_hex_of_canonical_json
from starlab.v15.strong_agent_scorecard_io import (
    build_strong_agent_scorecard_body_fixture,
    build_strong_agent_scorecard_body_operator,
    build_strong_agent_scorecard_report,
    emit_v15_strong_agent_scorecard,
    merge_operator_protocol,
    parse_protocol_json,
    seal_strong_agent_scorecard_body,
)
from starlab.v15.strong_agent_scorecard_models import (
    CONTRACT_ID_STRONG_AGENT_SCORECARD,
    FILENAME_STRONG_AGENT_SCORECARD,
    LADDER_STAGE_IDS,
    PROFILE_FIXTURE_CI,
    PROFILE_OPERATOR_DECLARED,
    PROTOCOL_PROFILE_ID,
    REPORT_FILENAME_STRONG_AGENT_SCORECARD,
    REQUIRED_SCORECARD_METRIC_NAMES,
    SEAL_KEY_STRONG_AGENT,
)

REPO_ROOT = Path(__file__).resolve().parents[1]
Z = "0" * 64

REQUIRED_TOP_KEYS = (
    "contract_id",
    "protocol_profile_id",
    "milestone_id",
    "generated_by",
    "profile",
    "benchmark_protocol_status",
    "benchmark_execution_performed",
    "strong_agent_claim_authorized",
    "long_gpu_run_authorized",
    "candidate_checkpoint_evaluated",
    "human_panel_included",
    "live_sc2_included",
    "xai_review_performed",
    "evidence_scope",
    "benchmark_identity",
    "evaluation_ladder",
    "candidate_subject",
    "baseline_subjects",
    "map_pool",
    "opponent_pool",
    "scorecard_fields",
    "gate_thresholds",
    "evidence_requirements",
    "failure_mode_probes",
    "xai_requirements",
    "reserved_human_panel_section",
    "optional_bindings",
    "status_vocabulary",
    "subject_kind_vocabulary",
    "metric_vocabulary",
    "gate_vocabulary",
    "evidence_kind_vocabulary",
    "required_fields",
    "check_results",
    "m05_verification_attestation",
    "non_claims",
    "carry_forward_items",
)
SEAL_KEY_ONLY = (SEAL_KEY_STRONG_AGENT,)


def _field_row(name: str) -> dict[str, object]:
    return {
        "field_name": name,
        "field_type": "ratio" if "rate" in name else "count",
        "required": True,
        "description": f"d:{name}",
        "status": "defined",
    }


def _complete_operator_protocol() -> dict[str, object]:
    return {
        "profile": "operator_declared",
        "protocol_profile_id": PROTOCOL_PROFILE_ID,
        "benchmark_id": "op.bench.1",
        "benchmark_name": "Operator test benchmark",
        "evaluation_ladder": [
            {
                "stage_id": "E0_artifact_integrity",
                "stage_name": "E0",
                "stage_status": "defined",
                "owner_milestone": "M05",
                "notes": "n",
            }
        ],
        "candidate_subject": {
            "subject_id": "cand1",
            "subject_kind": "candidate_checkpoint",
            "checkpoint_id": "ck1",
            "checkpoint_lineage_manifest_sha256": Z,
            "environment_lock_sha256": Z,
            "training_run_reference": "run1",
            "claim_use": "evaluation",
            "subject_status": "declared_only",
            "notes": "",
        },
        "baseline_subjects": [
            {
                "subject_id": "b1",
                "subject_kind": "scripted_baseline",
                "baseline_family": "m21",
                "source_milestone": "M21",
                "scorecard_reference": "r1",
                "subject_status": "defined",
                "notes": "n",
            }
        ],
        "map_pool": {
            "map_pool_id": "m1",
            "map_pool_name": "p1",
            "map_ids": ["a", "b"],
            "map_source": "declared",
            "rights_posture": "ok",
            "map_pool_status": "defined",
            "notes": "n",
        },
        "opponent_pool": {
            "opponent_pool_id": "o1",
            "opponent_kinds": ["h"],
            "opponent_ids": ["x"],
            "pool_status": "defined",
            "notes": "n",
        },
        "scorecard_fields": [_field_row(n) for n in REQUIRED_SCORECARD_METRIC_NAMES],
        "gate_thresholds": [
            {
                "gate_id": "g1",
                "gate_name": "g",
                "metric_name": "win_rate",
                "comparison": ">=",
                "threshold_value": "0.5",
                "required": True,
                "gate_status": "not_evaluated",
                "notes": "n",
            }
        ],
        "evidence_requirements": [
            {
                "evidence_id": "e1",
                "evidence_kind": "environment_lock",
                "required": True,
                "source_contract": "starlab.v15.long_gpu_environment_lock.v1",
                "evidence_status": "defined",
                "notes": "n",
            }
        ],
        "failure_mode_probes": [
            {
                "probe_id": "p1",
                "probe_kind": "econ",
                "required": True,
                "probe_status": "not_evaluated",
                "notes": "n",
            }
        ],
        "xai_requirements": [
            {
                "xai_requirement_id": "x1",
                "required_artifact": "pack",
                "required": True,
                "source_contract": "starlab.v15.xai_evidence_pack.v1",
                "requirement_status": "defined",
                "notes": "n",
            }
        ],
        "human_panel_reserved": {
            "reserved": True,
            "owner_milestone": "V15-M06",
            "execution_performed": False,
            "claim_authorized": False,
            "non_claim": "nc",
        },
        "operator_notes": "op",
        "non_claims": ["extra non-claim"],
    }


def test_cli_help() -> None:
    out = subprocess.run(
        [sys.executable, "-m", "starlab.v15.emit_v15_strong_agent_scorecard", "--help"],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
        check=True,
    )
    joined = (out.stdout + out.stderr).lower()
    assert "emit_v15_strong_agent_scorecard" in joined or "output-dir" in out.stdout


def test_cli_emits_artifacts_and_contract_ids(tmp_path: Path) -> None:
    subprocess.run(
        [
            sys.executable,
            "-m",
            "starlab.v15.emit_v15_strong_agent_scorecard",
            "--output-dir",
            str(tmp_path),
        ],
        cwd=str(REPO_ROOT),
        check=True,
    )
    c = tmp_path / FILENAME_STRONG_AGENT_SCORECARD
    r = tmp_path / REPORT_FILENAME_STRONG_AGENT_SCORECARD
    assert c.is_file() and r.is_file()
    data = json.loads(c.read_text(encoding="utf-8"))
    assert data["contract_id"] == CONTRACT_ID_STRONG_AGENT_SCORECARD
    assert data["protocol_profile_id"] == PROTOCOL_PROFILE_ID
    assert data["profile"] == PROFILE_FIXTURE_CI
    rep = json.loads(r.read_text(encoding="utf-8"))
    assert rep.get(SEAL_KEY_STRONG_AGENT) == data[SEAL_KEY_STRONG_AGENT]


def test_fixture_flags_and_booleans() -> None:
    body = build_strong_agent_scorecard_body_fixture()
    assert body["benchmark_protocol_status"] == "fixture_only"
    for k in (
        "benchmark_execution_performed",
        "strong_agent_claim_authorized",
        "long_gpu_run_authorized",
        "candidate_checkpoint_evaluated",
        "human_panel_included",
        "live_sc2_included",
        "xai_review_performed",
    ):
        assert body[k] is False, k


def test_required_sections_and_ladder_stages() -> None:
    body = build_strong_agent_scorecard_body_fixture()
    for k in REQUIRED_TOP_KEYS:
        assert k in body, k
    sealed = seal_strong_agent_scorecard_body(body)
    for k in SEAL_KEY_ONLY:
        assert k in sealed, k
    ids = [s["stage_id"] for s in body["evaluation_ladder"]]
    for sid in LADDER_STAGE_IDS:
        assert sid in ids, sid
    mset = {str(m.get("field_name")) for m in body["scorecard_fields"] if isinstance(m, dict)}
    for m in REQUIRED_SCORECARD_METRIC_NAMES:
        assert m in mset, m
    for group in body["status_vocabulary"].values():
        assert isinstance(group, list) and len(group) >= 1
    h = body["reserved_human_panel_section"]
    assert h.get("reserved") is True
    assert h.get("claim_authorized") is False
    x = body["xai_review_reserved"]
    assert x.get("reserved") is True
    assert x.get("review_performed") is False
    assert x.get("faithfulness_validated") is False


def test_report_includes_seal() -> None:
    body = build_strong_agent_scorecard_body_fixture()
    sealed = seal_strong_agent_scorecard_body(body)
    rep = build_strong_agent_scorecard_report(sealed)
    assert rep[SEAL_KEY_STRONG_AGENT] == sealed[SEAL_KEY_STRONG_AGENT]


GOLDEN_FIXTURE_SEAL = "c1fca80f8e7cbfadb2769ff0d52b8541fd1f9e51907a3fd5bc042a508b92951c"


def test_determinism_and_golden_seal() -> None:
    b1 = build_strong_agent_scorecard_body_fixture()
    b2 = build_strong_agent_scorecard_body_fixture()
    d1 = sha256_hex_of_canonical_json(b1)
    d2 = sha256_hex_of_canonical_json(b2)
    assert d1 == d2
    s1 = seal_strong_agent_scorecard_body(b1)
    s2 = seal_strong_agent_scorecard_body(b2)
    assert s1[SEAL_KEY_STRONG_AGENT] == s2[SEAL_KEY_STRONG_AGENT]
    assert s1[SEAL_KEY_STRONG_AGENT] == GOLDEN_FIXTURE_SEAL


def test_fixture_no_absolute_path_emission(tmp_path: Path) -> None:
    subprocess.run(
        [
            sys.executable,
            "-m",
            "starlab.v15.emit_v15_strong_agent_scorecard",
            "--output-dir",
            str(tmp_path),
        ],
        cwd=str(REPO_ROOT),
        check=True,
    )
    raw = (tmp_path / FILENAME_STRONG_AGENT_SCORECARD).read_text(encoding="utf-8")
    # Windows and POSIX absolute-path shapes should not appear (fixture has none)
    assert not re.search(r'[A-Za-z]:[\\/][^"\\s,}\]]+', raw)
    assert "<REDACTED_ABSOLUTE_PATH>" not in raw


def test_operator_protocol_partial_is_incomplete(tmp_path: Path) -> None:
    p = tmp_path / "part.json"
    p.write_text(
        json.dumps(
            {
                "profile": "operator_declared",
                "protocol_profile_id": PROTOCOL_PROFILE_ID,
                "benchmark_id": "b2",
                "benchmark_name": "n2",
            }
        ),
        encoding="utf-8",
    )
    d = parse_protocol_json(p)
    m = merge_operator_protocol(d)
    empty_binds = {"checkpoint_lineage": None, "xai_evidence": None, "environment_lock": None}
    out = build_strong_agent_scorecard_body_operator(m, optional_bindings=empty_binds)
    assert out["benchmark_protocol_status"] == "operator_declared_incomplete"
    assert out["benchmark_execution_performed"] is False


def test_operator_path_redaction(tmp_path: Path) -> None:
    p = tmp_path / "op.json"
    p.write_text(
        json.dumps(
            {
                "profile": "operator_declared",
                "protocol_profile_id": PROTOCOL_PROFILE_ID,
                "benchmark_id": "b2",
                "benchmark_name": "n2",
                "evaluation_ladder": [
                    {
                        "stage_id": "E0_artifact_integrity",
                        "stage_name": "E0",
                        "stage_status": "defined",
                        "owner_milestone": "M05",
                        "notes": "C:\\Users\\x\\secret\\file.json",
                    }
                ],
                "candidate_subject": {
                    "subject_id": "c1",
                    "subject_kind": "candidate_checkpoint",
                    "checkpoint_id": "ck1",
                    "checkpoint_lineage_manifest_sha256": Z,
                    "environment_lock_sha256": Z,
                    "training_run_reference": "run1",
                    "claim_use": "eval",
                    "subject_status": "declared",
                    "notes": "n",
                },
                "baseline_subjects": [
                    {
                        "subject_id": "b1",
                        "subject_kind": "scripted_baseline",
                        "baseline_family": "m21",
                        "source_milestone": "M21",
                        "scorecard_reference": "r",
                        "subject_status": "defined",
                        "notes": "n",
                    }
                ],
                "map_pool": {
                    "map_pool_id": "m1",
                    "map_pool_name": "p",
                    "map_ids": ["a"],
                    "map_source": "s",
                    "rights_posture": "r",
                    "map_pool_status": "defined",
                    "notes": "n",
                },
                "opponent_pool": {
                    "opponent_pool_id": "o1",
                    "opponent_kinds": ["h"],
                    "opponent_ids": ["x"],
                    "pool_status": "defined",
                    "notes": "n",
                },
                "scorecard_fields": [_field_row(n) for n in REQUIRED_SCORECARD_METRIC_NAMES],
                "gate_thresholds": [
                    {
                        "gate_id": "g1",
                        "gate_name": "g",
                        "metric_name": "win_rate",
                        "comparison": ">=",
                        "threshold_value": "0.5",
                        "required": True,
                        "gate_status": "not_evaluated",
                        "notes": "n",
                    }
                ],
                "evidence_requirements": [
                    {
                        "evidence_id": "e1",
                        "evidence_kind": "environment_lock",
                        "required": True,
                        "source_contract": "starlab.v15.long_gpu_environment_lock.v1",
                        "evidence_status": "defined",
                        "notes": "n",
                    }
                ],
                "failure_mode_probes": [
                    {
                        "probe_id": "p1",
                        "probe_kind": "econ",
                        "required": True,
                        "probe_status": "not_evaluated",
                        "notes": "n",
                    }
                ],
                "xai_requirements": [
                    {
                        "xai_requirement_id": "x1",
                        "required_artifact": "pack",
                        "required": True,
                        "source_contract": "starlab.v15.xai_evidence_pack.v1",
                        "requirement_status": "defined",
                        "notes": "n",
                    }
                ],
                "human_panel_reserved": {
                    "reserved": True,
                    "owner_milestone": "V15-M06",
                    "execution_performed": False,
                    "claim_authorized": False,
                    "non_claim": "c",
                },
                "operator_notes": "",
                "non_claims": [],
            }
        ),
        encoding="utf-8",
    )
    outd = tmp_path / "out_redact"
    sealed, _, c_path, _ = emit_v15_strong_agent_scorecard(
        outd,
        profile=PROFILE_OPERATOR_DECLARED,
        protocol_path=p,
    )
    out_txt = c_path.read_text(encoding="utf-8")
    assert "<REDACTED_ABSOLUTE_PATH>" in out_txt
    assert "C:\\\\Users" not in out_txt
    assert sealed["protocol_profile_id"] == PROTOCOL_PROFILE_ID
    assert sealed["long_gpu_run_authorized"] is False
    assert sealed["strong_agent_claim_authorized"] is False


def test_operator_complete_status_without_execution() -> None:
    op = _complete_operator_protocol()
    m = merge_operator_protocol(op)
    empty_binds = {"checkpoint_lineage": None, "xai_evidence": None, "environment_lock": None}
    out = build_strong_agent_scorecard_body_operator(m, optional_bindings=empty_binds)
    assert out["benchmark_protocol_status"] == "operator_declared_complete"
    assert out["benchmark_execution_performed"] is False
    assert out["strong_agent_claim_authorized"] is False
    assert out["long_gpu_run_authorized"] is False


def test_optional_binding_shas_only(tmp_path: Path) -> None:
    m02 = tmp_path / "m02.json"
    m02.write_text(
        '{"contract_id": "starlab.v15.long_gpu_environment_lock.v1"}\n',
        encoding="utf-8",
    )
    m03 = tmp_path / "m03.json"
    m03.write_text(
        '{"contract_id": "starlab.v15.checkpoint_lineage_manifest.v1"}\n',
        encoding="utf-8",
    )
    m04 = tmp_path / "m04.json"
    m04.write_text('{"contract_id": "starlab.v15.xai_evidence_pack.v1"}\n', encoding="utf-8")
    proto = tmp_path / "p.json"
    proto.write_text(json.dumps(_complete_operator_protocol()), encoding="utf-8")
    outd = tmp_path / "o"
    sealed, _, c_path, _ = emit_v15_strong_agent_scorecard(
        outd,
        profile=PROFILE_OPERATOR_DECLARED,
        protocol_path=proto,
        environment_lock_path=m02,
        checkpoint_lineage_path=m03,
        xai_evidence_path=m04,
    )
    b = json.loads(c_path.read_text(encoding="utf-8"))
    ob = b["optional_bindings"]
    for k, v in ob.items():
        if v is not None:
            assert len(str(v)) == 64, k
    assert "Users" not in c_path.read_text()
    assert sealed["strong_agent_claim_authorized"] is False


def test_runtime_and_governance_docs() -> None:
    rt = REPO_ROOT / "docs" / "runtime" / "v15_strong_agent_benchmark_protocol_v1.md"
    assert rt.is_file()
    t = rt.read_text(encoding="utf-8")
    assert CONTRACT_ID_STRONG_AGENT_SCORECARD in t
    assert "starlab.v15.strong_agent_benchmark_protocol.v1" in t
    s15 = (REPO_ROOT / "docs" / "starlab-v1.5.md").read_text(encoding="utf-8")
    assert "V15-M05" in s15
    assert "starlab.v15.strong_agent_scorecard.v1" in s15
    assert "M05 non-claims" in s15 or "M05" in s15
    sm = (REPO_ROOT / "docs" / "starlab.md").read_text(encoding="utf-8")
    assert "docs/starlab-v1.5.md" in sm
    assert "v15_strong_agent_benchmark_protocol_v1.md" in sm


def test_public_registers_no_new_data_rows() -> None:
    cp = (REPO_ROOT / "docs" / "checkpoint_asset_register.md").read_text(encoding="utf-8")
    assert "| — |" in cp or "No rows" in cp or "*No rows.*" in cp
    xr = (REPO_ROOT / "docs" / "xai_evidence_register.md").read_text(encoding="utf-8")
    assert "*No rows.*" in xr or "no real rows" in xr.lower()
