"""CLI: emit scripted_baseline_suite.json and scripted_baseline_suite_report.json (M21)."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from starlab.baselines.scripted_baseline_models import (
    SCRIPTED_BASELINE_SUITE_FILENAME,
    SCRIPTED_BASELINE_SUITE_REPORT_FILENAME,
)
from starlab.baselines.scripted_baseline_suite import build_scripted_baseline_suite_and_report
from starlab.runs.json_util import canonical_json_dumps


def _load_benchmark_contract(path: Path) -> dict[str, Any]:
    raw = path.read_text(encoding="utf-8")
    try:
        obj: Any = json.loads(raw)
    except json.JSONDecodeError as exc:
        msg = f"invalid JSON in benchmark contract: {exc}"
        raise ValueError(msg) from exc
    if not isinstance(obj, dict):
        msg = "benchmark contract must be a JSON object"
        raise TypeError(msg)
    return obj


def write_scripted_baseline_suite_artifacts(
    *,
    benchmark_contract_path: Path,
    output_dir: Path,
) -> tuple[Path, Path]:
    """Write suite + report under ``output_dir``; return written paths."""

    contract = _load_benchmark_contract(benchmark_contract_path)
    suite, report = build_scripted_baseline_suite_and_report(contract)

    output_dir.mkdir(parents=True, exist_ok=True)
    p_suite = output_dir / SCRIPTED_BASELINE_SUITE_FILENAME
    p_report = output_dir / SCRIPTED_BASELINE_SUITE_REPORT_FILENAME
    p_suite.write_text(canonical_json_dumps(suite), encoding="utf-8")
    p_report.write_text(canonical_json_dumps(report), encoding="utf-8")
    return p_suite, p_report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="python -m starlab.baselines.emit_scripted_baseline_suite",
        description=(
            "Emit scripted_baseline_suite.json and scripted_baseline_suite_report.json "
            "from one M20 benchmark contract (fixture_only)."
        ),
    )
    parser.add_argument(
        "--benchmark-contract",
        required=True,
        type=Path,
        help="Path to benchmark contract JSON",
    )
    parser.add_argument(
        "--output-dir",
        required=True,
        type=Path,
        help="Directory for suite + report JSON outputs",
    )
    args = parser.parse_args(argv)

    try:
        write_scripted_baseline_suite_artifacts(
            benchmark_contract_path=args.benchmark_contract,
            output_dir=args.output_dir,
        )
    except (OSError, TypeError, ValueError) as exc:
        print(str(exc), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
