"""CLI: emit agent training program contract JSON (M40)."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from starlab.training.training_program_io import write_agent_training_program_contract


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="python -m starlab.training.emit_agent_training_program_contract",
        description=(
            "Emit agent_training_program_contract.json and "
            "agent_training_program_contract_report.json under the output directory."
        ),
    )
    parser.add_argument(
        "--output-dir",
        required=True,
        type=Path,
        help="Directory for outputs (e.g. out/training_program)",
    )
    args = parser.parse_args(argv)
    out = args.output_dir.resolve()
    try:
        write_agent_training_program_contract(out)
    except OSError as exc:
        print(f"emit_agent_training_program_contract: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
