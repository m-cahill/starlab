"""Build, seal, and write V15-M15 operator evidence collection preflight JSON + report + checklist."""

# ruff: noqa: E501

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from starlab.runs.json_util import canonical_json_dumps, sha256_hex_of_canonical_json
from starlab.v15.evidence_remediation_io import parse_m13_v2_decision
from starlab.v15.evidence_remediation_models import (
    ALL_GAP_IDS,
    ALL_REMEDIATION_GATE_IDS,
    CONTRACT_ID_EVIDENCE_REMEDIATION_PLAN,
    STATUS_OPERATOR_EVIDENCE_NOT_COLLECTED,
)
from starlab.v15.operator_evidence_preflight_models import (
    CONTRACT_ID_OPERATOR_EVIDENCE_COLLECTION_PREFLIGHT,
    EMITTER_MODULE_OPERATOR_EVIDENCE_PREFLIGHT,
    FILENAME_OPERATOR_EVIDENCE_COLLECTION_CHECKLIST_MD,
    FILENAME_OPERATOR_EVIDENCE_COLLECTION_PREFLIGHT,
    FORBIDDEN_CHECKLIST_SUBSTRINGS,
    GATE_POSTURE_PASS,
    GATE_POSTURE_PASS_FIXTURE,
    MILESTONE_ID_V15_M15,
    NON_CLAIMS_V15_M15,
    P0_M13_NO_GO,
    P1_M14_PLAN,
    P2_PRIVATE_WORKSPACE,
    P3_NO_PRIVATE_PATHS_COMMITTED,
    P4_INPUTS_INVENTORY,
    P5_RIGHTS_TOUCHPOINTS,
    P6_M16_ENV,
    P7_M17_LONG,
    P8_M18_CHECKPOINT,
    P9_M19_XAI,
    P10_HUMAN_PANEL,
    P11_SHOWCASE_RELEASE,
    P12_V2_BLOCKED,
    P13_NO_EXEC,
    P14_DOCS_TESTS,
    PLACEHOLDER_SHA256,
    PREFLIGHT_STATUS_PLAN_READY,
    PROFILE_FIXTURE_CI,
    PROFILE_WITH_M13_M14_BINDINGS,
    REGISTER_TOUCHPOINT_PATHS,
    REPORT_FILENAME_OPERATOR_EVIDENCE_COLLECTION_PREFLIGHT,
    REPORT_VERSION_OPERATOR_EVIDENCE_PREFLIGHT,
    S0_CONTEXT,
    S1_WORKSPACE,
    S2_ENV_SHORT,
    S3_TRAINING,
    S4_LONG_GPU,
    S5_CHECKPOINT,
    S6_EVAL,
    S7_XAI,
    S8_HUMAN,
    S9_SHOWCASE,
    S10_V2,
    SEAL_KEY_ARTIFACT,
    SEQUENCE_STATUS_BLOCKED_ARTIFACTS,
    SEQUENCE_STATUS_BLOCKED_RIGHTS,
    SEQUENCE_STATUS_BLOCKED_UPSTREAM,
    SEQUENCE_STATUS_NOT_APPLICABLE,
    SEQUENCE_STATUS_NOT_STARTED,
    SEQUENCE_STATUS_READY_REVIEW,
    STATUS_OPERATOR_EVIDENCE_NOT_STARTED,
)

_SEAL = SEAL_KEY_ARTIFACT


def _json_file_canonical_sha256(path: Path) -> str:
    raw = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ValueError("JSON must be a single object")
    return sha256_hex_of_canonical_json(raw)


def parse_m14_remediation_plan(path: Path) -> dict[str, Any]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ValueError("M14 remediation plan JSON must be a single object")
    cid = str(raw.get("contract_id", ""))
    if cid != CONTRACT_ID_EVIDENCE_REMEDIATION_PLAN:
        raise ValueError(
            f"M14 remediation plan: contract_id must be {CONTRACT_ID_EVIDENCE_REMEDIATION_PLAN!r} "
            f"(got {cid!r})"
        )
    inv = raw.get("evidence_gap_inventory")
    if not isinstance(inv, list):
        raise ValueError("M14 remediation plan: evidence_gap_inventory must be a list")
    got_gaps = {str(x.get("gap_id", "")) for x in inv if isinstance(x, dict)}
    missing = set(ALL_GAP_IDS) - got_gaps
    if missing:
        raise ValueError(f"M14 remediation plan: missing gap_id entries: {sorted(missing)}")
    gates = raw.get("remediation_gates")
    if not isinstance(gates, list):
        raise ValueError("M14 remediation plan: remediation_gates must be a list")
    got_gates = {str(x.get("gate_id", "")) for x in gates if isinstance(x, dict)}
    missing_g = set(ALL_REMEDIATION_GATE_IDS) - got_gates
    if missing_g:
        raise ValueError(f"M14 remediation plan: missing remediation gate_id: {sorted(missing_g)}")
    sec = raw.get("remediation_status_secondary")
    if not isinstance(sec, list) or STATUS_OPERATOR_EVIDENCE_NOT_COLLECTED not in [
        str(x) for x in sec
    ]:
        raise ValueError(
            "M14 remediation plan: remediation_status_secondary must list "
            f"{STATUS_OPERATOR_EVIDENCE_NOT_COLLECTED!r} (operator evidence not collected posture)"
        )
    af = raw.get("authorization_flags")
    if isinstance(af, dict) and af.get("v2_authorized") is True:
        raise ValueError(
            "M14 remediation plan: v2_authorized true is inconsistent with M15 preflight defaults; "
            "use a fixture-honest M14 JSON with v2_authorized false."
        )
    return raw


def _check_m13_v2_not_authorized(m13: dict[str, Any]) -> None:
    af = m13.get("authorization_flags")
    if isinstance(af, dict) and af.get("v2_authorized") is True:
        raise ValueError(
            "M13 v2 decision: v2_authorized true is inconsistent with M15 preflight defaults; "
            "bind an M13 JSON with v2_authorized false for this preflight artifact."
        )


def _gate(
    gate_id: str,
    name: str,
    default_status: str,
    notes: str,
) -> dict[str, Any]:
    return {
        "gate_id": gate_id,
        "name": name,
        "default_status": default_status,
        "notes": notes,
    }


def _build_preflight_gates(
    *,
    m13_bound: bool,
    m14_bound: bool,
) -> list[dict[str, Any]]:
    fx, ps = GATE_POSTURE_PASS_FIXTURE, GATE_POSTURE_PASS
    p0 = fx if m13_bound else fx
    p0_note = (
        "M13 no-go / defer JSON bound by canonical SHA-256 or fixture placeholder retained."
        if m13_bound
        else "Fixture placeholder: bind v15_v2_go_no_go_decision.json with --m13-v2-decision-json."
    )
    p1 = fx if m14_bound else fx
    p1_note = (
        "M14 remediation plan bound by canonical SHA-256 with required gaps and E0–E13 gates."
        if m14_bound
        else (
            "Fixture placeholder: bind v15_evidence_remediation_plan.json with "
            "--m14-remediation-plan-json."
        )
    )
    return [
        _gate(
            P0_M13_NO_GO, "M13 no-go / defer context bound or fixture placeholder used", p0, p0_note
        ),
        _gate(
            P1_M14_PLAN,
            "M14 remediation plan bound or fixture placeholder used",
            p1,
            p1_note,
        ),
        _gate(
            P2_PRIVATE_WORKSPACE,
            "Operator-private workspace convention declared",
            ps,
            "Local `out/`, optional `docs/company_secrets/` (untracked) per project policy.",
        ),
        _gate(
            P3_NO_PRIVATE_PATHS_COMMITTED,
            "Private path commit prohibition recorded",
            ps,
            "No absolute operator paths, weights, or raw media in public commits.",
        ),
        _gate(
            P4_INPUTS_INVENTORY,
            "Required input classes inventoried",
            ps,
            "evidence_sequence and required_operator_inputs enumerate acquisition classes only.",
        ),
        _gate(
            P5_RIGHTS_TOUCHPOINTS,
            "Rights/register touchpoints declared",
            ps,
            "Register list references public register docs; no new claim-critical rows in M15.",
        ),
        _gate(
            P6_M16_ENV,
            "M16 environment/short GPU inputs defined",
            ps,
            "Sequencing for short GPU / environment evidence; not execution.",
        ),
        _gate(
            P7_M17_LONG,
            "M17 long GPU inputs defined",
            ps,
            "Sequencing for long-campaign evidence; not a completed campaign claim.",
        ),
        _gate(
            P8_M18_CHECKPOINT,
            "M18 checkpoint/eval inputs defined",
            ps,
            "Sequencing for evaluation evidence; not promotion or strong-agent claim.",
        ),
        _gate(
            P9_M19_XAI,
            "M19 XAI inputs defined",
            ps,
            "Sequencing for XAI evidence; not inference or faithfulness proof.",
        ),
        _gate(
            P10_HUMAN_PANEL,
            "M20 human-panel inputs defined",
            ps,
            "Sequencing for human-benchmark evidence; not panel execution.",
        ),
        _gate(
            P11_SHOWCASE_RELEASE,
            "Showcase release-pack input expectations preserved",
            ps,
            "Release-pack vocabulary preserved from M12 class surfaces; not release authorization.",
        ),
        _gate(
            P12_V2_BLOCKED,
            "v2 remains blocked until evidence exists",
            ps,
            "v2_authorized and v2_recharter_authorized false on default and honest binding paths.",
        ),
        _gate(
            P13_NO_EXEC,
            "Preflight artifact confirms no operator execution in M15",
            ps,
            "M15 is definition and sequencing only; no GPU, SC2, or benchmark execution in emit.",
        ),
        _gate(
            P14_DOCS_TESTS,
            "Docs and governance tests aligned for M15 contract",
            ps,
            "starlab-v1.5.md, runtime doc, rights register note, and tests reference this contract.",
        ),
    ]


def _seq_row(
    sequence_id: str,
    label: str,
    future_milestone: str,
    required_inputs: list[str],
    required_registers: list[str],
    public_private_posture: str,
    default_status: str,
    blocking_reason: str,
    non_claims: str,
) -> dict[str, Any]:
    return {
        "sequence_id": sequence_id,
        "label": label,
        "future_milestone": future_milestone,
        "required_inputs": required_inputs,
        "required_registers": required_registers,
        "public_private_posture": public_private_posture,
        "default_status": default_status,
        "blocking_reason": blocking_reason,
        "non_claims": non_claims,
    }


def _build_evidence_sequence() -> list[dict[str, Any]]:
    reg = list(REGISTER_TOUCHPOINT_PATHS)
    nc = "Sequencing label only; does not assert evidence exists or milestone ran."
    return [
        _seq_row(
            S0_CONTEXT,
            "Bind M13 decision and M14 remediation plan JSON by SHA (or accept placeholders).",
            "V15-M15",
            ["m13_v2_go_no_go_decision.json", "m14_evidence_remediation_plan.json (optional)"],
            ["docs/rights_register.md"],
            "public_shas_and_contract_ids; private operator trees",
            SEQUENCE_STATUS_READY_REVIEW,
            "Complete SHA bindings for audit trail before downstream collection.",
            nc,
        ),
        _seq_row(
            S1_WORKSPACE,
            "Declare private workspace roots and .gitignore posture.",
            "V15-M16",
            ["local out/ root", "optional company_secrets path (untracked)"],
            [reg[0]],
            "private_local_only",
            SEQUENCE_STATUS_NOT_STARTED,
            "Operator must declare local roots; not evaluated in public CI.",
            nc,
        ),
        _seq_row(
            S2_ENV_SHORT,
            "M07-class short GPU / environment lock inputs and receipts (operator-local).",
            "V15-M16",
            ["M02 environment lock JSON", "M07 receipt JSON class"],
            [reg[1], reg[0]],
            "public lock summaries; private CUDA/GPU paths",
            SEQUENCE_STATUS_BLOCKED_ARTIFACTS,
            "Requires operator-local M02/M07-class artifacts.",
            nc,
        ),
        _seq_row(
            S3_TRAINING,
            "Training asset manifests, dataset rights, M01 register alignment.",
            "V15-M16",
            ["dataset manifests", "training asset register rows"],
            [reg[1], reg[2], reg[0]],
            "public register templates; private corpora",
            SEQUENCE_STATUS_BLOCKED_RIGHTS,
            "Rights and clearance review before public reference rows.",
            nc,
        ),
        _seq_row(
            S4_LONG_GPU,
            "M08 long GPU campaign manifest and receipt (operator-local).",
            "V15-M17",
            ["m08 long_gpu_training_manifest", "m08 campaign receipt"],
            [reg[1], reg[0]],
            "public SHA; private logs and trees under out/",
            SEQUENCE_STATUS_BLOCKED_UPSTREAM,
            "Blocked until M16 environment inputs and operator authorization recorded.",
            nc,
        ),
        _seq_row(
            S5_CHECKPOINT,
            "M03 checkpoint lineage, resume, interruption vocabulary (no blob reads in CI).",
            "V15-M18",
            ["lineage JSON", "checkpoint id graph"],
            [reg[4], reg[0]],
            "public hash refs; private checkpoint blobs",
            SEQUENCE_STATUS_BLOCKED_UPSTREAM,
            "Requires upstream long-run or declared lineage files.",
            nc,
        ),
        _seq_row(
            S6_EVAL,
            "M09 evaluation and promotion decision JSON (governance metadata only).",
            "V15-M18",
            ["m09 checkpoint evaluation", "m05 scorecard protocol bind"],
            [reg[4], reg[0]],
            "public JSON summaries; no performance claim from metadata alone",
            SEQUENCE_STATUS_BLOCKED_UPSTREAM,
            "Requires promoted-candidate class inputs when non-fixture.",
            nc,
        ),
        _seq_row(
            S7_XAI,
            "M04 XAI pack and M10 demonstration bindings (no inference in emit).",
            "V15-M19",
            ["m04 xai pack JSON", "m10 demonstration JSON"],
            [reg[5], reg[0]],
            "public contract rows; private saliency tensors and media",
            SEQUENCE_STATUS_BLOCKED_UPSTREAM,
            "Requires promoted candidate or declared XAI class evidence.",
            nc,
        ),
        _seq_row(
            S8_HUMAN,
            "M11 human panel execution and claim-decision JSON (protocol + privacy).",
            "V15-M20",
            ["m11 execution JSON", "m06 protocol bind"],
            [reg[6], reg[0]],
            "public protocol; private participant rosters",
            SEQUENCE_STATUS_BLOCKED_UPSTREAM,
            "Requires protocol, rights, and participant preflight before execution milestone.",
            nc,
        ),
        _seq_row(
            S9_SHOWCASE,
            "M12 showcase release pack inputs and upstream SHA closure.",
            "V15-M20",
            ["m12 release pack JSON"],
            [reg[0]],
            "public pack metadata; private weights and videos",
            SEQUENCE_STATUS_BLOCKED_UPSTREAM,
            "Requires upstream M08–M11 evidence class inputs when claiming release posture.",
            nc,
        ),
        _seq_row(
            S10_V2,
            "M13 / M21 style v2 reconsideration with governed evidence package.",
            "V15-M21",
            ["m13 decision JSON with real upstream bindings", "m14 remediation plan current"],
            [reg[0]],
            "public decision metadata; private evidence bundles",
            SEQUENCE_STATUS_NOT_APPLICABLE,
            "v2 reconsideration blocked until M16–M20 evidence or explicit defer recorded.",
            nc,
        ),
    ]


def _future_milestone_map() -> list[dict[str, Any]]:
    return [
        {
            "milestone": "V15-M16",
            "purpose": "Short GPU / environment evidence collection",
            "m15_posture": "blocked until M15 preflight gates pass",
        },
        {
            "milestone": "V15-M17",
            "purpose": "Long GPU campaign evidence collection",
            "m15_posture": "blocked until M16 and required inputs pass",
        },
        {
            "milestone": "V15-M18",
            "purpose": "Candidate checkpoint evaluation evidence collection",
            "m15_posture": "blocked until long-run / checkpoint evidence exists",
        },
        {
            "milestone": "V15-M19",
            "purpose": "XAI evidence collection and validation",
            "m15_posture": "blocked until promoted candidate or declared candidate evidence exists",
        },
        {
            "milestone": "V15-M20",
            "purpose": "Human / bounded human benchmark evidence collection",
            "m15_posture": "blocked until candidate, protocol, rights, and participant preflight pass",
        },
        {
            "milestone": "V15-M21",
            "purpose": "v2 reconsideration decision",
            "m15_posture": "blocked until M16–M20 evidence is present or explicitly deferred",
        },
    ]


def _public_private_boundary() -> dict[str, Any]:
    return {
        "public_safe": [
            "contract_ids",
            "sha256_bindings",
            "logical_artifact_names",
            "milestone_ids",
            "gate_ids",
            "redacted_operator_path_conventions",
            "register_names",
            "non_claims",
        ],
        "private_local_only": [
            "absolute_paths",
            "sc2_client_paths",
            "map_pack_locations",
            "replay_files",
            "model_weights",
            "checkpoint_blobs",
            "saliency_tensors",
            "videos",
            "human_participant_identities",
            "consent_records",
            "session_notes",
            "private_operator_notes",
            "local_training_logs",
            "raw_campaign_trees_under_out",
        ],
    }


def _required_operator_inputs() -> list[dict[str, Any]]:
    return [
        {
            "input_id": "IN_m13_v2_decision_json",
            "description": "Optional M13 v2 go/no-go decision JSON for SHA binding",
            "default_posture": "fixture_placeholder_or_file",
        },
        {
            "input_id": "IN_m14_remediation_plan_json",
            "description": "Optional M14 evidence remediation plan JSON for SHA binding",
            "default_posture": "fixture_placeholder_or_file",
        },
        {
            "input_id": "IN_local_out_root",
            "description": "Operator-declared output root (local, not committed)",
            "default_posture": "private_local_only",
        },
    ]


def _operator_instructions() -> list[str]:
    return [
        "Emit default fixture: python -m starlab.v15.emit_v15_operator_evidence_collection_preflight "
        + "--output-dir <path> (no operator files required).",
        "Optionally pass --m13-v2-decision-json and --m14-remediation-plan-json for real SHA bindings.",
        "Do not commit private paths, weights, replays, or participant data; use registers for clearance.",
    ]


def _m13_binding_placeholder() -> dict[str, Any]:
    return {
        "binding_mode": "fixture_placeholder",
        "m13_v2_decision_json_canonical_sha256": PLACEHOLDER_SHA256,
        "note": "Supply --m13-v2-decision-json to bind real M13 JSON (starlab.v15.v2_go_no_go_decision.v1).",
    }


def _m14_binding_placeholder() -> dict[str, Any]:
    return {
        "binding_mode": "fixture_placeholder",
        "m14_remediation_plan_json_canonical_sha256": PLACEHOLDER_SHA256,
        "note": "Supply --m14-remediation-plan-json to bind real M14 JSON "
        f"({CONTRACT_ID_EVIDENCE_REMEDIATION_PLAN}).",
    }


def _m13_binding_file(path: Path) -> dict[str, Any]:
    m13 = parse_m13_v2_decision(path)
    _check_m13_v2_not_authorized(m13)
    sha = _json_file_canonical_sha256(path)
    ro = m13.get("decision_outcome", "")
    return {
        "binding_mode": "file_bound",
        "m13_v2_decision_json_canonical_sha256": sha,
        "m13_contract_id_readonly": str(m13.get("contract_id", "")),
        "m13_decision_outcome_readonly": str(ro) if ro is not None else "",
    }


def _m14_binding_file(path: Path) -> dict[str, Any]:
    m14 = parse_m14_remediation_plan(path)
    sha = _json_file_canonical_sha256(path)
    return {
        "binding_mode": "file_bound",
        "m14_remediation_plan_json_canonical_sha256": sha,
        "m14_remediation_status_primary_readonly": str(m14.get("remediation_status_primary", "")),
        "m14_operator_evidence_not_collected_readonly": True,
    }


def build_operator_evidence_preflight_body(
    *,
    m13_path: Path | None,
    m14_path: Path | None,
) -> dict[str, Any]:
    """Build preflight body; optional M13/M14 paths bound once each."""
    m13_bound = m13_path is not None
    m14_bound = m14_path is not None
    profile = PROFILE_WITH_M13_M14_BINDINGS if (m13_bound or m14_bound) else PROFILE_FIXTURE_CI
    m13b = _m13_binding_file(m13_path) if m13_path else _m13_binding_placeholder()
    m14b = _m14_binding_file(m14_path) if m14_path else _m14_binding_placeholder()
    return {
        "contract_id": CONTRACT_ID_OPERATOR_EVIDENCE_COLLECTION_PREFLIGHT,
        "milestone": MILESTONE_ID_V15_M15,
        "emitter_module": EMITTER_MODULE_OPERATOR_EVIDENCE_PREFLIGHT,
        "emit_profile": profile,
        "preflight_status": PREFLIGHT_STATUS_PLAN_READY,
        "operator_evidence_collection_status": STATUS_OPERATOR_EVIDENCE_NOT_STARTED,
        "v2_authorized": False,
        "v2_recharter_authorized": False,
        "m13_binding": m13b,
        "m14_binding": m14b,
        "evidence_sequence": _build_evidence_sequence(),
        "preflight_gates": _build_preflight_gates(m13_bound=m13_bound, m14_bound=m14_bound),
        "required_operator_inputs": _required_operator_inputs(),
        "future_milestone_map": _future_milestone_map(),
        "register_touchpoints": [{"register_doc": p} for p in REGISTER_TOUCHPOINT_PATHS],
        "public_private_boundary": _public_private_boundary(),
        "non_claims": [NON_CLAIMS_V15_M15],
        "operator_instructions": _operator_instructions(),
    }


def seal_operator_evidence_preflight_body(body: dict[str, Any]) -> dict[str, Any]:
    base = {k: v for k, v in body.items() if k != _SEAL}
    digest = sha256_hex_of_canonical_json(base)
    sealed = dict(base)
    sealed[_SEAL] = digest
    return sealed


def build_operator_evidence_preflight_report(sealed: dict[str, Any]) -> dict[str, Any]:
    base = {k: v for k, v in sealed.items() if k != _SEAL}
    digest = sha256_hex_of_canonical_json(base)
    return {
        "report_kind": "v15_operator_evidence_collection_preflight_report",
        "report_version": REPORT_VERSION_OPERATOR_EVIDENCE_PREFLIGHT,
        "milestone": MILESTONE_ID_V15_M15,
        "artifact_sha256": digest,
        "seal_field": _SEAL,
        "seal_value_matches_artifact": sealed.get(_SEAL) == digest,
        "primary_filename": FILENAME_OPERATOR_EVIDENCE_COLLECTION_PREFLIGHT,
        "checklist_markdown": FILENAME_OPERATOR_EVIDENCE_COLLECTION_CHECKLIST_MD,
    }


def render_operator_evidence_checklist_md(sealed: dict[str, Any]) -> str:
    lines: list[str] = [
        "# V15-M15 — Operator evidence collection (preflight checklist)",
        "",
        "This checklist is a **governance / sequencing** artifact. It does **not** assert that "
        "operator evidence was collected or that downstream milestones ran.",
        "",
        "## Emitted JSON summary",
        "",
        f"- Contract: `{sealed.get('contract_id', '')}`",
        f"- Preflight status: `{sealed.get('preflight_status', '')}`",
        f"- Operator evidence collection: `{sealed.get('operator_evidence_collection_status', '')}`",
        f"- v2 authorized: {sealed.get('v2_authorized')!s} (must remain false on honest default path)",
        "",
        "## M13 / M14 bindings (SHA posture)",
        "",
    ]
    m13b = sealed.get("m13_binding")
    m14b = sealed.get("m14_binding")
    if isinstance(m13b, dict):
        lines.append(
            f"- M13: `{m13b.get('binding_mode', '')}` | SHA: `{m13b.get('m13_v2_decision_json_canonical_sha256', '')[:16]}…`"
        )
    if isinstance(m14b, dict):
        lines.append(
            f"- M14: `{m14b.get('binding_mode', '')}` | SHA: `{m14b.get('m14_remediation_plan_json_canonical_sha256', '')[:16]}…`"
        )
    lines.extend(
        [
            "",
            "## Preflight gates (P0–P14)",
            "",
        ]
    )
    gates = sealed.get("preflight_gates")
    if isinstance(gates, list):
        for g in gates:
            if isinstance(g, dict):
                lines.append(
                    f"- **{g.get('gate_id', '')}** — {g.get('name', '')} "
                    f"(`{g.get('default_status', '')}`)"
                )
    lines.extend(["", "## Evidence sequence (S0–S10)", ""])
    seq = sealed.get("evidence_sequence")
    if isinstance(seq, list):
        for s in seq:
            if isinstance(s, dict):
                lines.append(
                    f"- **{s.get('sequence_id', '')}** — {s.get('label', '')} → `{s.get('future_milestone', '')}`"
                )
    lines.extend(
        [
            "",
            "## Non-claims",
            "",
        ]
    )
    nc = sealed.get("non_claims")
    if isinstance(nc, list):
        for item in nc:
            lines.append(f"- {item}")
    text = "\n".join(lines) + "\n"
    low = text.lower()
    for bad in FORBIDDEN_CHECKLIST_SUBSTRINGS:
        if bad in low:
            raise ValueError(f"checklist would contain forbidden phrase: {bad!r}")
    return text


def emit_v15_operator_evidence_collection_preflight(
    output_dir: Path,
    *,
    m13_path: Path | None = None,
    m14_path: Path | None = None,
) -> tuple[dict[str, Any], dict[str, Any], Path, Path, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    body = build_operator_evidence_preflight_body(
        m13_path=m13_path,
        m14_path=m14_path,
    )
    sealed = seal_operator_evidence_preflight_body(body)
    report = build_operator_evidence_preflight_report(sealed)
    md = render_operator_evidence_checklist_md(sealed)
    pj = output_dir / FILENAME_OPERATOR_EVIDENCE_COLLECTION_PREFLIGHT
    pr = output_dir / REPORT_FILENAME_OPERATOR_EVIDENCE_COLLECTION_PREFLIGHT
    pm = output_dir / FILENAME_OPERATOR_EVIDENCE_COLLECTION_CHECKLIST_MD
    pj.write_text(canonical_json_dumps(sealed), encoding="utf-8", newline="\n")
    pr.write_text(canonical_json_dumps(report), encoding="utf-8", newline="\n")
    pm.write_text(md, encoding="utf-8", newline="\n")
    return sealed, report, pj, pr, pm


__all__ = [
    "build_operator_evidence_preflight_body",
    "build_operator_evidence_preflight_report",
    "emit_v15_operator_evidence_collection_preflight",
    "parse_m14_remediation_plan",
    "render_operator_evidence_checklist_md",
    "seal_operator_evidence_preflight_body",
]
