"""Deterministic PV1 post-campaign comparative readout (PV1-M04, aggregation-only)."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any, Final

from starlab.runs.json_util import canonical_json_dumps, sha256_hex_of_canonical_json
from starlab.training.pv1_campaign_observability_views import build_campaign_observability_index

PV1_POST_CAMPAIGN_READOUT_VERSION: Final[str] = "starlab.pv1_post_campaign_readout.v1"
PV1_POST_CAMPAIGN_READOUT_REPORT_VERSION: Final[str] = "starlab.pv1_post_campaign_readout_report.v1"

PV1_POST_CAMPAIGN_READOUT_FILENAME: Final[str] = "pv1_post_campaign_readout.json"
PV1_POST_CAMPAIGN_READOUT_REPORT_FILENAME: Final[str] = "pv1_post_campaign_readout_report.json"

TRANCHE_A_OPERATOR_NOTE: Final[str] = "tranche_a_operator_note.md"
TRANCHE_B_OPERATOR_NOTE: Final[str] = "tranche_b_operator_note.md"
THRESHOLD_DECLARATION: Final[str] = "full_run_threshold_declaration.md"

PV1_POST_CAMPAIGN_READOUT_NON_CLAIMS_V1: Final[tuple[str, ...]] = (
    "benchmark_integrity_global",
    "does_not_add_new_execution_evidence",
    "does_not_reinterpret_threshold_fields",
    "ladder_or_public_strength",
    "live_sc2_in_ci_as_default_merge_norm",
    "multi_environment_readiness",
    "replay_execution_equivalence_universal",
    "universal_replay_execution_equivalence",
)

_THRESHOLD_HEADING_RE = re.compile(
    r"###\s+\*\*`(threshold-not-met|threshold-met)`\*\*",
    re.IGNORECASE | re.MULTILINE,
)
_EXEC_ID_ROW_RE = re.compile(
    r"\|\s*`execution_id`\s*\|\s*`([^`]+)`\s*\|",
    re.MULTILINE,
)
_POSTURE_LINE_RE = re.compile(
    r"\*\*Posture:\*\*\s*(.+)$",
    re.MULTILINE | re.IGNORECASE,
)


def _rel(root: Path, p: Path | None) -> str | None:
    if p is None:
        return None
    try:
        return p.relative_to(root.resolve()).as_posix()
    except ValueError:
        return None


def _read_optional(path: Path) -> str | None:
    if not path.is_file():
        return None
    return path.read_text(encoding="utf-8")


def _parse_execution_id(note_body: str | None) -> str | None:
    if not note_body:
        return None
    m = _EXEC_ID_ROW_RE.search(note_body)
    return m.group(1).strip() if m else None


def _parse_posture_line(note_body: str | None) -> str | None:
    if not note_body:
        return None
    m = _POSTURE_LINE_RE.search(note_body)
    return m.group(1).strip() if m else None


def _normalize_tranche_posture(raw: str | None) -> str:
    if not raw:
        return "unknown"
    lower = raw.lower()
    if "completed within" in lower or "within scope" in lower or "within declared scope" in lower:
        return "completed_within_scope"
    if "not completed" in lower or "incomplete" in lower:
        return "not_completed_within_scope"
    return "unknown"


def _parse_threshold_posture(decl_body: str | None) -> tuple[str | None, list[str], list[str]]:
    """Return (threshold_posture, unmet_fields, parse_warnings)."""

    warnings: list[str] = []
    if not decl_body:
        return None, [], ["full_run_threshold_declaration.md missing or unreadable"]

    m = _THRESHOLD_HEADING_RE.search(decl_body)
    if not m:
        warnings.append(
            "threshold declaration: no ### `threshold-not-met` / `threshold-met` heading found"
        )
        return None, [], warnings

    posture = m.group(1).strip().lower()
    if posture not in ("threshold-not-met", "threshold-met"):
        return None, [], warnings + [f"unexpected threshold token: {posture!r}"]

    unmet: list[str] = []
    if posture == "threshold-not-met":
        # Honest bounded default: list duration target only when the declaration discusses it.
        txt = decl_body.lower()
        if "full_run_duration_target" in txt or "duration target" in txt:
            unmet.append("full_run_duration_target")
        else:
            warnings.append(
                "threshold-not-met declared but full_run_duration_target not mentioned in text — "
                "unmet fields list left empty"
            )

    return posture, unmet, warnings


def _checkpoint_ref_for(
    refs: list[str],
    substring: str,
) -> str | None:
    for r in refs:
        if substring in r.replace("\\", "/"):
            return r
    return None


def _execution_hidden_run_rel(root: Path, execution_id: str) -> str | None:
    p = root / "campaign_runs" / execution_id / "hidden_rollout_campaign_run.json"
    if p.is_file():
        return _rel(root, p)
    return None


def build_pv1_post_campaign_readout(
    *,
    campaign_root: Path,
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Aggregate observability index + on-disk operator/threshold markdown into readout JSON pair.

    Does not execute SC2 or campaigns. Missing files reduce completeness; see report warnings.
    """

    root = campaign_root
    if not root.is_dir():
        raise ValueError(f"campaign root is not a directory: {root}")

    index_body, index_report = build_campaign_observability_index(campaign_root=root)
    scan = index_body.get("index_scan") or {}
    ck_refs: list[str] = list(index_body.get("checkpoint_receipt_refs") or [])

    a_note_path = root / TRANCHE_A_OPERATOR_NOTE
    b_note_path = root / TRANCHE_B_OPERATOR_NOTE
    decl_path = root / THRESHOLD_DECLARATION

    a_note = _read_optional(a_note_path)
    b_note = _read_optional(b_note_path)
    decl = _read_optional(decl_path)

    exec_a = _parse_execution_id(a_note)
    exec_b = _parse_execution_id(b_note)
    posture_a = _normalize_tranche_posture(_parse_posture_line(a_note))
    posture_b = _normalize_tranche_posture(_parse_posture_line(b_note))

    threshold_posture, threshold_unmet, decl_warnings = _parse_threshold_posture(decl)

    warnings: list[str] = list(decl_warnings)
    contract_rel = scan.get("campaign_contract_rel")
    preflight_rel = scan.get("preflight_receipt_rel")

    ck_a = _checkpoint_ref_for(ck_refs, "tranche_a_close")
    ck_b = _checkpoint_ref_for(ck_refs, "tranche_b_close")

    exec_a_ref = _execution_hidden_run_rel(root, exec_a) if exec_a else None
    exec_b_ref = _execution_hidden_run_rel(root, exec_b) if exec_b else None
    if exec_a and exec_a_ref is None:
        warnings.append(
            f"Tranche A execution_id {exec_a!r}: hidden_rollout_campaign_run.json not found"
        )
    if exec_b and exec_b_ref is None:
        warnings.append(
            f"Tranche B execution_id {exec_b!r}: hidden_rollout_campaign_run.json not found"
        )

    idx_status = str(
        index_report.get("index_status") or index_body.get("index_status") or "unknown"
    )
    summary = index_report.get("summary") or {}
    if idx_status == "complete" and a_note and b_note and decl and threshold_posture:
        ev_complete = "complete"
    elif idx_status != "complete":
        ev_complete = "incomplete_observability"
    else:
        ev_complete = "incomplete_operator_or_threshold_docs"

    campaign_id = str(index_body.get("campaign_id") or root.name)

    tuple_parts = [
        f"tranche_a:{posture_a}",
        f"tranche_b:{posture_b}",
        f"threshold:{threshold_posture or 'unknown'}",
    ]
    summary_line = (
        f"PV1 campaign {campaign_id}: "
        f"Tranche A {posture_a}; Tranche B {posture_b}; "
        f"full-run threshold {threshold_posture or 'unknown'}"
    )

    body_wo: dict[str, Any] = {
        "artifact_kind": "pv1_post_campaign_readout",
        "bounded_lessons": [],
        "campaign_contract_ref": contract_rel,
        "campaign_id": campaign_id,
        "campaign_preflight_ref": preflight_rel,
        "campaign_result_summary": {
            "components": {
                "threshold_posture": threshold_posture,
                "tranche_a_posture": posture_a,
                "tranche_b_posture": posture_b,
            },
            "summary_line": summary_line,
            "tuple": tuple_parts,
        },
        "campaign_root": index_body.get("campaign_root"),
        "comparative_evidence_summary": {
            "campaign_observability_index_status": idx_status,
            "checkpoint_receipt_count": int(summary.get("checkpoint_receipt_count") or 0),
            "evidence_completeness_status": ev_complete,
            "execution_count": int(summary.get("execution_count") or 0),
            "watchable_validation_count": int(summary.get("watchable_validation_count") or 0),
        },
        "follow_on_questions": [],
        "non_claims": list(PV1_POST_CAMPAIGN_READOUT_NON_CLAIMS_V1),
        "operator_summary": {
            "final_operator_decision_trail": [
                TRANCHE_A_OPERATOR_NOTE,
                TRANCHE_B_OPERATOR_NOTE,
                THRESHOLD_DECLARATION,
            ],
            "threshold_declaration_ref": THRESHOLD_DECLARATION if decl else None,
            "tranche_a_operator_note_ref": TRANCHE_A_OPERATOR_NOTE if a_note else None,
            "tranche_b_operator_note_ref": TRANCHE_B_OPERATOR_NOTE if b_note else None,
        },
        "product_filenames": {
            "pv1_post_campaign_readout": PV1_POST_CAMPAIGN_READOUT_FILENAME,
            "pv1_post_campaign_readout_report": PV1_POST_CAMPAIGN_READOUT_REPORT_FILENAME,
        },
        "readout_version": PV1_POST_CAMPAIGN_READOUT_VERSION,
        "threshold_declaration_ref": THRESHOLD_DECLARATION if decl else None,
        "threshold_posture": threshold_posture,
        "threshold_unmet_fields": list(threshold_unmet),
        "tranche_a_checkpoint_ref": ck_a,
        "tranche_a_execution_ref": exec_a_ref,
        "tranche_a_operator_note_ref": TRANCHE_A_OPERATOR_NOTE if a_note else None,
        "tranche_a_posture": posture_a,
        "tranche_b_checkpoint_ref": ck_b,
        "tranche_b_execution_ref": exec_b_ref,
        "tranche_b_operator_note_ref": TRANCHE_B_OPERATOR_NOTE if b_note else None,
        "tranche_b_posture": posture_b,
    }
    digest = sha256_hex_of_canonical_json(body_wo)
    readout = {
        **body_wo,
        "readout_sha256": digest,
    }

    report = {
        "artifact_kind": "pv1_post_campaign_readout_report",
        "non_claims": list(PV1_POST_CAMPAIGN_READOUT_NON_CLAIMS_V1),
        "readout_sha256": digest,
        "readout_version": PV1_POST_CAMPAIGN_READOUT_VERSION,
        "report_version": PV1_POST_CAMPAIGN_READOUT_REPORT_VERSION,
        "summary": {
            "campaign_id": campaign_id,
            "threshold_posture": threshold_posture,
            "warnings": sorted(set(warnings)),
        },
    }
    return readout, report


def write_pv1_post_campaign_readout_artifacts(
    *,
    campaign_root: Path,
    output_dir: Path,
) -> tuple[Path, Path]:
    readout, report = build_pv1_post_campaign_readout(campaign_root=campaign_root)
    output_dir.mkdir(parents=True, exist_ok=True)
    p1 = output_dir / PV1_POST_CAMPAIGN_READOUT_FILENAME
    p2 = output_dir / PV1_POST_CAMPAIGN_READOUT_REPORT_FILENAME
    p1.write_text(canonical_json_dumps(readout), encoding="utf-8")
    p2.write_text(canonical_json_dumps(report), encoding="utf-8")
    return p1, p2
