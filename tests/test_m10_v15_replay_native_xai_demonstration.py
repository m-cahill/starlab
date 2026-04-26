"""V15-M10 replay-native XAI demonstration emitter (governance; no inference)."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest
from starlab.runs.json_util import sha256_hex_of_canonical_json
from starlab.v15.checkpoint_evaluation_io import (
    emit_v15_checkpoint_evaluation_fixture,
    emit_v15_checkpoint_promotion_decision,
)
from starlab.v15.long_gpu_training_manifest_io import build_campaign_receipt_body_not_executed
from starlab.v15.xai_demonstration_io import (
    build_demonstration_body_fixture,
    emit_v15_replay_native_xai_demonstration_fixture,
    emit_v15_replay_native_xai_demonstration_operator_declared,
    emit_v15_replay_native_xai_demonstration_operator_preflight,
    seal_replay_native_xai_demonstration_body,
)
from starlab.v15.xai_demonstration_models import (
    ALL_GATE_IDS,
    CONTRACT_ID_REPLAY_NATIVE_XAI_DEMONSTRATION,
    DEMONSTRATION_STATUS_BLOCKED_M08_RECEIPT,
    DEMONSTRATION_STATUS_FIXTURE_CONTRACT_ONLY,
    FILENAME_REPLAY_NATIVE_XAI_DEMONSTRATION,
    FILENAME_XAI_EXPLANATION_REPORT_MD,
    GATE_STATUS_BLOCKED,
    GATE_STATUS_NOT_APPLICABLE,
    GATE_STATUS_NOT_EVALUATED,
    GATE_STATUS_PASS,
    GATE_STATUS_WARNING,
    REPORT_FILENAME_REPLAY_NATIVE_XAI_DEMONSTRATION,
    SEAL_KEY_REPLAY_NATIVE_XAI_DEMONSTRATION,
)
from starlab.v15.xai_evidence_io import emit_v15_xai_evidence_pack
from starlab.v15.xai_evidence_models import PROFILE_FIXTURE_CI as XAI_PROFILE_FIXTURE

REPO_ROOT = Path(__file__).resolve().parents[1]

_FORBIDDEN_SUBSTR = (
    "the model is explainable",
    "the explanation is faithful",
    "the agent is strong",
    "the checkpoint is promoted",
)


def test_fixture_emits_three_files(tmp_path: Path) -> None:
    emit_v15_replay_native_xai_demonstration_fixture(tmp_path)
    assert (tmp_path / FILENAME_REPLAY_NATIVE_XAI_DEMONSTRATION).is_file()
    assert (tmp_path / REPORT_FILENAME_REPLAY_NATIVE_XAI_DEMONSTRATION).is_file()
    assert (tmp_path / FILENAME_XAI_EXPLANATION_REPORT_MD).is_file()


def test_fixture_status_honest(tmp_path: Path) -> None:
    emit_v15_replay_native_xai_demonstration_fixture(tmp_path)
    d = json.loads(
        (tmp_path / FILENAME_REPLAY_NATIVE_XAI_DEMONSTRATION).read_text(encoding="utf-8")
    )
    assert d["demonstration_status"] in (DEMONSTRATION_STATUS_FIXTURE_CONTRACT_ONLY,)
    af = d["authorization_flags"]
    assert af["real_inference_executed"] is False
    assert af["faithfulness_validated"] is False
    assert af["strong_agent_claim_authorized"] is False
    assert af["v2_authorized"] is False


def test_fixture_deterministic() -> None:
    a = build_demonstration_body_fixture()
    b = build_demonstration_body_fixture()
    assert a == b
    sa = seal_replay_native_xai_demonstration_body(a)
    sb = seal_replay_native_xai_demonstration_body(b)
    assert (
        sa[SEAL_KEY_REPLAY_NATIVE_XAI_DEMONSTRATION] == sb[SEAL_KEY_REPLAY_NATIVE_XAI_DEMONSTRATION]
    )
    base = {k: v for k, v in a.items()}
    assert sa[SEAL_KEY_REPLAY_NATIVE_XAI_DEMONSTRATION] == sha256_hex_of_canonical_json(base)


def test_all_gates_present_and_vocab(tmp_path: Path) -> None:
    emit_v15_replay_native_xai_demonstration_fixture(tmp_path)
    d = json.loads(
        (tmp_path / FILENAME_REPLAY_NATIVE_XAI_DEMONSTRATION).read_text(encoding="utf-8")
    )
    gates = d.get("demonstration_gates")
    assert isinstance(gates, list)
    ids = [g["gate_id"] for g in gates]
    assert ids == list(ALL_GATE_IDS)
    vocab = {
        GATE_STATUS_PASS,
        GATE_STATUS_WARNING,
        GATE_STATUS_BLOCKED,
        GATE_STATUS_NOT_EVALUATED,
        GATE_STATUS_NOT_APPLICABLE,
    }
    for g in gates:
        assert g["status"] in vocab


def test_scene_decision_coverage_fixture(tmp_path: Path) -> None:
    emit_v15_replay_native_xai_demonstration_fixture(tmp_path)
    d = json.loads(
        (tmp_path / FILENAME_REPLAY_NATIVE_XAI_DEMONSTRATION).read_text(encoding="utf-8")
    )
    sc = d["scene_coverage"]
    stypes = {x["scene_type"] for x in sc}
    assert "loss_or_failure_case" in stypes
    assert "counterfactual_decision" in stypes
    dcc = d["decision_class_coverage"]
    cl = {x["decision_class"] for x in dcc}
    assert "macro" in cl and "tactical" in cl and "scouting_uncertainty" in cl
    assert "counterfactual" in cl


def test_operator_declared_binds_shas_and_malformed_fails(
    tmp_path: Path,
) -> None:
    ev_dir = tmp_path / "ev"
    xai_dir = tmp_path / "xai"
    ev_dir.mkdir()
    xai_dir.mkdir()
    emit_v15_checkpoint_evaluation_fixture(ev_dir)
    ev_json = ev_dir / "v15_checkpoint_evaluation.json"
    emit_v15_checkpoint_promotion_decision(tmp_path / "pr", ev_json)
    promo = tmp_path / "pr" / "v15_checkpoint_promotion_decision.json"
    emit_v15_xai_evidence_pack(xai_dir, profile=XAI_PROFILE_FIXTURE)
    pack = xai_dir / "v15_xai_evidence_pack.json"
    m10out = tmp_path / "m10"
    emit_v15_replay_native_xai_demonstration_operator_declared(m10out, promo, pack)
    d = json.loads((m10out / FILENAME_REPLAY_NATIVE_XAI_DEMONSTRATION).read_text(encoding="utf-8"))
    b09 = d["m09_promotion_decision_binding"]
    b04 = d["m04_xai_evidence_pack_binding"]
    assert len(str(b09["promotion_decision_json_canonical_sha256"])) == 64
    assert len(str(b04["xai_evidence_pack_json_canonical_sha256"])) == 64
    bad = tmp_path / "bad_xai.json"
    bad.write_text(json.dumps({"contract_id": "wrong"}), encoding="utf-8")
    with pytest.raises(ValueError, match="M04"):
        emit_v15_replay_native_xai_demonstration_operator_declared(tmp_path / "e2", promo, bad)


def test_markdown_deterministic_and_non_claim(tmp_path: Path) -> None:
    emit_v15_replay_native_xai_demonstration_fixture(tmp_path)
    t1 = (tmp_path / FILENAME_XAI_EXPLANATION_REPORT_MD).read_text(encoding="utf-8")
    emit_v15_replay_native_xai_demonstration_fixture(tmp_path)
    t2 = (tmp_path / FILENAME_XAI_EXPLANATION_REPORT_MD).read_text(encoding="utf-8")
    assert t1 == t2
    low = t1.lower()
    assert "governed" in low
    assert "does not prove" in low or "not prove" in low
    for bad in _FORBIDDEN_SUBSTR:
        assert bad not in low


def test_fixture_path_safety(tmp_path: Path) -> None:
    emit_v15_replay_native_xai_demonstration_fixture(tmp_path)
    raw = (tmp_path / FILENAME_REPLAY_NATIVE_XAI_DEMONSTRATION).read_text(encoding="utf-8")
    assert "C:\\" not in raw
    assert "D:\\" not in raw


def test_operator_preflight_contracts(tmp_path: Path) -> None:
    promo = {
        "contract_id": "starlab.v15.checkpoint_promotion_decision.v1",
        "promotion_status": "blocked",
    }
    p_pack = {
        "contract_id": "starlab.v15.xai_evidence_pack.v1",
        "xai_evidence_status": "fixture_only",
    }
    m08 = build_campaign_receipt_body_not_executed(campaign_id="m10t")
    m03 = {
        "contract_id": "starlab.v15.checkpoint_lineage_manifest.v1",
        "contract_version": "1",
        "checkpoint_lineage": [],
    }
    m05 = {
        "contract_id": "starlab.v15.strong_agent_scorecard.v1",
        "contract_version": "1",
        "protocol_profile": {},
    }
    for name, d in [
        ("promo.json", promo),
        ("xai.json", p_pack),
        ("m08.json", m08),
        ("m03.json", m03),
        ("m05.json", m05),
    ]:
        (tmp_path / name).write_text(json.dumps(d), encoding="utf-8")
    out = tmp_path / "out"
    emit_v15_replay_native_xai_demonstration_operator_preflight(
        out,
        tmp_path / "promo.json",
        tmp_path / "xai.json",
        tmp_path / "m08.json",
        tmp_path / "m03.json",
        tmp_path / "m05.json",
    )
    d = json.loads((out / FILENAME_REPLAY_NATIVE_XAI_DEMONSTRATION).read_text(encoding="utf-8"))
    assert d["contract_id"] == CONTRACT_ID_REPLAY_NATIVE_XAI_DEMONSTRATION
    assert d["demonstration_status"] == DEMONSTRATION_STATUS_BLOCKED_M08_RECEIPT


def test_emit_cli_fixture_rc_zero(tmp_path: Path) -> None:
    out = tmp_path / "cli_out"
    proc = subprocess.run(
        [
            sys.executable,
            "-m",
            "starlab.v15.emit_v15_replay_native_xai_demonstration",
            "--output-dir",
            str(out),
        ],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
        timeout=60,
        check=False,
    )
    assert proc.returncode == 0, proc.stderr
