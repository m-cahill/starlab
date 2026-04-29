"""V15-M36 smoke benchmark execution surface tests."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from starlab.runs.json_util import canonical_json_dumps, sha256_hex_of_canonical_json
from starlab.v15.emit_v15_m36_smoke_benchmark_execution import (
    main as emit_m36_main,
)
from starlab.v15.m35_candidate_checkpoint_smoke_benchmark_readiness_io import (
    emit_m35_readiness_operator_preflight,
    seal_m35_body,
)
from starlab.v15.m35_candidate_checkpoint_smoke_benchmark_readiness_models import (
    EXPECTED_PUBLIC_CANDIDATE_SHA256,
    STATUS_FIXTURE_ONLY,
    STATUS_READY,
)
from starlab.v15.m36_smoke_benchmark_execution_io import (
    emit_m36_bounded_synthetic_smoke,
    emit_m36_fixture,
    emit_m36_operator_preflight,
)
from starlab.v15.m36_smoke_benchmark_execution_models import (
    CONTRACT_ID_M36_EXECUTION,
    PROFILE_M36_SURFACE,
    STATUS_BLOCKED_INVALID_M35,
    STATUS_BLOCKED_MISSING_M35,
    STATUS_BLOCKED_NOT_READY,
    STATUS_BLOCKED_SHA_MISMATCH,
    STATUS_COMPLETED_SYNTHETIC,
    STATUS_READY_BUT_NOT_RUN,
)
from starlab.v15.m36_smoke_benchmark_execution_models import (
    STATUS_FIXTURE_ONLY as M36_STATUS_FIXTURE,
)

from tests.test_v35_candidate_checkpoint_smoke_benchmark_readiness import (
    _sealed_m33_cuda_completed,
)


def _write_m33(tmp_path: Path, m33: dict[str, object]) -> Path:
    p = tmp_path / "m33.json"
    p.write_text(canonical_json_dumps(m33), encoding="utf-8")
    return p


@pytest.fixture
def sealed_m35_ready_path(tmp_path: Path) -> Path:
    """Sealed M35 with smoke_benchmark_ready_for_future_execution."""
    m33 = _sealed_m33_cuda_completed()
    out = tmp_path / "m35_out"
    emit_m35_readiness_operator_preflight(
        out,
        m33_path=_write_m33(tmp_path, m33),
        expected_candidate_sha256=None,
        m05_path=None,
    )
    p = out / "v15_candidate_checkpoint_smoke_benchmark_readiness.json"
    assert p.is_file()
    js = json.loads(p.read_text(encoding="utf-8"))
    assert js["readiness_status"] == STATUS_READY
    return p


def test_m36_fixture_emits_three_artifacts(tmp_path: Path) -> None:
    sealed, p_main, p_rep, p_chk = emit_m36_fixture(tmp_path / "o")
    assert sealed["execution_status"] == M36_STATUS_FIXTURE
    assert p_main.is_file() and p_rep.is_file() and p_chk.is_file()
    nc_list = sealed.get("non_claims") or []
    assert isinstance(nc_list, list) and len(nc_list) >= 5
    js = json.loads(p_main.read_text(encoding="utf-8"))
    assert js["contract_id"] == CONTRACT_ID_M36_EXECUTION
    assert js["profile_id"] == PROFILE_M36_SURFACE


def test_m36_fixture_cli(tmp_path: Path) -> None:
    rc = emit_m36_main(
        ["--fixture-ci", "--output-dir", str(tmp_path / "o")],
    )
    assert rc == 0
    js = json.loads((tmp_path / "o" / "v15_smoke_benchmark_execution.json").read_text())
    assert js["execution_status"] == M36_STATUS_FIXTURE


def test_m36_fixture_claim_flags_false(tmp_path: Path) -> None:
    sealed, *_ = emit_m36_fixture(tmp_path / "o")
    for _k, v in sealed["claim_flags"].items():
        assert v is False
    assert sealed["claim_flags"]["benchmark_execution_performed"] is False
    assert sealed["smoke_execution"]["smoke_execution_performed"] is False


def test_operator_preflight_success(sealed_m35_ready_path: Path, tmp_path: Path) -> None:
    sealed, *_ = emit_m36_operator_preflight(
        tmp_path / "out",
        m35_path=sealed_m35_ready_path,
        expected_candidate_sha256=None,
    )
    assert sealed["execution_status"] == STATUS_READY_BUT_NOT_RUN
    assert sealed["smoke_execution"]["smoke_execution_performed"] is False


def test_operator_preflight_missing_m35(tmp_path: Path) -> None:
    sealed, *_ = emit_m36_operator_preflight(
        tmp_path / "out",
        m35_path=None,
        expected_candidate_sha256=EXPECTED_PUBLIC_CANDIDATE_SHA256,
    )
    assert sealed["execution_status"] == STATUS_BLOCKED_MISSING_M35


def test_operator_preflight_invalid_contract(
    sealed_m35_ready_path: Path,
    tmp_path: Path,
) -> None:
    raw = json.loads(sealed_m35_ready_path.read_text(encoding="utf-8"))
    raw["contract_id"] = "wrong.contract.id"
    bad = seal_m35_body({k: v for k, v in raw.items() if k != "artifact_sha256"})
    p = tmp_path / "bad.json"
    p.write_text(canonical_json_dumps(bad), encoding="utf-8")
    sealed, *_ = emit_m36_operator_preflight(
        tmp_path / "o",
        m35_path=p,
        expected_candidate_sha256=None,
    )
    assert sealed["execution_status"] == STATUS_BLOCKED_INVALID_M35


def test_operator_preflight_not_ready(
    sealed_m35_ready_path: Path,
    tmp_path: Path,
) -> None:
    raw = json.loads(sealed_m35_ready_path.read_text(encoding="utf-8"))
    raw["readiness_status"] = STATUS_FIXTURE_ONLY
    bad = seal_m35_body({k: v for k, v in raw.items() if k != "artifact_sha256"})
    p = tmp_path / "nr.json"
    p.write_text(canonical_json_dumps(bad), encoding="utf-8")
    sealed, *_ = emit_m36_operator_preflight(
        tmp_path / "o",
        m35_path=p,
        expected_candidate_sha256=None,
    )
    assert sealed["execution_status"] == STATUS_BLOCKED_NOT_READY


def test_operator_preflight_sha_mismatch(
    sealed_m35_ready_path: Path,
    tmp_path: Path,
) -> None:
    sealed, *_ = emit_m36_operator_preflight(
        tmp_path / "o",
        m35_path=sealed_m35_ready_path,
        expected_candidate_sha256="f" * 64,
    )
    assert sealed["execution_status"] == STATUS_BLOCKED_SHA_MISMATCH


def test_bounded_smoke_emits_completed(
    sealed_m35_ready_path: Path,
    tmp_path: Path,
) -> None:
    sealed, *_ = emit_m36_bounded_synthetic_smoke(
        tmp_path / "b",
        m35_path=sealed_m35_ready_path,
        expected_candidate_sha256=None,
        max_smoke_steps=1,
    )
    assert sealed["execution_status"] == STATUS_COMPLETED_SYNTHETIC
    assert sealed["smoke_execution"]["smoke_execution_performed"] is True
    assert sealed["claim_flags"]["benchmark_execution_performed"] is False
    assert sealed["claim_flags"]["benchmark_passed"] is False
    assert "synthetic_bounded_smoke_receipt_sha256" in sealed["smoke_execution"]


def test_bounded_smoke_cli(
    sealed_m35_ready_path: Path,
    tmp_path: Path,
) -> None:
    rc = emit_m36_main(
        [
            "--profile",
            "operator_local_bounded_smoke",
            "--allow-operator-local-execution",
            "--authorize-smoke-benchmark-execution",
            "--m35-readiness-json",
            str(sealed_m35_ready_path),
            "--output-dir",
            str(tmp_path / "out"),
        ],
    )
    assert rc == 0
    js = json.loads((tmp_path / "out" / "v15_smoke_benchmark_execution.json").read_text())
    assert js["execution_status"] == STATUS_COMPLETED_SYNTHETIC


def test_bounded_smoke_rejects_invalid_m35(
    sealed_m35_ready_path: Path,
    tmp_path: Path,
) -> None:
    raw = json.loads(sealed_m35_ready_path.read_text(encoding="utf-8"))
    raw["readiness_status"] = STATUS_FIXTURE_ONLY
    bad = seal_m35_body({k: v for k, v in raw.items() if k != "artifact_sha256"})
    p = tmp_path / "badm35.json"
    p.write_text(canonical_json_dumps(bad), encoding="utf-8")
    with pytest.raises(ValueError):
        emit_m36_bounded_synthetic_smoke(
            tmp_path / "o",
            m35_path=p,
            expected_candidate_sha256=None,
            max_smoke_steps=1,
        )


def test_checklist_non_claims(sealed_m35_ready_path: Path, tmp_path: Path) -> None:
    _, _, _, p_chk = emit_m36_operator_preflight(
        tmp_path / "out",
        m35_path=sealed_m35_ready_path,
        expected_candidate_sha256=None,
    )
    text = p_chk.read_text(encoding="utf-8").lower()
    assert "non-claims" in text
    assert "not_benchmark_pass" in text or "not benchmark" in text


def test_no_windows_path_leak_fixture(tmp_path: Path) -> None:
    _, p_main, _, _ = emit_m36_fixture(tmp_path / "o")
    low = p_main.read_text(encoding="utf-8").lower()
    assert "c:\\coding" not in low


def test_fixture_seal_deterministic_twice(tmp_path: Path) -> None:
    s1, *_ = emit_m36_fixture(tmp_path / "a")
    s2, *_ = emit_m36_fixture(tmp_path / "b")

    def strip_seal(d: dict[str, object]) -> dict[str, object]:
        return {k: v for k, v in d.items() if k != "artifact_sha256"}

    wo1 = strip_seal(s1)
    wo2 = strip_seal(s2)
    assert sha256_hex_of_canonical_json(wo1) == sha256_hex_of_canonical_json(wo2)


def test_claim_flags_always_false_across_profiles(
    sealed_m35_ready_path: Path,
    tmp_path: Path,
) -> None:
    rows: list[dict[str, object]] = []
    s0, *_ = emit_m36_fixture(tmp_path / "fx")
    rows.append(s0)
    s1, *_ = emit_m36_operator_preflight(
        tmp_path / "ms",
        m35_path=None,
        expected_candidate_sha256=None,
    )
    rows.append(s1)
    s2, *_ = emit_m36_operator_preflight(
        tmp_path / "ok",
        m35_path=sealed_m35_ready_path,
        expected_candidate_sha256=None,
    )
    rows.append(s2)
    s3, *_ = emit_m36_bounded_synthetic_smoke(
        tmp_path / "bd",
        m35_path=sealed_m35_ready_path,
        expected_candidate_sha256=None,
        max_smoke_steps=1,
    )
    rows.append(s3)

    for sealed in rows:
        claim_flags = sealed["claim_flags"]
        assert isinstance(claim_flags, dict)
        for _k, v in claim_flags.items():
            assert v is False
