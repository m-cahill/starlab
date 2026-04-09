"""CLI: emit benchmark + scorecard JSON Schemas and companion reports (M20)."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

from starlab.benchmarks.benchmark_contract_models import (
    BENCHMARK_CONTRACT_SCHEMA_FILENAME,
    BENCHMARK_CONTRACT_SCHEMA_REPORT_FILENAME,
    BENCHMARK_SCORECARD_SCHEMA_FILENAME,
    BENCHMARK_SCORECARD_SCHEMA_REPORT_FILENAME,
)
from starlab.benchmarks.benchmark_contract_schema import (
    build_benchmark_contract_json_schema,
    build_benchmark_contract_schema_report,
)
from starlab.benchmarks.benchmark_scorecard_schema import (
    build_benchmark_scorecard_json_schema,
    build_benchmark_scorecard_schema_report,
)
from starlab.runs.json_util import canonical_json_dumps


def _default_fixture_dir() -> Path:
    return Path(__file__).resolve().parent.parent.parent / "tests" / "fixtures" / "m20"


def _optional_example_fixtures() -> dict[str, Path]:
    d = _default_fixture_dir()
    mapping = {
        "valid_benchmark_contract": d / "valid_benchmark_contract.json",
        "invalid_benchmark_contract": d / "invalid_benchmark_contract.json",
        "valid_benchmark_scorecard": d / "valid_benchmark_scorecard.json",
        "invalid_benchmark_scorecard": d / "invalid_benchmark_scorecard.json",
    }
    return {k: v for k, v in mapping.items() if v.is_file()}


def _assert_valid_json_schema(schema: dict[str, Any], label: str) -> None:
    Draft202012Validator.check_schema(schema)


def write_benchmark_contract_artifacts(
    output_dir: Path,
    *,
    example_fixture_paths: dict[str, Path] | None = None,
) -> tuple[Path, Path, Path, Path]:
    """Write four deterministic JSON files under ``output_dir``."""

    output_dir.mkdir(parents=True, exist_ok=True)

    contract_schema = build_benchmark_contract_json_schema()
    scorecard_schema = build_benchmark_scorecard_json_schema()
    _assert_valid_json_schema(contract_schema, "benchmark_contract")
    _assert_valid_json_schema(scorecard_schema, "benchmark_scorecard")

    if example_fixture_paths is not None:
        fixtures = example_fixture_paths
    else:
        fixtures = _optional_example_fixtures()

    contract_report = build_benchmark_contract_schema_report(
        schema_obj=contract_schema,
        example_fixture_paths={
            k: v
            for k, v in fixtures.items()
            if k in ("valid_benchmark_contract", "invalid_benchmark_contract")
        }
        or None,
    )
    scorecard_report = build_benchmark_scorecard_schema_report(
        schema_obj=scorecard_schema,
        example_fixture_paths={
            k: v
            for k, v in fixtures.items()
            if k in ("valid_benchmark_scorecard", "invalid_benchmark_scorecard")
        }
        or None,
    )

    p1 = output_dir / BENCHMARK_CONTRACT_SCHEMA_FILENAME
    p2 = output_dir / BENCHMARK_CONTRACT_SCHEMA_REPORT_FILENAME
    p3 = output_dir / BENCHMARK_SCORECARD_SCHEMA_FILENAME
    p4 = output_dir / BENCHMARK_SCORECARD_SCHEMA_REPORT_FILENAME

    p1.write_text(canonical_json_dumps(contract_schema), encoding="utf-8")
    p2.write_text(canonical_json_dumps(contract_report), encoding="utf-8")
    p3.write_text(canonical_json_dumps(scorecard_schema), encoding="utf-8")
    p4.write_text(canonical_json_dumps(scorecard_report), encoding="utf-8")

    return p1, p2, p3, p4


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="python -m starlab.benchmarks.emit_benchmark_contracts",
        description=(
            "Emit benchmark_contract_schema.json, benchmark_contract_schema_report.json, "
            "benchmark_scorecard_schema.json, and benchmark_scorecard_schema_report.json."
        ),
    )
    parser.add_argument(
        "--output-dir",
        required=True,
        type=Path,
        help="Directory for the four JSON outputs",
    )
    args = parser.parse_args(argv)

    try:
        write_benchmark_contract_artifacts(args.output_dir)
    except (OSError, ValueError) as exc:
        print(str(exc), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
