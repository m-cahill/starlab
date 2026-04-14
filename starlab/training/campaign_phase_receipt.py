"""M51: per-phase receipts for governed campaign execution."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Final

from starlab.runs.json_util import canonical_json_dumps

CAMPAIGN_PHASE_RECEIPT_VERSION: Final[str] = "starlab.campaign_phase_receipt.v1"
PHASE_RECEIPT_FILENAME: Final[str] = "phase_receipt.json"


def build_phase_receipt(
    *,
    phase_name: str,
    phase_order_index: int,
    phase_kind: str,
    requested: bool,
    eligible: bool,
    executed: bool,
    final_status: str,
    reason_codes: list[str],
    warnings: list[str],
    input_artifact_refs: dict[str, Any],
    output_artifact_refs: dict[str, Any],
    resume_posture: str,
    stop_boundary_reached: bool,
) -> dict[str, Any]:
    """Deterministic phase receipt body (also aggregated into hidden_rollout_campaign_run)."""

    return {
        "campaign_phase_receipt_version": CAMPAIGN_PHASE_RECEIPT_VERSION,
        "eligible": eligible,
        "executed": executed,
        "final_status": final_status,
        "input_artifact_refs": dict(input_artifact_refs),
        "output_artifact_refs": dict(output_artifact_refs),
        "phase_kind": phase_kind,
        "phase_name": phase_name,
        "phase_order_index": int(phase_order_index),
        "reason_codes": list(reason_codes),
        "requested": requested,
        "resume_posture": resume_posture,
        "stop_boundary_reached": stop_boundary_reached,
        "warnings": list(warnings),
    }


def write_phase_receipt(*, phase_output_dir: Path, receipt: dict[str, Any]) -> Path:
    phase_output_dir.mkdir(parents=True, exist_ok=True)
    path = phase_output_dir / PHASE_RECEIPT_FILENAME
    path.write_text(canonical_json_dumps(receipt), encoding="utf-8")
    return path
