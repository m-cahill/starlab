"""V15-M31 candidate checkpoint evaluation harness dry-run gate tests."""

from __future__ import annotations

from pathlib import Path

from starlab.runs.json_util import canonical_json_dumps
from starlab.v15.candidate_checkpoint_evaluation_package_io import seal_package_body
from starlab.v15.emit_v15_m31_candidate_checkpoint_evaluation_harness_gate import (
    main as emit_m31_main,
)
from starlab.v15.m30_sc2_backed_candidate_checkpoint_evaluation_package_io import (
    emit_m30_sc2_backed_candidate_checkpoint_evaluation_package,
)
from starlab.v15.m30_sc2_backed_candidate_checkpoint_evaluation_package_models import (
    PACKAGE_PROFILE_ID_M30,
)
from starlab.v15.m31_candidate_checkpoint_evaluation_harness_gate_io import (
    build_fixture_m30_sealed_package,
    emit_v15_m31_candidate_checkpoint_evaluation_harness_gate,
    load_sealed_m30_package_json,
)
from starlab.v15.m31_candidate_checkpoint_evaluation_harness_gate_models import (
    CONTRACT_ID_M31_GATE,
    PROFILE_M31_DRY_RUN,
)
from starlab.v15.m31_candidate_checkpoint_evaluation_harness_gate_models import (
    STATUS_READY as GATE_READY,
)
from starlab.v15.sc2_backed_t1_candidate_training_io import seal_m28_body
from starlab.v15.strong_agent_scorecard_models import (
    CONTRACT_ID_STRONG_AGENT_SCORECARD,
    PROTOCOL_PROFILE_ID,
)

from tests.test_v30_sc2_backed_candidate_checkpoint_evaluation_package import (
    _write_aligned_fixture_chain as write_m30_chain_fixture,
)


def _reseal_mutated_package(sealed: dict[str, object], **updates: object) -> dict[str, object]:
    body = {k: v for k, v in sealed.items() if k != "artifact_sha256"}
    body.update(**updates)
    return seal_package_body(body)


def test_m31_fixture_ci_success(tmp_path: Path) -> None:
    m30 = build_fixture_m30_sealed_package()
    sealed, jp, _, _ = emit_v15_m31_candidate_checkpoint_evaluation_harness_gate(
        tmp_path / "gate",
        m30_sealed=m30,
        fixture_ci=True,
        m05_path=None,
    )
    txt = jp.read_text(encoding="utf-8").lower()
    assert "c:\\coding" not in txt
    assert "/home/" not in txt
    assert sealed["contract_id"] == CONTRACT_ID_M31_GATE
    assert sealed["profile"] == PROFILE_M31_DRY_RUN
    assert sealed["gate_status"] == GATE_READY
    assert sealed["evaluation_harness_ready"] is True
    assert sealed["blocked_reasons"] == []
    assert sealed["evaluation_execution_performed"] is False
    assert sealed["candidate_model_loaded"] is False
    assert sealed["fixture_ci"] is True


def test_m31_emit_from_m30_package_chain_success(tmp_path: Path) -> None:
    mdir = tmp_path / "m30_out"
    upstream_dir = tmp_path / "upstream"
    upstream_dir.mkdir(parents=True, exist_ok=True)
    p27, p28, p29 = write_m30_chain_fixture(upstream_dir)
    m30_sealed, _, _, _ = emit_m30_sc2_backed_candidate_checkpoint_evaluation_package(
        mdir,
        m27_path=p27,
        m28_path=p28,
        m29_path=p29,
        scorecard_path=None,
    )
    assert m30_sealed["package_profile_id"] == PACKAGE_PROFILE_ID_M30
    pkg_p = mdir / "v15_candidate_checkpoint_evaluation_package.json"
    sealed, _, _, _ = emit_v15_m31_candidate_checkpoint_evaluation_harness_gate(
        tmp_path / "g",
        m30_sealed=load_sealed_m30_package_json(pkg_p),
        fixture_ci=False,
        m05_path=None,
    )
    assert sealed["gate_status"] == GATE_READY
    assert sealed["blocked_reasons"] == []


def test_m30_package_not_ready(tmp_path: Path) -> None:
    m30_base = build_fixture_m30_sealed_package()
    bad = _reseal_mutated_package(
        m30_base,
        evaluation_package_ready=False,
        ready_for_future_checkpoint_evaluation=False,
    )
    sealed, *_ = emit_v15_m31_candidate_checkpoint_evaluation_harness_gate(
        tmp_path / "gate",
        m30_sealed=bad,
        fixture_ci=True,
        m05_path=None,
    )
    assert "blocked_m30_package_not_ready" in sealed["blocked_reasons"]
    assert sealed["evaluation_harness_ready"] is False


def test_blocked_invalid_m30_profile(tmp_path: Path) -> None:
    base = build_fixture_m30_sealed_package()
    bad = _reseal_mutated_package(base, package_profile_id=f"{PACKAGE_PROFILE_ID_M30}x")
    sealed, *_ = emit_v15_m31_candidate_checkpoint_evaluation_harness_gate(
        tmp_path / "g",
        m30_sealed=bad,
        fixture_ci=True,
        m05_path=None,
    )
    assert "blocked_invalid_m30_profile" in sealed["blocked_reasons"]


def test_blocked_claim_flags_inconsistent(tmp_path: Path) -> None:
    base = build_fixture_m30_sealed_package()
    bad = _reseal_mutated_package(base, benchmark_passed=True)
    sealed, *_ = emit_v15_m31_candidate_checkpoint_evaluation_harness_gate(
        tmp_path / "g",
        m30_sealed=bad,
        fixture_ci=True,
        m05_path=None,
    )
    assert "blocked_m30_claim_flags_inconsistent" in sealed["blocked_reasons"]


def test_blocked_candidate_not_candidate_only(tmp_path: Path) -> None:
    base = build_fixture_m30_sealed_package()
    cc = dict(base["candidate_checkpoint"])
    cc["promotion_status"] = "promoted"
    bad = _reseal_mutated_package(base, candidate_checkpoint=cc)
    sealed, *_ = emit_v15_m31_candidate_checkpoint_evaluation_harness_gate(
        tmp_path / "g",
        m30_sealed=bad,
        fixture_ci=True,
        m05_path=None,
    )
    assert "blocked_m30_candidate_checkpoint_not_candidate_only" in sealed["blocked_reasons"]


def test_optional_m05_valid(tmp_path: Path) -> None:
    sc_pre = {
        "contract_id": CONTRACT_ID_STRONG_AGENT_SCORECARD,
        "protocol_profile_id": PROTOCOL_PROFILE_ID,
    }
    sc_path = tmp_path / "m05.json"
    sc_path.write_text(canonical_json_dumps(seal_m28_body(sc_pre)), encoding="utf-8")
    base = build_fixture_m30_sealed_package()
    sealed, *_ = emit_v15_m31_candidate_checkpoint_evaluation_harness_gate(
        tmp_path / "g",
        m30_sealed=base,
        fixture_ci=True,
        m05_path=sc_path,
    )
    assert sealed["scorecard_binding_status"] == "bound_in_m31"
    assert sealed["evaluation_harness_ready"] is True
    assert sealed["blocked_reasons"] == []


def test_optional_m05_invalid_blocked(tmp_path: Path) -> None:
    sc_path = tmp_path / "bad.json"
    sc_path.write_text(
        canonical_json_dumps({"contract_id": "wrong", "protocol_profile_id": PROTOCOL_PROFILE_ID}),
        encoding="utf-8",
    )
    sealed, *_ = emit_v15_m31_candidate_checkpoint_evaluation_harness_gate(
        tmp_path / "g",
        m30_sealed=build_fixture_m30_sealed_package(),
        fixture_ci=True,
        m05_path=sc_path,
    )
    assert "blocked_invalid_scorecard_protocol_json" in sealed["blocked_reasons"]


def test_path_upstream_redacted_in_emitted_gate_json(tmp_path: Path) -> None:
    """Malicious-ish protocol string must not propagate raw path patterns."""

    body = {k: v for k, v in build_fixture_m30_sealed_package().items() if k != "artifact_sha256"}
    ep = dict(body.get("evaluation_protocol_binding") or {})
    leak = r"C:\\coding\\evil"
    ep["evaluation_protocol_contract_id"] = leak
    body["evaluation_protocol_binding"] = ep
    contaminated = seal_package_body(body)
    _, jp, _, _ = emit_v15_m31_candidate_checkpoint_evaluation_harness_gate(
        tmp_path / "g",
        m30_sealed=contaminated,
        fixture_ci=True,
        m05_path=None,
    )
    content = jp.read_text(encoding="utf-8")
    assert "redacted_path_like_upstream_value" in content
    low = content.lower()
    assert "\\coding\\" not in low.replace("\\\\", "\\") and ":\\coding" not in low


def test_fixture_ci_cli_returns_zero(tmp_path: Path) -> None:
    assert emit_m31_main(["--fixture-ci", "--output-dir", str(tmp_path / "o")]) == 0
    assert (tmp_path / "o" / "v15_candidate_checkpoint_evaluation_harness_gate.json").is_file()
