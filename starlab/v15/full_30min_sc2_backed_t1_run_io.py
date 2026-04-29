"""Seal and emit V15-M29 full-horizon SC2-backed T1 run artifacts."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from starlab.runs.json_util import canonical_json_dumps
from starlab.v15.full_30min_sc2_backed_t1_run_models import (
    CONTRACT_ID,
    M20_M21_DEFERRED,
    MILESTONE_LABEL,
    PROFILE_FIXTURE_CI,
    REPORT_CONTRACT_KIND,
    UPSTREAM_M28_CANDIDATE_PT_SHA_SAMPLE,
)
from starlab.v15.sc2_backed_t1_candidate_training_io import seal_m28_body


def build_m29_evidence_payload(
    *,
    m28_sealed: dict[str, Any],
    profile: str,
    m29_outcome: str,
    evaluation_gate_status: str,
    fixture_only: bool,
) -> dict[str, Any]:
    ta = m28_sealed.get("training_attempt") or {}
    cc = m28_sealed.get("candidate_checkpoint") or {}
    upstream_roll = m28_sealed.get("upstream_m27_rollout") or {}
    chk_count = int(ta.get("checkpoint_count") or 0)

    wc = float(ta.get("wall_clock_seconds") or 0.0)
    req_sec = float(ta.get("requested_min_wall_clock_seconds") or 0.0)

    cand_sha_op = cc.get("sha256")
    cand_ref = cand_sha_op or UPSTREAM_M28_CANDIDATE_PT_SHA_SAMPLE

    ncs = list(m28_sealed.get("non_claims") or [])
    if fixture_only:
        ncs.extend(["m29_fixture_only_operator_local_not_this_path"])

    body_pre: dict[str, Any] = {
        "contract_id": CONTRACT_ID,
        "milestone": MILESTONE_LABEL,
        "profile": PROFILE_FIXTURE_CI if fixture_only else profile,
        "upstream_m27_artifact_sha256": str(upstream_roll.get("sha256") or ""),
        "upstream_m28_candidate_checkpoint_sha256_reference": cand_ref,
        "candidate_checkpoint_sha256_operator_local": cand_sha_op,
        "upstream_m28_contract_consumed": str(m28_sealed.get("contract_id") or ""),
        "run_mode": "fixture_ci_smoke_m29_bundle" if fixture_only else profile,
        "required_wall_clock_minutes_field": round(req_sec / 60.0, 9) if req_sec else None,
        "observed_wall_clock_seconds": wc,
        "requested_min_wall_clock_seconds": req_sec if req_sec else None,
        "full_wall_clock_satisfied": bool(ta.get("full_wall_clock_satisfied"))
        if not fixture_only
        else False,
        "early_stop_disabled": bool(ta.get("disable_loss_floor_early_stop")),
        "loss_floor_early_stop_disabled": bool(ta.get("disable_loss_floor_early_stop")),
        "continue_after_checkpoint": bool(ta.get("continue_after_checkpoint")),
        "sc2_backed_features_used": bool(ta.get("sc2_backed_features_used")),
        "training_update_count": int(ta.get("training_update_count") or 0),
        "checkpoint_count": chk_count,
        "candidate_checkpoint_promotion_status": cc.get(
            "promotion_status",
            "not_promoted_candidate_only",
        ),
        "m29_outcome": m29_outcome,
        "m28_upstream_outcome_mirror": str(m28_sealed.get("m28_outcome") or ""),
        "evaluation_package_gate_status": evaluation_gate_status,
        "upstream_m28_primary_artifact_sha256": str(m28_sealed.get("artifact_sha256") or ""),
        "m20_m21_gate_integration": M20_M21_DEFERRED,
        "non_claims": ncs,
    }
    return body_pre


def seal_m29_body(body_pre: dict[str, Any]) -> dict[str, Any]:
    return seal_m28_body(body_pre)


def write_m29_bundle(output_dir: Path, main_sealed: dict[str, Any]) -> tuple[Path, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    p_main = output_dir / "v15_full_30min_sc2_backed_t1_run.json"
    p_rep = output_dir / "v15_full_30min_sc2_backed_t1_run_report.json"
    p_main.write_text(canonical_json_dumps(main_sealed), encoding="utf-8")
    report = {
        "report_kind": REPORT_CONTRACT_KIND,
        "source_artifact_sha256": main_sealed.get("artifact_sha256"),
        "milestone": MILESTONE_LABEL,
        "summary": {
            "m29_outcome": main_sealed.get("m29_outcome"),
            "profile": main_sealed.get("profile"),
            "full_wall_clock_satisfied": main_sealed.get("full_wall_clock_satisfied"),
        },
    }
    p_rep.write_text(canonical_json_dumps(report), encoding="utf-8")
    return p_main, p_rep


def load_m28_sealed(path: Path) -> dict[str, Any]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        msg = "M28 artifact root must be an object."
        raise TypeError(msg)
    return raw
