"""PX1-M03 demo-readiness protocol & evidence emitters (fixture-only synthetic data)."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from starlab._io import load_json_object_strict
from starlab.runs.json_util import sha256_hex_of_canonical_json
from starlab.sc2.emit_px1_demo_readiness_evidence import write_px1_demo_readiness_evidence_artifacts
from starlab.sc2.emit_px1_demo_readiness_protocol import write_px1_demo_readiness_protocol_artifacts
from starlab.sc2.px1_demo_readiness_models import (
    PX1_DEMO_READINESS_EVIDENCE_CONTRACT_ID,
    PX1_DEMO_READINESS_PROTOCOL_CONTRACT_ID,
    PX1_M03_PROTOCOL_PROFILE_DEMO_READINESS_REMEDIATION_V1,
)
from starlab.sc2.px1_demo_readiness_protocol import px1_demo_readiness_protocol_bundle

REPO_ROOT = Path(__file__).resolve().parents[1]
FIX = REPO_ROOT / "tests" / "fixtures" / "px1_m03"
PROTOCOL_INPUT = FIX / "protocol_input_v1.json"
EVAL_DEMO_READY = FIX / "evaluation_input_demo_ready.json"
EVAL_NO_DEMO = FIX / "evaluation_input_no_demo_ready.json"


def test_protocol_bundle_rejects_wrong_profile_id() -> None:
    import hashlib

    obj = load_json_object_strict(PROTOCOL_INPUT)
    obj["protocol_profile_id"] = "starlab.invalid.profile"
    raw = json.dumps(obj, sort_keys=True).encode("utf-8")
    with pytest.raises(ValueError, match="unsupported protocol_profile_id"):
        px1_demo_readiness_protocol_bundle(
            input_obj=obj,
            input_sha256=hashlib.sha256(raw).hexdigest(),
        )


def test_protocol_bundle_rejects_non_string_optional_notes() -> None:
    import hashlib

    obj = load_json_object_strict(PROTOCOL_INPUT)
    obj["candidate_pool"][0]["notes"] = 123
    raw = json.dumps(obj, sort_keys=True).encode("utf-8")
    with pytest.raises(ValueError, match="optional string"):
        px1_demo_readiness_protocol_bundle(
            input_obj=obj,
            input_sha256=hashlib.sha256(raw).hexdigest(),
        )


def test_protocol_contract_id_and_profile() -> None:
    raw = PROTOCOL_INPUT.read_bytes()
    obj = load_json_object_strict(PROTOCOL_INPUT)
    p, r = px1_demo_readiness_protocol_bundle(
        input_obj=obj,
        input_sha256=__import__("hashlib").sha256(raw).hexdigest(),
    )
    assert p["contract_id"] == PX1_DEMO_READINESS_PROTOCOL_CONTRACT_ID
    assert p["protocol_profile_id"] == PX1_M03_PROTOCOL_PROFILE_DEMO_READINESS_REMEDIATION_V1
    assert r["protocol_canonical_sha256"] == sha256_hex_of_canonical_json(p)


def test_protocol_emit_is_byte_stable(tmp_path: Path) -> None:
    a1, _ = write_px1_demo_readiness_protocol_artifacts(
        input_path=PROTOCOL_INPUT,
        output_dir=tmp_path / "a",
    )
    a2, _ = write_px1_demo_readiness_protocol_artifacts(
        input_path=PROTOCOL_INPUT,
        output_dir=tmp_path / "b",
    )
    assert a1.read_text(encoding="utf-8") == a2.read_text(encoding="utf-8")


def test_evidence_emit_demo_ready_consistent(tmp_path: Path) -> None:
    pdir = tmp_path / "proto"
    write_px1_demo_readiness_protocol_artifacts(input_path=PROTOCOL_INPUT, output_dir=pdir)
    protocol_path = pdir / "px1_demo_readiness_protocol.json"
    e1, r1 = write_px1_demo_readiness_evidence_artifacts(
        protocol_path=protocol_path,
        evaluation_input_path=EVAL_DEMO_READY,
        output_dir=tmp_path / "e1",
    )
    ev = load_json_object_strict(e1)
    assert ev["contract_id"] == PX1_DEMO_READINESS_EVIDENCE_CONTRACT_ID
    assert ev["evaluation"]["selection"]["status"] == "demo-ready-candidate-selected"
    rep = load_json_object_strict(r1)
    assert rep["selection_consistent_with_thresholds"] is True


def test_evidence_emit_no_demo_ready_consistent(tmp_path: Path) -> None:
    pdir = tmp_path / "proto"
    write_px1_demo_readiness_protocol_artifacts(input_path=PROTOCOL_INPUT, output_dir=pdir)
    e_path, r_path = write_px1_demo_readiness_evidence_artifacts(
        protocol_path=pdir / "px1_demo_readiness_protocol.json",
        evaluation_input_path=EVAL_NO_DEMO,
        output_dir=tmp_path / "out",
    )
    ev = load_json_object_strict(e_path)
    assert ev["evaluation"]["selection"]["status"] == "no-demo-ready-candidate-within-scope"
    rep = load_json_object_strict(r_path)
    assert rep["selection_consistent_with_thresholds"] is True


def test_emit_protocol_cli_main(tmp_path: Path) -> None:
    from starlab.sc2.emit_px1_demo_readiness_protocol import main as protocol_main

    out = tmp_path / "proto_out"
    out.mkdir()
    assert (
        protocol_main(
            ["--input", str(PROTOCOL_INPUT), "--output-dir", str(out)],
        )
        == 0
    )


def test_protocol_cli_main_missing_input_returns_1(tmp_path: Path) -> None:
    from starlab.sc2.emit_px1_demo_readiness_protocol import main as protocol_main

    assert (
        protocol_main(
            ["--input", str(tmp_path / "missing.json"), "--output-dir", str(tmp_path / "out")],
        )
        == 1
    )


def test_evidence_cli_main_missing_protocol_returns_1(tmp_path: Path) -> None:
    from starlab.sc2.emit_px1_demo_readiness_evidence import main as ev_main

    assert (
        ev_main(
            [
                "--protocol",
                str(tmp_path / "missing.json"),
                "--evaluation-input",
                str(EVAL_DEMO_READY),
                "--output-dir",
                str(tmp_path / "ev_out"),
            ],
        )
        == 1
    )


def test_evidence_bundle_rejects_protocol_contract_mismatch(tmp_path: Path) -> None:
    from starlab.sc2.px1_demo_readiness_evidence import px1_demo_readiness_evidence_bundle

    pdir = tmp_path / "proto"
    write_px1_demo_readiness_protocol_artifacts(input_path=PROTOCOL_INPUT, output_dir=pdir)
    p = load_json_object_strict(pdir / "px1_demo_readiness_protocol.json")
    p["contract_id"] = "starlab.px1_demo_readiness_protocol.invalid"
    e = load_json_object_strict(EVAL_DEMO_READY)
    with pytest.raises(ValueError, match="protocol contract_id"):
        px1_demo_readiness_evidence_bundle(
            protocol_obj=p,
            evaluation_input_obj=e,
            evaluation_input_sha256="a" * 64,
        )


def test_evidence_bundle_rejects_protocol_schema_mismatch(tmp_path: Path) -> None:
    from starlab.sc2.px1_demo_readiness_evidence import px1_demo_readiness_evidence_bundle

    pdir = tmp_path / "proto"
    write_px1_demo_readiness_protocol_artifacts(input_path=PROTOCOL_INPUT, output_dir=pdir)
    p = load_json_object_strict(pdir / "px1_demo_readiness_protocol.json")
    p["schema_version"] = "0.0.0"
    e = load_json_object_strict(EVAL_DEMO_READY)
    with pytest.raises(ValueError, match="protocol schema_version"):
        px1_demo_readiness_evidence_bundle(
            protocol_obj=p,
            evaluation_input_obj=e,
            evaluation_input_sha256="c" * 64,
        )


def test_validate_rejects_empty_evaluation_series_id(tmp_path: Path) -> None:
    from starlab.sc2.px1_demo_readiness_evidence import validate_demo_readiness_evaluation_input

    pdir = tmp_path / "proto"
    write_px1_demo_readiness_protocol_artifacts(input_path=PROTOCOL_INPUT, output_dir=pdir)
    p = load_json_object_strict(pdir / "px1_demo_readiness_protocol.json")
    e = load_json_object_strict(EVAL_DEMO_READY)
    e["evaluation_series_id"] = "  "
    with pytest.raises(ValueError, match="evaluation_series_id"):
        validate_demo_readiness_evaluation_input(protocol_obj=p, eval_obj=e)
