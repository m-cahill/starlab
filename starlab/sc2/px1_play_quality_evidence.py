"""Build deterministic px1_play_quality_evidence.json + report (PX1-M02)."""

from __future__ import annotations

from typing import Any

from starlab.runs.json_util import sha256_hex_of_canonical_json
from starlab.sc2.px1_play_quality_models import (
    PX1_PLAY_QUALITY_EVIDENCE_CONTRACT_ID,
    PX1_PLAY_QUALITY_EVIDENCE_REPORT_SCHEMA_VERSION,
    PX1_PLAY_QUALITY_EVIDENCE_SCHEMA_VERSION,
    PX1_PLAY_QUALITY_PROTOCOL_CONTRACT_ID,
    PX1_PLAY_QUALITY_PROTOCOL_SCHEMA_VERSION,
    PX1_PLAY_QUALITY_RUNTIME_DOC_REL_PATH,
)


def _as_str(value: Any, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        msg = f"{field} must be a non-empty string"
        raise ValueError(msg)
    return value.strip()


def _check_protocol_header(protocol_obj: dict[str, Any]) -> None:
    if protocol_obj.get("contract_id") != PX1_PLAY_QUALITY_PROTOCOL_CONTRACT_ID:
        msg = "protocol contract_id mismatch"
        raise ValueError(msg)
    if protocol_obj.get("schema_version") != PX1_PLAY_QUALITY_PROTOCOL_SCHEMA_VERSION:
        msg = "protocol schema_version mismatch"
        raise ValueError(msg)


def _evaluate_candidate_vs_frozen(
    *,
    fp: dict[str, Any],
    profile_ids: list[str],
    candidate_block: dict[str, Any],
) -> tuple[bool, list[str]]:
    """Return (satisfies_thresholds, failure_reasons)."""

    reasons: list[str] = []
    cand_id = candidate_block.get("candidate_id", "")
    per = candidate_block.get("per_opponent_profile")
    if not isinstance(per, dict):
        reasons.append("per_opponent_profile must be an object")
        return False, reasons

    min_m = int(fp["minimum_matches_per_candidate_per_opponent_profile"])
    for pid in profile_ids:
        row = per.get(pid)
        if not isinstance(row, dict):
            reasons.append(f"missing per_opponent_profile[{pid!r}]")
            continue
        played = int(row.get("matches_played", 0))
        if played < min_m:
            reasons.append(
                f"{cand_id}: matches_played for {pid} is {played}, need >= {min_m}",
            )
        inv = int(row.get("continuity_invalidations", 0))
        max_inv = int(fp["allowed_continuity_invalidations"])
        if inv > max_inv:
            reasons.append(
                f"{cand_id}: continuity_invalidations for {pid} is {inv}, allowed {max_inv}",
            )

    agg = candidate_block.get("aggregate")
    if not isinstance(agg, dict):
        reasons.append("aggregate must be an object")
        return False, reasons

    total_matches = int(agg.get("total_live_matches", 0))
    min_total = int(fp["minimum_total_live_matches_for_selected_candidate"])
    if total_matches < min_total:
        reasons.append(f"total_live_matches {total_matches} < {min_total}")

    wins = int(agg.get("overall_wins", 0))
    min_wins = int(fp["minimum_selected_candidate_win_count"])
    if wins < min_wins:
        reasons.append(f"overall_wins {wins} < {min_wins}")

    rate = float(agg.get("overall_win_rate", 0.0))
    min_rate = float(fp["minimum_selected_candidate_overall_win_rate"])
    if rate + 1e-9 < min_rate:
        reasons.append(f"overall_win_rate {rate} < {min_rate}")

    rb = int(agg.get("replay_backed_wins", 0))
    min_rb = int(fp["minimum_replay_backed_wins_for_selected_candidate"])
    if rb < min_rb:
        reasons.append(f"replay_backed_wins {rb} < {min_rb}")

    ww = int(agg.get("watchable_wins", 0))
    min_ww = int(fp["minimum_watchable_wins_for_selected_candidate"])
    if ww < min_ww:
        reasons.append(f"watchable_wins {ww} < {min_ww}")

    completeness_req = str(fp["minimum_evidence_completeness"])
    observed = str(agg.get("evidence_completeness", "incomplete"))
    if completeness_req == "complete" and observed != "complete":
        reasons.append(f"evidence_completeness {observed!r} != {completeness_req!r}")

    ok = not reasons
    return ok, reasons


def validate_evaluation_input(
    *,
    protocol_obj: dict[str, Any],
    eval_obj: dict[str, Any],
) -> dict[str, Any]:
    """Validate evaluation input shape; return normalized evaluation body."""

    _check_protocol_header(protocol_obj)

    series = _as_str(eval_obj.get("evaluation_series_id", ""), "evaluation_series_id")
    mode = _as_str(
        eval_obj.get("required_runtime_mode_asserted", ""),
        "required_runtime_mode_asserted",
    )
    req = protocol_obj["frozen_parameters"]["required_runtime_mode"]
    if mode != req:
        msg = f"required_runtime_mode_asserted {mode!r} must match protocol {req!r}"
        raise ValueError(msg)

    cands_raw = eval_obj.get("candidates_evaluated")
    if not isinstance(cands_raw, list) or not cands_raw:
        msg = "candidates_evaluated must be a non-empty array"
        raise ValueError(msg)

    min_cand = int(protocol_obj["frozen_parameters"]["minimum_candidates_evaluated"])
    if len(cands_raw) < min_cand:
        msg = (
            f"candidates_evaluated length {len(cands_raw)} < "
            f"minimum_candidates_evaluated {min_cand}"
        )
        raise ValueError(msg)

    profile_ids = [p["opponent_profile_id"] for p in protocol_obj["opponent_profiles"]]
    profile_id_set = set(profile_ids)

    normalized_candidates: list[dict[str, Any]] = []
    for i, block in enumerate(cands_raw):
        if not isinstance(block, dict):
            msg = f"candidates_evaluated[{i}] must be an object"
            raise ValueError(msg)
        cid = _as_str(block.get("candidate_id", ""), f"candidates_evaluated[{i}].candidate_id")
        per = block.get("per_opponent_profile")
        if not isinstance(per, dict):
            msg = f"candidates_evaluated[{i}].per_opponent_profile must be an object"
            raise ValueError(msg)
        if set(per.keys()) != profile_id_set:
            msg = (
                f"candidates_evaluated[{i}].per_opponent_profile keys must match "
                "protocol profiles"
            )
            raise ValueError(msg)
        per_norm: dict[str, Any] = {}
        for pid in sorted(per.keys()):
            row = per[pid]
            if not isinstance(row, dict):
                msg = f"per_opponent_profile[{pid!r}] must be an object"
                raise ValueError(msg)
            per_norm[pid] = dict(
                sorted(
                    {
                        "continuity_invalidations": int(row.get("continuity_invalidations", 0)),
                        "matches_played": int(row.get("matches_played", 0)),
                        "replay_backed_wins": int(row.get("replay_backed_wins", 0)),
                        "watchable_wins": int(row.get("watchable_wins", 0)),
                        "wins": int(row.get("wins", 0)),
                    }.items(),
                ),
            )
        agg = block.get("aggregate")
        if not isinstance(agg, dict):
            msg = f"candidates_evaluated[{i}].aggregate must be an object"
            raise ValueError(msg)
        agg_norm = dict(
            sorted(
                {
                    "evidence_completeness": _as_str(
                        agg.get("evidence_completeness", ""),
                        f"candidates_evaluated[{i}].aggregate.evidence_completeness",
                    ),
                    "overall_win_rate": float(agg.get("overall_win_rate", 0.0)),
                    "overall_wins": int(agg.get("overall_wins", 0)),
                    "replay_backed_wins": int(agg.get("replay_backed_wins", 0)),
                    "total_live_matches": int(agg.get("total_live_matches", 0)),
                    "watchable_wins": int(agg.get("watchable_wins", 0)),
                }.items(),
            ),
        )
        normalized_candidates.append(
            dict(
                sorted(
                    {
                        "aggregate": agg_norm,
                        "candidate_id": cid,
                        "per_opponent_profile": dict(sorted(per_norm.items())),
                    }.items(),
                ),
            ),
        )
    normalized_candidates = sorted(normalized_candidates, key=lambda x: x["candidate_id"])

    sel = eval_obj.get("selection")
    if not isinstance(sel, dict):
        msg = "selection must be an object"
        raise ValueError(msg)
    status = _as_str(sel.get("status", ""), "selection.status")
    if status not in ("candidate-selected", "not_selected_within_scope"):
        msg = "selection.status must be candidate-selected|not_selected_within_scope"
        raise ValueError(msg)
    rationale = _as_str(sel.get("rationale", ""), "selection.rationale")
    selected_id = sel.get("selected_candidate_id")
    if status == "candidate-selected":
        if not isinstance(selected_id, str) or not selected_id.strip():
            msg = "selection.selected_candidate_id required when status is candidate-selected"
            raise ValueError(msg)
        selected_id = selected_id.strip()
    elif selected_id is not None:
        if not isinstance(selected_id, str):
            msg = "selection.selected_candidate_id must be a string or null"
            raise ValueError(msg)
        selected_id = selected_id.strip() if selected_id else None

    selection_norm: dict[str, Any] = {
        "rationale": rationale,
        "status": status,
    }
    if selected_id is not None:
        selection_norm["selected_candidate_id"] = selected_id
    selection_norm = dict(sorted(selection_norm.items()))

    return {
        "candidates_evaluated": normalized_candidates,
        "evaluation_series_id": series,
        "required_runtime_mode_asserted": mode,
        "selection": selection_norm,
    }


def px1_play_quality_evidence_bundle(
    *,
    protocol_obj: dict[str, Any],
    evaluation_input_obj: dict[str, Any],
    evaluation_input_sha256: str,
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Return evidence JSON + report with threshold checks."""

    _check_protocol_header(protocol_obj)
    protocol_sha = sha256_hex_of_canonical_json(protocol_obj)
    fp = protocol_obj["frozen_parameters"]
    profile_ids = [p["opponent_profile_id"] for p in protocol_obj["opponent_profiles"]]

    normalized = validate_evaluation_input(
        protocol_obj=protocol_obj,
        eval_obj=evaluation_input_obj,
    )

    threshold_results: list[dict[str, Any]] = []
    for block in normalized["candidates_evaluated"]:
        ok, reasons = _evaluate_candidate_vs_frozen(
            fp=fp,
            profile_ids=profile_ids,
            candidate_block=block,
        )
        threshold_results.append(
            {
                "candidate_id": block["candidate_id"],
                "failure_reasons": reasons,
                "satisfies_frozen_thresholds": ok,
            },
        )

    sel_status = normalized["selection"]["status"]
    selected_id = normalized["selection"].get("selected_candidate_id")

    selection_consistent = True
    consistency_notes: list[str] = []
    if sel_status == "candidate-selected":
        if not selected_id:
            selection_consistent = False
            consistency_notes.append("status candidate-selected but no selected_candidate_id")
        else:
            match_blocks = [
                b for b in normalized["candidates_evaluated"] if b["candidate_id"] == selected_id
            ]
            if len(match_blocks) != 1:
                selection_consistent = False
                consistency_notes.append("selected_candidate_id not found exactly once")
            else:
                ok = next(
                    tr["satisfies_frozen_thresholds"]
                    for tr in threshold_results
                    if tr["candidate_id"] == selected_id
                )
                if not ok:
                    selection_consistent = False
                    consistency_notes.append(
                        "candidate-selected but selected candidate does not satisfy "
                        "frozen thresholds",
                    )
    elif sel_status == "not_selected_within_scope" and selected_id:
        selection_consistent = False
        consistency_notes.append("not_selected_within_scope but selected_candidate_id is set")

    evidence_body: dict[str, Any] = {
        "contract_id": PX1_PLAY_QUALITY_EVIDENCE_CONTRACT_ID,
        "evaluation": normalized,
        "generated_attribution": {
            "protocol_canonical_sha256": protocol_sha,
            "protocol_contract_id": PX1_PLAY_QUALITY_PROTOCOL_CONTRACT_ID,
            "runtime_doc_rel_path": PX1_PLAY_QUALITY_RUNTIME_DOC_REL_PATH,
        },
        "px1_m01_anchor": dict(sorted(protocol_obj["px1_m01_anchor"].items())),
        "schema_version": PX1_PLAY_QUALITY_EVIDENCE_SCHEMA_VERSION,
        "threshold_evaluation": sorted(threshold_results, key=lambda x: x["candidate_id"]),
    }
    evidence = dict(sorted(evidence_body.items()))
    evidence_sha = sha256_hex_of_canonical_json(evidence)

    report: dict[str, Any] = {
        "evaluation_input_sha256": evaluation_input_sha256,
        "evidence_canonical_sha256": evidence_sha,
        "schema_version": PX1_PLAY_QUALITY_EVIDENCE_REPORT_SCHEMA_VERSION,
        "selection_consistent_with_thresholds": selection_consistent,
        "selection_consistency_notes": sorted(consistency_notes),
    }
    return evidence, dict(sorted(report.items()))
