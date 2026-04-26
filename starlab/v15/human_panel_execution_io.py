"""Build, seal, and write V15-M11 human panel execution and human-benchmark claim decision JSON."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Final

from starlab.runs.json_util import canonical_json_dumps, sha256_hex_of_canonical_json
from starlab.v15.checkpoint_evaluation_io import m08_campaign_receipt_valid_for_m09
from starlab.v15.checkpoint_evaluation_models import (
    CONTRACT_ID_CHECKPOINT_PROMOTION_DECISION,
    PROMOTION_STATUS_BLOCKED,
    PROMOTION_STATUS_NOT_PROMOTED,
    PROMOTION_STATUS_PROMOTED_CANDIDATE,
    PROMOTION_STATUS_PROMOTED_XAI,
)
from starlab.v15.checkpoint_lineage_models import CONTRACT_ID_CHECKPOINT_LINEAGE
from starlab.v15.human_panel_benchmark_io import redact_path_and_contact_in_value
from starlab.v15.human_panel_benchmark_models import (
    CONTRACT_ID_HUMAN_PANEL_BENCHMARK,
    PROTOCOL_PROFILE_ID_HUMAN_PANEL,
    THRESHOLD_OPTION_IDS,
)
from starlab.v15.human_panel_execution_models import (
    ALL_HUMAN_PANEL_GATE_IDS,
    CLAIM_DECISION_AUTH_BOUNDED,
    CLAIM_DECISION_BLOCKED_NO_EXEC,
    CLAIM_DECISION_BLOCKED_PROMOTED_CP,
    CLAIM_DECISION_BLOCKED_THRESHOLD,
    CLAIM_DECISION_EVALUATED_NOT_AUTH,
    CONTRACT_ID_HUMAN_BENCHMARK_CLAIM_DECISION,
    CONTRACT_ID_HUMAN_PANEL_EXECUTION,
    CONTRACT_VERSION,
    EMITTER_MODULE_HUMAN_BENCHMARK_CLAIM_DECISION,
    EMITTER_MODULE_HUMAN_PANEL_EXECUTION,
    FILENAME_HUMAN_BENCHMARK_CLAIM_DECISION,
    FILENAME_HUMAN_PANEL_EXECUTION,
    FIXTURE_CLAIM_DECISION_ID,
    FIXTURE_EXECUTION_ID,
    GATE_STATUS_BLOCKED,
    GATE_STATUS_NOT_EVALUATED,
    GATE_STATUS_PASS,
    GATE_STATUS_WARNING,
    HUMAN_PANEL_STATUS_BLOCKED_M08,
    HUMAN_PANEL_STATUS_BLOCKED_PROMOTED_CP,
    HUMAN_PANEL_STATUS_FIXTURE_ONLY,
    HUMAN_PANEL_STATUS_OP_EXEC_DECLARED,
    HUMAN_PANEL_STATUS_OP_PANEL_EVIDENCE,
    MILESTONE_ID_V15_M11,
    NON_CLAIMS_V15_M11_CLAIM,
    NON_CLAIMS_V15_M11_EXECUTION,
    PLACEHOLDER_SHA256,
    PROFILE_FIXTURE_CI,
    PROFILE_ID_HUMAN_BENCHMARK_CLAIM,
    PROFILE_ID_HUMAN_PANEL_EXECUTION,
    PROFILE_OPERATOR_DECLARED,
    PROFILE_OPERATOR_PREFLIGHT,
    REPORT_FILENAME_HUMAN_BENCHMARK_CLAIM_DECISION,
    REPORT_FILENAME_HUMAN_PANEL_EXECUTION,
    REPORT_VERSION_HUMAN_BENCHMARK_CLAIM,
    REPORT_VERSION_HUMAN_PANEL_EXECUTION,
    SEAL_KEY_HUMAN_BENCHMARK_CLAIM_DECISION,
    SEAL_KEY_HUMAN_PANEL_EXECUTION,
    default_m11_authorization_flags,
)
from starlab.v15.long_gpu_training_manifest_models import CONTRACT_ID_LONG_GPU_CAMPAIGN_RECEIPT
from starlab.v15.strong_agent_scorecard_models import CONTRACT_ID_STRONG_AGENT_SCORECARD
from starlab.v15.training_run_receipt_io import _redaction_token_count
from starlab.v15.xai_demonstration_models import CONTRACT_ID_REPLAY_NATIVE_XAI_DEMONSTRATION

SEAL_HPE = SEAL_KEY_HUMAN_PANEL_EXECUTION
SEAL_HBC = SEAL_KEY_HUMAN_BENCHMARK_CLAIM_DECISION

PANEL_EVIDENCE_ALLOWED_KEYS: Final[frozenset[str]] = frozenset(
    {
        "evidence_id",
        "participant_count",
        "participant_tier_summary",
        "match_count",
        "replay_capture_status",
        "threshold_policy_id",
        "threshold_frozen",
        "privacy_profile_id",
        "anonymized_participant_ids",
        "operator_notes",
    }
)
_HEX64 = re.compile(r"^[0-9a-fA-F]{64}$")


def _json_file_canonical_sha256(path: Path) -> str:
    raw = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ValueError("JSON must be a single object")
    return sha256_hex_of_canonical_json(raw)


def _require_contract(obj: dict[str, Any], expected: str, ctx: str) -> None:
    if str(obj.get("contract_id", "")) != expected:
        raise ValueError(f"{ctx} contract_id must be {expected!r} (got {obj.get('contract_id')!r})")


def _parse_panel_evidence(path: Path) -> dict[str, Any]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ValueError("panel evidence JSON must be a single object")
    unknown = set(raw) - PANEL_EVIDENCE_ALLOWED_KEYS
    if unknown:
        raise ValueError(f"panel evidence: unknown keys {sorted(unknown)}")
    for tid in (raw.get("threshold_policy_id"),):
        if isinstance(tid, str) and tid and tid not in THRESHOLD_OPTION_IDS:
            raise ValueError(
                f"panel evidence: threshold_policy_id {tid!r} not in M06 THRESHOLD_OPTION_IDS"
            )
    return raw


def _g(gate_id: str, status: str, notes: str) -> dict[str, Any]:
    return {"gate_id": gate_id, "status": status, "notes": notes}


def _fixture_h12_gates() -> list[dict[str, Any]]:
    gs = GATE_STATUS_PASS
    gb = GATE_STATUS_BLOCKED
    gne = GATE_STATUS_NOT_EVALUATED
    return [
        _g(
            ALL_HUMAN_PANEL_GATE_IDS[0],
            gs,
            "Fixture CI artifact: deterministic M11 schema; sealed.",
        ),
        _g(
            ALL_HUMAN_PANEL_GATE_IDS[1],
            gb,
            "M06 protocol: fixture placeholder SHA; not operator-bound.",
        ),
        _g(
            ALL_HUMAN_PANEL_GATE_IDS[2],
            gb,
            (
                "H2: blocked_missing_promoted_checkpoint — M09 posture: no checkpoint promoted for "
                "downstream human panel on default path."
            ),
        ),
        _g(
            ALL_HUMAN_PANEL_GATE_IDS[3],
            gb,
            (
                "H3: blocked_missing_m08_campaign_receipt — no valid long-campaign completion "
                "receipt on default honest path."
            ),
        ),
        _g(
            ALL_HUMAN_PANEL_GATE_IDS[4],
            gb,
            "H4: participant privacy review not completed for a real panel in CI/fixture default.",
        ),
        _g(
            ALL_HUMAN_PANEL_GATE_IDS[5],
            gne,
            "H5: participant tier coverage not executed (no real roster).",
        ),
        _g(
            ALL_HUMAN_PANEL_GATE_IDS[6],
            gne,
            "H6: match schedule not executed (no real matches in CI).",
        ),
        _g(
            ALL_HUMAN_PANEL_GATE_IDS[7],
            gb,
            "H7: replay capture blocked — no real replay package on default path.",
        ),
        _g(
            ALL_HUMAN_PANEL_GATE_IDS[8],
            gne,
            "H8: result integrity not established (no real match results).",
        ),
        _g(
            ALL_HUMAN_PANEL_GATE_IDS[9],
            gb,
            "H9: threshold policy not frozen for a real human benchmark run.",
        ),
        _g(
            ALL_HUMAN_PANEL_GATE_IDS[10],
            gb,
            "H10: XAI sample / M10 binding is fixture placeholder on default path.",
        ),
        _g(
            ALL_HUMAN_PANEL_GATE_IDS[11],
            gs,
            "H11: public artifact has no absolute paths (fixture).",
        ),
        _g(
            ALL_HUMAN_PANEL_GATE_IDS[12],
            gs,
            "H12: non-claim language present; no live execution in CI default.",
        ),
    ]


def build_human_panel_execution_body_fixture() -> dict[str, Any]:
    af = default_m11_authorization_flags()
    return {
        "contract_id": CONTRACT_ID_HUMAN_PANEL_EXECUTION,
        "contract_version": CONTRACT_VERSION,
        "profile_id": PROFILE_ID_HUMAN_PANEL_EXECUTION,
        "profile": PROFILE_FIXTURE_CI,
        "milestone": MILESTONE_ID_V15_M11,
        "created_by": EMITTER_MODULE_HUMAN_PANEL_EXECUTION,
        "execution_id": FIXTURE_EXECUTION_ID,
        "human_panel_status": HUMAN_PANEL_STATUS_FIXTURE_ONLY,
        "secondary_statuses": [
            HUMAN_PANEL_STATUS_BLOCKED_PROMOTED_CP,
            HUMAN_PANEL_STATUS_BLOCKED_M08,
        ],
        "blocked_path_reasons": [
            HUMAN_PANEL_STATUS_FIXTURE_ONLY,
            HUMAN_PANEL_STATUS_BLOCKED_PROMOTED_CP,
            "no_operator_declared_panel_evidence",
        ],
        "m06_human_panel_benchmark_binding": {
            "contract_id": CONTRACT_ID_HUMAN_PANEL_BENCHMARK,
            "protocol_profile_id": PROTOCOL_PROFILE_ID_HUMAN_PANEL,
            "human_panel_benchmark_json_canonical_sha256": PLACEHOLDER_SHA256,
            "binding_status": "fixture_placeholder",
        },
        "m09_promotion_decision_binding": {
            "contract_id": CONTRACT_ID_CHECKPOINT_PROMOTION_DECISION,
            "promotion_decision_json_canonical_sha256": PLACEHOLDER_SHA256,
            "binding_status": "fixture_placeholder",
        },
        "m10_replay_native_xai_demonstration_binding": {
            "contract_id": CONTRACT_ID_REPLAY_NATIVE_XAI_DEMONSTRATION,
            "replay_native_xai_demonstration_json_canonical_sha256": PLACEHOLDER_SHA256,
            "binding_status": "fixture_placeholder",
        },
        "m08_campaign_receipt_binding": {
            "contract_id": CONTRACT_ID_LONG_GPU_CAMPAIGN_RECEIPT,
            "m08_campaign_receipt_json_canonical_sha256": PLACEHOLDER_SHA256,
            "binding_status": "not_applicable_fixture",
        },
        "m05_strong_agent_scorecard_binding": {
            "contract_id": CONTRACT_ID_STRONG_AGENT_SCORECARD,
            "strong_agent_scorecard_json_canonical_sha256": PLACEHOLDER_SHA256,
            "binding_status": "not_applicable_fixture",
        },
        "m03_checkpoint_lineage_binding": {
            "contract_id": CONTRACT_ID_CHECKPOINT_LINEAGE,
            "checkpoint_lineage_manifest_json_canonical_sha256": PLACEHOLDER_SHA256,
            "binding_status": "not_applicable_fixture",
        },
        "panel_evidence_summary": {
            "evidence_status": "fixture_only",
            "participant_count": 0,
            "match_count": 0,
        },
        "human_panel_gates": _fixture_h12_gates(),
        "upstream_m09_promotion_status": "blocked",
        "non_claims": list(NON_CLAIMS_V15_M11_EXECUTION),
        "authorization_flags": af,
    }


def seal_human_panel_execution_body(body: dict[str, Any]) -> dict[str, Any]:
    out = {k: v for k, v in body.items() if k != SEAL_HPE}
    digest = sha256_hex_of_canonical_json(out)
    sealed = dict(out)
    sealed[SEAL_HPE] = digest
    return sealed


def build_human_panel_execution_report(
    sealed: dict[str, Any], *, redaction_count: int
) -> dict[str, Any]:
    base = {k: v for k, v in sealed.items() if k != SEAL_HPE}
    digest = sha256_hex_of_canonical_json(base)
    return {
        "report_kind": "v15_human_panel_execution_report",
        "report_version": REPORT_VERSION_HUMAN_PANEL_EXECUTION,
        "milestone": MILESTONE_ID_V15_M11,
        "artifact_sha256": digest,
        "seal_field": SEAL_HPE,
        "seal_value_matches_artifact": sealed.get(SEAL_HPE) == digest,
        "redaction_events": int(redaction_count),
        "primary_filename": FILENAME_HUMAN_PANEL_EXECUTION,
    }


def _extract_promotion_status(m09: dict[str, Any]) -> str:
    return str(m09.get("promotion_status", "blocked"))


def _gates_operator(
    *, profile: str, m09: dict[str, Any], m08: dict[str, Any] | None, has_panel: bool
) -> list[dict[str, Any]]:
    """Compute H0–H12 for non-fixture paths (deterministic; flags remain false on default)."""
    promo = _extract_promotion_status(m09)
    m08_ok = False
    if m08 is not None:
        m08_ok = m08_campaign_receipt_valid_for_m09(m08)
    if profile == PROFILE_OPERATOR_DECLARED and m08 is not None:
        raise ValueError("operator_declared does not bind M08 (use operator_preflight for M08)")

    gpass = GATE_STATUS_PASS
    gblk = GATE_STATUS_BLOCKED
    gw = GATE_STATUS_WARNING
    gne = GATE_STATUS_NOT_EVALUATED

    h2 = (
        gpass
        if promo in (PROMOTION_STATUS_PROMOTED_XAI, PROMOTION_STATUS_PROMOTED_CANDIDATE)
        else gblk
    )
    h2_note = (
        "M09 promotion status allows downstream routing label (not a strength claim)."
        if h2 == gpass
        else f"M09 promotion_status={promo!r}: no promoted checkpoint for human panel binding."
    )
    h3 = gpass if m08_ok else gblk
    h3_note = (
        "M08 campaign receipt present with completion markers (operator-local evidence only)."
        if m08_ok
        else (
            "H3: no valid M08 long-campaign completion receipt; "
            "human panel not unblocked by receipt."
        )
    )
    h4 = gblk if not has_panel else gw
    h4_note = (
        "Panel evidence object supplied (privacy review still not proven by M11 default)."
        if has_panel
        else "H4: no operator panel evidence package; privacy / consent posture not reviewed here."
    )

    if profile == PROFILE_OPERATOR_PREFLIGHT:
        return [
            _g(
                ALL_HUMAN_PANEL_GATE_IDS[0],
                gpass,
                "Preflight: JSON objects parsed; contract_ids checked.",
            ),
            _g(ALL_HUMAN_PANEL_GATE_IDS[1], gpass, "M06 protocol JSON bound by canonical SHA-256."),
            _g(ALL_HUMAN_PANEL_GATE_IDS[2], h2, h2_note),
            _g(ALL_HUMAN_PANEL_GATE_IDS[3], h3, h3_note),
            _g(ALL_HUMAN_PANEL_GATE_IDS[4], h4, h4_note),
            _g(
                ALL_HUMAN_PANEL_GATE_IDS[5],
                gne,
                "H5: roster tier coverage not proven by JSON-only preflight.",
            ),
            _g(
                ALL_HUMAN_PANEL_GATE_IDS[6],
                gne,
                "H6: match schedule not proven without execution receipts.",
            ),
            _g(
                ALL_HUMAN_PANEL_GATE_IDS[7],
                gblk,
                "H7: replay capture not attested in repository tooling.",
            ),
            _g(
                ALL_HUMAN_PANEL_GATE_IDS[8],
                gne,
                "H8: aggregate results not integrity-verified in M11 default.",
            ),
            _g(
                ALL_HUMAN_PANEL_GATE_IDS[9],
                gblk,
                "H9: threshold must be operator-frozen; not authorized here.",
            ),
            _g(
                ALL_HUMAN_PANEL_GATE_IDS[10],
                gpass,
                "M10 JSON bound by SHA (demonstration/reporting only).",
            ),
            _g(
                ALL_HUMAN_PANEL_GATE_IDS[11],
                gpass,
                "Path/contact redaction applied to operator inputs for emission.",
            ),
            _g(
                ALL_HUMAN_PANEL_GATE_IDS[12],
                gpass,
                "Non-claim boundary preserved; no CI human execution.",
            ),
        ]
    # operator_declared
    h3_decl = gblk
    h3n = "H3: M08 campaign receipt not part of operator_declared M11 input set; preflight for M08."
    return [
        _g(ALL_HUMAN_PANEL_GATE_IDS[0], gpass, "Operator-declared: artifacts parsed and sealed."),
        _g(
            ALL_HUMAN_PANEL_GATE_IDS[1],
            gpass,
            "M06 human panel benchmark protocol bound by canonical SHA-256.",
        ),
        _g(ALL_HUMAN_PANEL_GATE_IDS[2], h2, h2_note),
        _g(ALL_HUMAN_PANEL_GATE_IDS[3], h3_decl, h3n),
        _g(ALL_HUMAN_PANEL_GATE_IDS[4], h4, h4_note),
        _g(
            ALL_HUMAN_PANEL_GATE_IDS[5],
            gne,
            "H5: participant tier coverage not established from public JSON.",
        ),
        _g(ALL_HUMAN_PANEL_GATE_IDS[6], gne, "H6: match schedule not established."),
        _g(ALL_HUMAN_PANEL_GATE_IDS[7], gblk, "H7: replay capture not verified; default blocked."),
        _g(
            ALL_HUMAN_PANEL_GATE_IDS[8],
            gne,
            "H8: match results not integrity-verified in default posture.",
        ),
        _g(
            ALL_HUMAN_PANEL_GATE_IDS[9],
            gblk,
            "H9: threshold freeze not public claim without governance review.",
        ),
        _g(
            ALL_HUMAN_PANEL_GATE_IDS[10],
            gpass,
            "M10 replay-native XAI JSON bound by SHA-256 (not inference).",
        ),
        _g(
            ALL_HUMAN_PANEL_GATE_IDS[11],
            gpass,
            "Redaction policy applied to emitted operator bundle.",
        ),
        _g(
            ALL_HUMAN_PANEL_GATE_IDS[12],
            gpass,
            "M11 non-claims: no real human panel execution in CI default.",
        ),
    ]


def _human_panel_status_for_operator(
    m09: dict[str, Any], has_panel: bool, panel: dict[str, Any] | None
) -> str:
    promo = _extract_promotion_status(m09)
    if promo in (PROMOTION_STATUS_BLOCKED, PROMOTION_STATUS_NOT_PROMOTED, "blocked", ""):
        return HUMAN_PANEL_STATUS_BLOCKED_PROMOTED_CP
    if not has_panel:
        return HUMAN_PANEL_STATUS_OP_PANEL_EVIDENCE
    if panel and panel.get("threshold_frozen") is True and panel.get("match_count", 0) > 0:
        return HUMAN_PANEL_STATUS_OP_EXEC_DECLARED
    return HUMAN_PANEL_STATUS_OP_PANEL_EVIDENCE


def build_operator_declared_body(
    m06: dict[str, Any],
    m09: dict[str, Any],
    m10: dict[str, Any],
    panel: dict[str, Any],
    m06_path: Path,
    m09_path: Path,
    m10_path: Path,
    panel_path: Path,
) -> dict[str, Any]:
    _require_contract(m06, CONTRACT_ID_HUMAN_PANEL_BENCHMARK, "M06")
    if str(m06.get("protocol_profile_id", "")) != PROTOCOL_PROFILE_ID_HUMAN_PANEL:
        raise ValueError(
            "M06 protocol_profile_id must match starlab.v15.human_panel_benchmark_protocol.v1"
        )
    _require_contract(m09, CONTRACT_ID_CHECKPOINT_PROMOTION_DECISION, "M09")
    _require_contract(m10, CONTRACT_ID_REPLAY_NATIVE_XAI_DEMONSTRATION, "M10")
    s06 = _json_file_canonical_sha256(m06_path)
    s09 = _json_file_canonical_sha256(m09_path)
    s10 = _json_file_canonical_sha256(m10_path)
    _ = _json_file_canonical_sha256(panel_path)  # validate parseable
    af = default_m11_authorization_flags()
    pr_panel = {
        "participant_count": int(panel.get("participant_count", 0)),
        "match_count": int(panel.get("match_count", 0)),
        "replay_capture_status": str(panel.get("replay_capture_status", "not_evaluated")),
        "threshold_policy_id": str(
            panel.get("threshold_policy_id", "no_claim_without_threshold_freeze")
        ),
        "threshold_frozen": bool(panel.get("threshold_frozen", False)),
        "privacy_profile_id": str(panel.get("privacy_profile_id", "not_stated")),
    }
    st = _human_panel_status_for_operator(m09, True, panel)
    return {
        "contract_id": CONTRACT_ID_HUMAN_PANEL_EXECUTION,
        "contract_version": CONTRACT_VERSION,
        "profile_id": PROFILE_ID_HUMAN_PANEL_EXECUTION,
        "profile": PROFILE_OPERATOR_DECLARED,
        "milestone": MILESTONE_ID_V15_M11,
        "created_by": EMITTER_MODULE_HUMAN_PANEL_EXECUTION,
        "execution_id": "v15_m11:operator_declared:deterministic",
        "human_panel_status": st,
        "secondary_statuses": [
            HUMAN_PANEL_STATUS_BLOCKED_M08,
            HUMAN_PANEL_STATUS_BLOCKED_PROMOTED_CP,
        ]
        if _extract_promotion_status(m09)
        in (PROMOTION_STATUS_BLOCKED, PROMOTION_STATUS_NOT_PROMOTED, "blocked", "")
        else [HUMAN_PANEL_STATUS_BLOCKED_M08],
        "blocked_path_reasons": [
            f"promotion={_extract_promotion_status(m09)}",
            "m08_receipt_not_in_operator_declared_profile",
        ],
        "m06_human_panel_benchmark_binding": {
            "contract_id": CONTRACT_ID_HUMAN_PANEL_BENCHMARK,
            "protocol_profile_id": PROTOCOL_PROFILE_ID_HUMAN_PANEL,
            "human_panel_benchmark_json_canonical_sha256": s06,
            "binding_status": "bound",
        },
        "m09_promotion_decision_binding": {
            "contract_id": CONTRACT_ID_CHECKPOINT_PROMOTION_DECISION,
            "promotion_decision_json_canonical_sha256": s09,
            "binding_status": "bound",
        },
        "m10_replay_native_xai_demonstration_binding": {
            "contract_id": CONTRACT_ID_REPLAY_NATIVE_XAI_DEMONSTRATION,
            "replay_native_xai_demonstration_json_canonical_sha256": s10,
            "binding_status": "bound",
        },
        "m08_campaign_receipt_binding": {
            "contract_id": CONTRACT_ID_LONG_GPU_CAMPAIGN_RECEIPT,
            "m08_campaign_receipt_json_canonical_sha256": PLACEHOLDER_SHA256,
            "binding_status": "not_bound_operator_declared",
        },
        "m05_strong_agent_scorecard_binding": {
            "contract_id": CONTRACT_ID_STRONG_AGENT_SCORECARD,
            "strong_agent_scorecard_json_canonical_sha256": PLACEHOLDER_SHA256,
            "binding_status": "not_bound_operator_declared",
        },
        "m03_checkpoint_lineage_binding": {
            "contract_id": CONTRACT_ID_CHECKPOINT_LINEAGE,
            "checkpoint_lineage_manifest_json_canonical_sha256": PLACEHOLDER_SHA256,
            "binding_status": "not_bound_operator_declared",
        },
        "panel_evidence_summary": pr_panel,
        "human_panel_gates": _gates_operator(
            profile=PROFILE_OPERATOR_DECLARED, m09=m09, m08=None, has_panel=True
        ),
        "upstream_m09_promotion_status": _extract_promotion_status(m09),
        "non_claims": list(NON_CLAIMS_V15_M11_EXECUTION),
        "authorization_flags": af,
    }


def build_operator_preflight_body(
    m06: dict[str, Any],
    m09: dict[str, Any],
    m10: dict[str, Any],
    m08: dict[str, Any],
    m05: dict[str, Any],
    m03: dict[str, Any],
    panel: dict[str, Any],
    paths: tuple[Path, ...],
) -> dict[str, Any]:
    m06p, m09p, m10p, m08p, m05p, m03p, panelp = paths
    _require_contract(m06, CONTRACT_ID_HUMAN_PANEL_BENCHMARK, "M06")
    _require_contract(m09, CONTRACT_ID_CHECKPOINT_PROMOTION_DECISION, "M09")
    _require_contract(m10, CONTRACT_ID_REPLAY_NATIVE_XAI_DEMONSTRATION, "M10")
    _require_contract(m08, CONTRACT_ID_LONG_GPU_CAMPAIGN_RECEIPT, "M08")
    _require_contract(m05, CONTRACT_ID_STRONG_AGENT_SCORECARD, "M05")
    _require_contract(m03, CONTRACT_ID_CHECKPOINT_LINEAGE, "M03")
    s06 = _json_file_canonical_sha256(m06p)
    s09 = _json_file_canonical_sha256(m09p)
    s10 = _json_file_canonical_sha256(m10p)
    s08 = _json_file_canonical_sha256(m08p)
    s05 = _json_file_canonical_sha256(m05p)
    s03 = _json_file_canonical_sha256(m03p)
    _ = _json_file_canonical_sha256(panelp)
    m08_ok = m08_campaign_receipt_valid_for_m09(m08)
    af = default_m11_authorization_flags()
    st = _human_panel_status_for_operator(m09, True, panel)
    return {
        "contract_id": CONTRACT_ID_HUMAN_PANEL_EXECUTION,
        "contract_version": CONTRACT_VERSION,
        "profile_id": PROFILE_ID_HUMAN_PANEL_EXECUTION,
        "profile": PROFILE_OPERATOR_PREFLIGHT,
        "milestone": MILESTONE_ID_V15_M11,
        "created_by": EMITTER_MODULE_HUMAN_PANEL_EXECUTION,
        "execution_id": "v15_m11:operator_preflight:deterministic",
        "human_panel_status": st,
        "secondary_statuses": [HUMAN_PANEL_STATUS_BLOCKED_PROMOTED_CP]
        if not m08_ok
        else [HUMAN_PANEL_STATUS_OP_PANEL_EVIDENCE],
        "blocked_path_reasons": ([] if m08_ok else [HUMAN_PANEL_STATUS_BLOCKED_M08])
        + [f"promotion={_extract_promotion_status(m09)}"],
        "m06_human_panel_benchmark_binding": {
            "contract_id": CONTRACT_ID_HUMAN_PANEL_BENCHMARK,
            "protocol_profile_id": PROTOCOL_PROFILE_ID_HUMAN_PANEL,
            "human_panel_benchmark_json_canonical_sha256": s06,
            "binding_status": "bound",
        },
        "m09_promotion_decision_binding": {
            "contract_id": CONTRACT_ID_CHECKPOINT_PROMOTION_DECISION,
            "promotion_decision_json_canonical_sha256": s09,
            "binding_status": "bound",
        },
        "m10_replay_native_xai_demonstration_binding": {
            "contract_id": CONTRACT_ID_REPLAY_NATIVE_XAI_DEMONSTRATION,
            "replay_native_xai_demonstration_json_canonical_sha256": s10,
            "binding_status": "bound",
        },
        "m08_campaign_receipt_binding": {
            "contract_id": CONTRACT_ID_LONG_GPU_CAMPAIGN_RECEIPT,
            "m08_campaign_receipt_json_canonical_sha256": s08,
            "binding_status": "bound" if m08_ok else "bound_not_valid_for_m09",
        },
        "m05_strong_agent_scorecard_binding": {
            "contract_id": CONTRACT_ID_STRONG_AGENT_SCORECARD,
            "strong_agent_scorecard_json_canonical_sha256": s05,
            "binding_status": "bound",
        },
        "m03_checkpoint_lineage_binding": {
            "contract_id": CONTRACT_ID_CHECKPOINT_LINEAGE,
            "checkpoint_lineage_manifest_json_canonical_sha256": s03,
            "binding_status": "bound",
        },
        "panel_evidence_summary": {
            "participant_count": int(panel.get("participant_count", 0)),
            "match_count": int(panel.get("match_count", 0)),
            "threshold_frozen": bool(panel.get("threshold_frozen", False)),
        },
        "human_panel_gates": _gates_operator(
            profile=PROFILE_OPERATOR_PREFLIGHT, m09=m09, m08=m08, has_panel=True
        ),
        "upstream_m09_promotion_status": _extract_promotion_status(m09),
        "non_claims": list(NON_CLAIMS_V15_M11_EXECUTION),
        "authorization_flags": af,
    }


def emit_v15_human_panel_execution_fixture(
    out_dir: Path,
) -> tuple[dict[str, Any], dict[str, Any], int, Path, Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    body = build_human_panel_execution_body_fixture()
    sealed = seal_human_panel_execution_body(body)
    rep = build_human_panel_execution_report(sealed, redaction_count=0)
    p_sealed = {**sealed}
    p1 = out_dir / FILENAME_HUMAN_PANEL_EXECUTION
    p2 = out_dir / REPORT_FILENAME_HUMAN_PANEL_EXECUTION
    p1.write_text(canonical_json_dumps(p_sealed), encoding="utf-8")
    p2.write_text(canonical_json_dumps(rep), encoding="utf-8")
    return sealed, rep, 0, p1, p2


def emit_v15_human_panel_execution_operator_declared(
    out_dir: Path,
    m06: Path,
    m09: Path,
    m10: Path,
    panel: Path,
) -> tuple[dict[str, Any], dict[str, Any], int, Path, Path]:
    m06d = json.loads(m06.read_text(encoding="utf-8"))
    m09d = json.loads(m09.read_text(encoding="utf-8"))
    m10d = json.loads(m10.read_text(encoding="utf-8"))
    if not isinstance(m06d, dict) or not isinstance(m09d, dict) or not isinstance(m10d, dict):
        raise ValueError("M06/M09/M10 JSON must be single objects")
    pan = _parse_panel_evidence(panel)
    body = build_operator_declared_body(m06d, m09d, m10d, pan, m06, m09, m10, panel)
    red_body = redact_path_and_contact_in_value(body)
    rc = _redaction_token_count(red_body)
    sealed = seal_human_panel_execution_body(red_body)
    rpt = build_human_panel_execution_report(sealed, redaction_count=rc)
    out_dir.mkdir(parents=True, exist_ok=True)
    p1 = out_dir / FILENAME_HUMAN_PANEL_EXECUTION
    p2 = out_dir / REPORT_FILENAME_HUMAN_PANEL_EXECUTION
    p1.write_text(canonical_json_dumps(sealed), encoding="utf-8")
    p2.write_text(canonical_json_dumps(rpt), encoding="utf-8")
    return sealed, rpt, rc, p1, p2


def emit_v15_human_panel_execution_operator_preflight(
    out_dir: Path,
    m06: Path,
    m09: Path,
    m10: Path,
    m08: Path,
    m05: Path,
    m03: Path,
    panel: Path,
) -> tuple[dict[str, Any], dict[str, Any], int, Path, Path]:
    m06d = json.loads(m06.read_text(encoding="utf-8"))
    m09d = json.loads(m09.read_text(encoding="utf-8"))
    m10d = json.loads(m10.read_text(encoding="utf-8"))
    m08d = json.loads(m08.read_text(encoding="utf-8"))
    m05d = json.loads(m05.read_text(encoding="utf-8"))
    m03d = json.loads(m03.read_text(encoding="utf-8"))
    for d, name in [
        (m06d, "M06"),
        (m09d, "M09"),
        (m10d, "M10"),
        (m08d, "M08"),
        (m05d, "M05"),
        (m03d, "M03"),
    ]:
        if not isinstance(d, dict):
            raise ValueError(f"{name} JSON must be a single object")
    pan = _parse_panel_evidence(panel)
    body = build_operator_preflight_body(
        m06d,
        m09d,
        m10d,
        m08d,
        m05d,
        m03d,
        pan,
        (m06, m09, m10, m08, m05, m03, panel),
    )
    red_body = redact_path_and_contact_in_value(body)
    rc = _redaction_token_count(red_body)
    sealed = seal_human_panel_execution_body(red_body)
    rpt = build_human_panel_execution_report(sealed, redaction_count=rc)
    out_dir.mkdir(parents=True, exist_ok=True)
    p1 = out_dir / FILENAME_HUMAN_PANEL_EXECUTION
    p2 = out_dir / REPORT_FILENAME_HUMAN_PANEL_EXECUTION
    p1.write_text(canonical_json_dumps(sealed), encoding="utf-8")
    p2.write_text(canonical_json_dumps(rpt), encoding="utf-8")
    return sealed, rpt, rc, p1, p2


def derive_claim_decision_label(execution: dict[str, Any]) -> str:
    prof = str(execution.get("profile", ""))
    flags = execution.get("authorization_flags")
    if not isinstance(flags, dict):
        flags = default_m11_authorization_flags()
    if flags.get("human_benchmark_claim_authorized"):
        return CLAIM_DECISION_AUTH_BOUNDED
    if (
        prof == PROFILE_FIXTURE_CI
        or execution.get("human_panel_status") == HUMAN_PANEL_STATUS_FIXTURE_ONLY
    ):
        return CLAIM_DECISION_EVALUATED_NOT_AUTH
    promo = str(execution.get("upstream_m09_promotion_status", ""))
    if promo in (
        PROMOTION_STATUS_BLOCKED,
        PROMOTION_STATUS_NOT_PROMOTED,
        "blocked",
        "evaluated_not_promoted",
        "",
    ):
        return CLAIM_DECISION_BLOCKED_PROMOTED_CP
    psum = execution.get("panel_evidence_summary")
    if (
        isinstance(psum, dict)
        and psum.get("threshold_frozen") is False
        and prof in (PROFILE_OPERATOR_DECLARED, PROFILE_OPERATOR_PREFLIGHT)
    ):
        return CLAIM_DECISION_BLOCKED_THRESHOLD
    if not flags.get("human_panel_execution_performed", False):
        return CLAIM_DECISION_BLOCKED_NO_EXEC
    return CLAIM_DECISION_EVALUATED_NOT_AUTH


def _claim_mirroring_gates(execution: dict[str, Any]) -> list[dict[str, Any]]:
    hg = execution.get("human_panel_gates")
    if not isinstance(hg, list):
        return []
    return [dict(x) for x in hg if isinstance(x, dict)]


def build_human_benchmark_claim_decision_body(execution: dict[str, Any]) -> dict[str, Any]:
    ex2 = {k: v for k, v in execution.items() if k not in (SEAL_HPE, SEAL_HBC)}
    sh = sha256_hex_of_canonical_json(ex2)
    label = derive_claim_decision_label(execution)
    af0 = execution.get("authorization_flags")
    af: dict[str, bool] = (
        {k: bool(v) for k, v in af0.items()}
        if isinstance(af0, dict)
        else default_m11_authorization_flags()
    )
    for k, d in default_m11_authorization_flags().items():
        af.setdefault(k, d)
    return {
        "contract_id": CONTRACT_ID_HUMAN_BENCHMARK_CLAIM_DECISION,
        "contract_version": CONTRACT_VERSION,
        "profile_id": PROFILE_ID_HUMAN_BENCHMARK_CLAIM,
        "milestone": MILESTONE_ID_V15_M11,
        "created_by": EMITTER_MODULE_HUMAN_BENCHMARK_CLAIM_DECISION,
        "claim_decision_id": FIXTURE_CLAIM_DECISION_ID,
        "source_contract_id": CONTRACT_ID_HUMAN_PANEL_EXECUTION,
        "source_execution_sha256": sh,
        "claim_decision_label": label,
        "decision_gates": _claim_mirroring_gates(execution),
        "authorization_flags": af,
        "non_claims": list(NON_CLAIMS_V15_M11_CLAIM),
    }


def validate_strict_execution_bindings(execution: dict[str, Any]) -> None:
    for key, subkey in [
        ("m06_human_panel_benchmark_binding", "human_panel_benchmark_json_canonical_sha256"),
        ("m09_promotion_decision_binding", "promotion_decision_json_canonical_sha256"),
        (
            "m10_replay_native_xai_demonstration_binding",
            "replay_native_xai_demonstration_json_canonical_sha256",
        ),
    ]:
        b = execution.get(key)
        if not isinstance(b, dict):
            raise ValueError(f"strict: missing {key}")
        hx = str(b.get(subkey, ""))
        if not _HEX64.match(hx) or hx == PLACEHOLDER_SHA256:
            raise ValueError(f"strict: {key} must have non-placeholder 64-hex {subkey}")


def seal_benchmark_claim_decision_body(body: dict[str, Any]) -> dict[str, Any]:
    out = {k: v for k, v in body.items() if k != SEAL_HBC}
    d = sha256_hex_of_canonical_json(out)
    s = dict(out)
    s[SEAL_HBC] = d
    return s


def build_benchmark_claim_decision_report(sealed: dict[str, Any]) -> dict[str, Any]:
    base = {k: v for k, v in sealed.items() if k != SEAL_HBC}
    d = sha256_hex_of_canonical_json(base)
    return {
        "report_kind": "v15_human_benchmark_claim_decision_report",
        "report_version": REPORT_VERSION_HUMAN_BENCHMARK_CLAIM,
        "milestone": MILESTONE_ID_V15_M11,
        "artifact_sha256": d,
        "seal_field": SEAL_HBC,
        "seal_value_matches_artifact": sealed.get(SEAL_HBC) == d,
        "primary_filename": FILENAME_HUMAN_BENCHMARK_CLAIM_DECISION,
    }


def emit_v15_human_benchmark_claim_decision(
    out_dir: Path, execution_path: Path, *, strict: bool = False
) -> tuple[dict[str, Any], dict[str, Any], Path, Path]:
    raw = json.loads(execution_path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ValueError("execution JSON must be a single object")
    _require_contract(raw, CONTRACT_ID_HUMAN_PANEL_EXECUTION, "execution")
    digest = str(raw.get(SEAL_HPE, ""))
    base = {k: v for k, v in raw.items() if k != SEAL_HPE}
    expected = sha256_hex_of_canonical_json(base)
    if digest and digest != expected:
        raise ValueError("execution seal does not match canonical JSON (rejecting tampered file)")
    if strict:
        validate_strict_execution_bindings(raw)
    body = build_human_benchmark_claim_decision_body(raw)
    if str(raw.get("profile")) != PROFILE_FIXTURE_CI:
        body = {
            **body,
            "claim_decision_id": f"v15_m11:claim:{sha256_hex_of_canonical_json(base)[:16]}",
        }
    sealed = seal_benchmark_claim_decision_body(body)
    rep = build_benchmark_claim_decision_report(sealed)
    out_dir.mkdir(parents=True, exist_ok=True)
    p1 = out_dir / FILENAME_HUMAN_BENCHMARK_CLAIM_DECISION
    p2 = out_dir / REPORT_FILENAME_HUMAN_BENCHMARK_CLAIM_DECISION
    p1.write_text(canonical_json_dumps(sealed), encoding="utf-8")
    p2.write_text(canonical_json_dumps(rep), encoding="utf-8")
    return sealed, rep, p1, p2
