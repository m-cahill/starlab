"""CLI: emit sc2_foundation_v1_proof_pack.json + report (M61)."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from starlab.release_lock.sc2_foundation_proof_pack import (
    write_sc2_foundation_v1_proof_pack_artifacts,
)


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(
        prog="python -m starlab.release_lock.emit_sc2_foundation_v1_proof_pack",
        description=(
            "Emit deterministic SC2 foundation v1 proof pack JSON from operator-authored input."
        ),
    )
    p.add_argument(
        "--input",
        type=Path,
        required=True,
        help="Path to proof_pack_input.json (see docs/runtime/sc2_foundation_release_lock_v1.md).",
    )
    p.add_argument(
        "--output-dir",
        type=Path,
        required=True,
        help="Directory for sc2_foundation_v1_proof_pack.json and report.",
    )
    p.add_argument(
        "--base-dir",
        type=Path,
        default=None,
        help="Directory used to resolve relative paths in input (default: input file's parent).",
    )
    args = p.parse_args(argv)
    try:
        out = write_sc2_foundation_v1_proof_pack_artifacts(
            input_path=args.input.resolve(),
            output_dir=args.output_dir.resolve(),
            base_dir=args.base_dir.resolve() if args.base_dir is not None else None,
        )
        print(f"Wrote {out[0]}")
        print(f"Wrote {out[1]}")
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(f"emit_sc2_foundation_v1_proof_pack: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
