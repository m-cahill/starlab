"""Tests for V15-M56 bounded evaluation package readout / decision."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from starlab.runs.json_util import canonical_json_dumps, sha256_hex_of_canonical_json
from starlab.v15.emit_v15_m56_bounded_evaluation_package_readout_decision import (
    main as emit_m56_main,
)
from starlab.v15.m54_twelve_hour_run_package_readiness_io import (
    build_fixture_m54_body,
    seal_m54_body,
)
from starlab.v15.m54_twelve_hour_run_package_readiness_models import (
    STATUS_READY as M54_STATUS_READY,
)
from starlab.v15.m55_bounded_evaluation_package_preflight_io import (
    OperatorDeclaredInputs,
    build_fixture_preflight,
    build_operator_declared_preflight,
    seal_m55_body,
    write_preflight_artifacts,
)
from starlab.v15.m55_bounded_evaluation_package_preflight_models import (
    CANONICAL_UPSTREAM_M54_PACKAGE_ID,
    CANONICAL_UPSTREAM_M54_PACKAGE_SHA256,
)
from starlab.v15.m55_bounded_evaluation_package_preflight_models import (
    GATE_ARTIFACT_DIGEST_FIELD as M55_DIGEST,
)
from starlab.v15.m56_bounded_evaluation_package_readout_decision_io import (
    OperatorDeclaredReadoutInputs,
    OperatorPreflightReadoutInputs,
    build_fixture_readout_decision,
    build_operator_declared_readout_decision,
    build_operator_preflight_readout_decision,
    write_readout_artifacts,
)
from starlab.v15.m56_bounded_evaluation_package_readout_decision_models import (
    CANONICAL_CANDIDATE_CHECKPOINT_SHA256,
    CANONICAL_M53_RUN_ARTIFACT_SHA256,
    CANONICAL_M54_PACKAGE_SHA256,
    DECISION_BLOCKED_CANDIDATE_MISMATCH,
    DECISION_BLOCKED_CLAIM_FLAGS,
    DECISION_BLOCKED_INVALID_M55_SEAL,
    DECISION_BLOCKED_M53_MISMATCH,
    DECISION_BLOCKED_M54_MISMATCH,
    DECISION_BLOCKED_M55_NOT_READY,
    DECISION_BLOCKED_MISSING_M55,
    DECISION_BLOCKED_PRIVATE_BOUNDARY,
    DECISION_READY,
    FILENAME_MAIN_JSON,
    FORBIDDEN_FLAG_RUN_BENCHMARK,
    ROUTE_STATUS,
)
from starlab.v15.m56a_latest_candidate_visual_watchability_confirmation_models import (
    CONTRACT_ID as CONTRACT_ID_M56A_MAIN,
)
from starlab.v15.m56a_latest_candidate_visual_watchability_confirmation_models import (
    POLICY_SCAFFOLD,
)


def _sealed_m54_for_cross_check(
    *,
    m53_artifact_sha: str,
    produced_candidate_sha: str,
) -> dict[str, Any]:
    body = build_fixture_m54_body(package_status=M54_STATUS_READY)
    mb = body["m53_binding"]
    if isinstance(mb, dict):
        mb = dict(mb)
        mb["artifact_sha256"] = m53_artifact_sha
        mb["run_status"] = "completed"
        body["m53_binding"] = mb
    ccb = body["candidate_checkpoint_binding"]
    if isinstance(ccb, dict):
        ccb = dict(ccb)
        ccb["produced_candidate_checkpoint_sha256"] = produced_candidate_sha
        body["candidate_checkpoint_binding"] = ccb
    return seal_m54_body(body)


def test_fixture_deterministic_seal_and_route(tmp_path: Path) -> None:
    sealed1, paths1 = write_readout_artifacts(
        tmp_path / "a", body_unsealed=build_fixture_readout_decision()
    )
    sealed2, _paths2 = write_readout_artifacts(
        tmp_path / "b", body_unsealed=build_fixture_readout_decision()
    )
    assert canonical_json_dumps(sealed1) == canonical_json_dumps(sealed2)
    assert sealed1["readout"]["decision_status"] == DECISION_READY
    assert sealed1["route_recommendation"]["route_status"] == ROUTE_STATUS
    for _k, v in sealed1["claim_flags"].items():
        assert v is False
    dig = sealed1[M55_DIGEST]
    base = {k: v for k, v in sealed1.items() if k != M55_DIGEST}
    assert dig == sha256_hex_of_canonical_json(base)


def test_m56_seal_roundtrip(tmp_path: Path) -> None:
    body = build_fixture_readout_decision()
    sealed, _ = write_readout_artifacts(tmp_path, body_unsealed=body)
    dig = sealed[M55_DIGEST]
    wo = {k: v for k, v in sealed.items() if k != M55_DIGEST}
    assert dig == sha256_hex_of_canonical_json(wo)


def test_operator_preflight_happy_without_m54_file(tmp_path: Path) -> None:
    m55_dir = tmp_path / "m55"
    write_preflight_artifacts(m55_dir, body_unsealed=build_fixture_preflight())
    m55_path = m55_dir / "v15_bounded_evaluation_package_preflight.json"
    body = build_operator_preflight_readout_decision(
        OperatorPreflightReadoutInputs(
            m55_preflight_json=m55_path,
            expected_m54_package_sha256=CANONICAL_M54_PACKAGE_SHA256,
            expected_m53_run_artifact_sha256=CANONICAL_M53_RUN_ARTIFACT_SHA256,
            expected_candidate_sha256=CANONICAL_CANDIDATE_CHECKPOINT_SHA256,
            m54_readiness_json=None,
            m56a_context_json=None,
        ),
    )
    assert body["readout"]["decision_status"] == DECISION_READY
    from starlab.v15.m56_bounded_evaluation_package_readout_decision_models import (
        WARNING_CROSS_CHECK_NO_M54_BODY,
    )

    assert WARNING_CROSS_CHECK_NO_M54_BODY in body["readout"]["warnings"]


def _m55_ready_for_m54_digest(tmp_path: Path, m54_package_digest: str) -> Path:
    raw = build_fixture_preflight()
    ip = dict(raw["input_package"])
    ip["declared_upstream_m54_package_sha256"] = m54_package_digest
    raw["input_package"] = ip
    ri = dict(raw["required_inputs"])
    ri["m54_package_sha256"] = m54_package_digest
    raw["required_inputs"] = ri
    d = tmp_path / "m55w"
    write_preflight_artifacts(d, body_unsealed=raw)
    return d / "v15_bounded_evaluation_package_preflight.json"


def test_operator_preflight_with_m54_file(tmp_path: Path) -> None:
    m54_sealed = _sealed_m54_for_cross_check(
        m53_artifact_sha=CANONICAL_M53_RUN_ARTIFACT_SHA256,
        produced_candidate_sha=CANONICAL_CANDIDATE_CHECKPOINT_SHA256,
    )
    m54_path = tmp_path / "mReadiness.json"
    m54_path.write_text(canonical_json_dumps(m54_sealed), encoding="utf-8")
    m55_path = _m55_ready_for_m54_digest(tmp_path, str(m54_sealed[M55_DIGEST]))
    body = build_operator_preflight_readout_decision(
        OperatorPreflightReadoutInputs(
            m55_preflight_json=m55_path,
            expected_m54_package_sha256=str(m54_sealed[M55_DIGEST]),
            expected_m53_run_artifact_sha256=CANONICAL_M53_RUN_ARTIFACT_SHA256,
            expected_candidate_sha256=CANONICAL_CANDIDATE_CHECKPOINT_SHA256,
            m54_readiness_json=m54_path,
            m56a_context_json=None,
        ),
    )
    assert body["readout"]["decision_status"] == DECISION_READY
    assert not any("cross_check" in str(w).lower() for w in body["readout"]["warnings"])


def test_operator_preflight_m53_mismatch_with_m54(tmp_path: Path) -> None:
    m54_sealed = _sealed_m54_for_cross_check(
        m53_artifact_sha="a" * 64,
        produced_candidate_sha=CANONICAL_CANDIDATE_CHECKPOINT_SHA256,
    )
    m54_path = tmp_path / "m54.json"
    m54_path.write_text(canonical_json_dumps(m54_sealed), encoding="utf-8")
    m55_path = _m55_ready_for_m54_digest(tmp_path, str(m54_sealed[M55_DIGEST]))
    body = build_operator_preflight_readout_decision(
        OperatorPreflightReadoutInputs(
            m55_preflight_json=m55_path,
            expected_m54_package_sha256=str(m54_sealed[M55_DIGEST]),
            expected_m53_run_artifact_sha256=CANONICAL_M53_RUN_ARTIFACT_SHA256,
            expected_candidate_sha256=CANONICAL_CANDIDATE_CHECKPOINT_SHA256,
            m54_readiness_json=m54_path,
            m56a_context_json=None,
        ),
    )
    assert body["readout"]["decision_status"] == DECISION_BLOCKED_M53_MISMATCH


def test_operator_preflight_m55_not_ready(tmp_path: Path) -> None:
    raw = build_fixture_preflight()
    raw["preflight_status"] = "blocked_missing_required_input"
    sealed = seal_m55_body(raw)
    p = tmp_path / "m55.json"
    p.write_text(canonical_json_dumps(sealed), encoding="utf-8")
    body = build_operator_preflight_readout_decision(
        OperatorPreflightReadoutInputs(
            m55_preflight_json=p,
            expected_m54_package_sha256=CANONICAL_M54_PACKAGE_SHA256,
            expected_m53_run_artifact_sha256=CANONICAL_M53_RUN_ARTIFACT_SHA256,
            expected_candidate_sha256=CANONICAL_CANDIDATE_CHECKPOINT_SHA256,
            m54_readiness_json=None,
            m56a_context_json=None,
        ),
    )
    assert body["readout"]["decision_status"] == DECISION_BLOCKED_M55_NOT_READY


def test_operator_preflight_m54_mismatch_from_m55(tmp_path: Path) -> None:
    raw = build_fixture_preflight()
    ip = raw.get("input_package")
    if isinstance(ip, dict):
        ip = dict(ip)
        ip["declared_upstream_m54_package_sha256"] = "f" * 64
        raw["input_package"] = ip
    sealed = seal_m55_body(raw)
    p = tmp_path / "m55.json"
    p.write_text(canonical_json_dumps(sealed), encoding="utf-8")
    body = build_operator_preflight_readout_decision(
        OperatorPreflightReadoutInputs(
            m55_preflight_json=p,
            expected_m54_package_sha256=CANONICAL_M54_PACKAGE_SHA256,
            expected_m53_run_artifact_sha256=CANONICAL_M53_RUN_ARTIFACT_SHA256,
            expected_candidate_sha256=CANONICAL_CANDIDATE_CHECKPOINT_SHA256,
            m54_readiness_json=None,
            m56a_context_json=None,
        ),
    )
    assert body["readout"]["decision_status"] == DECISION_BLOCKED_M54_MISMATCH


def test_operator_preflight_wrong_expected_m53_without_m54(tmp_path: Path) -> None:
    m55_dir = tmp_path / "m55"
    write_preflight_artifacts(m55_dir, body_unsealed=build_fixture_preflight())
    m55_path = m55_dir / "v15_bounded_evaluation_package_preflight.json"
    body = build_operator_preflight_readout_decision(
        OperatorPreflightReadoutInputs(
            m55_preflight_json=m55_path,
            expected_m54_package_sha256=CANONICAL_M54_PACKAGE_SHA256,
            expected_m53_run_artifact_sha256="b" * 64,
            expected_candidate_sha256=CANONICAL_CANDIDATE_CHECKPOINT_SHA256,
            m54_readiness_json=None,
            m56a_context_json=None,
        ),
    )
    assert body["readout"]["decision_status"] == DECISION_BLOCKED_M53_MISMATCH


def test_operator_preflight_invalid_m55_seal(tmp_path: Path) -> None:
    write_preflight_artifacts(tmp_path / "m", body_unsealed=build_fixture_preflight())
    p = tmp_path / "m" / "v15_bounded_evaluation_package_preflight.json"
    obj = json.loads(p.read_text(encoding="utf-8"))
    obj[M55_DIGEST] = "c" * 64
    p.write_text(canonical_json_dumps(obj), encoding="utf-8")
    body = build_operator_preflight_readout_decision(
        OperatorPreflightReadoutInputs(
            m55_preflight_json=p,
            expected_m54_package_sha256=CANONICAL_M54_PACKAGE_SHA256,
            expected_m53_run_artifact_sha256=CANONICAL_M53_RUN_ARTIFACT_SHA256,
            expected_candidate_sha256=CANONICAL_CANDIDATE_CHECKPOINT_SHA256,
            m54_readiness_json=None,
            m56a_context_json=None,
        ),
    )
    assert body["readout"]["decision_status"] == DECISION_BLOCKED_INVALID_M55_SEAL


def test_operator_preflight_missing_m55(tmp_path: Path) -> None:
    body = build_operator_preflight_readout_decision(
        OperatorPreflightReadoutInputs(
            m55_preflight_json=tmp_path / "missing.json",
            expected_m54_package_sha256=CANONICAL_M54_PACKAGE_SHA256,
            expected_m53_run_artifact_sha256=CANONICAL_M53_RUN_ARTIFACT_SHA256,
            expected_candidate_sha256=CANONICAL_CANDIDATE_CHECKPOINT_SHA256,
            m54_readiness_json=None,
            m56a_context_json=None,
        ),
    )
    assert body["readout"]["decision_status"] == DECISION_BLOCKED_MISSING_M55


def test_m56a_scaffold_warning_only(tmp_path: Path) -> None:
    m55_dir = tmp_path / "m55"
    write_preflight_artifacts(m55_dir, body_unsealed=build_fixture_preflight())
    m55_path = m55_dir / "v15_bounded_evaluation_package_preflight.json"
    m56a = tmp_path / "m56a.json"
    m56a.write_text(
        json.dumps(
            {
                "contract_id": CONTRACT_ID_M56A_MAIN,
                "watchability_profile": {"policy_source": POLICY_SCAFFOLD},
            },
        ),
        encoding="utf-8",
    )
    body = build_operator_preflight_readout_decision(
        OperatorPreflightReadoutInputs(
            m55_preflight_json=m55_path,
            expected_m54_package_sha256=CANONICAL_M54_PACKAGE_SHA256,
            expected_m53_run_artifact_sha256=CANONICAL_M53_RUN_ARTIFACT_SHA256,
            expected_candidate_sha256=CANONICAL_CANDIDATE_CHECKPOINT_SHA256,
            m54_readiness_json=None,
            m56a_context_json=m56a,
        ),
    )
    assert body["readout"]["decision_status"] == DECISION_READY
    from starlab.v15.m56_bounded_evaluation_package_readout_decision_models import (
        WARNING_M56A_STUB,
    )

    assert WARNING_M56A_STUB in body["readout"]["warnings"]


def test_operator_declared_happy(tmp_path: Path) -> None:
    m55_dir = tmp_path / "m55"
    man = tmp_path / "man.json"
    cand = tmp_path / "cand.json"
    score = tmp_path / "score.json"
    man.write_text(json.dumps({"kind": "m"}), encoding="utf-8")
    cand.write_text(json.dumps({"kind": "c"}), encoding="utf-8")
    score.write_text(json.dumps({"kind": "s"}), encoding="utf-8")
    from starlab.v15.m55_bounded_evaluation_package_preflight_io import (
        evaluation_package_binding_sha256,
        sha256_file_hex,
    )

    md, cd, sd = sha256_file_hex(man), sha256_file_hex(cand), sha256_file_hex(score)
    pkg = evaluation_package_binding_sha256(
        manifest_sha256=md,
        candidate_sha256=cd,
        scorecard_sha256=sd,
    )
    write_preflight_artifacts(
        m55_dir,
        body_unsealed=build_operator_declared_preflight(
            OperatorDeclaredInputs(
                evaluation_package_id="e.test",
                evaluation_package_sha256=pkg,
                upstream_m54_package_id=CANONICAL_UPSTREAM_M54_PACKAGE_ID,
                upstream_m54_package_sha256=CANONICAL_UPSTREAM_M54_PACKAGE_SHA256,
                evaluation_package_manifest=man,
                candidate_identity=cand,
                scorecard_readout_plan=score,
            ),
        ),
    )
    m55_path = m55_dir / "v15_bounded_evaluation_package_preflight.json"
    decl = tmp_path / "decl.json"
    decl.write_text(
        json.dumps(
            {"declared_candidate_checkpoint_sha256": CANONICAL_CANDIDATE_CHECKPOINT_SHA256},
        ),
        encoding="utf-8",
    )
    body = build_operator_declared_readout_decision(
        OperatorDeclaredReadoutInputs(
            declared_readout_json=decl,
            m55_preflight_json=m55_path,
            expected_candidate_sha256=CANONICAL_CANDIDATE_CHECKPOINT_SHA256,
        ),
    )
    assert body["readout"]["decision_status"] == DECISION_READY


def test_operator_declared_overclaim_blocked(tmp_path: Path) -> None:
    decl = tmp_path / "decl.json"
    decl.write_text(json.dumps({"evaluation_executed": True}), encoding="utf-8")
    m55_dir = tmp_path / "m55"
    write_preflight_artifacts(m55_dir, body_unsealed=build_fixture_preflight())
    m55_path = m55_dir / "v15_bounded_evaluation_package_preflight.json"
    body = build_operator_declared_readout_decision(
        OperatorDeclaredReadoutInputs(
            declared_readout_json=decl,
            m55_preflight_json=m55_path,
            expected_candidate_sha256=CANONICAL_CANDIDATE_CHECKPOINT_SHA256,
        ),
    )
    assert body["readout"]["decision_status"] == DECISION_BLOCKED_CLAIM_FLAGS


def test_operator_declared_private_boundary(tmp_path: Path) -> None:
    decl = tmp_path / "decl.json"
    decl.write_text(
        json.dumps({"note": "docs/company_secrets/x"}),
        encoding="utf-8",
    )
    m55_dir = tmp_path / "m55"
    write_preflight_artifacts(m55_dir, body_unsealed=build_fixture_preflight())
    m55_path = m55_dir / "v15_bounded_evaluation_package_preflight.json"
    body = build_operator_declared_readout_decision(
        OperatorDeclaredReadoutInputs(
            declared_readout_json=decl,
            m55_preflight_json=m55_path,
            expected_candidate_sha256=CANONICAL_CANDIDATE_CHECKPOINT_SHA256,
        ),
    )
    assert body["readout"]["decision_status"] == DECISION_BLOCKED_PRIVATE_BOUNDARY


def test_operator_declared_candidate_mismatch(tmp_path: Path) -> None:
    decl = tmp_path / "decl.json"
    decl.write_text(
        json.dumps({"declared_candidate_checkpoint_sha256": "d" * 64}),
        encoding="utf-8",
    )
    m55_dir = tmp_path / "m55"
    write_preflight_artifacts(m55_dir, body_unsealed=build_fixture_preflight())
    m55_path = m55_dir / "v15_bounded_evaluation_package_preflight.json"
    body = build_operator_declared_readout_decision(
        OperatorDeclaredReadoutInputs(
            declared_readout_json=decl,
            m55_preflight_json=m55_path,
            expected_candidate_sha256=CANONICAL_CANDIDATE_CHECKPOINT_SHA256,
        ),
    )
    assert body["readout"]["decision_status"] == DECISION_BLOCKED_CANDIDATE_MISMATCH


def test_emit_m56_cli_fixture_ci_writes_main_json(tmp_path: Path) -> None:
    out = tmp_path / "out"
    assert (
        emit_m56_main(
            [
                "--profile",
                "fixture_ci",
                "--output-dir",
                str(out),
            ],
        )
        == 0
    )
    main_p = out / FILENAME_MAIN_JSON
    assert main_p.is_file()
    sealed = json.loads(main_p.read_text(encoding="utf-8"))
    assert sealed["readout"]["decision_status"] == DECISION_READY


def test_emit_m56_cli_operator_preflight_missing_args(tmp_path: Path) -> None:
    assert (
        emit_m56_main(
            [
                "--profile",
                "operator_preflight",
                "--output-dir",
                str(tmp_path / "o"),
            ],
        )
        == 2
    )


def test_emit_m56_cli_operator_preflight_invalid_candidate_hex(tmp_path: Path) -> None:
    m55_dir = tmp_path / "m55"
    write_preflight_artifacts(m55_dir, body_unsealed=build_fixture_preflight())
    m55_path = m55_dir / "v15_bounded_evaluation_package_preflight.json"
    assert (
        emit_m56_main(
            [
                "--profile",
                "operator_preflight",
                "--output-dir",
                str(tmp_path / "o"),
                "--m55-preflight-json",
                str(m55_path),
                "--expected-m54-package-sha256",
                CANONICAL_M54_PACKAGE_SHA256,
                "--expected-m53-run-artifact-sha256",
                CANONICAL_M53_RUN_ARTIFACT_SHA256,
                "--expected-candidate-sha256",
                "not_hex",
            ],
        )
        == 2
    )


def test_emit_m56_cli_operator_preflight_happy(tmp_path: Path) -> None:
    m55_dir = tmp_path / "m55"
    write_preflight_artifacts(m55_dir, body_unsealed=build_fixture_preflight())
    m55_path = m55_dir / "v15_bounded_evaluation_package_preflight.json"
    out = tmp_path / "out"
    assert (
        emit_m56_main(
            [
                "--profile",
                "operator_preflight",
                "--output-dir",
                str(out),
                "--m55-preflight-json",
                str(m55_path),
                "--expected-m54-package-sha256",
                CANONICAL_M54_PACKAGE_SHA256,
                "--expected-m53-run-artifact-sha256",
                CANONICAL_M53_RUN_ARTIFACT_SHA256,
                "--expected-candidate-sha256",
                CANONICAL_CANDIDATE_CHECKPOINT_SHA256,
            ],
        )
        == 0
    )
    sealed = json.loads((out / FILENAME_MAIN_JSON).read_text(encoding="utf-8"))
    assert sealed["readout"]["decision_status"] == DECISION_READY


def test_emit_m56_cli_operator_preflight_blocked_exit_3(tmp_path: Path) -> None:
    write_preflight_artifacts(tmp_path / "m", body_unsealed=build_fixture_preflight())
    p = tmp_path / "m" / "v15_bounded_evaluation_package_preflight.json"
    obj = json.loads(p.read_text(encoding="utf-8"))
    obj[M55_DIGEST] = "c" * 64
    p.write_text(canonical_json_dumps(obj), encoding="utf-8")
    out = tmp_path / "out"
    assert (
        emit_m56_main(
            [
                "--profile",
                "operator_preflight",
                "--output-dir",
                str(out),
                "--m55-preflight-json",
                str(p),
                "--expected-m54-package-sha256",
                CANONICAL_M54_PACKAGE_SHA256,
                "--expected-m53-run-artifact-sha256",
                CANONICAL_M53_RUN_ARTIFACT_SHA256,
                "--expected-candidate-sha256",
                CANONICAL_CANDIDATE_CHECKPOINT_SHA256,
            ],
        )
        == 3
    )


def test_emit_m56_cli_forbidden_flag_emits_blocked_readout(tmp_path: Path) -> None:
    out = tmp_path / "out"
    assert (
        emit_m56_main(
            [
                "--profile",
                "fixture_ci",
                "--output-dir",
                str(out),
                FORBIDDEN_FLAG_RUN_BENCHMARK,
            ],
        )
        == 0
    )
    sealed = json.loads((out / FILENAME_MAIN_JSON).read_text(encoding="utf-8"))
    assert sealed["readout"]["decision_status"] == DECISION_BLOCKED_CLAIM_FLAGS


def test_emit_m56_cli_operator_declared_missing_args(tmp_path: Path) -> None:
    assert (
        emit_m56_main(
            [
                "--profile",
                "operator_declared",
                "--output-dir",
                str(tmp_path / "o"),
            ],
        )
        == 2
    )


def test_emit_m56_cli_operator_declared_happy(tmp_path: Path) -> None:
    m55_dir = tmp_path / "m55"
    man = tmp_path / "man.json"
    cand = tmp_path / "cand.json"
    score = tmp_path / "score.json"
    man.write_text(json.dumps({"kind": "m"}), encoding="utf-8")
    cand.write_text(json.dumps({"kind": "c"}), encoding="utf-8")
    score.write_text(json.dumps({"kind": "s"}), encoding="utf-8")
    from starlab.v15.m55_bounded_evaluation_package_preflight_io import (
        evaluation_package_binding_sha256,
        sha256_file_hex,
    )

    md, cd, sd = sha256_file_hex(man), sha256_file_hex(cand), sha256_file_hex(score)
    pkg = evaluation_package_binding_sha256(
        manifest_sha256=md,
        candidate_sha256=cd,
        scorecard_sha256=sd,
    )
    write_preflight_artifacts(
        m55_dir,
        body_unsealed=build_operator_declared_preflight(
            OperatorDeclaredInputs(
                evaluation_package_id="e.test",
                evaluation_package_sha256=pkg,
                upstream_m54_package_id=CANONICAL_UPSTREAM_M54_PACKAGE_ID,
                upstream_m54_package_sha256=CANONICAL_UPSTREAM_M54_PACKAGE_SHA256,
                evaluation_package_manifest=man,
                candidate_identity=cand,
                scorecard_readout_plan=score,
            ),
        ),
    )
    m55_path = m55_dir / "v15_bounded_evaluation_package_preflight.json"
    decl = tmp_path / "decl.json"
    decl.write_text(
        json.dumps(
            {"declared_candidate_checkpoint_sha256": CANONICAL_CANDIDATE_CHECKPOINT_SHA256},
        ),
        encoding="utf-8",
    )
    out = tmp_path / "out"
    assert (
        emit_m56_main(
            [
                "--profile",
                "operator_declared",
                "--output-dir",
                str(out),
                "--declared-readout-json",
                str(decl),
                "--m55-preflight-json",
                str(m55_path),
                "--expected-candidate-sha256",
                CANONICAL_CANDIDATE_CHECKPOINT_SHA256,
            ],
        )
        == 0
    )
    sealed = json.loads((out / FILENAME_MAIN_JSON).read_text(encoding="utf-8"))
    assert sealed["readout"]["decision_status"] == DECISION_READY


def test_emit_m56_cli_operator_declared_blocked_exit_3(tmp_path: Path) -> None:
    decl = tmp_path / "decl.json"
    decl.write_text(json.dumps({"evaluation_executed": True}), encoding="utf-8")
    m55_dir = tmp_path / "m55"
    write_preflight_artifacts(m55_dir, body_unsealed=build_fixture_preflight())
    m55_path = m55_dir / "v15_bounded_evaluation_package_preflight.json"
    out = tmp_path / "out"
    assert (
        emit_m56_main(
            [
                "--profile",
                "operator_declared",
                "--output-dir",
                str(out),
                "--declared-readout-json",
                str(decl),
                "--m55-preflight-json",
                str(m55_path),
                "--expected-candidate-sha256",
                CANONICAL_CANDIDATE_CHECKPOINT_SHA256,
            ],
        )
        == 3
    )
