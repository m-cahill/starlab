"""CLI: emit benchmark_integrity_evidence.json + report (M56)."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from starlab.benchmark_integrity.benchmark_integrity_evidence import (
    benchmark_integrity_evidence_bundle,
)
from starlab.benchmark_integrity.benchmark_integrity_models import (
    EVIDENCE_FILENAME,
    EVIDENCE_REPORT_FILENAME,
    M56_SCOPE_FIXTURE_ONLY_BASELINE_CHAIN_V1,
)
from starlab.runs.json_util import canonical_json_dumps


def write_benchmark_integrity_evidence_artifacts(
    *,
    scope_id: str,
    output_dir: Path,
    scripted_baseline_suite: Path,
    heuristic_baseline_suite: Path,
    evaluation_tournament: Path,
    evaluation_diagnostics: Path,
    baseline_evidence_pack: Path,
) -> tuple[Path, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    evidence, report = benchmark_integrity_evidence_bundle(
        scope_id=scope_id,
        scripted_baseline_suite_path=scripted_baseline_suite,
        heuristic_baseline_suite_path=heuristic_baseline_suite,
        evaluation_tournament_path=evaluation_tournament,
        evaluation_diagnostics_path=evaluation_diagnostics,
        baseline_evidence_pack_path=baseline_evidence_pack,
    )
    ev_path = output_dir / EVIDENCE_FILENAME
    rep_path = output_dir / EVIDENCE_REPORT_FILENAME
    ev_path.write_text(canonical_json_dumps(evidence), encoding="utf-8")
    rep_path.write_text(canonical_json_dumps(report), encoding="utf-8")
    return ev_path, rep_path


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(
        description=(
            "Emit deterministic benchmark_integrity_evidence.json + report for M56 bounded scope."
        )
    )
    p.add_argument(
        "--scope-id",
        default=M56_SCOPE_FIXTURE_ONLY_BASELINE_CHAIN_V1,
        help="Benchmark integrity scope id (default: fixture-only baseline chain v1).",
    )
    p.add_argument("--output-dir", type=Path, default=Path("."), help="Output directory.")
    p.add_argument(
        "--scripted-baseline-suite",
        type=Path,
        required=True,
        help="Path to scripted_baseline_suite.json (M21).",
    )
    p.add_argument(
        "--heuristic-baseline-suite",
        type=Path,
        required=True,
        help="Path to heuristic_baseline_suite.json (M22).",
    )
    p.add_argument(
        "--evaluation-tournament",
        type=Path,
        required=True,
        help="Path to evaluation_tournament.json (M23).",
    )
    p.add_argument(
        "--evaluation-diagnostics",
        type=Path,
        required=True,
        help="Path to evaluation_diagnostics.json (M24).",
    )
    p.add_argument(
        "--baseline-evidence-pack",
        type=Path,
        required=True,
        help="Path to baseline_evidence_pack.json (M25).",
    )
    args = p.parse_args(argv)
    try:
        ev, rep = write_benchmark_integrity_evidence_artifacts(
            baseline_evidence_pack=args.baseline_evidence_pack,
            evaluation_diagnostics=args.evaluation_diagnostics,
            evaluation_tournament=args.evaluation_tournament,
            heuristic_baseline_suite=args.heuristic_baseline_suite,
            output_dir=args.output_dir,
            scope_id=args.scope_id,
            scripted_baseline_suite=args.scripted_baseline_suite,
        )
    except (OSError, TypeError, ValueError) as exc:
        print(str(exc), file=sys.stderr)
        return 1
    print(f"Wrote {ev}")
    print(f"Wrote {rep}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
