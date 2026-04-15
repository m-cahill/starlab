"""CLI: emit `benchmark_integrity_charter.json` + report (M55)."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from starlab.benchmark_integrity.benchmark_integrity_charter import (
    benchmark_integrity_charter_bundle,
)
from starlab.benchmark_integrity.benchmark_integrity_models import (
    CHARTER_FILENAME,
    CHARTER_REPORT_FILENAME,
)
from starlab.runs.json_util import canonical_json_dumps


def write_benchmark_integrity_charter_artifacts(output_dir: Path) -> tuple[Path, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    charter, report = benchmark_integrity_charter_bundle()
    charter_path = output_dir / CHARTER_FILENAME
    report_path = output_dir / CHARTER_REPORT_FILENAME
    charter_path.write_text(canonical_json_dumps(charter), encoding="utf-8")
    report_path.write_text(canonical_json_dumps(report), encoding="utf-8")
    return charter_path, report_path


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(
        description="Emit deterministic benchmark integrity charter JSON (M55 — charter only)."
    )
    p.add_argument(
        "--output-dir",
        type=Path,
        default=Path("."),
        help="Directory for charter + report JSON (default: cwd).",
    )
    args = p.parse_args(argv)
    c, r = write_benchmark_integrity_charter_artifacts(args.output_dir)
    print(f"Wrote {c}")
    print(f"Wrote {r}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
