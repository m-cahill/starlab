"""M61: SC2 foundation release lock proof pack + audit (deterministic, fixture-backed)."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from starlab.release_lock.release_lock_models import (
    AUDIT_FILENAME,
    AUDIT_REPORT_FILENAME,
    PROOF_PACK_FILENAME,
    PROOF_PACK_REPORT_FILENAME,
    RELEASE_SCOPE_NOT_EVALUABLE,
    RELEASE_SCOPE_NOT_READY,
    RELEASE_SCOPE_READY,
)
from starlab.release_lock.sc2_foundation_proof_pack import (
    build_sc2_foundation_v1_proof_pack,
    validate_and_normalize_input,
    write_sc2_foundation_v1_proof_pack_artifacts,
)
from starlab.release_lock.sc2_foundation_release_lock_audit import (
    build_sc2_foundation_release_lock_audit_bundle,
)
from starlab.runs.json_util import canonical_json_dumps, sha256_hex_of_canonical_json

REPO_ROOT = Path(__file__).resolve().parents[1]
FIX = REPO_ROOT / "tests" / "fixtures" / "m61"


def test_m61_proof_pack_deterministic_fixture(tmp_path: Path) -> None:
    inp = json.loads((FIX / "proof_pack_input.json").read_text(encoding="utf-8"))
    a, _ = build_sc2_foundation_v1_proof_pack(input_data=inp, base_dir=FIX)
    b, _ = build_sc2_foundation_v1_proof_pack(input_data=inp, base_dir=FIX)
    assert a == b
    h1 = sha256_hex_of_canonical_json({k: v for k, v in a.items() if k != "proof_pack_sha256"})
    assert a["proof_pack_sha256"] == h1


def test_m61_proof_pack_emit_cli_writes_files(tmp_path: Path) -> None:
    p1, p2 = write_sc2_foundation_v1_proof_pack_artifacts(
        input_path=FIX / "proof_pack_input.json",
        output_dir=tmp_path,
        base_dir=FIX,
    )
    assert p1.name == PROOF_PACK_FILENAME
    assert p2.name == PROOF_PACK_REPORT_FILENAME
    assert json.loads(p1.read_text(encoding="utf-8"))["contract_id"]


def test_m61_audit_ready_within_scope_fixture_ok(tmp_path: Path) -> None:
    write_sc2_foundation_v1_proof_pack_artifacts(
        input_path=FIX / "proof_pack_input.json",
        output_dir=tmp_path,
        base_dir=FIX,
    )
    pack = json.loads((tmp_path / PROOF_PACK_FILENAME).read_text(encoding="utf-8"))
    audit, report = build_sc2_foundation_release_lock_audit_bundle(pack)
    assert audit["release_scope_status"] == RELEASE_SCOPE_READY
    assert report["release_scope_status"] == RELEASE_SCOPE_READY


def test_m61_audit_not_ready_when_campaign_incomplete(tmp_path: Path) -> None:
    write_sc2_foundation_v1_proof_pack_artifacts(
        input_path=FIX / "proof_pack_input_missing_campaign.json",
        output_dir=tmp_path,
        base_dir=FIX,
    )
    pack = json.loads((tmp_path / PROOF_PACK_FILENAME).read_text(encoding="utf-8"))
    audit, report = build_sc2_foundation_release_lock_audit_bundle(pack)
    assert audit["release_scope_status"] == RELEASE_SCOPE_NOT_READY
    assert report["release_scope_status"] == RELEASE_SCOPE_NOT_READY
    assert audit["campaign_evidence_status"] == "incomplete_or_blocked"


def test_m61_validate_input_rejects_non_full_run_threshold() -> None:
    raw = json.loads((FIX / "proof_pack_input.json").read_text(encoding="utf-8"))
    raw["campaign_threshold_declaration"]["campaign_length_class"] = "shakedown"
    with pytest.raises(ValueError, match="operator_declared_full_run"):
        validate_and_normalize_input(raw)


def test_m61_audit_not_evaluable_on_bad_sha(tmp_path: Path) -> None:
    write_sc2_foundation_v1_proof_pack_artifacts(
        input_path=FIX / "proof_pack_input.json",
        output_dir=tmp_path,
        base_dir=FIX,
    )
    p = tmp_path / PROOF_PACK_FILENAME
    obj = json.loads(p.read_text(encoding="utf-8"))
    obj["proof_pack_sha256"] = "0" * 64
    p.write_text(canonical_json_dumps(obj), encoding="utf-8")
    pack = json.loads(p.read_text(encoding="utf-8"))
    audit, _ = build_sc2_foundation_release_lock_audit_bundle(pack)
    assert audit["release_scope_status"] == RELEASE_SCOPE_NOT_EVALUABLE


def test_m61_emit_audit_cli_writes(tmp_path: Path) -> None:
    from starlab.release_lock.sc2_foundation_release_lock_audit import (
        write_sc2_foundation_release_lock_audit_artifacts,
    )

    write_sc2_foundation_v1_proof_pack_artifacts(
        input_path=FIX / "proof_pack_input.json",
        output_dir=tmp_path / "p",
        base_dir=FIX,
    )
    a, r = write_sc2_foundation_release_lock_audit_artifacts(
        proof_pack_path=tmp_path / "p" / PROOF_PACK_FILENAME,
        output_dir=tmp_path / "a",
    )
    assert a.name == AUDIT_FILENAME
    assert r.name == AUDIT_REPORT_FILENAME
