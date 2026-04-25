"""Build, seal, write V15-M10 replay-native XAI demonstration + JSON report + Markdown report."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from starlab.runs.json_util import canonical_json_dumps, sha256_hex_of_canonical_json
from starlab.v15.checkpoint_evaluation_io import m08_campaign_receipt_valid_for_m09
from starlab.v15.checkpoint_evaluation_models import (
    CONTRACT_ID_CHECKPOINT_PROMOTION_DECISION,
    PROMOTION_STATUS_PROMOTED_XAI,
)
from starlab.v15.checkpoint_lineage_models import CONTRACT_ID_CHECKPOINT_LINEAGE
from starlab.v15.environment_lock_io import redact_paths_in_value
from starlab.v15.long_gpu_training_manifest_models import CONTRACT_ID_LONG_GPU_CAMPAIGN_RECEIPT
from starlab.v15.strong_agent_scorecard_models import CONTRACT_ID_STRONG_AGENT_SCORECARD
from starlab.v15.training_run_receipt_io import _redaction_token_count, redact_receipt_value
from starlab.v15.xai_demonstration_models import (
    ALL_DECISION_CLASSES,
    ALL_GATE_IDS,
    ALL_SCENE_TYPES,
    CONTRACT_ID_REPLAY_NATIVE_XAI_DEMONSTRATION,
    CONTRACT_VERSION,
    DEMONSTRATION_STATUS_BLOCKED_M08_RECEIPT,
    DEMONSTRATION_STATUS_BLOCKED_PROMOTED_CP,
    DEMONSTRATION_STATUS_FIXTURE_CONTRACT_ONLY,
    DEMONSTRATION_STATUS_OPERATOR_DECLARED_PACK,
    EMITTER_MODULE_REPLAY_NATIVE_XAI,
    FILENAME_REPLAY_NATIVE_XAI_DEMONSTRATION,
    FILENAME_XAI_EXPLANATION_REPORT_MD,
    FIXTURE_DEMONSTRATION_ID,
    MILESTONE_ID_V15_M10,
    NON_CLAIMS_V15_M10,
    PLACEHOLDER_SHA256,
    PROFILE_FIXTURE_CI,
    PROFILE_ID_REPLAY_NATIVE_XAI_DEMONSTRATION,
    PROFILE_OPERATOR_DECLARED,
    PROFILE_OPERATOR_PREFLIGHT,
    REPORT_FILENAME_REPLAY_NATIVE_XAI_DEMONSTRATION,
    REPORT_VERSION_REPLAY_NATIVE_XAI,
    SEAL_KEY_REPLAY_NATIVE_XAI_DEMONSTRATION,
    XAI_EVIDENCE_FAMILY_CONTRACT_ID,
    default_m10_authorization_flags,
)
from starlab.v15.xai_demonstration_models import GATE_STATUS_BLOCKED as GS_BLOCKED
from starlab.v15.xai_demonstration_models import GATE_STATUS_NOT_EVALUATED as GS_NE
from starlab.v15.xai_demonstration_models import GATE_STATUS_PASS as GS_PASS
from starlab.v15.xai_demonstration_models import GATE_STATUS_WARNING as GS_WARN
from starlab.v15.xai_evidence_models import CONTRACT_ID_XAI_EVIDENCE


def _json_file_canonical_sha256(path: Path) -> str:
    raw = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ValueError("JSON must be a single object")
    return sha256_hex_of_canonical_json(raw)


def redact_demonstration_value(obj: Any) -> Any:
    return redact_receipt_value(redact_paths_in_value(obj))


def _gate(gate_id: str, status: str, notes: str) -> dict[str, Any]:
    return {"gate_id": gate_id, "status": status, "notes": notes}


def _fixture_gates() -> list[dict[str, Any]]:
    return [
        _gate(ALL_GATE_IDS[0], GS_PASS, "Fixture JSON matches M10 schema; deterministic."),
        _gate(
            ALL_GATE_IDS[1],
            GS_BLOCKED,
            (
                "M09 public posture: no promoted checkpoint for downstream XAI "
                "binding on default path."
            ),
        ),
        _gate(
            ALL_GATE_IDS[2],
            GS_BLOCKED,
            "Replay identity is fixture metadata only; no real replay binary bound in fixture_ci.",
        ),
        _gate(
            ALL_GATE_IDS[3],
            GS_BLOCKED,
            "Checkpoint identity is placeholder; no promoted trained checkpoint for XAI demo.",
        ),
        _gate(
            ALL_GATE_IDS[4],
            GS_WARN,
            "Decision trace rows are fixture vocabulary; not model output.",
        ),
        _gate(
            ALL_GATE_IDS[5],
            GS_PASS,
            (
                "Scene coverage vocabulary present for macro/tactical/scout/counterfactual "
                "(fixture rows)."
            ),
        ),
        _gate(
            ALL_GATE_IDS[6],
            GS_BLOCKED,
            "Counterfactual coverage is schema-level on default path; not executed evaluation.",
        ),
        _gate(
            ALL_GATE_IDS[7],
            GS_BLOCKED,
            (
                "Replay overlay manifest is metadata only; no committed media in repository "
                "default path."
            ),
        ),
        _gate(
            ALL_GATE_IDS[8],
            GS_PASS,
            "Markdown explanation report emitted deterministically from JSON.",
        ),
        _gate(
            ALL_GATE_IDS[9], GS_PASS, "No absolute paths in fixture artifact; paths not committed."
        ),
        _gate(
            ALL_GATE_IDS[10],
            GS_PASS,
            "Non-claims and authorization flags are false on fixture default path.",
        ),
    ]


def _fixture_scene_coverage() -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for i, st in enumerate(ALL_SCENE_TYPES):
        is_loss = st == "loss_or_failure_case"
        out.append(
            {
                "scene_type": st,
                "posture": "fixture_row",
                "represented_in_fixture": True,
                "executed_against_trained_model": False,
                "notes": (
                    "Fixture row for scene vocabulary; real demonstration blocked without promoted "
                    "checkpoint and operator evidence."
                    if not is_loss
                    else (
                        "Loss/failure case included as fixture vocabulary; "
                        "not a real match outcome."
                    )
                ),
            }
        )
    return out


def _fixture_decision_class_coverage() -> list[dict[str, Any]]:
    return [
        {
            "decision_class": dc,
            "fixture_rows": 1
            if dc in ("macro", "tactical", "scouting_uncertainty", "counterfactual")
            else 0,
            "posture": "fixture_vocabulary",
        }
        for dc in ALL_DECISION_CLASSES
    ]


def build_demonstration_body_fixture() -> dict[str, Any]:
    flags = default_m10_authorization_flags()
    return {
        "contract_id": CONTRACT_ID_REPLAY_NATIVE_XAI_DEMONSTRATION,
        "contract_version": CONTRACT_VERSION,
        "profile_id": PROFILE_ID_REPLAY_NATIVE_XAI_DEMONSTRATION,
        "profile": PROFILE_FIXTURE_CI,
        "milestone": MILESTONE_ID_V15_M10,
        "created_by": EMITTER_MODULE_REPLAY_NATIVE_XAI,
        "demonstration_id": FIXTURE_DEMONSTRATION_ID,
        "xai_evidence_family_contract_id": XAI_EVIDENCE_FAMILY_CONTRACT_ID,
        "demonstration_status": DEMONSTRATION_STATUS_FIXTURE_CONTRACT_ONLY,
        "blocked_path_reasons": [DEMONSTRATION_STATUS_BLOCKED_PROMOTED_CP, "M09: no promotion"],
        "evidence_scope": "ci_fixture_schema_only",
        "m09_promotion_decision_binding": {
            "contract_id": CONTRACT_ID_CHECKPOINT_PROMOTION_DECISION,
            "promotion_decision_json_canonical_sha256": PLACEHOLDER_SHA256,
            "binding_status": "fixture_placeholder",
        },
        "m04_xai_evidence_pack_binding": {
            "contract_id": CONTRACT_ID_XAI_EVIDENCE,
            "xai_evidence_pack_json_canonical_sha256": PLACEHOLDER_SHA256,
            "binding_status": "fixture_placeholder",
        },
        "m08_campaign_receipt_binding": {
            "contract_id": CONTRACT_ID_LONG_GPU_CAMPAIGN_RECEIPT,
            "m08_campaign_receipt_json_canonical_sha256": PLACEHOLDER_SHA256,
            "binding_status": "not_applicable_fixture",
        },
        "scene_coverage": _fixture_scene_coverage(),
        "decision_class_coverage": _fixture_decision_class_coverage(),
        "counterfactual_coverage": {
            "status": "blocked",
            "notes": (
                "Counterfactual probe schema exists under M04; "
                "no executed counterfactual eval here."
            ),
        },
        "demonstration_gates": _fixture_gates(),
        "non_claims": list(NON_CLAIMS_V15_M10),
        "authorization_flags": flags,
        "redaction_policy": {
            "fixture": "no_paths_or_secrets",
            "operator": "redact_absolute_paths_and_contacts",
        },
    }


def seal_replay_native_xai_demonstration_body(body: dict[str, Any]) -> dict[str, Any]:
    out = {k: v for k, v in body.items() if k != SEAL_KEY_REPLAY_NATIVE_XAI_DEMONSTRATION}
    digest = sha256_hex_of_canonical_json(out)
    sealed = dict(out)
    sealed[SEAL_KEY_REPLAY_NATIVE_XAI_DEMONSTRATION] = digest
    return sealed


def build_replay_native_xai_demonstration_report(
    sealed: dict[str, Any], *, redaction_count: int
) -> dict[str, Any]:
    base = {k: v for k, v in sealed.items() if k != SEAL_KEY_REPLAY_NATIVE_XAI_DEMONSTRATION}
    digest = sha256_hex_of_canonical_json(base)
    return {
        "report_kind": "v15_replay_native_xai_demonstration_report",
        "report_version": REPORT_VERSION_REPLAY_NATIVE_XAI,
        "milestone": MILESTONE_ID_V15_M10,
        "artifact_sha256": digest,
        "seal_field": SEAL_KEY_REPLAY_NATIVE_XAI_DEMONSTRATION,
        "seal_value_matches_artifact": sealed.get(SEAL_KEY_REPLAY_NATIVE_XAI_DEMONSTRATION)
        == digest,
        "redaction_events": int(redaction_count),
        "primary_filename": FILENAME_REPLAY_NATIVE_XAI_DEMONSTRATION,
        "companion_markdown": FILENAME_XAI_EXPLANATION_REPORT_MD,
    }


def render_xai_explanation_markdown(demonstration: dict[str, Any]) -> str:
    """Deterministic Markdown from demonstration JSON (use body without seal for stable text)."""
    d = {k: v for k, v in demonstration.items() if k != SEAL_KEY_REPLAY_NATIVE_XAI_DEMONSTRATION}
    status = str(d.get("demonstration_status", ""))
    m09 = d.get("m09_promotion_decision_binding")
    m04 = d.get("m04_xai_evidence_pack_binding")
    m09b = m09 if isinstance(m09, dict) else {}
    m04b = m04 if isinstance(m04, dict) else {}
    lines: list[str] = [
        "# V15 Replay-Native XAI Demonstration Report",
        "",
        "This fixture pack validates the governed XAI demonstration artifact shape. "
        "This report does not prove real model inference, faithfulness, or agent strength.",
        "",
        "- **Demonstration status** — " + status,
        "- **M04 XAI evidence family (contract id)** — "
        f"`{d.get('xai_evidence_family_contract_id', XAI_EVIDENCE_FAMILY_CONTRACT_ID)}`",
        "",
        "## Promotion / evidence bindings (metadata)",
        "",
        f"- **Promotion decision binding (M09)**: `binding_status` = "
        f"{m09b.get('binding_status', '')!r}; "
        f"`promotion_status_observed` = {m09b.get('promotion_status_observed', 'n/a')!r}",
        f"- **XAI evidence pack binding (M04)**: `binding_status` = "
        f"{m04b.get('binding_status', '')!r}",
        "",
        "## Identity surfaces (governance — not real inference)",
        "",
        "- **Replay identity status** — as recorded in scene coverage: fixture metadata; "
        "no committed replay bytes in the default path.",
        (
            "- **Checkpoint identity status** — placeholder or SHA metadata only; "
            "no weight blobs in-repo."
        ),
        "",
        "## Scene coverage summary",
        "",
    ]
    sc = d.get("scene_coverage")
    if isinstance(sc, list):
        for row in sc:
            if not isinstance(row, dict):
                continue
            st = str(row.get("scene_type", ""))
            rep = str(row.get("represented_in_fixture", ""))
            lines.append(f"- `{st}` — represented_in_fixture={rep}")
    lines += [
        "",
        "## Decision-class coverage summary",
        "",
    ]
    dc = d.get("decision_class_coverage")
    if isinstance(dc, list):
        for row in dc:
            if not isinstance(row, dict):
                continue
            lines.append(
                f"- `{row.get('decision_class', '')}` — fixture_rows={row.get('fixture_rows', 0)}"
            )
    cf = d.get("counterfactual_coverage")
    if isinstance(cf, dict):
        lines += [
            "",
            "## Counterfactual coverage summary",
            "",
            f"- **status** — {cf.get('status', '')}",
            f"- **notes** — {cf.get('notes', '')}",
        ]
    lines += [
        "",
        "## Gate table",
        "",
        "| gate_id | status | notes |",
        "| --- | --- | --- |",
    ]
    gates = d.get("demonstration_gates")
    if isinstance(gates, list):
        for g in gates:
            if not isinstance(g, dict):
                continue
            gid = str(g.get("gate_id", ""))
            st = str(g.get("status", ""))
            note = str(g.get("notes", "")).replace("|", "\\|")
            lines.append(f"| {gid} | {st} | {note} |")
    lines += [
        "",
        "## Public / private boundary",
        "",
        (
            "Public artifacts are schema, hashes, and sanitized narratives. Raw replays, weights, "
            "checkpoints, saliency tensors, and operator-local paths are not committed in the "
            "default path."
        ),
        "",
        "## Non-claims",
        "",
    ]
    ncs = d.get("non_claims")
    if isinstance(ncs, list):
        for n in ncs:
            lines.append(f"- {n}")
    else:
        for n in NON_CLAIMS_V15_M10:
            lines.append(f"- {n}")
    lines.append("")
    return "\n".join(lines)


def _demonstration_status_for_promotion(promo: dict[str, Any]) -> str:
    pstat = str(promo.get("promotion_status", ""))
    if pstat == PROMOTION_STATUS_PROMOTED_XAI:
        return DEMONSTRATION_STATUS_OPERATOR_DECLARED_PACK
    return DEMONSTRATION_STATUS_BLOCKED_PROMOTED_CP


def _validate_promotion_file(obj: dict[str, Any]) -> None:
    if str(obj.get("contract_id", "")) != CONTRACT_ID_CHECKPOINT_PROMOTION_DECISION:
        raise ValueError("m09 file must be a checkpoint promotion decision (contract_id mismatch)")


def _validate_xai_pack_file(obj: dict[str, Any]) -> None:
    if str(obj.get("contract_id", "")) != CONTRACT_ID_XAI_EVIDENCE:
        raise ValueError("m04 file must be an M04 XAI evidence pack (contract_id mismatch)")


def _validate_lineage_file(obj: dict[str, Any]) -> None:
    if str(obj.get("contract_id", "")) != CONTRACT_ID_CHECKPOINT_LINEAGE:
        raise ValueError("m03 file must be checkpoint lineage manifest (contract_id mismatch)")


def _validate_m05_file(obj: dict[str, Any]) -> None:
    if str(obj.get("contract_id", "")) != CONTRACT_ID_STRONG_AGENT_SCORECARD:
        raise ValueError("m05 file must be strong agent scorecard JSON (contract_id mismatch)")


def _validate_m08_receipt_file(obj: dict[str, Any]) -> None:
    if str(obj.get("contract_id", "")) != CONTRACT_ID_LONG_GPU_CAMPAIGN_RECEIPT:
        raise ValueError("m08 file must be long GPU campaign receipt JSON (contract_id mismatch)")


def build_demonstration_body_operator_declared(
    m09_path: Path,
    m04_path: Path,
) -> tuple[dict[str, Any], int]:
    p_raw = json.loads(m09_path.read_text(encoding="utf-8"))
    x_raw = json.loads(m04_path.read_text(encoding="utf-8"))
    if not isinstance(p_raw, dict) or not isinstance(x_raw, dict):
        raise ValueError("M09 and M04 inputs must be JSON objects")
    _validate_promotion_file(p_raw)
    _validate_xai_pack_file(x_raw)

    sha_p = _json_file_canonical_sha256(m09_path)
    sha_x = _json_file_canonical_sha256(m04_path)
    dst = _demonstration_status_for_promotion(p_raw)
    pstat = str(p_raw.get("promotion_status", ""))

    body: dict[str, Any] = {
        "contract_id": CONTRACT_ID_REPLAY_NATIVE_XAI_DEMONSTRATION,
        "contract_version": CONTRACT_VERSION,
        "profile_id": PROFILE_ID_REPLAY_NATIVE_XAI_DEMONSTRATION,
        "profile": PROFILE_OPERATOR_DECLARED,
        "milestone": MILESTONE_ID_V15_M10,
        "created_by": EMITTER_MODULE_REPLAY_NATIVE_XAI,
        "demonstration_id": f"v15_m10:operator_declared:{sha_p[:12]}",
        "xai_evidence_family_contract_id": XAI_EVIDENCE_FAMILY_CONTRACT_ID,
        "demonstration_status": dst,
        "blocked_path_reasons": (
            []
            if dst == DEMONSTRATION_STATUS_OPERATOR_DECLARED_PACK
            else [DEMONSTRATION_STATUS_BLOCKED_PROMOTED_CP]
        ),
        "evidence_scope": "operator_declared_json_sha_bindings",
        "m09_promotion_decision_binding": {
            "contract_id": CONTRACT_ID_CHECKPOINT_PROMOTION_DECISION,
            "promotion_decision_json_canonical_sha256": sha_p,
            "binding_status": "sha_bound",
            "promotion_status_observed": pstat,
        },
        "m04_xai_evidence_pack_binding": {
            "contract_id": CONTRACT_ID_XAI_EVIDENCE,
            "xai_evidence_pack_json_canonical_sha256": sha_x,
            "binding_status": "sha_bound",
        },
        "m08_campaign_receipt_binding": {
            "contract_id": CONTRACT_ID_LONG_GPU_CAMPAIGN_RECEIPT,
            "m08_campaign_receipt_json_canonical_sha256": None,
            "binding_status": "not_supplied",
        },
        "scene_coverage": _fixture_scene_coverage(),
        "decision_class_coverage": _fixture_decision_class_coverage(),
        "counterfactual_coverage": {
            "status": "not_executed",
            "notes": (
                "M10 does not execute counterfactual evaluation; M04 schema only on this path."
            ),
        },
        "demonstration_gates": _operator_declared_gates(dst),
        "non_claims": list(NON_CLAIMS_V15_M10),
        "authorization_flags": default_m10_authorization_flags(),
        "redaction_policy": {
            "fixture": "no_paths_or_secrets",
            "operator": "redact_absolute_paths_and_contacts",
        },
    }
    redacted = redact_demonstration_value(body)
    rc = _redaction_token_count(redacted)
    return redacted, rc


def _operator_declared_gates(demo_status: str) -> list[dict[str, Any]]:
    if demo_status == DEMONSTRATION_STATUS_OPERATOR_DECLARED_PACK:
        return [
            _gate(
                ALL_GATE_IDS[0], GS_PASS, "Artifact structure valid; M09/M04 contract ids accepted."
            ),
            _gate(
                ALL_GATE_IDS[1], GS_PASS, "SHA binding recorded for M09 promotion decision JSON."
            ),
            _gate(
                ALL_GATE_IDS[2],
                GS_WARN,
                "Replay identity must still be supplied outside this emitter.",
            ),
            _gate(
                ALL_GATE_IDS[3],
                GS_WARN,
                "Checkpoint identity remains governance metadata; no blob I/O.",
            ),
            _gate(
                ALL_GATE_IDS[4],
                GS_WARN,
                "Decision trace still schema-level unless separately executed.",
            ),
            _gate(
                ALL_GATE_IDS[5], GS_PASS, "Scene coverage vocabulary available in binding profile."
            ),
            _gate(
                ALL_GATE_IDS[6],
                GS_WARN,
                "Counterfactual execution not implied by M10 default path.",
            ),
            _gate(
                ALL_GATE_IDS[7], GS_WARN, "Overlay media remains private/operator-local by default."
            ),
            _gate(ALL_GATE_IDS[8], GS_PASS, "Report rendering emitted."),
            _gate(ALL_GATE_IDS[9], GS_PASS, "Paths are not embedded as committed assets."),
            _gate(
                ALL_GATE_IDS[10], GS_PASS, "Non-claim boundary preserved; execution flags false."
            ),
        ]
    return [
        _gate(ALL_GATE_IDS[0], GS_PASS, "Artifact structure valid; M09/M04 contract ids accepted."),
        _gate(
            ALL_GATE_IDS[1],
            GS_BLOCKED,
            "M09 promotion_status does not allow downstream XAI demo label.",
        ),
        _gate(
            ALL_GATE_IDS[2],
            GS_BLOCKED,
            "Replay identity not established for a real demo on this path.",
        ),
        _gate(ALL_GATE_IDS[3], GS_BLOCKED, "Checkpoint promotion for XAI not evidenced."),
        _gate(ALL_GATE_IDS[4], GS_NE, "Decision trace coverage not proven."),
        _gate(ALL_GATE_IDS[5], GS_WARN, "Scene vocabulary present; full scene execution blocked."),
        _gate(
            ALL_GATE_IDS[6], GS_BLOCKED, "Counterfactual coverage blocked pending promotion path."
        ),
        _gate(ALL_GATE_IDS[7], GS_BLOCKED, "Overlay manifest not established for public demo."),
        _gate(ALL_GATE_IDS[8], GS_PASS, "Report rendering emitted (governance)."),
        _gate(ALL_GATE_IDS[9], GS_PASS, "SHA-only bindings; no raw asset commits."),
        _gate(ALL_GATE_IDS[10], GS_PASS, "Non-claim boundary explicit."),
    ]


def build_demonstration_body_operator_preflight(
    m09_path: Path,
    m04_path: Path,
    m08_receipt_path: Path,
    m03_lineage_path: Path,
    m05_scorecard_path: Path,
) -> dict[str, Any]:
    p_raw = json.loads(m09_path.read_text(encoding="utf-8"))
    x_raw = json.loads(m04_path.read_text(encoding="utf-8"))
    r_raw = json.loads(m08_receipt_path.read_text(encoding="utf-8"))
    l_raw = json.loads(m03_lineage_path.read_text(encoding="utf-8"))
    s_raw = json.loads(m05_scorecard_path.read_text(encoding="utf-8"))
    for obj, _ in [(p_raw, "m09"), (x_raw, "m04"), (r_raw, "m08"), (l_raw, "m03"), (s_raw, "m05")]:
        if not isinstance(obj, dict):
            raise ValueError("Preflight JSON inputs must be objects")
    _validate_promotion_file(p_raw)
    _validate_xai_pack_file(x_raw)
    _validate_m08_receipt_file(r_raw)
    _validate_lineage_file(l_raw)
    _validate_m05_file(s_raw)

    sha_p = _json_file_canonical_sha256(m09_path)
    sha_x = _json_file_canonical_sha256(m04_path)
    sha_r = _json_file_canonical_sha256(m08_receipt_path)
    sha_l = _json_file_canonical_sha256(m03_lineage_path)
    sha_s = _json_file_canonical_sha256(m05_scorecard_path)
    receipt_ok = m08_campaign_receipt_valid_for_m09(r_raw)
    pstat = str(p_raw.get("promotion_status", ""))
    if not receipt_ok:
        dstatus = DEMONSTRATION_STATUS_BLOCKED_M08_RECEIPT
    elif pstat != PROMOTION_STATUS_PROMOTED_XAI:
        dstatus = DEMONSTRATION_STATUS_BLOCKED_PROMOTED_CP
    else:
        dstatus = DEMONSTRATION_STATUS_OPERATOR_DECLARED_PACK

    return {
        "contract_id": CONTRACT_ID_REPLAY_NATIVE_XAI_DEMONSTRATION,
        "contract_version": CONTRACT_VERSION,
        "profile_id": PROFILE_ID_REPLAY_NATIVE_XAI_DEMONSTRATION,
        "profile": PROFILE_OPERATOR_PREFLIGHT,
        "milestone": MILESTONE_ID_V15_M10,
        "created_by": EMITTER_MODULE_REPLAY_NATIVE_XAI,
        "demonstration_id": f"v15_m10:operator_preflight:{sha_p[:12]}",
        "xai_evidence_family_contract_id": XAI_EVIDENCE_FAMILY_CONTRACT_ID,
        "demonstration_status": dstatus,
        "blocked_path_reasons": (
            [DEMONSTRATION_STATUS_BLOCKED_M08_RECEIPT]
            if not receipt_ok
            else (
                [DEMONSTRATION_STATUS_BLOCKED_PROMOTED_CP]
                if dstatus == DEMONSTRATION_STATUS_BLOCKED_PROMOTED_CP
                else []
            )
        ),
        "evidence_scope": "operator_preflight_sha_bindings",
        "m09_promotion_decision_binding": {
            "contract_id": CONTRACT_ID_CHECKPOINT_PROMOTION_DECISION,
            "promotion_decision_json_canonical_sha256": sha_p,
            "binding_status": "sha_bound",
            "promotion_status_observed": pstat,
        },
        "m04_xai_evidence_pack_binding": {
            "contract_id": CONTRACT_ID_XAI_EVIDENCE,
            "xai_evidence_pack_json_canonical_sha256": sha_x,
            "binding_status": "sha_bound",
        },
        "m08_campaign_receipt_binding": {
            "contract_id": CONTRACT_ID_LONG_GPU_CAMPAIGN_RECEIPT,
            "m08_campaign_receipt_json_canonical_sha256": sha_r,
            "binding_status": "sha_bound" if receipt_ok else "incomplete_or_not_completed",
        },
        "m03_checkpoint_lineage_binding": {
            "contract_id": CONTRACT_ID_CHECKPOINT_LINEAGE,
            "checkpoint_lineage_manifest_json_canonical_sha256": sha_l,
            "binding_status": "sha_bound",
        },
        "m05_strong_agent_scorecard_binding": {
            "contract_id": CONTRACT_ID_STRONG_AGENT_SCORECARD,
            "strong_agent_scorecard_json_canonical_sha256": sha_s,
            "binding_status": "sha_bound",
        },
        "scene_coverage": _fixture_scene_coverage(),
        "decision_class_coverage": _fixture_decision_class_coverage(),
        "counterfactual_coverage": {
            "status": "governance_only",
            "notes": (
                "Preflight binds M04 pack by SHA; does not run inference or counterfactual "
                "execution."
            ),
        },
        "demonstration_gates": _preflight_gates(dstatus, receipt_ok),
        "non_claims": list(NON_CLAIMS_V15_M10),
        "authorization_flags": default_m10_authorization_flags(),
        "redaction_policy": {
            "fixture": "no_paths_or_secrets",
            "operator": "redact_absolute_paths_and_contacts",
        },
    }


def _preflight_gates(dstatus: str, receipt_ok: bool) -> list[dict[str, Any]]:
    if not receipt_ok:
        note = (
            "M08 campaign receipt does not record a completed long GPU campaign "
            "(M09 gate parallel)."
        )
        return _preflight_gates_base(block_m08=True, note=note)
    if dstatus != DEMONSTRATION_STATUS_OPERATOR_DECLARED_PACK:
        return _preflight_gates_base(
            block_m08=False, note="M09 promotion_status is not promoted_for_xai in supplied JSON."
        )
    return _preflight_gates_base(
        block_m08=False, note="Preflight SHA bindings present; M10 still does not run inference."
    )


def _preflight_gates_base(*, block_m08: bool, note: str) -> list[dict[str, Any]]:
    b1 = GS_BLOCKED if block_m08 else GS_PASS
    return [
        _gate(
            ALL_GATE_IDS[0],
            GS_PASS,
            "JSON objects validated; contract ids match expected families.",
        ),
        _gate(
            ALL_GATE_IDS[1],
            b1,
            note if block_m08 else "M09/M04/M05/M08/M03 SHAs bound for preflight.",
        ),
        _gate(
            ALL_GATE_IDS[2],
            GS_WARN,
            "Replay identity not verified by M10; SHA binding only elsewhere.",
        ),
        _gate(ALL_GATE_IDS[3], GS_WARN, "Checkpoint identity metadata only; no blob reads."),
        _gate(ALL_GATE_IDS[4], GS_NE, "Decision trace not executed in M10 preflight path."),
        _gate(ALL_GATE_IDS[5], GS_PASS, "Scene vocabulary check satisfied at schema level."),
        _gate(ALL_GATE_IDS[6], GS_WARN, "Counterfactual execution not performed."),
        _gate(ALL_GATE_IDS[7], GS_NE, "Overlay assets not in repository scope."),
        _gate(ALL_GATE_IDS[8], GS_PASS, "Report rendering (this milestone)."),
        _gate(ALL_GATE_IDS[9], GS_PASS, "SHA-only public footprint for supplied JSONs."),
        _gate(ALL_GATE_IDS[10], GS_PASS, "Non-claims and false execution flags preserved."),
    ]


def emit_v15_replay_native_xai_demonstration_fixture(
    output_dir: Path,
) -> tuple[dict[str, Any], dict[str, Any], Path, Path, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    body = build_demonstration_body_fixture()
    sealed = seal_replay_native_xai_demonstration_body(body)
    report = build_replay_native_xai_demonstration_report(sealed, redaction_count=0)
    md = render_xai_explanation_markdown(sealed)
    p_json = output_dir / FILENAME_REPLAY_NATIVE_XAI_DEMONSTRATION
    p_report = output_dir / REPORT_FILENAME_REPLAY_NATIVE_XAI_DEMONSTRATION
    p_md = output_dir / FILENAME_XAI_EXPLANATION_REPORT_MD
    p_json.write_text(canonical_json_dumps(sealed), encoding="utf-8")
    p_report.write_text(canonical_json_dumps(report), encoding="utf-8")
    p_md.write_text(md, encoding="utf-8", newline="\n")
    return sealed, report, p_json, p_report, p_md


def emit_v15_replay_native_xai_demonstration_operator_declared(
    output_dir: Path,
    m09_path: Path,
    m04_path: Path,
) -> tuple[dict[str, Any], dict[str, Any], int, Path, Path, Path]:
    body, rc = build_demonstration_body_operator_declared(m09_path, m04_path)
    sealed = seal_replay_native_xai_demonstration_body(body)
    report = build_replay_native_xai_demonstration_report(sealed, redaction_count=rc)
    md = render_xai_explanation_markdown(sealed)
    output_dir.mkdir(parents=True, exist_ok=True)
    p_json = output_dir / FILENAME_REPLAY_NATIVE_XAI_DEMONSTRATION
    p_report = output_dir / REPORT_FILENAME_REPLAY_NATIVE_XAI_DEMONSTRATION
    p_md = output_dir / FILENAME_XAI_EXPLANATION_REPORT_MD
    p_json.write_text(canonical_json_dumps(sealed), encoding="utf-8")
    p_report.write_text(canonical_json_dumps(report), encoding="utf-8")
    p_md.write_text(md, encoding="utf-8", newline="\n")
    return sealed, report, rc, p_json, p_report, p_md


def emit_v15_replay_native_xai_demonstration_operator_preflight(
    output_dir: Path,
    m09_path: Path,
    m04_path: Path,
    m08_receipt_path: Path,
    m03_lineage_path: Path,
    m05_scorecard_path: Path,
) -> tuple[dict[str, Any], dict[str, Any], Path, Path, Path]:
    body = build_demonstration_body_operator_preflight(
        m09_path,
        m04_path,
        m08_receipt_path,
        m03_lineage_path,
        m05_scorecard_path,
    )
    sealed = seal_replay_native_xai_demonstration_body(body)
    report = build_replay_native_xai_demonstration_report(sealed, redaction_count=0)
    md = render_xai_explanation_markdown(sealed)
    output_dir.mkdir(parents=True, exist_ok=True)
    p_json = output_dir / FILENAME_REPLAY_NATIVE_XAI_DEMONSTRATION
    p_report = output_dir / REPORT_FILENAME_REPLAY_NATIVE_XAI_DEMONSTRATION
    p_md = output_dir / FILENAME_XAI_EXPLANATION_REPORT_MD
    p_json.write_text(canonical_json_dumps(sealed), encoding="utf-8")
    p_report.write_text(canonical_json_dumps(report), encoding="utf-8")
    p_md.write_text(md, encoding="utf-8", newline="\n")
    return sealed, report, p_json, p_report, p_md
