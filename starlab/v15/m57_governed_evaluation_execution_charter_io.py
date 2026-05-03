"""V15-M57 — governed evaluation execution charter / dry-run gate IO."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Final, cast

from starlab.runs.json_util import canonical_json_dumps, sha256_hex_of_canonical_json
from starlab.v15.environment_lock_io import redact_paths_in_value
from starlab.v15.m31_candidate_checkpoint_evaluation_harness_gate_io import (
    emission_has_private_path_patterns,
)
from starlab.v15.m56a_latest_candidate_visual_watchability_confirmation_io import (
    validate_sha256 as validate_sha256_hex,
)
from starlab.v15.m57_governed_evaluation_execution_charter_models import (
    BLOCKED_CANDIDATE_IDENTITY,
    BLOCKED_CANDIDATE_POLICY_NOT_CONFIRMED,
    BLOCKED_CLAIM_FLAGS,
    BLOCKED_INVALID_M56_READOUT_CONTEXT,
    BLOCKED_INVALID_MATCH_PROOF,
    BLOCKED_INVALID_SEAL,
    BLOCKED_M52A_NOT_COMPLETED,
    BLOCKED_M52A_OP1_ANCHOR,
    BLOCKED_M57A_NOT_CANDIDATE_LIVE,
    BLOCKED_M57A_OP1_ANCHOR,
    BLOCKED_M57A_SCAFFOLD_ONLY,
    BLOCKED_MATCH_PROOF_ACTION_MISMATCH,
    BLOCKED_MATCH_PROOF_MAP_MISMATCH,
    BLOCKED_MISSING_M52A,
    BLOCKED_MISSING_M57A,
    BLOCKED_PRIVATE_BOUNDARY,
    BLOCKED_REPLAY_ANCHOR,
    BLOCKED_REPLAY_NOT_SAVED,
    CANONICAL_CANDIDATE_CHECKPOINT_SHA256,
    CANONICAL_M53_RUN_ARTIFACT_SHA256,
    CANONICAL_M54_PACKAGE_SHA256,
    CANONICAL_M57A_OP1_M52A_ADAPTER_SHA256,
    CANONICAL_M57A_OP1_REPLAY_SHA256,
    CANONICAL_M57A_OP1_WATCH_SESSION_SHA256,
    CHARTER_BLOCKED,
    CHARTER_READY,
    CHARTER_READY_WARNINGS,
    CHECKLIST_FILENAME,
    CLASSIFICATION_CANDIDATE_LIVE_WATCH_COMPLETED,
    CLASSIFICATION_SCAFFOLD_WATCH,
    CONTRACT_ID,
    CONTRACT_ID_M52A,
    CONTRACT_ID_M56,
    CONTRACT_ID_M57A,
    DEFAULT_CLAIM_FLAGS,
    DRY_RUN_BLOCKED,
    DRY_RUN_COMMAND_FILENAME,
    DRY_RUN_COMMAND_PLANNED,
    DRY_RUN_READY,
    EMITTER_MODULE,
    FILENAME_MAIN_JSON,
    GATE_ARTIFACT_DIGEST_FIELD,
    M52A_STATUS_COMPLETED,
    M56_DECISION_READY,
    M56_ROUTE_EXPECTED,
    M57_FORBIDDEN_TRUE_CLAIM_KEYS,
    MILESTONE,
    NON_CLAIMS,
    NOTICE_M56_READOUT_VERIFIED,
    POLICY_CANDIDATE_LIVE_ADAPTER,
    PROFILE_FIXTURE_CI,
    PROFILE_M57,
    PROFILE_OPERATOR_DECLARED,
    PROFILE_OPERATOR_PREFLIGHT,
    RECOMMENDED_NEXT_MILESTONE,
    RECOMMENDED_NEXT_TITLE,
    REPORT_CONTRACT_ID,
    REPORT_FILENAME,
    ROUTE_M58,
    ROUTE_STATUS_RECOMMENDED_NOT_EXECUTED,
    SCHEMA_VERSION,
    STRONGEST_ALLOWED,
    WARNING_M56_READOUT_ABSENT,
)

DIGEST_FIELD: Final[str] = GATE_ARTIFACT_DIGEST_FIELD
_HEX64: Final[re.Pattern[str]] = re.compile(r"^[0-9a-f]{64}$")


def seal_m57_body(body: dict[str, Any]) -> dict[str, Any]:
    wo = {k: v for k, v in body.items() if k != DIGEST_FIELD}
    digest = sha256_hex_of_canonical_json(wo)
    sealed = dict(wo)
    sealed[DIGEST_FIELD] = digest
    return sealed


def _parse_json_object(path: Path) -> dict[str, Any]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ValueError("JSON root must be an object")
    return raw


def _seal_ok(obj: dict[str, Any]) -> bool:
    seal_in = obj.get(DIGEST_FIELD)
    if seal_in is None or str(seal_in).strip() == "":
        return False
    wo = {k: v for k, v in obj.items() if k != DIGEST_FIELD}
    computed = sha256_hex_of_canonical_json(wo)
    return str(seal_in).strip().lower() == computed.lower()


def _claim_flags_illegal_true(obj: Any) -> bool:
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k == "claim_flags" and isinstance(v, dict):
                for ck, cv in v.items():
                    if ck in M57_FORBIDDEN_TRUE_CLAIM_KEYS and cv is True:
                        return True
            if _claim_flags_illegal_true(v):
                return True
    if isinstance(obj, list):
        return any(_claim_flags_illegal_true(x) for x in obj)
    return False


def _validate_m57a_watch_session(m57a: dict[str, Any]) -> list[str]:
    errs: list[str] = []
    if str(m57a.get("contract_id") or "") != CONTRACT_ID_M57A:
        errs.append(BLOCKED_INVALID_SEAL)
        return errs
    if not _seal_ok(m57a):
        errs.append(BLOCKED_INVALID_SEAL)
        return errs
    dig = str(m57a.get(DIGEST_FIELD) or "").strip().lower()
    if dig != CANONICAL_M57A_OP1_WATCH_SESSION_SHA256:
        errs.append(BLOCKED_M57A_OP1_ANCHOR)
    vc = m57a.get("visual_classification")
    if not isinstance(vc, dict):
        errs.append(BLOCKED_M57A_NOT_CANDIDATE_LIVE)
    else:
        cls = str(vc.get("classification") or "")
        if cls == CLASSIFICATION_SCAFFOLD_WATCH:
            errs.append(BLOCKED_M57A_SCAFFOLD_ONLY)
        elif cls != CLASSIFICATION_CANDIDATE_LIVE_WATCH_COMPLETED:
            errs.append(BLOCKED_M57A_NOT_CANDIDATE_LIVE)
        if vc.get("is_scaffold_policy") is True:
            errs.append(BLOCKED_M57A_SCAFFOLD_ONLY)
    cf = m57a.get("claim_flags")
    if not isinstance(cf, dict) or cf.get("candidate_policy_control_confirmed") is not True:
        errs.append(BLOCKED_CANDIDATE_POLICY_NOT_CONFIRMED)
    ws = m57a.get("watch_session")
    if not isinstance(ws, dict):
        errs.append(BLOCKED_M57A_NOT_CANDIDATE_LIVE)
    else:
        if str(ws.get("policy_source") or "") != POLICY_CANDIDATE_LIVE_ADAPTER:
            errs.append(BLOCKED_M57A_NOT_CANDIDATE_LIVE)
        if ws.get("live_sc2_invoked") is not True:
            errs.append(BLOCKED_M57A_NOT_CANDIDATE_LIVE)
        if ws.get("replay_saved") is not True:
            errs.append(BLOCKED_REPLAY_NOT_SAVED)
    ib = m57a.get("input_bindings")
    if isinstance(ib, dict):
        cand = str(ib.get("candidate_checkpoint_sha256") or "").strip().lower()
        if cand != CANONICAL_CANDIDATE_CHECKPOINT_SHA256:
            errs.append(BLOCKED_CANDIDATE_IDENTITY)
    else:
        errs.append(BLOCKED_CANDIDATE_IDENTITY)
    aref = m57a.get("artifact_references")
    if isinstance(aref, dict):
        rph = str(aref.get("replay_sha256") or "").strip().lower()
        if rph != CANONICAL_M57A_OP1_REPLAY_SHA256:
            errs.append(BLOCKED_REPLAY_ANCHOR)
    else:
        errs.append(BLOCKED_REPLAY_ANCHOR)
    if _claim_flags_illegal_true(m57a):
        errs.append(BLOCKED_CLAIM_FLAGS)
    return sorted(set(errs))


def _validate_m52a_adapter(m52a: dict[str, Any]) -> list[str]:
    errs: list[str] = []
    if str(m52a.get("contract_id") or "") != CONTRACT_ID_M52A:
        errs.append(BLOCKED_INVALID_SEAL)
        return errs
    if not _seal_ok(m52a):
        errs.append(BLOCKED_INVALID_SEAL)
        return errs
    dig = str(m52a.get(DIGEST_FIELD) or "").strip().lower()
    if dig != CANONICAL_M57A_OP1_M52A_ADAPTER_SHA256:
        errs.append(BLOCKED_M52A_OP1_ANCHOR)
    if str(m52a.get("adapter_status") or "") != M52A_STATUS_COMPLETED:
        errs.append(BLOCKED_M52A_NOT_COMPLETED)
    if m52a.get("live_sc2_executed") is not True:
        errs.append(BLOCKED_M52A_NOT_COMPLETED)
    wr = m52a.get("watchability_run")
    if not isinstance(wr, dict) or wr.get("replay_saved") is not True:
        errs.append(BLOCKED_REPLAY_NOT_SAVED)
    cid = m52a.get("candidate_identity")
    if isinstance(cid, dict):
        csha = str(cid.get("candidate_checkpoint_sha256") or "").strip().lower()
        if csha != CANONICAL_CANDIDATE_CHECKPOINT_SHA256:
            errs.append(BLOCKED_CANDIDATE_IDENTITY)
    else:
        errs.append(BLOCKED_CANDIDATE_IDENTITY)
    if _claim_flags_illegal_true(m52a):
        errs.append(BLOCKED_CLAIM_FLAGS)
    return sorted(set(errs))


def _validate_match_proof(
    proof: dict[str, Any] | None,
    *,
    expected_action_count: int,
) -> list[str]:
    if proof is None:
        return []
    errs: list[str] = []
    ah = str(proof.get("artifact_hash") or "").strip().lower()
    if not _HEX64.match(ah):
        errs.append(BLOCKED_INVALID_MATCH_PROOF)
    fs = str(proof.get("final_status") or "")
    if fs != "ok":
        errs.append(BLOCKED_INVALID_MATCH_PROOF)
    ac = proof.get("action_count")
    if ac is not None and int(ac) != int(expected_action_count):
        errs.append(BLOCKED_MATCH_PROOF_ACTION_MISMATCH)
    mk = str(proof.get("map_logical_key") or "")
    if "Waterfall" not in mk:
        errs.append(BLOCKED_MATCH_PROOF_MAP_MISMATCH)
    return sorted(set(errs))


def _validate_m56_readout(
    m56: dict[str, Any] | None,
    *,
    expected_candidate_sha: str,
) -> tuple[list[str], list[str]]:
    """Returns (blocked_reasons, notices)."""
    if m56 is None:
        return [], [WARNING_M56_READOUT_ABSENT]
    blocked: list[str] = []
    if str(m56.get("contract_id") or "") != CONTRACT_ID_M56:
        blocked.append(BLOCKED_INVALID_M56_READOUT_CONTEXT)
        return blocked, []
    if not _seal_ok(m56):
        blocked.append(BLOCKED_INVALID_M56_READOUT_CONTEXT)
        return blocked, []
    ro = m56.get("readout")
    if not isinstance(ro, dict):
        blocked.append(BLOCKED_INVALID_M56_READOUT_CONTEXT)
        return blocked, []
    if str(ro.get("decision_status") or "") != M56_DECISION_READY:
        blocked.append(BLOCKED_INVALID_M56_READOUT_CONTEXT)
        return blocked, []
    rr = m56.get("route_recommendation")
    if not isinstance(rr, dict):
        blocked.append(BLOCKED_INVALID_M56_READOUT_CONTEXT)
        return blocked, []
    if str(rr.get("route") or "").strip() != M56_ROUTE_EXPECTED:
        blocked.append(BLOCKED_INVALID_M56_READOUT_CONTEXT)
        return blocked, []
    if str(rr.get("route_status") or "").strip() != ROUTE_STATUS_RECOMMENDED_NOT_EXECUTED:
        blocked.append(BLOCKED_INVALID_M56_READOUT_CONTEXT)
        return blocked, []
    ib = m56.get("input_bindings")
    if isinstance(ib, dict):
        cand = str(ib.get("candidate_checkpoint_sha256") or "").strip().lower()
        if cand != expected_candidate_sha.strip().lower():
            blocked.append(BLOCKED_INVALID_M56_READOUT_CONTEXT)
            return blocked, []
    if _claim_flags_illegal_true(m56):
        blocked.append(BLOCKED_CLAIM_FLAGS)
        return blocked, []
    return [], [NOTICE_M56_READOUT_VERIFIED]


def _evaluation_charter_template(
    *,
    charter_status: str,
    execution_performed: bool,
) -> dict[str, Any]:
    return {
        "charter_status": charter_status,
        "execution_performed_in_m57": execution_performed,
        "candidate_policy_source": "m52a_candidate_live_adapter",
        "candidate_checkpoint_sha256": CANONICAL_CANDIDATE_CHECKPOINT_SHA256,
        "initial_evaluation_class": "bounded_candidate_adapter_evaluation_smoke",
        "initial_baseline_class": "passive_or_scripted_baseline",
        "initial_map_policy": {
            "map_pool_status": "single_map_initial",
            "map_logical_key": "Maps/Waterfall.SC2Map",
        },
        "horizon_policy": {
            "game_step": 8,
            "max_game_steps": 2048,
            "horizon_source": "m57a_op1_observed_default",
        },
        "replay_policy": {
            "save_replay_required": True,
            "replay_hash_required_if_available": True,
            "raw_replay_committed": False,
        },
        "metric_policy": {
            "allowed_metrics": [
                "live_sc2_executed",
                "replay_saved",
                "action_count",
                "game_steps_observed",
                "observation_count",
                "adapter_status",
                "sc2_result_metadata",
                "refusal_status",
            ],
            "forbidden_metrics_in_m57": [
                "benchmark_pass_fail",
                "strength_score",
                "promotion_decision",
                "human_panel_claim",
                "v2_authorization",
            ],
        },
    }


def _dry_run_gate_template(
    *,
    gate_status: str,
    command_emitted: bool,
) -> dict[str, Any]:
    return {
        "gate_status": gate_status,
        "dry_run_command_emitted": command_emitted,
        "dry_run_command_path": DRY_RUN_COMMAND_FILENAME,
        "dry_run_command_status": DRY_RUN_COMMAND_PLANNED,
        "m58_runner_exists_in_m57": False,
        "execution_authorized_in_m57": False,
        "m58_execution_recommended": gate_status == DRY_RUN_READY,
    }


def _upstream_readiness_ready() -> dict[str, Any]:
    return {
        "m56_route_status": ROUTE_STATUS_RECOMMENDED_NOT_EXECUTED,
        "m57a_visual_watch_status": CLASSIFICATION_CANDIDATE_LIVE_WATCH_COMPLETED,
        "candidate_policy_control_confirmed": True,
        "candidate_adapter_path_validated": True,
        "live_sc2_watchability_confirmed": True,
        "replay_capture_confirmed": True,
        "upstream_ready_for_charter": True,
    }


def _input_bindings_template(
    *,
    m56_sha: str | None,
    m57a_sha: str | None,
    m52a_sha: str | None,
    proof_sha: str | None,
) -> dict[str, Any]:
    return {
        "m56_readout_artifact_sha256": m56_sha,
        "m57a_watch_session_artifact_sha256": m57a_sha,
        "m52a_adapter_artifact_sha256": m52a_sha,
        "m57a_match_execution_proof_sha256": proof_sha,
        "m57a_replay_sha256": CANONICAL_M57A_OP1_REPLAY_SHA256,
        "m54_package_sha256": CANONICAL_M54_PACKAGE_SHA256,
        "m53_run_artifact_sha256": CANONICAL_M53_RUN_ARTIFACT_SHA256,
        "candidate_checkpoint_sha256": CANONICAL_CANDIDATE_CHECKPOINT_SHA256,
    }


def build_m58_dry_run_command_text() -> str:
    lines = [
        "# PLANNED_NOT_EXECUTED",
        "# V15-M58 runner is not implemented in V15-M57.",
        "# This is a frozen command template for the future V15-M58 milestone.",
        "# Do not execute as part of V15-M57.",
        "",
        (
            "python -m starlab.v15.run_v15_m58_bounded_candidate_adapter_evaluation_"
            "execution_attempt \\"
        ),
        "  --allow-operator-local-execution \\",
        "  --authorize-bounded-candidate-adapter-evaluation \\",
        "  --candidate-checkpoint <path-to-latest-candidate.pt> \\",
        f"  --expected-candidate-sha256 {CANONICAL_CANDIDATE_CHECKPOINT_SHA256} \\",
        '  --map-path "C:\\Program Files (x86)\\StarCraft II\\Maps\\Waterfall.SC2Map" \\',
        '  --sc2-root "C:\\Program Files (x86)\\StarCraft II" \\',
        "  --game-step 8 \\",
        "  --max-game-steps 2048 \\",
        "  --opponent-mode passive_or_scripted_baseline \\",
        "  --save-replay \\",
        "  --output-dir out/v15_m58/bounded_candidate_adapter_eval_001",
    ]
    return "\n".join(lines) + "\n"


def build_charter_checklist(
    body: dict[str, Any],
    *,
    blocked_reasons: list[str],
    notices: list[str],
) -> str:
    ec = body.get("evaluation_charter") or {}
    cs = str(ec.get("charter_status") or CHARTER_BLOCKED)
    dr = body.get("dry_run_gate") or {}
    gs = str(dr.get("gate_status") or DRY_RUN_BLOCKED)
    lines = [
        "# V15-M57 — Governed Evaluation Execution Charter / Dry-Run Gate Checklist",
        "",
        f"- **Charter status:** `{cs}`",
        f"- **Dry-run gate:** `{gs}`",
    ]
    if notices:
        lines.append("- **Notices:**")
        for n in notices:
            lines.append(f"  - `{n}`")
    if blocked_reasons:
        lines.append("- **Blocked reasons:**")
        for b in blocked_reasons:
            lines.append(f"  - `{b}`")
    checklist_gates = [
        ("C0", "M56 readout context present or explicitly absent with notice"),
        ("C1", "M57A watch session artifact present and sealed"),
        ("C2", "M57A classification is candidate_live_visual_watch_completed"),
        ("C3", "M57A candidate policy control confirmed"),
        ("C4", "M52A adapter artifact confirms model/checkpoint load and live SC2"),
        ("C5", "Latest candidate SHA matches expected V15-M53/V15-M54 candidate"),
        ("C6", "Replay saved and hash recorded where available"),
        ("C7", "Map / opponent / horizon policy frozen"),
        ("C8", "Allowed metrics and forbidden metrics frozen"),
        ("C9", "M58 dry-run command emitted but not executed"),
        ("C10", "Claim flags remain false for execution/pass/strength/promotion"),
        ("C11", "Public/private boundary preserved"),
    ]
    lines.append("")
    for cid, desc in checklist_gates:
        lines.append(f"- **{cid}** — {desc}")
    lines.append("")
    return "\n".join(lines)


def build_charter_report(
    body: dict[str, Any],
    *,
    blocked: list[str],
    notices: list[str],
) -> dict[str, Any]:
    ec = body.get("evaluation_charter") or {}
    dr = body.get("dry_run_gate") or {}
    cs = str(ec.get("charter_status") or CHARTER_BLOCKED)
    gs = str(dr.get("gate_status") or DRY_RUN_BLOCKED)
    ready = cs == CHARTER_READY and not blocked
    summary = (
        f"V15-M57 / {cs} / {gs}"
        if ready
        else f"V15-M57 blocked: {', '.join(blocked) if blocked else gs}"
    )
    return {
        "contract_id": REPORT_CONTRACT_ID,
        "milestone": MILESTONE,
        "charter_status": cs,
        "dry_run_gate_status": gs,
        "summary": summary,
        "strongest_allowed_claim": STRONGEST_ALLOWED,
        "warnings": list(notices),
        "blocked_reasons": list(blocked),
        "non_claims": list(NON_CLAIMS),
        "next_recommended_step": f"{RECOMMENDED_NEXT_MILESTONE} — {RECOMMENDED_NEXT_TITLE}",
    }


def build_fixture_charter() -> dict[str, Any]:
    return {
        "contract_id": CONTRACT_ID,
        "profile_id": PROFILE_M57,
        "milestone": MILESTONE,
        "emitter_module": EMITTER_MODULE,
        "schema_version": SCHEMA_VERSION,
        "profile": PROFILE_FIXTURE_CI,
        "input_bindings": _input_bindings_template(
            m56_sha=None,
            m57a_sha=CANONICAL_M57A_OP1_WATCH_SESSION_SHA256,
            m52a_sha=CANONICAL_M57A_OP1_M52A_ADAPTER_SHA256,
            proof_sha=None,
        ),
        "upstream_readiness": _upstream_readiness_ready(),
        "evaluation_charter": _evaluation_charter_template(
            charter_status=CHARTER_READY,
            execution_performed=False,
        ),
        "dry_run_gate": _dry_run_gate_template(
            gate_status=DRY_RUN_READY,
            command_emitted=True,
        ),
        "claim_flags": dict(DEFAULT_CLAIM_FLAGS),
        "non_claims": list(NON_CLAIMS),
        "route_recommendation": {
            "route": ROUTE_M58,
            "route_status": ROUTE_STATUS_RECOMMENDED_NOT_EXECUTED,
            "recommended_next_milestone": RECOMMENDED_NEXT_MILESTONE,
            "recommended_next_title": RECOMMENDED_NEXT_TITLE,
            "route_note": "M58 owns first bounded candidate adapter evaluation execution attempt.",
        },
    }


def _blocked_charter_body(blocked: list[str], notices: list[str]) -> dict[str, Any]:
    return {
        "contract_id": CONTRACT_ID,
        "profile_id": PROFILE_M57,
        "milestone": MILESTONE,
        "emitter_module": EMITTER_MODULE,
        "schema_version": SCHEMA_VERSION,
        "profile": PROFILE_OPERATOR_PREFLIGHT,
        "blocked_reasons": list(blocked),
        "input_bindings": _input_bindings_template(
            m56_sha=None,
            m57a_sha=None,
            m52a_sha=None,
            proof_sha=None,
        ),
        "upstream_readiness": {
            "m56_route_status": ROUTE_STATUS_RECOMMENDED_NOT_EXECUTED,
            "m57a_visual_watch_status": "",
            "candidate_policy_control_confirmed": False,
            "candidate_adapter_path_validated": False,
            "live_sc2_watchability_confirmed": False,
            "replay_capture_confirmed": False,
            "upstream_ready_for_charter": False,
        },
        "evaluation_charter": _evaluation_charter_template(
            charter_status=CHARTER_BLOCKED,
            execution_performed=False,
        ),
        "dry_run_gate": _dry_run_gate_template(
            gate_status=DRY_RUN_BLOCKED,
            command_emitted=False,
        ),
        "claim_flags": dict(DEFAULT_CLAIM_FLAGS),
        "non_claims": list(NON_CLAIMS),
        "route_recommendation": {
            "route": ROUTE_M58,
            "route_status": ROUTE_STATUS_RECOMMENDED_NOT_EXECUTED,
            "recommended_next_milestone": RECOMMENDED_NEXT_MILESTONE,
            "recommended_next_title": RECOMMENDED_NEXT_TITLE,
            "route_note": "Charter blocked; M58 not recommended until remediation.",
        },
        "_notices": list(notices),
    }


@dataclass(frozen=True)
class OperatorPreflightCharterInputs:
    m57a_watch_session_json: Path
    m52a_adapter_json: Path
    expected_candidate_sha256: str
    m56_readout_json: Path | None = None
    match_execution_proof_json: Path | None = None


def build_operator_preflight_charter(
    inputs: OperatorPreflightCharterInputs,
) -> dict[str, Any]:
    notices: list[str] = []
    blocked: list[str] = []
    exp_c = validate_sha256_hex(str(inputs.expected_candidate_sha256))
    if exp_c is None or exp_c.lower() != CANONICAL_CANDIDATE_CHECKPOINT_SHA256:
        blocked.append(BLOCKED_CANDIDATE_IDENTITY)
        return _blocked_charter_body(blocked, notices)

    m56_obj: dict[str, Any] | None = None
    if inputs.m56_readout_json is not None:
        if not inputs.m56_readout_json.is_file():
            blocked.append(BLOCKED_INVALID_M56_READOUT_CONTEXT)
            return _blocked_charter_body(blocked, notices)
        try:
            m56_obj = _parse_json_object(inputs.m56_readout_json.resolve())
        except (OSError, json.JSONDecodeError, ValueError):
            blocked.append(BLOCKED_INVALID_M56_READOUT_CONTEXT)
            return _blocked_charter_body(blocked, notices)

    b56, n56 = _validate_m56_readout(m56_obj, expected_candidate_sha=exp_c)
    notices.extend(n56)
    blocked.extend(b56)
    if blocked:
        return _blocked_charter_body(blocked, notices)

    if not inputs.m57a_watch_session_json.is_file():
        blocked.append(BLOCKED_MISSING_M57A)
        return _blocked_charter_body(blocked, notices)
    if not inputs.m52a_adapter_json.is_file():
        blocked.append(BLOCKED_MISSING_M52A)
        return _blocked_charter_body(blocked, notices)

    try:
        m57a = _parse_json_object(inputs.m57a_watch_session_json.resolve())
        m52a = _parse_json_object(inputs.m52a_adapter_json.resolve())
    except (OSError, json.JSONDecodeError, ValueError):
        blocked.append(BLOCKED_INVALID_SEAL)
        return _blocked_charter_body(blocked, notices)

    blocked.extend(_validate_m57a_watch_session(m57a))
    if blocked:
        return _blocked_charter_body(blocked, notices)
    blocked.extend(_validate_m52a_adapter(m52a))
    if blocked:
        return _blocked_charter_body(blocked, notices)

    proof_obj: dict[str, Any] | None = None
    proof_sha: str | None = None
    if inputs.match_execution_proof_json is not None:
        if inputs.match_execution_proof_json.is_file():
            try:
                raw_p = json.loads(
                    inputs.match_execution_proof_json.read_text(encoding="utf-8"),
                )
                proof_obj = raw_p if isinstance(raw_p, dict) else None
            except (OSError, json.JSONDecodeError):
                blocked.append(BLOCKED_INVALID_MATCH_PROOF)
                return _blocked_charter_body(blocked, notices)
        if proof_obj is not None:
            ws = m57a.get("watch_session")
            ac = int(ws.get("action_count") or 0) if isinstance(ws, dict) else 0
            blocked.extend(_validate_match_proof(proof_obj, expected_action_count=ac))
            if blocked:
                return _blocked_charter_body(blocked, notices)
            proof_sha = sha256_hex_of_canonical_json(
                cast(dict[str, Any], redact_paths_in_value(proof_obj)),
            )

    m56_digest = str(m56_obj.get(DIGEST_FIELD) or "").strip().lower() if m56_obj else None
    m57a_d = str(m57a.get(DIGEST_FIELD) or "").strip().lower()
    m52a_d = str(m52a.get(DIGEST_FIELD) or "").strip().lower()

    charter_status = CHARTER_READY_WARNINGS if notices else CHARTER_READY
    body: dict[str, Any] = {
        "contract_id": CONTRACT_ID,
        "profile_id": PROFILE_M57,
        "milestone": MILESTONE,
        "emitter_module": EMITTER_MODULE,
        "schema_version": SCHEMA_VERSION,
        "profile": PROFILE_OPERATOR_PREFLIGHT,
        "input_bindings": _input_bindings_template(
            m56_sha=m56_digest,
            m57a_sha=m57a_d,
            m52a_sha=m52a_d,
            proof_sha=proof_sha,
        ),
        "upstream_readiness": _upstream_readiness_ready(),
        "evaluation_charter": _evaluation_charter_template(
            charter_status=charter_status,
            execution_performed=False,
        ),
        "dry_run_gate": _dry_run_gate_template(
            gate_status=DRY_RUN_READY,
            command_emitted=True,
        ),
        "claim_flags": dict(DEFAULT_CLAIM_FLAGS),
        "non_claims": list(NON_CLAIMS),
        "route_recommendation": {
            "route": ROUTE_M58,
            "route_status": ROUTE_STATUS_RECOMMENDED_NOT_EXECUTED,
            "recommended_next_milestone": RECOMMENDED_NEXT_MILESTONE,
            "recommended_next_title": RECOMMENDED_NEXT_TITLE,
            "route_note": "M58 owns first bounded candidate adapter evaluation execution attempt.",
        },
        "_notices": list(notices),
    }
    return body


@dataclass(frozen=True)
class OperatorDeclaredCharterInputs:
    declared_charter_json: Path
    m57a_watch_session_json: Path
    expected_candidate_sha256: str


def build_operator_declared_charter(
    inputs: OperatorDeclaredCharterInputs,
) -> dict[str, Any]:
    notices: list[str] = []
    exp_c = validate_sha256_hex(str(inputs.expected_candidate_sha256))
    if exp_c is None or exp_c != CANONICAL_CANDIDATE_CHECKPOINT_SHA256:
        return _blocked_charter_body([BLOCKED_CANDIDATE_IDENTITY], notices)

    if not inputs.declared_charter_json.is_file():
        return _blocked_charter_body([BLOCKED_INVALID_SEAL], notices)
    if not inputs.m57a_watch_session_json.is_file():
        return _blocked_charter_body([BLOCKED_MISSING_M57A], notices)

    try:
        declared = _parse_json_object(inputs.declared_charter_json.resolve())
        m57a = _parse_json_object(inputs.m57a_watch_session_json.resolve())
    except (OSError, json.JSONDecodeError, ValueError):
        return _blocked_charter_body([BLOCKED_INVALID_SEAL], notices)

    if emission_has_private_path_patterns(canonical_json_dumps(declared)):
        return _blocked_charter_body([BLOCKED_PRIVATE_BOUNDARY], notices)
    if _claim_flags_illegal_true(declared):
        return _blocked_charter_body([BLOCKED_CLAIM_FLAGS], notices)
    ec = declared.get("evaluation_charter")
    if isinstance(ec, dict) and ec.get("execution_performed_in_m57") is True:
        return _blocked_charter_body([BLOCKED_CLAIM_FLAGS], notices)
    dr = declared.get("dry_run_gate")
    if isinstance(dr, dict) and dr.get("execution_authorized_in_m57") is True:
        return _blocked_charter_body([BLOCKED_CLAIM_FLAGS], notices)

    blocked = list({*_validate_m57a_watch_session(m57a)})
    if blocked:
        return _blocked_charter_body(blocked, notices)

    ib = declared.get("input_bindings")
    if not isinstance(ib, dict):
        return _blocked_charter_body([BLOCKED_M52A_OP1_ANCHOR], notices)
    m52a_bind = str(ib.get("m52a_adapter_artifact_sha256") or "").strip().lower()
    if m52a_bind != CANONICAL_M57A_OP1_M52A_ADAPTER_SHA256:
        return _blocked_charter_body([BLOCKED_M52A_OP1_ANCHOR], notices)
    m57a_bind = str(ib.get("m57a_watch_session_artifact_sha256") or "").strip().lower()
    if m57a_bind != CANONICAL_M57A_OP1_WATCH_SESSION_SHA256:
        return _blocked_charter_body([BLOCKED_M57A_OP1_ANCHOR], notices)

    merged = build_fixture_charter()
    merged["profile"] = PROFILE_OPERATOR_DECLARED
    merged["input_bindings"] = cast(dict[str, Any], redact_paths_in_value(ib))
    merged["_notices"] = notices
    return merged


def write_charter_artifacts(
    output_dir: Path,
    *,
    body_unsealed: dict[str, Any],
) -> tuple[dict[str, Any], tuple[Path, ...]]:
    out = output_dir.resolve()
    out.mkdir(parents=True, exist_ok=True)
    working = dict(body_unsealed)
    notices = list(working.pop("_notices", []) or [])
    blocked = list(working.pop("blocked_reasons", []) or [])
    ec = working.get("evaluation_charter")
    charter_blocked = (
        isinstance(ec, dict) and str(ec.get("charter_status") or "") == CHARTER_BLOCKED
    )
    to_seal = cast(dict[str, Any], redact_paths_in_value(working))
    sealed = seal_m57_body(to_seal)

    report = build_charter_report(sealed, blocked=blocked, notices=notices)
    checklist = build_charter_checklist(
        sealed,
        blocked_reasons=blocked,
        notices=notices,
    )
    cmd_text = build_m58_dry_run_command_text()
    if not charter_blocked:
        cmd_path = out / DRY_RUN_COMMAND_FILENAME
        cmd_path.write_text(cmd_text, encoding="utf-8")
    else:
        cmd_path = None

    main_p = out / FILENAME_MAIN_JSON
    main_p.write_text(
        canonical_json_dumps(sealed) + "\n",
        encoding="utf-8",
    )
    report_p = out / REPORT_FILENAME
    report_p.write_text(
        canonical_json_dumps(report) + "\n",
        encoding="utf-8",
    )
    chk_p = out / CHECKLIST_FILENAME
    chk_p.write_text(checklist, encoding="utf-8")
    paths: list[Path] = [main_p, report_p, chk_p]
    if cmd_path is not None:
        paths.append(cmd_path)
    return sealed, tuple(paths)


def emit_forbidden_refusal(output_dir: Path, *, flags: list[str]) -> None:
    blocked = [f"forbidden_cli_flag:{','.join(sorted(flags))}"]
    body = _blocked_charter_body(blocked, [])
    write_charter_artifacts(output_dir, body_unsealed=body)


def charter_is_blocked(body: dict[str, Any]) -> bool:
    ec = body.get("evaluation_charter")
    if isinstance(ec, dict) and str(ec.get("charter_status") or "") == CHARTER_BLOCKED:
        return True
    br = body.get("blocked_reasons")
    return isinstance(br, list) and len(br) > 0
