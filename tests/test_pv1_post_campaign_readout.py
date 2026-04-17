"""PV1-M04 post-campaign readout (fixture-only)."""

from __future__ import annotations

import json
from pathlib import Path

from starlab.runs.json_util import canonical_json_dumps
from starlab.training.pv1_post_campaign_readout import (
    PV1_POST_CAMPAIGN_READOUT_FILENAME,
    build_pv1_post_campaign_readout,
    write_pv1_post_campaign_readout_artifacts,
)

REPO = Path(__file__).resolve().parents[1]
FIX = REPO / "tests" / "fixtures" / "pv1_m04" / "minimal_campaign"


def test_readout_fixture_threshold_not_met_and_tranches_within_scope() -> None:
    r1, rep1 = build_pv1_post_campaign_readout(campaign_root=FIX)
    r2, rep2 = build_pv1_post_campaign_readout(campaign_root=FIX)
    assert canonical_json_dumps(r1) == canonical_json_dumps(r2)
    assert r1["campaign_id"] == "pv1_m04_readout_fixture"
    assert r1["threshold_posture"] == "threshold-not-met"
    assert r1["threshold_unmet_fields"] == ["full_run_duration_target"]
    assert r1["tranche_a_posture"] == "completed_within_scope"
    assert r1["tranche_b_posture"] == "completed_within_scope"
    assert r1["campaign_result_summary"]["tuple"] == [
        "tranche_a:completed_within_scope",
        "tranche_b:completed_within_scope",
        "threshold:threshold-not-met",
    ]
    assert "threshold-not-met" in r1["campaign_result_summary"]["summary_line"]
    assert r1["comparative_evidence_summary"]["campaign_observability_index_status"] == "complete"
    assert r1["comparative_evidence_summary"]["execution_count"] == 2
    assert r1["comparative_evidence_summary"]["checkpoint_receipt_count"] == 2
    assert rep1["summary"]["threshold_posture"] == "threshold-not-met"


def test_emit_readout_writes_json(tmp_path: Path) -> None:
    p1, p2 = write_pv1_post_campaign_readout_artifacts(campaign_root=FIX, output_dir=tmp_path)
    assert p1.name == PV1_POST_CAMPAIGN_READOUT_FILENAME
    body = json.loads(p1.read_text(encoding="utf-8"))
    assert body["readout_sha256"] == json.loads(p1.read_text(encoding="utf-8"))["readout_sha256"]
    assert p2.is_file()
