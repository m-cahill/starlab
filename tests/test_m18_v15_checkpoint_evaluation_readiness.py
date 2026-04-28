"""V15-M18 checkpoint evaluation readiness / refusal — classification, CLI, governance."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from starlab.runs.json_util import sha256_hex_of_canonical_json
from starlab.v15.checkpoint_evaluation_readiness_io import (
    emit_v15_checkpoint_evaluation_readiness,
    seal_readiness_body,
)
from starlab.v15.checkpoint_evaluation_readiness_models import (
    CONTRACT_ID_CANDIDATE_CHECKPOINT_MANIFEST,
    CONTRACT_ID_CHECKPOINT_EVALUATION_READINESS,
    EMITTER_MODULE_CHECKPOINT_EVALUATION_READINESS,
    FILENAME_CHECKPOINT_EVALUATION_READINESS,
    NON_CLAIMS_V15_M18,
    PROFILE_FIXTURE_DEFAULT,
    REFUSAL_CHECKPOINT_COUNT_ZERO,
    REFUSAL_JOBLIB_ONLY,
    REFUSAL_NO_MANIFEST,
    REFUSAL_NOT_EXECUTED,
    REFUSAL_WATCHABILITY_ONLY,
    SEAL_KEY_ARTIFACT,
    CandidateReadinessStatus,
)
from starlab.v15.checkpoint_lineage_models import CONTRACT_ID_CHECKPOINT_LINEAGE
from starlab.v15.long_gpu_training_manifest_io import build_campaign_receipt_body_not_executed
from starlab.v15.long_gpu_training_manifest_models import (
    CONTRACT_ID_LONG_GPU_CAMPAIGN_RECEIPT,
    CONTRACT_VERSION,
    MILESTONE_ID_V15_M08,
    PROFILE_ID_LONG_GPU_CAMPAIGN_EXECUTION,
    default_m08_authorization_flags,
)

REPO_ROOT = Path(__file__).resolve().parents[1]

SYNTHETIC_SHA = sha256_hex_of_canonical_json({"m18_fixture": "pytorch_candidate_v1"})
_BIND_ENV = sha256_hex_of_canonical_json({"m18_env_bind": "v1"})
_BIND_DS = sha256_hex_of_canonical_json({"m18_dataset_bind": "v1"})


def _synthetic_completed_receipt(*, checkpoint_id: str, sha: str) -> dict[str, object]:
    auth = default_m08_authorization_flags()
    auth["long_gpu_campaign_completed"] = True
    return {
        "contract_id": CONTRACT_ID_LONG_GPU_CAMPAIGN_RECEIPT,
        "contract_version": CONTRACT_VERSION,
        "profile_id": PROFILE_ID_LONG_GPU_CAMPAIGN_EXECUTION,
        "milestone": MILESTONE_ID_V15_M08,
        "campaign_id": "m18_synthetic_campaign",
        "execution_id": "m18_exec_fixture",
        "checkpoint_count": 1,
        "checkpoint_hashes": [sha],
        "final_checkpoint_id": checkpoint_id,
        "final_checkpoint_sha256": sha,
        "campaign_completion_status": "completed",
        "authorization_flags": auth,
        "non_claims": ["m18_synthetic_fixture_only"],
    }


def _good_manifest(*, candidate_id: str, sha: str) -> dict[str, object]:
    return {
        "contract_id": CONTRACT_ID_CANDIDATE_CHECKPOINT_MANIFEST,
        "candidate_id": candidate_id,
        "primary_artifact_uri_or_reference": "logical/private/m18_candidate.pt",
        "candidate_checkpoint_sha256": sha,
        "environment_manifest_sha256": _BIND_ENV,
        "dataset_manifest_sha256": _BIND_DS,
        "evaluation_protocol_id": "starlab.v15.strong_agent_benchmark_protocol.v1",
    }


def _good_lineage(*, candidate_id: str, sha: str) -> dict[str, object]:
    return {
        "contract_id": CONTRACT_ID_CHECKPOINT_LINEAGE,
        "profile": "fixture_ci",
        "checkpoints": [
            {
                "checkpoint_id": candidate_id,
                "checkpoint_sha256": sha,
                "checkpoint_role": "candidate",
            }
        ],
    }


def test_default_emit_no_candidate_refusal(tmp_path: Path) -> None:
    sealed, p, _ = emit_v15_checkpoint_evaluation_readiness(tmp_path)
    assert sealed["readiness_status"] == str(CandidateReadinessStatus.NO_CANDIDATE_REFUSAL)
    assert sealed["candidate_kind"] == "none"
    assert REFUSAL_NO_MANIFEST in sealed["refusal_reasons"]
    assert sealed["profile"] == PROFILE_FIXTURE_DEFAULT
    raw = json.loads(p.read_text(encoding="utf-8"))
    assert raw["contract_id"] == CONTRACT_ID_CHECKPOINT_EVALUATION_READINESS
    assert SEAL_KEY_ARTIFACT in raw


def test_emit_deterministic_two_runs(tmp_path: Path) -> None:
    a = tmp_path / "a"
    b = tmp_path / "b"
    emit_v15_checkpoint_evaluation_readiness(a)
    emit_v15_checkpoint_evaluation_readiness(b)
    assert (a / FILENAME_CHECKPOINT_EVALUATION_READINESS).read_text() == (
        b / FILENAME_CHECKPOINT_EVALUATION_READINESS
    ).read_text()


def test_not_executed_receipt_refuses(tmp_path: Path) -> None:
    m = _good_manifest(candidate_id="c1", sha=SYNTHETIC_SHA)
    r = build_campaign_receipt_body_not_executed(campaign_id="x")
    sealed, _, _ = emit_v15_checkpoint_evaluation_readiness(
        tmp_path, candidate_manifest=m, campaign_receipt=r
    )
    assert sealed["readiness_status"] == str(CandidateReadinessStatus.NO_CANDIDATE_REFUSAL)
    assert REFUSAL_NOT_EXECUTED in sealed["refusal_reasons"]


def test_checkpoint_count_zero_refuses(tmp_path: Path) -> None:
    m = _good_manifest(candidate_id="c1", sha=SYNTHETIC_SHA)
    r = dict(build_campaign_receipt_body_not_executed(campaign_id="y"))
    r["campaign_completion_status"] = "completed"
    r["checkpoint_count"] = 0
    af = dict(default_m08_authorization_flags())
    af["long_gpu_campaign_completed"] = True
    r["authorization_flags"] = af
    sealed, _, _ = emit_v15_checkpoint_evaluation_readiness(
        tmp_path, candidate_manifest=m, campaign_receipt=r
    )
    assert sealed["readiness_status"] == str(CandidateReadinessStatus.NO_CANDIDATE_REFUSAL)
    assert REFUSAL_CHECKPOINT_COUNT_ZERO in sealed["refusal_reasons"]


def test_joblib_only_invalid(tmp_path: Path) -> None:
    m = {
        "contract_id": CONTRACT_ID_CANDIDATE_CHECKPOINT_MANIFEST,
        "candidate_id": "h1",
        "primary_artifact_uri_or_reference": "out/harness/model.joblib",
        "candidate_checkpoint_sha256": SYNTHETIC_SHA,
        "environment_manifest_sha256": _BIND_ENV,
        "dataset_manifest_sha256": _BIND_DS,
        "evaluation_protocol_id": "starlab.v15.strong_agent_benchmark_protocol.v1",
    }
    sealed, _, _ = emit_v15_checkpoint_evaluation_readiness(tmp_path, candidate_manifest=m)
    assert sealed["readiness_status"] == str(
        CandidateReadinessStatus.INVALID_OR_UNSUPPORTED_CANDIDATE
    )
    assert REFUSAL_JOBLIB_ONLY in sealed["refusal_reasons"]


def test_watchability_only_refuses(tmp_path: Path) -> None:
    m = {
        "contract_id": CONTRACT_ID_CANDIDATE_CHECKPOINT_MANIFEST,
        "candidate_id": "w1",
        "watchability_only": True,
        "evidence_classes": ["m44_watchability"],
    }
    sealed, _, _ = emit_v15_checkpoint_evaluation_readiness(tmp_path, candidate_manifest=m)
    assert sealed["readiness_status"] == str(CandidateReadinessStatus.NO_CANDIDATE_REFUSAL)
    assert REFUSAL_WATCHABILITY_ONLY in sealed["refusal_reasons"]


def test_synthetic_ready_for_evaluation(tmp_path: Path) -> None:
    cid = "m18_candidate_fixture"
    m = _good_manifest(candidate_id=cid, sha=SYNTHETIC_SHA)
    r = _synthetic_completed_receipt(checkpoint_id=cid, sha=SYNTHETIC_SHA)
    lineage_body = _good_lineage(candidate_id=cid, sha=SYNTHETIC_SHA)
    sealed, _, rep = emit_v15_checkpoint_evaluation_readiness(
        tmp_path,
        candidate_manifest=m,
        campaign_receipt=r,
        checkpoint_lineage=lineage_body,
    )
    assert sealed["readiness_status"] == str(
        CandidateReadinessStatus.CANDIDATE_READY_FOR_EVALUATION
    )
    assert sealed["refusal_reasons"] == []
    report = json.loads(rep.read_text(encoding="utf-8"))
    assert report["ready_semantics"] is not None
    assert "future evaluation" in report["ready_semantics"].lower()
    for nc in NON_CLAIMS_V15_M18:
        assert nc in report["non_claims"]


def test_m26_t1_synthetic_cuda_lineage_deferred_ready(tmp_path: Path) -> None:
    cid = "t1_candidate_deadbeef0000"
    m = _good_manifest(candidate_id=cid, sha=SYNTHETIC_SHA)
    m["artifact_notes"] = {"trainer_surface": "t1_synthetic_cuda_mlp"}
    r = _synthetic_completed_receipt(checkpoint_id=cid, sha=SYNTHETIC_SHA)
    r["artifact_notes"] = {"tier": "T1_30_MIN"}
    lineage_mismatch = _good_lineage(
        candidate_id="legacy_only",
        sha="ab" * 32,
    )
    sealed, _, _ = emit_v15_checkpoint_evaluation_readiness(
        tmp_path,
        candidate_manifest=m,
        campaign_receipt=r,
        checkpoint_lineage=lineage_mismatch,
    )
    assert sealed["readiness_status"] == str(
        CandidateReadinessStatus.CANDIDATE_READY_FOR_EVALUATION,
    )

    body = {"schema_version": "1.0", "contract_id": CONTRACT_ID_CHECKPOINT_EVALUATION_READINESS}
    a = seal_readiness_body(body)
    b = seal_readiness_body(body)
    assert a[SEAL_KEY_ARTIFACT] == b[SEAL_KEY_ARTIFACT]


def test_cli_default(tmp_path: Path) -> None:
    rc = subprocess.run(
        [
            sys.executable,
            "-m",
            "starlab.v15.emit_v15_checkpoint_evaluation_readiness",
            "--output-dir",
            str(tmp_path / "o"),
        ],
        cwd=REPO_ROOT,
        check=False,
    ).returncode
    assert rc == 0
    js = json.loads(
        (tmp_path / "o" / FILENAME_CHECKPOINT_EVALUATION_READINESS).read_text(encoding="utf-8")
    )
    assert js["readiness_status"] == str(CandidateReadinessStatus.NO_CANDIDATE_REFUSAL)


def test_governance_docs_starlab_v15_and_ledger() -> None:
    v15 = (REPO_ROOT / "docs" / "starlab-v1.5.md").read_text(encoding="utf-8")
    assert "V15-M18" in v15
    assert CONTRACT_ID_CHECKPOINT_EVALUATION_READINESS in v15
    assert "M18 non-claims" in v15 or "non-claims" in v15
    assert "v15_checkpoint_evaluation_readiness_v1.md" in v15
    assert EMITTER_MODULE_CHECKPOINT_EVALUATION_READINESS in v15
    sm = (REPO_ROOT / "docs" / "starlab.md").read_text(encoding="utf-8")
    assert "docs/starlab-v1.5.md" in sm
    assert "V15-M18" in sm
    assert "v15_checkpoint_evaluation_readiness_v1.md" in sm
