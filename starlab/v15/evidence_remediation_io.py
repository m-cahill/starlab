"""Build, seal, and write V15-M14 evidence remediation plan JSON + report + runbook."""

# ruff: noqa: E501

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Final

from starlab.runs.json_util import canonical_json_dumps, sha256_hex_of_canonical_json
from starlab.v15.evidence_remediation_models import (
    CONTRACT_ID_EVIDENCE_REMEDIATION_PLAN,
    CONTRACT_VERSION,
    E0_M13_DECISION_CONTEXT,
    E1_EVIDENCE_GAPS_ENUMERATED,
    E2_OPERATOR_PRIVATE_PATHS,
    E3_LONG_GPU_EVIDENCE_REQ,
    E4_CHECKPOINT_LINEAGE_REQ,
    E5_PROMOTION_EVAL_REQ,
    E6_XAI_EVIDENCE_REQ,
    E7_HUMAN_BENCHMARK_REQ,
    E8_RIGHTS_REGISTER_TOUCHPOINTS,
    E9_PUBLIC_PRIVATE_BOUNDARY,
    E10_PROPOSED_ROADMAP,
    E11_V2_REMAINS_UNAUTHORIZED,
    E12_NO_FABRICATED_EVIDENCE,
    E13_DOCS_GOVERNANCE_ALIGNED,
    EMITTER_MODULE_EVIDENCE_REMEDIATION,
    FILENAME_EVIDENCE_REMEDIATION_PLAN,
    FILENAME_OPERATOR_RUNBOOK_MD,
    FIXTURE_REMEDIATION_PLAN_ID,
    FORBIDDEN_RUNBOOK_SUBSTRINGS,
    GATE_STATUS_PASS,
    GATE_STATUS_WARNING,
    MILESTONE_ID_V15_M14,
    NON_CLAIMS_V15_M14,
    PLACEHOLDER_SHA256,
    PROFILE_FIXTURE_CI,
    PROFILE_ID_EVIDENCE_REMEDIATION_PLAN,
    PROFILE_WITH_M13_BINDING,
    PROPOSED_M15_M21,
    REPORT_FILENAME_EVIDENCE_REMEDIATION_PLAN,
    REPORT_VERSION_EVIDENCE_REMEDIATION,
    SEAL_KEY_EVIDENCE_REMEDIATION_PLAN,
    STATUS_EVIDENCE_GAP_INVENTORY_ONLY,
    STATUS_OPERATOR_EVIDENCE_NOT_COLLECTED,
    STATUS_REMEDIATION_PLAN_READY,
    default_m14_authorization_flags,
)
from starlab.v15.human_panel_benchmark_io import redact_path_and_contact_in_value
from starlab.v15.training_run_receipt_io import _redaction_token_count, redact_receipt_value
from starlab.v15.v2_decision_models import CONTRACT_ID_V2_GO_NO_GO_DECISION

_SEAL = SEAL_KEY_EVIDENCE_REMEDIATION_PLAN


def _redact_body_for_emit(body: dict[str, Any]) -> tuple[dict[str, Any], int]:
    red = redact_receipt_value(redact_path_and_contact_in_value(body))
    if not isinstance(red, dict):
        return body, 0
    return red, _redaction_token_count(red)


GAP_ROWS_SPEC: Final[
    list[
        tuple[
            str,
            str,
            str,
            str,
            str,
        ]
    ]
] = [
    (
        "GAP-01-long-gpu-run-receipt",
        "open",
        "Governed long GPU campaign receipt (M08-class) with manifests and stop/resume records.",
        "Collect under operator-local `out/` or declared campaign root; bind JSON by SHA in downstream milestones.",
        "V15-M17",
    ),
    (
        "GAP-02-checkpoint-lineage",
        "open",
        "Checkpoint lineage graph with parent/child ids and environment/dataset hash references (M03-class).",
        "Emit/refresh `v15_checkpoint_lineage_manifest` from operator tree; no blob reads in public CI.",
        "V15-M16",
    ),
    (
        "GAP-03-promoted-checkpoint",
        "open",
        "Promoted candidate checkpoint with evaluation and promotion decision tied to M05/M09 gates.",
        "Operator-local evaluation; promotion decision JSON bound by SHA; no default promotion in CI.",
        "V15-M18",
    ),
    (
        "GAP-04-training-scale-provenance",
        "open",
        "Training-scale provenance: dataset, rights, environment lock, training asset registers consistent.",
        "Refresh M01/M02/M07/M08 receipts and registers before claiming training-scale completeness.",
        "V15-M16",
    ),
    (
        "GAP-05-strong-agent-benchmark",
        "open",
        "Executed strong-agent scorecard / benchmark ladder (not protocol-only).",
        "Run declared ladder under M05 protocol; store results in governed JSON; no live SC2 in default CI.",
        "V15-M18",
    ),
    (
        "GAP-06-replay-native-xai-pack",
        "open",
        "Real replay-native XAI evidence packs (inference and reporting under M04/M10 contracts).",
        "Operator-local XAI pipeline; bind packs by SHA; no faithfulness claim by default.",
        "V15-M19",
    ),
    (
        "GAP-07-human-benchmark-evidence",
        "open",
        "Human panel execution and bounded human-benchmark claim decision under M06/M11 rules.",
        "Operator-local panel; private participant data; claim decision JSON only after execution.",
        "V15-M20",
    ),
    (
        "GAP-08-showcase-release-evidence",
        "open",
        "Showcase agent release pack with upstream SHA bindings and authorization flags (M12-class).",
        "Assemble only after upstream gaps close; no default public release rows.",
        "V15-M20",
    ),
    (
        "GAP-09-v2-readiness-evidence",
        "open",
        "Consolidated v1.5 evidence package sufficient for M13/M21-style reconsideration, not a v2 claim.",
        "Follow proposed M15–M20 sequence; re-run decision surfaces with real bindings.",
        "V15-M21",
    ),
    (
        "GAP-10-rights-and-asset-clearance",
        "open",
        "Rights and register review for weights, replays, video, and participant materials.",
        "Update private notes and public registers per project policy; no uncleared public commits.",
        "V15-M15+",
    ),
]


def _row(gate_id: str, status: str, notes: str) -> dict[str, Any]:
    return {"gate_id": gate_id, "status": status, "notes": notes}


def _json_file_canonical_sha256(path: Path) -> str:
    raw = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ValueError("JSON must be a single object")
    return sha256_hex_of_canonical_json(raw)


def parse_m13_v2_decision(path: Path) -> dict[str, Any]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ValueError("M13 JSON must be a single object")
    cid = str(raw.get("contract_id", ""))
    if cid != CONTRACT_ID_V2_GO_NO_GO_DECISION:
        raise ValueError(
            f"M13 v2 decision: contract_id must be {CONTRACT_ID_V2_GO_NO_GO_DECISION!r} (got {cid!r})"
        )
    return raw


def build_evidence_gap_inventory() -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for gap_id, status, missing, path_text, owner in GAP_ROWS_SPEC:
        out.append(
            {
                "gap_id": gap_id,
                "status": status,
                "missing_evidence": missing,
                "proposed_acquisition_path": path_text,
                "proposed_remediation_milestone": owner,
                "non_claim_reminder": (
                    "This gap entry is an inventory label only; it does not assert that the evidence exists "
                    "or that the milestone has run."
                ),
            }
        )
    return out


def _remediation_gates(
    *,
    m13_bound: bool,
) -> list[dict[str, Any]]:
    gp, gw = GATE_STATUS_PASS, GATE_STATUS_WARNING
    e0 = gp if m13_bound else gw
    e0_note = (
        "M13 v2 go/no-go JSON bound by canonical SHA-256; no-go context recorded."
        if m13_bound
        else "M13 decision JSON not supplied; use --m13-v2-decision-json to bind a sealed decision."
    )
    return [
        _row(E0_M13_DECISION_CONTEXT, e0, e0_note),
        _row(
            E1_EVIDENCE_GAPS_ENUMERATED,
            gp,
            "Ten governed gap ids enumerated with proposed milestones.",
        ),
        _row(
            E2_OPERATOR_PRIVATE_PATHS,
            gp,
            "Acquisition paths are operator-local (`out/`, private notes); not merge-gate execution.",
        ),
        _row(
            E3_LONG_GPU_EVIDENCE_REQ,
            gp,
            "Long GPU receipt requirements reference M08 runtime; evidence not collected in M14.",
        ),
        _row(
            E4_CHECKPOINT_LINEAGE_REQ,
            gp,
            "Lineage and resume vocabulary declared (M03); no checkpoint blob verification in M14.",
        ),
        _row(
            E5_PROMOTION_EVAL_REQ,
            gp,
            "Evaluation and promotion evidence requirements declared (M09); not executed in M14.",
        ),
        _row(
            E6_XAI_EVIDENCE_REQ,
            gp,
            "XAI pack requirements declared (M04/M10); no XAI inference in M14.",
        ),
        _row(
            E7_HUMAN_BENCHMARK_REQ,
            gp,
            "Human-benchmark evidence requirements declared (M06/M11); no panel execution in M14.",
        ),
        _row(
            E8_RIGHTS_REGISTER_TOUCHPOINTS,
            gp,
            "Rights and asset registers are touchpoints; M14 does not add claim-critical public rows by default.",
        ),
        _row(
            E9_PUBLIC_PRIVATE_BOUNDARY,
            gp,
            "Redaction and SHA-only public bindings; no raw paths or private notes in emitted JSON.",
        ),
        _row(
            E10_PROPOSED_ROADMAP,
            gp,
            "Proposed V15-M15–M21 labels recorded as follow-ons; not started unless separately approved.",
        ),
        _row(
            E11_V2_REMAINS_UNAUTHORIZED,
            gp,
            "M14 program posture: v2_authorized false; M13 no-go on default public path is preserved in scope.",
        ),
        _row(
            E12_NO_FABRICATED_EVIDENCE,
            gp,
            "No synthetic campaign receipt, promotion, or benchmark results are emitted as real evidence.",
        ),
        _row(
            E13_DOCS_GOVERNANCE_ALIGNED,
            gw,
            "Runtime and starlab-v1.5.md updated in this milestone; CI governance tests enforce pointers.",
        ),
    ]


def build_evidence_remediation_body_fixture() -> dict[str, Any]:
    af = default_m14_authorization_flags()
    return {
        "contract_id": CONTRACT_ID_EVIDENCE_REMEDIATION_PLAN,
        "contract_version": CONTRACT_VERSION,
        "milestone_id": MILESTONE_ID_V15_M14,
        "profile_id": PROFILE_ID_EVIDENCE_REMEDIATION_PLAN,
        "emit_profile": PROFILE_FIXTURE_CI,
        "emitter_module": EMITTER_MODULE_EVIDENCE_REMEDIATION,
        "remediation_plan_id": FIXTURE_REMEDIATION_PLAN_ID,
        "remediation_status_primary": STATUS_EVIDENCE_GAP_INVENTORY_ONLY,
        "remediation_status_secondary": [
            STATUS_OPERATOR_EVIDENCE_NOT_COLLECTED,
            STATUS_REMEDIATION_PLAN_READY,
        ],
        "m13_v2_decision_json_canonical_sha256": PLACEHOLDER_SHA256,
        "m13_decision_context": {
            "m13_file_bound": False,
            "m13_recommended_next_step": "bind_m13_json_for_audit_trail",
        },
        "proposed_roadmap_m15_m21": [
            {
                "milestone_id": mid,
                "title": title,
                "status": st,
            }
            for mid, title, st in PROPOSED_M15_M21
        ],
        "evidence_gap_inventory": build_evidence_gap_inventory(),
        "remediation_gates": _remediation_gates(m13_bound=False),
        "non_claims": [NON_CLAIMS_V15_M14],
        "authorization_flags": af,
    }


def build_evidence_remediation_body_with_m13(m13_path: Path) -> dict[str, Any]:
    m13 = parse_m13_v2_decision(m13_path)
    m13_sha = _json_file_canonical_sha256(m13_path)
    af_m13 = m13.get("authorization_flags")
    v2_readonly = None
    if isinstance(af_m13, dict):
        v2_readonly = bool(af_m13.get("v2_authorized", False))
    rec = str(m13.get("recommended_next_step", ""))
    outcome = str(m13.get("decision_outcome", ""))
    body = build_evidence_remediation_body_fixture()
    body["emit_profile"] = PROFILE_WITH_M13_BINDING
    body["remediation_plan_id"] = f"v15_m14:m13_bound:{m13_sha[:16]}"
    body["m13_v2_decision_json_canonical_sha256"] = m13_sha
    body["m13_decision_context"] = {
        "m13_file_bound": True,
        "m13_decision_outcome_readonly": outcome,
        "m13_recommended_next_step_readonly": rec,
        "m13_v2_authorized_readonly": v2_readonly,
        "note": (
            "Readonly fields are copied from the bound M13 JSON for traceability. "
            "M14 authorization_flags remain false; M14 does not re-authorize v2."
        ),
    }
    body["remediation_gates"] = _remediation_gates(m13_bound=True)
    return body


def seal_evidence_remediation_body(body: dict[str, Any]) -> dict[str, Any]:
    base = {k: v for k, v in body.items() if k != _SEAL}
    digest = sha256_hex_of_canonical_json(base)
    sealed = dict(base)
    sealed[_SEAL] = digest
    return sealed


def build_evidence_remediation_report(
    sealed: dict[str, Any], *, redaction_count: int
) -> dict[str, Any]:
    base = {k: v for k, v in sealed.items() if k != _SEAL}
    digest = sha256_hex_of_canonical_json(base)
    return {
        "report_kind": "v15_evidence_remediation_plan_report",
        "report_version": REPORT_VERSION_EVIDENCE_REMEDIATION,
        "milestone": MILESTONE_ID_V15_M14,
        "artifact_sha256": digest,
        "seal_field": _SEAL,
        "seal_value_matches_artifact": sealed.get(_SEAL) == digest,
        "redaction_events": int(redaction_count),
        "primary_filename": FILENAME_EVIDENCE_REMEDIATION_PLAN,
        "operator_runbook_markdown": FILENAME_OPERATOR_RUNBOOK_MD,
    }


def render_operator_runbook_md(sealed: dict[str, Any]) -> str:
    intro = (
        "# V15 Operator Evidence Acquisition Runbook\n\n"
        "This remediation runbook documents evidence still required after M13’s default no-go / defer decision.\n"
        "It does not execute training, GPU campaigns, or authorize v2.\n"
    )
    m13c = sealed.get("m13_decision_context")
    m13_block = "## M13 no-go summary\n\n"
    if isinstance(m13c, dict) and m13c.get("m13_file_bound"):
        m13_block += (
            f"- M13 decision outcome (readonly): `{m13c.get('m13_decision_outcome_readonly', '')}`\n"
            f"- Recommended next step (readonly): `{m13c.get('m13_recommended_next_step_readonly', '')}`\n"
        )
    else:
        m13_block += (
            "- Default public record: v2 not authorized; collect operator evidence before re-evaluation.\n"
            "- Bind `v15_v2_go_no_go_decision.json` with `--m13-v2-decision-json` for SHA traceability.\n"
        )
    gaps = sealed.get("evidence_gap_inventory")
    g_lines: list[str] = ["\n## Evidence gaps\n"]
    if isinstance(gaps, list):
        for g in gaps:
            if isinstance(g, dict):
                g_lines.append(
                    f"- **{g.get('gap_id', '')}** — {g.get('missing_evidence', '')} "
                    f"(proposed owner: {g.get('proposed_remediation_milestone', '')})\n"
                )
    road = sealed.get("proposed_roadmap_m15_m21")
    r_lines: list[str] = ["\n## Proposed follow-on milestones (not started)\n"]
    if isinstance(road, list):
        for row in road:
            if isinstance(row, dict):
                r_lines.append(
                    f"- `{row.get('milestone_id', '')}` — {row.get('title', '')} — **{row.get('status', '')}**\n"
                )
    rest = [
        "\n## Recommended evidence collection sequence\n",
        "1. Preflight and environment evidence (M15–M16).\n",
        "2. Long GPU campaign receipt and lineage (M17).\n",
        "3. Checkpoint evaluation and strong-agent benchmark execution (M18).\n",
        "4. XAI evidence (M19).\n",
        "5. Human / bounded human benchmark (M20).\n",
        "6. Showcase and v2 reconsideration (M20–M21)\n",
        "\n## Operator-local / private artifact locations\n",
        "- Typical roots: `out/`, local `docs/company_secrets/` (untracked), external archives for weights.\n",
        "- Do not commit raw weights, replays, or participant data to the public repo.\n",
        "\n## Public/private boundary\n",
        "- Public: contract ids, gate ids, gap ids, SHA-256, proposed roadmap, non-claims.\n",
        "- Private: absolute paths, credentials, rosters, uncleared media.\n",
        "\n## Rights and register review\n",
        "- Future evidence must be reviewed against `docs/rights_register.md` and asset registers before claims.\n",
        "\n## Exit criteria for re-running a v2 / evidence decision (M13/M21 class)\n",
        "- Governed upstream JSONs exist with real SHA bindings, not placeholders, where claims require it.\n",
        "\n## Non-claims\n",
    ]
    nc = sealed.get("non_claims")
    n_lines: list[str] = []
    if isinstance(nc, list):
        for item in nc:
            n_lines.append(f"- {item}\n")
    text = (
        intro
        + m13_block
        + "".join(g_lines)
        + "".join(r_lines)
        + "".join(rest)
        + "".join(n_lines)
        + "\n"
    )
    low = text.lower()
    for bad in FORBIDDEN_RUNBOOK_SUBSTRINGS:
        if bad in low:
            raise ValueError(f"runbook would contain forbidden phrase: {bad!r}")
    return text


def emit_v15_evidence_remediation_plan_fixture(
    output_dir: Path,
) -> tuple[dict[str, Any], dict[str, Any], Path, Path, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    body = build_evidence_remediation_body_fixture()
    sealed = seal_evidence_remediation_body(body)
    report = build_evidence_remediation_report(sealed, redaction_count=0)
    md = render_operator_runbook_md(sealed)
    pj = output_dir / FILENAME_EVIDENCE_REMEDIATION_PLAN
    pr = output_dir / REPORT_FILENAME_EVIDENCE_REMEDIATION_PLAN
    pm = output_dir / FILENAME_OPERATOR_RUNBOOK_MD
    pj.write_text(canonical_json_dumps(sealed), encoding="utf-8", newline="\n")
    pr.write_text(canonical_json_dumps(report), encoding="utf-8", newline="\n")
    pm.write_text(md, encoding="utf-8", newline="\n")
    return sealed, report, pj, pr, pm


def emit_v15_evidence_remediation_plan_with_m13(
    output_dir: Path,
    m13_path: Path,
) -> tuple[dict[str, Any], dict[str, Any], Path, Path, Path]:
    body = build_evidence_remediation_body_with_m13(m13_path)
    red_body, rc = _redact_body_for_emit(body)
    sealed = seal_evidence_remediation_body(red_body)
    report = build_evidence_remediation_report(sealed, redaction_count=rc)
    md = render_operator_runbook_md(sealed)
    output_dir.mkdir(parents=True, exist_ok=True)
    pj = output_dir / FILENAME_EVIDENCE_REMEDIATION_PLAN
    pr = output_dir / REPORT_FILENAME_EVIDENCE_REMEDIATION_PLAN
    pm = output_dir / FILENAME_OPERATOR_RUNBOOK_MD
    pj.write_text(canonical_json_dumps(sealed), encoding="utf-8", newline="\n")
    pr.write_text(canonical_json_dumps(report), encoding="utf-8", newline="\n")
    pm.write_text(md, encoding="utf-8", newline="\n")
    return sealed, report, pj, pr, pm


__all__ = [
    "build_evidence_gap_inventory",
    "build_evidence_remediation_body_fixture",
    "build_evidence_remediation_body_with_m13",
    "build_evidence_remediation_report",
    "emit_v15_evidence_remediation_plan_fixture",
    "emit_v15_evidence_remediation_plan_with_m13",
    "parse_m13_v2_decision",
    "render_operator_runbook_md",
    "seal_evidence_remediation_body",
    "GAP_ROWS_SPEC",
]
