"""CLI: emit evaluation_diagnostics.json and evaluation_diagnostics_report.json (M24)."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

from starlab.evaluation.diagnostics_models import (
    EVALUATION_DIAGNOSTICS_FILENAME,
    EVALUATION_DIAGNOSTICS_REPORT_FILENAME,
)
from starlab.evaluation.diagnostics_views import build_derived_views, load_tournament_json
from starlab.runs.json_util import canonical_json_dumps


def build_evaluation_diagnostics_artifacts(
    tournament: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Build diagnostics + report dicts from a loaded M23 tournament object."""

    return build_derived_views(tournament)


def write_evaluation_diagnostics_artifacts(
    *,
    tournament_path: Path,
    output_dir: Path,
) -> tuple[Path, Path]:
    """Write diagnostics + report under ``output_dir``; return written paths."""

    tournament = load_tournament_json(tournament_path)
    diagnostics, report = build_derived_views(tournament)
    output_dir.mkdir(parents=True, exist_ok=True)
    p_d = output_dir / EVALUATION_DIAGNOSTICS_FILENAME
    p_r = output_dir / EVALUATION_DIAGNOSTICS_REPORT_FILENAME
    p_d.write_text(canonical_json_dumps(diagnostics), encoding="utf-8")
    p_r.write_text(canonical_json_dumps(report), encoding="utf-8")
    return p_d, p_r


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="python -m starlab.evaluation.emit_evaluation_diagnostics",
        description=(
            "Emit evaluation_diagnostics.json and evaluation_diagnostics_report.json "
            "from one governed evaluation_tournament.json (M23)."
        ),
    )
    parser.add_argument(
        "--tournament",
        required=True,
        type=Path,
        help="Path to evaluation_tournament.json",
    )
    parser.add_argument(
        "--output-dir",
        required=True,
        type=Path,
        help="Directory for diagnostics + report JSON outputs",
    )
    args = parser.parse_args(argv)

    try:
        write_evaluation_diagnostics_artifacts(
            tournament_path=args.tournament,
            output_dir=args.output_dir,
        )
    except (OSError, TypeError, ValueError) as exc:
        print(str(exc), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
