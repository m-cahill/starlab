"""Bounded continuation run consuming current-candidate JSON (PX2-M03 slice 11)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Final, cast

from starlab.sc2.px2.self_play.campaign_continuity import (
    EXECUTION_KIND_SLICE11,
    EXECUTION_KIND_SLICE13,
)
from starlab.sc2.px2.self_play.campaign_root import (
    DEFAULT_CAMPAIGN_ROOT_SUBDIRS,
    recommended_operator_out_campaign_root_path,
    run_slice5_operator_local_campaign,
)
from starlab.sc2.px2.self_play.campaign_root_manifest import (
    build_px2_self_play_campaign_root_manifest_artifacts,
)
from starlab.sc2.px2.self_play.continuation_run_record import (
    CONTINUATION_RULE_CONSUME_CURRENT_CANDIDATE_STUB,
    build_px2_self_play_continuation_run_artifacts,
)
from starlab.sc2.px2.self_play.current_candidate import (
    CURRENT_CANDIDATE_JSON,
    load_px2_self_play_current_candidate,
)
from starlab.sc2.px2.self_play.opponent_selection import OPPONENT_SELECTION_ROUND_ROBIN
from starlab.sc2.px2.self_play.run_artifacts import (
    default_operator_local_slice4_subdirs,
    write_json,
)
from starlab.sc2.px2.self_play.weight_loading import WEIGHT_MODE_INIT_ONLY, WEIGHT_MODE_WEIGHTS_FILE

SLICE11_CAMPAIGN_PROFILE_ID: Final[str] = "px2_m03_slice11_continuation_run_v1"
SLICE13_SECOND_HOP_CAMPAIGN_PROFILE_ID: Final[str] = "px2_m03_slice13_second_hop_continuation_v1"

CONTINUATION_RUN_JSON: Final[str] = "px2_self_play_continuation_run.json"


def _load_continuity_run(campaign_root: Path, run_id: str) -> dict[str, Any]:
    p = campaign_root / "runs" / run_id / "px2_self_play_campaign_continuity.json"
    return cast(dict[str, Any], json.loads(p.read_text(encoding="utf-8")))


def validate_current_candidate_for_continuation_run(
    *,
    campaign_root: Path,
    campaign_id: str,
    init_only: bool,
    weights_path: Path | None,
    weight_bundle_ref: str | None,
) -> tuple[dict[str, Any] | None, list[str]]:
    """Return ``(current_candidate_manifest, mismatch_reasons)``.

    When ``mismatch_reasons`` is non-empty, the continuation run must **not** execute.
    """

    errors: list[str] = []
    cc = load_px2_self_play_current_candidate(campaign_root)
    if cc is None:
        return None, ["missing_px2_self_play_current_candidate_json"]

    if str(cc.get("campaign_id", "")) != campaign_id:
        errors.append("campaign_id_mismatch")

    man_path = campaign_root / "px2_self_play_campaign_root_manifest.json"
    if not man_path.is_file():
        errors.append("missing_px2_self_play_campaign_root_manifest_json")
        return cc, errors

    man = cast(dict[str, Any], json.loads(man_path.read_text(encoding="utf-8")))
    if str(cc.get("campaign_contract_sha256", "")) != str(man.get("campaign_contract_sha256", "")):
        errors.append("campaign_contract_sha256_mismatch")
    if str(cc.get("opponent_pool_identity_sha256", "")) != str(
        man.get("opponent_pool_identity_sha256", "")
    ):
        errors.append("opponent_pool_identity_sha256_mismatch")
    if str(cc.get("campaign_root_manifest_sha256", "")) != str(
        man.get("campaign_root_manifest_sha256", "")
    ):
        errors.append("campaign_root_manifest_sha256_mismatch")

    sess_path = campaign_root / "px2_self_play_operator_local_session.json"
    if sess_path.is_file():
        sess = cast(dict[str, Any], json.loads(sess_path.read_text(encoding="utf-8")))
        if str(cc.get("operator_local_session_sha256", "")) != str(
            sess.get("operator_local_session_sha256", "")
        ):
            errors.append("operator_local_session_sha256_mismatch")

    hint = str(cc.get("weight_mode_declared_hint", ""))
    if init_only and hint != WEIGHT_MODE_INIT_ONLY:
        errors.append("weight_mode_hint_mismatch_expected_init_only")
    if not init_only and hint != WEIGHT_MODE_WEIGHTS_FILE:
        errors.append("weight_mode_hint_mismatch_expected_weights_file")
    if init_only and weights_path is not None:
        errors.append("weights_path_forbidden_when_init_only")
    if not init_only and weights_path is None:
        errors.append("weights_path_required_when_not_init_only")

    wb_in = weight_bundle_ref.strip() if weight_bundle_ref else None
    wre = cc.get("weight_bundle_ref")
    wb_cc = str(wre).strip() if wre else None
    if wb_cc != wb_in:
        errors.append("weight_bundle_ref_mismatch")

    anchor = cc.get("anchor")
    if isinstance(anchor, dict):
        arid = str(anchor.get("continuity_run_id", ""))
        if arid:
            cont = _load_continuity_run(campaign_root, arid)
            if cont.get("weight_identity") != cc.get("weight_identity"):
                errors.append("weight_identity_mismatch_vs_anchor_continuity")

    return cc, errors


def merge_campaign_root_manifest_after_continuation_run(
    campaign_root: Path,
    *,
    campaign_id: str,
    new_run_id: str,
    new_continuity_sha256: str,
    opponent_selection_rule_id: str,
    execution_kind: str = EXECUTION_KIND_SLICE11,
) -> tuple[str, dict[str, Any], dict[str, Any]]:
    """Append one run to the sealed campaign-root manifest (slice-11 continuation)."""

    man_path = campaign_root / "px2_self_play_campaign_root_manifest.json"
    man = cast(dict[str, Any], json.loads(man_path.read_text(encoding="utf-8")))
    refs: list[dict[str, str]] = []
    for r in man["continuity_run_references"]:
        if isinstance(r, dict):
            refs.append({str(k): str(v) for k, v in r.items()})
    refs.append(
        {
            "run_id": new_run_id,
            "continuity_sha256": new_continuity_sha256,
            "relative_path": f"runs/{new_run_id}/",
            "run_manifest_relative_path": f"runs/{new_run_id}/run_manifest.json",
        }
    )
    sub4 = default_operator_local_slice4_subdirs()
    root_non_claims = (
        [
            "Slice-13 second-hop bounded continuation run — manifest append; "
            "not industrial campaign.",
            "Not merge-gate default CI proof.",
        ]
        if execution_kind == EXECUTION_KIND_SLICE13
        else [
            "Slice-11 bounded continuation run — manifest append; not industrial campaign.",
            "Not merge-gate default CI proof.",
        ]
    )
    manifest, report = build_px2_self_play_campaign_root_manifest_artifacts(
        campaign_id=campaign_id,
        campaign_contract_sha256=str(man["campaign_contract_sha256"]),
        root_path_expected=recommended_operator_out_campaign_root_path(campaign_id),
        allowed_subdirectories=DEFAULT_CAMPAIGN_ROOT_SUBDIRS,
        run_subdirectory_receipt_layout=dict(sub4),
        continuity_run_references=tuple(refs),
        opponent_pool_identity_sha256=str(man["opponent_pool_identity_sha256"]),
        opponent_selection_rule_id=opponent_selection_rule_id,
        non_claims=root_non_claims,
    )
    write_json(campaign_root / "px2_self_play_campaign_root_manifest.json", manifest)
    write_json(campaign_root / "px2_self_play_campaign_root_manifest_report.json", report)
    return str(manifest["campaign_root_manifest_sha256"]), manifest, report


def run_bounded_continuation_run_consuming_current_candidate(
    *,
    corpus_root: Path,
    campaign_root: Path,
    campaign_id: str,
    continuation_run_id: str,
    init_only: bool = True,
    weights_path: Path | None = None,
    weight_bundle_ref: str | None = None,
    torch_seed: int = 99,
    continuity_step_count: int = 2,
    device_intent: str = "cpu",
    map_location: str = "cpu",
    execution_kind: str = EXECUTION_KIND_SLICE11,
    campaign_profile_id: str = SLICE11_CAMPAIGN_PROFILE_ID,
    continuation_rule_id: str = CONTINUATION_RULE_CONSUME_CURRENT_CANDIDATE_STUB,
    continuation_run_record_version: str | None = None,
) -> dict[str, Any]:
    """One bounded continuity pass under ``campaign_root`` after validating current-candidate JSON.

    **Not** industrial self-play; **not** **PX2-M04** exploit closure; **not** merge-gate CI.
    """

    root = campaign_root.resolve()
    cc, mismatch = validate_current_candidate_for_continuation_run(
        campaign_root=root,
        campaign_id=campaign_id,
        init_only=init_only,
        weights_path=weights_path,
        weight_bundle_ref=weight_bundle_ref,
    )
    if cc is None:
        msg = "current candidate missing"
        raise RuntimeError(msg)

    anchor = cc.get("anchor")
    ck_sha = ""
    if isinstance(anchor, dict):
        ck_sha = str(anchor.get("checkpoint_receipt_sha256", ""))

    prior_man = str(cc.get("campaign_root_manifest_sha256", ""))
    base_non_claims = (
        [
            "Slice-13 second-hop bounded continuation — current-candidate consumption record.",
            "Not industrial execution; not PX2-M04 exploit closure; not ladder strength.",
            "Not merge-gate default CI proof.",
        ]
        if execution_kind == EXECUTION_KIND_SLICE13
        else [
            "Slice-11 bounded continuation run — current-candidate consumption record.",
            "Not industrial execution; not PX2-M04 exploit closure; not ladder strength.",
            "Not merge-gate default CI proof.",
        ]
    )

    def _emit_record(
        *,
        consumption_status: str,
        mismatch_reasons: list[str],
        cont_sha: str | None,
        updated_man_sha: str | None,
    ) -> tuple[dict[str, Any], dict[str, Any]]:
        return build_px2_self_play_continuation_run_artifacts(
            execution_kind=execution_kind,
            campaign_id=campaign_id,
            campaign_profile_id=campaign_profile_id,
            campaign_root_resolved=root,
            continuation_rule_id=continuation_rule_id,
            continuation_run_record_version=continuation_run_record_version,
            current_candidate_sha256=str(cc.get("current_candidate_sha256", "")),
            operator_local_session_sha256=str(cc.get("operator_local_session_sha256", "")),
            operator_local_session_transition_sha256=str(
                cc.get("operator_local_session_transition_sha256", "")
            ),
            campaign_contract_sha256=str(cc.get("campaign_contract_sha256", "")),
            opponent_pool_identity_sha256=str(cc.get("opponent_pool_identity_sha256", "")),
            prior_campaign_root_manifest_sha256=prior_man,
            consumed_checkpoint_receipt_sha256=ck_sha,
            continuation_run_id=continuation_run_id,
            continuation_continuity_sha256=cont_sha,
            consumption_status=consumption_status,
            mismatch_reasons=mismatch_reasons,
            updated_campaign_root_manifest_sha256=updated_man_sha,
            non_claims=base_non_claims,
        )

    if mismatch:
        tm, tr = _emit_record(
            consumption_status="rejected_mismatch",
            mismatch_reasons=mismatch,
            cont_sha=None,
            updated_man_sha=None,
        )
        write_json(root / CONTINUATION_RUN_JSON, tm)
        write_json(root / "px2_self_play_continuation_run_report.json", tr)
        return {
            "campaign_root": str(root),
            "continuation_run_sha256": tm["continuation_run_sha256"],
            "consumption_status": "rejected_mismatch",
            "mismatch_reasons": mismatch,
            "current_candidate_path": str(root / CURRENT_CANDIDATE_JSON),
        }

    inner = run_slice5_operator_local_campaign(
        corpus_root=corpus_root,
        campaign_root=root,
        init_only=init_only,
        weights_path=weights_path,
        weight_bundle_ref=weight_bundle_ref,
        campaign_id=campaign_id,
        campaign_profile_id=campaign_profile_id,
        torch_seed=torch_seed,
        run_id=continuation_run_id,
        continuity_step_count=continuity_step_count,
        device_intent=device_intent,
        map_location=map_location,
        opponent_selection_rule_id=OPPONENT_SELECTION_ROUND_ROBIN,
        execution_kind=execution_kind,
        write_campaign_root_manifest=False,
    )
    cont_sha = str(inner["continuity_sha256"])
    man_path = root / "px2_self_play_campaign_root_manifest.json"
    man_before = cast(dict[str, Any], json.loads(man_path.read_text(encoding="utf-8")))
    opp_rule = str(man_before.get("opponent_selection_rule_id", OPPONENT_SELECTION_ROUND_ROBIN))
    updated_sha, _, _ = merge_campaign_root_manifest_after_continuation_run(
        root,
        campaign_id=campaign_id,
        new_run_id=continuation_run_id,
        new_continuity_sha256=cont_sha,
        opponent_selection_rule_id=opp_rule,
        execution_kind=execution_kind,
    )

    tm_ok, tr_ok = _emit_record(
        consumption_status="consumed_ok",
        mismatch_reasons=[],
        cont_sha=cont_sha,
        updated_man_sha=updated_sha,
    )
    write_json(root / CONTINUATION_RUN_JSON, tm_ok)
    write_json(root / "px2_self_play_continuation_run_report.json", tr_ok)

    return {
        "campaign_root": str(root),
        "continuation_run_sha256": tm_ok["continuation_run_sha256"],
        "consumption_status": "consumed_ok",
        "continuation_run_id": continuation_run_id,
        "continuation_continuity_sha256": cont_sha,
        "updated_campaign_root_manifest_sha256": updated_sha,
        "current_candidate_path": str(root / CURRENT_CANDIDATE_JSON),
    }
