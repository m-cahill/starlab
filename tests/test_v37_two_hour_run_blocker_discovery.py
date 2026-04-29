"""V15-M37 two-hour run blocker discovery tests."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from starlab.runs.json_util import canonical_json_dumps
from starlab.v15.emit_v15_m37_two_hour_run_blocker_discovery import (
    main as emit_m37_main,
)
from starlab.v15.full_30min_sc2_backed_t1_run_io import seal_m29_body
from starlab.v15.full_30min_sc2_backed_t1_run_models import CONTRACT_ID as CONTRACT_ID_M29_FULL_RUN
from starlab.v15.m37_two_hour_run_blocker_discovery_io import (
    emit_m37_fixture,
    emit_m37_operator_audit,
    extrapolate_checkpoint_storage_risk,
    sha256_file_hex,
)
from starlab.v15.m37_two_hour_run_blocker_discovery_models import (
    CONTRACT_ID_M37_DISCOVERY,
    EXPECTED_PUBLIC_CANDIDATE_SHA256,
    PROFILE_M37_OPERATOR_READINESS,
    STATUS_COMPLETED_READY_M38,
    STATUS_FIXTURE_SCHEMA_ONLY,
)

from tests.test_v35_candidate_checkpoint_smoke_benchmark_readiness import (
    _sealed_m33_cuda_completed,
    _write_m33,
)

REPO_ROOT = Path(__file__).resolve().parents[1]


def _write_minimal_sealed_m29(tmp_path: Path, *, cand_sha: str) -> Path:
    from starlab.v15.m37_two_hour_run_blocker_discovery_models import (
        ANCHOR_UPSTREAM_M27_ARTIFACT_SHA256,
    )

    body_pre = {
        "contract_id": CONTRACT_ID_M29_FULL_RUN,
        "milestone": "V15-M29",
        "upstream_m27_artifact_sha256": ANCHOR_UPSTREAM_M27_ARTIFACT_SHA256,
        "candidate_checkpoint_sha256_operator_local": cand_sha,
        "upstream_m28_candidate_checkpoint_sha256_reference": cand_sha,
        "observed_wall_clock_seconds": 1800.0,
        "checkpoint_count": 49537,
        "training_update_count": 2476886,
    }
    sealed = seal_m29_body(body_pre)
    p = tmp_path / "m29_full.json"
    p.write_text(canonical_json_dumps(sealed), encoding="utf-8")
    return p


@pytest.fixture
def sealed_m35_ready_with_chain(tmp_path: Path) -> tuple[Path, Path, Path]:
    m33_path = _write_m33(tmp_path, _sealed_m33_cuda_completed())
    out35 = tmp_path / "m35_out"
    from starlab.v15.m35_candidate_checkpoint_smoke_benchmark_readiness_io import (
        emit_m35_readiness_operator_preflight,
    )

    emit_m35_readiness_operator_preflight(
        out35,
        m33_path=m33_path,
        expected_candidate_sha256=None,
        m05_path=None,
    )
    m35 = out35 / "v15_candidate_checkpoint_smoke_benchmark_readiness.json"
    assert m35.is_file()
    m29 = _write_minimal_sealed_m29(tmp_path, cand_sha=EXPECTED_PUBLIC_CANDIDATE_SHA256)
    return m29, m33_path, m35


def test_m37_fixture_emits_all_artifacts(tmp_path: Path) -> None:
    sealed, *paths = emit_m37_fixture(tmp_path / "o")
    assert len(paths) == 5
    assert sealed["audit_status"] == STATUS_FIXTURE_SCHEMA_ONLY
    names = {p.name for p in paths}
    assert "v15_two_hour_run_blocker_discovery.json" in names
    assert "v15_two_hour_run_blocker_discovery_report.json" in names
    assert "v15_two_hour_run_blocker_discovery_checklist.md" in names
    assert "v15_m38_remediation_map.md" in names
    assert "v15_m39_candidate_runbook_draft.md" in names


def test_m37_fixture_claim_flags_false(tmp_path: Path) -> None:
    sealed, *_ = emit_m37_fixture(tmp_path / "o")
    assert sealed["contract_id"] == CONTRACT_ID_M37_DISCOVERY
    assert sealed["profile_id"] == PROFILE_M37_OPERATOR_READINESS
    for _k, v in sealed["claim_flags"].items():
        assert v is False


def test_m37_fixture_cli(tmp_path: Path) -> None:
    rc = emit_m37_main(["--fixture-ci", "--output-dir", str(tmp_path / "o")])
    assert rc == 0
    js = json.loads((tmp_path / "o" / "v15_two_hour_run_blocker_discovery.json").read_text())
    assert js["audit_status"] == STATUS_FIXTURE_SCHEMA_ONLY


def test_operator_audit_clean_chain_no_sha_errors(
    sealed_m35_ready_with_chain: tuple[Path, Path, Path],
    tmp_path: Path,
) -> None:
    m29, m33, m35 = sealed_m35_ready_with_chain
    sealed, *_ = emit_m37_operator_audit(
        tmp_path / "audit_out",
        repo_root=REPO_ROOT,
        allow_operator_local_inspection=False,
        candidate_checkpoint_path=None,
        expected_candidate_sha256=EXPECTED_PUBLIC_CANDIDATE_SHA256,
        authorize_checkpoint_file_sha256=False,
        m27_rollout_json=None,
        m28_training_json=None,
        m29_full_run_json=m29,
        m34_cuda_probe_json=m33,
        m35_readiness_json=m35,
        m36_smoke_execution_json=None,
        target_wall_clock_seconds=7200.0,
        min_free_disk_gb=100.0,
    )
    assert sealed["audit_status"] == STATUS_COMPLETED_READY_M38
    ids = {b["blocker_id"] for b in sealed["blockers"]}
    assert "candidate_lineage_mismatch" not in ids
    assert "checkpoint_cadence_too_high" not in ids
    assert "m29_wrapper_name_or_contract_too_30min_specific" in ids


def test_missing_m35_path_flags_blocker(tmp_path: Path) -> None:
    m29 = _write_minimal_sealed_m29(tmp_path, cand_sha=EXPECTED_PUBLIC_CANDIDATE_SHA256)
    m33 = _write_m33(tmp_path, _sealed_m33_cuda_completed())
    sealed, *_ = emit_m37_operator_audit(
        tmp_path / "o",
        repo_root=REPO_ROOT,
        allow_operator_local_inspection=False,
        candidate_checkpoint_path=None,
        expected_candidate_sha256=EXPECTED_PUBLIC_CANDIDATE_SHA256,
        authorize_checkpoint_file_sha256=False,
        m27_rollout_json=None,
        m28_training_json=None,
        m29_full_run_json=m29,
        m34_cuda_probe_json=m33,
        m35_readiness_json=None,
        m36_smoke_execution_json=None,
        target_wall_clock_seconds=7200.0,
        min_free_disk_gb=100.0,
    )
    ids = {b["blocker_id"] for b in sealed["blockers"]}
    assert "missing_m35_readiness" in ids


def test_candidate_sha_expected_mismatch_critical(
    sealed_m35_ready_with_chain: tuple[Path, Path, Path],
    tmp_path: Path,
) -> None:
    m29, m33, m35 = sealed_m35_ready_with_chain
    sealed, *_ = emit_m37_operator_audit(
        tmp_path / "o",
        repo_root=REPO_ROOT,
        allow_operator_local_inspection=False,
        candidate_checkpoint_path=None,
        expected_candidate_sha256="f" * 64,
        authorize_checkpoint_file_sha256=False,
        m27_rollout_json=None,
        m28_training_json=None,
        m29_full_run_json=m29,
        m34_cuda_probe_json=m33,
        m35_readiness_json=m35,
        m36_smoke_execution_json=None,
        target_wall_clock_seconds=7200.0,
        min_free_disk_gb=100.0,
    )
    crit = [b for b in sealed["blockers"] if b["severity"] == "critical"]
    assert any("candidate_sha_mismatch" in str(b["blocker_id"]) for b in crit)


def test_checkpoint_file_requires_authorization(
    sealed_m35_ready_with_chain: tuple[Path, Path, Path],
    tmp_path: Path,
) -> None:
    m29, m33, m35 = sealed_m35_ready_with_chain
    ck = tmp_path / "candidate_dummy.pt"
    ck.write_bytes(b"dummy-bytes-not-real-checkpoint")
    sealed, *_ = emit_m37_operator_audit(
        tmp_path / "o",
        repo_root=REPO_ROOT,
        allow_operator_local_inspection=False,
        candidate_checkpoint_path=ck,
        expected_candidate_sha256=EXPECTED_PUBLIC_CANDIDATE_SHA256,
        authorize_checkpoint_file_sha256=False,
        m27_rollout_json=None,
        m28_training_json=None,
        m29_full_run_json=m29,
        m34_cuda_probe_json=m33,
        m35_readiness_json=m35,
        m36_smoke_execution_json=None,
        target_wall_clock_seconds=7200.0,
        min_free_disk_gb=100.0,
    )
    ids = {b["blocker_id"] for b in sealed["blockers"]}
    assert "candidate_checkpoint_not_hash_authorized" in ids


def test_checkpoint_file_hash_authorization_verifies_sha(
    sealed_m35_ready_with_chain: tuple[Path, Path, Path],
    tmp_path: Path,
) -> None:
    m29, m33, m35 = sealed_m35_ready_with_chain
    ck = tmp_path / "candidate_dummy.pt"
    ck.write_bytes(b"dummy-bytes-not-real-checkpoint")
    sealed, *_ = emit_m37_operator_audit(
        tmp_path / "o",
        repo_root=REPO_ROOT,
        allow_operator_local_inspection=False,
        candidate_checkpoint_path=ck,
        expected_candidate_sha256=EXPECTED_PUBLIC_CANDIDATE_SHA256,
        authorize_checkpoint_file_sha256=True,
        m27_rollout_json=None,
        m28_training_json=None,
        m29_full_run_json=m29,
        m34_cuda_probe_json=m33,
        m35_readiness_json=m35,
        m36_smoke_execution_json=None,
        target_wall_clock_seconds=7200.0,
        min_free_disk_gb=100.0,
    )
    ids = {b["blocker_id"] for b in sealed["blockers"]}
    assert "candidate_sha_mismatch_file_hash" in ids


def test_extrapolated_checkpoint_volume_flags_without_retention_controls(tmp_path: Path) -> None:
    fake_root = tmp_path / "r"
    (fake_root / "starlab" / "v15").mkdir(parents=True)
    (fake_root / "starlab" / "v15" / "sc2_backed_t1_training_execution.py").write_text(
        "# no retention needles\n",
        encoding="utf-8",
    )
    (fake_root / "starlab" / "v15" / "run_v15_m28_sc2_backed_t1_candidate_training.py").write_text(
        "# no retention needles\n",
        encoding="utf-8",
    )
    tel, blocker = extrapolate_checkpoint_storage_risk(
        observed_wall_clock_seconds=1800.0,
        checkpoint_count=49537.0,
        target_wall_clock_seconds=7200.0,
        cadence_source="ledger_fallback_constants",
        repo_root=fake_root,
    )
    assert blocker is not None
    assert blocker["blocker_id"] == "checkpoint_cadence_too_high"
    assert tel["estimated_checkpoints_for_target_wall_clock"] > 150000


def test_remediation_and_runbook_generated(tmp_path: Path) -> None:
    sealed, *_paths = emit_m37_fixture(tmp_path / "o")
    assert sealed["audit_status"] == STATUS_FIXTURE_SCHEMA_ONLY
    rem = (tmp_path / "o" / "v15_m38_remediation_map.md").read_text(encoding="utf-8").lower()
    rb = (tmp_path / "o" / "v15_m39_candidate_runbook_draft.md").read_text(encoding="utf-8").lower()
    assert "remediation" in rem
    assert "non-claims" in rb or "not benchmark" in rb
    chk = (
        (tmp_path / "o" / "v15_two_hour_run_blocker_discovery_checklist.md")
        .read_text(
            encoding="utf-8",
        )
        .lower()
    )
    assert "non-claims" in chk


def test_m29_seal_invalid_flags(tmp_path: Path) -> None:
    p = _write_minimal_sealed_m29(tmp_path, cand_sha=EXPECTED_PUBLIC_CANDIDATE_SHA256)
    raw = json.loads(p.read_text(encoding="utf-8"))
    raw["artifact_sha256"] = "0" * 64
    p.write_text(canonical_json_dumps(raw), encoding="utf-8")
    m33 = _write_m33(tmp_path, _sealed_m33_cuda_completed())
    out35 = tmp_path / "m35_out"
    from starlab.v15.m35_candidate_checkpoint_smoke_benchmark_readiness_io import (
        emit_m35_readiness_operator_preflight,
    )

    emit_m35_readiness_operator_preflight(
        out35,
        m33_path=m33,
        expected_candidate_sha256=None,
        m05_path=None,
    )
    m35 = out35 / "v15_candidate_checkpoint_smoke_benchmark_readiness.json"
    sealed, *_ = emit_m37_operator_audit(
        tmp_path / "o",
        repo_root=REPO_ROOT,
        allow_operator_local_inspection=False,
        candidate_checkpoint_path=None,
        expected_candidate_sha256=EXPECTED_PUBLIC_CANDIDATE_SHA256,
        authorize_checkpoint_file_sha256=False,
        m27_rollout_json=None,
        m28_training_json=None,
        m29_full_run_json=p,
        m34_cuda_probe_json=m33,
        m35_readiness_json=m35,
        m36_smoke_execution_json=None,
        target_wall_clock_seconds=7200.0,
        min_free_disk_gb=100.0,
    )
    ids = {b["blocker_id"] for b in sealed["blockers"]}
    assert "seal_mismatch_m29" in ids


def test_hardcoded_runner_detection() -> None:
    scan_path = REPO_ROOT / "starlab" / "v15" / "run_v15_m29_full_30min_sc2_backed_t1_run.py"
    txt = scan_path.read_text(encoding="utf-8")
    assert "1800.0" in txt


def test_sha256_file_hex_reads(tmp_path: Path) -> None:
    p = tmp_path / "t.bin"
    p.write_bytes(b"abc")
    h = sha256_file_hex(p)
    assert len(h) == 64
