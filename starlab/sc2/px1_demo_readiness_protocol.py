"""Build deterministic px1_demo_readiness_protocol.json + report (PX1-M03)."""

from __future__ import annotations

from typing import Any

from starlab.runs.json_util import sha256_hex_of_canonical_json
from starlab.sc2.px1_demo_readiness_models import (
    PX1_DEMO_READINESS_PROTOCOL_CONTRACT_ID,
    PX1_DEMO_READINESS_PROTOCOL_REPORT_SCHEMA_VERSION,
    PX1_DEMO_READINESS_PROTOCOL_SCHEMA_VERSION,
    PX1_DEMO_READINESS_RUNTIME_DOC_REL_PATH,
    PX1_M03_PROTOCOL_PROFILE_DEMO_READINESS_REMEDIATION_V1,
)


def _as_str(value: Any, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        msg = f"{field} must be a non-empty string"
        raise ValueError(msg)
    return value.strip()


def _as_opt_str(value: Any) -> str | None:
    if value is None:
        return None
    if not isinstance(value, str):
        msg = "optional string fields must be strings or null"
        raise ValueError(msg)
    s = value.strip()
    return s if s else None


def validate_demo_readiness_protocol_input(obj: dict[str, Any]) -> dict[str, Any]:
    """Validate and normalize PX1-M03 demo-readiness protocol input."""

    profile = _as_str(obj.get("protocol_profile_id", ""), "protocol_profile_id")
    if profile != PX1_M03_PROTOCOL_PROFILE_DEMO_READINESS_REMEDIATION_V1:
        msg = (
            f"unsupported protocol_profile_id {profile!r}; only "
            f"{PX1_M03_PROTOCOL_PROFILE_DEMO_READINESS_REMEDIATION_V1!r} is supported in "
            "PX1-M03 v1"
        )
        raise ValueError(msg)

    cid = obj.get("contract_id")
    if cid is not None:
        if cid != PX1_DEMO_READINESS_PROTOCOL_CONTRACT_ID:
            msg = f"contract_id must be {PX1_DEMO_READINESS_PROTOCOL_CONTRACT_ID!r} when set"
            raise ValueError(msg)

    pv = _as_str(obj.get("protocol_version", ""), "protocol_version")
    if pv != PX1_DEMO_READINESS_PROTOCOL_SCHEMA_VERSION:
        msg = f"protocol_version must be {PX1_DEMO_READINESS_PROTOCOL_SCHEMA_VERSION!r}"
        raise ValueError(msg)

    runtime_doc = _as_str(
        obj.get("runtime_doc_rel_path", ""),
        "runtime_doc_rel_path",
    )
    if runtime_doc != PX1_DEMO_READINESS_RUNTIME_DOC_REL_PATH:
        msg = (
            f"runtime_doc_rel_path must be {PX1_DEMO_READINESS_RUNTIME_DOC_REL_PATH!r} for "
            "PX1-M03 v1"
        )
        raise ValueError(msg)

    anchor = obj.get("px1_m01_anchor")
    if not isinstance(anchor, dict):
        msg = "px1_m01_anchor must be an object"
        raise ValueError(msg)
    campaign_id = _as_str(anchor.get("campaign_id", ""), "px1_m01_anchor.campaign_id")
    execution_id = _as_str(anchor.get("execution_id", ""), "px1_m01_anchor.execution_id")
    anchor_norm: dict[str, Any] = {
        "campaign_id": campaign_id,
        "execution_id": execution_id,
    }

    pool_raw = obj.get("candidate_pool")
    if not isinstance(pool_raw, list) or not pool_raw:
        msg = "candidate_pool must be a non-empty array"
        raise ValueError(msg)
    candidate_pool: list[dict[str, Any]] = []
    seen_c: set[str] = set()
    for i, row in enumerate(pool_raw):
        if not isinstance(row, dict):
            msg = f"candidate_pool[{i}] must be an object"
            raise ValueError(msg)
        cand_id = _as_str(row.get("candidate_id", ""), f"candidate_pool[{i}].candidate_id")
        if cand_id in seen_c:
            msg = f"duplicate candidate_id {cand_id!r}"
            raise ValueError(msg)
        seen_c.add(cand_id)
        desc = _as_str(row.get("pool_description", ""), f"candidate_pool[{i}].pool_description")
        rel = _as_str(
            row.get("relative_to_campaign_run", ""),
            f"candidate_pool[{i}].relative_to_campaign_run",
        )
        notes = _as_opt_str(row.get("notes"))
        entry: dict[str, Any] = {
            "candidate_id": cand_id,
            "pool_description": desc,
            "relative_to_campaign_run": rel,
        }
        if notes is not None:
            entry["notes"] = notes
        candidate_pool.append(dict(sorted(entry.items())))
    candidate_pool = sorted(candidate_pool, key=lambda x: x["candidate_id"])

    opp_raw = obj.get("opponent_profiles")
    if not isinstance(opp_raw, list) or len(opp_raw) < 2:
        msg = "opponent_profiles must be an array with at least two profiles"
        raise ValueError(msg)
    opponent_profiles: list[dict[str, Any]] = []
    seen_o: set[str] = set()
    for i, row in enumerate(opp_raw):
        if not isinstance(row, dict):
            msg = f"opponent_profiles[{i}] must be an object"
            raise ValueError(msg)
        oid = _as_str(
            row.get("opponent_profile_id", ""),
            f"opponent_profiles[{i}].opponent_profile_id",
        )
        if oid in seen_o:
            msg = f"duplicate opponent_profile_id {oid!r}"
            raise ValueError(msg)
        seen_o.add(oid)
        posture = _as_str(
            row.get("posture_label", ""),
            f"opponent_profiles[{i}].posture_label",
        )
        mpath = _as_str(
            row.get("match_config_repo_relative_path", ""),
            f"opponent_profiles[{i}].match_config_repo_relative_path",
        )
        nc = _as_str(
            row.get("non_claim", ""),
            f"opponent_profiles[{i}].non_claim",
        )
        oentry: dict[str, Any] = {
            "match_config_repo_relative_path": mpath,
            "non_claim": nc,
            "opponent_profile_id": oid,
            "posture_label": posture,
        }
        opponent_profiles.append(dict(sorted(oentry.items())))
    opponent_profiles = sorted(opponent_profiles, key=lambda x: x["opponent_profile_id"])

    fp_raw = obj.get("frozen_parameters")
    if not isinstance(fp_raw, dict):
        msg = "frozen_parameters must be an object"
        raise ValueError(msg)
    required_fp_keys = (
        "minimum_candidates_evaluated",
        "preferred_candidates_evaluated",
        "minimum_distinct_opponent_profiles",
        "minimum_matches_per_candidate_per_opponent_profile",
        "minimum_total_live_matches_for_selected_candidate",
        "minimum_selected_candidate_overall_win_rate",
        "minimum_selected_candidate_win_count",
        "minimum_replay_backed_wins_for_selected_candidate",
        "minimum_watchable_wins_for_selected_candidate",
        "minimum_evidence_completeness",
        "required_runtime_mode",
        "allowed_continuity_invalidations",
        "selection_rule",
    )
    frozen_parameters: dict[str, Any] = {}
    for key in required_fp_keys:
        if key not in fp_raw:
            msg = f"frozen_parameters missing required key {key!r}"
            raise ValueError(msg)
        val = fp_raw[key]
        if key == "selection_rule":
            frozen_parameters[key] = _as_str(val, f"frozen_parameters.{key}")
        elif key == "minimum_evidence_completeness":
            s = _as_str(val, f"frozen_parameters.{key}")
            if s not in ("complete", "incomplete"):
                msg = f"frozen_parameters.{key} must be 'complete' or 'incomplete'"
                raise ValueError(msg)
            frozen_parameters[key] = s
        elif key == "required_runtime_mode":
            s = _as_str(val, f"frozen_parameters.{key}")
            if s != "local_live_sc2":
                msg = f"frozen_parameters.{key} must be 'local_live_sc2' for PX1-M03 v1"
                raise ValueError(msg)
            frozen_parameters[key] = s
        elif key in (
            "minimum_candidates_evaluated",
            "preferred_candidates_evaluated",
            "minimum_distinct_opponent_profiles",
            "minimum_matches_per_candidate_per_opponent_profile",
            "minimum_total_live_matches_for_selected_candidate",
            "minimum_selected_candidate_win_count",
            "minimum_replay_backed_wins_for_selected_candidate",
            "minimum_watchable_wins_for_selected_candidate",
            "allowed_continuity_invalidations",
        ):
            if not isinstance(val, int) or isinstance(val, bool):
                msg = f"frozen_parameters.{key} must be an integer"
                raise ValueError(msg)
            frozen_parameters[key] = int(val)
        elif key == "minimum_selected_candidate_overall_win_rate":
            if not isinstance(val, (int, float)) or isinstance(val, bool):
                msg = f"frozen_parameters.{key} must be a number"
                raise ValueError(msg)
            frozen_parameters[key] = float(val)

    non_claims_raw = obj.get("non_claims")
    if not isinstance(non_claims_raw, list):
        msg = "non_claims must be an array of strings"
        raise ValueError(msg)
    non_claims = sorted(
        {_as_str(x, f"non_claims[{i}]") for i, x in enumerate(non_claims_raw)},
    )

    protocol: dict[str, Any] = {
        "candidate_pool": candidate_pool,
        "contract_id": PX1_DEMO_READINESS_PROTOCOL_CONTRACT_ID,
        "frozen_parameters": dict(sorted(frozen_parameters.items())),
        "non_claims": non_claims,
        "opponent_profiles": opponent_profiles,
        "protocol_profile_id": profile,
        "protocol_version": pv,
        "px1_m01_anchor": anchor_norm,
        "runtime_doc_rel_path": runtime_doc,
        "schema_version": PX1_DEMO_READINESS_PROTOCOL_SCHEMA_VERSION,
    }
    return dict(sorted(protocol.items()))


def px1_demo_readiness_protocol_bundle(
    *,
    input_obj: dict[str, Any],
    input_sha256: str,
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Return canonical protocol JSON + report."""

    protocol = validate_demo_readiness_protocol_input(input_obj)
    canonical_sha = sha256_hex_of_canonical_json(protocol)
    report: dict[str, Any] = {
        "input_sha256": input_sha256,
        "protocol_canonical_sha256": canonical_sha,
        "schema_version": PX1_DEMO_READINESS_PROTOCOL_REPORT_SCHEMA_VERSION,
    }
    return protocol, dict(sorted(report.items()))
