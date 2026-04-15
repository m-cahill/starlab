"""CLI: emit benchmark_integrity_reproducibility_gates.json + report (M56)."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

from starlab.benchmark_integrity.benchmark_integrity_gate_evaluation import (
    build_benchmark_integrity_reproducibility_gates_bundle,
    load_evidence_object,
    load_evidence_report_object,
)
from starlab.benchmark_integrity.benchmark_integrity_models import (
    REPRODUCIBILITY_GATES_FILENAME,
    REPRODUCIBILITY_GATES_REPORT_FILENAME,
)
from starlab.runs.json_util import canonical_json_dumps


def write_benchmark_integrity_gates_artifacts(
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
    gates, gates_report = build_benchmark_integrity_reproducibility_gates_bundle(
        evidence=evidence,
        evidence_report=report,
    )
    g_path = output_dir / REPRODUCIBILITY_GATES_FILENAME
    r_path = output_dir / REPRODUCIBILITY_GATES_REPORT_FILENAME
    g_path.write_text(canonical_json_dumps(gates), encoding="utf-8")
    r_path.write_text(canonical_json_dumps(gates_report), encoding="utf-8")
    return g_path, r_path


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(
        description=(
            "Emit reproducibility gates JSON + report over M56 benchmark integrity evidence."
        ),
    )
    p.add_argument(
        "--evidence",
        type=Path,
        required=True,
        help="Path to benchmark_integrity_evidence.json",
    )
    p.add_argument(
        "--evidence-report",
        type=Path,
        default=None,
        help="Optional path to benchmark_integrity_evidence_report.json for SHA cross-check.",
    )
    p.add_argument("--output-dir", type=Path, default=Path("."), help="Output directory.")
    args = p.parse_args(argv)
    try:
        gp, rp = write_benchmark_integrity_gates_artifacts(
            evidence_path=args.evidence,
            evidence_report_path=args.evidence_report,
            output_dir=args.output_dir,
        )
    except (OSError, TypeError, ValueError) as exc:
        print(str(exc), file=sys.stderr)
        return 1
    print(f"Wrote {gp}")
    print(f"Wrote {rp}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
