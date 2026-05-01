"""V15-M52A — candidate live adapter spike IO (M51-bound; watchability only)."""

from __future__ import annotations

import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any, cast

from starlab.runs.json_util import canonical_json_dumps, sha256_hex_of_canonical_json
from starlab.sc2.harness import run_match_execution
from starlab.sc2.match_config import (
    BURNYSC2_OPPONENT_MODE_PASSIVE_BOT,
    BURNYSC2_POLICY_V15_M52A_CANDIDATE_PROJECTION_SPIKE_V1,
    BoundedHorizon,
    MapSpec,
    MatchConfig,
)
from starlab.v15.environment_lock_io import redact_paths_in_value
from starlab.v15.m31_candidate_checkpoint_evaluation_harness_gate_io import (
    emission_has_private_path_patterns,
)
from starlab.v15.m51_live_candidate_watchability_harness_io import (
    emit_m51_fixture_ci,
    proof_record_to_dict,
    sha256_hex_file_optional,
)
from starlab.v15.m51_live_candidate_watchability_harness_models import (
    CONTRACT_ID_M51,
    PROFILE_M51_SURFACE,
)
from starlab.v15.m51_live_candidate_watchability_harness_models import (
    FILENAME_MAIN_JSON as M51_FILENAME_MAIN_JSON,
)
from starlab.v15.m52_candidate_live_adapter_spike_models import (
    ACTION_VOCABULARY,
    ADAPTER_BLOCKED_LABEL,
    ADAPTER_FIXTURE_LABEL,
    ADAPTER_ID,
    ADAPTER_SPIKE_LABEL,
    BRIEF_FILENAME,
    CONTRACT_ID_M52A,
    DIGEST_FIELD,
    EMITTER_MODULE_M52A,
    FILENAME_MAIN_JSON,
    FORBIDDEN_FLAG_TO_REFUSAL,
    M51_UPSTREAM_HONESTY_FALSE_KEYS,
    M52A_DECLARED_OVERCLAIM_KEYS,
    M52A_HONESTY_FALSE_KEYS,
    MILESTONE_LABEL_M52A,
    NON_CLAIMS_M52A,
    PROFILE_FIXTURE_CI,
    PROFILE_ID_FIXTURE_CI,
    PROFILE_ID_OPERATOR_DECLARED,
    PROFILE_ID_OPERATOR_LOCAL_ADAPTER,
    PROFILE_ID_OPERATOR_PREFLIGHT,
    PROFILE_M52A_SURFACE,
    PROFILE_OPERATOR_DECLARED,
    PROFILE_OPERATOR_PREFLIGHT,
    PROJECTION_ID,
    REFUSED_ACTION_MAPPING_MISSING,
    REFUSED_BENCHMARK_CLAIM,
    REFUSED_CANDIDATE_CHECKPOINT_MISSING,
    REFUSED_CANDIDATE_CHECKPOINT_SHA,
    REFUSED_CANDIDATE_MODEL_LOAD_FAILED,
    REFUSED_LIVE_SC2_RUNTIME,
    REFUSED_M51_CONTRACT_INVALID,
    REFUSED_M51_HONESTY,
    REFUSED_M51_ROUTE_NOT_12HR_REHEARSAL,
    REFUSED_M51_SHA_MISMATCH,
    REFUSED_MAP_MISSING,
    REFUSED_OPERATOR_AUTH,
    REFUSED_SC2_ROOT,
    REPORT_FILENAME,
    ROUTE_STATUS_RECOMMENDED_NOT_EXECUTED,
    ROUTE_TO_M52_BLOCKER_REHEARSAL,
    RUNNER_MODULE_M52A,
    SCHEMA_VERSION,
    STATUS_FIXTURE_SCHEMA_ONLY,
    STATUS_PREFLIGHT_BLOCKED,
    STATUS_PREFLIGHT_READY,
    STATUS_PREFLIGHT_READY_WARNINGS,
    STATUS_SPIKE_BLOCKED,
    STATUS_SPIKE_COMPLETED,
    STATUS_SPIKE_FAILED,
)

M52_ROUTE_NOT_EXECUTED = ROUTE_STATUS_RECOMMENDED_NOT_EXECUTED


def profile_catalog_id_for_emit(*, emit_profile_short: str) -> str:
    if emit_profile_short == PROFILE_FIXTURE_CI:
        return PROFILE_ID_FIXTURE_CI
    if emit_profile_short == PROFILE_OPERATOR_PREFLIGHT:
        return PROFILE_ID_OPERATOR_PREFLIGHT
    if emit_profile_short == PROFILE_OPERATOR_DECLARED:
        return PROFILE_ID_OPERATOR_DECLARED
    return PROFILE_M52A_SURFACE


def _parse_json_object(path: Path) -> dict[str, Any]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ValueError("JSON root must be an object")
    return raw


def _seal_ok(raw: dict[str, Any]) -> bool:
    seal_in = raw.get(DIGEST_FIELD)
    if seal_in is None:
        return False
    wo = {k: v for k, v in raw.items() if k != DIGEST_FIELD}
    computed = sha256_hex_of_canonical_json(wo)
    return str(seal_in).lower() == computed.lower()


def _sha_like(v: object) -> bool:
    if not isinstance(v, str):
        return False
    s = v.strip().lower()
    return len(s) == 64 and all(c in "0123456789abcdef" for c in s)


def m51_upstream_honesty_violation(m51: dict[str, Any]) -> bool:
    return any(m51.get(k) is True for k in M51_UPSTREAM_HONESTY_FALSE_KEYS)


def structural_m51_issues_for_m52a(
    m51: dict[str, Any],
    *,
    require_canonical_seal: bool,
) -> list[str]:
    errs: list[str] = []
    if str(m51.get("contract_id", "")) != CONTRACT_ID_M51:
        errs.append("m51_contract_id_mismatch")
    surf = str(m51.get("profile_surface") or "")
    if surf != PROFILE_M51_SURFACE:
        errs.append("m51_profile_surface_mismatch")
    if require_canonical_seal and not _seal_ok(m51):
        errs.append("m51_seal_invalid")
    rr = m51.get("route_recommendation")
    if not isinstance(rr, dict):
        errs.append("m51_route_missing")
    else:
        r = str(rr.get("route") or "").strip()
        rs = str(rr.get("route_status") or "").strip()
        if r != ROUTE_TO_M52_BLOCKER_REHEARSAL:
            errs.append("m51_route_not_to_12hr_rehearsal")
        if rs and rs != M52_ROUTE_NOT_EXECUTED:
            errs.append("m51_route_status_not_recommended_only")
    return errs


def validate_m51_for_m52a(
    m51: dict[str, Any] | None,
    *,
    expected_sha256_lower: str | None,
    require_canonical_seal: bool,
) -> tuple[list[str], str]:
    if m51 is None:
        return [REFUSED_M51_CONTRACT_INVALID], ""

    digest = str(m51.get(DIGEST_FIELD) or "").lower()
    errs = structural_m51_issues_for_m52a(m51, require_canonical_seal=require_canonical_seal)
    codes: list[str] = []

    if errs:
        if "m51_contract_id_mismatch" in errs or "m51_profile_surface_mismatch" in errs:
            codes.append(REFUSED_M51_CONTRACT_INVALID)
        if "m51_seal_invalid" in errs:
            codes.append(REFUSED_M51_CONTRACT_INVALID)
        if "m51_route_missing" in errs or "m51_route_not_to_12hr_rehearsal" in errs:
            codes.append(REFUSED_M51_ROUTE_NOT_12HR_REHEARSAL)
        if "m51_route_status_not_recommended_only" in errs:
            codes.append(REFUSED_M51_ROUTE_NOT_12HR_REHEARSAL)
        if codes:
            return sorted(set(codes)), digest

    if expected_sha256_lower is not None and expected_sha256_lower.strip():
        exp = expected_sha256_lower.strip().lower()
        if not _sha_like(exp):
            return [REFUSED_M51_SHA_MISMATCH], digest
        if digest != exp:
            return [REFUSED_M51_SHA_MISMATCH], digest

    if m51_upstream_honesty_violation(m51):
        return [REFUSED_M51_HONESTY], digest

    return [], digest


def _honesty_m52a_block(
    *,
    torch_load: bool,
    checkpoint_blob: bool,
    live_sc2: bool,
) -> dict[str, Any]:
    out: dict[str, Any] = {k: False for k in M52A_HONESTY_FALSE_KEYS}
    out["torch_load_invoked"] = bool(torch_load)
    out["checkpoint_blob_loaded"] = bool(checkpoint_blob)
    out["live_sc2_executed"] = bool(live_sc2)
    return out


def _route_m52b_placeholder() -> dict[str, Any]:
    return {
        "route": ROUTE_TO_M52_BLOCKER_REHEARSAL,
        "route_status": M52_ROUTE_NOT_EXECUTED,
    }


def _m51_binding_summary(m51: dict[str, Any] | None) -> dict[str, Any]:
    if m51 is None:
        return {
            "contract_id": None,
            "artifact_sha256": None,
            "route": ROUTE_TO_M52_BLOCKER_REHEARSAL,
            "route_status": None,
        }
    rr = m51.get("route_recommendation")
    r = ROUTE_TO_M52_BLOCKER_REHEARSAL
    rs = None
    if isinstance(rr, dict):
        r = str(rr.get("route") or ROUTE_TO_M52_BLOCKER_REHEARSAL)
        rs = str(rr.get("route_status") or "")
    return {
        "contract_id": str(m51.get("contract_id") or ""),
        "artifact_sha256": str(m51.get(DIGEST_FIELD) or "").lower(),
        "route": r,
        "route_status": rs,
    }


def seal_m52a_body(body: dict[str, Any]) -> dict[str, Any]:
    wo = {k: v for k, v in body.items() if k != DIGEST_FIELD}
    digest = sha256_hex_of_canonical_json(wo)
    sealed = dict(wo)
    sealed[DIGEST_FIELD] = digest
    return sealed


def build_m52a_report(sealed: dict[str, Any]) -> dict[str, Any]:
    base = {k: v for k, v in sealed.items() if k != DIGEST_FIELD}
    digest = sha256_hex_of_canonical_json(base)
    return {
        "report_kind": "v15_candidate_live_adapter_spike_report",
        "report_version": "m52a",
        "milestone": MILESTONE_LABEL_M52A,
        "contract_id": CONTRACT_ID_M52A,
        "profile_id": sealed.get("profile_id"),
        DIGEST_FIELD: digest,
        "adapter_status": sealed.get("adapter_status"),
    }


def build_m52a_brief_md(*, sealed: dict[str, Any]) -> str:
    m51b = sealed.get("m51_binding") or {}
    ad = sealed.get("adapter") or {}
    wr = sealed.get("watchability_run") or {}
    lines = [
        "# V15-M52A candidate live adapter spike brief",
        "",
        "## M51 binding",
        f"- `contract_id`: `{m51b.get('contract_id', '')}`",
        f"- `artifact_sha256`: `{m51b.get('artifact_sha256', '')}`",
        f"- `route`: `{m51b.get('route', '')}`",
        f"- `route_status`: `{m51b.get('route_status', '')}`",
        "",
        "## Adapter",
        f"- `adapter_status`: `{sealed.get('adapter_status', '')}`",
        f"- `adapter_kind`: `{sealed.get('adapter_kind', '')}`",
        f"- `adapter_id`: `{ad.get('adapter_id', '')}`",
        f"- `candidate_output_projection`: `{ad.get('candidate_output_projection', '')}`",
        f"- `live_sc2_executed`: `{wr.get('live_sc2_executed', '')}`",
        "",
        "## Non-claims",
    ]
    ncl = sealed.get("non_claims") or []
    if isinstance(ncl, list):
        lines.extend([f"- `{x}`" for x in ncl])
    lines.extend(
        [
            "",
            "---",
            "",
            "V15-M52A is a candidate-to-live policy adapter spike for watchability only. "
            "It is not benchmark execution, not benchmark pass/fail, not strength evaluation, "
            "not checkpoint promotion, and not the 12-hour run.",
            "",
        ]
    )
    return "\n".join(lines) + "\n"


def _assert_no_path_leak(blob: str) -> None:
    if emission_has_private_path_patterns(blob):
        raise RuntimeError("V15-M52A emission leaked path patterns into public artifacts")


def refusal_code_from_forbidden_flags(flags: list[str]) -> str:
    fs = sorted(set(flags))
    for f in fs:
        if f in FORBIDDEN_FLAG_TO_REFUSAL:
            return FORBIDDEN_FLAG_TO_REFUSAL[f]
    return REFUSED_BENCHMARK_CLAIM


def _refs(codes: list[str]) -> list[dict[str, str]]:
    seen: set[str] = set()
    out: list[dict[str, str]] = []
    for c in codes:
        if c not in seen:
            seen.add(c)
            out.append({"code": c, "detail": c})
    return out


def _empty_watchability_run() -> dict[str, Any]:
    return {
        "live_sc2_executed": False,
        "run_mode": "preflight_only",
        "game_step": None,
        "max_game_steps": None,
        "action_count": None,
        "observation_count": None,
        "replay_saved": False,
    }


def _adapter_block(
    *,
    model_loaded: bool,
    torch_load: bool,
    checkpoint_blob: bool,
    projection: str | None,
) -> dict[str, Any]:
    return {
        "adapter_id": ADAPTER_ID,
        "candidate_output_projection": projection,
        "action_vocabulary_size": len(ACTION_VOCABULARY),
        "model_loaded": model_loaded,
        "torch_load_invoked": torch_load,
        "checkpoint_blob_loaded": checkpoint_blob,
    }


def _assemble_m52a_body(
    *,
    adapter_status: str,
    adapter_kind: str,
    emit_profile_short: str,
    m51_plain: dict[str, Any] | None,
    m51_digest: str,
    refusals: list[str],
    adapter_block: dict[str, Any],
    watchability_run: dict[str, Any],
    candidate_identity: dict[str, Any],
    honesty_torch: bool,
    honesty_ckblob: bool,
    honesty_live: bool,
) -> dict[str, Any]:
    catalog_id = profile_catalog_id_for_emit(emit_profile_short=emit_profile_short)
    body: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "contract_id": CONTRACT_ID_M52A,
        "profile_id": catalog_id,
        "profile_surface": PROFILE_M52A_SURFACE,
        "milestone": MILESTONE_LABEL_M52A,
        "emitter_module": EMITTER_MODULE_M52A,
        "profile": emit_profile_short,
        "adapter_status": adapter_status,
        "adapter_kind": adapter_kind,
        "m51_binding": _m51_binding_summary(m51_plain),
        "candidate_identity": candidate_identity,
        "adapter": adapter_block,
        "watchability_run": watchability_run,
        "route_recommendation": _route_m52b_placeholder(),
        "refusals": _refs(refusals),
        "warnings": [],
        "non_claims": list(NON_CLAIMS_M52A),
        **_honesty_m52a_block(
            torch_load=honesty_torch,
            checkpoint_blob=honesty_ckblob,
            live_sc2=honesty_live,
        ),
    }
    if m51_digest:
        cast(dict[str, Any], body["m51_binding"])["artifact_sha256"] = m51_digest
    return body


def _emit_m52a_artifacts(
    sealed: dict[str, Any],
    output_dir: Path,
) -> tuple[dict[str, Any], tuple[Path, ...]]:
    output_dir.mkdir(parents=True, exist_ok=True)
    rep = cast(dict[str, Any], redact_paths_in_value(build_m52a_report(sealed)))
    brief = build_m52a_brief_md(sealed=sealed)
    p_main = output_dir / FILENAME_MAIN_JSON
    p_rep = output_dir / REPORT_FILENAME
    p_brf = output_dir / BRIEF_FILENAME
    p_main.write_text(canonical_json_dumps(sealed), encoding="utf-8")
    p_rep.write_text(canonical_json_dumps(rep), encoding="utf-8")
    p_brf.write_text(brief, encoding="utf-8")
    blob = canonical_json_dumps(sealed) + canonical_json_dumps(rep) + brief
    _assert_no_path_leak(blob)
    return sealed, (p_main, p_rep, p_brf)


def emit_m52a_forbidden_flag_refusal(
    output_dir: Path,
    *,
    emit_profile_short: str,
    triggered_flags: list[str],
) -> tuple[dict[str, Any], tuple[Path, ...]]:
    output_dir.mkdir(parents=True, exist_ok=True)
    primary = refusal_code_from_forbidden_flags(triggered_flags)
    bad = sorted(set(triggered_flags))
    body = _assemble_m52a_body(
        adapter_status=STATUS_PREFLIGHT_BLOCKED,
        adapter_kind=ADAPTER_BLOCKED_LABEL,
        emit_profile_short=emit_profile_short,
        m51_plain=None,
        m51_digest="",
        refusals=[primary],
        adapter_block=_adapter_block(
            model_loaded=False,
            torch_load=False,
            checkpoint_blob=False,
            projection=None,
        ),
        watchability_run=_empty_watchability_run(),
        candidate_identity={
            "candidate_checkpoint_sha256": None,
            "candidate_source": "fixture",
            "promotion_status": "not_promoted_candidate_only",
        },
        honesty_torch=False,
        honesty_ckblob=False,
        honesty_live=False,
    )
    body["forbidden_execution_cli_flags_seen"] = bad
    sealed = seal_m52a_body(cast(dict[str, Any], redact_paths_in_value(body)))
    return _emit_m52a_artifacts(sealed, output_dir)


def _fixture_candidate_identity() -> dict[str, Any]:
    return {
        "candidate_checkpoint_sha256": None,
        "candidate_source": "fixture",
        "promotion_status": "not_promoted_candidate_only",
    }


def emit_m52a_fixture_ci(output_dir: Path) -> tuple[dict[str, Any], tuple[Path, ...]]:
    sub = output_dir / "m51_upstream_fixture"
    emit_m51_fixture_ci(sub)
    m51_path = sub / M51_FILENAME_MAIN_JSON
    return emit_m52a_operator_preflight(
        output_dir,
        m51_path=m51_path,
        m51_plain_override=None,
        expected_m51_sha256_lower=None,
        emit_profile_short=PROFILE_FIXTURE_CI,
        require_canonical_seal=True,
        sc2_root=None,
        map_path=None,
        checkpoint_path=None,
        expected_candidate_sha256=None,
        m39_run_json_path=None,
    )


def emit_m52a_operator_preflight(
    output_dir: Path,
    *,
    m51_path: Path | None,
    m51_plain_override: dict[str, Any] | None = None,
    expected_m51_sha256_lower: str | None,
    emit_profile_short: str,
    require_canonical_seal: bool,
    sc2_root: Path | None,
    map_path: Path | None,
    checkpoint_path: Path | None,
    expected_candidate_sha256: str | None,
    m39_run_json_path: Path | None,
) -> tuple[dict[str, Any], tuple[Path, ...]]:
    output_dir.mkdir(parents=True, exist_ok=True)
    m51_plain: dict[str, Any] | None = None
    if m51_plain_override is not None:
        m51_plain = m51_plain_override
    elif m51_path is not None:
        rp = Path(m51_path).resolve()
        if rp.is_file():
            try:
                m51_plain = _parse_json_object(rp)
            except (json.JSONDecodeError, OSError, UnicodeError, ValueError):
                m51_plain = None

    codes, digest = validate_m51_for_m52a(
        m51_plain,
        expected_sha256_lower=expected_m51_sha256_lower,
        require_canonical_seal=require_canonical_seal,
    )

    warns: list[str] = []
    cid_body: dict[str, Any] = {
        "candidate_checkpoint_sha256": None,
        "candidate_source": "fixture",
        "promotion_status": "not_promoted_candidate_only",
    }

    ck_path = Path(checkpoint_path).resolve() if checkpoint_path is not None else None
    exp_ck = str(expected_candidate_sha256).strip().lower() if expected_candidate_sha256 else None

    if m39_run_json_path is not None and Path(m39_run_json_path).is_file():
        try:
            m39 = _parse_json_object(Path(m39_run_json_path).resolve())
        except (json.JSONDecodeError, OSError, UnicodeError, ValueError):
            m39 = {}
        if isinstance(m39, dict):
            cid_body["candidate_source"] = "m39_final_candidate"
            b = m39.get("final_candidate") or m39.get("checkpoint")
            if isinstance(b, dict):
                sh = str(b.get("sha256") or "")
                if sh:
                    cid_body["candidate_checkpoint_sha256"] = sh.lower()

    if ck_path is not None and ck_path.is_file():
        cid_body["candidate_source"] = "declared"
        sha_f = sha256_hex_file_optional(ck_path)
        cid_body["candidate_checkpoint_sha256"] = sha_f
        if exp_ck and sha_f != exp_ck:
            codes = sorted(set(codes + [REFUSED_CANDIDATE_CHECKPOINT_SHA]))
    elif exp_ck:
        cid_body["candidate_checkpoint_sha256"] = exp_ck
        cid_body["candidate_source"] = "declared"

    if (
        emit_profile_short == PROFILE_OPERATOR_PREFLIGHT
        and not codes
        and ck_path is None
        and not exp_ck
    ):
        warns.append("candidate_checkpoint_not_supplied_preflight_only")

    if sc2_root is not None and not Path(sc2_root).is_dir():
        warns.append("sc2_root_path_not_found_on_preflight_host")
    if map_path is not None and not Path(map_path).is_file():
        warns.append("map_path_not_found_on_preflight_host")

    if codes:
        st = STATUS_PREFLIGHT_BLOCKED
        kind = ADAPTER_BLOCKED_LABEL
    elif warns:
        st = STATUS_PREFLIGHT_READY_WARNINGS
        kind = ADAPTER_FIXTURE_LABEL
    else:
        st = STATUS_PREFLIGHT_READY
        kind = ADAPTER_FIXTURE_LABEL

    if emit_profile_short == PROFILE_FIXTURE_CI and not codes:
        st = STATUS_FIXTURE_SCHEMA_ONLY
        kind = ADAPTER_FIXTURE_LABEL

    body = _assemble_m52a_body(
        adapter_status=st,
        adapter_kind=kind,
        emit_profile_short=emit_profile_short,
        m51_plain=m51_plain,
        m51_digest=digest,
        refusals=codes,
        adapter_block=_adapter_block(
            model_loaded=False,
            torch_load=False,
            checkpoint_blob=False,
            projection=None,
        ),
        watchability_run=_empty_watchability_run(),
        candidate_identity=cid_body,
        honesty_torch=False,
        honesty_ckblob=False,
        honesty_live=False,
    )
    body["warnings"] = list(warns)
    sealed = seal_m52a_body(cast(dict[str, Any], redact_paths_in_value(body)))
    return _emit_m52a_artifacts(sealed, output_dir)


def emit_m52a_operator_declared(
    output_dir: Path,
    *,
    declared_path: Path,
    embedded_m51_path: Path | None,
    sc2_root: Path | None,
    map_path: Path | None,
    checkpoint_path: Path | None,
    expected_candidate_sha256: str | None,
    m39_run_json_path: Path | None,
) -> tuple[dict[str, Any], tuple[Path, ...]]:
    rp = Path(declared_path).resolve()
    raw_in = json.loads(rp.read_text(encoding="utf-8"))
    if not isinstance(raw_in, dict):
        raise ValueError("declared envelope must be a JSON object")
    declared = cast(dict[str, Any], redact_paths_in_value(raw_in))

    cid = str(declared.get("contract_id") or "")
    pid = str(declared.get("profile_id") or "")
    surface_ok = cid == CONTRACT_ID_M52A and pid in (
        PROFILE_M52A_SURFACE,
        PROFILE_ID_OPERATOR_DECLARED,
    )

    violations = [k for k in M52A_DECLARED_OVERCLAIM_KEYS if declared.get(k) is True]

    m51_plain: dict[str, Any] | None = None
    sm51 = declared.get("sealed_m51")
    if isinstance(sm51, dict):
        m51_plain = sm51
    elif embedded_m51_path is not None and Path(embedded_m51_path).is_file():
        try:
            m51_plain = _parse_json_object(Path(embedded_m51_path).resolve())
        except (json.JSONDecodeError, OSError, UnicodeError, ValueError):
            m51_plain = None

    exp_field = declared.get("expected_m51_watchability_sha256")
    exp_decl = (
        str(exp_field).strip().lower() if isinstance(exp_field, str) and exp_field.strip() else None
    )

    if not surface_ok or violations:
        body = _assemble_m52a_body(
            adapter_status=STATUS_PREFLIGHT_BLOCKED,
            adapter_kind=ADAPTER_BLOCKED_LABEL,
            emit_profile_short=PROFILE_OPERATOR_DECLARED,
            m51_plain=None,
            m51_digest="",
            refusals=[REFUSED_M51_CONTRACT_INVALID],
            adapter_block=_adapter_block(
                model_loaded=False,
                torch_load=False,
                checkpoint_blob=False,
                projection=None,
            ),
            watchability_run=_empty_watchability_run(),
            candidate_identity=_fixture_candidate_identity(),
            honesty_torch=False,
            honesty_ckblob=False,
            honesty_live=False,
        )
        body["refusals"] = _refs([REFUSED_M51_CONTRACT_INVALID])
        sealed = seal_m52a_body(cast(dict[str, Any], redact_paths_in_value(body)))
        return _emit_m52a_artifacts(sealed, output_dir.resolve())

    if m51_plain is None:
        body = _assemble_m52a_body(
            adapter_status=STATUS_PREFLIGHT_BLOCKED,
            adapter_kind=ADAPTER_BLOCKED_LABEL,
            emit_profile_short=PROFILE_OPERATOR_DECLARED,
            m51_plain=None,
            m51_digest="",
            refusals=[REFUSED_M51_CONTRACT_INVALID],
            adapter_block=_adapter_block(
                model_loaded=False,
                torch_load=False,
                checkpoint_blob=False,
                projection=None,
            ),
            watchability_run=_empty_watchability_run(),
            candidate_identity=_fixture_candidate_identity(),
            honesty_torch=False,
            honesty_ckblob=False,
            honesty_live=False,
        )
        body["refusals"] = _refs([REFUSED_M51_CONTRACT_INVALID])
        sealed = seal_m52a_body(cast(dict[str, Any], redact_paths_in_value(body)))
        return _emit_m52a_artifacts(sealed, output_dir.resolve())

    return emit_m52a_operator_preflight(
        output_dir.resolve(),
        m51_path=None,
        m51_plain_override=m51_plain,
        expected_m51_sha256_lower=exp_decl,
        emit_profile_short=PROFILE_OPERATOR_DECLARED,
        require_canonical_seal=False,
        sc2_root=sc2_root,
        map_path=map_path,
        checkpoint_path=checkpoint_path,
        expected_candidate_sha256=expected_candidate_sha256,
        m39_run_json_path=m39_run_json_path,
    )


@dataclass(frozen=True)
class M52aAdapterRunParams:
    m51_path: Path
    output_dir: Path
    sc2_root: Path
    map_path: Path
    candidate_checkpoint_path: Path
    expected_candidate_sha256: str
    game_step: int
    max_game_steps: int
    save_replay: bool
    device: str
    seed: int
    expected_m51_sha256: str | None
    operator_note_path: Path | None
    m39_run_json_path: Path | None


def run_m52a_operator_local_adapter_spike(
    params: M52aAdapterRunParams,
    *,
    allow_local: bool,
    authorize_spike: bool,
) -> tuple[dict[str, Any], tuple[Path, ...]]:
    from starlab.v15.m52_candidate_live_adapter_spike_projection import (
        load_checkpoint_state_dict,
        make_pick_action_index_from_state,
    )

    out = params.output_dir.resolve()
    out.mkdir(parents=True, exist_ok=True)
    spike_sub = out / "candidate_live_adapter_watch"
    spike_sub.mkdir(parents=True, exist_ok=True)

    m51_plain: dict[str, Any] | None = None
    if params.m51_path.is_file():
        try:
            m51_plain = _parse_json_object(params.m51_path.resolve())
        except (json.JSONDecodeError, OSError, UnicodeError, ValueError):
            m51_plain = None

    codes, digest = validate_m51_for_m52a(
        m51_plain,
        expected_sha256_lower=params.expected_m51_sha256,
        require_canonical_seal=True,
    )

    if not allow_local or not authorize_spike:
        codes = sorted(set(codes + [REFUSED_OPERATOR_AUTH]))

    if not Path(params.candidate_checkpoint_path).is_file():
        codes = sorted(set(codes + [REFUSED_CANDIDATE_CHECKPOINT_MISSING]))

    exp_ck = str(params.expected_candidate_sha256).strip().lower()
    if not _sha_like(exp_ck):
        codes = sorted(set(codes + [REFUSED_CANDIDATE_CHECKPOINT_SHA]))

    ck_sha = (
        sha256_hex_file_optional(Path(params.candidate_checkpoint_path).resolve())
        if Path(params.candidate_checkpoint_path).is_file()
        else ""
    )
    if ck_sha and ck_sha != exp_ck:
        codes = sorted(set(codes + [REFUSED_CANDIDATE_CHECKPOINT_SHA]))

    if not Path(params.sc2_root).is_dir():
        codes.append(REFUSED_SC2_ROOT)
    if not Path(params.map_path).is_file():
        codes.append(REFUSED_MAP_MISSING)

    cid_body: dict[str, Any] = {
        "candidate_checkpoint_sha256": ck_sha or exp_ck,
        "candidate_source": "declared",
        "promotion_status": "not_promoted_candidate_only",
    }
    if params.m39_run_json_path is not None and Path(params.m39_run_json_path).is_file():
        cid_body["candidate_source"] = "m39_final_candidate"

    watch_run = _empty_watchability_run()
    watch_run.update(
        {
            "run_mode": "operator_local_candidate_adapter_spike",
            "game_step": int(params.game_step),
            "max_game_steps": int(params.max_game_steps),
        }
    )

    torch_on = False
    ck_blob = False
    model_loaded = False
    projection = None

    if codes:
        body = _assemble_m52a_body(
            adapter_status=STATUS_SPIKE_BLOCKED,
            adapter_kind=ADAPTER_BLOCKED_LABEL,
            emit_profile_short="operator_local_adapter_spike",
            m51_plain=m51_plain,
            m51_digest=digest,
            refusals=codes,
            adapter_block=_adapter_block(
                model_loaded=False,
                torch_load=False,
                checkpoint_blob=False,
                projection=None,
            ),
            watchability_run=watch_run,
            candidate_identity=cid_body,
            honesty_torch=False,
            honesty_ckblob=False,
            honesty_live=False,
        )
        body["profile_id"] = PROFILE_ID_OPERATOR_LOCAL_ADAPTER
        body["runner_module"] = RUNNER_MODULE_M52A
        sealed = seal_m52a_body(cast(dict[str, Any], redact_paths_in_value(body)))
        return _emit_m52a_artifacts(sealed, out)

    try:
        st = load_checkpoint_state_dict(
            str(Path(params.candidate_checkpoint_path).resolve()),
            map_location=params.device,
        )
        torch_on = True
        ck_blob = True
        model_loaded = True
        projection = PROJECTION_ID
    except (OSError, ValueError, RuntimeError, ImportError) as exc:
        body = _assemble_m52a_body(
            adapter_status=STATUS_SPIKE_BLOCKED,
            adapter_kind=ADAPTER_BLOCKED_LABEL,
            emit_profile_short="operator_local_adapter_spike",
            m51_plain=m51_plain,
            m51_digest=digest,
            refusals=[REFUSED_CANDIDATE_MODEL_LOAD_FAILED],
            adapter_block=_adapter_block(
                model_loaded=False,
                torch_load=torch_on,
                checkpoint_blob=False,
                projection=None,
            ),
            watchability_run=watch_run,
            candidate_identity=cid_body,
            honesty_torch=torch_on,
            honesty_ckblob=False,
            honesty_live=False,
        )
        body["refusals"] = _refs([REFUSED_CANDIDATE_MODEL_LOAD_FAILED])
        body["load_error"] = str(exc)[:500]
        body["profile_id"] = PROFILE_ID_OPERATOR_LOCAL_ADAPTER
        body["runner_module"] = RUNNER_MODULE_M52A
        sealed = seal_m52a_body(cast(dict[str, Any], redact_paths_in_value(body)))
        return _emit_m52a_artifacts(sealed, out)

    try:
        pick_fn = make_pick_action_index_from_state(st)
    except (TypeError, ValueError) as exc:
        body = _assemble_m52a_body(
            adapter_status=STATUS_SPIKE_BLOCKED,
            adapter_kind=ADAPTER_BLOCKED_LABEL,
            emit_profile_short="operator_local_adapter_spike",
            m51_plain=m51_plain,
            m51_digest=digest,
            refusals=[REFUSED_ACTION_MAPPING_MISSING],
            adapter_block=_adapter_block(
                model_loaded=True,
                torch_load=True,
                checkpoint_blob=True,
                projection=None,
            ),
            watchability_run=watch_run,
            candidate_identity=cid_body,
            honesty_torch=True,
            honesty_ckblob=True,
            honesty_live=False,
        )
        body["refusals"] = _refs([REFUSED_ACTION_MAPPING_MISSING])
        body["projection_error"] = str(exc)[:500]
        body["profile_id"] = PROFILE_ID_OPERATOR_LOCAL_ADAPTER
        body["runner_module"] = RUNNER_MODULE_M52A
        sealed = seal_m52a_body(cast(dict[str, Any], redact_paths_in_value(body)))
        return _emit_m52a_artifacts(sealed, out)

    os.environ["SC2PATH"] = str(Path(params.sc2_root).resolve())

    cfg = MatchConfig(
        schema_version="1",
        adapter="burnysc2",
        seed=int(params.seed),
        bounded_horizon=BoundedHorizon(
            max_game_steps=int(params.max_game_steps),
            game_step=int(params.game_step),
        ),
        map=MapSpec(
            path=str(Path(params.map_path).resolve()),
            discover_under_maps_dir=False,
            battle_net_map_name=None,
        ),
        save_replay=bool(params.save_replay),
        replay_filename="validation.SC2Replay" if params.save_replay else None,
        burnysc2_policy=BURNYSC2_POLICY_V15_M52A_CANDIDATE_PROJECTION_SPIKE_V1,
        opponent_mode=BURNYSC2_OPPONENT_MODE_PASSIVE_BOT,
    )
    cfg.validate()

    spike_bundle = {"pick_action_index": pick_fn}
    hres = run_match_execution(
        cfg,
        output_dir=spike_sub,
        m52a_candidate_spike_bundle=spike_bundle,
    )

    live_ok = False
    if not hres.ok or hres.proof is None:
        body = _assemble_m52a_body(
            adapter_status=STATUS_SPIKE_FAILED,
            adapter_kind=ADAPTER_SPIKE_LABEL,
            emit_profile_short="operator_local_adapter_spike",
            m51_plain=m51_plain,
            m51_digest=digest,
            refusals=[REFUSED_LIVE_SC2_RUNTIME],
            adapter_block=_adapter_block(
                model_loaded=model_loaded,
                torch_load=torch_on,
                checkpoint_blob=ck_blob,
                projection=projection,
            ),
            watchability_run=watch_run,
            candidate_identity=cid_body,
            honesty_torch=torch_on,
            honesty_ckblob=ck_blob,
            honesty_live=False,
        )
        body["refusals"] = _refs([REFUSED_LIVE_SC2_RUNTIME])
        body["runtime_message"] = str(hres.message or "")[:500]
        body["profile_id"] = PROFILE_ID_OPERATOR_LOCAL_ADAPTER
        body["runner_module"] = RUNNER_MODULE_M52A
        sealed = seal_m52a_body(cast(dict[str, Any], redact_paths_in_value(body)))
        return _emit_m52a_artifacts(sealed, out)

    proof = hres.proof
    proof_d = proof_record_to_dict(proof)
    (spike_sub / "match_execution_proof.json").write_text(
        canonical_json_dumps(cast(dict[str, Any], redact_paths_in_value(proof_d))),
        encoding="utf-8",
    )

    live_ok = True
    watch_run["live_sc2_executed"] = True
    watch_run["action_count"] = int(proof.action_count)
    watch_run["observation_count"] = len(proof.observation_summaries)
    replay_saved = False
    if proof.replay is not None:
        replay_saved = bool(proof.replay.replay_saved)
    watch_run["replay_saved"] = replay_saved

    if params.operator_note_path is not None and Path(params.operator_note_path).is_file():
        txt = Path(params.operator_note_path).read_text(encoding="utf-8", errors="replace")
        (spike_sub / "operator_watch_note.md").write_text(txt, encoding="utf-8")

    body = _assemble_m52a_body(
        adapter_status=STATUS_SPIKE_COMPLETED,
        adapter_kind=ADAPTER_SPIKE_LABEL,
        emit_profile_short="operator_local_adapter_spike",
        m51_plain=m51_plain,
        m51_digest=digest,
        refusals=[],
        adapter_block=_adapter_block(
            model_loaded=model_loaded,
            torch_load=torch_on,
            checkpoint_blob=ck_blob,
            projection=projection,
        ),
        watchability_run=watch_run,
        candidate_identity=cid_body,
        honesty_torch=torch_on,
        honesty_ckblob=ck_blob,
        honesty_live=live_ok,
    )
    body["profile_id"] = PROFILE_ID_OPERATOR_LOCAL_ADAPTER
    body["runner_module"] = RUNNER_MODULE_M52A
    sealed = seal_m52a_body(cast(dict[str, Any], redact_paths_in_value(body)))

    replay_dir = spike_sub / "replay"
    replay_dir.mkdir(parents=True, exist_ok=True)
    if replay_saved:
        rp = replay_dir / "validation.SC2Replay"
        alt = spike_sub / "validation.SC2Replay"
        if alt.is_file() and not rp.is_file():
            rp.write_bytes(alt.read_bytes())

    return _emit_m52a_artifacts(sealed, out)
