"""M59 ladder/public evaluation protocol & evidence surface (fixture-only; synthetic data)."""

from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest
from starlab._io import load_json_object_strict
from starlab.runs.json_util import canonical_json_dumps, sha256_hex_of_canonical_json
from starlab.sc2.emit_ladder_public_evaluation_evidence import (
    write_ladder_public_evaluation_evidence_artifacts,
)
from starlab.sc2.emit_ladder_public_evaluation_protocol import (
    write_ladder_public_evaluation_protocol_artifacts,
)
from starlab.sc2.ladder_public_evaluation_evidence import ladder_public_evaluation_evidence_bundle
from starlab.sc2.ladder_public_evaluation_models import (
    LADDER_PUBLIC_EVALUATION_EVIDENCE_CONTRACT_ID,
    LADDER_PUBLIC_EVALUATION_PROTOCOL_CONTRACT_ID,
    M59_PROTOCOL_PROFILE_SINGLE_CANDIDATE_PUBLIC_EVAL_V1,
)
from starlab.sc2.ladder_public_evaluation_protocol import ladder_public_evaluation_protocol_bundle

REPO_ROOT = Path(__file__).resolve().parents[1]
FIX = REPO_ROOT / "tests" / "fixtures" / "m59"
PROTOCOL_INPUT = FIX / "subject_candidate.json"
ROWS_COMPLETE = FIX / "result_rows_complete.json"
ROWS_INCOMPLETE = FIX / "result_rows_incomplete.json"


def test_governance_docs_include_m59_runtime_doc() -> None:
    text = (REPO_ROOT / "tests" / "test_governance_docs.py").read_text(encoding="utf-8")
    assert "ladder_public_evaluation_protocol_evidence_surface_v1.md" in text


def test_protocol_contract_id_and_profile() -> None:
    raw = PROTOCOL_INPUT.read_bytes()
    obj = load_json_object_strict(PROTOCOL_INPUT)
    p, r = ladder_public_evaluation_protocol_bundle(
        input_obj=obj,
        input_sha256=__import__("hashlib").sha256(raw).hexdigest(),
    )
    assert p["contract_id"] == LADDER_PUBLIC_EVALUATION_PROTOCOL_CONTRACT_ID
    assert p["protocol_profile_id"] == M59_PROTOCOL_PROFILE_SINGLE_CANDIDATE_PUBLIC_EVAL_V1
    assert r["protocol_canonical_sha256"] == sha256_hex_of_canonical_json(p)


def test_protocol_emit_is_byte_stable(tmp_path: Path) -> None:
    a1, _ = write_ladder_public_evaluation_protocol_artifacts(
        input_path=PROTOCOL_INPUT,
        output_dir=tmp_path / "a",
    )
    a2, _ = write_ladder_public_evaluation_protocol_artifacts(
        input_path=PROTOCOL_INPUT,
        output_dir=tmp_path / "b",
    )
    assert a1.read_text(encoding="utf-8") == a2.read_text(encoding="utf-8")


def test_evidence_emit_complete_is_stable_and_sorted(tmp_path: Path) -> None:
    pdir = tmp_path / "proto"
    write_ladder_public_evaluation_protocol_artifacts(input_path=PROTOCOL_INPUT, output_dir=pdir)
    protocol_path = pdir / "ladder_public_evaluation_protocol.json"
    e1, _ = write_ladder_public_evaluation_evidence_artifacts(
        protocol_path=protocol_path,
        result_rows_path=ROWS_COMPLETE,
        output_dir=tmp_path / "e1",
    )
    shuffled = json.loads(ROWS_COMPLETE.read_text(encoding="utf-8"))
    rows = shuffled["result_rows"]
    shuffled["result_rows"] = list(reversed(rows))
    sp = tmp_path / "shuffled.json"
    sp.write_text(json.dumps(shuffled, indent=2) + "\n", encoding="utf-8")
    e2, _ = write_ladder_public_evaluation_evidence_artifacts(
        protocol_path=protocol_path,
        result_rows_path=sp,
        output_dir=tmp_path / "e2",
    )
    j1 = load_json_object_strict(e1)
    j2 = load_json_object_strict(e2)
    j1.pop("generated_attribution", None)
    j2.pop("generated_attribution", None)
    assert j1 == j2
    ev = load_json_object_strict(e1)
    ids = [r["stable_match_id"] for r in ev["result_rows"]]
    assert ids == sorted(ids)


def test_aggregate_counts_complete_fixture(tmp_path: Path) -> None:
    pdir = tmp_path / "proto"
    write_ladder_public_evaluation_protocol_artifacts(input_path=PROTOCOL_INPUT, output_dir=pdir)
    ev_path, _ = write_ladder_public_evaluation_evidence_artifacts(
        protocol_path=pdir / "ladder_public_evaluation_protocol.json",
        result_rows_path=ROWS_COMPLETE,
        output_dir=tmp_path / "out",
    )
    ev = load_json_object_strict(ev_path)
    assert ev["contract_id"] == LADDER_PUBLIC_EVALUATION_EVIDENCE_CONTRACT_ID
    s = ev["aggregate_summary"]
    assert s["total_matches_observed"] == 6
    assert s["results"] == {"wins": 3, "losses": 1, "draws": 1, "unknown": 1}
    assert s["map_coverage"]["unknown_map_name_rows"] == 0
    assert ev["evidence_posture_status"] == "bounded_complete"
    assert any("synthetic" in x.lower() or "fixture" in x.lower() for x in ev["non_claims"])


def test_incomplete_posture_and_gaps(tmp_path: Path) -> None:
    pdir = tmp_path / "proto"
    write_ladder_public_evaluation_protocol_artifacts(input_path=PROTOCOL_INPUT, output_dir=pdir)
    ev_path, _ = write_ladder_public_evaluation_evidence_artifacts(
        protocol_path=pdir / "ladder_public_evaluation_protocol.json",
        result_rows_path=ROWS_INCOMPLETE,
        output_dir=tmp_path / "out",
    )
    ev = load_json_object_strict(ev_path)
    assert ev["evidence_posture_status"] == "bounded_incomplete"
    kinds = {g["kind"] for g in ev["coverage_gaps"]}
    assert "map_name_unknown" in kinds
    assert "replay_linkage_incomplete" not in kinds


def test_reject_subject_mismatch(tmp_path: Path) -> None:
    pdir = tmp_path / "proto"
    write_ladder_public_evaluation_protocol_artifacts(input_path=PROTOCOL_INPUT, output_dir=pdir)
    bad = copy.deepcopy(load_json_object_strict(ROWS_COMPLETE))
    bad["result_rows"][0]["subject_candidate_id"] = "wrong_id"
    bp = tmp_path / "bad.json"
    bp.write_text(canonical_json_dumps(bad), encoding="utf-8")
    with pytest.raises(ValueError, match="subject_candidate_id mismatch"):
        write_ladder_public_evaluation_evidence_artifacts(
            protocol_path=pdir / "ladder_public_evaluation_protocol.json",
            result_rows_path=bp,
            output_dir=tmp_path / "o",
        )


def test_reject_venue_mismatch(tmp_path: Path) -> None:
    pdir = tmp_path / "proto"
    write_ladder_public_evaluation_protocol_artifacts(input_path=PROTOCOL_INPUT, output_dir=pdir)
    bad = copy.deepcopy(load_json_object_strict(ROWS_COMPLETE))
    bad["result_rows"][0]["venue_surface_kind"] = "public_match_set"
    bp = tmp_path / "bad.json"
    bp.write_text(canonical_json_dumps(bad), encoding="utf-8")
    with pytest.raises(ValueError, match="venue_surface_kind mismatch"):
        write_ladder_public_evaluation_evidence_artifacts(
            protocol_path=pdir / "ladder_public_evaluation_protocol.json",
            result_rows_path=bp,
            output_dir=tmp_path / "o",
        )


def test_reject_evidence_class_not_in_protocol(tmp_path: Path) -> None:
    pdir = tmp_path / "proto"
    write_ladder_public_evaluation_protocol_artifacts(input_path=PROTOCOL_INPUT, output_dir=pdir)
    bad = copy.deepcopy(load_json_object_strict(ROWS_COMPLETE))
    bad["result_rows"][0]["evidence_class"] = "result_row_only"
    bad["result_rows"][0].pop("replay_reference_hash", None)
    bad["result_rows"][0]["source_reference"] = "synthetic://fixture/result_only/007.json"
    bp = tmp_path / "bad.json"
    bp.write_text(canonical_json_dumps(bad), encoding="utf-8")
    narrow = load_json_object_strict(PROTOCOL_INPUT)
    narrow["accepted_evidence_classes"] = ["replay_bound_result"]
    narrow_path = tmp_path / "narrow_protocol_input.json"
    narrow_path.write_text(canonical_json_dumps(narrow), encoding="utf-8")
    write_ladder_public_evaluation_protocol_artifacts(
        input_path=narrow_path,
        output_dir=tmp_path / "narrow_proto",
    )
    with pytest.raises(ValueError, match="not accepted by protocol"):
        write_ladder_public_evaluation_evidence_artifacts(
            protocol_path=tmp_path / "narrow_proto" / "ladder_public_evaluation_protocol.json",
            result_rows_path=bp,
            output_dir=tmp_path / "o",
        )


def test_reject_duplicate_stable_match_id() -> None:
    obj = load_json_object_strict(PROTOCOL_INPUT)
    raw = PROTOCOL_INPUT.read_bytes()
    protocol_obj, _ = ladder_public_evaluation_protocol_bundle(
        input_obj=obj,
        input_sha256=__import__("hashlib").sha256(raw).hexdigest(),
    )
    rows_obj = load_json_object_strict(ROWS_COMPLETE)
    rows_obj["result_rows"].append(copy.deepcopy(rows_obj["result_rows"][0]))
    with pytest.raises(ValueError, match="duplicate stable_match_id"):
        ladder_public_evaluation_evidence_bundle(
            protocol_obj=protocol_obj,
            result_input_obj=rows_obj,
            result_input_sha256="0" * 64,
        )


def test_m59_sc2_modules_are_self_contained() -> None:
    forbidden = ("starlab.replays", "s2protocol", "canonical_state")
    for name in (
        "ladder_public_evaluation_models.py",
        "ladder_public_evaluation_protocol.py",
        "ladder_public_evaluation_evidence.py",
        "emit_ladder_public_evaluation_protocol.py",
        "emit_ladder_public_evaluation_evidence.py",
    ):
        text = (REPO_ROOT / "starlab" / "sc2" / name).read_text(encoding="utf-8")
        for sub in forbidden:
            assert sub not in text, f"{name} must not reference {sub}"


def test_non_claims_preserved_from_protocol(tmp_path: Path) -> None:
    pdir = tmp_path / "proto"
    write_ladder_public_evaluation_protocol_artifacts(input_path=PROTOCOL_INPUT, output_dir=pdir)
    protocol = load_json_object_strict(pdir / "ladder_public_evaluation_protocol.json")
    needle = "Fixture protocol"
    assert any(needle in x for x in protocol["required_non_claims"])
    ev_path, _ = write_ladder_public_evaluation_evidence_artifacts(
        protocol_path=pdir / "ladder_public_evaluation_protocol.json",
        result_rows_path=ROWS_COMPLETE,
        output_dir=tmp_path / "out",
    )
    ev = load_json_object_strict(ev_path)
    joined = "\n".join(ev["non_claims"])
    assert needle in joined
