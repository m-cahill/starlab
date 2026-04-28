"""V19 candidate checkpoint evaluation package — assembly, CLI, governance."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from starlab.runs.json_util import canonical_json_dumps, sha256_hex_of_canonical_json
from starlab.v15.candidate_checkpoint_evaluation_package_io import (
    emit_operator_declared_package,
    emit_v15_candidate_checkpoint_evaluation_package,
    seal_package_body,
)
from starlab.v15.candidate_checkpoint_evaluation_package_models import (
    CONTRACT_ID_CANDIDATE_CHECKPOINT_EVALUATION_PACKAGE,
    FILENAME_PACKAGE,
    NON_CLAIMS_V15_M19,
    PROFILE_FIXTURE_DEFAULT,
    PROFILE_OPERATOR_DECLARED,
    REASON_INVALID_M18_CONTRACT,
    REASON_NOT_EXECUTED,
    SEAL_KEY_ARTIFACT,
    PackageStatus,
)
from starlab.v15.checkpoint_evaluation_readiness_io import emit_v15_checkpoint_evaluation_readiness
from starlab.v15.checkpoint_evaluation_readiness_models import (
    CONTRACT_ID_CANDIDATE_CHECKPOINT_MANIFEST,
    CandidateReadinessStatus,
)
from starlab.v15.checkpoint_lineage_models import CONTRACT_ID_CHECKPOINT_LINEAGE
from starlab.v15.environment_lock_io import emit_long_gpu_environment_lock
from starlab.v15.environment_lock_models import FILENAME_LONG_GPU_ENV
from starlab.v15.environment_lock_models import PROFILE_FIXTURE_CI as M02_PROF
from starlab.v15.long_gpu_training_manifest_io import build_campaign_receipt_body_not_executed
from starlab.v15.long_gpu_training_manifest_models import (
    CONTRACT_ID_LONG_GPU_CAMPAIGN_RECEIPT,
    CONTRACT_VERSION,
    MILESTONE_ID_V15_M08,
    PROFILE_ID_LONG_GPU_CAMPAIGN_EXECUTION,
    default_m08_authorization_flags,
)
from starlab.v15.strong_agent_scorecard_io import emit_v15_strong_agent_scorecard
from starlab.v15.strong_agent_scorecard_models import (
    FILENAME_STRONG_AGENT_SCORECARD,
    PROTOCOL_PROFILE_ID,
)
from starlab.v15.strong_agent_scorecard_models import (
    PROFILE_FIXTURE_CI as M05_PROF,
)

REPO_ROOT = Path(__file__).resolve().parents[1]

SYNTHETIC_SHA = sha256_hex_of_canonical_json({"m19_fixture": "pytorch_candidate_v1"})


def _synthetic_completed_receipt(*, checkpoint_id: str, sha: str) -> dict[str, object]:
    auth = default_m08_authorization_flags()
    auth["long_gpu_campaign_completed"] = True
    return {
        "contract_id": CONTRACT_ID_LONG_GPU_CAMPAIGN_RECEIPT,
        "contract_version": CONTRACT_VERSION,
        "profile_id": PROFILE_ID_LONG_GPU_CAMPAIGN_EXECUTION,
        "milestone": MILESTONE_ID_V15_M08,
        "campaign_id": "m19_synthetic_campaign",
        "execution_id": "m19_exec_fixture",
        "checkpoint_count": 1,
        "checkpoint_hashes": [sha],
        "final_checkpoint_id": checkpoint_id,
        "final_checkpoint_sha256": sha,
        "campaign_completion_status": "completed",
        "authorization_flags": auth,
        "non_claims": ["m19_synthetic_fixture_only"],
    }


def _good_manifest(*, candidate_id: str, sha: str, env_sha: str, ds_sha: str) -> dict[str, object]:
    return {
        "contract_id": CONTRACT_ID_CANDIDATE_CHECKPOINT_MANIFEST,
        "candidate_id": candidate_id,
        "primary_artifact_uri_or_reference": "logical/private/m19_candidate.pt",
        "candidate_checkpoint_sha256": sha,
        "environment_manifest_sha256": env_sha,
        "dataset_manifest_sha256": ds_sha,
        "evaluation_protocol_id": PROTOCOL_PROFILE_ID,
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


def _write_json(p: Path, o: object) -> None:
    p.write_text(canonical_json_dumps(o) + "\n", encoding="utf-8", newline="\n")


def test_fixture_default_blocked(tmp_path: Path) -> None:
    sealed, _, _, chk = emit_v15_candidate_checkpoint_evaluation_package(tmp_path)
    assert sealed["package_status"] == str(
        PackageStatus.BLOCKED_MISSING_CANDIDATE_CHECKPOINT_EVIDENCE
    )
    assert sealed["profile"] == PROFILE_FIXTURE_DEFAULT
    assert not sealed["ready_for_future_checkpoint_evaluation"]
    assert sealed["input_bindings"]["m18_readiness_sha256"] is None
    assert sealed["contract_id"] == CONTRACT_ID_CANDIDATE_CHECKPOINT_EVALUATION_PACKAGE
    assert SEAL_KEY_ARTIFACT in sealed
    assert "P0" in chk.read_text(encoding="utf-8")
    rep = json.loads(
        (tmp_path / "v15_candidate_checkpoint_evaluation_package_report.json").read_text(
            encoding="utf-8"
        )
    )
    assert "missing_inputs" in rep or rep.get("missing_inputs") is not None
    assert "allowed_next_steps" in str(rep) or rep.get("allowed_next_steps") is not None


def test_emit_deterministic_two_runs(tmp_path: Path) -> None:
    a = tmp_path / "a"
    b = tmp_path / "b"
    emit_v15_candidate_checkpoint_evaluation_package(a)
    emit_v15_candidate_checkpoint_evaluation_package(b)
    sa = (a / FILENAME_PACKAGE).read_text(encoding="utf-8")
    sb = (b / FILENAME_PACKAGE).read_text(encoding="utf-8")
    assert sa == sb


def _ready_inputs(tmp_path: Path) -> dict[str, Path]:
    m02d = tmp_path / "m02"
    emit_long_gpu_environment_lock(m02d, profile=M02_PROF)
    m02_path = m02d / FILENAME_LONG_GPU_ENV
    env_obj = json.loads(m02_path.read_text(encoding="utf-8"))
    assert isinstance(env_obj, dict)
    env_sha = sha256_hex_of_canonical_json(env_obj)

    m05d = tmp_path / "m05"
    emit_v15_strong_agent_scorecard(m05d, profile=M05_PROF)
    sc_path = m05d / FILENAME_STRONG_AGENT_SCORECARD
    sc_obj = json.loads(sc_path.read_text(encoding="utf-8"))
    sc_sha = sha256_hex_of_canonical_json(sc_obj)

    ds_path = tmp_path / "dataset.json"
    _write_json(ds_path, {"schema_version": "1.0", "dataset_id": "m19_test_ds"})
    ds_file_sha = sha256_hex_of_canonical_json(json.loads(ds_path.read_text(encoding="utf-8")))

    cid = "m19_candidate_fixture"
    man = _good_manifest(candidate_id=cid, sha=SYNTHETIC_SHA, env_sha=env_sha, ds_sha=ds_file_sha)
    r = _synthetic_completed_receipt(checkpoint_id=cid, sha=SYNTHETIC_SHA)
    lin = _good_lineage(candidate_id=cid, sha=SYNTHETIC_SHA)
    man_p = tmp_path / "manifest.json"
    r_p = tmp_path / "receipt.json"
    lin_p = tmp_path / "lineage.json"
    _write_json(man_p, man)
    _write_json(r_p, r)
    _write_json(lin_p, lin)

    m18d = tmp_path / "m18o"
    emit_v15_checkpoint_evaluation_readiness(
        m18d,
        candidate_manifest=man,
        campaign_receipt=r,
        checkpoint_lineage=lin,
    )
    m18_path = m18d / "v15_checkpoint_evaluation_readiness.json"
    m18j = json.loads(m18_path.read_text(encoding="utf-8"))
    assert m18j["readiness_status"] == str(CandidateReadinessStatus.CANDIDATE_READY_FOR_EVALUATION)
    # Ensure manifest SHAs still match (same bytes as M19 will read)
    assert env_sha == sha256_hex_of_canonical_json(json.loads(m02_path.read_text(encoding="utf-8")))
    assert sc_sha == sha256_hex_of_canonical_json(json.loads(sc_path.read_text(encoding="utf-8")))
    return {
        "m18": m18_path,
        "manifest": man_p,
        "receipt": r_p,
        "lineage": lin_p,
        "env": m02_path,
        "ds": ds_path,
        "score": sc_path,
    }


def test_synthetic_package_ready_and_claims_false(tmp_path: Path) -> None:
    p = _ready_inputs(tmp_path)
    out = tmp_path / "m19o"
    sealed, _, rep_p, ch_p = emit_v15_candidate_checkpoint_evaluation_package(
        out,
        profile="operator_preflight",
        m18_path=p["m18"],
        candidate_manifest_path=p["manifest"],
        campaign_receipt_path=p["receipt"],
        checkpoint_lineage_path=p["lineage"],
        environment_manifest_path=p["env"],
        dataset_manifest_path=p["ds"],
        evaluation_protocol_path=p["score"],
    )
    assert sealed["package_status"] == str(PackageStatus.EVALUATION_PACKAGE_READY)
    assert sealed["ready_for_future_checkpoint_evaluation"] is True
    for k in (
        "strength_evaluated",
        "checkpoint_promoted",
        "benchmark_passed",
        "xai_claim_authorized",
        "human_benchmark_claim_authorized",
        "showcase_release_authorized",
        "v2_authorized",
    ):
        assert sealed[k] is False
    for nc in NON_CLAIMS_V15_M19:
        assert nc in sealed["non_claims"]
    rep = json.loads(rep_p.read_text(encoding="utf-8"))
    assert "recommended_m20_fork" in str(rep) or rep.get("allowed_next_steps")
    assert "P9" in ch_p.read_text(encoding="utf-8")


def test_m18_no_candidate_produces_missing(tmp_path: Path) -> None:
    p = _ready_inputs(tmp_path)
    m18d = tmp_path / "m18b"
    emit_v15_checkpoint_evaluation_readiness(m18d)  # default no-candidate
    m18_path = m18d / "v15_checkpoint_evaluation_readiness.json"
    out = tmp_path / "m19b"
    sealed, _, _, _ = emit_v15_candidate_checkpoint_evaluation_package(
        out,
        profile="operator_preflight",
        m18_path=m18_path,
        candidate_manifest_path=p["manifest"],
        campaign_receipt_path=p["receipt"],
        checkpoint_lineage_path=p["lineage"],
        environment_manifest_path=p["env"],
        dataset_manifest_path=p["ds"],
        evaluation_protocol_path=p["score"],
    )
    assert sealed["package_status"] == str(
        PackageStatus.BLOCKED_MISSING_CANDIDATE_CHECKPOINT_EVIDENCE
    )


def test_m18_incomplete_produces_incomplete(tmp_path: Path) -> None:
    m02d = tmp_path / "m02"
    emit_long_gpu_environment_lock(m02d, profile=M02_PROF)
    m02_path = m02d / FILENAME_LONG_GPU_ENV
    env_obj = json.loads(m02_path.read_text(encoding="utf-8"))
    assert isinstance(env_obj, dict)
    env_sha = sha256_hex_of_canonical_json(env_obj)

    m05d = tmp_path / "m05"
    emit_v15_strong_agent_scorecard(m05d, profile=M05_PROF)
    sc_path = m05d / FILENAME_STRONG_AGENT_SCORECARD
    ds_path = tmp_path / "dataset.json"
    _write_json(ds_path, {"schema_version": "1.0", "dataset_id": "m19x"})
    ds_file_sha = sha256_hex_of_canonical_json(json.loads(ds_path.read_text(encoding="utf-8")))

    cid = "c_inc"
    man = {
        "contract_id": CONTRACT_ID_CANDIDATE_CHECKPOINT_MANIFEST,
        "candidate_id": cid,
        "primary_artifact_uri_or_reference": "x.pt",
        "candidate_checkpoint_sha256": SYNTHETIC_SHA,
        "environment_manifest_sha256": env_sha,
        "dataset_manifest_sha256": ds_file_sha,
        "evaluation_protocol_id": PROTOCOL_PROFILE_ID,
    }
    m18d = tmp_path / "m18i"
    emit_v15_checkpoint_evaluation_readiness(
        m18d,
        candidate_manifest=man,
    )
    m18p = m18d / "v15_checkpoint_evaluation_readiness.json"
    _write_json(tmp_path / "m.json", man)
    _write_json(
        tmp_path / "r.json", _synthetic_completed_receipt(checkpoint_id=cid, sha=SYNTHETIC_SHA)
    )
    _write_json(tmp_path / "l.json", _good_lineage(candidate_id=cid, sha=SYNTHETIC_SHA))
    out = tmp_path / "m19i"
    sealed, _, _, _ = emit_v15_candidate_checkpoint_evaluation_package(
        out,
        profile="operator_preflight",
        m18_path=m18p,
        candidate_manifest_path=tmp_path / "m.json",
        campaign_receipt_path=tmp_path / "r.json",
        checkpoint_lineage_path=tmp_path / "l.json",
        environment_manifest_path=m02_path,
        dataset_manifest_path=ds_path,
        evaluation_protocol_path=sc_path,
    )
    assert sealed["package_status"] == str(
        PackageStatus.BLOCKED_INCOMPLETE_EVALUATION_PACKAGE_INPUTS
    )


def test_wrong_m18_contract_id(tmp_path: Path) -> None:
    p = _ready_inputs(tmp_path)
    bad = tmp_path / "m18bad.json"
    bad.write_text(
        canonical_json_dumps(
            {
                "schema_version": "1.0",
                "contract_id": "not.starlab.v15.m18",
                "readiness_status": "candidate_ready_for_evaluation",
            }
        )
        + "\n",
        encoding="utf-8",
    )
    out = tmp_path / "m19bad"
    sealed, _, _, _ = emit_v15_candidate_checkpoint_evaluation_package(
        out,
        profile="operator_preflight",
        m18_path=bad,
        candidate_manifest_path=p["manifest"],
        campaign_receipt_path=p["receipt"],
        checkpoint_lineage_path=p["lineage"],
        environment_manifest_path=p["env"],
        dataset_manifest_path=p["ds"],
        evaluation_protocol_path=p["score"],
    )
    assert sealed["package_status"] == str(PackageStatus.BLOCKED_INVALID_CANDIDATE_PACKAGE)
    assert REASON_INVALID_M18_CONTRACT in sealed.get("blocked_reasons", [])


def test_m18_joblib_manifest_invalid_package(tmp_path: Path) -> None:
    p = _ready_inputs(tmp_path)
    m18d = tmp_path / "m18j"
    m18d.mkdir(parents=True, exist_ok=True)
    job_man = {
        "contract_id": CONTRACT_ID_CANDIDATE_CHECKPOINT_MANIFEST,
        "candidate_id": "j1",
        "primary_artifact_uri_or_reference": "w.joblib",
        "candidate_checkpoint_sha256": SYNTHETIC_SHA,
        "environment_manifest_sha256": "0" * 64,
        "dataset_manifest_sha256": "0" * 64,
        "evaluation_protocol_id": PROTOCOL_PROFILE_ID,
    }
    r = _synthetic_completed_receipt(checkpoint_id="j1", sha=SYNTHETIC_SHA)
    _write_json(tmp_path / "mjob.json", job_man)
    _write_json(tmp_path / "rjob.json", r)
    _write_json(
        tmp_path / "ljob.json",
        _good_lineage(candidate_id="j1", sha=SYNTHETIC_SHA),
    )
    emit_v15_checkpoint_evaluation_readiness(
        m18d,
        candidate_manifest=job_man,
        campaign_receipt=r,
        checkpoint_lineage=_good_lineage(candidate_id="j1", sha=SYNTHETIC_SHA),
    )
    m18p = m18d / "v15_checkpoint_evaluation_readiness.json"
    out = tmp_path / "m19j"
    sealed, _, _, _ = emit_v15_candidate_checkpoint_evaluation_package(
        out,
        profile="operator_preflight",
        m18_path=m18p,
        candidate_manifest_path=tmp_path / "mjob.json",
        campaign_receipt_path=tmp_path / "rjob.json",
        checkpoint_lineage_path=tmp_path / "ljob.json",
        environment_manifest_path=p["env"],
        dataset_manifest_path=p["ds"],
        evaluation_protocol_path=p["score"],
    )
    assert sealed["package_status"] == str(PackageStatus.BLOCKED_INVALID_CANDIDATE_PACKAGE)


def test_not_executed_receipt_missing(tmp_path: Path) -> None:
    p = _ready_inputs(tmp_path)
    r = build_campaign_receipt_body_not_executed(campaign_id="n")
    _write_json(tmp_path / "rn.json", r)
    m18d = tmp_path / "m18n"
    emit_v15_checkpoint_evaluation_readiness(
        m18d,
        candidate_manifest=json.loads(p["manifest"].read_text()),
        campaign_receipt=r,
        checkpoint_lineage=json.loads(p["lineage"].read_text()),
    )
    m18p = m18d / "v15_checkpoint_evaluation_readiness.json"
    out = tmp_path / "m19n"
    sealed, _, _, _ = emit_v15_candidate_checkpoint_evaluation_package(
        out,
        profile="operator_preflight",
        m18_path=m18p,
        candidate_manifest_path=p["manifest"],
        campaign_receipt_path=tmp_path / "rn.json",
        checkpoint_lineage_path=p["lineage"],
        environment_manifest_path=p["env"],
        dataset_manifest_path=p["ds"],
        evaluation_protocol_path=p["score"],
    )
    assert sealed["package_status"] == str(
        PackageStatus.BLOCKED_MISSING_CANDIDATE_CHECKPOINT_EVIDENCE
    )
    assert REASON_NOT_EXECUTED in str(sealed.get("blocked_reasons", []))


def test_checkpoint_count_zero_missing(tmp_path: Path) -> None:
    p = _ready_inputs(tmp_path)
    r = dict(_synthetic_completed_receipt(checkpoint_id="m19_candidate_fixture", sha=SYNTHETIC_SHA))
    r["checkpoint_count"] = 0
    r["campaign_completion_status"] = "completed"
    _write_json(tmp_path / "r0.json", r)
    m18d = tmp_path / "m180"
    emit_v15_checkpoint_evaluation_readiness(
        m18d,
        candidate_manifest=json.loads(p["manifest"].read_text()),
        campaign_receipt=r,
        checkpoint_lineage=json.loads(p["lineage"].read_text()),
    )
    m18p = m18d / "v15_checkpoint_evaluation_readiness.json"
    out = tmp_path / "m190"
    sealed, _, _, _ = emit_v15_candidate_checkpoint_evaluation_package(
        out,
        profile="operator_preflight",
        m18_path=m18p,
        candidate_manifest_path=p["manifest"],
        campaign_receipt_path=tmp_path / "r0.json",
        checkpoint_lineage_path=p["lineage"],
        environment_manifest_path=p["env"],
        dataset_manifest_path=p["ds"],
        evaluation_protocol_path=p["score"],
    )
    assert sealed["package_status"] == str(
        PackageStatus.BLOCKED_MISSING_CANDIDATE_CHECKPOINT_EVIDENCE
    )


def test_hash_mismatch_lineage(tmp_path: Path) -> None:
    p = _ready_inputs(tmp_path)
    r = _synthetic_completed_receipt(checkpoint_id="m19_candidate_fixture", sha="f" * 64)
    _write_json(tmp_path / "rm.json", r)
    lin2 = _good_lineage(candidate_id="m19_candidate_fixture", sha="f" * 64)
    _write_json(tmp_path / "lm.json", lin2)
    m18d = tmp_path / "m18hm"
    emit_v15_checkpoint_evaluation_readiness(
        m18d,
        candidate_manifest=json.loads(p["manifest"].read_text()),
        campaign_receipt=r,
        checkpoint_lineage=lin2,
    )
    m18p = m18d / "v15_checkpoint_evaluation_readiness.json"
    out = tmp_path / "m19hm"
    sealed, _, _, _ = emit_v15_candidate_checkpoint_evaluation_package(
        out,
        profile="operator_preflight",
        m18_path=m18p,
        candidate_manifest_path=p["manifest"],
        campaign_receipt_path=tmp_path / "rm.json",
        checkpoint_lineage_path=tmp_path / "lm.json",
        environment_manifest_path=p["env"],
        dataset_manifest_path=p["ds"],
        evaluation_protocol_path=p["score"],
    )
    assert sealed["package_status"] == str(PackageStatus.BLOCKED_INVALID_CANDIDATE_PACKAGE)


def test_operator_declared_redacts_path_and_reseals(tmp_path: Path) -> None:
    """metadata-only: JSON in, re-seal out; no checkpoint blob I/O in this code path."""
    a = tmp_path / "fixture_out"
    _, p_pkg, _, _ = emit_v15_candidate_checkpoint_evaluation_package(a)
    raw = json.loads(p_pkg.read_text(encoding="utf-8"))
    raw["operator_path_probe"] = "C:\\Users\\x\\op\\secret_weights.pt"
    p_pkg.write_text(canonical_json_dumps(raw) + "\n", encoding="utf-8", newline="\n")
    b = tmp_path / "op_decl"
    sealed, out_pkg, _, _ = emit_operator_declared_package(b, package_json=p_pkg)
    assert sealed["profile"] == PROFILE_OPERATOR_DECLARED
    assert str(sealed.get("package_status", "")) == str(
        PackageStatus.BLOCKED_MISSING_CANDIDATE_CHECKPOINT_EVIDENCE
    )
    out_txt = out_pkg.read_text(encoding="utf-8")
    assert "<REDACTED_ABSOLUTE_PATH>" in out_txt
    for k in (
        "strength_evaluated",
        "checkpoint_promoted",
        "benchmark_passed",
        "xai_claim_authorized",
        "human_benchmark_claim_authorized",
        "showcase_release_authorized",
        "v2_authorized",
    ):
        assert sealed[k] is False


def test_m18_readiness_status_strings_documented() -> None:
    """Map prompt checklist: refusal → missing, incomplete → incomplete, invalid → invalid."""
    assert str(CandidateReadinessStatus.NO_CANDIDATE_REFUSAL) == "no_candidate_refusal"
    assert (
        str(CandidateReadinessStatus.CANDIDATE_EVIDENCE_INCOMPLETE)
        == "candidate_evidence_incomplete"
    )
    assert (
        str(CandidateReadinessStatus.INVALID_OR_UNSUPPORTED_CANDIDATE)
        == "invalid_or_unsupported_candidate"
    )


def test_seal_stable() -> None:
    body: dict[str, object] = {
        "schema_version": "1.0",
        "contract_id": CONTRACT_ID_CANDIDATE_CHECKPOINT_EVALUATION_PACKAGE,
    }
    a = seal_package_body(body)
    b = seal_package_body(body)
    assert a[SEAL_KEY_ARTIFACT] == b[SEAL_KEY_ARTIFACT]


def test_cli_default(tmp_path: Path) -> None:
    rc = subprocess.run(
        [
            sys.executable,
            "-m",
            "starlab.v15.emit_v15_candidate_checkpoint_evaluation_package",
            "--output-dir",
            str(tmp_path / "o"),
        ],
        cwd=REPO_ROOT,
        check=False,
    ).returncode
    assert rc == 0
    js = json.loads((tmp_path / "o" / FILENAME_PACKAGE).read_text(encoding="utf-8"))
    assert js["package_status"] == str(PackageStatus.BLOCKED_MISSING_CANDIDATE_CHECKPOINT_EVIDENCE)


def test_governance_docs_point_to_m19() -> None:
    v15 = (REPO_ROOT / "docs" / "starlab-v1.5.md").read_text(encoding="utf-8")
    assert "V15-M19" in v15
    assert "starlab.v15.candidate_checkpoint_evaluation_package.v1" in v15
    sm = (REPO_ROOT / "docs" / "starlab.md").read_text(encoding="utf-8")
    assert "docs/starlab-v1.5.md" in sm
    assert "V15-M19" in sm
    assert "v15_candidate_checkpoint_evaluation_package_v1.md" in sm


def test_starlab_md_v15_arc_pointer_current_milestone_id_once() -> None:
    """The compact v1.5 arc pointer line carries exactly one active-milestone ID (now V15-M20)."""
    lines = (REPO_ROOT / "docs" / "starlab.md").read_text(encoding="utf-8").splitlines()
    v15_lines = [ln for ln in lines if "docs/starlab-v1.5.md" in ln and "v1.5 arc (V15)" in ln]
    assert len(v15_lines) == 1, "expected a single v1.5 arc pointer line"
    assert "V15-M20" in v15_lines[0]
    assert v15_lines[0].count("V15-M20") == 1
