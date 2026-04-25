"""V15-M03: checkpoint lineage manifest deterministic JSON + governance pointers."""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

import pytest
from starlab.runs.json_util import sha256_hex_of_canonical_json
from starlab.v15.checkpoint_lineage_io import (
    build_checkpoint_lineage_body,
    build_checkpoint_lineage_body_fixture,
    emit_checkpoint_lineage_manifest,
    seal_checkpoint_lineage_body,
)
from starlab.v15.checkpoint_lineage_models import (
    CONTRACT_ID_CHECKPOINT_LINEAGE,
    FILENAME_CHECKPOINT_LINEAGE,
    PROFILE_FIXTURE_CI,
    PROFILE_OPERATOR_DECLARED,
    REPORT_FILENAME_CHECKPOINT_LINEAGE,
)

REPO_ROOT = Path(__file__).resolve().parents[1]
_SEAL = "checkpoint_lineage_manifest_sha256"

REQUIRED_TOP_KEYS = (
    "contract_id",
    "milestone_id",
    "generated_by",
    "profile",
    "lineage_manifest_status",
    "long_gpu_run_authorized",
    "checkpoint_bytes_verified",
    "resume_execution_verified",
    "rollback_execution_verified",
    "evidence_scope",
    "training_run_identity",
    "environment_lock_reference",
    "dataset_reference",
    "model_config_reference",
    "checkpoint_lineage",
    "interruption_receipts",
    "resume_receipts",
    "rollback_receipts",
    "lineage_manifest_status_vocabulary",
    "checkpoint_role_vocabulary",
    "promotion_status_vocabulary",
    "hash_verification_status_vocabulary",
    "resume_verification_status_vocabulary",
    "rollback_verification_status_vocabulary",
    "receipt_status_vocabulary",
    "storage_posture_vocabulary",
    "path_disclosure_vocabulary",
    "required_fields",
    "check_results",
    "m03_verification_attestation",
    "non_claims",
    "carry_forward_items",
)


def test_checkpoint_lineage_seal_stable() -> None:
    body = build_checkpoint_lineage_body_fixture()
    sealed = seal_checkpoint_lineage_body(body)
    assert sealed[_SEAL] == sha256_hex_of_canonical_json(body)
    assert sealed["contract_id"] == CONTRACT_ID_CHECKPOINT_LINEAGE


def test_checkpoint_lineage_golden_sha256() -> None:
    body = build_checkpoint_lineage_body_fixture()
    sealed = seal_checkpoint_lineage_body(body)
    assert sealed[_SEAL] == ("c5b14ffbf257fdfad9f779ab6be90d1d039db8342e6434f6cb4a6112736420dc")


def test_emit_fixture_writes_files(tmp_path: Path) -> None:
    sealed, rep, c_path, r_path = emit_checkpoint_lineage_manifest(
        tmp_path, profile=PROFILE_FIXTURE_CI, lineage_path=None, environment_lock_path=None
    )
    assert c_path.name == FILENAME_CHECKPOINT_LINEAGE
    assert r_path.name == REPORT_FILENAME_CHECKPOINT_LINEAGE
    assert rep["checkpoint_lineage_manifest_sha256"] == sealed[_SEAL]


def test_emit_is_deterministic(tmp_path: Path, tmp_path_factory: pytest.TempPathFactory) -> None:
    a = tmp_path_factory.mktemp("a")
    b = tmp_path_factory.mktemp("b")
    emit_checkpoint_lineage_manifest(
        a, profile=PROFILE_FIXTURE_CI, lineage_path=None, environment_lock_path=None
    )
    emit_checkpoint_lineage_manifest(
        b, profile=PROFILE_FIXTURE_CI, lineage_path=None, environment_lock_path=None
    )
    t1 = (a / FILENAME_CHECKPOINT_LINEAGE).read_text(encoding="utf-8")
    t2 = (b / FILENAME_CHECKPOINT_LINEAGE).read_text(encoding="utf-8")
    assert t1 == t2


def test_fixture_posture() -> None:
    body = build_checkpoint_lineage_body(
        PROFILE_FIXTURE_CI, lineage_data=None, environment_lock_path=None
    )
    assert body["lineage_manifest_status"] == "fixture_only"
    assert body["long_gpu_run_authorized"] is False
    assert body["checkpoint_bytes_verified"] is False
    assert body["resume_execution_verified"] is False
    assert body["rollback_execution_verified"] is False
    assert body["profile"] == "fixture_ci"


def test_fixture_no_absolute_path_patterns(tmp_path: Path) -> None:
    emit_checkpoint_lineage_manifest(
        tmp_path, profile=PROFILE_FIXTURE_CI, lineage_path=None, environment_lock_path=None
    )
    text = (tmp_path / FILENAME_CHECKPOINT_LINEAGE).read_text(encoding="utf-8")
    assert not re.search(r"[A-Za-z]:\\", text)
    assert "\\\\" not in text
    assert "/home/" not in text
    assert "/Users/" not in text


def test_non_claims_present() -> None:
    body = build_checkpoint_lineage_body_fixture()
    assert "m03_executes_gpu_training" in body["non_claims"]
    assert "px2_m04_opened" in body["non_claims"]


def test_required_sections_and_vocab() -> None:
    body = build_checkpoint_lineage_body_fixture()
    for k in REQUIRED_TOP_KEYS:
        assert k in body, f"missing {k}"


def test_report_has_sha256_field(tmp_path: Path) -> None:
    _, rep, _, _ = emit_checkpoint_lineage_manifest(
        tmp_path, profile=PROFILE_FIXTURE_CI, lineage_path=None, environment_lock_path=None
    )
    assert "checkpoint_lineage_manifest_sha256" in rep
    assert rep["checkpoint_lineage_manifest_sha256"]


def test_starlab_ledger_m03_pointers() -> None:
    text = (REPO_ROOT / "docs" / "starlab.md").read_text(encoding="utf-8")
    assert "docs/starlab-v1.5.md" in text
    assert "v15_checkpoint_lineage_resume_discipline_v1.md" in text


def test_runtime_doc_v15_m03() -> None:
    doc = (
        REPO_ROOT / "docs" / "runtime" / "v15_checkpoint_lineage_resume_discipline_v1.md"
    ).read_text(encoding="utf-8")
    assert "starlab.v15.checkpoint_lineage_manifest.v1" in doc
    v15 = (REPO_ROOT / "docs" / "starlab-v1.5.md").read_text(encoding="utf-8")
    assert "V15-M03" in v15
    assert "starlab.v15.checkpoint_lineage_manifest.v1" in v15
    assert "python -m starlab.v15.emit_v15_checkpoint_lineage_manifest" in v15
    assert "**M03 non-claims" in v15


def test_emit_cli_help() -> None:
    proc = subprocess.run(
        [sys.executable, "-m", "starlab.v15.emit_v15_checkpoint_lineage_manifest", "--help"],
        check=False,
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0
    assert "v15_checkpoint_lineage_manifest" in proc.stdout
    assert "fixture_ci" in proc.stdout


def test_emit_cli_default_fixture(tmp_path: Path) -> None:
    proc = subprocess.run(
        [
            sys.executable,
            "-m",
            "starlab.v15.emit_v15_checkpoint_lineage_manifest",
            "--output-dir",
            str(tmp_path),
        ],
        check=False,
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0
    data = json.loads((tmp_path / FILENAME_CHECKPOINT_LINEAGE).read_text(encoding="utf-8"))
    assert data["profile"] == PROFILE_FIXTURE_CI


def _full_checkpoint_row(
    checkpoint_id: str, parent: str | None, note: str = "ok"
) -> dict[str, object]:
    z = "0" * 64
    return {
        "checkpoint_id": checkpoint_id,
        "checkpoint_role": "candidate",
        "checkpoint_storage_posture": "local_out",
        "checkpoint_path_disclosure": "redacted",
        "checkpoint_uri_or_reference": f"logical:checkpoint/{checkpoint_id}",
        "checkpoint_sha256": z,
        "hash_verification_status": "declared_only",
        "parent_checkpoint_id": parent,
        "training_run_id": "op-run-1",
        "environment_lock_sha256": z,
        "dataset_manifest_sha256": z,
        "model_config_sha256": z,
        "step": 0,
        "episode": 0,
        "wall_clock_elapsed": "PT0S",
        "promotion_status": "candidate",
        "created_by_event": "operator",
        "non_claims": [note],
    }


def _intr() -> list[dict[str, object]]:
    return [
        {
            "interruption_id": "i1",
            "training_run_id": "op-run-1",
            "checkpoint_id": "a",
            "reason": "test",
            "interruption_step": 0,
            "interruption_episode": 0,
            "operator_declared_at": "2026-01-01T00:00:00Z",
            "receipt_status": "declared_only",
            "notes": "n",
        }
    ]


def _res() -> list[dict[str, object]]:
    return [
        {
            "resume_id": "r1",
            "training_run_id": "op-run-1",
            "from_checkpoint_id": "a",
            "resume_step": 0,
            "resume_episode": 0,
            "resume_policy": "from_checkpoint",
            "resume_verification_status": "not_executed",
            "notes": "n",
        }
    ]


def _roll() -> list[dict[str, object]]:
    return [
        {
            "rollback_id": "rb1",
            "training_run_id": "op-run-1",
            "from_checkpoint_id": "b",
            "to_checkpoint_id": "a",
            "rollback_reason": "regression",
            "rollback_policy": "manual",
            "rollback_verification_status": "not_executed",
            "notes": "n",
        }
    ]


def test_operator_lineage_json_redacts_paths(tmp_path: Path) -> None:
    a = _full_checkpoint_row("a", None)
    a["non_claims"] = ["x"]
    a["checkpoint_uri_or_reference"] = "C:\\\\Data\\\\weights\\\\ckpt"
    p = tmp_path / "lineage.json"
    p.write_text(
        json.dumps(
            {
                "profile": "operator_declared",
                "training_run_id": "op-run-1",
                "environment_lock_reference": {"k": 1},
                "dataset_reference": None,
                "model_config_reference": None,
                "checkpoints": [a, _full_checkpoint_row("b", "a")],
                "interruption_receipts": _intr(),
                "resume_receipts": _res(),
                "rollback_receipts": _roll(),
                "operator_notes": "see C:\\\\secret\\\\path",
            }
        ),
        encoding="utf-8",
    )
    emit_checkpoint_lineage_manifest(
        tmp_path,
        profile=PROFILE_OPERATOR_DECLARED,
        lineage_path=p,
        environment_lock_path=None,
    )
    out = (tmp_path / FILENAME_CHECKPOINT_LINEAGE).read_text(encoding="utf-8")
    assert "C:\\" not in out or "REDACTED" in out
    assert "REDACTED_ABSOLUTE_PATH" in out


def test_operator_partial_incomplete(tmp_path: Path) -> None:
    p = tmp_path / "lineage.json"
    p.write_text(
        json.dumps(
            {
                "profile": "operator_declared",
                "training_run_id": "x",
                "checkpoints": [],
            }
        ),
        encoding="utf-8",
    )
    emit_checkpoint_lineage_manifest(
        tmp_path, profile=PROFILE_OPERATOR_DECLARED, lineage_path=p, environment_lock_path=None
    )
    d = json.loads((tmp_path / FILENAME_CHECKPOINT_LINEAGE).read_text(encoding="utf-8"))
    assert d["lineage_manifest_status"] == "operator_declared_incomplete"


def test_operator_complete_verified_bytes_and_no_long_run_auth(tmp_path: Path) -> None:
    cpa = {**_full_checkpoint_row("a", None), "hash_verification_status": "verified_external"}
    cpb = {**_full_checkpoint_row("b", "a"), "hash_verification_status": "verified_external"}
    p = tmp_path / "lineage.json"
    p.write_text(
        json.dumps(
            {
                "profile": "operator_declared",
                "training_run_id": "op-run-1",
                "checkpoints": [cpa, cpb],
                "interruption_receipts": _intr(),
                "resume_receipts": _res(),
                "rollback_receipts": _roll(),
            }
        ),
        encoding="utf-8",
    )
    emit_checkpoint_lineage_manifest(
        tmp_path, profile=PROFILE_OPERATOR_DECLARED, lineage_path=p, environment_lock_path=None
    )
    d = json.loads((tmp_path / FILENAME_CHECKPOINT_LINEAGE).read_text(encoding="utf-8"))
    assert d["lineage_manifest_status"] == "operator_declared_complete"
    assert d["checkpoint_bytes_verified"] is True
    assert d["long_gpu_run_authorized"] is False
    assert d["resume_execution_verified"] is False
    assert d["rollback_execution_verified"] is False


def test_receipts_do_not_imply_execution_by_default(tmp_path: Path) -> None:
    a = {
        **_full_checkpoint_row("a", None),
        "hash_verification_status": "verified_external",
    }
    b = {
        **_full_checkpoint_row("b", "a"),
        "hash_verification_status": "verified_external",
    }
    p = tmp_path / "lineage.json"
    p.write_text(
        json.dumps(
            {
                "profile": "operator_declared",
                "training_run_id": "op-run-1",
                "checkpoints": [a, b],
                "interruption_receipts": _intr(),
                "resume_receipts": [
                    {
                        "resume_id": "r1",
                        "training_run_id": "op-run-1",
                        "from_checkpoint_id": "b",
                        "resume_step": 1,
                        "resume_episode": 0,
                        "resume_policy": "p",
                        "resume_verification_status": "verified_external",
                        "notes": "external says ok",
                    }
                ],
                "rollback_receipts": _roll(),
            }
        ),
        encoding="utf-8",
    )
    emit_checkpoint_lineage_manifest(
        tmp_path, profile=PROFILE_OPERATOR_DECLARED, lineage_path=p, environment_lock_path=None
    )
    d = json.loads((tmp_path / FILENAME_CHECKPOINT_LINEAGE).read_text(encoding="utf-8"))
    assert d["resume_execution_verified"] is False
    assert d["rollback_execution_verified"] is False


def test_environment_lock_json_binds_hash(tmp_path: Path) -> None:
    m02 = {
        "contract_id": "starlab.v15.long_gpu_environment_lock.v1",
        "milestone_id": "V15-M02",
        "profile": "fixture_ci",
        "long_gpu_environment_lock_sha256": "abc",
    }
    m02p = tmp_path / "m02.json"
    m02p.write_text(json.dumps(m02, sort_keys=True), encoding="utf-8")
    exp = sha256_hex_of_canonical_json(json.loads(m02p.read_text(encoding="utf-8")))
    a = _full_checkpoint_row("a", None)
    b = _full_checkpoint_row("b", "a")
    p = tmp_path / "lineage.json"
    p.write_text(
        json.dumps(
            {
                "profile": "operator_declared",
                "training_run_id": "op-run-1",
                "checkpoints": [a, b],
                "interruption_receipts": _intr(),
                "resume_receipts": _res(),
                "rollback_receipts": _roll(),
            }
        ),
        encoding="utf-8",
    )
    outd = tmp_path / "out"
    outd.mkdir()
    emit_checkpoint_lineage_manifest(
        outd,
        profile=PROFILE_OPERATOR_DECLARED,
        lineage_path=p,
        environment_lock_path=m02p,
    )
    d = json.loads((outd / FILENAME_CHECKPOINT_LINEAGE).read_text(encoding="utf-8"))
    assert d["checkpoint_lineage"][0]["environment_lock_sha256"] == exp
    assert d["environment_lock_reference"]["environment_lock_json_canonical_sha256"] == exp
