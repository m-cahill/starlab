"""PV1-M01 observability index + tranche checkpoint receipt (fixture-only)."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from starlab.runs.json_util import canonical_json_dumps
from starlab.training.emit_campaign_observability_index import (
    write_campaign_observability_index_artifacts,
)
from starlab.training.emit_tranche_checkpoint_receipt import (
    write_tranche_checkpoint_receipt_artifacts,
)
from starlab.training.pv1_campaign_observability_models import ALL_EVIDENCE_STATUSES_V1
from starlab.training.pv1_campaign_observability_views import (
    build_campaign_observability_index,
    build_tranche_checkpoint_receipt,
)

REPO = Path(__file__).resolve().parents[1]
FIX = REPO / "tests" / "fixtures" / "pv1_m01"


def _expect_root(path: Path) -> str:
    return path.resolve().as_posix()


def test_evidence_status_vocabulary_sorted() -> None:
    assert list(ALL_EVIDENCE_STATUSES_V1) == sorted(ALL_EVIDENCE_STATUSES_V1)


def test_index_complete_fixture() -> None:
    root = FIX / "campaign_complete"
    body, rep = build_campaign_observability_index(campaign_root=root)
    assert body["index_status"] == "complete"
    assert body["missing_required_evidence"] == []
    assert body["campaign_id"] == "pv1_m01_complete_fixture"
    assert body["campaign_root"] == _expect_root(root)
    assert rep["index_status"] == "complete"


def test_index_missing_watchable_fixture() -> None:
    root = FIX / "campaign_missing_watchable"
    body, _rep = build_campaign_observability_index(campaign_root=root)
    assert body["index_status"] == "missing_required_evidence"
    missing = body["missing_required_evidence"]
    assert any("local_live_play_validation" in m for m in missing)


def test_checkpoint_receipt_complete() -> None:
    root = FIX / "campaign_complete"
    receipt, report = build_tranche_checkpoint_receipt(
        campaign_root=root,
        tranche_id="tranche_a",
        checkpoint_id="close_001",
        operator_paused=False,
        operator_incomplete=False,
        operator_note=None,
        operator_note_ref=None,
    )
    assert receipt["checkpoint_evidence_status"] == "complete"
    assert receipt["missing_evidence_refs"] == []
    assert report["checkpoint_evidence_status"] == "complete"


def test_checkpoint_receipt_paused_when_complete_tree() -> None:
    root = FIX / "campaign_complete"
    receipt, _ = build_tranche_checkpoint_receipt(
        campaign_root=root,
        tranche_id="tranche_a",
        checkpoint_id="pause_001",
        operator_paused=True,
        operator_incomplete=False,
        operator_note="scheduled pause",
        operator_note_ref=None,
    )
    assert receipt["checkpoint_evidence_status"] == "paused"
    assert receipt["operator_note"] == "scheduled pause"


def test_checkpoint_receipt_missing_overrides_paused() -> None:
    root = FIX / "campaign_missing_watchable"
    receipt, _ = build_tranche_checkpoint_receipt(
        campaign_root=root,
        tranche_id="tranche_a",
        checkpoint_id="k",
        operator_paused=True,
        operator_incomplete=False,
        operator_note=None,
        operator_note_ref=None,
    )
    assert receipt["checkpoint_evidence_status"] == "missing_required_evidence"


def test_checkpoint_receipt_incomplete_flag() -> None:
    root = FIX / "campaign_complete"
    receipt, _ = build_tranche_checkpoint_receipt(
        campaign_root=root,
        tranche_id="t",
        checkpoint_id="k",
        operator_paused=False,
        operator_incomplete=True,
        operator_note=None,
        operator_note_ref=None,
    )
    assert receipt["checkpoint_evidence_status"] == "incomplete"


def test_deterministic_rerun_index() -> None:
    root = FIX / "campaign_complete"
    a1, r1 = build_campaign_observability_index(campaign_root=root)
    a2, r2 = build_campaign_observability_index(campaign_root=root)
    assert canonical_json_dumps(a1) == canonical_json_dumps(a2)
    assert canonical_json_dumps(r1) == canonical_json_dumps(r2)


def test_emit_index_writes_valid_json(tmp_path: Path) -> None:
    root = FIX / "campaign_complete"
    p1, p2 = write_campaign_observability_index_artifacts(
        campaign_root=root,
        output_dir=tmp_path,
        campaign_contract=None,
    )
    assert json.loads(p1.read_text(encoding="utf-8"))["index_status"] == "complete"
    assert json.loads(p2.read_text(encoding="utf-8"))["index_status"] == "complete"


def test_emit_checkpoint_writes_valid_json(tmp_path: Path) -> None:
    root = FIX / "campaign_complete"
    p1, p2 = write_tranche_checkpoint_receipt_artifacts(
        campaign_root=root,
        output_dir=tmp_path,
        tranche_id="a",
        checkpoint_id="b",
        operator_paused=False,
        operator_incomplete=False,
        operator_note=None,
        operator_note_ref=None,
        campaign_contract=None,
    )
    assert json.loads(p1.read_text(encoding="utf-8"))["checkpoint_evidence_status"] == "complete"
    assert "receipt_sha256" in json.loads(p1.read_text(encoding="utf-8"))
    assert p2.is_file()


def test_bad_campaign_root_errors(tmp_path: Path) -> None:
    p = tmp_path / "not_a_dir"
    p.write_text("x", encoding="utf-8")
    with pytest.raises(ValueError, match="not a directory"):
        build_campaign_observability_index(campaign_root=p)
