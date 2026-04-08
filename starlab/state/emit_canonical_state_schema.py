"""CLI: emit canonical_state_schema.json + canonical_state_schema_report.json (M15)."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from starlab.state.canonical_state_io import write_canonical_state_schema_artifacts


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="python -m starlab.state.emit_canonical_state_schema",
        description=(
            "Emit canonical_state_schema.json and canonical_state_schema_report.json "
            "(deterministic JSON Schema v1 for a single replay-native state frame)."
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
            "(repeatable). Example: --example-fixture valid=tests/fixtures/m15/valid.json"
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

    write_canonical_state_schema_artifacts(
        args.output_dir,
        example_fixture_paths=example_paths or None,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
