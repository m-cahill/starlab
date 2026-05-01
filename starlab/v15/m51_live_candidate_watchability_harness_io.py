"""V15-M51 — live candidate watchability harness IO (M50-bound, sealed emission)."""

from __future__ import annotations

import hashlib
import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any, cast

from starlab.runs.json_util import canonical_json_dumps, sha256_hex_of_canonical_json
from starlab.sc2.artifacts import (
    ExecutionProofRecord,
    compute_artifact_hash,
    proof_record_to_hash_input_dict,
)
from starlab.sc2.harness import run_match_execution
from starlab.sc2.match_config import (
    BURNYSC2_OPPONENT_MODE_PASSIVE_BOT,
    BURNYSC2_POLICY_V15_M27_NONTRIVIAL_MACRO_SMOKE_V1,
    BoundedHorizon,
    MapSpec,
    MatchConfig,
)
from starlab.v15.environment_lock_io import redact_paths_in_value
from starlab.v15.m31_candidate_checkpoint_evaluation_harness_gate_io import (
    emission_has_private_path_patterns,
)
from starlab.v15.m50_scorecard_result_readout_decision_io import emit_m50_fixture_ci
from starlab.v15.m50_scorecard_result_readout_decision_models import (
    CONTRACT_ID_M50_READOUT,
    PROFILE_M50_SURFACE,
)
from starlab.v15.m50_scorecard_result_readout_decision_models import (
    FILENAME_MAIN_JSON as M50_FILENAME_MAIN_JSON,
)
from starlab.v15.m51_live_candidate_watchability_harness_models import (
    BEHAVIOR_TAGS_SUGGESTED,
    BRIEF_FILENAME,
    CANDIDATE_POLICY_FIXTURE,
    CANDIDATE_POLICY_SCAFFOLD,
    CANDIDATE_POLICY_UNAVAILABLE,
    CONTRACT_ID_M51,
    DIGEST_FIELD,
    EMITTER_MODULE_M51,
    FILENAME_MAIN_JSON,
    FORBIDDEN_FLAG_TO_REFUSAL,
    M50_UPSTREAM_HONESTY_FALSE_KEYS,
    M51_DECLARED_OVERCLAIM_KEYS,
    M51_HONESTY_FALSE_KEYS,
    MILESTONE_LABEL_M51,
    NON_CLAIMS_M51,
    POLICY_ADAPTER_SCAFFOLD_BURNY_M27_STYLE,
    PROFILE_FIXTURE_CI,
    PROFILE_ID_FIXTURE_CI,
    PROFILE_ID_OPERATOR_DECLARED,
    PROFILE_ID_OPERATOR_LOCAL_WATCHABILITY,
    PROFILE_ID_OPERATOR_PREFLIGHT,
    PROFILE_M51_SURFACE,
    PROFILE_OPERATOR_DECLARED,
    PROFILE_OPERATOR_PREFLIGHT,
    REFUSED_ADAPTER_MISSING,
    REFUSED_BENCHMARK_CLAIM,
    REFUSED_CANDIDATE_CHECKPOINT_SHA,
    REFUSED_CANDIDATE_IDENTITY,
    REFUSED_INVALID_DECLARED_M51,
    REFUSED_LIVE_SC2_RUNTIME,
    REFUSED_M50_CONTRACT_INVALID,
    REFUSED_M50_HONESTY,
    REFUSED_M50_ROUTE_EXECUTED,
    REFUSED_M50_ROUTE_NOT_WATCHABILITY,
    REFUSED_M50_SHA_MISMATCH,
    REFUSED_MAP_MISSING,
    REFUSED_MISSING_M50,
    REFUSED_OPERATOR_AUTH,
    REFUSED_SC2_ROOT,
    REPORT_FILENAME,
    ROUTE_STATUS_RECOMMENDED_NOT_EXECUTED,
    ROUTE_TO_M51_UPSTREAM,
    ROUTE_TO_M52,
    RUNNER_MODULE_M51,
    SCHEMA_VERSION,
    STATUS_BLOCKED_MISSING_ADAPTER,
    STATUS_FIXTURE_SCHEMA_ONLY,
    STATUS_LIVE_BLOCKED,
    STATUS_LIVE_COMPLETED_WARNINGS,
    STATUS_LIVE_FAILED,
    STATUS_PREFLIGHT_BLOCKED,
    STATUS_PREFLIGHT_READY,
    STATUS_PREFLIGHT_READY_WARNINGS,
    STATUS_SCAFFOLD_COMPLETED,
)

M51_ROUTE_NOT_EXECUTED = ROUTE_STATUS_RECOMMENDED_NOT_EXECUTED


def profile_catalog_id_for_emit(*, emit_profile_short: str) -> str:
    if emit_profile_short == PROFILE_FIXTURE_CI:
        return PROFILE_ID_FIXTURE_CI
    if emit_profile_short == PROFILE_OPERATOR_PREFLIGHT:
        return PROFILE_ID_OPERATOR_PREFLIGHT
    if emit_profile_short == PROFILE_OPERATOR_DECLARED:
        return PROFILE_ID_OPERATOR_DECLARED
    return PROFILE_M51_SURFACE


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


def m50_upstream_honesty_violation(m50: dict[str, Any]) -> bool:
    return any(m50.get(k) is True for k in M50_UPSTREAM_HONESTY_FALSE_KEYS)


def structural_m50_issues_for_m51(
    m50: dict[str, Any],
    *,
    require_canonical_seal: bool,
) -> list[str]:
    errs: list[str] = []
    if str(m50.get("contract_id", "")) != CONTRACT_ID_M50_READOUT:
        errs.append("m50_contract_id_mismatch")
    if str(m50.get("profile_id", "")) != PROFILE_M50_SURFACE:
        errs.append("m50_profile_id_mismatch")
    if require_canonical_seal and not _seal_ok(m50):
        errs.append("m50_seal_invalid")
    route = m50.get("route_recommendation")
    if not isinstance(route, dict):
        errs.append("m50_route_missing")
    else:
        next_r = str(route.get("next_route") or "").strip()
        rs = str(route.get("route_status") or "").strip()
        if next_r != ROUTE_TO_M51_UPSTREAM:
            errs.append("m51_route_expectation_failed")
        if rs and rs != M51_ROUTE_NOT_EXECUTED:
            errs.append("m51_route_status_not_recommended_only")
    return errs


def validate_m50_for_m51(
    m50: dict[str, Any] | None,
    *,
    expected_sha256_lower: str | None,
    require_canonical_seal: bool,
) -> tuple[list[str], str]:
    """Return refusal codes list (possibly empty) and M50 artifact digest lowercase."""

    if m50 is None:
        return [REFUSED_MISSING_M50], ""

    digest = str(m50.get(DIGEST_FIELD) or "").lower()
    errs = structural_m50_issues_for_m51(m50, require_canonical_seal=require_canonical_seal)
    codes: list[str] = []

    if errs:
        if "m50_contract_id_mismatch" in errs or "m50_profile_id_mismatch" in errs:
            codes.append(REFUSED_M50_CONTRACT_INVALID)
        if "m50_seal_invalid" in errs:
            codes.append(REFUSED_M50_CONTRACT_INVALID)
        if "m50_route_missing" in errs or "m51_route_expectation_failed" in errs:
            codes.append(REFUSED_M50_ROUTE_NOT_WATCHABILITY)
        if "m51_route_status_not_recommended_only" in errs:
            codes.append(REFUSED_M50_ROUTE_EXECUTED)
        if codes:
            return sorted(set(codes)), digest

    if expected_sha256_lower is not None and expected_sha256_lower.strip():
        exp = expected_sha256_lower.strip().lower()
        if not _sha_like(exp):
            return [REFUSED_M50_SHA_MISMATCH], digest
        if digest != exp:
            return [REFUSED_M50_SHA_MISMATCH], digest

    if m50_upstream_honesty_violation(m50):
        return [REFUSED_M50_HONESTY], digest

    return [], digest


def _honesty_m51_block(*, live_sc2_executed: bool) -> dict[str, Any]:
    out: dict[str, Any] = {k: False for k in M51_HONESTY_FALSE_KEYS}
    out["live_sc2_executed"] = bool(live_sc2_executed)
    return out


def _route_next_m52() -> dict[str, Any]:
    return {
        "route": ROUTE_TO_M52,
        "route_status": M51_ROUTE_NOT_EXECUTED,
    }


def _m50_binding_summary(m50: dict[str, Any] | None) -> dict[str, Any]:
    if m50 is None:
        return {
            "contract_id": None,
            "artifact_sha256": None,
            "route": ROUTE_TO_M51_UPSTREAM,
            "route_status": None,
        }
    rr = m50.get("route_recommendation")
    nr = ROUTE_TO_M51_UPSTREAM
    rs = None
    if isinstance(rr, dict):
        nr = str(rr.get("next_route") or ROUTE_TO_M51_UPSTREAM)
        rs = str(rr.get("route_status") or "")
    return {
        "contract_id": str(m50.get("contract_id") or ""),
        "artifact_sha256": str(m50.get(DIGEST_FIELD) or "").lower(),
        "route": nr,
        "route_status": rs,
    }


def _candidate_identity_for_preflight(
    *,
    checkpoint_path: Path | None,
    expected_ck_sha: str | None,
    m42: dict[str, Any] | None,
) -> tuple[dict[str, Any], list[str]]:
    refusals: list[str] = []

    cid = ""
    csha = ""
    source = "fixture"
    if m42 is not None:
        cid = str(m42.get("package_id") or m42.get("evaluation_package_id") or "m42_unknown")
        b = m42.get("checkpoint_bindings") or m42.get("bindings")
        if isinstance(b, dict):
            csha = str(
                b.get("final_candidate_checkpoint_sha256") or b.get("checkpoint_sha256") or ""
            )
        if not csha:
            idx = m42.get("final_candidate_checkpoint")
            if isinstance(idx, dict):
                csha = str(idx.get("sha256") or "")
        source = "m42"
    if checkpoint_path is not None and checkpoint_path.is_file():
        if not cid:
            cid = "declared_checkpoint_path"
        sha_f = sha256_hex_file_optional(checkpoint_path)
        if csha and sha_f and csha.lower() != sha_f.lower():
            refusals.append(REFUSED_CANDIDATE_CHECKPOINT_SHA)
        elif sha_f:
            csha = sha_f
        source = "declared"

    if expected_ck_sha is not None and expected_ck_sha.strip():
        exp = expected_ck_sha.strip().lower()
        if csha and csha.lower() != exp:
            refusals.append(REFUSED_CANDIDATE_CHECKPOINT_SHA)
        elif not csha:
            csha = exp

    promotion_status = "not_promoted_candidate_only"
    body = {
        "candidate_id": cid or "candidate_identity_optional",
        "candidate_checkpoint_sha256": csha or None,
        "candidate_source": source if cid or csha or m42 else "fixture",
        "promotion_status": promotion_status,
    }
    if refusals:
        body["candidate_id"] = body["candidate_id"] or "checkpoint_sha_mismatch"
    return body, refusals


def sha256_hex_file_optional(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest().lower()


def behavior_tags_from_proof_dict(proof: dict[str, Any]) -> list[str]:
    tags: list[str] = []
    seq = proof.get("status_sequence")
    if isinstance(seq, list):
        sl = [str(x) for x in seq]
        if any("in_game" in x for x in sl):
            tags.append("started_game")
        if any("configure" in x or "launch" in x for x in sl):
            tags.append("loaded_map")
        if any("bounded_exit" in x for x in sl):
            tags.append("bounded_exit")
    ac = proof.get("action_count")
    try:
        acn = int(ac) if ac is not None else 0
    except (TypeError, ValueError):
        acn = 0
    if acn > 0:
        tags.append("issued_actions")
    else:
        tags.append("no_actions_observed")
    lbs = proof.get("live_action_behavior_summary")
    if isinstance(lbs, dict):
        s = str(lbs.get("operator_readable_summary_v1") or "").lower()
        if "scout" in s:
            tags.append("scouted")
        if "macro" in s or "worker" in s:
            tags.append("built_workers")
    rep = proof.get("replay")
    if isinstance(rep, dict) and rep.get("replay_saved") is True:
        tags.append("replay_saved")
    return [t for t in tags if t in BEHAVIOR_TAGS_SUGGESTED]


def seal_m51_body(body: dict[str, Any]) -> dict[str, Any]:
    wo = {k: v for k, v in body.items() if k != DIGEST_FIELD}
    digest = sha256_hex_of_canonical_json(wo)
    sealed = dict(wo)
    sealed[DIGEST_FIELD] = digest
    return sealed


def build_m51_report(sealed: dict[str, Any]) -> dict[str, Any]:
    base = {k: v for k, v in sealed.items() if k != DIGEST_FIELD}
    digest = sha256_hex_of_canonical_json(base)
    return {
        "report_kind": "v15_live_candidate_watchability_harness_report",
        "report_version": "m51",
        "milestone": MILESTONE_LABEL_M51,
        "contract_id": CONTRACT_ID_M51,
        "profile_id": sealed.get("profile_id"),
        DIGEST_FIELD: digest,
        "watchability_status": sealed.get("watchability_status"),
    }


def build_m51_brief_md(*, sealed: dict[str, Any]) -> str:
    m50b = sealed.get("m50_binding") or {}
    cp = sealed.get("candidate_policy") or {}
    wr = sealed.get("watchability_run") or {}
    lines = [
        "# V15-M51 live candidate watchability harness brief",
        "",
        "## M50 binding",
        f"- `contract_id`: `{m50b.get('contract_id', '')}`",
        f"- `artifact_sha256`: `{m50b.get('artifact_sha256', '')}`",
        f"- `route`: `{m50b.get('route', '')}`",
        f"- `route_status`: `{m50b.get('route_status', '')}`",
        "",
        "## Watchability",
        f"- `watchability_status`: `{sealed.get('watchability_status', '')}`",
        f"- `candidate_policy_mode`: `{cp.get('candidate_policy_mode', '')}`",
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
            "V15-M51 is a governed live candidate watchability harness so an operator can "
            "observe behavior. It is not benchmark execution, not benchmark pass/fail, not "
            "strength evaluation, not checkpoint promotion, and not the 12-hour run.",
            "",
        ]
    )
    return "\n".join(lines) + "\n"


def _assert_no_path_leak(blob: str) -> None:
    if emission_has_private_path_patterns(blob):
        raise RuntimeError("V15-M51 emission leaked path patterns into public artifacts")


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


def _emit_m51_artifacts(
    sealed: dict[str, Any],
    output_dir: Path,
) -> tuple[dict[str, Any], tuple[Path, ...]]:
    output_dir.mkdir(parents=True, exist_ok=True)
    rep = cast(dict[str, Any], redact_paths_in_value(build_m51_report(sealed)))
    brief = build_m51_brief_md(sealed=sealed)
    p_main = output_dir / FILENAME_MAIN_JSON
    p_rep = output_dir / REPORT_FILENAME
    p_brf = output_dir / BRIEF_FILENAME
    p_main.write_text(canonical_json_dumps(sealed), encoding="utf-8")
    p_rep.write_text(canonical_json_dumps(rep), encoding="utf-8")
    p_brf.write_text(brief, encoding="utf-8")
    blob = canonical_json_dumps(sealed) + canonical_json_dumps(rep) + brief
    _assert_no_path_leak(blob)
    return sealed, (p_main, p_rep, p_brf)


def emit_m51_forbidden_flag_refusal(
    output_dir: Path,
    *,
    emit_profile_short: str,
    triggered_flags: list[str],
) -> tuple[dict[str, Any], tuple[Path, ...]]:
    output_dir.mkdir(parents=True, exist_ok=True)
    primary = refusal_code_from_forbidden_flags(triggered_flags)
    bad = sorted(set(triggered_flags))
    body = _assemble_m51_body(
        watchability_status=STATUS_PREFLIGHT_BLOCKED,
        emit_profile_short=emit_profile_short,
        m50_plain=None,
        m50_digest="",
        refusals=[primary],
        detail_extra=f"forbidden_cli_flags:{','.join(bad)}",
        candidate_policy_mode=CANDIDATE_POLICY_FIXTURE,
        watchability_run=_empty_watchability_run(),
        candidate_identity=_fixture_candidate_identity(),
        candidate_policy_block=_candidate_policy_block(
            mode=CANDIDATE_POLICY_FIXTURE,
            checkpoint_loaded=False,
            torch_load=False,
            adapter=None,
        ),
        operator_observation=_empty_operator_observation(),
        live_sc2_executed=False,
        warnings=(),
    )
    body["forbidden_execution_cli_flags_seen"] = bad
    sealed = seal_m51_body(cast(dict[str, Any], redact_paths_in_value(body)))
    return _emit_m51_artifacts(sealed, output_dir)


def _empty_watchability_run() -> dict[str, Any]:
    return {
        "live_sc2_executed": False,
        "run_mode": "preflight_only",
        "map": None,
        "game_step": None,
        "max_game_steps": None,
        "action_count": None,
        "observation_count": None,
        "replay_saved": False,
        "video_registered": False,
    }


def _fixture_candidate_identity() -> dict[str, Any]:
    return {
        "candidate_id": "fixture_ci_m51",
        "candidate_checkpoint_sha256": None,
        "candidate_source": "fixture",
        "promotion_status": "not_promoted_candidate_only",
    }


def _empty_operator_observation() -> dict[str, Any]:
    return {
        "operator_note_attached": False,
        "observed_behavior_tags": [],
        "stalls_or_failures": [],
    }


def _candidate_policy_block(
    *,
    mode: str,
    checkpoint_loaded: bool,
    torch_load: bool,
    adapter: str | None,
) -> dict[str, Any]:
    return {
        "candidate_policy_mode": mode,
        "checkpoint_loaded": checkpoint_loaded,
        "torch_load_invoked": torch_load,
        "policy_adapter_id": adapter,
    }


def _assemble_m51_body(
    *,
    watchability_status: str,
    emit_profile_short: str,
    m50_plain: dict[str, Any] | None,
    m50_digest: str,
    refusals: list[str],
    detail_extra: str | None,
    candidate_policy_mode: str,
    watchability_run: dict[str, Any],
    candidate_identity: dict[str, Any],
    candidate_policy_block: dict[str, Any],
    operator_observation: dict[str, Any],
    live_sc2_executed: bool,
    warnings: tuple[str, ...],
    run_subdir_note: str | None = None,
) -> dict[str, Any]:
    catalog_id = profile_catalog_id_for_emit(emit_profile_short=emit_profile_short)
    refs = _refs(refusals)
    if detail_extra and refs:
        refs[0] = {**refs[0], "detail": refs[0].get("detail", "") + "|" + detail_extra}
    body: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "contract_id": CONTRACT_ID_M51,
        "profile_id": catalog_id,
        "profile_surface": PROFILE_M51_SURFACE,
        "milestone": MILESTONE_LABEL_M51,
        "emitter_module": EMITTER_MODULE_M51,
        "profile": emit_profile_short,
        "watchability_status": watchability_status,
        "m50_binding": _m50_binding_summary(m50_plain),
        "candidate_identity": candidate_identity,
        "candidate_policy": candidate_policy_block,
        "watchability_run": watchability_run,
        "operator_observation": operator_observation,
        "route_recommendation": _route_next_m52(),
        "refusals": refs,
        "warnings": list(warnings),
        "non_claims": list(NON_CLAIMS_M51),
        **_honesty_m51_block(live_sc2_executed=live_sc2_executed),
    }
    if m50_digest:
        cast(dict[str, Any], body["m50_binding"])["artifact_sha256"] = m50_digest
    if run_subdir_note:
        body["operator_local_subdir"] = run_subdir_note
    return body


def emit_m51_fixture_ci(output_dir: Path) -> tuple[dict[str, Any], tuple[Path, ...]]:
    sub = output_dir / "m50_upstream_fixture"
    emit_m50_fixture_ci(sub)
    m50_path = sub / M50_FILENAME_MAIN_JSON
    return emit_m51_operator_preflight(
        output_dir,
        m50_path=m50_path,
        m50_plain_override=None,
        expected_sha256_lower=None,
        emit_profile_short=PROFILE_FIXTURE_CI,
        require_canonical_seal=True,
        sc2_root=None,
        map_path=None,
        checkpoint_path=None,
        expected_candidate_sha256=None,
        m42_path=None,
    )


def emit_m51_operator_preflight(
    output_dir: Path,
    *,
    m50_path: Path | None,
    m50_plain_override: dict[str, Any] | None = None,
    expected_sha256_lower: str | None,
    emit_profile_short: str,
    require_canonical_seal: bool,
    sc2_root: Path | None,
    map_path: Path | None,
    checkpoint_path: Path | None,
    expected_candidate_sha256: str | None,
    m42_path: Path | None,
) -> tuple[dict[str, Any], tuple[Path, ...]]:
    output_dir.mkdir(parents=True, exist_ok=True)
    m50_plain: dict[str, Any] | None = None
    if m50_plain_override is not None:
        m50_plain = m50_plain_override
    elif m50_path is not None:
        rp = Path(m50_path).resolve()
        if rp.is_file():
            try:
                m50_plain = _parse_json_object(rp)
            except (json.JSONDecodeError, OSError, UnicodeError, ValueError):
                m50_plain = None

    codes, digest = validate_m50_for_m51(
        m50_plain,
        expected_sha256_lower=expected_sha256_lower,
        require_canonical_seal=require_canonical_seal,
    )

    m42_blob: dict[str, Any] | None = None
    if m42_path is not None and Path(m42_path).is_file():
        try:
            m42_blob = _parse_json_object(Path(m42_path).resolve())
        except (json.JSONDecodeError, OSError, UnicodeError, ValueError):
            m42_blob = None

    ck_path = Path(checkpoint_path).resolve() if checkpoint_path is not None else None
    exp_ck = str(expected_candidate_sha256).strip().lower() if expected_candidate_sha256 else None
    cand_id, extra_ref = _candidate_identity_for_preflight(
        checkpoint_path=ck_path,
        expected_ck_sha=exp_ck,
        m42=m42_blob,
    )
    codes = sorted(set(codes + extra_ref))

    warns: list[str] = []
    if sc2_root is not None and not Path(sc2_root).is_dir():
        warns.append("sc2_root_path_not_found_on_preflight_host")
    if map_path is not None and not Path(map_path).is_file():
        warns.append("map_path_not_found_on_preflight_host")

    if codes:
        st = STATUS_PREFLIGHT_BLOCKED
        mode = CANDIDATE_POLICY_UNAVAILABLE
    elif warns:
        st = STATUS_PREFLIGHT_READY_WARNINGS
        mode = CANDIDATE_POLICY_UNAVAILABLE
    else:
        st = STATUS_PREFLIGHT_READY
        mode = CANDIDATE_POLICY_UNAVAILABLE

    if emit_profile_short == PROFILE_FIXTURE_CI and not codes:
        st = STATUS_FIXTURE_SCHEMA_ONLY
        mode = CANDIDATE_POLICY_FIXTURE

    body = _assemble_m51_body(
        watchability_status=st,
        emit_profile_short=emit_profile_short,
        m50_plain=m50_plain,
        m50_digest=digest,
        refusals=codes,
        detail_extra=None,
        candidate_policy_mode=mode,
        watchability_run=_empty_watchability_run(),
        candidate_identity=cand_id,
        candidate_policy_block=_candidate_policy_block(
            mode=mode,
            checkpoint_loaded=False,
            torch_load=False,
            adapter=None,
        ),
        operator_observation=_empty_operator_observation(),
        live_sc2_executed=False,
        warnings=tuple(warns),
    )
    sealed = seal_m51_body(cast(dict[str, Any], redact_paths_in_value(body)))
    return _emit_m51_artifacts(sealed, output_dir)


@dataclass(frozen=True)
class M51LiveRunParams:
    m50_path: Path
    output_dir: Path
    sc2_root: Path
    map_path: Path
    game_step: int
    max_game_steps: int
    save_replay: bool
    allow_scaffold: bool
    seed: int
    video_path: Path | None
    operator_note_path: Path | None
    run_id: str | None
    expected_m50_sha256: str | None
    checkpoint_path: Path | None
    expected_candidate_sha256: str | None
    m42_path: Path | None


def run_m51_operator_local_watchability(
    params: M51LiveRunParams,
    *,
    allow_local: bool,
    authorize_watchability: bool,
) -> tuple[dict[str, Any], tuple[Path, ...]]:
    """Dual-guarded optional live SC2 via BurnySC2 watchability scaffold (not candidate policy)."""

    out = params.output_dir.resolve()
    out.mkdir(parents=True, exist_ok=True)
    watch_sub = out / "watchability_run"
    watch_sub.mkdir(parents=True, exist_ok=True)

    m50_plain: dict[str, Any] | None = None
    if params.m50_path.is_file():
        try:
            m50_plain = _parse_json_object(params.m50_path.resolve())
        except (json.JSONDecodeError, OSError, UnicodeError, ValueError):
            m50_plain = None

    codes, digest = validate_m50_for_m51(
        m50_plain,
        expected_sha256_lower=params.expected_m50_sha256,
        require_canonical_seal=True,
    )

    if not allow_local or not authorize_watchability:
        codes = sorted(set(codes + [REFUSED_OPERATOR_AUTH]))

    m42_blob: dict[str, Any] | None = None
    if params.m42_path is not None and params.m42_path.is_file():
        try:
            m42_blob = _parse_json_object(params.m42_path.resolve())
        except (json.JSONDecodeError, OSError, UnicodeError, ValueError):
            m42_blob = None

    exp_ck = (
        str(params.expected_candidate_sha256).strip().lower()
        if params.expected_candidate_sha256
        else None
    )
    ck_path = params.checkpoint_path.resolve() if params.checkpoint_path is not None else None

    cand_id, extra_ref = _candidate_identity_for_preflight(
        checkpoint_path=ck_path,
        expected_ck_sha=exp_ck,
        m42=m42_blob,
    )

    cand_id.setdefault("candidate_id", "")
    if (
        cand_id.get("candidate_source") == "fixture"
        and not cand_id.get("candidate_checkpoint_sha256")
        and m42_blob is None
        and ck_path is None
    ):
        extra_ref.append(REFUSED_CANDIDATE_IDENTITY)

    codes = sorted(set(codes + extra_ref))

    if not Path(params.sc2_root).is_dir():
        codes.append(REFUSED_SC2_ROOT)
    if not Path(params.map_path).is_file():
        codes.append(REFUSED_MAP_MISSING)

    scaffold_ok = bool(params.allow_scaffold)

    warns: list[str] = []

    watch_run = _empty_watchability_run()
    watch_run.update(
        {
            "run_mode": "operator_local_watchability",
            "map": str(params.map_path.resolve()),
            "game_step": int(params.game_step),
            "max_game_steps": int(params.max_game_steps),
        }
    )
    tags: list[str] = []

    policy_mode = CANDIDATE_POLICY_UNAVAILABLE
    adapter_id = None
    status = STATUS_LIVE_BLOCKED
    torch_load_invoked = False
    chk_loaded = False
    live_sc2_executed = False

    sealed: dict[str, Any]

    if codes:
        body = _assemble_m51_body(
            watchability_status=STATUS_LIVE_BLOCKED,
            emit_profile_short="operator_local_watchability_run",
            m50_plain=m50_plain,
            m50_digest=digest,
            refusals=codes,
            detail_extra=None,
            candidate_policy_mode=policy_mode,
            watchability_run=watch_run,
            candidate_identity=cand_id,
            candidate_policy_block=_candidate_policy_block(
                mode=policy_mode,
                checkpoint_loaded=chk_loaded,
                torch_load=torch_load_invoked,
                adapter=adapter_id,
            ),
            operator_observation=_empty_operator_observation(),
            live_sc2_executed=False,
            warnings=tuple(warns),
            run_subdir_note="watchability_run/",
        )
        body["profile_id"] = PROFILE_ID_OPERATOR_LOCAL_WATCHABILITY
        body["runner_module"] = RUNNER_MODULE_M51
        sealed = seal_m51_body(cast(dict[str, Any], redact_paths_in_value(body)))
        return _emit_m51_artifacts(sealed, out)

    if not scaffold_ok:
        policy_mode = CANDIDATE_POLICY_UNAVAILABLE
        status = STATUS_BLOCKED_MISSING_ADAPTER
        block_codes = [REFUSED_ADAPTER_MISSING]
        body = _assemble_m51_body(
            watchability_status=status,
            emit_profile_short="operator_local_watchability_run",
            m50_plain=m50_plain,
            m50_digest=digest,
            refusals=block_codes,
            detail_extra="real_candidate_adapter_missing_and_scaffold_not_authorized",
            candidate_policy_mode=policy_mode,
            watchability_run=watch_run,
            candidate_identity=cand_id,
            candidate_policy_block=_candidate_policy_block(
                mode=policy_mode,
                checkpoint_loaded=False,
                torch_load=False,
                adapter=None,
            ),
            operator_observation=_empty_operator_observation(),
            live_sc2_executed=False,
            warnings=tuple(warns),
            run_subdir_note="watchability_run/",
        )
        body["profile_id"] = PROFILE_ID_OPERATOR_LOCAL_WATCHABILITY
        body["runner_module"] = RUNNER_MODULE_M51
        sealed = seal_m51_body(cast(dict[str, Any], redact_paths_in_value(body)))
        return _emit_m51_artifacts(sealed, out)

    policy_mode = CANDIDATE_POLICY_SCAFFOLD
    adapter_id = POLICY_ADAPTER_SCAFFOLD_BURNY_M27_STYLE
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
        burnysc2_policy=BURNYSC2_POLICY_V15_M27_NONTRIVIAL_MACRO_SMOKE_V1,
        opponent_mode=BURNYSC2_OPPONENT_MODE_PASSIVE_BOT,
    )
    cfg.validate()

    hres = run_match_execution(cfg, output_dir=watch_sub, hierarchical_sklearn_bundle=None)

    replay_saved = False
    op_note = False
    stalls: list[str] = []

    if not hres.ok or hres.proof is None:
        status = STATUS_LIVE_FAILED
        stalls.append(str(hres.message or "match_harness_failure"))
        live_sc2_executed = True
        body = _assemble_m51_body(
            watchability_status=status,
            emit_profile_short="operator_local_watchability_run",
            m50_plain=m50_plain,
            m50_digest=digest,
            refusals=[REFUSED_LIVE_SC2_RUNTIME],
            detail_extra=str(hres.message or "")[:500],
            candidate_policy_mode=policy_mode,
            watchability_run=watch_run,
            candidate_identity=cand_id,
            candidate_policy_block=_candidate_policy_block(
                mode=policy_mode,
                checkpoint_loaded=False,
                torch_load=False,
                adapter=adapter_id,
            ),
            operator_observation={
                "operator_note_attached": False,
                "observed_behavior_tags": [],
                "stalls_or_failures": stalls,
            },
            live_sc2_executed=live_sc2_executed,
            warnings=tuple(warns),
            run_subdir_note="watchability_run/",
        )
        body["profile_id"] = PROFILE_ID_OPERATOR_LOCAL_WATCHABILITY
        body["runner_module"] = RUNNER_MODULE_M51
        sealed = seal_m51_body(cast(dict[str, Any], redact_paths_in_value(body)))
        return _emit_m51_artifacts(sealed, out)

    proof = hres.proof
    proof_d = proof_record_to_dict(proof)
    (watch_sub / "match_execution_proof.json").write_text(
        canonical_json_dumps(cast(dict[str, Any], redact_paths_in_value(proof_d))),
        encoding="utf-8",
    )

    live_sc2_executed = True
    watch_run["live_sc2_executed"] = True
    watch_run["action_count"] = int(proof.action_count)
    watch_run["observation_count"] = len(proof.observation_summaries)
    if proof.replay is not None:
        replay_saved = bool(proof.replay.replay_saved)
    watch_run["replay_saved"] = replay_saved

    tags = behavior_tags_from_proof_dict(proof_d)

    if params.video_path is not None and Path(params.video_path).is_file():
        watch_run["video_registered"] = True
        vp = Path(params.video_path).resolve()
        vm = {
            "path_logical": "operator_supplied",
            "sha256": sha256_hex_file_optional(vp),
            "size_bytes": int(vp.stat().st_size),
        }
        (watch_sub / "video_manifest.json").write_text(
            canonical_json_dumps(vm),
            encoding="utf-8",
        )

    if params.operator_note_path is not None and Path(params.operator_note_path).is_file():
        op_note = True
        txt = Path(params.operator_note_path).read_text(encoding="utf-8", errors="replace")
        (watch_sub / "operator_watch_note.md").write_text(txt, encoding="utf-8")

    if warns:
        status = STATUS_LIVE_COMPLETED_WARNINGS
    else:
        status = STATUS_SCAFFOLD_COMPLETED

    body = _assemble_m51_body(
        watchability_status=status,
        emit_profile_short="operator_local_watchability_run",
        m50_plain=m50_plain,
        m50_digest=digest,
        refusals=[],
        detail_extra=None,
        candidate_policy_mode=policy_mode,
        watchability_run=watch_run,
        candidate_identity=cand_id,
        candidate_policy_block=_candidate_policy_block(
            mode=policy_mode,
            checkpoint_loaded=False,
            torch_load=False,
            adapter=adapter_id,
        ),
        operator_observation={
            "operator_note_attached": op_note,
            "observed_behavior_tags": tags,
            "stalls_or_failures": stalls,
        },
        live_sc2_executed=live_sc2_executed,
        warnings=tuple(warns),
        run_subdir_note="watchability_run/",
    )
    body["profile_id"] = PROFILE_ID_OPERATOR_LOCAL_WATCHABILITY
    body["runner_module"] = RUNNER_MODULE_M51
    if params.run_id:
        body["run_id"] = str(params.run_id)
    sealed = seal_m51_body(cast(dict[str, Any], redact_paths_in_value(body)))
    _emit_m51_artifacts(sealed, out)

    replay_dir = watch_sub / "replay"
    replay_dir.mkdir(parents=True, exist_ok=True)
    if replay_saved:
        rp = replay_dir / "validation.SC2Replay"
        alt = watch_sub / "validation.SC2Replay"
        if alt.is_file() and not rp.is_file():
            rp.write_bytes(alt.read_bytes())

    return sealed, (
        out / FILENAME_MAIN_JSON,
        out / REPORT_FILENAME,
        out / BRIEF_FILENAME,
    )


def emit_m51_operator_declared(
    output_dir: Path,
    *,
    declared_path: Path,
    embedded_m50_path: Path | None,
    sc2_root: Path | None,
    map_path: Path | None,
    checkpoint_path: Path | None,
    expected_candidate_sha256: str | None,
    m42_path: Path | None,
) -> tuple[dict[str, Any], tuple[Path, ...]]:
    """Operator-declared envelope with embedded sealed M50 dict (or sibling file)."""

    rp = Path(declared_path).resolve()
    raw_in = json.loads(rp.read_text(encoding="utf-8"))
    if not isinstance(raw_in, dict):
        raise ValueError("declared envelope must be a JSON object")
    declared = cast(dict[str, Any], redact_paths_in_value(raw_in))

    cid = str(declared.get("contract_id") or "")
    pid = str(declared.get("profile_id") or "")
    surface_ok = cid == CONTRACT_ID_M51 and pid in (
        PROFILE_M51_SURFACE,
        PROFILE_ID_OPERATOR_DECLARED,
    )

    violations = [k for k in M51_DECLARED_OVERCLAIM_KEYS if declared.get(k) is True]

    m50_plain: dict[str, Any] | None = None
    sm50 = declared.get("sealed_m50")
    if isinstance(sm50, dict):
        m50_plain = sm50
    elif embedded_m50_path is not None and Path(embedded_m50_path).is_file():
        try:
            m50_plain = _parse_json_object(Path(embedded_m50_path).resolve())
        except (json.JSONDecodeError, OSError, UnicodeError, ValueError):
            m50_plain = None

    exp_field = declared.get("expected_m50_readout_sha256")
    exp_decl = (
        str(exp_field).strip().lower() if isinstance(exp_field, str) and exp_field.strip() else None
    )

    if not surface_ok or violations:
        codes = [REFUSED_INVALID_DECLARED_M51]
        body = _assemble_m51_body(
            watchability_status=STATUS_PREFLIGHT_BLOCKED,
            emit_profile_short=PROFILE_OPERATOR_DECLARED,
            m50_plain=None,
            m50_digest="",
            refusals=codes,
            detail_extra=(
                "overclaim:" + ",".join(violations) if violations else "contract_profile_bad"
            ),
            candidate_policy_mode=CANDIDATE_POLICY_UNAVAILABLE,
            watchability_run=_empty_watchability_run(),
            candidate_identity=_fixture_candidate_identity(),
            candidate_policy_block=_candidate_policy_block(
                mode=CANDIDATE_POLICY_UNAVAILABLE,
                checkpoint_loaded=False,
                torch_load=False,
                adapter=None,
            ),
            operator_observation=_empty_operator_observation(),
            live_sc2_executed=False,
            warnings=(),
        )
        sealed = seal_m51_body(cast(dict[str, Any], redact_paths_in_value(body)))
        return _emit_m51_artifacts(sealed, output_dir.resolve())

    if m50_plain is None:
        body = _assemble_m51_body(
            watchability_status=STATUS_PREFLIGHT_BLOCKED,
            emit_profile_short=PROFILE_OPERATOR_DECLARED,
            m50_plain=None,
            m50_digest="",
            refusals=[REFUSED_MISSING_M50],
            detail_extra="sealed_m50_missing",
            candidate_policy_mode=CANDIDATE_POLICY_UNAVAILABLE,
            watchability_run=_empty_watchability_run(),
            candidate_identity=_fixture_candidate_identity(),
            candidate_policy_block=_candidate_policy_block(
                mode=CANDIDATE_POLICY_UNAVAILABLE,
                checkpoint_loaded=False,
                torch_load=False,
                adapter=None,
            ),
            operator_observation=_empty_operator_observation(),
            live_sc2_executed=False,
            warnings=(),
        )
        sealed = seal_m51_body(cast(dict[str, Any], redact_paths_in_value(body)))
        return _emit_m51_artifacts(sealed, output_dir.resolve())

    return emit_m51_operator_preflight(
        output_dir.resolve(),
        m50_path=None,
        m50_plain_override=m50_plain,
        expected_sha256_lower=exp_decl,
        emit_profile_short=PROFILE_OPERATOR_DECLARED,
        require_canonical_seal=False,
        sc2_root=sc2_root,
        map_path=map_path,
        checkpoint_path=checkpoint_path,
        expected_candidate_sha256=expected_candidate_sha256,
        m42_path=m42_path,
    )


def proof_record_to_dict(proof: ExecutionProofRecord) -> dict[str, Any]:
    d = dict(proof_record_to_hash_input_dict(proof))
    d["artifact_hash"] = compute_artifact_hash(proof)
    return d
