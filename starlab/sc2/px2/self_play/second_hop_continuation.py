"""Bounded second-hop continuation after slice-12 re-anchor (PX2-M03 slice 13)."""

from __future__ import annotations

import json
import shutil
from pathlib import Path
from typing import Any, Final, cast

from starlab.sc2.px2.self_play.campaign_continuity import (
    EXECUTION_KIND_SLICE11,
    EXECUTION_KIND_SLICE12,
    EXECUTION_KIND_SLICE13,
)
from starlab.sc2.px2.self_play.continuation_run import (
    CONTINUATION_RUN_JSON,
    SLICE13_SECOND_HOP_CAMPAIGN_PROFILE_ID,
    run_bounded_continuation_run_consuming_current_candidate,
)
from starlab.sc2.px2.self_play.continuation_run_record import (
    CONTINUATION_RULE_SECOND_HOP_CONSUME_CURRENT_CANDIDATE_STUB,
    CONTINUATION_RUN_RECORD_VERSION_SLICE13,
)
from starlab.sc2.px2.self_play.current_candidate import (
    load_px2_self_play_current_candidate,
)
from starlab.sc2.px2.self_play.current_candidate_reanchor import (
    CURRENT_CANDIDATE_REANCHOR_JSON,
    run_bounded_current_candidate_reanchor_after_second_hop,
)
from starlab.sc2.px2.self_play.current_candidate_record import (
    CURRENT_CANDIDATE_RECORD_VERSION_SLICE12,
)
from starlab.sc2.px2.self_play.run_artifacts import write_json
from starlab.sc2.px2.self_play.second_hop_continuation_record import (
    SECOND_HOP_RULE_AFTER_SLICE12_REANCHOR_STUB,
    build_px2_self_play_second_hop_continuation_artifacts,
)

SLICE13_ORCHESTRATION_PROFILE_ID: Final[str] = "px2_m03_slice13_second_hop_orchestration_v1"

FIRST_HOP_CONTINUATION_SNAPSHOT_JSON: Final[str] = (
    "px2_self_play_first_hop_continuation_snapshot.json"
)
SLICE12_REANCHOR_SNAPSHOT_JSON: Final[str] = "px2_self_play_slice12_reanchor_snapshot.json"
SECOND_HOP_CONTINUATION_JSON: Final[str] = "px2_self_play_second_hop_continuation.json"


def _emit_second_hop_record(
    *,
    root: Path,
    campaign_id: str,
    prior_post_slice12_cc_sha: str,
    prior_first_hop_cont_sha: str,
    prior_slice12_reanchor_sha: str,
    second_hop_run_id: str,
    second_hop_cont_sha: str | None,
    root_cont_sha: str | None,
    prior_man_sha: str,
    updated_man_sha: str | None,
    status: str,
    mismatch_reasons: list[str],
) -> tuple[dict[str, Any], dict[str, Any]]:
    base_non_claims = [
        "Slice-13 bounded second-hop continuation — not industrial campaign.",
        "Repeatability bookkeeping; not PX2-M04 exploit closure; not merge-gate CI proof.",
    ]
    return build_px2_self_play_second_hop_continuation_artifacts(
        campaign_id=campaign_id,
        campaign_profile_id=SLICE13_ORCHESTRATION_PROFILE_ID,
        campaign_root_resolved=root,
        second_hop_rule_id=SECOND_HOP_RULE_AFTER_SLICE12_REANCHOR_STUB,
        prior_post_slice12_current_candidate_sha256=prior_post_slice12_cc_sha,
        prior_first_hop_continuation_run_sha256=prior_first_hop_cont_sha,
        prior_slice12_reanchor_sha256=prior_slice12_reanchor_sha,
        second_hop_continuation_run_id=second_hop_run_id,
        second_hop_continuation_run_sha256=second_hop_cont_sha,
        root_continuation_run_sha256=root_cont_sha,
        prior_campaign_root_manifest_sha256=prior_man_sha,
        updated_campaign_root_manifest_sha256=updated_man_sha,
        second_hop_status=status,
        mismatch_reasons=mismatch_reasons,
        non_claims=base_non_claims,
    )


def validate_post_slice12_state_for_second_hop(
    *,
    campaign_root: Path,
    campaign_id: str,
) -> tuple[bool, list[str]]:
    """Return ``(ok, rejection_reasons)`` for starting a slice-13 second hop."""

    root = campaign_root.resolve()
    reasons: list[str] = []
    cc = load_px2_self_play_current_candidate(root)
    if cc is None:
        return False, ["missing_px2_self_play_current_candidate_json"]
    if str(cc.get("campaign_id", "")) != campaign_id:
        reasons.append("campaign_id_mismatch")
    if (
        str(cc.get("current_candidate_record_version", ""))
        != CURRENT_CANDIDATE_RECORD_VERSION_SLICE12
    ):
        reasons.append("current_candidate_not_post_slice12_reanchor_record_version")
    if str(cc.get("execution_kind", "")) != EXECUTION_KIND_SLICE12:
        reasons.append("current_candidate_execution_kind_not_slice12_reanchor")

    rj = root / CURRENT_CANDIDATE_REANCHOR_JSON
    if not rj.is_file():
        reasons.append("missing_px2_self_play_current_candidate_reanchor_json")
    else:
        rr = cast(dict[str, Any], json.loads(rj.read_text(encoding="utf-8")))
        if str(rr.get("reanchor_status", "")) != "reanchored_ok":
            reasons.append("slice12_reanchor_not_reanchored_ok")

    cp = root / CONTINUATION_RUN_JSON
    if not cp.is_file():
        reasons.append("missing_px2_self_play_continuation_run_json")
    else:
        cr = cast(dict[str, Any], json.loads(cp.read_text(encoding="utf-8")))
        if str(cr.get("consumption_status", "")) != "consumed_ok":
            reasons.append("first_hop_continuation_not_consumed_ok")
        ek = str(cr.get("execution_kind", ""))
        if ek != EXECUTION_KIND_SLICE11:
            reasons.append("first_hop_continuation_execution_kind_not_slice11")

    return (len(reasons) == 0, reasons)


def run_bounded_second_hop_continuation_after_slice12(
    *,
    corpus_root: Path,
    campaign_root: Path,
    campaign_id: str,
    second_hop_continuation_run_id: str = "second_hop_cont",
    init_only: bool = True,
    weights_path: Path | None = None,
    weight_bundle_ref: str | None = None,
    torch_seed: int = 99,
    continuity_step_count: int = 2,
    device_intent: str = "cpu",
    map_location: str = "cpu",
    symmetric_reanchor: bool = True,
) -> dict[str, Any]:
    """Run one bounded second continuation hop; optionally symmetric re-anchor.

    **Not** industrial self-play; **not** **PX2-M04** exploit closure; **not** merge-gate CI.
    """

    root = campaign_root.resolve()
    ok, pre_reasons = validate_post_slice12_state_for_second_hop(
        campaign_root=root,
        campaign_id=campaign_id,
    )
    cc_before = load_px2_self_play_current_candidate(root)
    prior_cc_sha = (
        str(cc_before.get("current_candidate_sha256", "")) if cc_before is not None else ""
    )
    man_path = root / "px2_self_play_campaign_root_manifest.json"
    prior_man_sha = ""
    if man_path.is_file():
        prior_man_sha = str(
            cast(dict[str, Any], json.loads(man_path.read_text(encoding="utf-8"))).get(
                "campaign_root_manifest_sha256", ""
            )
        )

    if not ok:
        sm, sr = _emit_second_hop_record(
            root=root,
            campaign_id=campaign_id,
            prior_post_slice12_cc_sha=prior_cc_sha,
            prior_first_hop_cont_sha="",
            prior_slice12_reanchor_sha="",
            second_hop_run_id=second_hop_continuation_run_id,
            second_hop_cont_sha=None,
            root_cont_sha=None,
            prior_man_sha=prior_man_sha,
            updated_man_sha=None,
            status="rejected",
            mismatch_reasons=pre_reasons,
        )
        write_json(root / SECOND_HOP_CONTINUATION_JSON, sm)
        write_json(root / "px2_self_play_second_hop_continuation_report.json", sr)
        return {
            "campaign_root": str(root),
            "second_hop_status": "rejected",
            "second_hop_continuation_sha256": sm["second_hop_continuation_sha256"],
            "rejection_reasons": pre_reasons,
            "continuation_consumption_status": None,
            "symmetric_reanchor": None,
        }

    first_hop = cast(
        dict[str, Any],
        json.loads((root / CONTINUATION_RUN_JSON).read_text(encoding="utf-8")),
    )
    prior_first_hop_sha = str(first_hop.get("continuation_run_sha256", ""))
    rj = cast(
        dict[str, Any],
        json.loads((root / CURRENT_CANDIDATE_REANCHOR_JSON).read_text(encoding="utf-8")),
    )
    prior_slice12_reanchor_sha = str(rj.get("current_candidate_reanchor_sha256", ""))

    shutil.copy2(root / CONTINUATION_RUN_JSON, root / FIRST_HOP_CONTINUATION_SNAPSHOT_JSON)
    shutil.copy2(root / CURRENT_CANDIDATE_REANCHOR_JSON, root / SLICE12_REANCHOR_SNAPSHOT_JSON)

    inner = run_bounded_continuation_run_consuming_current_candidate(
        corpus_root=corpus_root,
        campaign_root=root,
        campaign_id=campaign_id,
        continuation_run_id=second_hop_continuation_run_id,
        init_only=init_only,
        weights_path=weights_path,
        weight_bundle_ref=weight_bundle_ref,
        torch_seed=torch_seed,
        continuity_step_count=continuity_step_count,
        device_intent=device_intent,
        map_location=map_location,
        execution_kind=EXECUTION_KIND_SLICE13,
        campaign_profile_id=SLICE13_SECOND_HOP_CAMPAIGN_PROFILE_ID,
        continuation_rule_id=CONTINUATION_RULE_SECOND_HOP_CONSUME_CURRENT_CANDIDATE_STUB,
        continuation_run_record_version=CONTINUATION_RUN_RECORD_VERSION_SLICE13,
    )

    root_cont = cast(
        dict[str, Any],
        json.loads((root / CONTINUATION_RUN_JSON).read_text(encoding="utf-8")),
    )
    root_cont_sha = str(root_cont.get("continuation_run_sha256", ""))
    second_hop_sha = root_cont_sha if inner.get("consumption_status") == "consumed_ok" else None
    updated_man_sha = None
    if inner.get("consumption_status") == "consumed_ok":
        updated_man_sha = str(inner.get("updated_campaign_root_manifest_sha256", ""))

    sm, sr = _emit_second_hop_record(
        root=root,
        campaign_id=campaign_id,
        prior_post_slice12_cc_sha=prior_cc_sha,
        prior_first_hop_cont_sha=prior_first_hop_sha,
        prior_slice12_reanchor_sha=prior_slice12_reanchor_sha,
        second_hop_run_id=second_hop_continuation_run_id,
        second_hop_cont_sha=second_hop_sha,
        root_cont_sha=root_cont_sha,
        prior_man_sha=prior_man_sha,
        updated_man_sha=updated_man_sha,
        status="second_hop_ok" if inner.get("consumption_status") == "consumed_ok" else "rejected",
        mismatch_reasons=(
            []
            if inner.get("consumption_status") == "consumed_ok"
            else list(inner.get("mismatch_reasons", []))
        ),
    )
    write_json(root / SECOND_HOP_CONTINUATION_JSON, sm)
    write_json(root / "px2_self_play_second_hop_continuation_report.json", sr)

    reanchor_out: dict[str, Any] | None = None
    if symmetric_reanchor and inner.get("consumption_status") == "consumed_ok":
        reanchor_out = run_bounded_current_candidate_reanchor_after_second_hop(
            campaign_root=root,
            campaign_id=campaign_id,
            prior_first_hop_continuation_run_sha256=prior_first_hop_sha,
            prior_slice12_reanchor_sha256=prior_slice12_reanchor_sha,
        )

    return {
        "campaign_root": str(root),
        "second_hop_status": sm["second_hop_status"],
        "second_hop_continuation_sha256": sm["second_hop_continuation_sha256"],
        "continuation_consumption_status": inner.get("consumption_status"),
        "continuation_run_sha256": root_cont_sha,
        "prior_first_hop_continuation_run_sha256": prior_first_hop_sha,
        "prior_slice12_reanchor_sha256": prior_slice12_reanchor_sha,
        "symmetric_reanchor": reanchor_out,
    }
