"""CLI: emit v15_training_readiness_charter.json + report (V15-M00)."""

from __future__ import annotations

import argparse
from pathlib import Path

from starlab.v15.training_readiness_charter_io import emit_training_readiness_charter


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Emit governed STARLAB v1.5 training readiness charter + report (V15-M00). "
            "Planning artifact only — does not run GPU training or benchmarks."
        ),
    )
    parser.add_argument(
        "--output-dir",
        required=True,
        type=Path,
        help="Directory for v15_training_readiness_charter.json and report",
    )
    args = parser.parse_args(argv)

    sealed, _rep, c_path, r_path = emit_training_readiness_charter(args.output_dir)
    print(f"wrote {c_path}")
    print(f"wrote {r_path}")
    print(f"training_readiness_charter_sha256={sealed['training_readiness_charter_sha256']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
