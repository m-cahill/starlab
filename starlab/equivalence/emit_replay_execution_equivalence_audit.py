"""CLI: emit replay_execution_equivalence_audit.json + report (M54)."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

from starlab.equivalence.equivalence_audit import (
    build_replay_execution_equivalence_audit_bundle,
    load_evidence_object,
    load_evidence_report_object,
)
from starlab.equivalence.equivalence_models import AUDIT_FILENAME, AUDIT_REPORT_FILENAME
from starlab.runs.json_util import canonical_json_dumps


def write_replay_execution_equivalence_audit_artifacts(
    *,
    evidence_path: Path,
    evidence_report_path: Path | None,
    output_dir: Path,
) -> tuple[Path, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    evidence = load_evidence_object(evidence_path)
    report: dict[str, Any] | None = None
    if evidence_report_path is not None:
        report = load_evidence_report_object(evidence_report_path)
    audit, audit_report = build_replay_execution_equivalence_audit_bundle(
        evidence=evidence,
        evidence_report=report,
    )
    a_path = output_dir / AUDIT_FILENAME
    r_path = output_dir / AUDIT_REPORT_FILENAME
    a_path.write_text(canonical_json_dumps(audit), encoding="utf-8")
    r_path.write_text(canonical_json_dumps(audit_report), encoding="utf-8")
    return a_path, r_path


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(
        description=(
            "Emit deterministic replay-vs-execution equivalence audit JSON over M53 evidence (M54)."
        )
    )
    p.add_argument(
        "--evidence",
        type=Path,
        required=True,
        help="Path to replay_execution_equivalence_evidence.json (M53).",
    )
    p.add_argument(
        "--evidence-report",
        type=Path,
        default=None,
        help=(
            "Optional path to replay_execution_equivalence_evidence_report.json "
            "for SHA cross-check."
        ),
    )
    p.add_argument(
        "--output-dir",
        type=Path,
        default=Path("."),
        help="Directory for audit + audit report JSON.",
    )
    args = p.parse_args(argv)
    ev, rep = write_replay_execution_equivalence_audit_artifacts(
        evidence_path=args.evidence,
        evidence_report_path=args.evidence_report,
        output_dir=args.output_dir,
    )
    print(f"Wrote {ev}")
    print(f"Wrote {rep}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
