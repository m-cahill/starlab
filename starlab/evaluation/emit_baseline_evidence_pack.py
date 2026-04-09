"""CLI: emit baseline_evidence_pack.json and baseline_evidence_pack_report.json (M25)."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from starlab.evaluation.evidence_pack_models import (
    BASELINE_EVIDENCE_PACK_FILENAME,
    BASELINE_EVIDENCE_PACK_REPORT_FILENAME,
)
from starlab.evaluation.evidence_pack_views import build_baseline_evidence_pack_artifacts
from starlab.runs.json_util import canonical_json_dumps


def write_baseline_evidence_pack_artifacts(
    *,
    suite_paths: list[Path],
    tournament_path: Path,
    diagnostics_path: Path,
    output_dir: Path,
) -> tuple[Path, Path]:
    """Write pack + report under ``output_dir``; return written paths."""

    pack, report = build_baseline_evidence_pack_artifacts(
        suite_paths=suite_paths,
        tournament_path=tournament_path,
        diagnostics_path=diagnostics_path,
    )
    output_dir.mkdir(parents=True, exist_ok=True)
    p_pack = output_dir / BASELINE_EVIDENCE_PACK_FILENAME
    p_rep = output_dir / BASELINE_EVIDENCE_PACK_REPORT_FILENAME
    p_pack.write_text(canonical_json_dumps(pack), encoding="utf-8")
    p_rep.write_text(canonical_json_dumps(report), encoding="utf-8")
    return p_pack, p_rep


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="python -m starlab.evaluation.emit_baseline_evidence_pack",
        description=(
            "Emit baseline_evidence_pack.json and baseline_evidence_pack_report.json "
            "from governed M21/M22 suites + M23 tournament + M24 diagnostics (M25)."
        ),
    )
    parser.add_argument(
        "--suite",
        action="append",
        dest="suites",
        required=True,
        metavar="PATH",
        type=Path,
        help="Path to scripted_baseline_suite.json or heuristic_baseline_suite.json (repeatable)",
    )
    parser.add_argument(
        "--tournament",
        required=True,
        type=Path,
        help="Path to evaluation_tournament.json",
    )
    parser.add_argument(
        "--diagnostics",
        required=True,
        type=Path,
        help="Path to evaluation_diagnostics.json",
    )
    parser.add_argument(
        "--output-dir",
        required=True,
        type=Path,
        help="Directory for pack + report JSON outputs",
    )
    args = parser.parse_args(argv)

    try:
        write_baseline_evidence_pack_artifacts(
            suite_paths=args.suites,
            tournament_path=args.tournament,
            diagnostics_path=args.diagnostics,
            output_dir=args.output_dir,
        )
    except (OSError, TypeError, ValueError) as exc:
        print(str(exc), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
