"""Build, seal, and write V15-M12 showcase agent release pack + report + Markdown brief."""

from __future__ import annotations

import json
import re
from collections.abc import Mapping
from pathlib import Path
from typing import Any, Final

from starlab.runs.json_util import canonical_json_dumps, sha256_hex_of_canonical_json
from starlab.v15.checkpoint_evaluation_io import m08_campaign_receipt_valid_for_m09
from starlab.v15.checkpoint_evaluation_models import (
    CONTRACT_ID_CHECKPOINT_PROMOTION_DECISION,
    PROMOTION_STATUS_PROMOTED_CANDIDATE,
    PROMOTION_STATUS_PROMOTED_XAI,
)
from starlab.v15.checkpoint_lineage_models import CONTRACT_ID_CHECKPOINT_LINEAGE
from starlab.v15.human_panel_benchmark_io import redact_path_and_contact_in_value
from starlab.v15.human_panel_execution_models import CONTRACT_ID_HUMAN_BENCHMARK_CLAIM_DECISION
from starlab.v15.long_gpu_training_manifest_models import CONTRACT_ID_LONG_GPU_CAMPAIGN_RECEIPT
from starlab.v15.showcase_release_models import (
    CONTRACT_ID_OPERATOR_RELEASE_EVIDENCE_DECLARED,
    CONTRACT_ID_SHOWCASE_AGENT_RELEASE_PACK,
    CONTRACT_VERSION,
    EMITTER_MODULE_SHOWCASE_RELEASE,
    FILENAME_SHOWCASE_RELEASE_BRIEF_MD,
    FILENAME_SHOWCASE_RELEASE_PACK,
    FIXTURE_RELEASE_PACK_ID,
    GATE_STATUS_BLOCKED,
    GATE_STATUS_PASS,
    GATE_STATUS_WARNING,
    MILESTONE_ID_V15_M12,
    NON_CLAIMS_V15_M12,
    OPERATOR_RELEASE_EVIDENCE_KEYS,
    PLACEHOLDER_SHA256,
    PROFILE_FIXTURE_CI,
    PROFILE_ID_SHOWCASE_RELEASE_PACK,
    PROFILE_OPERATOR_DECLARED,
    PROFILE_OPERATOR_PREFLIGHT,
    R0_ARTIFACT_INTEGRITY,
    R1_CAMPAIGN_RECEIPT_BINDING,
    R2_CHECKPOINT_PROMOTION_BINDING,
    R3_CHECKPOINT_LINEAGE_BINDING,
    R4_STRONG_AGENT_SCORECARD_BINDING,
    R5_XAI_DEMONSTRATION_BINDING,
    R6_HUMAN_BENCHMARK_CLAIM_BINDING,
    R7_RIGHTS_AND_REGISTER_POSTURE,
    R8_PUBLIC_PRIVATE_BOUNDARY,
    R9_RELEASE_MANIFEST_COMPLETENESS,
    R10_CLAIM_TEXT_BOUNDARY,
    R11_REPRODUCIBILITY_SHA_BINDINGS,
    R12_RAW_ASSET_EXCLUSION,
    R13_OPERATOR_NOTES_REDACTION,
    R14_V2_BOUNDARY,
    REPORT_FILENAME_SHOWCASE_RELEASE_PACK,
    REPORT_VERSION_SHOWCASE_RELEASE,
    SEAL_KEY_SHOWCASE_RELEASE_PACK,
    STATUS_BLOCKED_HUMAN_BENCHMARK,
    STATUS_BLOCKED_M08_RECEIPT,
    STATUS_BLOCKED_MANIFEST,
    STATUS_BLOCKED_PROMOTED_CP,
    STATUS_BLOCKED_RIGHTS,
    STATUS_BLOCKED_STRONG_AGENT,
    STATUS_BLOCKED_XAI,
    STATUS_FIXTURE_CONTRACT_ONLY,
    STATUS_OP_DECLARED_VALIDATED,
    STATUS_OP_PREFLIGHT_VALIDATED,
    default_m12_authorization_flags,
)
from starlab.v15.strong_agent_scorecard_models import CONTRACT_ID_STRONG_AGENT_SCORECARD
from starlab.v15.training_run_receipt_io import _redaction_token_count, redact_receipt_value
from starlab.v15.xai_demonstration_models import (
    CONTRACT_ID_REPLAY_NATIVE_XAI_DEMONSTRATION,
    DEMONSTRATION_STATUS_OPERATOR_DECLARED_PACK,
)

_SEAL = SEAL_KEY_SHOWCASE_RELEASE_PACK
_HEX64 = re.compile(r"^[0-9a-fA-F]{64}$")

FORBIDDEN_BRIEF_SUBSTRINGS: Final[tuple[str, ...]] = (
    "STARLAB has released a strong agent",
    "the agent beats most humans",
    "the checkpoint is promoted",
    "the XAI is faithful",
    "v2 is authorized",
)


def _json_file_canonical_sha256(path: Path) -> str:
    raw = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ValueError("JSON must be a single object")
    return sha256_hex_of_canonical_json(raw)


def _require_contract(obj: dict[str, Any], expected: str, ctx: str) -> None:
    if str(obj.get("contract_id", "")) != expected:
        raise ValueError(
            f"{ctx}: contract_id must be {expected!r} (got {obj.get('contract_id')!r})"
        )


def redact_release_pack_value(obj: Any) -> Any:
    return redact_receipt_value(redact_path_and_contact_in_value(obj))


def _parse_release_evidence(path: Path) -> dict[str, Any]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ValueError("release evidence JSON must be a single object")
    unknown = set(raw) - OPERATOR_RELEASE_EVIDENCE_KEYS
    if unknown:
        raise ValueError(f"release evidence: unknown keys {sorted(unknown)}")
    _require_contract(raw, CONTRACT_ID_OPERATOR_RELEASE_EVIDENCE_DECLARED, "release_evidence")
    eid = raw.get("evidence_bundle_id")
    if not isinstance(eid, str) or not eid.strip():
        raise ValueError("release evidence: evidence_bundle_id required")
    rc = raw.get("rights_clearance_operator_declared")
    if rc is not None and not isinstance(rc, bool):
        raise ValueError(
            "release evidence: rights_clearance_operator_declared must be bool or omitted"
        )
    return raw


def _row(gate_id: str, status: str, notes: str) -> dict[str, Any]:
    return {"gate_id": gate_id, "status": status, "notes": notes}


def _fixture_release_gates() -> list[dict[str, Any]]:
    gp, gb, gw = GATE_STATUS_PASS, GATE_STATUS_BLOCKED, GATE_STATUS_WARNING
    return [
        _row(R0_ARTIFACT_INTEGRITY, gp, "Fixture release pack: deterministic schema; sealed."),
        _row(
            R1_CAMPAIGN_RECEIPT_BINDING,
            gb,
            "No completed M08 long GPU campaign receipt on default fixture path.",
        ),
        _row(
            R2_CHECKPOINT_PROMOTION_BINDING,
            gb,
            "No promoted checkpoint for showcase release binding on default fixture path.",
        ),
        _row(
            R3_CHECKPOINT_LINEAGE_BINDING,
            gw,
            "M03 lineage SHA is placeholder on fixture path; metadata only.",
        ),
        _row(
            R4_STRONG_AGENT_SCORECARD_BINDING,
            gb,
            "Strong-agent benchmark not executed; scorecard is protocol/fixture only.",
        ),
        _row(
            R5_XAI_DEMONSTRATION_BINDING,
            gb,
            "Replay-native XAI demonstration is fixture-only; no inference path.",
        ),
        _row(
            R6_HUMAN_BENCHMARK_CLAIM_BINDING,
            gb,
            "Human-benchmark claim not authorized on default path (M11 posture).",
        ),
        _row(
            R7_RIGHTS_AND_REGISTER_POSTURE,
            gb,
            "Rights / register clearance for public release not established.",
        ),
        _row(R8_PUBLIC_PRIVATE_BOUNDARY, gp, "Fixture pack contains no absolute paths."),
        _row(
            R9_RELEASE_MANIFEST_COMPLETENESS,
            gb,
            "Release manifest incomplete for a real showcase drop (fixture contract only).",
        ),
        _row(
            R10_CLAIM_TEXT_BOUNDARY,
            gp,
            "Non-claim vocabulary present; no default public performance authorization.",
        ),
        _row(
            R11_REPRODUCIBILITY_SHA_BINDINGS,
            gw,
            "Upstream SHA bindings are placeholders on fixture path.",
        ),
        _row(
            R12_RAW_ASSET_EXCLUSION,
            gp,
            "Pack does not embed weight blobs, replay binaries, or checkpoint file paths.",
        ),
        _row(
            R13_OPERATOR_NOTES_REDACTION,
            gp,
            "No raw operator notes on fixture default path.",
        ),
        _row(
            R14_V2_BOUNDARY,
            gp,
            "v2 go/no-go is V15-M13; M12 does not authorize v2.",
        ),
    ]


def _non_placeholder_sha(s: str) -> bool:
    return bool(_HEX64.match(s)) and s != PLACEHOLDER_SHA256


def _summaries(
    m08: dict[str, Any],
    m09: dict[str, Any],
    m10: dict[str, Any],
    m11: dict[str, Any],
    m05: dict[str, Any],
    m03: dict[str, Any],
) -> dict[str, Any]:
    raw_af = m11.get("authorization_flags")
    af11: dict[str, Any] = raw_af if isinstance(raw_af, dict) else {}
    promo = str(m09.get("promotion_status", ""))
    lineage = m03.get("checkpoint_lineage")
    n_lin = len(lineage) if isinstance(lineage, list) else 0
    return {
        "m08_receipt_valid": m08_campaign_receipt_valid_for_m09(m08),
        "m09_promotion_status": promo,
        "m10_demonstration_status": str(m10.get("demonstration_status", "")),
        "m11_human_benchmark_claim_authorized": bool(af11.get("human_benchmark_claim_authorized")),
        "m05_benchmark_execution_performed": bool(m05.get("benchmark_execution_performed")),
        "m05_strong_agent_claim_authorized": bool(m05.get("strong_agent_claim_authorized")),
        "m03_lineage_row_count": n_lin,
    }


def _gates_operator(
    summaries: dict[str, Any],
    *,
    profile: str,
    bindings: Mapping[str, str | None],
    rights_declared: bool | None,
) -> list[dict[str, Any]]:
    gp, gb, gw = GATE_STATUS_PASS, GATE_STATUS_BLOCKED, GATE_STATUS_WARNING
    m08_ok = bool(summaries.get("m08_receipt_valid"))
    promo = str(summaries.get("m09_promotion_status", ""))
    promo_ok = promo in (PROMOTION_STATUS_PROMOTED_CANDIDATE, PROMOTION_STATUS_PROMOTED_XAI)
    dst = str(summaries.get("m10_demonstration_status", ""))
    xai_ok = dst == DEMONSTRATION_STATUS_OPERATOR_DECLARED_PACK
    h_ok = bool(summaries.get("m11_human_benchmark_claim_authorized"))
    bench_ok = bool(summaries.get("m05_benchmark_execution_performed")) and bool(
        summaries.get("m05_strong_agent_claim_authorized")
    )
    n_lin = int(summaries.get("m03_lineage_row_count") or 0)
    lineage_ok = n_lin > 0

    sha_vals = [v for v in bindings.values() if isinstance(v, str)]
    real_shas = all(_non_placeholder_sha(v) for v in sha_vals)

    r1 = gp if m08_ok else gb
    r1n = (
        "M08 campaign receipt records completion markers (operator-local evidence only)."
        if m08_ok
        else "M08 receipt does not record a completed long GPU campaign for release binding."
    )
    r2 = gp if promo_ok else gb
    r2n = (
        "M09 promotion_status allows downstream routing (not a strength or release claim)."
        if promo_ok
        else f"M09 promotion_status={promo!r} blocks promoted-checkpoint release binding."
    )
    r3 = gp if lineage_ok else gb
    r3n = (
        "M03 checkpoint lineage JSON bound by SHA."
        if lineage_ok
        else "M03 lineage empty or missing."
    )
    r4 = gp if bench_ok else gb
    r4n = (
        "Supplied M05 scorecard asserts benchmark execution and strong-agent authorization."
        if bench_ok
        else "M05 scorecard does not record benchmark execution + strong-agent authorization."
    )
    r5 = gp if xai_ok else gb
    r5n = (
        "M10 demonstration status is operator-declared pack (still not inference)."
        if xai_ok
        else "M10 demonstration is not operator-declared pack; XAI release gate blocked."
    )
    r6 = gp if h_ok else gb
    r6n = (
        "M11 authorizes bounded human-benchmark claim."
        if h_ok
        else "M11 human_benchmark_claim_authorized is false; showcase human gate blocked."
    )
    r7 = gp if rights_declared is True else gb
    r7n = (
        "Operator declared rights clearance summary in release-evidence bundle (governance only)."
        if rights_declared is True
        else "Rights / public-register clearance not operator-declared for this pack."
    )
    if profile == PROFILE_OPERATOR_PREFLIGHT:
        r7 = gb
        r7n = "Preflight profile does not accept rights declarations; use operator_declared."
    r8 = gp
    r8n = "Path/contact redaction applied to operator-supplied text fields before emission."
    r9 = gb if profile == PROFILE_OPERATOR_PREFLIGHT else gw
    r9n = (
        "Operator preflight validates bindings only; full release manifest is out of scope."
        if profile == PROFILE_OPERATOR_PREFLIGHT
        else "Release manifest completeness requires explicit non-default evidence (governance)."
    )
    r10 = gp
    r10n = "Claim text boundary preserved; authorization flags remain false unless evidence forces."
    r11 = gp if real_shas else gw
    r11n = (
        "All upstream JSON bindings use non-placeholder canonical SHA-256."
        if real_shas
        else "Some bindings are placeholder all-zero SHAs in supplied JSON."
    )
    r12 = gp
    r12n = "Emitter does not read checkpoint blobs, weights, or replay binaries."
    r13 = gp
    r13n = "Operator notes redacted when present (token count in report)."
    r14 = gp
    r14n = "v2 authorization deferred to V15-M13; M12 emits release-pack surface only."

    return [
        _row(R0_ARTIFACT_INTEGRITY, gp, "Upstream JSON parsed; contract_ids validated."),
        _row(R1_CAMPAIGN_RECEIPT_BINDING, r1, r1n),
        _row(R2_CHECKPOINT_PROMOTION_BINDING, r2, r2n),
        _row(R3_CHECKPOINT_LINEAGE_BINDING, r3, r3n),
        _row(R4_STRONG_AGENT_SCORECARD_BINDING, r4, r4n),
        _row(R5_XAI_DEMONSTRATION_BINDING, r5, r5n),
        _row(R6_HUMAN_BENCHMARK_CLAIM_BINDING, r6, r6n),
        _row(R7_RIGHTS_AND_REGISTER_POSTURE, r7, r7n),
        _row(R8_PUBLIC_PRIVATE_BOUNDARY, r8, r8n),
        _row(R9_RELEASE_MANIFEST_COMPLETENESS, r9, r9n),
        _row(R10_CLAIM_TEXT_BOUNDARY, r10, r10n),
        _row(R11_REPRODUCIBILITY_SHA_BINDINGS, r11, r11n),
        _row(R12_RAW_ASSET_EXCLUSION, r12, r12n),
        _row(R13_OPERATOR_NOTES_REDACTION, r13, r13n),
        _row(R14_V2_BOUNDARY, r14, r14n),
    ]


def _status_for_gates(gates: list[dict[str, Any]], *, profile: str) -> str:
    blocked = any(g["status"] == GATE_STATUS_BLOCKED for g in gates)
    if blocked:
        if profile == PROFILE_FIXTURE_CI:
            return STATUS_FIXTURE_CONTRACT_ONLY
        return STATUS_BLOCKED_MANIFEST
    if profile == PROFILE_OPERATOR_PREFLIGHT:
        return STATUS_OP_PREFLIGHT_VALIDATED
    if profile == PROFILE_OPERATOR_DECLARED:
        return STATUS_OP_DECLARED_VALIDATED
    return STATUS_FIXTURE_CONTRACT_ONLY


def build_release_pack_body_fixture() -> dict[str, Any]:
    af = default_m12_authorization_flags()
    return {
        "contract_id": CONTRACT_ID_SHOWCASE_AGENT_RELEASE_PACK,
        "contract_version": CONTRACT_VERSION,
        "milestone_id": MILESTONE_ID_V15_M12,
        "profile_id": PROFILE_ID_SHOWCASE_RELEASE_PACK,
        "emit_profile": PROFILE_FIXTURE_CI,
        "emitter_module": EMITTER_MODULE_SHOWCASE_RELEASE,
        "release_pack_id": FIXTURE_RELEASE_PACK_ID,
        "showcase_release_status": STATUS_FIXTURE_CONTRACT_ONLY,
        "showcase_release_status_secondary": [
            STATUS_BLOCKED_PROMOTED_CP,
            STATUS_BLOCKED_M08_RECEIPT,
            STATUS_BLOCKED_HUMAN_BENCHMARK,
        ],
        "candidate_identity_summary": {
            "candidate_checkpoint_id": "fixture:none",
            "training_run_id": "fixture:none",
            "logical_showcase_agent_id": "fixture:v15_m12_none",
        },
        "upstream_bindings": {
            "m08_campaign_receipt_json_canonical_sha256": PLACEHOLDER_SHA256,
            "m09_promotion_decision_json_canonical_sha256": PLACEHOLDER_SHA256,
            "m10_replay_native_xai_demonstration_json_canonical_sha256": PLACEHOLDER_SHA256,
            "m11_human_benchmark_claim_decision_json_canonical_sha256": PLACEHOLDER_SHA256,
            "m05_strong_agent_scorecard_json_canonical_sha256": PLACEHOLDER_SHA256,
            "m03_checkpoint_lineage_manifest_json_canonical_sha256": PLACEHOLDER_SHA256,
        },
        "upstream_summaries": {
            "m08_campaign_completion": "not_bound_fixture",
            "m09_promotion_status": "blocked",
            "m10_demonstration_status": "fixture_contract_only",
            "m11_claim_authorized": False,
            "m05_benchmark_executed": False,
        },
        "release_gates": _fixture_release_gates(),
        "non_claims": list(NON_CLAIMS_V15_M12),
        "authorization_flags": af,
        "redaction_policy": {
            "fixture": "no_operator_inputs",
            "operator": "redact_paths_contacts_secrets_in_declared_fields",
        },
        "operator_declared_release_evidence": None,
    }


def _bind_operator_inputs(
    m08p: Path,
    m09p: Path,
    m10p: Path,
    m11p: Path,
    m05p: Path,
    m03p: Path,
) -> tuple[dict[str, Any], dict[str, str]]:
    m08 = json.loads(m08p.read_text(encoding="utf-8"))
    m09 = json.loads(m09p.read_text(encoding="utf-8"))
    m10 = json.loads(m10p.read_text(encoding="utf-8"))
    m11 = json.loads(m11p.read_text(encoding="utf-8"))
    m05 = json.loads(m05p.read_text(encoding="utf-8"))
    m03 = json.loads(m03p.read_text(encoding="utf-8"))
    if not all(isinstance(x, dict) for x in (m08, m09, m10, m11, m05, m03)):
        raise ValueError("each upstream file must contain a JSON object")
    _require_contract(m08, CONTRACT_ID_LONG_GPU_CAMPAIGN_RECEIPT, "m08_campaign_receipt")
    _require_contract(m09, CONTRACT_ID_CHECKPOINT_PROMOTION_DECISION, "m09_promotion")
    _require_contract(m10, CONTRACT_ID_REPLAY_NATIVE_XAI_DEMONSTRATION, "m10_xai_demo")
    _require_contract(m11, CONTRACT_ID_HUMAN_BENCHMARK_CLAIM_DECISION, "m11_claim")
    _require_contract(m05, CONTRACT_ID_STRONG_AGENT_SCORECARD, "m05_scorecard")
    _require_contract(m03, CONTRACT_ID_CHECKPOINT_LINEAGE, "m03_lineage")
    bindings = {
        "m08_campaign_receipt_json_canonical_sha256": _json_file_canonical_sha256(m08p),
        "m09_promotion_decision_json_canonical_sha256": _json_file_canonical_sha256(m09p),
        "m10_replay_native_xai_demonstration_json_canonical_sha256": _json_file_canonical_sha256(
            m10p
        ),
        "m11_human_benchmark_claim_decision_json_canonical_sha256": _json_file_canonical_sha256(
            m11p
        ),
        "m05_strong_agent_scorecard_json_canonical_sha256": _json_file_canonical_sha256(m05p),
        "m03_checkpoint_lineage_manifest_json_canonical_sha256": _json_file_canonical_sha256(m03p),
    }
    summaries = _summaries(m08, m09, m10, m11, m05, m03)
    return summaries, bindings


def build_release_pack_body_operator_preflight(
    m08p: Path,
    m09p: Path,
    m10p: Path,
    m11p: Path,
    m05p: Path,
    m03p: Path,
) -> dict[str, Any]:
    summaries, bindings = _bind_operator_inputs(m08p, m09p, m10p, m11p, m05p, m03p)
    gates = _gates_operator(
        summaries,
        profile=PROFILE_OPERATOR_PREFLIGHT,
        bindings=bindings,
        rights_declared=None,
    )
    status = _status_for_gates(gates, profile=PROFILE_OPERATOR_PREFLIGHT)
    af = default_m12_authorization_flags()
    pre_sha = bindings["m09_promotion_decision_json_canonical_sha256"][:16]
    return {
        "contract_id": CONTRACT_ID_SHOWCASE_AGENT_RELEASE_PACK,
        "contract_version": CONTRACT_VERSION,
        "milestone_id": MILESTONE_ID_V15_M12,
        "profile_id": PROFILE_ID_SHOWCASE_RELEASE_PACK,
        "emit_profile": PROFILE_OPERATOR_PREFLIGHT,
        "emitter_module": EMITTER_MODULE_SHOWCASE_RELEASE,
        "release_pack_id": f"v15_m12:operator_preflight:{pre_sha}",
        "showcase_release_status": status,
        "showcase_release_status_secondary": _secondary_blockers(
            summaries, PROFILE_OPERATOR_PREFLIGHT
        ),
        "candidate_identity_summary": {
            "candidate_checkpoint_id": str(
                summaries.get("m09_promotion_status", "unknown"),
            ),
            "training_run_id": "not_emitted_in_m12",
            "logical_showcase_agent_id": "governance_placeholder",
        },
        "upstream_bindings": bindings,
        "upstream_summaries": {
            "m08_campaign_completion": "valid_receipt"
            if summaries["m08_receipt_valid"]
            else "invalid_or_incomplete",
            "m09_promotion_status": summaries["m09_promotion_status"],
            "m10_demonstration_status": summaries["m10_demonstration_status"],
            "m11_claim_authorized": summaries["m11_human_benchmark_claim_authorized"],
            "m05_benchmark_executed": summaries["m05_benchmark_execution_performed"],
        },
        "release_gates": gates,
        "non_claims": list(NON_CLAIMS_V15_M12),
        "authorization_flags": af,
        "redaction_policy": {
            "operator_preflight": "no_embedded_upstream_json_bodies_sha_only",
        },
        "operator_declared_release_evidence": None,
    }


def _secondary_blockers(summaries: dict[str, Any], profile: str) -> list[str]:
    out: list[str] = []
    if not summaries.get("m08_receipt_valid"):
        out.append(STATUS_BLOCKED_M08_RECEIPT)
    promo = str(summaries.get("m09_promotion_status", ""))
    if promo not in (PROMOTION_STATUS_PROMOTED_CANDIDATE, PROMOTION_STATUS_PROMOTED_XAI):
        out.append(STATUS_BLOCKED_PROMOTED_CP)
    if not summaries.get("m05_benchmark_execution_performed"):
        out.append(STATUS_BLOCKED_STRONG_AGENT)
    dst = str(summaries.get("m10_demonstration_status", ""))
    if dst != DEMONSTRATION_STATUS_OPERATOR_DECLARED_PACK:
        out.append(STATUS_BLOCKED_XAI)
    if not summaries.get("m11_human_benchmark_claim_authorized"):
        out.append(STATUS_BLOCKED_HUMAN_BENCHMARK)
    if profile == PROFILE_OPERATOR_PREFLIGHT:
        out.append(STATUS_BLOCKED_RIGHTS)
    return out


def build_release_pack_body_operator_declared(
    evidence_path: Path,
    m08p: Path,
    m09p: Path,
    m10p: Path,
    m11p: Path,
    m05p: Path,
    m03p: Path,
) -> tuple[dict[str, Any], dict[str, Any]]:
    ev = _parse_release_evidence(evidence_path)
    summaries, bindings = _bind_operator_inputs(m08p, m09p, m10p, m11p, m05p, m03p)
    rights_declared = ev.get("rights_clearance_operator_declared")
    rights_bool = bool(rights_declared) if isinstance(rights_declared, bool) else False
    gates = _gates_operator(
        summaries,
        profile=PROFILE_OPERATOR_DECLARED,
        bindings=bindings,
        rights_declared=rights_bool,
    )
    status = _status_for_gates(gates, profile=PROFILE_OPERATOR_DECLARED)
    af = default_m12_authorization_flags()
    ev_public = {
        "contract_id": ev["contract_id"],
        "evidence_bundle_id": ev["evidence_bundle_id"],
        "operator_public_notes": ev.get("operator_public_notes"),
        "rights_clearance_operator_declared": ev.get("rights_clearance_operator_declared"),
    }
    body = {
        "contract_id": CONTRACT_ID_SHOWCASE_AGENT_RELEASE_PACK,
        "contract_version": CONTRACT_VERSION,
        "milestone_id": MILESTONE_ID_V15_M12,
        "profile_id": PROFILE_ID_SHOWCASE_RELEASE_PACK,
        "emit_profile": PROFILE_OPERATOR_DECLARED,
        "emitter_module": EMITTER_MODULE_SHOWCASE_RELEASE,
        "release_pack_id": f"v15_m12:operator_declared:{ev['evidence_bundle_id']}",
        "showcase_release_status": status,
        "showcase_release_status_secondary": _secondary_blockers(
            summaries, PROFILE_OPERATOR_DECLARED
        ),
        "candidate_identity_summary": {
            "candidate_checkpoint_id": summaries["m09_promotion_status"],
            "training_run_id": "not_emitted_in_m12",
            "logical_showcase_agent_id": ev["evidence_bundle_id"],
        },
        "upstream_bindings": bindings,
        "upstream_summaries": {
            "m08_campaign_completion": "valid_receipt"
            if summaries["m08_receipt_valid"]
            else "invalid_or_incomplete",
            "m09_promotion_status": summaries["m09_promotion_status"],
            "m10_demonstration_status": summaries["m10_demonstration_status"],
            "m11_claim_authorized": summaries["m11_human_benchmark_claim_authorized"],
            "m05_benchmark_executed": summaries["m05_benchmark_execution_performed"],
        },
        "release_gates": gates,
        "non_claims": list(NON_CLAIMS_V15_M12),
        "authorization_flags": af,
        "redaction_policy": {
            "operator_declared": "redact_paths_contacts_secrets_in_declared_fields",
        },
        "operator_declared_release_evidence": ev_public,
    }
    return body, ev_public


def seal_showcase_release_pack_body(body: dict[str, Any]) -> dict[str, Any]:
    base = {k: v for k, v in body.items() if k != _SEAL}
    digest = sha256_hex_of_canonical_json(base)
    sealed = dict(base)
    sealed[_SEAL] = digest
    return sealed


def build_showcase_release_pack_report(
    sealed: dict[str, Any], *, redaction_count: int
) -> dict[str, Any]:
    base = {k: v for k, v in sealed.items() if k != _SEAL}
    digest = sha256_hex_of_canonical_json(base)
    return {
        "report_kind": "v15_showcase_agent_release_pack_report",
        "report_version": REPORT_VERSION_SHOWCASE_RELEASE,
        "milestone": MILESTONE_ID_V15_M12,
        "artifact_sha256": digest,
        "seal_field": _SEAL,
        "seal_value_matches_artifact": sealed.get(_SEAL) == digest,
        "redaction_events": int(redaction_count),
        "primary_filename": FILENAME_SHOWCASE_RELEASE_PACK,
        "markdown_brief_filename": FILENAME_SHOWCASE_RELEASE_BRIEF_MD,
    }


def render_showcase_release_brief_md(sealed: dict[str, Any]) -> str:
    us = sealed.get("upstream_summaries")
    if not isinstance(us, dict):
        us = {}
    m08s = us.get("m08_campaign_completion", "")
    m09s = us.get("m09_promotion_status", "")
    m05s = us.get("m05_benchmark_executed", "")
    m10s = us.get("m10_demonstration_status", "")
    m11s = us.get("m11_claim_authorized", "")
    rights_line = (
        "- Default path: no public rights clearance for weights, replays, or participant materials."
    )
    lines: list[str] = [
        "# V15 Showcase Agent Release Brief",
        "",
        "This fixture release pack validates the governed release-pack artifact shape.",
        "It does not release a showcase agent or authorize public performance claims.",
        "",
        "## Release status",
        f"- `showcase_release_status`: `{sealed.get('showcase_release_status', '')}`",
        f"- `emit_profile`: `{sealed.get('emit_profile', '')}`",
        "",
        "## Candidate identity summary",
    ]
    cis = sealed.get("candidate_identity_summary")
    if isinstance(cis, dict):
        for k in sorted(cis.keys()):
            lines.append(f"- `{k}`: `{cis[k]}`")
    lines.extend(
        [
            "",
            "## Campaign evidence status",
            f"- M08 receipt (summary): `{m08s}`",
            "",
            "## Checkpoint promotion status",
            f"- M09 promotion_status (summary): `{m09s}`",
            "",
            "## Strong-agent scorecard status",
            f"- M05 benchmark executed (summary): `{m05s}`",
            "",
            "## Replay-native XAI status",
            f"- M10 demonstration_status (summary): `{m10s}`",
            "",
            "## Human-benchmark claim status",
            f"- M11 claim authorized (summary): `{m11s}`",
            "",
            "## Rights / public-private status",
            rights_line,
            "",
            "## Gate table",
        ]
    )
    gates = sealed.get("release_gates")
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
            "- None on the default fixture path; all authorization flags are false.",
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
            "## V13 / v2 boundary note",
            "- v2 go/no-go is **V15-M13**; this pack does not authorize v2.",
            "",
        ]
    )
    return "\n".join(lines) + "\n"


def emit_v15_showcase_agent_release_pack_fixture(
    output_dir: Path,
) -> tuple[dict[str, Any], dict[str, Any], Path, Path, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    body = build_release_pack_body_fixture()
    sealed = seal_showcase_release_pack_body(body)
    report = build_showcase_release_pack_report(sealed, redaction_count=0)
    md = render_showcase_release_brief_md(sealed)
    pj = output_dir / FILENAME_SHOWCASE_RELEASE_PACK
    pr = output_dir / REPORT_FILENAME_SHOWCASE_RELEASE_PACK
    pm = output_dir / FILENAME_SHOWCASE_RELEASE_BRIEF_MD
    pj.write_text(canonical_json_dumps(sealed), encoding="utf-8")
    pr.write_text(canonical_json_dumps(report), encoding="utf-8")
    pm.write_text(md, encoding="utf-8", newline="\n")
    return sealed, report, pj, pr, pm


def emit_v15_showcase_agent_release_pack_operator_preflight(
    output_dir: Path,
    m08: Path,
    m09: Path,
    m10: Path,
    m11: Path,
    m05: Path,
    m03: Path,
) -> tuple[dict[str, Any], dict[str, Any], Path, Path, Path]:
    body = build_release_pack_body_operator_preflight(m08, m09, m10, m11, m05, m03)
    sealed = seal_showcase_release_pack_body(body)
    report = build_showcase_release_pack_report(sealed, redaction_count=0)
    md = render_showcase_release_brief_md(sealed)
    output_dir.mkdir(parents=True, exist_ok=True)
    pj = output_dir / FILENAME_SHOWCASE_RELEASE_PACK
    pr = output_dir / REPORT_FILENAME_SHOWCASE_RELEASE_PACK
    pm = output_dir / FILENAME_SHOWCASE_RELEASE_BRIEF_MD
    pj.write_text(canonical_json_dumps(sealed), encoding="utf-8")
    pr.write_text(canonical_json_dumps(report), encoding="utf-8")
    pm.write_text(md, encoding="utf-8", newline="\n")
    return sealed, report, pj, pr, pm


def emit_v15_showcase_agent_release_pack_operator_declared(
    output_dir: Path,
    release_evidence: Path,
    m08: Path,
    m09: Path,
    m10: Path,
    m11: Path,
    m05: Path,
    m03: Path,
) -> tuple[dict[str, Any], dict[str, Any], int, Path, Path, Path]:
    body, ev_raw = build_release_pack_body_operator_declared(
        release_evidence, m08, m09, m10, m11, m05, m03
    )
    redacted_ev = redact_release_pack_value(ev_raw)
    if not isinstance(redacted_ev, dict):
        raise ValueError("redacted evidence must be object")
    body["operator_declared_release_evidence"] = redacted_ev
    redacted_body = dict(body)
    redacted_body["operator_declared_release_evidence"] = redacted_ev
    rc = _redaction_token_count(redacted_ev)
    sealed = seal_showcase_release_pack_body(redacted_body)
    report = build_showcase_release_pack_report(sealed, redaction_count=rc)
    md = render_showcase_release_brief_md(sealed)
    output_dir.mkdir(parents=True, exist_ok=True)
    pj = output_dir / FILENAME_SHOWCASE_RELEASE_PACK
    pr = output_dir / REPORT_FILENAME_SHOWCASE_RELEASE_PACK
    pm = output_dir / FILENAME_SHOWCASE_RELEASE_BRIEF_MD
    pj.write_text(canonical_json_dumps(sealed), encoding="utf-8")
    pr.write_text(canonical_json_dumps(report), encoding="utf-8")
    pm.write_text(md, encoding="utf-8", newline="\n")
    return sealed, report, rc, pj, pr, pm


__all__ = [
    "FORBIDDEN_BRIEF_SUBSTRINGS",
    "build_release_pack_body_fixture",
    "build_release_pack_body_operator_preflight",
    "build_release_pack_body_operator_declared",
    "build_showcase_release_pack_report",
    "emit_v15_showcase_agent_release_pack_fixture",
    "emit_v15_showcase_agent_release_pack_operator_declared",
    "emit_v15_showcase_agent_release_pack_operator_preflight",
    "redact_release_pack_value",
    "render_showcase_release_brief_md",
    "seal_showcase_release_pack_body",
]
