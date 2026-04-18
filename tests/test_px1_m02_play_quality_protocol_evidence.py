"""PX1-M02 play-quality protocol & evidence emitters (fixture-only synthetic data)."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from starlab._io import load_json_object_strict
from starlab.runs.json_util import canonical_json_dumps, sha256_hex_of_canonical_json
from starlab.sc2.emit_px1_play_quality_evidence import write_px1_play_quality_evidence_artifacts
from starlab.sc2.emit_px1_play_quality_protocol import write_px1_play_quality_protocol_artifacts
from starlab.sc2.px1_play_quality_models import (
    PX1_M02_PROTOCOL_PROFILE_BOUNDED_LOCAL_LIVE_V1,
    PX1_PLAY_QUALITY_EVIDENCE_CONTRACT_ID,
    PX1_PLAY_QUALITY_PROTOCOL_CONTRACT_ID,
)
from starlab.sc2.px1_play_quality_protocol import px1_play_quality_protocol_bundle

REPO_ROOT = Path(__file__).resolve().parents[1]
FIX = REPO_ROOT / "tests" / "fixtures" / "px1_m02"
PROTOCOL_INPUT = FIX / "protocol_input.json"
EVAL_SELECTED = FIX / "evaluation_input_selected.json"
EVAL_NOT_SELECTED = FIX / "evaluation_input_not_selected.json"


def test_governance_docs_include_px1_m02_runtime_doc() -> None:
    text = (REPO_ROOT / "tests" / "test_governance_docs.py").read_text(encoding="utf-8")
    assert "px1_play_quality_demo_candidate_selection_v1.md" in text


def test_protocol_contract_id_and_profile() -> None:
    raw = PROTOCOL_INPUT.read_bytes()
    obj = load_json_object_strict(PROTOCOL_INPUT)
    p, r = px1_play_quality_protocol_bundle(
        input_obj=obj,
        input_sha256=__import__("hashlib").sha256(raw).hexdigest(),
    )
    assert p["contract_id"] == PX1_PLAY_QUALITY_PROTOCOL_CONTRACT_ID
    assert p["protocol_profile_id"] == PX1_M02_PROTOCOL_PROFILE_BOUNDED_LOCAL_LIVE_V1
    assert r["protocol_canonical_sha256"] == sha256_hex_of_canonical_json(p)


def test_protocol_emit_is_byte_stable(tmp_path: Path) -> None:
    a1, _ = write_px1_play_quality_protocol_artifacts(
        input_path=PROTOCOL_INPUT,
        output_dir=tmp_path / "a",
    )
    a2, _ = write_px1_play_quality_protocol_artifacts(
        input_path=PROTOCOL_INPUT,
        output_dir=tmp_path / "b",
    )
    assert a1.read_text(encoding="utf-8") == a2.read_text(encoding="utf-8")


def test_evidence_emit_selected_is_stable(tmp_path: Path) -> None:
    pdir = tmp_path / "proto"
    write_px1_play_quality_protocol_artifacts(input_path=PROTOCOL_INPUT, output_dir=pdir)
    protocol_path = pdir / "px1_play_quality_protocol.json"
    e1, r1 = write_px1_play_quality_evidence_artifacts(
        protocol_path=protocol_path,
        evaluation_input_path=EVAL_SELECTED,
        output_dir=tmp_path / "e1",
    )
    e2, r2 = write_px1_play_quality_evidence_artifacts(
        protocol_path=protocol_path,
        evaluation_input_path=EVAL_SELECTED,
        output_dir=tmp_path / "e2",
    )
    assert e1.read_text(encoding="utf-8") == e2.read_text(encoding="utf-8")
    ev = load_json_object_strict(e1)
    assert ev["contract_id"] == PX1_PLAY_QUALITY_EVIDENCE_CONTRACT_ID
    rep = load_json_object_strict(r1)
    assert rep["selection_consistent_with_thresholds"] is True


def test_evidence_emit_not_selected_consistent(tmp_path: Path) -> None:
    pdir = tmp_path / "proto"
    write_px1_play_quality_protocol_artifacts(input_path=PROTOCOL_INPUT, output_dir=pdir)
    e_path, r_path = write_px1_play_quality_evidence_artifacts(
        protocol_path=pdir / "px1_play_quality_protocol.json",
        evaluation_input_path=EVAL_NOT_SELECTED,
        output_dir=tmp_path / "out",
    )
    ev = load_json_object_strict(e_path)
    assert ev["evaluation"]["selection"]["status"] == "not_selected_within_scope"
    rep = load_json_object_strict(r_path)
    assert rep["selection_consistent_with_thresholds"] is True


def test_evaluation_per_profile_key_mismatch_raises(tmp_path: Path) -> None:
    pdir = tmp_path / "proto"
    write_px1_play_quality_protocol_artifacts(input_path=PROTOCOL_INPUT, output_dir=pdir)
    bad = json.loads(EVAL_SELECTED.read_text(encoding="utf-8"))
    per = bad["candidates_evaluated"][0]["per_opponent_profile"]
    only_key = next(iter(per))
    bad["candidates_evaluated"][0]["per_opponent_profile"] = {only_key: per[only_key]}
    bad_path = tmp_path / "bad.json"
    bad_path.write_text(canonical_json_dumps(bad), encoding="utf-8")

    with pytest.raises(ValueError, match="per_opponent_profile keys"):
        write_px1_play_quality_evidence_artifacts(
            protocol_path=pdir / "px1_play_quality_protocol.json",
            evaluation_input_path=bad_path,
            output_dir=tmp_path / "o",
        )


def test_emit_protocol_cli_main_success_and_errors(tmp_path: Path) -> None:
    from starlab.sc2.emit_px1_play_quality_protocol import main as protocol_main

    out = tmp_path / "proto_out"
    out.mkdir()
    assert (
        protocol_main(
            ["--input", str(PROTOCOL_INPUT), "--output-dir", str(out)],
        )
        == 0
    )
    assert (
        protocol_main(
            ["--input", str(tmp_path / "nonexistent_protocol.json"), "--output-dir", str(out)],
        )
        == 1
    )


def test_emit_evidence_cli_main_success_and_errors(tmp_path: Path) -> None:
    from starlab.sc2.emit_px1_play_quality_evidence import main as evidence_main

    pdir = tmp_path / "proto"
    write_px1_play_quality_protocol_artifacts(input_path=PROTOCOL_INPUT, output_dir=pdir)
    evout = tmp_path / "evidence_out"
    evout.mkdir()
    assert (
        evidence_main(
            [
                "--protocol",
                str(pdir / "px1_play_quality_protocol.json"),
                "--evaluation-input",
                str(EVAL_SELECTED),
                "--output-dir",
                str(evout),
            ],
        )
        == 0
    )
    assert (
        evidence_main(
            [
                "--protocol",
                str(pdir / "px1_play_quality_protocol.json"),
                "--evaluation-input",
                str(tmp_path / "missing_eval.json"),
                "--output-dir",
                str(evout),
            ],
        )
        == 1
    )
