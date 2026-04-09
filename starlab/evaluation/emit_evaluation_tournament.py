"""CLI: emit evaluation_tournament.json and evaluation_tournament_report.json (M23)."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

from starlab.evaluation.evaluation_runner import prepare_runner_inputs, suite_path_for_artifact
from starlab.evaluation.evaluation_runner_models import (
    EVALUATION_TOURNAMENT_FILENAME,
    EVALUATION_TOURNAMENT_ID,
    EVALUATION_TOURNAMENT_NON_CLAIMS_V1,
    EVALUATION_TOURNAMENT_REPORT_FILENAME,
    EVALUATION_TOURNAMENT_REPORT_VERSION,
    EVALUATION_TOURNAMENT_VERSION,
    EVALUATION_TOURNAMENT_WARNINGS_V1,
)
from starlab.evaluation.tournament_harness import (
    collect_scorecards_by_entrant,
    run_round_robin_tournament,
)
from starlab.runs.json_util import canonical_json_dumps


def build_evaluation_tournament_artifacts(
    *,
    benchmark_contract_path: Path,
    suite_paths: list[Path],
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Build tournament + report dicts."""

    benchmark_contract, bench_sha, suites, meta, entrants = prepare_runner_inputs(
        benchmark_contract_path=benchmark_contract_path,
        suite_paths=suite_paths,
    )

    scorecards_by_entrant = collect_scorecards_by_entrant(suites, entrants)
    matches, standings = run_round_robin_tournament(
        benchmark_contract=benchmark_contract,
        entrants=entrants,
        scorecards_by_entrant=scorecards_by_entrant,
    )

    suite_inputs: list[dict[str, Any]] = []
    for suite, (path, sha256) in zip(suites, meta, strict=True):
        suite_inputs.append(
            {
                "suite_id": suite["suite_id"],
                "suite_path": suite_path_for_artifact(path),
                "suite_sha256": sha256,
                "suite_version": suite["suite_version"],
            },
        )

    warnings = sorted(EVALUATION_TOURNAMENT_WARNINGS_V1)
    non_claims = sorted(EVALUATION_TOURNAMENT_NON_CLAIMS_V1)

    tournament: dict[str, Any] = {
        "benchmark_contract_sha256": bench_sha,
        "benchmark_id": benchmark_contract["benchmark_id"],
        "entrants": entrants,
        "evaluation_posture": "fixture_only",
        "matches": matches,
        "measurement_surface": "fixture_only",
        "non_claims": non_claims,
        "standings": standings,
        "suite_inputs": suite_inputs,
        "tournament_id": EVALUATION_TOURNAMENT_ID,
        "tournament_version": EVALUATION_TOURNAMENT_VERSION,
        "warnings": warnings,
    }

    report: dict[str, Any] = {
        "benchmark_contract_sha256": bench_sha,
        "entrant_count": len(entrants),
        "failures": [],
        "match_count": len(matches),
        "non_claims": non_claims,
        "report_version": EVALUATION_TOURNAMENT_REPORT_VERSION,
        "suite_count": len(suites),
        "tournament_verdict": "pass",
        "warnings": warnings,
    }

    return tournament, report


def write_evaluation_tournament_artifacts(
    *,
    benchmark_contract_path: Path,
    suite_paths: list[Path],
    output_dir: Path,
) -> tuple[Path, Path]:
    """Write tournament + report under ``output_dir``; return written paths."""

    tournament, report = build_evaluation_tournament_artifacts(
        benchmark_contract_path=benchmark_contract_path,
        suite_paths=suite_paths,
    )
    output_dir.mkdir(parents=True, exist_ok=True)
    p_t = output_dir / EVALUATION_TOURNAMENT_FILENAME
    p_r = output_dir / EVALUATION_TOURNAMENT_REPORT_FILENAME
    p_t.write_text(canonical_json_dumps(tournament), encoding="utf-8")
    p_r.write_text(canonical_json_dumps(report), encoding="utf-8")
    return p_t, p_r


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="python -m starlab.evaluation.emit_evaluation_tournament",
        description=(
            "Emit evaluation_tournament.json and evaluation_tournament_report.json "
            "from one M20 benchmark contract and one or more M21/M22 suite artifacts."
        ),
    )
    parser.add_argument(
        "--benchmark-contract",
        required=True,
        type=Path,
        help="Path to benchmark contract JSON",
    )
    parser.add_argument(
        "--suite",
        action="append",
        required=True,
        dest="suites",
        type=Path,
        help="Path to a baseline suite JSON (repeatable; order is preserved)",
    )
    parser.add_argument(
        "--output-dir",
        required=True,
        type=Path,
        help="Directory for tournament + report JSON outputs",
    )
    args = parser.parse_args(argv)

    try:
        write_evaluation_tournament_artifacts(
            benchmark_contract_path=args.benchmark_contract,
            suite_paths=list(args.suites),
            output_dir=args.output_dir,
        )
    except (OSError, TypeError, ValueError) as exc:
        print(str(exc), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
