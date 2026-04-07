"""CLI: build canonical run artifact v0 from M03 + M04 JSON (M05).

Packages STARLAB-owned records only. Does not accept replay or proof paths.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from starlab.runs.canonical_run_artifact import write_canonical_run_artifact_bundle


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Build a deterministic canonical run artifact directory from M03 run_identity.json, "
            "M03 lineage_seed.json, and M04 replay_binding.json (M05)."
        ),
    )
    parser.add_argument(
        "--run-identity",
        required=True,
        type=Path,
        help="Path to M03 run_identity.json",
    )
    parser.add_argument(
        "--lineage-seed",
        required=True,
        type=Path,
        help="Path to M03 lineage_seed.json",
    )
    parser.add_argument(
        "--replay-binding",
        required=True,
        type=Path,
        help="Path to M04 replay_binding.json",
    )
    parser.add_argument(
        "--output-dir",
        required=True,
        type=Path,
        help="Directory to create for the canonical bundle (must not already exist)",
    )
    args = parser.parse_args(argv)

    if not args.run_identity.is_file():
        print(f"error: run_identity not found: {args.run_identity}")
        return 1
    if not args.lineage_seed.is_file():
        print(f"error: lineage_seed not found: {args.lineage_seed}")
        return 1
    if not args.replay_binding.is_file():
        print(f"error: replay_binding not found: {args.replay_binding}")
        return 1

    try:
        write_canonical_run_artifact_bundle(
            lineage_seed_path=args.lineage_seed,
            output_dir=args.output_dir,
            replay_binding_path=args.replay_binding,
            run_identity_path=args.run_identity,
        )
    except ValueError as exc:
        print(f"error: {exc}")
        return 1

    print(f"wrote canonical run artifact bundle under {args.output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
