"""Build deterministic ladder_public_evaluation_protocol.json + report (M59)."""

from __future__ import annotations

from typing import Any

from starlab.runs.json_util import sha256_hex_of_canonical_json
from starlab.sc2.ladder_public_evaluation_models import (
    ALLOWED_EVIDENCE_CLASSES,
    DEFAULT_PROTOCOL_NON_CLAIMS,
    DEFAULT_PROTOCOL_OUT_OF_SCOPE,
    LADDER_PUBLIC_EVALUATION_PROTOCOL_CONTRACT_ID,
    LADDER_PUBLIC_EVALUATION_PROTOCOL_FILENAME,
    LADDER_PUBLIC_EVALUATION_PROTOCOL_REPORT_FILENAME,
    LADDER_PUBLIC_EVALUATION_PROTOCOL_REPORT_SCHEMA_VERSION,
    LADDER_PUBLIC_EVALUATION_PROTOCOL_SCHEMA_VERSION,
    LADDER_PUBLIC_EVALUATION_RUNTIME_DOC_REL_PATH,
    M59_PROTOCOL_PROFILE_SINGLE_CANDIDATE_PUBLIC_EVAL_V1,
    EvaluationSurfaceKind,
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


def validate_protocol_input(obj: dict[str, Any]) -> dict[str, Any]:
    """Validate and normalize protocol input (single subject, bounded profile)."""

    profile = _as_str(obj.get("protocol_profile_id", ""), "protocol_profile_id")
    if profile != M59_PROTOCOL_PROFILE_SINGLE_CANDIDATE_PUBLIC_EVAL_V1:
        msg = (
            f"unsupported protocol_profile_id {profile!r}; "
            f"only {M59_PROTOCOL_PROFILE_SINGLE_CANDIDATE_PUBLIC_EVAL_V1!r} is supported in M59 v1"
        )
        raise ValueError(msg)

    cid = obj.get("contract_id")
    if cid is not None:
        _as_str(cid, "contract_id")
        if cid != LADDER_PUBLIC_EVALUATION_PROTOCOL_CONTRACT_ID:
            msg = f"contract_id must be {LADDER_PUBLIC_EVALUATION_PROTOCOL_CONTRACT_ID!r} when set"
            raise ValueError(msg)

    protocol_version = _as_str(obj.get("protocol_version", ""), "protocol_version")

    subj = obj.get("subject_candidate")
    if not isinstance(subj, dict):
        msg = "subject_candidate must be an object"
        raise ValueError(msg)
    cand_id = _as_str(subj.get("candidate_id", ""), "subject_candidate.candidate_id")
    display_label = _as_opt_str(subj.get("display_label"))
    normalized_subject: dict[str, Any] = {"candidate_id": cand_id}
    if display_label is not None:
        normalized_subject["display_label"] = display_label

    lineage_raw = obj.get("candidate_lineage")
    lineage: list[dict[str, Any]] = []
    if lineage_raw is not None:
        if not isinstance(lineage_raw, list):
            msg = "candidate_lineage must be an array when present"
            raise ValueError(msg)
        for i, row in enumerate(lineage_raw):
            if not isinstance(row, dict):
                msg = f"candidate_lineage[{i}] must be an object"
                raise ValueError(msg)
            prov: dict[str, Any] = {}
            for key in (
                "source_artifact_path",
                "source_contract_id",
                "source_profile_id",
                "source_artifact_sha256",
                "source_run_id",
                "notes",
            ):
                if key in row:
                    v = row[key]
                    if v is None:
                        continue
                    prov[key] = _as_str(v, f"candidate_lineage[{i}].{key}")
            lineage.append(dict(sorted(prov.items())))

    surf = _as_str(obj.get("evaluation_surface_kind", ""), "evaluation_surface_kind")
    if surf not in ("ladder_public", "public_match_set"):
        msg = "evaluation_surface_kind must be 'ladder_public' or 'public_match_set'"
        raise ValueError(msg)
    surface_kind: EvaluationSurfaceKind = surf  # type: ignore[assignment]

    venue = obj.get("venue_descriptor")
    if not isinstance(venue, dict):
        msg = "venue_descriptor must be an object"
        raise ValueError(msg)
    venue_desc: dict[str, Any] = {}
    for k, v in venue.items():
        if not isinstance(k, str):
            msg = "venue_descriptor keys must be strings"
            raise ValueError(msg)
        if isinstance(v, str):
            venue_desc[k] = v.strip()
        elif isinstance(v, (int, float, bool)):
            venue_desc[k] = v
        elif v is None:
            venue_desc[k] = None
        else:
            msg = "venue_descriptor values must be strings, numbers, booleans, or null"
            raise ValueError(msg)
    venue_desc = dict(sorted(venue_desc.items()))

    classes_raw = obj.get("accepted_evidence_classes")
    if not isinstance(classes_raw, list) or not classes_raw:
        msg = "accepted_evidence_classes must be a non-empty array"
        raise ValueError(msg)
    accepted: list[str] = []
    for i, c in enumerate(classes_raw):
        s = _as_str(c, f"accepted_evidence_classes[{i}]")
        if s not in ALLOWED_EVIDENCE_CLASSES:
            msg = f"unknown evidence class {s!r}"
            raise ValueError(msg)
        accepted.append(s)
    accepted_sorted = sorted(set(accepted))

    agg = obj.get("aggregation_rules")
    if not isinstance(agg, dict):
        msg = "aggregation_rules must be an object"
        raise ValueError(msg)
    aggregation_rules = dict(sorted(agg.items()))

    req_nc = obj.get("required_non_claims")
    if req_nc is None:
        non_claims = list(DEFAULT_PROTOCOL_NON_CLAIMS)
    else:
        if not isinstance(req_nc, list):
            msg = "required_non_claims must be an array of strings"
            raise ValueError(msg)
        non_claims = list(DEFAULT_PROTOCOL_NON_CLAIMS)
        for i, line in enumerate(req_nc):
            non_claims.append(_as_str(line, f"required_non_claims[{i}]"))

    oos = obj.get("explicit_out_of_scope")
    if oos is None:
        out_of_scope = list(DEFAULT_PROTOCOL_OUT_OF_SCOPE)
    else:
        if not isinstance(oos, list):
            msg = "explicit_out_of_scope must be an array of strings"
            raise ValueError(msg)
        out_of_scope = list(DEFAULT_PROTOCOL_OUT_OF_SCOPE)
        for i, line in enumerate(oos):
            out_of_scope.append(_as_str(line, f"explicit_out_of_scope[{i}]"))

    return {
        "protocol_profile_id": profile,
        "protocol_version": protocol_version,
        "subject_candidate": normalized_subject,
        "candidate_lineage": lineage,
        "evaluation_surface_kind": surface_kind,
        "venue_descriptor": venue_desc,
        "accepted_evidence_classes": accepted_sorted,
        "aggregation_rules": aggregation_rules,
        "required_non_claims": non_claims,
        "explicit_out_of_scope": out_of_scope,
    }


def build_protocol_artifact(
    *,
    normalized: dict[str, Any],
    input_sha256: str,
) -> dict[str, Any]:
    attribution = {
        "emitter_module": "starlab.sc2.emit_ladder_public_evaluation_protocol",
        "input_canonical_sha256": input_sha256,
        "schema_version": LADDER_PUBLIC_EVALUATION_PROTOCOL_SCHEMA_VERSION,
        "runtime_contract": LADDER_PUBLIC_EVALUATION_RUNTIME_DOC_REL_PATH,
    }
    attribution = dict(sorted(attribution.items()))
    body: dict[str, Any] = {
        "contract_id": LADDER_PUBLIC_EVALUATION_PROTOCOL_CONTRACT_ID,
        "schema_version": LADDER_PUBLIC_EVALUATION_PROTOCOL_SCHEMA_VERSION,
        "runtime_contract": LADDER_PUBLIC_EVALUATION_RUNTIME_DOC_REL_PATH,
        **normalized,
        "generated_attribution": attribution,
    }
    return dict(sorted(body.items()))


def build_protocol_report(*, protocol_obj: dict[str, Any]) -> dict[str, Any]:
    charter_hash = sha256_hex_of_canonical_json(protocol_obj)
    return {
        "schema_version": LADDER_PUBLIC_EVALUATION_PROTOCOL_REPORT_SCHEMA_VERSION,
        "protocol_canonical_sha256": charter_hash,
        "protocol_artifact": LADDER_PUBLIC_EVALUATION_PROTOCOL_FILENAME,
        "report_artifact": LADDER_PUBLIC_EVALUATION_PROTOCOL_REPORT_FILENAME,
        "emitter_module": "starlab.sc2.emit_ladder_public_evaluation_protocol",
        "status": "ok",
        "protocol_profile_id": protocol_obj["protocol_profile_id"],
        "non_claims_preserved": True,
        "m59_boundary": {
            "summary": (
                "M59 packages descriptive public/ladder-shaped evidence only. It does not prove "
                "ladder strength, benchmark integrity, or replay↔execution equivalence."
            ),
            "explicit_non_claim": (
                "This report does not certify performance or statistical strength."
            ),
        },
    }


def ladder_public_evaluation_protocol_bundle(
    *,
    input_obj: dict[str, Any],
    input_sha256: str,
) -> tuple[dict[str, Any], dict[str, Any]]:
    normalized = validate_protocol_input(input_obj)
    protocol = build_protocol_artifact(normalized=normalized, input_sha256=input_sha256)
    report = build_protocol_report(protocol_obj=protocol)
    return protocol, report
