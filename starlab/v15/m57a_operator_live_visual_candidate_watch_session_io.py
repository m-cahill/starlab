"""V15-M57A — operator live visual watch session builders and writers."""

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
from starlab.v15.m51_live_candidate_watchability_harness_models import CONTRACT_ID_M51
from starlab.v15.m52_candidate_live_adapter_spike_models import (
    ADAPTER_SPIKE_LABEL,
    CONTRACT_ID_M52A,
    REFUSED_LIVE_SC2_RUNTIME,
    STATUS_PREFLIGHT_READY,
    STATUS_PREFLIGHT_READY_WARNINGS,
    STATUS_SPIKE_BLOCKED,
    STATUS_SPIKE_COMPLETED,
    STATUS_SPIKE_FAILED,
)
from starlab.v15.m56_bounded_evaluation_package_readout_decision_models import (
    CONTRACT_ID as CONTRACT_ID_M56,
)
from starlab.v15.m56a_latest_candidate_visual_watchability_confirmation_io import (
    _validate_m53_file,
    _validate_m54_file,
    sha256_file_hex,
    validate_sha256,
)
from starlab.v15.m57a_operator_live_visual_candidate_watch_session_models import (
    ADAPTER_AVAILABLE,
    ADAPTER_BLOCKED,
    ADAPTER_LOADED,
    ADAPTER_MISSING,
    ADAPTER_NOT_USED,
    CANONICAL_CANDIDATE_CHECKPOINT_SHA256,
    CANONICAL_M53_RUN_ARTIFACT_SHA256,
    CANONICAL_M54_PACKAGE_SHA256,
    CHECKLIST_FILENAME,
    CLASSIFICATION_ADAPTER_LOADED_SC2_BLOCKED,
    CLASSIFICATION_BLOCKED_MISSING_ADAPTER,
    CLASSIFICATION_CANDIDATE_LIVE_COMPLETED,
    CLASSIFICATION_FIXTURE,
    CLASSIFICATION_PREFLIGHT_BLOCKED,
    CLASSIFICATION_SCAFFOLD,
    CONTRACT_ID,
    DEFAULT_CLAIM_FLAGS,
    EMITTER_MODULE,
    FILENAME_MAIN_JSON,
    GATE_ARTIFACT_DIGEST_FIELD,
    MILESTONE,
    NON_CLAIMS,
    POLICY_BLOCKED,
    POLICY_CANDIDATE_LIVE_ADAPTER,
    POLICY_FIXTURE,
    POLICY_SCAFFOLD,
    PROFILE_M57A,
    RECOMMENDED_NEXT_MILESTONE,
    REPORT_CONTRACT_ID,
    REPORT_FILENAME,
    ROUTE_M57,
    ROUTE_STATUS_RECOMMENDED_NOT_EXECUTED,
    SCHEMA_VERSION,
    STATUS_FIXTURE_ONLY,
    STATUS_PREFLIGHT_BLOCKED,
    STATUS_PREFLIGHT_READY_ADAPTER,
    STATUS_PREFLIGHT_READY_SCAFFOLD,
    STRONGEST_ALLOWED_DEFAULT,
    WARNING_M56_READOUT_ABSENT,
    WARNING_M56A_ABSENT,
)

_DIGEST_FIELD = GATE_ARTIFACT_DIGEST_FIELD
_PATH_OUT_SEGMENT: Final[re.Pattern[str]] = re.compile(
    r"(?:^|[\\/])out(?:[\\/]|$)|[\\/]out[\\/]",
    re.IGNORECASE,
)


def seal_m57a_body(body: dict[str, Any]) -> dict[str, Any]:
    wo = {k: v for k, v in body.items() if k != _DIGEST_FIELD}
    digest = sha256_hex_of_canonical_json(wo)
    sealed = dict(wo)
    sealed[_DIGEST_FIELD] = digest
    return sealed


def _parse_json_object(path: Path) -> dict[str, Any]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ValueError("JSON root must be an object")
    return raw


def _seal_ok(obj: dict[str, Any], *, digest_field: str = _DIGEST_FIELD) -> bool:
    seal_in = obj.get(digest_field)
    if seal_in is None:
        return False
    wo = {k: v for k, v in obj.items() if k != digest_field}
    computed = sha256_hex_of_canonical_json(wo)
    return str(seal_in).lower() == computed.lower()


def _claim_template() -> dict[str, bool]:
    return dict(DEFAULT_CLAIM_FLAGS)


def _has_illegal_true_claim(obj: Any, *, disallowed_keys: frozenset[str]) -> bool:
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k == "claim_flags" and isinstance(v, dict):
                for ck, cv in v.items():
                    if ck in disallowed_keys and cv is True:
                        if ck in ("visual_watch_session_attempted", "live_sc2_executed"):
                            continue
                        return True
            elif k in disallowed_keys and v is True:
                if k in ("visual_watch_session_attempted", "live_sc2_executed"):
                    continue
                return True
            elif _has_illegal_true_claim(v, disallowed_keys=disallowed_keys):
                return True
    elif isinstance(obj, list):
        for item in obj:
            if _has_illegal_true_claim(item, disallowed_keys=disallowed_keys):
                return True
    return False


DISALLOWED_TRUE_CLAIMS: Final[frozenset[str]] = frozenset(
    k
    for k in DEFAULT_CLAIM_FLAGS
    if k
    not in (
        "visual_watch_session_attempted",
        "live_sc2_executed",
        "candidate_policy_control_confirmed",
        "scaffold_policy_used",
    )
)


def _boundary_violation_reason(raw_text: str) -> str | None:
    low = raw_text.lower()
    if "company_secrets" in low:
        return "blocked_private_boundary_violation"
    if _PATH_OUT_SEGMENT.search(raw_text):
        return "blocked_private_boundary_violation"
    if emission_has_private_path_patterns(raw_text):
        return "blocked_private_boundary_violation"
    return None


def _route_block() -> dict[str, Any]:
    return {
        "route": ROUTE_M57,
        "route_status": ROUTE_STATUS_RECOMMENDED_NOT_EXECUTED,
        "recommended_next_milestone": RECOMMENDED_NEXT_MILESTONE,
        "route_note": "Future evaluation remains separately chartered.",
    }


def build_fixture_watch_session() -> dict[str, Any]:
    return {
        "contract_id": CONTRACT_ID,
        "profile_id": PROFILE_M57A,
        "milestone": MILESTONE,
        "emitter_module": EMITTER_MODULE,
        "schema_version": SCHEMA_VERSION,
        "input_bindings": {
            "m56_readout_artifact_sha256": None,
            "m55_preflight_artifact_sha256": None,
            "m54_package_sha256": CANONICAL_M54_PACKAGE_SHA256,
            "m53_run_artifact_sha256": CANONICAL_M53_RUN_ARTIFACT_SHA256,
            "candidate_checkpoint_sha256": CANONICAL_CANDIDATE_CHECKPOINT_SHA256,
            "candidate_checkpoint_path_reference": None,
            "m51_watchability_json_sha256": None,
            "m52a_adapter_json_sha256": None,
            "m56a_context_sha256": None,
        },
        "watch_session": {
            "session_status": STATUS_FIXTURE_ONLY,
            "policy_source": POLICY_FIXTURE,
            "candidate_policy_adapter_status": ADAPTER_NOT_USED,
            "live_sc2_invoked": False,
            "torch_load_invoked_for_watchability_adapter": False,
            "checkpoint_blob_loaded_for_watchability_adapter": False,
            "replay_saved": False,
            "video_metadata_supplied": False,
            "operator_visual_observation_supplied": False,
            "map": None,
            "opponent_mode": None,
            "game_steps_observed": None,
            "action_count": None,
            "duration_seconds": None,
            "sc2_result": None,
        },
        "visual_classification": {
            "classification": CLASSIFICATION_FIXTURE,
            "classification_reason": "CI fixture schema only; no live SC2.",
            "is_candidate_policy_control_confirmed": False,
            "is_scaffold_policy": False,
            "is_benchmark_evidence": False,
        },
        "artifact_references": {
            "replay_file_reference": None,
            "replay_sha256": None,
            "video_metadata_reference": None,
            "operator_notes_reference": None,
            "watch_session_raw_receipt_sha256": None,
        },
        "claim_flags": _claim_template(),
        "non_claims": list(NON_CLAIMS),
        "route_recommendation": _route_block(),
    }


def build_watch_session_report(sealed: dict[str, Any]) -> dict[str, Any]:
    vc = sealed.get("visual_classification") or {}
    ws = sealed.get("watch_session") or {}
    cf = sealed.get("claim_flags") or {}
    summary_bits = [
        str(MILESTONE),
        str(ws.get("session_status") or ""),
        str(vc.get("classification") or ""),
    ]
    warnings: list[str] = []
    if sealed.get("_preflight_warnings"):
        warnings.extend([str(x) for x in (sealed.get("_preflight_warnings") or [])])
    strongest = STRONGEST_ALLOWED_DEFAULT
    if vc.get("classification") == CLASSIFICATION_SCAFFOLD:
        strongest = (
            "Scaffold watchability session recorded; this does not prove the trained candidate "
            "policy controlled gameplay."
        )
    if vc.get("classification") == CLASSIFICATION_CANDIDATE_LIVE_COMPLETED:
        strongest = (
            "Governed M52A candidate-live adapter spike completed with live SC2; watchability "
            "evidence only — not benchmark execution."
        )
    blocked: list[str] = []
    if vc.get("classification") == CLASSIFICATION_PREFLIGHT_BLOCKED:
        blocked.append(str(vc.get("classification_reason") or "preflight_blocked"))
    return {
        "contract_id": REPORT_CONTRACT_ID,
        "milestone": MILESTONE,
        "session_status": str(ws.get("session_status") or ""),
        "classification": str(vc.get("classification") or ""),
        "summary": " / ".join(summary_bits),
        "strongest_allowed_claim": strongest,
        "warnings": warnings,
        "blocked_reasons": blocked,
        "non_claims": list(NON_CLAIMS),
        "next_recommended_step": "V15-M57 — Governed Evaluation Execution Charter / Dry-Run Gate",
        "claim_flags_summary": {k: bool(cf.get(k)) for k in sorted(DEFAULT_CLAIM_FLAGS)},
    }


def build_watch_session_checklist(sealed: dict[str, Any]) -> str:
    ws = sealed.get("watch_session") or {}
    ib = sealed.get("input_bindings") or {}
    cf = sealed.get("claim_flags") or {}
    lines = [
        f"# {MILESTONE} checklist",
        "",
        "- [ ] **W0** — M56 readout context present or explicitly absent",
        f"      - m56_readout_artifact_sha256: `{ib.get('m56_readout_artifact_sha256')}`",
        "- [ ] **W1** — M54 package anchor matches canonical SHA",
        f"      - expected `{CANONICAL_M54_PACKAGE_SHA256}` vs `{ib.get('m54_package_sha256')}`",
        "- [ ] **W2** — M53 run artifact anchor matches canonical SHA",
        "      - expected "
        f"`{CANONICAL_M53_RUN_ARTIFACT_SHA256}` vs `{ib.get('m53_run_artifact_sha256')}`",
        "- [ ] **W3** — Latest candidate checkpoint SHA matches expected value",
        f"      - `{ib.get('candidate_checkpoint_sha256')}`",
        "- [ ] **W4** — Candidate checkpoint path, if supplied, hashes to expected SHA",
        "- [ ] **W5** — Candidate-live adapter availability classified",
        f"      - `{ws.get('candidate_policy_adapter_status')}`",
        "- [ ] **W6** — Scaffold fallback explicitly authorized if used",
        "- [ ] **W7** — Live SC2 invocation status recorded",
        f"      - live_sc2_invoked={ws.get('live_sc2_invoked')}",
        "- [ ] **W8** — Replay/video/operator notes references are local-only",
        "- [ ] **W9** — Candidate-policy vs scaffold-policy distinction preserved",
        "- [ ] **W10** — Benchmark/pass/promotion/strength claims remain false",
        "- [ ] **W11** — Route recommendation remains recommended_not_executed",
        "",
        "## Claim flags (must stay false for disallowed claims)",
        "",
    ]
    for k in sorted(DEFAULT_CLAIM_FLAGS):
        lines.append(f"- `{k}`: {cf.get(k)}")
    lines.append("")
    return "\n".join(lines)


def write_watch_session_artifacts(
    output_dir: Path,
    *,
    body_unsealed: dict[str, Any],
) -> tuple[dict[str, Any], tuple[Path, Path, Path]]:
    output_dir.mkdir(parents=True, exist_ok=True)
    clean = dict(body_unsealed)
    clean.pop("_preflight_warnings", None)
    sealed = seal_m57a_body(cast(dict[str, Any], redact_paths_in_value(clean)))
    rep = build_watch_session_report(
        {**sealed, "_preflight_warnings": body_unsealed.get("_preflight_warnings")}
    )
    chk = build_watch_session_checklist(sealed)
    p_main = output_dir / FILENAME_MAIN_JSON
    p_rep = output_dir / REPORT_FILENAME
    p_chk = output_dir / CHECKLIST_FILENAME
    p_main.write_text(canonical_json_dumps(sealed), encoding="utf-8")
    p_rep.write_text(
        canonical_json_dumps(cast(dict[str, Any], redact_paths_in_value(rep))), encoding="utf-8"
    )
    p_chk.write_text(chk, encoding="utf-8")
    blob = canonical_json_dumps(sealed) + canonical_json_dumps(rep) + chk
    if emission_has_private_path_patterns(blob):
        raise ValueError("emission_blocked_private_boundary_violation")
    return sealed, (p_main, p_rep, p_chk)


def emit_forbidden_refusal(output_dir: Path, *, flags: list[str]) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    body = build_fixture_watch_session()
    body["watch_session"]["session_status"] = STATUS_PREFLIGHT_BLOCKED
    body["visual_classification"]["classification"] = CLASSIFICATION_PREFLIGHT_BLOCKED
    body["visual_classification"]["classification_reason"] = "Forbidden CLI flags: " + ", ".join(
        sorted(set(flags))
    )
    write_watch_session_artifacts(output_dir, body_unsealed=body)


def _optional_sha256_path(path: Path | None) -> str | None:
    if path is None:
        return None
    rp = path.resolve()
    if not rp.is_file():
        return None
    return sha256_file_hex(rp)


def _load_m56_readout(path: Path | None) -> tuple[str | None, str | None]:
    if path is None:
        return None, None
    rp = path.resolve()
    if not rp.is_file():
        return None, "m56_readout_file_missing"
    txt = rp.read_text(encoding="utf-8")
    br = _boundary_violation_reason(txt)
    if br:
        return None, br
    try:
        raw = _parse_json_object(rp)
    except (json.JSONDecodeError, OSError, UnicodeError, ValueError):
        return None, "m56_readout_invalid_json"
    if str(raw.get("contract_id") or "") != CONTRACT_ID_M56:
        return None, "m56_readout_contract_mismatch"
    if not _seal_ok(raw):
        return None, "m56_readout_seal_invalid"
    return str(raw.get(_DIGEST_FIELD) or "").strip().lower(), None


@dataclass(frozen=True)
class PreflightInputs:
    m56_readout_json: Path | None
    m55_preflight_json: Path | None
    m54_package_json: Path | None
    m53_run_json: Path | None
    m51_watchability_json: Path | None
    m52a_adapter_json: Path | None
    m56a_context_json: Path | None
    candidate_checkpoint: Path | None
    expected_package_sha256: str
    expected_candidate_sha256: str


def _m52a_preflight_hint(path: Path | None) -> tuple[str | None, str | None]:
    if path is None:
        return None, None
    rp = path.resolve()
    if not rp.is_file():
        return None, None
    try:
        raw = _parse_json_object(rp)
    except (json.JSONDecodeError, OSError, UnicodeError, ValueError):
        return None, "m52a_json_unreadable"
    if str(raw.get("contract_id") or "") != CONTRACT_ID_M52A:
        return None, "m52a_contract_mismatch"
    digest = str(raw.get(_DIGEST_FIELD) or "").strip().lower()
    st = str(raw.get("adapter_status") or "")
    if st in (
        STATUS_PREFLIGHT_READY,
        STATUS_PREFLIGHT_READY_WARNINGS,
        STATUS_SPIKE_COMPLETED,
    ):
        return digest, None
    if st == STATUS_PREFLIGHT_BLOCKED:
        return digest, "m52a_preflight_blocked"
    return digest, None


def _m51_hint(path: Path | None) -> tuple[str | None, str | None]:
    if path is None:
        return None, None
    rp = path.resolve()
    if not rp.is_file():
        return None, None
    try:
        raw = _parse_json_object(rp)
    except (json.JSONDecodeError, OSError, UnicodeError, ValueError):
        return None, "m51_json_unreadable"
    if str(raw.get("contract_id") or "") != CONTRACT_ID_M51:
        return None, "m51_contract_mismatch"
    digest = str(raw.get(_DIGEST_FIELD) or "").strip().lower()
    return digest, None


def build_operator_preflight_watch_session(inp: PreflightInputs) -> dict[str, Any]:
    warnings: list[str] = []
    blocked: list[str] = []

    exp54 = str(inp.expected_package_sha256).strip().lower()
    exp_ck = str(inp.expected_candidate_sha256).strip().lower()
    if validate_sha256(exp54) is None or validate_sha256(exp_ck) is None:
        return _preflight_blocked_body(blocked + ["invalid_expected_sha"], warnings)

    if exp54 != CANONICAL_M54_PACKAGE_SHA256 or exp_ck != CANONICAL_CANDIDATE_CHECKPOINT_SHA256:
        return _preflight_blocked_body(blocked + ["canonical_anchor_mismatch"], warnings)

    m56_d, m56_err = _load_m56_readout(inp.m56_readout_json)
    if m56_err:
        blocked.append(m56_err)
    if inp.m56_readout_json is None:
        warnings.append(WARNING_M56_READOUT_ABSENT)

    m55_d = _optional_sha256_path(inp.m55_preflight_json)
    m54_d: str | None = None
    m53_d: str | None = None
    if inp.m54_package_json is not None:
        try:
            m54 = _validate_m54_file(inp.m54_package_json.resolve(), expected_sha=exp54)
            m54_d = str(m54.get(_DIGEST_FIELD) or "").lower()
        except ValueError as e:
            blocked.append(str(e))

    if inp.m53_run_json is not None:
        try:
            m53 = _validate_m53_file(
                inp.m53_run_json.resolve(),
                expected_sha=CANONICAL_M53_RUN_ARTIFACT_SHA256,
            )
            m53_d = str(m53.get(_DIGEST_FIELD) or "").lower()
        except ValueError as e:
            blocked.append(str(e))

    ck_path_ref: str | None = None
    if inp.candidate_checkpoint is not None and inp.candidate_checkpoint.is_file():
        got = sha256_file_hex(inp.candidate_checkpoint.resolve())
        if got != exp_ck:
            blocked.append("blocked_candidate_checkpoint_sha_mismatch")
        ck_path_ref = "operator_supplied_checkpoint_path"

    m52a_digest, m52a_err = _m52a_preflight_hint(inp.m52a_adapter_json)
    if m52a_err:
        blocked.append(m52a_err)
    m51_digest, m51_err = _m51_hint(inp.m51_watchability_json)
    if m51_err:
        blocked.append(m51_err)

    m56a_d = _optional_sha256_path(inp.m56a_context_json)
    if inp.m56a_context_json is None:
        warnings.append(WARNING_M56A_ABSENT)

    if blocked:
        return _preflight_blocked_body(sorted(set(blocked)), warnings)

    adapter_ready = m52a_digest is not None and m52a_err is None
    scaffold_ready = m51_digest is not None and m51_err is None

    if adapter_ready:
        sess = STATUS_PREFLIGHT_READY_ADAPTER
        adapter_st = ADAPTER_AVAILABLE
        classification = CLASSIFICATION_BLOCKED_MISSING_ADAPTER
        reason = (
            "Preflight: sealed M52A JSON indicates a governable candidate-live delegate path; "
            "live watch not executed in preflight-only profile."
        )
    elif scaffold_ready:
        sess = STATUS_PREFLIGHT_READY_SCAFFOLD
        adapter_st = ADAPTER_MISSING
        classification = CLASSIFICATION_BLOCKED_MISSING_ADAPTER
        reason = (
            "Preflight: M51 watchability JSON present for scaffold-only path; "
            "candidate-live adapter not indicated from supplied M52A JSON; live watch not executed."
        )
    else:
        sess = STATUS_PREFLIGHT_BLOCKED
        adapter_st = ADAPTER_MISSING
        classification = CLASSIFICATION_BLOCKED_MISSING_ADAPTER
        reason = (
            "Preflight: neither a usable M52A nor M51 watchability JSON path was supplied; "
            "candidate-live visual watch would be blocked without further inputs."
        )

    body = build_fixture_watch_session()
    body["input_bindings"].update(
        {
            "m56_readout_artifact_sha256": m56_d,
            "m55_preflight_artifact_sha256": m55_d,
            "m54_package_sha256": m54_d or CANONICAL_M54_PACKAGE_SHA256,
            "m53_run_artifact_sha256": m53_d or CANONICAL_M53_RUN_ARTIFACT_SHA256,
            "candidate_checkpoint_sha256": exp_ck,
            "candidate_checkpoint_path_reference": ck_path_ref,
            "m51_watchability_json_sha256": m51_digest,
            "m52a_adapter_json_sha256": m52a_digest,
            "m56a_context_sha256": m56a_d,
        },
    )
    body["watch_session"]["session_status"] = sess
    body["watch_session"]["policy_source"] = POLICY_BLOCKED
    body["watch_session"]["candidate_policy_adapter_status"] = adapter_st
    body["visual_classification"]["classification"] = classification
    body["visual_classification"]["classification_reason"] = reason
    body["_preflight_warnings"] = warnings
    return body


def _preflight_blocked_body(blocked: list[str], warnings: list[str]) -> dict[str, Any]:
    body = build_fixture_watch_session()
    body["watch_session"]["session_status"] = STATUS_PREFLIGHT_BLOCKED
    body["watch_session"]["policy_source"] = POLICY_BLOCKED
    body["watch_session"]["candidate_policy_adapter_status"] = ADAPTER_BLOCKED
    body["visual_classification"]["classification"] = CLASSIFICATION_PREFLIGHT_BLOCKED
    body["visual_classification"]["classification_reason"] = "; ".join(sorted(set(blocked)))
    body["_preflight_warnings"] = warnings
    return body


@dataclass(frozen=True)
class DeclaredInputs:
    declared_path: Path
    expected_candidate_sha256: str


def build_operator_declared_watch_session(inp: DeclaredInputs) -> dict[str, Any]:
    warnings: list[str] = []
    rp = inp.declared_path.resolve()
    if not rp.is_file():
        return _preflight_blocked_body(["declared_watch_session_file_missing"], warnings)
    txt = rp.read_text(encoding="utf-8")
    br = _boundary_violation_reason(txt)
    if br:
        return _preflight_blocked_body([br], warnings)
    try:
        raw = _parse_json_object(rp)
    except (json.JSONDecodeError, OSError, UnicodeError, ValueError):
        return _preflight_blocked_body(["declared_json_invalid"], warnings)
    if str(raw.get("contract_id") or "") != CONTRACT_ID:
        return _preflight_blocked_body(["declared_contract_id_mismatch"], warnings)
    exp = str(inp.expected_candidate_sha256).strip().lower()
    if validate_sha256(exp) is None or exp != CANONICAL_CANDIDATE_CHECKPOINT_SHA256:
        return _preflight_blocked_body(["expected_candidate_sha_mismatch"], warnings)
    ib = raw.get("input_bindings") or {}
    got_ck = ""
    if isinstance(ib, dict):
        got_ck = str(ib.get("candidate_checkpoint_sha256") or "").strip().lower()
    if got_ck != exp:
        return _preflight_blocked_body(["declared_candidate_sha_binding_mismatch"], warnings)
    if _has_illegal_true_claim(raw, disallowed_keys=DISALLOWED_TRUE_CLAIMS):
        return _preflight_blocked_body(["declared_overclaim_in_evidence"], warnings)
    declared_flags = raw.get("claim_flags")
    if isinstance(declared_flags, dict):
        for k, v in DEFAULT_CLAIM_FLAGS.items():
            if k in declared_flags and declared_flags[k] is True and k in DISALLOWED_TRUE_CLAIMS:
                return _preflight_blocked_body(["declared_disallowed_claim_flag_true"], warnings)
    policy = str(
        (raw.get("watch_session") or {}).get("policy_source")
        if isinstance(raw.get("watch_session"), dict)
        else "",
    )
    confirmed = bool(
        (raw.get("visual_classification") or {}).get("is_candidate_policy_control_confirmed")
        if isinstance(raw.get("visual_classification"), dict)
        else False,
    )
    if confirmed and policy != POLICY_CANDIDATE_LIVE_ADAPTER:
        return _preflight_blocked_body(
            ["candidate_policy_control_requires_candidate_live_adapter_policy_source"],
            warnings,
        )
    base = build_fixture_watch_session()
    merged = {**base, **{k: v for k, v in raw.items() if k != _DIGEST_FIELD}}
    merged["profile_id"] = PROFILE_M57A
    merged["emitter_module"] = EMITTER_MODULE
    merged["_preflight_warnings"] = warnings
    merged.setdefault("claim_flags", _claim_template())
    for k, v in _claim_template().items():
        merged["claim_flags"].setdefault(k, v)
    return merged


def build_runner_blocked_watch_session(
    *,
    reason: str,
    policy_source: str = POLICY_BLOCKED,
    classification: str = CLASSIFICATION_BLOCKED_MISSING_ADAPTER,
) -> dict[str, Any]:
    body = build_fixture_watch_session()
    body["watch_session"]["session_status"] = STATUS_PREFLIGHT_BLOCKED
    body["watch_session"]["policy_source"] = policy_source
    body["watch_session"]["candidate_policy_adapter_status"] = ADAPTER_MISSING
    body["visual_classification"]["classification"] = classification
    body["visual_classification"]["classification_reason"] = reason
    body["claim_flags"]["visual_watch_session_attempted"] = True
    return body


def session_body_from_m52a_delegate(
    m52_sealed: dict[str, Any],
    *,
    m57_output_dir: Path,
) -> dict[str, Any]:
    """Map sealed M52A primary JSON into M57A watch session fields (post delegate)."""

    adapter_st = str(m52_sealed.get("adapter_status") or "")
    adapter_kind = str(m52_sealed.get("adapter_kind") or "")
    live = bool(m52_sealed.get("live_sc2_executed"))
    torch_on = bool(m52_sealed.get("torch_load_invoked"))
    ck_blob = bool(m52_sealed.get("checkpoint_blob_loaded"))

    wr = m52_sealed.get("watchability_run") or {}
    replay_saved = bool(wr.get("replay_saved"))
    action_count = wr.get("action_count")
    game_steps = wr.get("observation_count")
    refusals = m52_sealed.get("refusals") or []

    replay_rel: str | None = None
    replay_sha: str | None = None
    if replay_saved:
        rpath = (
            m57_output_dir.resolve()
            / "m52a_delegate"
            / "candidate_live_adapter_watch"
            / "replay"
            / "validation.SC2Replay"
        )
        replay_rel = "m52a_delegate/candidate_live_adapter_watch/replay/validation.SC2Replay"
        if rpath.is_file():
            replay_sha = sha256_file_hex(rpath)

    classification = CLASSIFICATION_BLOCKED_MISSING_ADAPTER
    reason = "M52A delegate did not complete a governed candidate-live watch session."
    policy_src = POLICY_BLOCKED
    adapter_label = ADAPTER_MISSING
    session_status = CLASSIFICATION_BLOCKED_MISSING_ADAPTER
    sc2_result: str | None = None
    confirmed = False
    scaffold_used = False

    if adapter_st == STATUS_SPIKE_COMPLETED and live and adapter_kind == ADAPTER_SPIKE_LABEL:
        classification = CLASSIFICATION_CANDIDATE_LIVE_COMPLETED
        reason = "M52A candidate-live adapter spike completed with live SC2 (watchability only)."
        policy_src = POLICY_CANDIDATE_LIVE_ADAPTER
        adapter_label = ADAPTER_LOADED if ck_blob else ADAPTER_AVAILABLE
        session_status = CLASSIFICATION_CANDIDATE_LIVE_COMPLETED
        confirmed = True
        sc2_result = "completed"
    elif (
        adapter_st == STATUS_SPIKE_FAILED
        and torch_on
        and ck_blob
        and any(
            isinstance(r, dict) and str(r.get("code") or "") == REFUSED_LIVE_SC2_RUNTIME
            for r in (refusals if isinstance(refusals, list) else [])
        )
    ):
        classification = CLASSIFICATION_ADAPTER_LOADED_SC2_BLOCKED
        reason = (
            "Checkpoint loaded for M52A delegate but live SC2 harness failed (watchability only)."
        )
        policy_src = POLICY_CANDIDATE_LIVE_ADAPTER
        adapter_label = ADAPTER_LOADED
        session_status = CLASSIFICATION_ADAPTER_LOADED_SC2_BLOCKED
        sc2_result = "live_runtime_error"
    elif adapter_st == STATUS_SPIKE_BLOCKED:
        classification = CLASSIFICATION_BLOCKED_MISSING_ADAPTER
        reason = "M52A delegate blocked; candidate-live visual watch not completed."
        policy_src = POLICY_BLOCKED
        adapter_label = ADAPTER_BLOCKED
        session_status = CLASSIFICATION_BLOCKED_MISSING_ADAPTER

    body = build_fixture_watch_session()
    cid = m52_sealed.get("candidate_identity") or {}
    ck_sha = str(cid.get("candidate_checkpoint_sha256") or CANONICAL_CANDIDATE_CHECKPOINT_SHA256)
    body["input_bindings"]["candidate_checkpoint_sha256"] = ck_sha.lower()
    body["input_bindings"]["m52a_adapter_json_sha256"] = str(
        m52_sealed.get(_DIGEST_FIELD) or "",
    ).lower()
    body["watch_session"].update(
        {
            "session_status": session_status,
            "policy_source": policy_src,
            "candidate_policy_adapter_status": adapter_label,
            "live_sc2_invoked": live,
            "torch_load_invoked_for_watchability_adapter": torch_on,
            "checkpoint_blob_loaded_for_watchability_adapter": ck_blob,
            "replay_saved": replay_saved,
            "map": None,
            "opponent_mode": "burnysc2_passive_bot",
            "game_steps_observed": game_steps,
            "action_count": action_count,
            "duration_seconds": None,
            "sc2_result": sc2_result,
        },
    )
    body["visual_classification"].update(
        {
            "classification": classification,
            "classification_reason": reason,
            "is_candidate_policy_control_confirmed": confirmed,
            "is_scaffold_policy": scaffold_used,
            "is_benchmark_evidence": False,
        },
    )
    body["artifact_references"]["replay_file_reference"] = replay_rel
    body["artifact_references"]["replay_sha256"] = replay_sha
    body["artifact_references"]["watch_session_raw_receipt_sha256"] = str(
        m52_sealed.get(_DIGEST_FIELD) or "",
    ).lower()

    flags = _claim_template()
    flags["visual_watch_session_attempted"] = True
    flags["live_sc2_executed"] = live
    flags["candidate_policy_control_confirmed"] = confirmed
    flags["scaffold_policy_used"] = scaffold_used
    body["claim_flags"] = flags
    return body


def session_body_from_m51_delegate(
    m51_sealed: dict[str, Any],
    *,
    m57_output_dir: Path,
) -> dict[str, Any]:
    from starlab.v15.m51_live_candidate_watchability_harness_models import (
        STATUS_LIVE_COMPLETED_WARNINGS,
        STATUS_LIVE_FAILED,
        STATUS_SCAFFOLD_COMPLETED,
    )

    st = str(m51_sealed.get("watchability_status") or "")
    live = bool(m51_sealed.get("live_sc2_executed"))
    wr = m51_sealed.get("watchability_run") or {}
    replay_saved = bool(wr.get("replay_saved")) if isinstance(wr, dict) else False
    action_count = wr.get("action_count") if isinstance(wr, dict) else None
    obs_count = wr.get("observation_count") if isinstance(wr, dict) else None
    map_val = wr.get("map") if isinstance(wr, dict) else None
    if isinstance(map_val, str) and len(map_val) > 120:
        map_val = "local_map_path_redacted"

    classification = CLASSIFICATION_PREFLIGHT_BLOCKED
    reason = "M51 scaffold delegate did not complete successfully."
    session_status = CLASSIFICATION_PREFLIGHT_BLOCKED
    sc2_result: str | None = None
    if st in (STATUS_SCAFFOLD_COMPLETED, STATUS_LIVE_COMPLETED_WARNINGS):
        classification = CLASSIFICATION_SCAFFOLD
        reason = "M51 scaffold watchability completed; not candidate policy control."
        session_status = CLASSIFICATION_SCAFFOLD
        sc2_result = "completed"
    elif st == STATUS_LIVE_FAILED and live:
        classification = CLASSIFICATION_PREFLIGHT_BLOCKED
        reason = "M51 scaffold live SC2 failed at runtime (watchability only)."
        session_status = CLASSIFICATION_PREFLIGHT_BLOCKED
        sc2_result = "live_runtime_error"

    replay_rel: str | None = None
    replay_sha: str | None = None
    if replay_saved:
        _ = m57_output_dir
        replay_rel = "m51_delegate/watchability_run/replay/validation.SC2Replay"

    body = build_fixture_watch_session()
    cid = m51_sealed.get("candidate_identity") or {}
    ck_sha = str(
        cid.get("candidate_checkpoint_sha256") or CANONICAL_CANDIDATE_CHECKPOINT_SHA256,
    )
    body["input_bindings"]["candidate_checkpoint_sha256"] = ck_sha.lower()
    body["input_bindings"]["m51_watchability_json_sha256"] = str(
        m51_sealed.get(_DIGEST_FIELD) or "",
    ).lower()
    body["watch_session"].update(
        {
            "session_status": session_status,
            "policy_source": POLICY_SCAFFOLD,
            "candidate_policy_adapter_status": ADAPTER_NOT_USED,
            "live_sc2_invoked": live,
            "torch_load_invoked_for_watchability_adapter": False,
            "checkpoint_blob_loaded_for_watchability_adapter": False,
            "replay_saved": replay_saved,
            "map": map_val,
            "opponent_mode": "burnysc2_passive_bot",
            "game_steps_observed": obs_count,
            "action_count": action_count,
            "duration_seconds": None,
            "sc2_result": sc2_result,
        },
    )
    body["visual_classification"].update(
        {
            "classification": classification,
            "classification_reason": reason,
            "is_candidate_policy_control_confirmed": False,
            "is_scaffold_policy": True,
            "is_benchmark_evidence": False,
        },
    )
    body["artifact_references"]["replay_file_reference"] = replay_rel
    body["artifact_references"]["replay_sha256"] = replay_sha
    body["artifact_references"]["watch_session_raw_receipt_sha256"] = str(
        m51_sealed.get(_DIGEST_FIELD) or "",
    ).lower()

    flags = _claim_template()
    flags["visual_watch_session_attempted"] = True
    flags["live_sc2_executed"] = live
    flags["scaffold_policy_used"] = st in (
        STATUS_SCAFFOLD_COMPLETED,
        STATUS_LIVE_COMPLETED_WARNINGS,
    )
    body["claim_flags"] = flags
    return body


def validate_candidate_sha(path: Path | None, *, expected: str) -> str | None:
    exp = str(expected).strip().lower()
    if validate_sha256(exp) is None:
        return "invalid_expected_candidate_sha256"
    if path is None or not path.is_file():
        return "candidate_checkpoint_path_missing"
    got = sha256_file_hex(path.resolve())
    if got != exp:
        return "candidate_checkpoint_sha_mismatch"
    return None


def classify_policy_source(*, prefer_adapter: bool, scaffold_authorized: bool) -> str:
    if prefer_adapter:
        return POLICY_CANDIDATE_LIVE_ADAPTER
    if scaffold_authorized:
        return POLICY_SCAFFOLD
    return POLICY_BLOCKED


def classify_visual_session(*, session_status: str, policy: str) -> str:
    _ = session_status
    if policy == POLICY_SCAFFOLD:
        return CLASSIFICATION_SCAFFOLD
    if policy == POLICY_CANDIDATE_LIVE_ADAPTER:
        return CLASSIFICATION_CANDIDATE_LIVE_COMPLETED
    return CLASSIFICATION_BLOCKED_MISSING_ADAPTER
