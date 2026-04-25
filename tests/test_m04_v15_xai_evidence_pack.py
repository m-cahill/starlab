"""V15-M04: XAI evidence pack deterministic JSON + governance pointers."""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

import pytest
from starlab.runs.json_util import sha256_hex_of_canonical_json
from starlab.v15.xai_evidence_io import (
    build_xai_evidence_body,
    build_xai_evidence_body_fixture,
    emit_v15_xai_evidence_pack,
    parse_evidence_json,
    seal_xai_evidence_body,
)
from starlab.v15.xai_evidence_models import (
    CONTRACT_ID_XAI_EVIDENCE,
    FILENAME_XAI_EVIDENCE,
    PROFILE_FIXTURE_CI,
    PROFILE_OPERATOR_DECLARED,
    REPORT_FILENAME_XAI_EVIDENCE,
    REQUIRED_LOGICAL_ARTIFACT_NAMES,
    SCENE_TYPE_VOCABULARY,
    SEAL_KEY_XAI_EVIDENCE,
    STATUS_VOCABULARY,
)

REPO_ROOT = Path(__file__).resolve().parents[1]
Z = "0" * 64

REQUIRED_TOP_KEYS = (
    "contract_id",
    "milestone_id",
    "generated_by",
    "profile",
    "xai_evidence_status",
    "long_gpu_run_authorized",
    "real_xai_inference_executed",
    "replay_bound",
    "checkpoint_bound",
    "checkpoint_bytes_verified",
    "explanation_faithfulness_validated",
    "evidence_scope",
    "xai_pack_identity",
    "replay_identity",
    "checkpoint_identity",
    "decision_trace",
    "critical_decision_index",
    "attribution_summary",
    "concept_activation_summary",
    "counterfactual_probe_results",
    "alternative_action_rankings",
    "uncertainty_report",
    "replay_overlay_manifest",
    "xai_explanation_report",
    "required_artifact_names",
    "status_vocabulary",
    "scene_type_vocabulary",
    "method_vocabulary",
    "path_disclosure_vocabulary",
    "required_fields",
    "check_results",
    "m04_verification_attestation",
    "non_claims",
    "carry_forward_items",
)


def _replay() -> dict[str, object]:
    return {
        "replay_id": "op-replay-1",
        "replay_reference": "logical:replay/op1",
        "replay_sha256": Z,
        "replay_binding_status": "declared_only",
        "source_milestone": "V15-M04",
        "notes": "operator",
    }


def _checkpoint() -> dict[str, object]:
    return {
        "checkpoint_id": "op-cp-1",
        "checkpoint_reference": "logical:ckpt/op1",
        "checkpoint_lineage_manifest_sha256": Z,
        "checkpoint_hash_verification_status": "declared_only",
        "checkpoint_binding_status": "declared_only",
        "source_milestone": "V15-M04",
        "notes": "operator",
    }


def _dt() -> list[dict[str, object]]:
    return [
        {
            "decision_id": "d1",
            "gameloop": 1,
            "agent_perspective": "t",
            "decision_type": "macro",
            "selected_action": "a0",
            "selected_action_label": "l0",
            "available_alternatives_count": 2,
            "state_summary_reference": "s",
            "input_feature_references": "f",
            "policy_head": "h",
            "confidence": 0.5,
            "trace_status": "declared_only",
            "notes": "n",
        }
    ]


def _cdi() -> list[dict[str, object]]:
    return [
        {
            "decision_id": "d1",
            "criticality_reason": "test",
            "scene_type": "opening_build",
            "expected_review_status": "pending",
            "linked_trace_status": "declared_only",
            "notes": "n",
        }
    ]


def _attr() -> list[dict[str, object]]:
    return [
        {
            "decision_id": "d1",
            "method_id": "fixture_method",
            "feature_group": "g",
            "attribution_score": 0.1,
            "normalization_policy": "n",
            "attribution_status": "declared_only",
            "notes": "n",
        }
    ]


def _conc() -> list[dict[str, object]]:
    return [
        {
            "decision_id": "d1",
            "concept_id": "c1",
            "concept_label": "cl",
            "activation_score": 0.2,
            "concept_source": "op",
            "concept_status": "declared_only",
            "notes": "n",
        }
    ]


def _cf() -> list[dict[str, object]]:
    return [
        {
            "decision_id": "d1",
            "counterfactual_id": "cf1",
            "changed_factor": "x",
            "original_action": "a0",
            "counterfactual_action": "a1",
            "outcome_delta_summary": "d",
            "counterfactual_status": "declared_only",
            "notes": "n",
        }
    ]


def _alt() -> list[dict[str, object]]:
    return [
        {
            "decision_id": "d1",
            "rank": 1,
            "action_id": "x",
            "action_label": "l",
            "score": 0.3,
            "why_not_selected_summary": "w",
            "ranking_status": "declared_only",
            "notes": "n",
        }
    ]


def _unc() -> list[dict[str, object]]:
    return [
        {
            "decision_id": "d1",
            "uncertainty_kind": "entropy",
            "uncertainty_value": 0.4,
            "threshold_policy": "t",
            "uncertainty_status": "declared_only",
            "notes": "n",
        }
    ]


def _ovl() -> list[dict[str, object]]:
    return [
        {
            "overlay_id": "o1",
            "decision_id": "d1",
            "overlay_kind": "k",
            "overlay_reference": "r",
            "path_disclosure": "logical_reference_only",
            "overlay_status": "declared_only",
            "notes": "n",
        }
    ]


def _xrep() -> list[dict[str, object]]:
    return [
        {
            "report_id": "rep1",
            "report_format": "md",
            "report_reference": "rr",
            "path_disclosure": "logical_reference_only",
            "report_status": "declared_only",
            "notes": "n",
        }
    ]


def _complete_evidence_dict() -> dict[str, object]:
    return {
        "profile": "operator_declared",
        "xai_pack_id": "op-pack-1",
        "replay_identity": _replay(),
        "checkpoint_identity": _checkpoint(),
        "decision_trace": _dt(),
        "critical_decision_index": _cdi(),
        "attribution_summary": _attr(),
        "concept_activation_summary": _conc(),
        "counterfactual_probe_results": _cf(),
        "alternative_action_rankings": _alt(),
        "uncertainty_report": _unc(),
        "replay_overlay_manifest": _ovl(),
        "xai_explanation_report": _xrep(),
    }


def test_xai_evidence_seal_stable() -> None:
    body = build_xai_evidence_body_fixture()
    sealed = seal_xai_evidence_body(body)
    assert sealed[SEAL_KEY_XAI_EVIDENCE] == sha256_hex_of_canonical_json(body)
    assert sealed["contract_id"] == CONTRACT_ID_XAI_EVIDENCE


def test_xai_evidence_golden_sha256() -> None:
    body = build_xai_evidence_body_fixture()
    sealed = seal_xai_evidence_body(body)
    assert sealed[SEAL_KEY_XAI_EVIDENCE] == (
        "562fd6f650df7028b4f63d85d74bdc615b04b843d9576431870a7fa342216f6b"
    )


def test_emit_fixture_writes_files(tmp_path: Path) -> None:
    sealed, rep, c_path, r_path = emit_v15_xai_evidence_pack(
        tmp_path,
        profile=PROFILE_FIXTURE_CI,
        evidence_path=None,
        environment_lock_path=None,
        checkpoint_lineage_path=None,
    )
    assert c_path.name == FILENAME_XAI_EVIDENCE
    assert r_path.name == REPORT_FILENAME_XAI_EVIDENCE
    assert rep["xai_evidence_pack_sha256"] == sealed[SEAL_KEY_XAI_EVIDENCE]


def test_emit_is_deterministic(tmp_path: Path, tmp_path_factory: pytest.TempPathFactory) -> None:
    a = tmp_path_factory.mktemp("a")
    b = tmp_path_factory.mktemp("b")
    emit_v15_xai_evidence_pack(
        a,
        profile=PROFILE_FIXTURE_CI,
        evidence_path=None,
        environment_lock_path=None,
        checkpoint_lineage_path=None,
    )
    emit_v15_xai_evidence_pack(
        b,
        profile=PROFILE_FIXTURE_CI,
        evidence_path=None,
        environment_lock_path=None,
        checkpoint_lineage_path=None,
    )
    t1 = (a / FILENAME_XAI_EVIDENCE).read_text(encoding="utf-8")
    t2 = (b / FILENAME_XAI_EVIDENCE).read_text(encoding="utf-8")
    assert t1 == t2


def test_fixture_posture() -> None:
    body = build_xai_evidence_body(
        PROFILE_FIXTURE_CI,
        evidence_data=None,
        environment_lock_path=None,
        checkpoint_lineage_path=None,
    )
    assert body["xai_evidence_status"] == "fixture_only"
    assert body["long_gpu_run_authorized"] is False
    assert body["real_xai_inference_executed"] is False
    assert body["replay_bound"] is False
    assert body["checkpoint_bound"] is False
    assert body["checkpoint_bytes_verified"] is False
    assert body["explanation_faithfulness_validated"] is False
    assert body["profile"] == "fixture_ci"


def test_fixture_no_absolute_path_patterns(tmp_path: Path) -> None:
    emit_v15_xai_evidence_pack(
        tmp_path,
        profile=PROFILE_FIXTURE_CI,
        evidence_path=None,
        environment_lock_path=None,
        checkpoint_lineage_path=None,
    )
    text = (tmp_path / FILENAME_XAI_EVIDENCE).read_text(encoding="utf-8")
    assert not re.search(r"[A-Za-z]:\\", text)
    assert "\\\\" not in text


def test_non_claims_present() -> None:
    body = build_xai_evidence_body_fixture()
    assert "m04_executes_xai_inference" in body["non_claims"]
    assert "px2_m04_opened" in body["non_claims"]


def test_required_sections_and_vocab() -> None:
    body = build_xai_evidence_body_fixture()
    for k in REQUIRED_TOP_KEYS:
        assert k in body, f"missing {k}"
    assert set(body["status_vocabulary"]["xai_evidence_status"]) == set(
        STATUS_VOCABULARY["xai_evidence_status"]
    )
    assert set(body["scene_type_vocabulary"]) == set(SCENE_TYPE_VOCABULARY)
    assert set(REQUIRED_LOGICAL_ARTIFACT_NAMES).issubset(set(body["required_artifact_names"]))


def test_required_artifact_names_exactly() -> None:
    body = build_xai_evidence_body_fixture()
    assert body["required_artifact_names"] == list(REQUIRED_LOGICAL_ARTIFACT_NAMES)


def test_report_has_sha256_field(tmp_path: Path) -> None:
    _, rep, _, _ = emit_v15_xai_evidence_pack(
        tmp_path,
        profile=PROFILE_FIXTURE_CI,
        evidence_path=None,
        environment_lock_path=None,
        checkpoint_lineage_path=None,
    )
    assert "xai_evidence_pack_sha256" in rep
    assert rep["xai_evidence_pack_sha256"]


def test_runtime_doc_v15_m04() -> None:
    doc = (REPO_ROOT / "docs" / "runtime" / "v15_xai_evidence_contract_v1.md").read_text(
        encoding="utf-8"
    )
    assert "starlab.v15.xai_evidence_pack.v1" in doc
    v15 = (REPO_ROOT / "docs" / "starlab-v1.5.md").read_text(encoding="utf-8")
    assert "V15-M04" in v15
    assert "starlab.v15.xai_evidence_pack.v1" in v15
    assert "python -m starlab.v15.emit_v15_xai_evidence_pack" in v15
    assert "**M04 non-claims" in v15


def test_emit_cli_help() -> None:
    proc = subprocess.run(
        [sys.executable, "-m", "starlab.v15.emit_v15_xai_evidence_pack", "--help"],
        check=False,
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0
    assert "v15_xai_evidence_pack" in proc.stdout
    assert "fixture_ci" in proc.stdout


def test_emit_cli_default_fixture(tmp_path: Path) -> None:
    proc = subprocess.run(
        [
            sys.executable,
            "-m",
            "starlab.v15.emit_v15_xai_evidence_pack",
            "--output-dir",
            str(tmp_path),
        ],
        check=False,
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0
    data = json.loads((tmp_path / FILENAME_XAI_EVIDENCE).read_text(encoding="utf-8"))
    assert data["profile"] == PROFILE_FIXTURE_CI


def test_operator_evidence_unknown_key(tmp_path: Path) -> None:
    p = tmp_path / "evidence.json"
    p.write_text(json.dumps({**_complete_evidence_dict(), "extra_key": 1}), encoding="utf-8")
    with pytest.raises(ValueError, match="unknown top-level"):
        parse_evidence_json(p)


def test_operator_partial_incomplete(tmp_path: Path) -> None:
    p = tmp_path / "evidence.json"
    p.write_text(
        json.dumps(
            {
                "profile": "operator_declared",
                "replay_identity": _replay(),
                "checkpoint_identity": _checkpoint(),
                "decision_trace": [],
                "critical_decision_index": _cdi(),
                "attribution_summary": _attr(),
                "concept_activation_summary": _conc(),
                "counterfactual_probe_results": _cf(),
                "alternative_action_rankings": _alt(),
                "uncertainty_report": _unc(),
                "replay_overlay_manifest": _ovl(),
                "xai_explanation_report": _xrep(),
            }
        ),
        encoding="utf-8",
    )
    emit_v15_xai_evidence_pack(
        tmp_path,
        profile=PROFILE_OPERATOR_DECLARED,
        evidence_path=p,
        environment_lock_path=None,
        checkpoint_lineage_path=None,
    )
    d = json.loads((tmp_path / FILENAME_XAI_EVIDENCE).read_text(encoding="utf-8"))
    assert d["xai_evidence_status"] == "operator_declared_incomplete"
    assert d["long_gpu_run_authorized"] is False


def test_operator_complete_without_long_run_or_faithfulness(tmp_path: Path) -> None:
    p = tmp_path / "evidence.json"
    p.write_text(json.dumps(_complete_evidence_dict()), encoding="utf-8")
    emit_v15_xai_evidence_pack(
        tmp_path,
        profile=PROFILE_OPERATOR_DECLARED,
        evidence_path=p,
        environment_lock_path=None,
        checkpoint_lineage_path=None,
    )
    d = json.loads((tmp_path / FILENAME_XAI_EVIDENCE).read_text(encoding="utf-8"))
    assert d["xai_evidence_status"] == "operator_declared_complete"
    assert d["long_gpu_run_authorized"] is False
    assert d["real_xai_inference_executed"] is False
    assert d["explanation_faithfulness_validated"] is False


def test_operator_declares_inference_and_faithfulness_flags(tmp_path: Path) -> None:
    p = tmp_path / "evidence.json"
    ed = _complete_evidence_dict()
    ed["real_xai_inference_executed"] = True
    ed["explanation_faithfulness_validated"] = True
    p.write_text(json.dumps(ed), encoding="utf-8")
    emit_v15_xai_evidence_pack(
        tmp_path,
        profile=PROFILE_OPERATOR_DECLARED,
        evidence_path=p,
        environment_lock_path=None,
        checkpoint_lineage_path=None,
    )
    d = json.loads((tmp_path / FILENAME_XAI_EVIDENCE).read_text(encoding="utf-8"))
    assert d["real_xai_inference_executed"] is True
    assert d["explanation_faithfulness_validated"] is True
    assert d["long_gpu_run_authorized"] is False


def test_operator_evidence_redacts_paths(tmp_path: Path) -> None:
    r = _replay()
    r["notes"] = "see C:\\secret\\x\\y for details"
    p = tmp_path / "evidence.json"
    p.write_text(
        json.dumps(
            {
                **_complete_evidence_dict(),
                "replay_identity": r,
            }
        ),
        encoding="utf-8",
    )
    emit_v15_xai_evidence_pack(
        tmp_path,
        profile=PROFILE_OPERATOR_DECLARED,
        evidence_path=p,
        environment_lock_path=None,
        checkpoint_lineage_path=None,
    )
    out = (tmp_path / FILENAME_XAI_EVIDENCE).read_text(encoding="utf-8")
    assert "REDACTED_ABSOLUTE_PATH" in out


def test_xai_evidence_register_no_real_rows() -> None:
    text = (REPO_ROOT / "docs" / "xai_evidence_register.md").read_text(encoding="utf-8")
    assert "*No rows.*" in text


def test_starlab_ledger_m04_pointer() -> None:
    text = (REPO_ROOT / "docs" / "starlab.md").read_text(encoding="utf-8")
    assert "docs/starlab-v1.5.md" in text
    assert "v15_xai_evidence_contract_v1.md" in text
