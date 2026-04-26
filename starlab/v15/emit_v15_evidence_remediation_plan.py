"""CLI: emit v15_evidence_remediation_plan.json + report + operator runbook (V15-M14)."""

from __future__ import annotations

import argparse
from pathlib import Path

from starlab.v15.evidence_remediation_io import (
    emit_v15_evidence_remediation_plan_fixture,
    emit_v15_evidence_remediation_plan_with_m13,
)
from starlab.v15.evidence_remediation_models import SEAL_KEY_EVIDENCE_REMEDIATION_PLAN

_SEAL = SEAL_KEY_EVIDENCE_REMEDIATION_PLAN


def _must_file(p: Path, label: str) -> Path:
    if not p.is_file():
        raise SystemExit(f"error: {label} must be an existing file ({p})")
    return p


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Emit v1.5 evidence remediation plan JSON, report, and Markdown runbook (V15-M14). "
            "Planning only; no GPU, SC2, benchmarks, or XAI. "
            "Optional M13 v2 go/no-go JSON bound by SHA-256."
        ),
    )
    parser.add_argument(
        "--output-dir",
        required=True,
        type=Path,
        help="Directory for plan JSON, report JSON, and Markdown runbook",
    )
    parser.add_argument(
        "--m13-v2-decision-json",
        type=Path,
        default=None,
        help=(
            "Optional: path to v15_v2_go_no_go_decision.json (contract "
            "starlab.v15.v2_go_no_go_decision.v1) for SHA binding and readonly context"
        ),
    )
    args = parser.parse_args(argv)
    if args.m13_v2_decision_json is not None:
        p = _must_file(args.m13_v2_decision_json, "--m13-v2-decision-json")
        sealed, _rep, p_j, p_r, p_m = emit_v15_evidence_remediation_plan_with_m13(
            args.output_dir, p
        )
        print(f"wrote {p_j}", flush=True)
        print(f"wrote {p_r}", flush=True)
        print(f"wrote {p_m}", flush=True)
        print(f"{_SEAL}={sealed.get(_SEAL, '')}", flush=True)
        return 0
    sealed, _rep, p_j, p_r, p_m = emit_v15_evidence_remediation_plan_fixture(args.output_dir)
    print(f"wrote {p_j}", flush=True)
    print(f"wrote {p_r}", flush=True)
    print(f"wrote {p_m}", flush=True)
    print(f"{_SEAL}={sealed.get(_SEAL, '')}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
