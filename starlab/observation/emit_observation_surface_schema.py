"""CLI: emit observation_surface_schema.json + observation_surface_schema_report.json (M17)."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from starlab.observation.observation_surface_io import write_observation_surface_schema_artifacts


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="python -m starlab.observation.emit_observation_surface_schema",
        description=(
            "Emit observation_surface_schema.json and observation_surface_schema_report.json "
            "(deterministic JSON Schema v1 for a single player-relative observation frame)."
        ),
    )
    parser.add_argument(
        "--output-dir",
        required=True,
        type=Path,
        help="Directory for schema + report JSON outputs",
    )
    parser.add_argument(
        "--example-fixture",
        action="append",
        default=[],
        metavar="LABEL=PATH",
        help=(
            "Optional LABEL=PATH pairs to record SHA-256 of example JSON in the report "
            "(repeatable). Example: --example-fixture valid=tests/fixtures/m17/valid.json"
        ),
    )
    args = parser.parse_args(argv)

    example_paths: dict[str, Path] = {}
    for raw in args.example_fixture:
        if "=" not in raw:
            print(f"invalid --example-fixture (expected LABEL=PATH): {raw!r}", file=sys.stderr)
            return 2
        label, p = raw.split("=", 1)
        example_paths[label.strip()] = Path(p.strip())

    write_observation_surface_schema_artifacts(
        args.output_dir,
        example_fixture_paths=example_paths or None,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
