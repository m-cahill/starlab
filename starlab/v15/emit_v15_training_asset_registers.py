"""CLI: emit v15_training_asset_registers.json + report (V15-M01)."""

from __future__ import annotations

import argparse
from pathlib import Path

from starlab.v15.training_asset_register_io import emit_training_asset_registers


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Emit governed STARLAB v1.5 training-scale asset register contract + report (V15-M01). "
            "Planning artifact only — does not scan private assets, run GPU training, or approve "
            "claim-critical rows."
        ),
    )
    parser.add_argument(
        "--output-dir",
        required=True,
        type=Path,
        help="Directory for v15_training_asset_registers.json and report",
    )
    args = parser.parse_args(argv)

    sealed, _rep, c_path, r_path = emit_training_asset_registers(args.output_dir)
    print(f"wrote {c_path}")
    print(f"wrote {r_path}")
    print(f"training_asset_registers_sha256={sealed['training_asset_registers_sha256']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
