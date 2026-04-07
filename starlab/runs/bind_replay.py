"""CLI: bind a replay file to M03 run identity / lineage seed (M04).

Treats the replay as opaque bytes. Does not parse .SC2Replay semantics.
Reads ``proof_artifact_hash`` from the existing ``run_identity.json``,
not from raw proof files.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from starlab.runs.replay_binding import (
    build_replay_binding_record,
    build_replay_reference,
    compute_replay_content_sha256,
    load_lineage_seed,
    load_run_identity,
    write_replay_binding,
)


def bind_replay_from_paths(
    *,
    run_identity_path: Path,
    lineage_seed_path: Path,
    replay_path: Path,
    output_dir: Path,
) -> Path:
    """Load M03 artifacts, bind replay, write ``replay_binding.json``."""

    ri = load_run_identity(run_identity_path)
    ls = load_lineage_seed(lineage_seed_path)

    replay_sha = compute_replay_content_sha256(replay_path)
    replay_ref = build_replay_reference(replay_path)

    record = build_replay_binding_record(
        execution_id=ri["execution_id"],
        lineage_seed_id=ls["lineage_seed_id"],
        proof_artifact_hash=ri["proof_artifact_hash"],
        replay_content_sha256=replay_sha,
        replay_reference=replay_ref,
        run_spec_id=ri["run_spec_id"],
    )

    return write_replay_binding(output_dir, record)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Bind a replay file to M03 run identity / lineage seed. "
            "Treats replay as opaque bytes (M04)."
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
        "--replay",
        required=True,
        type=Path,
        help="Path to replay file (treated as opaque bytes)",
    )
    parser.add_argument(
        "--output-dir",
        required=True,
        type=Path,
        help="Directory to write replay_binding.json",
    )
    args = parser.parse_args(argv)

    if not args.run_identity.is_file():
        print(f"error: run_identity not found: {args.run_identity}")
        return 1
    if not args.lineage_seed.is_file():
        print(f"error: lineage_seed not found: {args.lineage_seed}")
        return 1
    if not args.replay.is_file():
        print(f"error: replay not found: {args.replay}")
        return 1

    out = bind_replay_from_paths(
        lineage_seed_path=args.lineage_seed,
        output_dir=args.output_dir,
        replay_path=args.replay,
        run_identity_path=args.run_identity,
    )
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
