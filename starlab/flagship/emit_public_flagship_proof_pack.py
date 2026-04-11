"""CLI: emit the M39 public flagship proof pack (deterministic, fixture-backed)."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from starlab.flagship.build_public_flagship_proof_pack import write_public_flagship_proof_pack


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="python -m starlab.flagship.emit_public_flagship_proof_pack",
        description=(
            "Emit public_flagship_proof_pack.json, report, subordinate M25/M28/M31 artifacts, "
            "and hashes.json under the output directory."
        ),
    )
    parser.add_argument(
        "--output-dir",
        required=True,
        type=Path,
        help="Directory for pack root (e.g. out/flagship)",
    )
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=None,
        help="Repository root (defaults: parent of the starlab package)",
    )
    args = parser.parse_args(argv)

    here = Path(__file__).resolve()
    repo_root = args.repo_root
    if repo_root is None:
        repo_root = here.parents[2]

    out = args.output_dir.resolve()
    try:
        write_public_flagship_proof_pack(repo_root=repo_root, output_dir=out)
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(f"emit_public_flagship_proof_pack: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
