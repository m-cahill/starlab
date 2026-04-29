"""V15-M31 harness gate validation, sealing, emit."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Final

from starlab.runs.json_util import canonical_json_dumps, sha256_hex_of_canonical_json
from starlab.v15.candidate_checkpoint_evaluation_package_io import seal_package_body
from starlab.v15.candidate_checkpoint_evaluation_package_models import (
    CONTRACT_ID_CANDIDATE_CHECKPOINT_EVALUATION_PACKAGE,
)
from starlab.v15.m30_sc2_backed_candidate_checkpoint_evaluation_package_models import (
    CONTRACT_ID_PACKAGE_V1 as M30_CONTRACT_ID,
)
from starlab.v15.m30_sc2_backed_candidate_checkpoint_evaluation_package_models import (
    EMITTER_MODULE_M30,
    MILESTONE_LABEL_V30,
    PACKAGE_PROFILE_ID_M30,
)
from starlab.v15.m30_sc2_backed_candidate_checkpoint_evaluation_package_models import (
    FILENAME_PACKAGE as M30_FILENAME_PACKAGE,
)
from starlab.v15.m30_sc2_backed_candidate_checkpoint_evaluation_package_models import (
    SCHEMA_VERSION as M30_SCHEMA_VERSION,
)
from starlab.v15.m30_sc2_backed_candidate_checkpoint_evaluation_package_models import (
    SCORECARD_OPTIONAL_NOT_SUPPLIED as M30_SCORECARD_OPTIONAL,
)
from starlab.v15.m30_sc2_backed_candidate_checkpoint_evaluation_package_models import (
    STATUS_READY as M30_PKG_STATUS_READY,
)
from starlab.v15.m31_candidate_checkpoint_evaluation_harness_gate_models import (
    CHECKLIST_FILENAME,
    CONTRACT_ID_M31_GATE,
    EMITTER_MODULE_M31,
    FILENAME_GATE_JSON,
    GATE_ARTIFACT_DIGEST_FIELD,
    MILESTONE_LABEL_M31,
    NON_CLAIMS_M31,
    PROFILE_M31_DRY_RUN,
    RECOMMENDED_NEXT_DEFAULT,
    REPORT_FILENAME,
    SCHEMA_VERSION,
    SCORECARD_BOUND_IN_M31,
    SCORECARD_OPTIONAL_NOT_SUPPLIED,
    STATUS_BLOCKED,
    STATUS_READY,
)
from starlab.v15.strong_agent_scorecard_models import (
    CONTRACT_ID_STRONG_AGENT_SCORECARD,
    PROTOCOL_PROFILE_ID,
)

_HEX64: Final[re.Pattern[str]] = re.compile(r"^[0-9a-f]{64}$")


def _is_hex64(s: str) -> bool:
    return bool(s and _HEX64.match(s.lower()))


def _canonical_seal_ok(raw: dict[str, Any]) -> bool:
    seal_in = raw.get("artifact_sha256")
    wo = {k: v for k, v in raw.items() if k != "artifact_sha256"}
    computed = sha256_hex_of_canonical_json(wo)
    return str(seal_in or "").lower() == computed.lower()


def _blocked_sorted(reasons: list[str]) -> list[str]:
    return sorted(dict.fromkeys(reasons))


def _validate_m05_protocol(scorecard: dict[str, Any]) -> list[str]:
    errs: list[str] = []
    if str(scorecard.get("contract_id", "")) != CONTRACT_ID_STRONG_AGENT_SCORECARD:
        errs.append("blocked_invalid_scorecard_protocol_json")
    if str(scorecard.get("protocol_profile_id", "")) != PROTOCOL_PROFILE_ID:
        errs.append("blocked_invalid_scorecard_protocol_json")
    return _blocked_sorted(errs)


def _parse_json_object(path: Path) -> dict[str, Any]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ValueError("JSON root must be an object")
    return raw


def load_sealed_m30_package_json(path: Path) -> dict[str, Any]:
    """Parse M30 sealed-package JSON."""
    return _parse_json_object(path)


def validate_m30_for_m31(m30_sealed: dict[str, Any]) -> list[str]:
    """Sorted blocker codes for M31 consumption of sealed M30 package JSON."""

    blocked: list[str] = []

    if not _canonical_seal_ok(m30_sealed):
        blocked.append("blocked_invalid_m30_contract")

    if (
        str(m30_sealed.get("contract_id", ""))
        != CONTRACT_ID_CANDIDATE_CHECKPOINT_EVALUATION_PACKAGE
    ):
        blocked.append("blocked_invalid_m30_contract")

    if str(m30_sealed.get("package_profile_id", "")) != PACKAGE_PROFILE_ID_M30:
        blocked.append("blocked_invalid_m30_profile")

    pkg_st = str(m30_sealed.get("package_status", ""))
    if pkg_st != M30_PKG_STATUS_READY:
        blocked.append("blocked_m30_package_not_ready")

    eval_ready = bool(m30_sealed.get("evaluation_package_ready"))
    ready_future = bool(m30_sealed.get("ready_for_future_checkpoint_evaluation"))
    if not eval_ready or not ready_future:
        blocked.append("blocked_m30_package_not_ready")

    if (
        bool(m30_sealed.get("checkpoint_promoted"))
        or bool(m30_sealed.get("strength_evaluated"))
        or bool(m30_sealed.get("benchmark_passed"))
    ):
        blocked.append("blocked_m30_claim_flags_inconsistent")

    cand_o = m30_sealed.get("candidate_checkpoint")
    cand: dict[str, Any] = cand_o if isinstance(cand_o, dict) else {}
    cand_sha = str(cand.get("sha256") or "").lower()

    if not cand:
        blocked.append("blocked_m30_candidate_checkpoint_missing")
    elif not _is_hex64(cand_sha):
        blocked.append("blocked_m30_candidate_checkpoint_sha_missing")
    elif str(cand.get("promotion_status") or "") != "not_promoted_candidate_only":
        blocked.append("blocked_m30_candidate_checkpoint_not_candidate_only")

    bind_o = m30_sealed.get("bindings")
    bind: dict[str, Any] = bind_o if isinstance(bind_o, dict) else {}

    key_m27 = str(bind.get("m27_sc2_rollout_artifact_sha256") or "")
    key_m28 = str(bind.get("m28_sc2_backed_training_artifact_sha256") or "")
    key_m29 = str(bind.get("m29_full_30min_artifact_sha256") or "")
    key_cc = str(bind.get("candidate_checkpoint_sha256") or "").lower()

    if not _is_hex64(key_m27):
        blocked.append("blocked_m30_binding_missing_m27")
    if not _is_hex64(key_m28):
        blocked.append("blocked_m30_binding_missing_m28")
    if not _is_hex64(key_m29):
        blocked.append("blocked_m30_binding_missing_m29")

    if cand and _is_hex64(cand_sha) and _is_hex64(key_cc) and cand_sha != key_cc:
        blocked.append("blocked_m30_candidate_checkpoint_sha_missing")

    return _blocked_sorted(blocked)


def build_fixture_m30_sealed_package() -> dict[str, Any]:
    """Synthetic sealed M30 package for `--fixture-ci` (deterministic hashes)."""

    sha27 = "1" * 64
    sha28 = "2" * 64
    sha29 = "3" * 64
    cand = "eac6fc1f37aa958279a80209822765ecfa6aa2525ed64a8bee88c0ac2be13d26"

    body_pre: dict[str, Any] = {
        "schema_version": M30_SCHEMA_VERSION,
        "contract_id": M30_CONTRACT_ID,
        "milestone": MILESTONE_LABEL_V30,
        "package_profile_id": PACKAGE_PROFILE_ID_M30,
        "emitter_module": EMITTER_MODULE_M30,
        "package_status": M30_PKG_STATUS_READY,
        "evaluation_package_ready": True,
        "ready_for_future_checkpoint_evaluation": True,
        "blocked_reasons": [],
        "strength_evaluated": False,
        "checkpoint_promoted": False,
        "benchmark_passed": False,
        "candidate_checkpoint": {
            "sha256": cand,
            "promotion_status": "not_promoted_candidate_only",
            "source_milestone": "fixture_ci",
        },
        "bindings": {
            "m27_sc2_rollout_artifact_sha256": sha27,
            "m28_sc2_backed_training_artifact_sha256": sha28,
            "m29_full_30min_artifact_sha256": sha29,
            "candidate_checkpoint_sha256": cand,
        },
        "upstream_m27_rollout_public_digest": {
            "path_role": "fixture_ci",
            "resolved_path_status": "redacted_operator_local_path",
            "artifact_sha256": sha27,
        },
        "evaluation_protocol_binding": {
            "scorecard_binding_status": M30_SCORECARD_OPTIONAL,
        },
        "non_claims": [
            "not_strength_evaluation",
            "not_benchmark_pass",
            "not_checkpoint_promotion",
        ],
    }
    return seal_package_body(body_pre)


def emission_has_private_path_patterns(text: str) -> bool:
    """Forbidden path-like leakage in public JSON."""

    lowered = text.lower()
    if "/home/" in lowered:
        return True
    collapsed = lowered
    prev = ""
    while collapsed != prev:
        prev = collapsed
        collapsed = collapsed.replace("\\\\", "\\")
    return ":\\coding\\" in collapsed


def _public_string_gate(s: str) -> str:
    """Strip path-shaped content that must not propagate into public artifacts."""

    raw = str(s or "")
    if emission_has_private_path_patterns(raw):
        return "[redacted_path_like_upstream_value]"
    return raw


def sanitize_m30_scorecard_upstream(m30: dict[str, Any]) -> dict[str, Any]:
    ep = m30.get("evaluation_protocol_binding")
    if not isinstance(ep, dict):
        return {"scorecard_binding_status_from_m30": ""}
    return {
        "scorecard_binding_status_from_m30": _public_string_gate(
            str(ep.get("scorecard_binding_status") or ""),
        ),
        "evaluation_protocol_contract_id": _public_string_gate(
            str(ep.get("evaluation_protocol_contract_id") or "")
        ),
        "evaluation_protocol_profile_id_from_m30": _public_string_gate(
            str(ep.get("evaluation_protocol_profile_id") or ""),
        ),
        "scorecard_artifact_sha256_from_m30": _public_string_gate(
            str(ep.get("scorecard_artifact_sha256") or "")
        ),
    }


def seal_m31_gate_body(body: dict[str, Any]) -> dict[str, Any]:
    wo = {k: v for k, v in body.items() if k != GATE_ARTIFACT_DIGEST_FIELD}
    digest = sha256_hex_of_canonical_json(wo)
    sealed = dict(wo)
    sealed[GATE_ARTIFACT_DIGEST_FIELD] = digest
    return sealed


def build_m31_gate_report(sealed_gate: dict[str, Any]) -> dict[str, Any]:
    base = {k: v for k, v in sealed_gate.items() if k != GATE_ARTIFACT_DIGEST_FIELD}
    digest = sha256_hex_of_canonical_json(base)
    return {
        "report_kind": "v15_candidate_checkpoint_evaluation_harness_gate_report",
        "report_version": "m31",
        "milestone": MILESTONE_LABEL_M31,
        "contract_id": CONTRACT_ID_M31_GATE,
        "profile": PROFILE_M31_DRY_RUN,
        "artifact_sha256": digest,
        "gate_status": sealed_gate.get("gate_status"),
        "evaluation_harness_ready": sealed_gate.get("evaluation_harness_ready"),
        "blocked_reasons": sealed_gate.get("blocked_reasons"),
    }


def build_m31_gate_checklist_md(sealed_gate: dict[str, Any]) -> str:
    br = sealed_gate.get("blocked_reasons") or []
    gs = str(sealed_gate.get("gate_status", ""))
    ready_gate = gs == STATUS_READY
    mk = "[x]" if ready_gate else "[ ]"
    br_txt = ", ".join(str(x) for x in br) if br else "(none)"
    return (
        "# V15-M31 — candidate checkpoint evaluation harness gate checklist\n\n"
        f"**`gate_status`:** `{gs}`  \n"
        f"**`blocked_reasons`:** `{br_txt}`\n\n"
        "| Gate | Check |\n"
        "| --- | --- |\n"
        f"| G0 — Fixture / operator profile valid | {mk} |\n"
        f"| G1 — M30 package canonical seal validates | {mk} |\n"
        f"| G2 — M30 contract/profile/status valid | {mk} |\n"
        f"| G3 — Candidate checkpoint identity candidate-only | {mk} |\n"
        f"| G4 — M27/M28/M29 bindings present in M30 JSON | {mk} |\n"
        f"| G5 — Optional M05 scorecard protocol (if supplied to M31) | {mk} |\n"
        f"| G6 — Dry-run evaluation plan constructed | {mk} |\n"
        f"| G7 — Claim/non-claim flags preserved | {mk} |\n"
        f"| G8 — No private path leakage in emitted JSON | {mk} |\n\n"
        "`evaluation_harness_ready` is **not** `benchmark_passed`.\n"
    )


def _non_claim_bools() -> dict[str, bool]:
    return {
        "evaluation_execution_performed": False,
        "scorecard_execution_performed": False,
        "strength_evaluated": False,
        "checkpoint_promoted": False,
        "benchmark_passed": False,
        "xai_execution_performed": False,
        "human_panel_execution_performed": False,
        "showcase_release_authorized": False,
        "v2_authorized": False,
        "t2_or_t3_authorized": False,
        "checkpoint_blob_io_performed": False,
        "candidate_model_loaded": False,
    }


def compute_m31_blockers_scorecard_binding(
    m30_sealed: dict[str, Any],
    m05_raw: dict[str, Any] | None,
) -> tuple[list[str], str]:
    """Return merged blockers and M05 binding label for serialization."""

    blockers_m30 = validate_m30_for_m31(m30_sealed)
    blockers_m05: list[str] = []
    score_status = SCORECARD_OPTIONAL_NOT_SUPPLIED
    if m05_raw is not None:
        vm = _validate_m05_protocol(m05_raw)
        if vm:
            blockers_m05.extend(vm)
        else:
            score_status = SCORECARD_BOUND_IN_M31
    merged = blockers_m30 + blockers_m05
    return _blocked_sorted(merged), score_status


def _m05_binding_public_detail(
    score_status: str,
    m05_raw: dict[str, Any] | None,
) -> dict[str, Any]:
    if m05_raw is None or score_status != SCORECARD_BOUND_IN_M31:
        return {}
    wo = {k: v for k, v in m05_raw.items() if k != "artifact_sha256"}
    return {
        "contract_id": str(m05_raw.get("contract_id") or ""),
        "protocol_profile_id": str(m05_raw.get("protocol_profile_id") or ""),
        "canonical_body_sha256_hex": sha256_hex_of_canonical_json(wo),
    }


def build_m31_gate_body_pre_seal(
    *,
    m30_sealed: dict[str, Any],
    blocked_reasons: list[str],
    scorecard_binding_status: str,
    m05_raw: dict[str, Any] | None,
    fixture_ci: bool,
) -> dict[str, Any]:
    cand = m30_sealed.get("candidate_checkpoint")
    cand_d: dict[str, Any] = cand if isinstance(cand, dict) else {}
    cand_sha = str(cand_d.get("sha256") or "").lower()
    m30_art = str(m30_sealed.get("artifact_sha256") or "").lower()
    pkg_status = str(m30_sealed.get("package_status") or "")
    nc = _non_claim_bools()
    dry_run = {
        "plan_status": "constructed_not_executed",
        "candidate_loaded": False,
        "matches_scheduled": False,
        "scorecard_results_present": False,
        "future_execution_requires_operator_authorization": True,
        "future_execution_requires_scorecard_protocol": True,
    }

    merged = list(blocked_reasons)
    ready = len(merged) == 0

    return {
        "schema_version": SCHEMA_VERSION,
        "contract_id": CONTRACT_ID_M31_GATE,
        "milestone": MILESTONE_LABEL_M31,
        "profile": PROFILE_M31_DRY_RUN,
        "emitter_module": EMITTER_MODULE_M31,
        "gate_status": STATUS_READY if ready else STATUS_BLOCKED,
        "evaluation_harness_ready": ready,
        "blocked_reasons": merged,
        "fixture_ci": fixture_ci,
        "m30_input_manifest": (
            "__fixture_ci_built_in_m30_package__" if fixture_ci else str(M30_FILENAME_PACKAGE)
        ),
        "m30_package_binding": {
            "artifact_sha256": m30_art,
            "package_status": pkg_status,
        },
        "candidate_checkpoint": {"sha256": cand_sha},
        "m30_evaluation_protocol_upstream": sanitize_m30_scorecard_upstream(m30_sealed),
        "scorecard_binding_status": scorecard_binding_status,
        "m05_protocol_binding_at_m31": _m05_binding_public_detail(
            scorecard_binding_status, m05_raw
        ),
        "recommended_next": RECOMMENDED_NEXT_DEFAULT,
        "non_claims": list(NON_CLAIMS_M31),
        "non_claim_booleans": nc,
        **nc,
        "dry_run_evaluation_plan": dry_run,
    }


def seal_with_path_hygiene(
    body_pre: dict[str, Any],
) -> dict[str, Any]:
    sealed = seal_m31_gate_body(body_pre)
    gate_txt = canonical_json_dumps(sealed)
    rep_txt = canonical_json_dumps(build_m31_gate_report(sealed))
    if emission_has_private_path_patterns(gate_txt + rep_txt):
        extra = ["blocked_private_path_leak_detected"]
        rebuilt = dict(body_pre)
        merged = _blocked_sorted([*(rebuilt.get("blocked_reasons") or []), *extra])
        rebuilt["blocked_reasons"] = merged
        rebuilt["evaluation_harness_ready"] = False
        rebuilt["gate_status"] = STATUS_BLOCKED
        return seal_m31_gate_body(rebuilt)
    return sealed


def emit_v15_m31_candidate_checkpoint_evaluation_harness_gate(
    output_dir: Path,
    *,
    m30_sealed: dict[str, Any],
    fixture_ci: bool,
    m05_path: Path | None,
) -> tuple[dict[str, Any], Path, Path, Path]:
    """Load optional M05, validate, seal gate JSON + report + checklist."""

    m05_raw: dict[str, Any] | None = None
    if m05_path is not None:
        m05_raw = _parse_json_object(m05_path)

    blocked_reasons0, score_status = compute_m31_blockers_scorecard_binding(m30_sealed, m05_raw)

    body_pre = build_m31_gate_body_pre_seal(
        m30_sealed=m30_sealed,
        blocked_reasons=blocked_reasons0,
        scorecard_binding_status=score_status,
        m05_raw=m05_raw,
        fixture_ci=fixture_ci,
    )
    sealed = seal_with_path_hygiene(body_pre)

    output_dir.mkdir(parents=True, exist_ok=True)
    rep = build_m31_gate_report(sealed)
    chk_md = build_m31_gate_checklist_md(sealed)

    p_pkg = output_dir / FILENAME_GATE_JSON
    p_rep = output_dir / REPORT_FILENAME
    p_chk = output_dir / CHECKLIST_FILENAME

    p_pkg.write_text(canonical_json_dumps(sealed), encoding="utf-8")
    p_rep.write_text(canonical_json_dumps(rep), encoding="utf-8")
    p_chk.write_text(chk_md, encoding="utf-8", newline="\n")

    gate_dump = canonical_json_dumps(sealed) + canonical_json_dumps(rep) + chk_md
    if emission_has_private_path_patterns(gate_dump):
        raise RuntimeError(
            "M31 emitter produced candidate path leakage; refuse to finalize output.",
        )

    return sealed, p_pkg, p_rep, p_chk
