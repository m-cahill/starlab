"""V15-M58 — bounded candidate adapter evaluation execution attempt IO."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Final, cast

from starlab.runs.json_util import canonical_json_dumps, sha256_hex_of_canonical_json
from starlab.v15.environment_lock_io import redact_paths_in_value
from starlab.v15.m31_candidate_checkpoint_evaluation_harness_gate_io import (
    emission_has_private_path_patterns,
)
from starlab.v15.m51_live_candidate_watchability_harness_io import sha256_hex_file_optional
from starlab.v15.m52_candidate_live_adapter_spike_models import (
    CONTRACT_ID_M52A as M52A_CONTRACT_ID,
)
from starlab.v15.m52_candidate_live_adapter_spike_models import (
    FILENAME_MAIN_JSON as M52A_MAIN_JSON,
)
from starlab.v15.m52_candidate_live_adapter_spike_models import (
    GUARD_ALLOW_OPERATOR_LOCAL,
    GUARD_AUTHORIZE_ADAPTER_SPIKE,
)
from starlab.v15.m52_candidate_live_adapter_spike_models import (
    STATUS_SPIKE_COMPLETED as M52A_STATUS_COMPLETED,
)
from starlab.v15.m57_governed_evaluation_execution_charter_models import (
    CHARTER_BLOCKED,
    CHARTER_READY_WARNINGS,
)
from starlab.v15.m58_bounded_candidate_adapter_evaluation_execution_models import (
    BLOCKED_CANDIDATE_CHECKPOINT_MISSING,
    BLOCKED_CANDIDATE_CHECKPOINT_SHA_MISMATCH,
    BLOCKED_CANDIDATE_IDENTITY_MISMATCH,
    BLOCKED_CLAIM_FLAGS_VIOLATION,
    BLOCKED_DISALLOWED_BASELINE,
    BLOCKED_DISALLOWED_HORIZON,
    BLOCKED_DISALLOWED_MAP,
    BLOCKED_INVALID_M57_ARTIFACT_SEAL,
    BLOCKED_INVALID_M57_CHARTER,
    BLOCKED_M52A_DELEGATE_FAILED,
    BLOCKED_M57_ROUTE_NOT_TO_M58,
    BLOCKED_M57_ROUTE_STATUS_NOT_RECOMMENDED,
    BLOCKED_MISSING_M57_CHARTER,
    BLOCKED_MISSING_MAP_PATH,
    BLOCKED_MISSING_SC2_ROOT,
    BLOCKED_PRIVATE_BOUNDARY_VIOLATION,
    BLOCKED_REPLAY_NOT_SAVED,
    CANONICAL_CANDIDATE_CHECKPOINT_SHA256,
    CANONICAL_M53_RUN_ARTIFACT_SHA256,
    CANONICAL_M54_PACKAGE_SHA256,
    CANONICAL_M57A_OP1_M52A_ADAPTER_SHA256,
    CANONICAL_M57A_OP1_REPLAY_SHA256,
    CANONICAL_M57A_OP1_WATCH_SESSION_SHA256,
    CHARTER_BASELINE_CLASS,
    CHARTER_GAME_STEP,
    CHARTER_MAP_LOGICAL_KEY,
    CHARTER_MAX_GAME_STEPS,
    CHECKLIST_FILENAME,
    CONTRACT_ID,
    CONTRACT_ID_M57_CHARTER,
    DEFAULT_CLAIM_FLAGS,
    EMITTER_MODULE,
    FILENAME_MAIN_JSON,
    GATE_ARTIFACT_DIGEST_FIELD,
    M52A_DELEGATE_SUBDIR,
    M58_FORBIDDEN_TRUE_CLAIM_KEYS,
    MAX_ATTEMPT_COUNT,
    MILESTONE,
    MIN_ATTEMPT_COUNT,
    NON_CLAIMS,
    NORMALIZED_OPPONENT_MODE,
    OPPONENT_MODE_BURNY_PASSIVE,
    OPPONENT_MODE_PASSIVE_OR_SCRIPTED,
    PROFILE_FIXTURE_CI,
    PROFILE_M58,
    PROFILE_OPERATOR_DECLARED,
    PROFILE_OPERATOR_LOCAL_EXECUTION,
    PROFILE_OPERATOR_PREFLIGHT,
    RECOMMENDED_NEXT_MILESTONE,
    RECOMMENDED_NEXT_TITLE,
    REPORT_CONTRACT_ID,
    REPORT_FILENAME,
    ROUTE_EXPECTED_FROM_M57,
    ROUTE_M59,
    ROUTE_STATUS_RECOMMENDED_NOT_EXECUTED,
    ROUTE_STATUS_TO_M59,
    SCHEMA_VERSION,
    STATUS_EXECUTION_BLOCKED,
    STATUS_EXECUTION_COMPLETED,
    STATUS_EXECUTION_COMPLETED_WARNINGS,
    STATUS_FIXTURE_SCHEMA_ONLY,
    STATUS_PREFLIGHT_BLOCKED,
    STATUS_PREFLIGHT_READY,
    STRONGEST_ALLOWED,
)

DIGEST_FIELD: Final[str] = GATE_ARTIFACT_DIGEST_FIELD


def seal_m58_body(body: dict[str, Any]) -> dict[str, Any]:
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


def normalize_opponent_mode(raw: str | None) -> str | None:
    if raw is None:
        return NORMALIZED_OPPONENT_MODE
    s = str(raw).strip()
    if s in (OPPONENT_MODE_PASSIVE_OR_SCRIPTED, OPPONENT_MODE_BURNY_PASSIVE):
        return NORMALIZED_OPPONENT_MODE
    return None


def _m57_horizon_int_leaf(v: Any) -> int | None:
    """Coerce horizon JSON ints; reject booleans and non-numeric strings."""
    if isinstance(v, bool):
        return None
    if isinstance(v, int):
        return v
    if isinstance(v, str):
        try:
            return int(v.strip(), 10)
        except ValueError:
            return None
    return None


def load_m57_charter(path: Path) -> tuple[dict[str, Any] | None, list[str]]:
    errs: list[str] = []
    if not path.is_file():
        return None, [BLOCKED_MISSING_M57_CHARTER]
    try:
        ch = _parse_json_object(path.resolve())
    except (OSError, json.JSONDecodeError, ValueError, UnicodeError):
        return None, [BLOCKED_INVALID_M57_CHARTER]

    if str(ch.get("contract_id") or "") != CONTRACT_ID_M57_CHARTER:
        errs.append(BLOCKED_INVALID_M57_CHARTER)

    if not _seal_ok(ch):
        errs.append(BLOCKED_INVALID_M57_ARTIFACT_SEAL)

    rr = ch.get("route_recommendation")
    if isinstance(rr, dict):
        r = str(rr.get("route") or "").strip()
        rs = str(rr.get("route_status") or "").strip()
        if r != ROUTE_EXPECTED_FROM_M57:
            errs.append(BLOCKED_M57_ROUTE_NOT_TO_M58)
        if rs != ROUTE_STATUS_RECOMMENDED_NOT_EXECUTED:
            errs.append(BLOCKED_M57_ROUTE_STATUS_NOT_RECOMMENDED)
    else:
        errs.extend([BLOCKED_M57_ROUTE_NOT_TO_M58, BLOCKED_M57_ROUTE_STATUS_NOT_RECOMMENDED])

    ec = ch.get("evaluation_charter")
    if isinstance(ec, dict):
        cs = str(ec.get("charter_status") or "")
        if cs == CHARTER_BLOCKED:
            errs.append(BLOCKED_INVALID_M57_CHARTER)
        mp = ec.get("initial_map_policy")
        hp = ec.get("horizon_policy")
        if isinstance(mp, dict):
            if str(mp.get("map_logical_key") or "") != CHARTER_MAP_LOGICAL_KEY:
                errs.append(BLOCKED_INVALID_M57_CHARTER)
        else:
            errs.append(BLOCKED_INVALID_M57_CHARTER)
        if isinstance(hp, dict):
            gi = _m57_horizon_int_leaf(hp.get("game_step"))
            gm = _m57_horizon_int_leaf(hp.get("max_game_steps"))
            if gi is None or gm is None:
                errs.append(BLOCKED_INVALID_M57_CHARTER)
            elif gi != CHARTER_GAME_STEP or gm != CHARTER_MAX_GAME_STEPS:
                errs.append(BLOCKED_INVALID_M57_CHARTER)
        else:
            errs.append(BLOCKED_INVALID_M57_CHARTER)
        if str(ec.get("initial_baseline_class") or "") != CHARTER_BASELINE_CLASS:
            errs.append(BLOCKED_INVALID_M57_CHARTER)
    elif ec is None:
        errs.append(BLOCKED_INVALID_M57_CHARTER)

    return ch, sorted(set(errs))


def m57_charter_digest(ch: dict[str, Any]) -> str:
    return str(ch.get(DIGEST_FIELD) or "").strip().lower()


def validate_candidate_checkpoint_sha(ck_path: Path, *, expected_lower: str) -> list[str]:
    exp = expected_lower.strip().lower()
    if len(exp) != 64:
        return [BLOCKED_CANDIDATE_IDENTITY_MISMATCH]
    if not ck_path.is_file():
        return [BLOCKED_CANDIDATE_CHECKPOINT_MISSING]
    dig = sha256_hex_file_optional(ck_path.resolve())
    if not dig:
        return [BLOCKED_CANDIDATE_CHECKPOINT_MISSING]
    if dig.lower() != exp:
        return [BLOCKED_CANDIDATE_CHECKPOINT_SHA_MISMATCH]
    return []


def validate_execution_claim_flags(obj: dict[str, Any]) -> bool:
    def _deep(o: Any) -> bool:
        if isinstance(o, dict):
            for k, v in o.items():
                if k == "claim_flags" and isinstance(v, dict):
                    for ck, cv in v.items():
                        if ck in M58_FORBIDDEN_TRUE_CLAIM_KEYS and cv is True:
                            return True
                if _deep(v):
                    return True
            return False
        if isinstance(o, list):
            return any(_deep(x) for x in o)
        return False

    return _deep(obj)


def parse_m52a_delegate_receipts(
    m52_output_dir: Path,
    *,
    require_replay: bool,
) -> dict[str, Any]:
    main_p = Path(m52_output_dir).resolve() / M52A_MAIN_JSON
    out: dict[str, Any] = {
        "ok": False,
        "blocked_reasons": [],
        "adapter_status": None,
        "live_sc2_executed": False,
        "replay_saved": False,
        "replay_sha256": None,
        "action_count": None,
        "observation_count": None,
        "game_steps_observed": None,
        "sc2_result_metadata": None,
    }
    if not main_p.is_file():
        out["blocked_reasons"] = [BLOCKED_M52A_DELEGATE_FAILED]
        return out
    try:
        blob = _parse_json_object(main_p)
    except (ValueError, OSError, UnicodeError, json.JSONDecodeError):
        out["blocked_reasons"] = [BLOCKED_M52A_DELEGATE_FAILED]
        return out
    if str(blob.get("contract_id") or "") != M52A_CONTRACT_ID:
        out["blocked_reasons"] = [BLOCKED_M52A_DELEGATE_FAILED]
        return out

    adapter_status = str(blob.get("adapter_status") or "")
    out["adapter_status"] = adapter_status
    wr = blob.get("watchability_run")
    if isinstance(wr, dict):
        out["live_sc2_executed"] = bool(wr.get("live_sc2_executed"))
        out["replay_saved"] = bool(wr.get("replay_saved"))
        ac = wr.get("action_count")
        oc = wr.get("observation_count")
        try:
            out["action_count"] = int(ac) if ac is not None else None
        except (TypeError, ValueError):
            out["action_count"] = None
        try:
            out["observation_count"] = int(oc) if oc is not None else None
        except (TypeError, ValueError):
            out["observation_count"] = None
        out["game_steps_observed"] = (
            wr.get("max_game_steps_observed")
            or wr.get("game_steps_observed")
            or out["observation_count"]
        )
        try:
            gso = out["game_steps_observed"]
            out["game_steps_observed"] = int(gso) if gso is not None else None
        except (TypeError, ValueError):
            out["game_steps_observed"] = None
        out["sc2_result_metadata"] = str(wr.get("final_status") or "") or None

    replay_path = (
        Path(m52_output_dir).resolve() / M52A_DELEGATE_SUBDIR / "replay" / "validation.SC2Replay"
    )
    if replay_path.is_file():
        rp_hash = sha256_hex_file_optional(replay_path)
        if out["replay_saved"] and rp_hash:
            out["replay_sha256"] = rp_hash
    blocked: list[str] = []
    if adapter_status != M52A_STATUS_COMPLETED:
        blocked.append(BLOCKED_M52A_DELEGATE_FAILED)
    if require_replay:
        if not out["replay_saved"] or out["replay_sha256"] is None:
            blocked.append(BLOCKED_REPLAY_NOT_SAVED)
    if blocked:
        out["blocked_reasons"] = sorted(set(blocked))
        out["ok"] = False
        return out
    out["ok"] = True
    out["blocked_reasons"] = []
    return out


def _route_m59_block() -> dict[str, Any]:
    return {
        "route": ROUTE_M59,
        "route_status": ROUTE_STATUS_TO_M59,
        "recommended_next_milestone": RECOMMENDED_NEXT_MILESTONE,
        "recommended_next_title": RECOMMENDED_NEXT_TITLE,
        "route_note": (
            "M59 owns readout/refusal/threshold interpretation over bounded M58 evidence."
        ),
    }


def _execution_plan_template(
    *,
    execution_performed: bool,
    attempt_requested: int,
    attempt_completed: int,
    opponent_normalized: str,
) -> dict[str, Any]:
    return {
        "execution_class": "bounded_candidate_adapter_evaluation_smoke",
        "execution_performed": execution_performed,
        "candidate_policy_source": "m52a_candidate_live_adapter",
        "baseline_class": CHARTER_BASELINE_CLASS,
        "opponent_mode_normalized": opponent_normalized,
        "map_policy": {
            "map_logical_key": CHARTER_MAP_LOGICAL_KEY,
            "map_pool_status": "single_map_initial",
        },
        "horizon_policy": {
            "game_step": CHARTER_GAME_STEP,
            "max_game_steps": CHARTER_MAX_GAME_STEPS,
        },
        "replay_policy": {"save_replay_required": True, "raw_replay_committed": False},
        "attempt_count_requested": attempt_requested,
        "attempt_count_completed": attempt_completed,
    }


def build_fixture_execution() -> dict[str, Any]:
    ib = {
        "m57_charter_artifact_sha256": None,
        "m57a_op1_watch_session_sha256": CANONICAL_M57A_OP1_WATCH_SESSION_SHA256,
        "m57a_op1_m52a_adapter_sha256": CANONICAL_M57A_OP1_M52A_ADAPTER_SHA256,
        "m57a_op1_replay_sha256": CANONICAL_M57A_OP1_REPLAY_SHA256,
        "m54_package_sha256": CANONICAL_M54_PACKAGE_SHA256,
        "m53_run_artifact_sha256": CANONICAL_M53_RUN_ARTIFACT_SHA256,
        "candidate_checkpoint_sha256": CANONICAL_CANDIDATE_CHECKPOINT_SHA256,
    }
    forbidden = {
        "benchmark_pass_fail": "not_computed",
        "strength_score": "not_computed",
        "promotion_decision": "not_made",
        "human_panel_claim": "not_made",
        "v2_authorization": "not_made",
    }
    exec_result = {
        "execution_status": STATUS_FIXTURE_SCHEMA_ONLY,
        "blocked_reasons": [],
        "warnings": [],
        "live_sc2_executed": False,
        "candidate_adapter_loaded": False,
        "candidate_policy_control_confirmed": False,
        "replay_saved": False,
        "replay_sha256": None,
        "game_steps_observed": None,
        "observation_count": None,
        "action_count": None,
        "sc2_result_metadata": None,
        "duration_seconds": None,
    }
    claims = dict(DEFAULT_CLAIM_FLAGS)
    return {
        "contract_id": CONTRACT_ID,
        "profile_id": PROFILE_M58,
        "emitter_module": EMITTER_MODULE,
        "milestone": MILESTONE,
        "schema_version": SCHEMA_VERSION,
        "artifact_sha256": None,
        "profile": PROFILE_FIXTURE_CI,
        "input_bindings": ib,
        "execution_plan": _execution_plan_template(
            execution_performed=False,
            attempt_requested=1,
            attempt_completed=0,
            opponent_normalized=NORMALIZED_OPPONENT_MODE,
        ),
        "attempts": [],
        "aggregation": {
            "attempt_count_requested": 1,
            "attempt_count_completed": 0,
            "total_action_count": None,
            "all_replays_saved": False,
        },
        "execution_result": exec_result,
        "allowed_metrics": {
            "live_sc2_executed": False,
            "replay_saved": False,
            "action_count": None,
            "game_steps_observed": None,
            "observation_count": None,
            "adapter_status": None,
            "sc2_result_metadata": None,
            "refusal_status": None,
        },
        "forbidden_interpretations": forbidden,
        "claim_flags": claims,
        "non_claims": list(NON_CLAIMS),
        "route_recommendation": _route_m59_block(),
    }


def build_m52a_delegate_argv(
    *,
    python_executable: str,
    m51_json: Path,
    delegate_output_dir: Path,
    ck_path: Path,
    expected_ck_sha: str,
    sc2_root: Path,
    map_path: Path,
    device: str,
    game_step: int,
    max_game_steps: int,
    save_replay: bool,
    seed: int,
    expected_m51_sha256: str | None,
) -> list[str]:
    cmd: list[str] = [
        python_executable,
        "-m",
        "starlab.v15.run_v15_m52_candidate_live_adapter_spike",
        GUARD_ALLOW_OPERATOR_LOCAL,
        GUARD_AUTHORIZE_ADAPTER_SPIKE,
        "--m51-watchability-json",
        str(Path(m51_json).resolve()),
        "--output-dir",
        str(Path(delegate_output_dir).resolve()),
        "--candidate-checkpoint-path",
        str(Path(ck_path).resolve()),
        "--expected-candidate-checkpoint-sha256",
        expected_ck_sha.strip().lower(),
        "--sc2-root",
        str(Path(sc2_root).resolve()),
        "--map-path",
        str(Path(map_path).resolve()),
        "--device",
        str(device),
        "--game-step",
        str(int(game_step)),
        "--max-game-steps",
        str(int(max_game_steps)),
        "--seed",
        str(int(seed)),
    ]
    if save_replay:
        cmd.append("--save-replay")
    if expected_m51_sha256:
        cmd.extend(["--expected-m51-watchability-sha256", expected_m51_sha256.strip().lower()])
    return cmd


def _preflight_blocked_body(
    blocked: list[str],
    *,
    charter: dict[str, Any] | None,
) -> dict[str, Any]:
    digest = m57_charter_digest(charter) if charter else ""
    body = build_fixture_execution()
    body["profile"] = PROFILE_OPERATOR_PREFLIGHT
    ib = dict(cast(dict[str, Any], body["input_bindings"]))
    ib["m57_charter_artifact_sha256"] = digest if digest else None
    body["input_bindings"] = ib
    body["_blocked_reasons_top"] = sorted(set(blocked))
    body["execution_result"] = dict(body["execution_result"])
    cast(dict[str, Any], body["execution_result"])["execution_status"] = STATUS_PREFLIGHT_BLOCKED
    cast(dict[str, Any], body["execution_result"])["blocked_reasons"] = sorted(set(blocked))
    body["execution_plan"] = _execution_plan_template(
        execution_performed=False,
        attempt_requested=1,
        attempt_completed=0,
        opponent_normalized=NORMALIZED_OPPONENT_MODE,
    )
    return body


@dataclass(frozen=True)
class OperatorPreflightExecutionInputs:
    m57_charter_json: Path
    expected_candidate_sha256: str
    candidate_checkpoint: Path | None
    sc2_root: Path | None
    map_path: Path | None
    opponent_mode: str | None
    game_step: int | None
    max_game_steps: int | None


def build_operator_preflight_execution(
    inputs: OperatorPreflightExecutionInputs,
) -> dict[str, Any]:
    notices: list[str] = []
    ch, errs = load_m57_charter(inputs.m57_charter_json.resolve())
    cand_exp = str(inputs.expected_candidate_sha256).strip().lower()
    if len(cand_exp) != 64 or any(c not in "0123456789abcdef" for c in cand_exp):
        if ch:
            body = _preflight_blocked_body(
                errs + [BLOCKED_CANDIDATE_IDENTITY_MISMATCH],
                charter=ch,
            )
            body["_notices"] = notices
            return body
        return _preflight_blocked_body(
            errs + [BLOCKED_CANDIDATE_IDENTITY_MISMATCH],
            charter=None,
        )

    if ch is None:
        merged = errs
        body = _preflight_blocked_body(merged, charter=None)
        body["_notices"] = notices
        return body

    if errs:
        body = _preflight_blocked_body(errs, charter=ch)
        body["_notices"] = notices
        return body

    if inputs.candidate_checkpoint is not None:
        c_err = validate_candidate_checkpoint_sha(
            inputs.candidate_checkpoint.resolve(),
            expected_lower=cand_exp,
        )
        if c_err:
            body = _preflight_blocked_body(sorted(set(list(errs) + c_err)), charter=ch)
            body["_notices"] = notices
            return body

    opponent = normalize_opponent_mode(inputs.opponent_mode)
    if opponent is None:
        body = _preflight_blocked_body([BLOCKED_DISALLOWED_BASELINE], charter=ch)
        body["_notices"] = notices
        return body

    if inputs.sc2_root is None or not inputs.sc2_root.is_dir():
        body = _preflight_blocked_body([BLOCKED_MISSING_SC2_ROOT], charter=ch)
        body["_notices"] = notices
        return body
    if inputs.map_path is None or not inputs.map_path.is_file():
        body = _preflight_blocked_body([BLOCKED_MISSING_MAP_PATH], charter=ch)
        body["_notices"] = notices
        return body
    mp_sp = str(inputs.map_path.resolve())
    if "waterfall" not in mp_sp.lower():
        body = _preflight_blocked_body([BLOCKED_DISALLOWED_MAP], charter=ch)
        body["_notices"] = notices
        return body

    if inputs.game_step is not None and int(inputs.game_step) != CHARTER_GAME_STEP:
        body = _preflight_blocked_body([BLOCKED_DISALLOWED_HORIZON], charter=ch)
        body["_notices"] = notices
        return body
    if inputs.max_game_steps is not None and int(inputs.max_game_steps) != CHARTER_MAX_GAME_STEPS:
        body = _preflight_blocked_body([BLOCKED_DISALLOWED_HORIZON], charter=ch)
        body["_notices"] = notices
        return body

    ec = ch.get("evaluation_charter")
    if isinstance(ec, dict) and str(ec.get("charter_status") or "") == CHARTER_READY_WARNINGS:
        notices.append("m57_charter_ready_with_upstream_warnings_non_blocking")

    digest = m57_charter_digest(ch)
    ib = dict(cast(dict[str, Any], build_fixture_execution()["input_bindings"]))
    ib["m57_charter_artifact_sha256"] = digest
    ib["candidate_checkpoint_sha256"] = cand_exp
    ep_pref = _execution_plan_template(
        execution_performed=False,
        attempt_requested=1,
        attempt_completed=0,
        opponent_normalized=opponent,
    )
    ep_pref["preflight_candidate_checkpoint_verified"] = bool(inputs.candidate_checkpoint)

    body = build_fixture_execution()
    body["profile"] = PROFILE_OPERATOR_PREFLIGHT
    body["input_bindings"] = ib
    body["execution_plan"] = ep_pref
    body["execution_result"] = dict(build_fixture_execution()["execution_result"])
    cast(dict[str, Any], body["execution_result"])["execution_status"] = STATUS_PREFLIGHT_READY
    cast(dict[str, Any], body["execution_result"])["blocked_reasons"] = []
    cast(dict[str, Any], body["execution_result"])["warnings"] = notices
    body["_notices"] = notices
    body["_blocked_reasons_top"] = []
    return body


@dataclass(frozen=True)
class OperatorDeclaredExecutionInputs:
    declared_execution_json: Path
    m57_charter_json: Path
    expected_candidate_sha256: str


def build_operator_declared_execution(
    inputs: OperatorDeclaredExecutionInputs,
) -> dict[str, Any]:
    notices: list[str] = []
    ch, errs = load_m57_charter(inputs.m57_charter_json.resolve())
    cand_exp = str(inputs.expected_candidate_sha256).strip().lower()
    if len(cand_exp) != 64 or any(c not in "0123456789abcdef" for c in cand_exp):
        errs2 = errs + [BLOCKED_CANDIDATE_IDENTITY_MISMATCH]
        merged = sorted(set(errs2))
        if ch is None:
            return _preflight_blocked_body(merged, charter=None)
        b = _preflight_blocked_body(merged if merged else errs2, charter=ch)
        b["_notices"] = notices
        return b
    if ch is None:
        b = _preflight_blocked_body(errs or [BLOCKED_INVALID_M57_CHARTER], charter=None)
        b["_notices"] = notices
        return b
    if errs:
        b = _preflight_blocked_body(errs, charter=ch)
        b["_notices"] = notices
        return b
    dec_path = inputs.declared_execution_json.resolve()
    if not dec_path.is_file():
        b = _preflight_blocked_body([BLOCKED_INVALID_M57_CHARTER], charter=ch)
        b["_notices"] = notices
        return b
    try:
        txt = dec_path.read_text(encoding="utf-8")
        declared_obj = cast(dict[str, Any], json.loads(txt))
        if not isinstance(declared_obj, dict):
            raise ValueError()
    except (OSError, json.JSONDecodeError, ValueError):
        b = _preflight_blocked_body([BLOCKED_INVALID_M57_CHARTER], charter=ch)
        b["_notices"] = notices
        return b
    blob = canonical_json_dumps(declared_obj)
    if emission_has_private_path_patterns(blob):
        return _preflight_blocked_body([BLOCKED_PRIVATE_BOUNDARY_VIOLATION], charter=ch)

    if validate_execution_claim_flags(declared_obj):
        return _preflight_blocked_body([BLOCKED_CLAIM_FLAGS_VIOLATION], charter=ch)

    dib = declared_obj.get("input_bindings")
    if isinstance(dib, dict):
        csha = str(dib.get("candidate_checkpoint_sha256") or "").strip().lower()
        if csha != cand_exp:
            return _preflight_blocked_body([BLOCKED_CANDIDATE_CHECKPOINT_SHA_MISMATCH], charter=ch)
        msha = str(dib.get("m57_charter_artifact_sha256") or "").strip().lower()
        if msha and msha != m57_charter_digest(ch):
            return _preflight_blocked_body([BLOCKED_INVALID_M57_ARTIFACT_SEAL], charter=ch)

    merged_body = dict(build_fixture_execution())
    merged_body["profile"] = PROFILE_OPERATOR_DECLARED
    merged_body["input_bindings"] = dict(
        cast(dict[str, Any], merged_body["input_bindings"]),
        m57_charter_artifact_sha256=m57_charter_digest(ch),
        candidate_checkpoint_sha256=cand_exp,
    )
    merged_body["execution_plan"] = declared_obj.get(
        "execution_plan",
        merged_body["execution_plan"],
    )
    merged_body["execution_result"] = declared_obj.get(
        "execution_result",
        merged_body["execution_result"],
    )
    merged_body["attempts"] = declared_obj.get("attempts", [])
    agg = declared_obj.get("aggregation")
    if isinstance(agg, dict):
        merged_body["aggregation"] = agg
    cf = declared_obj.get("claim_flags")
    if isinstance(cf, dict):
        merged_cf = dict(DEFAULT_CLAIM_FLAGS)
        merged_cf.update(cf)
        merged_body["claim_flags"] = merged_cf
    merged_body["_notices"] = notices
    merged_body["_blocked_reasons_top"] = []
    return merged_body


def apply_completed_attempts_to_body(
    *,
    charter: dict[str, Any],
    attempts: list[dict[str, Any]],
    durations_s: list[float],
    requested: int,
    warnings: list[str],
    opponent_norm: str,
) -> dict[str, Any]:
    body = dict(build_fixture_execution())
    digest = m57_charter_digest(charter)
    ib = dict(cast(dict[str, Any], body["input_bindings"]))
    ib["m57_charter_artifact_sha256"] = digest
    body["profile"] = PROFILE_OPERATOR_LOCAL_EXECUTION

    agg_completed = sum(1 for a in attempts if isinstance(a, dict) and a.get("ok") is True)

    tac: int | None = None
    if attempts:
        parts: list[int] = []
        for a in attempts:
            if not isinstance(a, dict):
                continue
            ac = a.get("action_count")
            try:
                parts.append(int(ac) if ac is not None else 0)
            except (TypeError, ValueError):
                parts.append(0)
        tac = int(sum(parts))

    all_replays = bool(attempts) and all(
        bool(a.get("replay_saved")) for a in attempts if isinstance(a, dict)
    )

    any_fail = agg_completed != len(attempts) or agg_completed != requested
    agg_block: dict[str, Any] = {
        "attempt_count_requested": requested,
        "attempt_count_completed": agg_completed,
        "total_action_count": tac,
        "all_replays_saved": all_replays,
    }

    last: dict[str, Any] = attempts[-1] if attempts else {}
    replay_sha = None
    for a in reversed(attempts):
        if isinstance(a, dict) and a.get("replay_sha256"):
            replay_sha = a.get("replay_sha256")
            break

    merged_warnings = list(warnings)
    merged_blocked_reasons = sorted(
        {
            str(br)
            for a in attempts
            if isinstance(a, dict)
            for br in (cast(list[Any], a.get("blocked_reasons") or []) or [])
        },
    )

    xs = STATUS_EXECUTION_COMPLETED if not any_fail else STATUS_EXECUTION_BLOCKED
    if not any_fail and merged_warnings:
        xs = STATUS_EXECUTION_COMPLETED_WARNINGS

    exec_result = {
        "execution_status": xs,
        "blocked_reasons": merged_blocked_reasons,
        "warnings": merged_warnings,
        "live_sc2_executed": bool(not any_fail),
        "candidate_adapter_loaded": bool(not any_fail),
        "candidate_policy_control_confirmed": bool(not any_fail),
        "replay_saved": bool(last.get("replay_saved")),
        "replay_sha256": replay_sha,
        "game_steps_observed": last.get("game_steps_observed"),
        "observation_count": last.get("observation_count"),
        "action_count": last.get("action_count"),
        "sc2_result_metadata": last.get("sc2_result_metadata"),
        "duration_seconds": sum(durations_s) if durations_s else None,
    }

    exec_plan = _execution_plan_template(
        execution_performed=agg_completed >= 1,
        attempt_requested=requested,
        attempt_completed=agg_completed,
        opponent_normalized=opponent_norm,
    )

    claims = dict(DEFAULT_CLAIM_FLAGS)
    if not any_fail and agg_completed >= 1:
        claims.update(
            {
                "evaluation_execution_performed": True,
                "bounded_adapter_execution_performed": True,
                "torch_load_invoked_for_execution": True,
                "checkpoint_blob_loaded_for_execution": True,
                "live_sc2_executed": True,
                "gpu_inference_executed": True,
            },
        )

    allowed = dict(cast(dict[str, Any], body["allowed_metrics"]))
    allowed.update(
        {
            "live_sc2_executed": bool(exec_result["live_sc2_executed"]),
            "replay_saved": bool(exec_result["replay_saved"]),
            "action_count": exec_result.get("action_count"),
            "game_steps_observed": exec_result.get("game_steps_observed"),
            "observation_count": exec_result.get("observation_count"),
            "adapter_status": last.get("adapter_status"),
            "sc2_result_metadata": exec_result.get("sc2_result_metadata"),
            "refusal_status": None if not merged_blocked_reasons else merged_blocked_reasons[0],
        },
    )

    body["input_bindings"] = ib
    body["attempts"] = list(attempts)
    body["aggregation"] = agg_block
    body["execution_plan"] = exec_plan
    body["execution_result"] = exec_result
    body["claim_flags"] = claims
    body["allowed_metrics"] = allowed
    body["_notices"] = list(warnings)
    body["_blocked_reasons_top"] = merged_blocked_reasons
    return body


def build_execution_report(
    body_sealed: dict[str, Any],
    *,
    blocked: list[str],
    notices: list[str],
) -> dict[str, Any]:
    er = body_sealed.get("execution_result")
    xs = STATUS_FIXTURE_SCHEMA_ONLY
    br: list[str] = []
    wl: list[str] = list(notices)
    if isinstance(er, dict):
        xs = str(er.get("execution_status") or xs)
        br = [str(x) for x in cast(list[Any], er.get("blocked_reasons") or [])]
        w2 = er.get("warnings")
        if isinstance(w2, list):
            wl = [str(x) for x in w2] + list(notices)
    if blocked:
        br = sorted(set(blocked + br))
    summary = f"V15-M58 / {xs}"
    if br:
        summary += f" blocked: {', '.join(br)}"
    return {
        "contract_id": REPORT_CONTRACT_ID,
        "milestone": MILESTONE,
        "execution_status": xs,
        "summary": summary,
        "strongest_allowed_claim": STRONGEST_ALLOWED,
        "warnings": wl,
        "blocked_reasons": br,
        "non_claims": list(NON_CLAIMS),
        "next_recommended_step": f"{RECOMMENDED_NEXT_MILESTONE} — {RECOMMENDED_NEXT_TITLE}",
    }


def build_execution_checklist(body: dict[str, Any]) -> str:
    er = body.get("execution_result") if isinstance(body.get("execution_result"), dict) else {}
    xs = str(cast(dict[str, Any], er).get("execution_status"))
    bl = cast(list[Any], cast(dict[str, Any], er).get("blocked_reasons") or [])
    lines = [
        "# V15-M58 — Bounded Candidate Adapter Evaluation Execution Attempt Checklist",
        "",
        f"- **Execution status:** `{xs}`",
    ]
    if bl:
        lines.append("- **Blocked reasons:**")
        for item in bl:
            lines.append(f"  - `{item}`")
    else:
        lines.append("- **Blocked reasons:** none")
    for gid, txt in (
        ("E0", "M57 charter present and valid"),
        ("E1", "M57 route to M58 is recommended_not_executed"),
        ("E2", "Latest candidate checkpoint SHA matches expected"),
        ("E3", "Checkpoint path hashes to expected when supplied"),
        ("E4", "Candidate-live adapter path is M52A-compatible (subprocess delegate)"),
        ("E5", "Baseline passive_or_scripted only"),
        ("E6", "Map / horizon match M57 charter"),
        ("E7", "Replay capture required for live execution"),
        ("E8", "Live SC2 execution status recorded"),
        ("E9", "Action / observation / completion metrics recorded"),
        ("E10", "Benchmark/pass/strength/promotion flags remain false"),
        ("E11", "Raw out/replay/checkpoint evidence stays local-only"),
    ):
        lines.append(f"- **{gid}** — {txt}")
    lines.append("")
    return "\n".join(lines)


def execution_is_blocked_profile(body: dict[str, Any]) -> bool:
    er = body.get("execution_result")
    if isinstance(er, dict):
        xs = str(er.get("execution_status") or "")
        if xs in (STATUS_PREFLIGHT_BLOCKED, STATUS_EXECUTION_BLOCKED):
            return True
        blocked = cast(list[Any], er.get("blocked_reasons") or [])
        if blocked:
            return True
        if xs.startswith("blocked_"):
            return True
    top = cast(list[Any], body.get("_blocked_reasons_top") or [])
    return bool(top)


def emit_forbidden_refusal(output_dir: Path, *, flags: list[str]) -> None:
    body = dict(build_fixture_execution())
    exec_res = dict(cast(dict[str, Any], body["execution_result"]))
    exec_res["blocked_reasons"] = [f"forbidden_cli_flag:{','.join(sorted(flags))}"]
    exec_res["execution_status"] = STATUS_PREFLIGHT_BLOCKED
    body["execution_result"] = exec_res
    write_execution_artifacts(output_dir, body_unsealed=body)


def write_execution_artifacts(
    output_dir: Path,
    *,
    body_unsealed: dict[str, Any],
) -> tuple[dict[str, Any], tuple[Path, Path, Path]]:
    out = Path(output_dir).resolve()
    out.mkdir(parents=True, exist_ok=True)
    wrk = dict(body_unsealed)
    notices = list(cast(list[Any], wrk.pop("_notices", []) or []))
    top_blocked_raw = cast(list[Any], wrk.pop("_blocked_reasons_top", []) or [])
    blk = sorted({str(x) for x in top_blocked_raw})

    to_seal = cast(dict[str, Any], redact_paths_in_value(wrk))
    to_seal["artifact_sha256"] = None

    er_in = dict(cast(dict[str, Any], to_seal.get("execution_result") or {}))
    er_blocked_existing = sorted(
        str(x) for x in cast(list[Any], er_in.get("blocked_reasons") or []) if str(x).strip()
    )
    merged_b = sorted(set(blk + er_blocked_existing))
    if merged_b:
        er_in["blocked_reasons"] = merged_b
        to_seal["execution_result"] = er_in

    sealed = seal_m58_body(dict(to_seal))

    merged_for_report = sorted(
        {
            *(str(x) for x in cast(list[Any], er_in.get("blocked_reasons") or [])),
            *(str(x) for x in blk),
        },
    )

    report = build_execution_report(sealed, blocked=merged_for_report, notices=notices)
    chk = build_execution_checklist(sealed)

    main_p = out / FILENAME_MAIN_JSON
    main_p.write_text(canonical_json_dumps(sealed) + "\n", encoding="utf-8")
    rep_p = out / REPORT_FILENAME
    rep_p.write_text(canonical_json_dumps(report) + "\n", encoding="utf-8")
    ch_p = out / CHECKLIST_FILENAME
    ch_p.write_text(chk, encoding="utf-8")

    return sealed, (main_p, rep_p, ch_p)


def validate_attempt_bounds(n: int) -> bool:
    try:
        v = int(n)
    except (TypeError, ValueError):
        return False
    return MIN_ATTEMPT_COUNT <= v <= MAX_ATTEMPT_COUNT


def build_blocked_execution_body(
    reasons: list[str],
    *,
    charter: dict[str, Any] | None,
) -> dict[str, Any]:
    return _preflight_blocked_body(sorted(set(reasons)), charter=charter)
