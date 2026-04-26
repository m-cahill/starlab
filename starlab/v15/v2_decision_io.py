"""Build, seal, and write V15-M13 v2 go/no-go decision JSON + report + Markdown brief."""

from __future__ import annotations

import json
from collections.abc import Mapping
from pathlib import Path
from typing import Any, Final

from starlab.runs.json_util import canonical_json_dumps, sha256_hex_of_canonical_json
from starlab.v15.checkpoint_evaluation_models import (
    CONTRACT_ID_CHECKPOINT_PROMOTION_DECISION,
    PROMOTION_STATUS_PROMOTED_CANDIDATE,
    PROMOTION_STATUS_PROMOTED_XAI,
)
from starlab.v15.checkpoint_lineage_models import CONTRACT_ID_CHECKPOINT_LINEAGE
from starlab.v15.human_panel_benchmark_io import redact_path_and_contact_in_value
from starlab.v15.human_panel_execution_models import CONTRACT_ID_HUMAN_BENCHMARK_CLAIM_DECISION
from starlab.v15.long_gpu_training_manifest_models import CONTRACT_ID_LONG_GPU_CAMPAIGN_RECEIPT
from starlab.v15.showcase_release_models import CONTRACT_ID_SHOWCASE_AGENT_RELEASE_PACK
from starlab.v15.strong_agent_scorecard_models import CONTRACT_ID_STRONG_AGENT_SCORECARD
from starlab.v15.training_run_receipt_io import _redaction_token_count, redact_receipt_value
from starlab.v15.v2_decision_models import (
    CONTRACT_ID_V2_DECISION_OPERATOR_EVIDENCE_DECLARED,
    CONTRACT_ID_V2_GO_NO_GO_DECISION,
    CONTRACT_VERSION,
    D0_ARTIFACT_INTEGRITY,
    D1_M12_RELEASE_PACK_BINDING,
    D2_CAMPAIGN_EVIDENCE_GATE,
    D3_CHECKPOINT_PROMOTION_GATE,
    D4_STRONG_AGENT_BENCHMARK_GATE,
    D5_XAI_EVIDENCE_GATE,
    D6_HUMAN_BENCHMARK_GATE,
    D7_RIGHTS_AND_REGISTER_GATE,
    D8_PUBLIC_PRIVATE_BOUNDARY_GATE,
    D9_CLAIM_BOUNDARY_GATE,
    D10_REPRODUCIBILITY_GATE,
    D11_AUDIT_POSTURE_GATE,
    D12_OPEN_RISK_DISPOSITION_GATE,
    D13_V2_RECHARTER_SCOPE_GATE,
    D14_NON_CLAIM_BOUNDARY_GATE,
    EMITTER_MODULE_V2_DECISION,
    FILENAME_V2_GO_NO_GO_DECISION,
    FILENAME_V2_GO_NO_GO_DECISION_BRIEF_MD,
    FIXTURE_V2_DECISION_ID,
    GATE_STATUS_BLOCKED,
    GATE_STATUS_NOT_EVALUATED,
    GATE_STATUS_PASS,
    GATE_STATUS_WARNING,
    MILESTONE_ID_V15_M13,
    NON_CLAIMS_V15_M13,
    OPERATOR_V2_DECISION_EVIDENCE_ALLOWED_KEYS,
    OUTCOME_NO_GO,
    OUTCOME_PROCEED_TO_V2,
    PLACEHOLDER_SHA256,
    PROFILE_FIXTURE_CI,
    PROFILE_ID_V2_GO_NO_GO_DECISION,
    PROFILE_OPERATOR_DECLARED,
    PROFILE_OPERATOR_PREFLIGHT,
    RECOMMENDED_NEXT_STEP_COLLECT,
    REPORT_FILENAME_V2_GO_NO_GO_DECISION,
    REPORT_VERSION_V2_DECISION,
    SEAL_KEY_V2_GO_NO_GO_DECISION,
    STATUS_BLOCKED_MISSING_SHOWCASE_RELEASE_AUTHORIZATION,
    STATUS_BLOCKED_MISSING_SHOWCASE_RELEASE_PACK,
    STATUS_FIXTURE_DECISION_ONLY,
    STATUS_NO_GO_INSUFFICIENT_EVIDENCE,
    STATUS_PROCEED_TO_V2_AUTHORIZED,
    default_m13_authorization_flags,
)
from starlab.v15.xai_demonstration_models import (
    CONTRACT_ID_REPLAY_NATIVE_XAI_DEMONSTRATION,
    DEMONSTRATION_STATUS_OPERATOR_DECLARED_PACK,
)

_SEAL = SEAL_KEY_V2_GO_NO_GO_DECISION

FORBIDDEN_BRIEF_SUBSTRINGS: Final[tuple[str, ...]] = (
    "v2 is authorized",
    "STARLAB has released a showcase agent",
    "the agent is strong",
    "the agent beats most humans",
    "the checkpoint is promoted",
    "the XAI is faithful",
)


def _json_file_canonical_sha256(path: Path) -> str:
    raw = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ValueError("JSON must be a single object")
    return sha256_hex_of_canonical_json(raw)


def _optional_path_sha(optional_paths: Mapping[str, Path | None], field: str) -> str:
    p = optional_paths.get(field)
    if p is None:
        return PLACEHOLDER_SHA256
    return _json_file_canonical_sha256(p)


def _require_contract(obj: dict[str, Any], expected: str, ctx: str) -> None:
    if str(obj.get("contract_id", "")) != expected:
        raise ValueError(
            f"{ctx}: contract_id must be {expected!r} (got {obj.get('contract_id')!r})"
        )


def redact_v2_decision_value(obj: Any) -> Any:
    return redact_receipt_value(redact_path_and_contact_in_value(obj))


def _parse_decision_evidence(path: Path) -> dict[str, Any]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ValueError("decision evidence JSON must be a single object")
    unknown = set(raw) - OPERATOR_V2_DECISION_EVIDENCE_ALLOWED_KEYS
    if unknown:
        raise ValueError(f"decision evidence: unknown keys {sorted(unknown)}")
    _require_contract(raw, CONTRACT_ID_V2_DECISION_OPERATOR_EVIDENCE_DECLARED, "decision_evidence")
    eid = raw.get("evidence_bundle_id")
    if not isinstance(eid, str) or not eid.strip():
        raise ValueError("decision evidence: evidence_bundle_id required")
    for key in (
        "rights_clearance_operator_declared",
        "v2_recharter_scope_declared",
    ):
        v = raw.get(key)
        if v is not None and not isinstance(v, bool):
            raise ValueError(f"decision evidence: {key} must be bool or omitted")
    return raw


def _row(gate_id: str, status: str, notes: str) -> dict[str, Any]:
    return {"gate_id": gate_id, "status": status, "notes": notes}


def _fixture_decision_gates() -> list[dict[str, Any]]:
    gp, gb, gw, ne = (
        GATE_STATUS_PASS,
        GATE_STATUS_BLOCKED,
        GATE_STATUS_WARNING,
        GATE_STATUS_NOT_EVALUATED,
    )
    return [
        _row(D0_ARTIFACT_INTEGRITY, gp, "Fixture decision: deterministic schema; sealed."),
        _row(
            D1_M12_RELEASE_PACK_BINDING,
            gb,
            "No M12 showcase release-pack JSON bound on default fixture path.",
        ),
        _row(
            D2_CAMPAIGN_EVIDENCE_GATE,
            gb,
            "No M08 long GPU campaign receipt evidence bound for v2 decision.",
        ),
        _row(
            D3_CHECKPOINT_PROMOTION_GATE,
            gb,
            "No promoted checkpoint evidence satisfies v2 decision gates on fixture path.",
        ),
        _row(
            D4_STRONG_AGENT_BENCHMARK_GATE,
            gb,
            "Strong-agent benchmark execution + claim not evidenced for v2.",
        ),
        _row(
            D5_XAI_EVIDENCE_GATE,
            gb,
            "Replay-native XAI demonstration is fixture-only; no faithful inference proof.",
        ),
        _row(
            D6_HUMAN_BENCHMARK_GATE,
            gb,
            "Human-benchmark claim not authorized on default public path.",
        ),
        _row(
            D7_RIGHTS_AND_REGISTER_GATE,
            gb,
            "Rights / register clearance for v2-scale publication not established.",
        ),
        _row(D8_PUBLIC_PRIVATE_BOUNDARY_GATE, gp, "Fixture output contains no absolute paths."),
        _row(
            D9_CLAIM_BOUNDARY_GATE,
            gp,
            "Non-claim vocabulary present; no default public performance authorization.",
        ),
        _row(
            D10_REPRODUCIBILITY_GATE,
            gw,
            "Upstream SHA cross-checks are placeholders on fixture path.",
        ),
        _row(D11_AUDIT_POSTURE_GATE, gp, "Governed artifact shape only; no audit weakening."),
        _row(
            D12_OPEN_RISK_DISPOSITION_GATE,
            ne,
            "Open-risk disposition not evaluated on fixture-only path.",
        ),
        _row(
            D13_V2_RECHARTER_SCOPE_GATE,
            gb,
            "v2 recharter scope not satisfied; insufficient governed evidence package.",
        ),
        _row(
            D14_NON_CLAIM_BOUNDARY_GATE,
            gp,
            "Fixture validates non-claim boundary; does not authorize v2.",
        ),
    ]


def _load_m12(path: Path) -> dict[str, Any]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ValueError("M12 JSON must be a single object")
    _require_contract(raw, CONTRACT_ID_SHOWCASE_AGENT_RELEASE_PACK, "m12_release_pack")
    return raw


_UPSTREAM_SPECS: Final[tuple[tuple[str, str, str], ...]] = (
    ("m08_campaign_receipt", CONTRACT_ID_LONG_GPU_CAMPAIGN_RECEIPT, "m08_campaign_receipt"),
    ("m09_promotion_decision", CONTRACT_ID_CHECKPOINT_PROMOTION_DECISION, "m09_promotion"),
    ("m10_xai_demonstration", CONTRACT_ID_REPLAY_NATIVE_XAI_DEMONSTRATION, "m10_xai_demo"),
    ("m11_human_benchmark_claim", CONTRACT_ID_HUMAN_BENCHMARK_CLAIM_DECISION, "m11_claim"),
    ("m05_strong_agent_scorecard", CONTRACT_ID_STRONG_AGENT_SCORECARD, "m05_scorecard"),
    ("m03_checkpoint_lineage", CONTRACT_ID_CHECKPOINT_LINEAGE, "m03_lineage"),
)

_BINDING_KEY_BY_FIELD: Final[dict[str, str]] = {
    "m08_campaign_receipt": "m08_campaign_receipt_json_canonical_sha256",
    "m09_promotion_decision": "m09_promotion_decision_json_canonical_sha256",
    "m10_xai_demonstration": "m10_replay_native_xai_demonstration_json_canonical_sha256",
    "m11_human_benchmark_claim": "m11_human_benchmark_claim_decision_json_canonical_sha256",
    "m05_strong_agent_scorecard": "m05_strong_agent_scorecard_json_canonical_sha256",
    "m03_checkpoint_lineage": "m03_checkpoint_lineage_manifest_json_canonical_sha256",
}


def verify_upstream_cross_checks(
    m12: dict[str, Any],
    paths: Mapping[str, Path | None],
) -> tuple[int, list[str]]:
    """Return (matched_count, error_messages). Raises ValueError on contract/SHA mismatch."""
    ub = m12.get("upstream_bindings")
    if not isinstance(ub, dict):
        raise ValueError("m12_release_pack: upstream_bindings missing")
    matched = 0
    notes: list[str] = []
    for field, contract_id, ctx in _UPSTREAM_SPECS:
        p = paths.get(field)
        if p is None:
            continue
        key = _BINDING_KEY_BY_FIELD[field]
        expected = ub.get(key)
        if not isinstance(expected, str):
            raise ValueError(f"m12_release_pack: missing binding {key!r}")
        obj = json.loads(p.read_text(encoding="utf-8"))
        if not isinstance(obj, dict):
            raise ValueError(f"{ctx}: JSON must be an object")
        _require_contract(obj, contract_id, ctx)
        got = sha256_hex_of_canonical_json(obj)
        if got != expected:
            raise ValueError(
                f"{ctx}: canonical SHA-256 mismatch (file does not match M12 binding for {key})"
            )
        matched += 1
        notes.append(f"{field}: sha_ok")
    return matched, notes


def _summaries_from_m12(m12: dict[str, Any]) -> dict[str, Any]:
    us = m12.get("upstream_summaries")
    if not isinstance(us, dict):
        us = {}
    af = m12.get("authorization_flags")
    af_d: dict[str, Any] = af if isinstance(af, dict) else {}
    return {
        "m08_campaign_completion": str(us.get("m08_campaign_completion", "")),
        "m09_promotion_status": str(us.get("m09_promotion_status", "")),
        "m10_demonstration_status": str(us.get("m10_demonstration_status", "")),
        "m11_claim_authorized": bool(us.get("m11_claim_authorized")),
        "m05_benchmark_executed": bool(us.get("m05_benchmark_executed")),
        "showcase_release_authorized": bool(af_d.get("showcase_agent_release_authorized")),
        "showcase_release_status": str(m12.get("showcase_release_status", "")),
    }


def _all_v2_prerequisites(m12: dict[str, Any]) -> bool:
    if not _summaries_from_m12(m12)["showcase_release_authorized"]:
        return False
    us = m12.get("upstream_summaries")
    if not isinstance(us, dict):
        return False
    if us.get("m08_campaign_completion") != "valid_receipt":
        return False
    promo = str(us.get("m09_promotion_status", ""))
    if promo not in (PROMOTION_STATUS_PROMOTED_CANDIDATE, PROMOTION_STATUS_PROMOTED_XAI):
        return False
    if str(us.get("m10_demonstration_status", "")) != DEMONSTRATION_STATUS_OPERATOR_DECLARED_PACK:
        return False
    if not us.get("m11_claim_authorized"):
        return False
    if not us.get("m05_benchmark_executed"):
        return False
    af = m12.get("authorization_flags")
    if not isinstance(af, dict):
        return False
    for k in (
        "strong_agent_claim_authorized",
        "human_benchmark_claim_authorized",
        "rights_clearance_for_public_release",
        "ladder_claim_authorized",
    ):
        if not af.get(k):
            return False
    for g in m12.get("release_gates") or []:
        if isinstance(g, dict) and g.get("status") == GATE_STATUS_BLOCKED:
            return False
    return True


def _compute_authorization_flags(
    m12: dict[str, Any] | None,
    *,
    operator_evidence: dict[str, Any] | None,
    prerequisites_met: bool,
) -> dict[str, bool]:
    out = default_m13_authorization_flags()
    if m12 is None:
        return out
    af12_raw = m12.get("authorization_flags")
    af12: dict[str, Any] = af12_raw if isinstance(af12_raw, dict) else {}
    out["showcase_agent_release_authorized"] = bool(af12.get("showcase_agent_release_authorized"))
    out["public_showcase_claim_authorized"] = bool(af12.get("public_showcase_claim_authorized"))
    out["strong_agent_claim_authorized"] = bool(af12.get("strong_agent_claim_authorized"))
    out["human_benchmark_claim_authorized"] = bool(af12.get("human_benchmark_claim_authorized"))
    out["ladder_claim_authorized"] = bool(af12.get("ladder_claim_authorized"))
    scope = False
    rights_ev = False
    if operator_evidence:
        scope = bool(operator_evidence.get("v2_recharter_scope_declared"))
        rc = operator_evidence.get("rights_clearance_operator_declared")
        rights_ev = bool(rc) if isinstance(rc, bool) else False
        out["operator_evidence_sufficient"] = True
    pub_rights = bool(af12.get("rights_clearance_for_public_release"))
    out["rights_clearance_for_v2"] = pub_rights or rights_ev
    if operator_evidence is not None:
        out["v2_authorized"] = bool(prerequisites_met and scope and rights_ev and pub_rights)
        out["v2_recharter_authorized"] = out["v2_authorized"]
    return out


def _gates_with_m12(
    m12: dict[str, Any] | None,
    *,
    profile: str,
    cross_matched: int,
    cross_attempted: int,
    prerequisites_met: bool,
) -> list[dict[str, Any]]:
    gp, gb, gw, ne = (
        GATE_STATUS_PASS,
        GATE_STATUS_BLOCKED,
        GATE_STATUS_WARNING,
        GATE_STATUS_NOT_EVALUATED,
    )
    if m12 is None:
        return _fixture_decision_gates()

    summ = _summaries_from_m12(m12)
    m08_ok = summ["m08_campaign_completion"] == "valid_receipt"
    promo = summ["m09_promotion_status"]
    promo_ok = promo in (PROMOTION_STATUS_PROMOTED_CANDIDATE, PROMOTION_STATUS_PROMOTED_XAI)
    xai_ok = summ["m10_demonstration_status"] == DEMONSTRATION_STATUS_OPERATOR_DECLARED_PACK
    h_ok = summ["m11_claim_authorized"]
    bench_ok = summ["m05_benchmark_executed"]
    showcase_auth = summ["showcase_release_authorized"]

    d1 = gp
    d1n = "M12 showcase release-pack JSON bound by canonical SHA-256; contract validated."
    d2 = gp if m08_ok else gb
    d2n = (
        "M08 upstream summary records valid long-campaign receipt binding."
        if m08_ok
        else "M08 campaign evidence gate blocked (receipt not valid per M12 summary)."
    )
    d3 = gp if promo_ok else gb
    d3n = (
        "M09 promotion status allows downstream routing per M12 summary."
        if promo_ok
        else f"M09 promotion gate blocked (promotion_status={promo!r})."
    )
    d4 = gp if bench_ok else gb
    d4n = (
        "M05 benchmark executed per M12 upstream summary."
        if bench_ok
        else "Strong-agent benchmark gate blocked (M05 not executed per M12 summary)."
    )
    d5 = gp if xai_ok else gb
    d5n = (
        "M10 demonstration status is operator-declared pack (still not inference proof)."
        if xai_ok
        else "XAI evidence gate blocked (M10 demonstration not operator-declared pack)."
    )
    d6 = gp if h_ok else gb
    d6n = (
        "M11 authorizes bounded human-benchmark claim per M12 summary."
        if h_ok
        else "Human-benchmark gate blocked (M11 claim not authorized per M12 summary)."
    )
    d7 = gp if showcase_auth else gb
    d7n = (
        "M12 authorization flags record showcase release authorization."
        if showcase_auth
        else "Rights/register gate blocked (showcase release not authorized in M12 flags)."
    )
    d8 = gp
    d8n = "Emitter redacts path-like and contact-like values in operator-declared fields."
    d9 = gp
    d9n = "Claim boundary preserved; v2 remains blocked unless all prerequisites and evidence pass."
    if cross_attempted == 0:
        d10 = gw
        d10n = "Optional upstream JSON files not supplied; reproducibility limited to M12 seal."
    else:
        d10 = gp
        d10n = "Supplied upstream JSON files match M12 canonical SHA-256 bindings."
    d11 = gp
    d11n = "Fixture/operator profiles do not weaken Ruff/mypy/pytest/governance posture."
    d12 = ne if profile == PROFILE_OPERATOR_PREFLIGHT else gw
    d12n = (
        "Open-risk disposition requires explicit operator record outside this emitter."
        if profile == PROFILE_OPERATOR_PREFLIGHT
        else "Operator-declared evidence may reference risk posture; not evaluated as proof."
    )
    d13 = gp if prerequisites_met else gb
    d13n = (
        "All M12 upstream summaries, authorization flags, and release gates allow v2 routing."
        if prerequisites_met
        else "v2 recharter scope gate blocked (M12 evidence package insufficient)."
    )
    d14 = gp
    d14n = "Non-claim boundary explicit; default path does not authorize public performance."

    return [
        _row(D0_ARTIFACT_INTEGRITY, gp, "M12 JSON parsed; primary binding established."),
        _row(D1_M12_RELEASE_PACK_BINDING, d1, d1n),
        _row(D2_CAMPAIGN_EVIDENCE_GATE, d2, d2n),
        _row(D3_CHECKPOINT_PROMOTION_GATE, d3, d3n),
        _row(D4_STRONG_AGENT_BENCHMARK_GATE, d4, d4n),
        _row(D5_XAI_EVIDENCE_GATE, d5, d5n),
        _row(D6_HUMAN_BENCHMARK_GATE, d6, d6n),
        _row(D7_RIGHTS_AND_REGISTER_GATE, d7, d7n),
        _row(D8_PUBLIC_PRIVATE_BOUNDARY_GATE, d8, d8n),
        _row(D9_CLAIM_BOUNDARY_GATE, d9, d9n),
        _row(D10_REPRODUCIBILITY_GATE, d10, d10n),
        _row(D11_AUDIT_POSTURE_GATE, d11, d11n),
        _row(D12_OPEN_RISK_DISPOSITION_GATE, d12, d12n),
        _row(D13_V2_RECHARTER_SCOPE_GATE, d13, d13n),
        _row(D14_NON_CLAIM_BOUNDARY_GATE, d14, d14n),
    ]


def _secondary_statuses(
    m12: dict[str, Any] | None,
    *,
    prerequisites_met: bool,
    auth_flags: dict[str, bool],
) -> list[str]:
    out: list[str] = []
    if m12 is None:
        out.append(STATUS_BLOCKED_MISSING_SHOWCASE_RELEASE_PACK)
        out.append(STATUS_NO_GO_INSUFFICIENT_EVIDENCE)
        return out
    if not auth_flags["showcase_agent_release_authorized"]:
        out.append(STATUS_BLOCKED_MISSING_SHOWCASE_RELEASE_AUTHORIZATION)
    summ = _summaries_from_m12(m12)
    if summ["m08_campaign_completion"] != "valid_receipt":
        out.append("blocked_missing_m08_campaign_receipt")
    promo = summ["m09_promotion_status"]
    if promo not in (PROMOTION_STATUS_PROMOTED_CANDIDATE, PROMOTION_STATUS_PROMOTED_XAI):
        out.append("blocked_missing_promoted_checkpoint")
    if not summ["m05_benchmark_executed"]:
        out.append("blocked_missing_strong_agent_benchmark")
    if summ["m10_demonstration_status"] != DEMONSTRATION_STATUS_OPERATOR_DECLARED_PACK:
        out.append("blocked_missing_xai_demonstration")
    if not summ["m11_claim_authorized"]:
        out.append("blocked_missing_human_benchmark_claim")
    if not auth_flags["rights_clearance_for_v2"]:
        out.append("blocked_missing_rights_clearance")
    if not prerequisites_met:
        out.append(STATUS_NO_GO_INSUFFICIENT_EVIDENCE)
    return out


def _decision_status_primary(
    m12: dict[str, Any] | None,
    *,
    v2_authorized: bool,
) -> str:
    if v2_authorized:
        return STATUS_PROCEED_TO_V2_AUTHORIZED
    if m12 is None:
        return STATUS_FIXTURE_DECISION_ONLY
    return STATUS_FIXTURE_DECISION_ONLY


def build_v2_decision_body_fixture() -> dict[str, Any]:
    af = default_m13_authorization_flags()
    return {
        "contract_id": CONTRACT_ID_V2_GO_NO_GO_DECISION,
        "contract_version": CONTRACT_VERSION,
        "milestone_id": MILESTONE_ID_V15_M13,
        "profile_id": PROFILE_ID_V2_GO_NO_GO_DECISION,
        "emit_profile": PROFILE_FIXTURE_CI,
        "emitter_module": EMITTER_MODULE_V2_DECISION,
        "v2_decision_id": FIXTURE_V2_DECISION_ID,
        "v2_decision_status": STATUS_FIXTURE_DECISION_ONLY,
        "v2_decision_status_secondary": [
            STATUS_NO_GO_INSUFFICIENT_EVIDENCE,
            STATUS_BLOCKED_MISSING_SHOWCASE_RELEASE_PACK,
            STATUS_BLOCKED_MISSING_SHOWCASE_RELEASE_AUTHORIZATION,
        ],
        "decision_outcome": OUTCOME_NO_GO,
        "recommended_next_step": RECOMMENDED_NEXT_STEP_COLLECT,
        "m12_showcase_release_pack_json_canonical_sha256": PLACEHOLDER_SHA256,
        "optional_upstream_crosscheck": {
            "m08_campaign_receipt_json_canonical_sha256": PLACEHOLDER_SHA256,
            "m09_promotion_decision_json_canonical_sha256": PLACEHOLDER_SHA256,
            "m10_replay_native_xai_demonstration_json_canonical_sha256": PLACEHOLDER_SHA256,
            "m11_human_benchmark_claim_decision_json_canonical_sha256": PLACEHOLDER_SHA256,
            "m05_strong_agent_scorecard_json_canonical_sha256": PLACEHOLDER_SHA256,
            "m03_checkpoint_lineage_manifest_json_canonical_sha256": PLACEHOLDER_SHA256,
        },
        "m12_upstream_summary_snapshot": {
            "bound": False,
            "showcase_release_status": "not_bound_fixture",
        },
        "decision_gates": _fixture_decision_gates(),
        "non_claims": list(NON_CLAIMS_V15_M13),
        "authorization_flags": af,
        "operator_declared_v2_decision_evidence": None,
    }


def build_v2_decision_body_operator_preflight(
    m12_path: Path,
    optional_paths: Mapping[str, Path | None],
) -> dict[str, Any]:
    m12 = _load_m12(m12_path)
    m12_sha = _json_file_canonical_sha256(m12_path)
    # Optional upstream paths use field keys matching M12 upstream_bindings.
    opt_fields = (
        "m08_campaign_receipt",
        "m09_promotion_decision",
        "m10_xai_demonstration",
        "m11_human_benchmark_claim",
        "m05_strong_agent_scorecard",
        "m03_checkpoint_lineage",
    )
    cross_attempted = sum(1 for f in opt_fields if optional_paths.get(f) is not None)
    cross_matched = 0
    if cross_attempted:
        cross_matched, _ = verify_upstream_cross_checks(m12, optional_paths)

    pre = _all_v2_prerequisites(m12)
    auth = _compute_authorization_flags(m12, operator_evidence=None, prerequisites_met=pre)
    # Preflight never authorizes v2 without operator_declared evidence contract
    auth["v2_authorized"] = False
    auth["v2_recharter_authorized"] = False
    gates = _gates_with_m12(
        m12,
        profile=PROFILE_OPERATOR_PREFLIGHT,
        cross_matched=cross_matched,
        cross_attempted=cross_attempted,
        prerequisites_met=pre,
    )
    secondary = _secondary_statuses(m12, prerequisites_met=pre, auth_flags=auth)
    summ = _summaries_from_m12(m12)
    body: dict[str, Any] = {
        "contract_id": CONTRACT_ID_V2_GO_NO_GO_DECISION,
        "contract_version": CONTRACT_VERSION,
        "milestone_id": MILESTONE_ID_V15_M13,
        "profile_id": PROFILE_ID_V2_GO_NO_GO_DECISION,
        "emit_profile": PROFILE_OPERATOR_PREFLIGHT,
        "emitter_module": EMITTER_MODULE_V2_DECISION,
        "v2_decision_id": f"v15_m13:operator_preflight:{m12_sha[:16]}",
        "v2_decision_status": _decision_status_primary(m12, v2_authorized=False),
        "v2_decision_status_secondary": secondary,
        "decision_outcome": OUTCOME_NO_GO,
        "recommended_next_step": RECOMMENDED_NEXT_STEP_COLLECT,
        "m12_showcase_release_pack_json_canonical_sha256": m12_sha,
        "optional_upstream_crosscheck": {
            _BINDING_KEY_BY_FIELD[f]: _optional_path_sha(optional_paths, f) for f in opt_fields
        },
        "m12_upstream_summary_snapshot": {
            "bound": True,
            "showcase_release_status": summ["showcase_release_status"],
            "m08_campaign_completion": summ["m08_campaign_completion"],
            "m09_promotion_status": summ["m09_promotion_status"],
        },
        "decision_gates": gates,
        "non_claims": list(NON_CLAIMS_V15_M13),
        "authorization_flags": auth,
        "operator_declared_v2_decision_evidence": None,
    }
    return body


def build_v2_decision_body_operator_declared(
    m12_path: Path,
    decision_evidence_path: Path,
    optional_paths: Mapping[str, Path | None],
) -> tuple[dict[str, Any], dict[str, Any], int]:
    ev = _parse_decision_evidence(decision_evidence_path)
    m12 = _load_m12(m12_path)
    m12_sha = _json_file_canonical_sha256(m12_path)
    opt_fields = (
        "m08_campaign_receipt",
        "m09_promotion_decision",
        "m10_xai_demonstration",
        "m11_human_benchmark_claim",
        "m05_strong_agent_scorecard",
        "m03_checkpoint_lineage",
    )
    cross_attempted = sum(1 for f in opt_fields if optional_paths.get(f) is not None)
    cross_matched = 0
    if cross_attempted:
        cross_matched, _ = verify_upstream_cross_checks(m12, optional_paths)

    pre = _all_v2_prerequisites(m12)
    ev_public = {
        "contract_id": ev["contract_id"],
        "evidence_bundle_id": ev["evidence_bundle_id"],
        "operator_public_notes": ev.get("operator_public_notes"),
        "operator_recommended_next_step": ev.get("operator_recommended_next_step"),
        "operator_rationale": ev.get("operator_rationale"),
        "v2_recharter_scope_declared": ev.get("v2_recharter_scope_declared"),
        "rights_clearance_operator_declared": ev.get("rights_clearance_operator_declared"),
    }
    redacted_ev = redact_v2_decision_value(ev_public)
    if not isinstance(redacted_ev, dict):
        raise ValueError("redacted operator evidence must be an object")
    rc = _redaction_token_count(redacted_ev)

    auth = _compute_authorization_flags(m12, operator_evidence=redacted_ev, prerequisites_met=pre)
    gates = _gates_with_m12(
        m12,
        profile=PROFILE_OPERATOR_DECLARED,
        cross_matched=cross_matched,
        cross_attempted=cross_attempted,
        prerequisites_met=pre,
    )
    secondary = _secondary_statuses(m12, prerequisites_met=pre, auth_flags=auth)
    if auth["v2_authorized"]:
        secondary = [STATUS_PROCEED_TO_V2_AUTHORIZED]
    summ = _summaries_from_m12(m12)
    rec = str(ev.get("operator_recommended_next_step") or "").strip()
    recommended = rec if rec else RECOMMENDED_NEXT_STEP_COLLECT
    if not auth["v2_authorized"]:
        recommended = RECOMMENDED_NEXT_STEP_COLLECT
    outcome = OUTCOME_PROCEED_TO_V2 if auth["v2_authorized"] else OUTCOME_NO_GO

    body: dict[str, Any] = {
        "contract_id": CONTRACT_ID_V2_GO_NO_GO_DECISION,
        "contract_version": CONTRACT_VERSION,
        "milestone_id": MILESTONE_ID_V15_M13,
        "profile_id": PROFILE_ID_V2_GO_NO_GO_DECISION,
        "emit_profile": PROFILE_OPERATOR_DECLARED,
        "emitter_module": EMITTER_MODULE_V2_DECISION,
        "v2_decision_id": f"v15_m13:operator_declared:{ev['evidence_bundle_id']}",
        "v2_decision_status": (
            STATUS_PROCEED_TO_V2_AUTHORIZED
            if auth["v2_authorized"]
            else STATUS_FIXTURE_DECISION_ONLY
        ),
        "v2_decision_status_secondary": secondary,
        "decision_outcome": outcome,
        "recommended_next_step": recommended,
        "m12_showcase_release_pack_json_canonical_sha256": m12_sha,
        "optional_upstream_crosscheck": {
            _BINDING_KEY_BY_FIELD[f]: _optional_path_sha(optional_paths, f) for f in opt_fields
        },
        "m12_upstream_summary_snapshot": {
            "bound": True,
            "showcase_release_status": summ["showcase_release_status"],
            "m08_campaign_completion": summ["m08_campaign_completion"],
            "m09_promotion_status": summ["m09_promotion_status"],
        },
        "decision_gates": gates,
        "non_claims": list(NON_CLAIMS_V15_M13),
        "authorization_flags": auth,
        "operator_declared_v2_decision_evidence": redacted_ev,
    }
    return body, redacted_ev, rc


def seal_v2_decision_body(body: dict[str, Any]) -> dict[str, Any]:
    base = {k: v for k, v in body.items() if k != _SEAL}
    digest = sha256_hex_of_canonical_json(base)
    sealed = dict(base)
    sealed[_SEAL] = digest
    return sealed


def build_v2_decision_report(sealed: dict[str, Any], *, redaction_count: int) -> dict[str, Any]:
    base = {k: v for k, v in sealed.items() if k != _SEAL}
    digest = sha256_hex_of_canonical_json(base)
    return {
        "report_kind": "v15_v2_go_no_go_decision_report",
        "report_version": REPORT_VERSION_V2_DECISION,
        "milestone": MILESTONE_ID_V15_M13,
        "artifact_sha256": digest,
        "seal_field": _SEAL,
        "seal_value_matches_artifact": sealed.get(_SEAL) == digest,
        "redaction_events": int(redaction_count),
        "primary_filename": FILENAME_V2_GO_NO_GO_DECISION,
        "markdown_brief_filename": FILENAME_V2_GO_NO_GO_DECISION_BRIEF_MD,
    }


def render_v2_decision_brief_md(sealed: dict[str, Any]) -> str:
    snap = sealed.get("m12_upstream_summary_snapshot")
    if not isinstance(snap, dict):
        snap = {}
    lines: list[str] = [
        "# V15 v2 Go / No-Go Decision Brief",
        "",
        "This fixture decision validates the governed v2 decision artifact shape.",
        "It does not authorize v2 or any public performance claim on the default path.",
        "The default recommendation is to collect operator evidence or continue v1.5 hardening "
        "before v2.",
        "",
        "## Decision status",
        f"- `v2_decision_status`: `{sealed.get('v2_decision_status', '')}`",
        f"- `decision_outcome`: `{sealed.get('decision_outcome', '')}`",
        f"- `recommended_next_step`: `{sealed.get('recommended_next_step', '')}`",
        f"- `emit_profile`: `{sealed.get('emit_profile', '')}`",
        "",
        "## M12 release-pack status",
        f"- M12 bound: `{snap.get('bound', '')}`",
        f"- `showcase_release_status` (snapshot): `{snap.get('showcase_release_status', '')}`",
        "",
        "## Campaign evidence status",
        f"- M08 campaign completion (snapshot): `{snap.get('m08_campaign_completion', '')}`",
        "",
        "## Checkpoint promotion status",
        f"- M09 promotion_status (snapshot): `{snap.get('m09_promotion_status', '')}`",
        "",
        "## Strong-agent benchmark status",
        "- See M12 upstream summaries; default path does not record benchmark execution.",
        "",
        "## XAI evidence status",
        "- Replay-native XAI demonstration is metadata-bound only on this surface.",
        "",
        "## Human benchmark status",
        "- Human-benchmark claim authorization is read from M12 summaries only.",
        "",
        "## Rights and public/private status",
        "- Default path: no rights clearance for raw weights, checkpoints, replays, videos, "
        "saliency tensors, or participant materials.",
        "",
        "## Open risks and dispositions",
        "- Not evaluated on fixture-only path; operator records remain outside this artifact.",
        "",
        "## Gate table",
    ]
    gates = sealed.get("decision_gates")
    if isinstance(gates, list):
        for g in gates:
            if isinstance(g, dict):
                gid = g.get("gate_id", "")
                st = g.get("status", "")
                notes = str(g.get("notes", "")).replace("\n", " ")
                lines.append(f"- `{gid}`: **{st}** — {notes}")
    lines.extend(
        [
            "",
            "## Authorized claims",
            "- None on the default fixture path; authorization flags are false unless "
            "non-default governed evidence explicitly supports them.",
        ]
    )
    af = sealed.get("authorization_flags")
    if isinstance(af, dict):
        lines.append("- Flag snapshot:")
        for k in sorted(af.keys()):
            lines.append(f"  - `{k}`: `{af[k]}`")
    lines.extend(
        [
            "",
            "## Non-claims",
        ]
    )
    nc = sealed.get("non_claims")
    if isinstance(nc, list):
        for item in nc:
            lines.append(f"- {item}")
    lines.extend(
        [
            "",
            "## v2 recharter boundary",
            "- v2 recharter requires a governed evidence package, M12 release authorization, "
            "and explicit operator-declared scope and rights posture. This artifact alone does "
            "not open v2.",
            "",
        ]
    )
    return "\n".join(lines) + "\n"


def emit_v15_v2_go_no_go_decision_fixture(
    output_dir: Path,
) -> tuple[dict[str, Any], dict[str, Any], Path, Path, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    body = build_v2_decision_body_fixture()
    sealed = seal_v2_decision_body(body)
    report = build_v2_decision_report(sealed, redaction_count=0)
    md = render_v2_decision_brief_md(sealed)
    pj = output_dir / FILENAME_V2_GO_NO_GO_DECISION
    pr = output_dir / REPORT_FILENAME_V2_GO_NO_GO_DECISION
    pm = output_dir / FILENAME_V2_GO_NO_GO_DECISION_BRIEF_MD
    pj.write_text(canonical_json_dumps(sealed), encoding="utf-8")
    pr.write_text(canonical_json_dumps(report), encoding="utf-8")
    pm.write_text(md, encoding="utf-8", newline="\n")
    return sealed, report, pj, pr, pm


def emit_v15_v2_go_no_go_decision_operator_preflight(
    output_dir: Path,
    m12_path: Path,
    optional_paths: Mapping[str, Path | None],
) -> tuple[dict[str, Any], dict[str, Any], Path, Path, Path]:
    body = build_v2_decision_body_operator_preflight(m12_path, optional_paths)
    sealed = seal_v2_decision_body(body)
    report = build_v2_decision_report(sealed, redaction_count=0)
    md = render_v2_decision_brief_md(sealed)
    output_dir.mkdir(parents=True, exist_ok=True)
    pj = output_dir / FILENAME_V2_GO_NO_GO_DECISION
    pr = output_dir / REPORT_FILENAME_V2_GO_NO_GO_DECISION
    pm = output_dir / FILENAME_V2_GO_NO_GO_DECISION_BRIEF_MD
    pj.write_text(canonical_json_dumps(sealed), encoding="utf-8")
    pr.write_text(canonical_json_dumps(report), encoding="utf-8")
    pm.write_text(md, encoding="utf-8", newline="\n")
    return sealed, report, pj, pr, pm


def emit_v15_v2_go_no_go_decision_operator_declared(
    output_dir: Path,
    m12_path: Path,
    decision_evidence_path: Path,
    optional_paths: Mapping[str, Path | None],
) -> tuple[dict[str, Any], dict[str, Any], int, Path, Path, Path]:
    body, _ev, rc = build_v2_decision_body_operator_declared(
        m12_path, decision_evidence_path, optional_paths
    )
    sealed = seal_v2_decision_body(body)
    report = build_v2_decision_report(sealed, redaction_count=rc)
    md = render_v2_decision_brief_md(sealed)
    output_dir.mkdir(parents=True, exist_ok=True)
    pj = output_dir / FILENAME_V2_GO_NO_GO_DECISION
    pr = output_dir / REPORT_FILENAME_V2_GO_NO_GO_DECISION
    pm = output_dir / FILENAME_V2_GO_NO_GO_DECISION_BRIEF_MD
    pj.write_text(canonical_json_dumps(sealed), encoding="utf-8")
    pr.write_text(canonical_json_dumps(report), encoding="utf-8")
    pm.write_text(md, encoding="utf-8", newline="\n")
    return sealed, report, rc, pj, pr, pm


__all__ = [
    "FORBIDDEN_BRIEF_SUBSTRINGS",
    "build_v2_decision_body_fixture",
    "build_v2_decision_body_operator_declared",
    "build_v2_decision_body_operator_preflight",
    "build_v2_decision_report",
    "emit_v15_v2_go_no_go_decision_fixture",
    "emit_v15_v2_go_no_go_decision_operator_declared",
    "emit_v15_v2_go_no_go_decision_operator_preflight",
    "redact_v2_decision_value",
    "render_v2_decision_brief_md",
    "seal_v2_decision_body",
    "verify_upstream_cross_checks",
]
