"""V15-M09 checkpoint evaluation + promotion decision (governance; no real checkpoint I/O)."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from starlab.runs.json_util import sha256_hex_of_canonical_json
from starlab.v15.checkpoint_evaluation_io import (
    build_checkpoint_evaluation_body_fixture,
    build_promotion_decision_from_evaluation,
    emit_v15_checkpoint_evaluation_fixture,
    emit_v15_checkpoint_evaluation_operator_declared,
    emit_v15_checkpoint_evaluation_operator_preflight,
    emit_v15_checkpoint_promotion_decision,
    seal_checkpoint_evaluation_body,
)
from starlab.v15.checkpoint_evaluation_models import (
    CONTRACT_ID_CHECKPOINT_EVALUATION,
    CONTRACT_ID_CHECKPOINT_PROMOTION_DECISION,
    EVALUATION_STATUS_BLOCKED_NO_RECEIPT,
    PLACEHOLDER_SHA256,
    PROFILE_ID_CHECKPOINT_EVALUATION_PROMOTION,
    PROMOTION_STATUS_BLOCKED,
    SEAL_KEY_CHECKPOINT_EVALUATION,
)
from starlab.v15.long_gpu_training_manifest_io import build_campaign_receipt_body_not_executed
from starlab.v15.long_gpu_training_manifest_models import (
    CONTRACT_ID_LONG_GPU_TRAINING_MANIFEST,
    MILESTONE_ID_V15_M08,
    PROFILE_ID_LONG_GPU_CAMPAIGN_EXECUTION,
)
from starlab.v15.long_gpu_training_manifest_models import (
    CONTRACT_VERSION as M08_VERSION,
)

REPO_ROOT = Path(__file__).resolve().parents[1]


def test_fixture_evaluation_deterministic() -> None:
    a = build_checkpoint_evaluation_body_fixture()
    b = build_checkpoint_evaluation_body_fixture()
    assert a == b
    sa = seal_checkpoint_evaluation_body(a)
    sb = seal_checkpoint_evaluation_body(b)
    assert sa[SEAL_KEY_CHECKPOINT_EVALUATION] == sb[SEAL_KEY_CHECKPOINT_EVALUATION]
    d = {k: v for k, v in a.items()}
    assert sa[SEAL_KEY_CHECKPOINT_EVALUATION] == sha256_hex_of_canonical_json(d)


def test_fixture_contract_ids() -> None:
    b = build_checkpoint_evaluation_body_fixture()
    assert b["contract_id"] == CONTRACT_ID_CHECKPOINT_EVALUATION
    assert b["profile_id"] == PROFILE_ID_CHECKPOINT_EVALUATION_PROMOTION
    for k, v in b["authorization_flags"].items():
        assert v is False, k


def test_promotion_from_fixture() -> None:
    s = seal_checkpoint_evaluation_body(build_checkpoint_evaluation_body_fixture())
    p = build_promotion_decision_from_evaluation(s)
    assert p["contract_id"] == CONTRACT_ID_CHECKPOINT_PROMOTION_DECISION
    assert p["profile_id"] == PROFILE_ID_CHECKPOINT_EVALUATION_PROMOTION
    assert p["promotion_status"] == PROMOTION_STATUS_BLOCKED
    assert p["authorization_flags"]["strong_agent_claim_authorized"] is False


def test_emit_promotion_artifacts(tmp_path: Path) -> None:
    emit_v15_checkpoint_evaluation_fixture(tmp_path)
    ev = tmp_path / "v15_checkpoint_evaluation.json"
    pout = tmp_path / "p"
    sealed, _, _, _, _ = emit_v15_checkpoint_promotion_decision(pout, ev)
    assert (pout / "v15_checkpoint_promotion_decision.json").is_file()
    assert str(sealed.get("contract_id", "")) == CONTRACT_ID_CHECKPOINT_PROMOTION_DECISION
    assert sealed.get("promotion_status") == PROMOTION_STATUS_BLOCKED
    raw = (pout / "v15_checkpoint_promotion_decision.json").read_text(encoding="utf-8")
    assert raw.find(PLACEHOLDER_SHA256) == -1


def test_preflight_blocks_without_m08_receipt(tmp_path: Path) -> None:
    m = {
        "contract_id": CONTRACT_ID_LONG_GPU_TRAINING_MANIFEST,
        "contract_version": M08_VERSION,
        "profile_id": PROFILE_ID_LONG_GPU_CAMPAIGN_EXECUTION,
        "milestone": MILESTONE_ID_V15_M08,
        "campaign_id": "m09_test",
    }
    mpath = tmp_path / "m.json"
    mpath.write_text(json.dumps(m), encoding="utf-8")
    rpath = tmp_path / "r.json"
    rpath.write_text(
        json.dumps(build_campaign_receipt_body_not_executed(campaign_id="x")),
        encoding="utf-8",
    )
    cand_sha = "a" * 64
    line = {
        "contract_id": "starlab.v15.checkpoint_lineage_manifest.v1",
        "contract_version": "1",
        "checkpoint_lineage": [
            {"checkpoint_id": "cand1", "parent_checkpoint_id": None},
        ],
    }
    lpath = tmp_path / "l.json"
    lpath.write_text(json.dumps(line), encoding="utf-8")
    meta = {
        "candidate_checkpoint_id": "cand1",
        "candidate_checkpoint_role": "current_candidate",
        "checkpoint_sha256": cand_sha,
    }
    cpath = tmp_path / "cand.json"
    cpath.write_text(json.dumps(meta), encoding="utf-8")
    for name, d in [
        ("el.json", {"environment_lock_status": "operator_local_ready"}),
        ("tc.json", {"training_config": True}),
        ("ds.json", {"dataset": True}),
        ("rm.json", {"rights": True}),
    ]:
        (tmp_path / name).write_text(json.dumps(d), encoding="utf-8")
    out = tmp_path / "out"
    emit_v15_checkpoint_evaluation_operator_preflight(
        out,
        m08_training_manifest=mpath,
        m08_campaign_receipt=rpath,
        checkpoint_lineage=lpath,
        candidate_checkpoint_metadata=cpath,
        environment_lock=tmp_path / "el.json",
        training_config=tmp_path / "tc.json",
        dataset_manifest=tmp_path / "ds.json",
        rights_manifest=tmp_path / "rm.json",
        strong_agent_scorecard=None,
        xai_evidence=None,
        human_panel_benchmark=None,
    )
    evj = json.loads((out / "v15_checkpoint_evaluation.json").read_text(encoding="utf-8"))
    assert evj["evaluation_status"] == EVALUATION_STATUS_BLOCKED_NO_RECEIPT
    sha = evj["m08_training_manifest_binding"]["m08_training_manifest_json_canonical_sha256"]
    assert len(sha) == 64
    t = (out / "v15_checkpoint_evaluation.json").read_text(encoding="utf-8")
    assert "C:\\" not in t
    assert "D:\\" not in t


def test_operator_declared_redacts(tmp_path: Path) -> None:
    raw = build_checkpoint_evaluation_body_fixture()
    raw["provenance_gaps"] = list(raw.get("provenance_gaps", [])) + [
        "contact: evil@b.com and D:\\p\\a",
    ]
    p = tmp_path / "e.json"
    p.write_text(json.dumps(raw), encoding="utf-8")
    o = tmp_path / "eout"
    emit_v15_checkpoint_evaluation_operator_declared(o, p)
    t = (o / "v15_checkpoint_evaluation.json").read_text(encoding="utf-8")
    assert "evil@" not in t


def test_cli_fixture_succeeds(tmp_path: Path) -> None:
    rc = subprocess.run(
        [
            sys.executable,
            "-m",
            "starlab.v15.emit_v15_checkpoint_evaluation",
            "--output-dir",
            str(tmp_path / "c"),
        ],
        cwd=REPO_ROOT,
        check=False,
    ).returncode
    assert rc == 0


def test_cli_preflight_missing_args(tmp_path: Path) -> None:
    rc = subprocess.run(
        [
            sys.executable,
            "-m",
            "starlab.v15.emit_v15_checkpoint_evaluation",
            "--profile",
            "operator_preflight",
            "--output-dir",
            str(tmp_path / "o"),
        ],
        cwd=REPO_ROOT,
        check=False,
    ).returncode
    assert rc == 2
