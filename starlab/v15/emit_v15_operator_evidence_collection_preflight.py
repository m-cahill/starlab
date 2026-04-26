"""CLI: emit v15 operator evidence collection preflight JSON + report + checklist (V15-M15)."""

from __future__ import annotations

import argparse
from pathlib import Path

from starlab.v15.operator_evidence_preflight_io import (
    emit_v15_operator_evidence_collection_preflight,
)
from starlab.v15.operator_evidence_preflight_models import SEAL_KEY_ARTIFACT

_SEAL = SEAL_KEY_ARTIFACT


def _must_file(p: Path, label: str) -> Path:
    if not p.is_file():
        raise SystemExit(f"error: {label} must be an existing file ({p})")
    return p


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Emit v1.5 operator evidence collection preflight JSON, report, and Markdown checklist "
            "(V15-M15). Preflight and sequencing only; no GPU, SC2, or evidence collection. "
            "Optional M13 / M14 JSON for SHA-256 binding."
        ),
    )
    parser.add_argument(
        "--output-dir",
        required=True,
        type=Path,
        help="Directory for preflight JSON, report JSON, and checklist Markdown",
    )
    parser.add_argument(
        "--m13-v2-decision-json",
        type=Path,
        default=None,
        help=(
            "Optional: v15_v2_go_no_go_decision.json ("
            "starlab.v15.v2_go_no_go_decision.v1) for SHA binding; v2_authorized must be false"
        ),
    )
    parser.add_argument(
        "--m14-remediation-plan-json",
        type=Path,
        default=None,
        help=(
            "Optional: v15_evidence_remediation_plan.json "
            "(starlab.v15.evidence_remediation_plan.v1); SHA binding; M14 gap/gate set required"
        ),
    )
    args = parser.parse_args(argv)
    m13 = (
        _must_file(args.m13_v2_decision_json, "--m13-v2-decision-json")
        if args.m13_v2_decision_json
        else None
    )
    m14 = (
        _must_file(args.m14_remediation_plan_json, "--m14-remediation-plan-json")
        if args.m14_remediation_plan_json
        else None
    )
    sealed, _rep, p_j, p_r, p_m = emit_v15_operator_evidence_collection_preflight(
        args.output_dir, m13_path=m13, m14_path=m14
    )
    print(f"wrote {p_j}", flush=True)
    print(f"wrote {p_r}", flush=True)
    print(f"wrote {p_m}", flush=True)
    print(f"{_SEAL}={sealed.get(_SEAL, '')}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
