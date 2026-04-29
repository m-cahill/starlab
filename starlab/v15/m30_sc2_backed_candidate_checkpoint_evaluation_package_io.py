"""Build and emit V15-M30 SC2-backed candidate checkpoint evaluation package."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Final

from starlab.runs.json_util import canonical_json_dumps, sha256_hex_of_canonical_json
from starlab.v15.candidate_checkpoint_evaluation_package_io import seal_package_body
from starlab.v15.full_30min_sc2_backed_t1_run_models import (
    CONTRACT_ID as CONTRACT_M29,
)
from starlab.v15.full_30min_sc2_backed_t1_run_models import (
    OUTCOME_FULL_30_WITH_CHECKPOINT,
    PROFILE_OPERATOR_LOCAL_FULL_WALL,
)
from starlab.v15.m30_sc2_backed_candidate_checkpoint_evaluation_package_models import (
    CHECKLIST_FILENAME,
    CONTRACT_ID_PACKAGE_V1,
    EMITTER_MODULE_M30,
    FILENAME_PACKAGE,
    MILESTONE_LABEL_V30,
    NON_CLAIMS_M30,
    PACKAGE_PROFILE_ID_M30,
    REPORT_FILENAME,
    SCHEMA_VERSION,
    SCORECARD_BOUND,
    SCORECARD_OPTIONAL_NOT_SUPPLIED,
    STATUS_BLOCKED,
    STATUS_READY,
)
from starlab.v15.sc2_backed_t1_candidate_training_models import (
    CONTRACT_ID as CONTRACT_M28,
)
from starlab.v15.sc2_backed_t1_candidate_training_models import (
    EXPECTED_M27_CONTRACT_ID,
    M27_OUTCOME_COMPLETED,
)
from starlab.v15.sc2_backed_t1_candidate_training_models import (
    OUTCOME_WITH_CHECKPOINT as M28_OUTCOME_WITH_CKPT,
)
from starlab.v15.sc2_rollout_training_loop_integration_models import CONTRACT_ID as CONTRACT_M27
from starlab.v15.strong_agent_scorecard_models import (
    CONTRACT_ID_STRONG_AGENT_SCORECARD,
    PROTOCOL_PROFILE_ID,
)

_HEX64: Final[re.Pattern[str]] = re.compile(r"^[0-9a-f]{64}$")

_FULL_CLOCK_TOLERANCE_S: Final[float] = 10.0


def _is_hex64(s: str) -> bool:
    return bool(s and _HEX64.match(s.lower()))


def _parse_json_object(path: Path) -> dict[str, Any]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ValueError("JSON root must be an object")
    return raw


def _canonical_seal_ok(raw: dict[str, Any]) -> tuple[bool, str]:
    seal_in = raw.get("artifact_sha256")
    wo = {k: v for k, v in raw.items() if k != "artifact_sha256"}
    computed = sha256_hex_of_canonical_json(wo)
    return str(seal_in or "").lower() == computed.lower(), computed


def _blocked_sorted(reasons: list[str]) -> list[str]:
    return sorted(dict.fromkeys(reasons))


def _validate_optional_scorecard(obj: dict[str, Any]) -> list[str]:
    errs: list[str] = []
    if str(obj.get("contract_id", "")) != CONTRACT_ID_STRONG_AGENT_SCORECARD:
        errs.append("blocked_invalid_scorecard_protocol_json")
    if str(obj.get("protocol_profile_id", "")) != PROTOCOL_PROFILE_ID:
        errs.append("blocked_invalid_scorecard_protocol_json")
    return sorted(dict.fromkeys(errs))


def _public_upstream_m27_digest(m28_upstream: dict[str, Any]) -> dict[str, Any]:
    """Bind lineage without leaking absolute paths."""
    out = {
        "path_role": str(m28_upstream.get("path_role") or ""),
        "resolved_path_status": "redacted_operator_local_path",
        "contract_id": str(m28_upstream.get("contract_id") or ""),
        "artifact_sha256": str(m28_upstream.get("sha256") or ""),
        "outcome": str(m28_upstream.get("outcome") or ""),
        "training_loop_binding_status": str(m28_upstream.get("training_loop_binding_status") or ""),
        "action_count_summary": m28_upstream.get("action_count_summary"),
    }
    return out


def validate_m30_inputs(
    *,
    m27: dict[str, Any],
    m28: dict[str, Any],
    m29: dict[str, Any],
    scorecard: dict[str, Any] | None,
) -> list[str]:
    """Return sorted blocker codes (empty list means package may seal ready)."""
    blocked: list[str] = []

    seal_ok27, _ = _canonical_seal_ok(m27)
    if not seal_ok27:
        blocked.append("blocked_invalid_m27_contract")
    seal_ok28, _ = _canonical_seal_ok(m28)
    if not seal_ok28:
        blocked.append("blocked_invalid_m28_contract")
    seal_ok29, _ = _canonical_seal_ok(m29)
    if not seal_ok29:
        blocked.append("blocked_invalid_m29_contract")

    if str(m27.get("contract_id", "")) != CONTRACT_M27:
        blocked.append("blocked_invalid_m27_contract")
    if str(m28.get("contract_id", "")) != CONTRACT_M28:
        blocked.append("blocked_invalid_m28_contract")
    if str(m29.get("contract_id", "")) != CONTRACT_M29:
        blocked.append("blocked_invalid_m29_contract")

    m27_sha = str(m27.get("artifact_sha256") or "").lower()
    m28_sha = str(m28.get("artifact_sha256") or "").lower()
    m29_sha = str(m29.get("artifact_sha256") or "").lower()
    if not _is_hex64(m27_sha):
        blocked.append("blocked_invalid_m27_contract")
    if not _is_hex64(m28_sha):
        blocked.append("blocked_invalid_m28_contract")
    if not _is_hex64(m29_sha):
        blocked.append("blocked_invalid_m29_contract")

    # M29 profile / outcome / wall clock
    prof = str(m29.get("profile") or "")
    if prof != PROFILE_OPERATOR_LOCAL_FULL_WALL:
        blocked.append("blocked_invalid_m29_contract")

    if str(m29.get("m29_outcome") or "") != OUTCOME_FULL_30_WITH_CHECKPOINT:
        blocked.append("blocked_m29_not_candidate_checkpoint_outcome")

    if not bool(m29.get("full_wall_clock_satisfied")):
        blocked.append("blocked_m29_full_wall_clock_not_satisfied")

    req_sec = float(m29.get("requested_min_wall_clock_seconds") or 0.0)
    obs_sec = float(m29.get("observed_wall_clock_seconds") or 0.0)
    if req_sec + 1e-9 < 1800.0:
        blocked.append("blocked_invalid_m29_contract")
    if obs_sec + _FULL_CLOCK_TOLERANCE_S + 1e-9 < req_sec:
        blocked.append("blocked_m29_full_wall_clock_not_satisfied")

    if not bool(m29.get("sc2_backed_features_used")):
        blocked.append("blocked_invalid_m29_contract")

    if str(m29.get("candidate_checkpoint_promotion_status") or "") != "not_promoted_candidate_only":
        blocked.append("blocked_candidate_checkpoint_not_candidate_only")

    cand_m29 = str(m29.get("candidate_checkpoint_sha256_operator_local") or "").lower()
    if not _is_hex64(cand_m29):
        blocked.append("blocked_invalid_m29_contract")

    # M28 expectations
    if str(m28.get("m28_outcome") or "") != M28_OUTCOME_WITH_CKPT:
        blocked.append("blocked_invalid_m28_contract")

    _ta = m28.get("training_attempt")
    ta: dict[str, Any] = _ta if isinstance(_ta, dict) else {}
    _cc = m28.get("candidate_checkpoint")
    cc_m28: dict[str, Any] = _cc if isinstance(_cc, dict) else {}

    if not bool(ta.get("sc2_backed_features_used")):
        blocked.append("blocked_invalid_m28_contract")

    if not bool(ta.get("full_wall_clock_satisfied")):
        blocked.append("blocked_invalid_m28_contract")

    if not bool(ta.get("require_full_wall_clock")):
        blocked.append("blocked_invalid_m28_contract")

    wc28 = float(ta.get("wall_clock_seconds") or 0.0)
    req28 = float(ta.get("requested_min_wall_clock_seconds") or 0.0)
    if wc28 + _FULL_CLOCK_TOLERANCE_S + 1e-9 < req28 or req28 + 1e-9 < 1800.0:
        blocked.append("blocked_invalid_m28_contract")

    if not bool(cc_m28.get("produced")):
        blocked.append("blocked_candidate_checkpoint_not_produced")

    sha_ck_m28 = str(cc_m28.get("sha256") or "").lower()
    if str(cc_m28.get("promotion_status") or "") != "not_promoted_candidate_only":
        blocked.append("blocked_candidate_checkpoint_not_candidate_only")

    if cand_m29 and sha_ck_m28 and cand_m29 != sha_ck_m28:
        blocked.append("blocked_candidate_checkpoint_sha_mismatch")

    if str(ta.get("candidate_checkpoint_sha256") or "").lower() != cand_m29:
        blocked.append("blocked_candidate_checkpoint_sha_mismatch")

    primary28 = str(m29.get("upstream_m28_primary_artifact_sha256") or "").lower()
    if m28_sha and primary28 and m28_sha != primary28:
        blocked.append("blocked_m28_m29_artifact_sha_mismatch")

    upstream27_ref = str(m29.get("upstream_m27_artifact_sha256") or "").lower()
    if upstream27_ref and m27_sha and upstream27_ref != m27_sha:
        blocked.append("blocked_m27_m28_m29_artifact_sha_mismatch")

    _um = m28.get("upstream_m27_rollout")
    um27_m28: dict[str, Any] = _um if isinstance(_um, dict) else {}
    um27_sha_m28 = str(um27_m28.get("sha256") or "").lower()
    if um27_sha_m28 and m27_sha and um27_sha_m28 != m27_sha:
        blocked.append("blocked_m27_m28_m29_artifact_sha_mismatch")

    cand_ref = str(m29.get("upstream_m28_candidate_checkpoint_sha256_reference") or "").lower()
    if cand_ref and cand_m29 and cand_ref != cand_m29:
        blocked.append("blocked_candidate_checkpoint_sha_mismatch")

    # M27 semantics (completed rollout + training loop binding + nonzero actions)
    if str(m27.get("m27_outcome") or "") != M27_OUTCOME_COMPLETED:
        blocked.append("blocked_invalid_m27_contract")

    _bind = m27.get("training_loop_binding")
    bind: dict[str, Any] = _bind if isinstance(_bind, dict) else {}
    if str(bind.get("status") or "") != "training_update_executed":
        blocked.append("blocked_invalid_m27_contract")

    eps = m27.get("episodes") if isinstance(m27.get("episodes"), list) else []
    if not eps:
        blocked.append("blocked_invalid_m27_contract")
    else:
        for ep in eps:
            if not isinstance(ep, dict):
                blocked.append("blocked_invalid_m27_contract")
                break
            ac = int(ep.get("action_count") or 0)
            if ac <= 0:
                blocked.append("blocked_invalid_m27_contract")
                break

    if str(um27_m28.get("contract_id") or "") != EXPECTED_M27_CONTRACT_ID:
        blocked.append("blocked_invalid_m27_contract")

    acts_raw = um27_m28.get("action_count_summary")
    acts = acts_raw if isinstance(acts_raw, list) else []
    if acts:
        for x in acts:
            try:
                if int(x) <= 0:
                    blocked.append("blocked_invalid_m27_contract")
                    break
            except (TypeError, ValueError):
                blocked.append("blocked_invalid_m27_contract")
                break

    if scorecard is not None:
        blocked.extend(_validate_optional_scorecard(scorecard))

    return _blocked_sorted(blocked)


def build_m30_package_body(
    *,
    m27: dict[str, Any],
    m28: dict[str, Any],
    m29: dict[str, Any],
    scorecard: dict[str, Any] | None,
    scorecard_sha256: str | None,
    blocked_reasons: list[str],
) -> dict[str, Any]:
    cand_sha = str(m29.get("candidate_checkpoint_sha256_operator_local") or "").lower()
    upstream27 = str(m29.get("upstream_m27_artifact_sha256") or "").lower()
    upstream28 = str(m29.get("upstream_m28_primary_artifact_sha256") or "").lower()
    upstream29 = str(m29.get("artifact_sha256") or "").lower()

    _up_roll = m28.get("upstream_m27_rollout")
    up_roll: dict[str, Any] = _up_roll if isinstance(_up_roll, dict) else {}

    score_invalid = "blocked_invalid_scorecard_protocol_json" in blocked_reasons
    if scorecard is None:
        score_binding = {
            "scorecard_binding_status": SCORECARD_OPTIONAL_NOT_SUPPLIED,
        }
    elif score_invalid:
        score_binding = {
            "scorecard_binding_status": "invalid_scorecard_protocol_json",
            "evaluation_protocol_contract_id": str(scorecard.get("contract_id") or ""),
            "evaluation_protocol_profile_id": str(scorecard.get("protocol_profile_id") or ""),
        }
    else:
        score_binding = {
            "scorecard_binding_status": SCORECARD_BOUND,
            "evaluation_protocol_contract_id": str(scorecard.get("contract_id") or ""),
            "evaluation_protocol_profile_id": str(scorecard.get("protocol_profile_id") or ""),
            "scorecard_artifact_sha256": str(scorecard_sha256 or ""),
        }

    ready = len(blocked_reasons) == 0

    body: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "contract_id": CONTRACT_ID_PACKAGE_V1,
        "milestone": MILESTONE_LABEL_V30,
        "package_profile_id": PACKAGE_PROFILE_ID_M30,
        "emitter_module": EMITTER_MODULE_M30,
        "package_status": STATUS_READY if ready else STATUS_BLOCKED,
        "evaluation_package_ready": ready,
        "ready_for_future_checkpoint_evaluation": ready,
        "blocked_reasons": blocked_reasons,
        "strength_evaluated": False,
        "checkpoint_promoted": False,
        "benchmark_passed": False,
        "candidate_checkpoint": {
            "sha256": cand_sha,
            "promotion_status": "not_promoted_candidate_only",
            "source_milestone": "V15-M29",
        },
        "bindings": {
            "m27_sc2_rollout_artifact_sha256": upstream27,
            "m28_sc2_backed_training_artifact_sha256": upstream28,
            "m29_full_30min_artifact_sha256": upstream29,
            "candidate_checkpoint_sha256": cand_sha,
        },
        "upstream_m27_rollout_public_digest": _public_upstream_m27_digest(up_roll),
        "evaluation_protocol_binding": score_binding,
        "non_claims": list(NON_CLAIMS_M30),
    }
    return body


def build_m30_report(sealed: dict[str, Any]) -> dict[str, Any]:
    base = {k: v for k, v in sealed.items() if k != "artifact_sha256"}
    digest = sha256_hex_of_canonical_json(base)
    return {
        "report_kind": "v15_candidate_checkpoint_evaluation_package_report",
        "report_version": "m30",
        "milestone": MILESTONE_LABEL_V30,
        "contract_id": CONTRACT_ID_PACKAGE_V1,
        "package_profile_id": PACKAGE_PROFILE_ID_M30,
        "artifact_sha256": digest,
        "package_status": sealed.get("package_status"),
        "evaluation_package_ready": sealed.get("evaluation_package_ready"),
        "blocked_reasons": sealed.get("blocked_reasons"),
        "bindings": sealed.get("bindings"),
        "candidate_checkpoint": sealed.get("candidate_checkpoint"),
    }


def build_m30_checklist_md(sealed: dict[str, Any]) -> str:
    st = str(sealed.get("package_status", ""))
    ready = str(sealed.get("package_status")) == STATUS_READY
    mark = "[x]" if ready else "[ ]"
    br = sealed.get("blocked_reasons") or []
    br_txt = ", ".join(str(x) for x in br) if br else "(none)"
    return (
        "# V15-M30 — SC2-backed candidate checkpoint evaluation package checklist\n\n"
        f"**`package_status`:** `{st}`  \n"
        f"**`blocked_reasons`:** `{br_txt}`\n\n"
        "| Gate | Check |\n"
        "| --- | --- |\n"
        f"| G1 — M29 contract + full wall clock + candidate outcome | {mark} |\n"
        f"| G2 — M28 SC2-backed training + delegated seal matches M29 | {mark} |\n"
        f"| G3 — M27 rollout seal + binding consistency | {mark} |\n"
        f"| G4 — Candidate checkpoint SHA chain | {mark} |\n"
        f"| G5 — Optional M05 scorecard (when supplied) | {mark} protocol binding only |\n"
        f"| G6 — Non-claims / no strength or promotion claims | {mark} |\n\n"
        "V15-M30 binds sealed operator receipts for future evaluation. "
        "It does not execute benchmark matches or measure strength.\n"
    )


def emit_m30_sc2_backed_candidate_checkpoint_evaluation_package(
    output_dir: Path,
    *,
    m27_path: Path,
    m28_path: Path,
    m29_path: Path,
    scorecard_path: Path | None,
) -> tuple[dict[str, Any], Path, Path, Path]:
    """Load inputs, validate, emit sealed JSON + report + checklist under output_dir."""

    m27 = _parse_json_object(m27_path)
    m28 = _parse_json_object(m28_path)
    m29 = _parse_json_object(m29_path)

    scorecard: dict[str, Any] | None = None
    score_sha: str | None = None
    if scorecard_path is not None:
        scorecard = _parse_json_object(scorecard_path)
        wo = {k: v for k, v in scorecard.items() if k != "artifact_sha256"}
        score_sha = sha256_hex_of_canonical_json(wo)

    blocked = validate_m30_inputs(m27=m27, m28=m28, m29=m29, scorecard=scorecard)

    body_pre = build_m30_package_body(
        m27=m27,
        m28=m28,
        m29=m29,
        scorecard=scorecard,
        scorecard_sha256=score_sha,
        blocked_reasons=blocked,
    )
    sealed = seal_package_body(body_pre)

    output_dir.mkdir(parents=True, exist_ok=True)
    rep = build_m30_report(sealed)
    chk = build_m30_checklist_md(sealed)

    p_pkg = output_dir / FILENAME_PACKAGE
    p_rep = output_dir / REPORT_FILENAME
    p_chk = output_dir / CHECKLIST_FILENAME

    p_pkg.write_text(canonical_json_dumps(sealed), encoding="utf-8")
    p_rep.write_text(canonical_json_dumps(rep), encoding="utf-8")
    p_chk.write_text(chk, encoding="utf-8", newline="\n")
    return sealed, p_pkg, p_rep, p_chk
