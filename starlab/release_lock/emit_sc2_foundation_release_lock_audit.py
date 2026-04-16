"""CLI: emit sc2_foundation_release_lock_audit.json + report (M61)."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from starlab.release_lock.sc2_foundation_release_lock_audit import (
    write_sc2_foundation_release_lock_audit_artifacts,
)


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(
        prog="python -m starlab.release_lock.emit_sc2_foundation_release_lock_audit",
        description="Emit release-lock audit JSON evaluating an SC2 foundation v1 proof pack.",
    )
    p.add_argument(
        "--proof-pack",
        type=Path,
        required=True,
        help="Path to sc2_foundation_v1_proof_pack.json.",
    )
    p.add_argument(
        "--output-dir",
        type=Path,
        required=True,
        help="Directory for audit + audit report JSON.",
    )
    args = p.parse_args(argv)
    try:
        out = write_sc2_foundation_release_lock_audit_artifacts(
            proof_pack_path=args.proof_pack.resolve(),
            output_dir=args.output_dir.resolve(),
        )
        print(f"Wrote {out[0]}")
        print(f"Wrote {out[1]}")
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(f"emit_sc2_foundation_release_lock_audit: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
