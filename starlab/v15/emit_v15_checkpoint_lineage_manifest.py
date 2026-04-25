"""CLI: emit v15_checkpoint_lineage_manifest.json + report (V15-M03)."""

from __future__ import annotations

import argparse
from pathlib import Path

from starlab.v15.checkpoint_lineage_io import emit_checkpoint_lineage_manifest
from starlab.v15.checkpoint_lineage_models import PROFILE_FIXTURE_CI, PROFILE_OPERATOR_DECLARED

_SEAL = "checkpoint_lineage_manifest_sha256"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Emit governed STARLAB v1.5 checkpoint lineage manifest + report (V15-M03). "
            "Does not read checkpoint weight files, does not run training or resume. "
            "Default profile is fixture_ci (CI-safe, deterministic)."
        ),
    )
    parser.add_argument(
        "--output-dir",
        required=True,
        type=Path,
        help="Directory for v15_checkpoint_lineage_manifest.json and report",
    )
    parser.add_argument(
        "--profile",
        choices=(PROFILE_FIXTURE_CI, PROFILE_OPERATOR_DECLARED),
        default=PROFILE_FIXTURE_CI,
        help="fixture_ci (default) or operator_declared (requires --lineage-json)",
    )
    parser.add_argument(
        "--lineage-json",
        type=Path,
        default=None,
        help=(
            "Operator lineage JSON (metadata-only; see "
            "docs/runtime/v15_checkpoint_lineage_resume_discipline_v1.md). "
            "Required for --profile operator_declared."
        ),
    )
    parser.add_argument(
        "--environment-lock-json",
        type=Path,
        default=None,
        help=(
            "Optional M02 v15_long_gpu_environment_lock.json (or compatible object). "
            "Canonical JSON SHA-256 is bound; not required in fixture mode."
        ),
    )
    args = parser.parse_args(argv)

    if args.profile == PROFILE_OPERATOR_DECLARED and args.lineage_json is None:
        print("error: --lineage-json is required for operator_declared", flush=True)
        return 2

    if args.profile == PROFILE_FIXTURE_CI and args.lineage_json is not None:
        print("warning: --lineage-json is ignored for fixture_ci profile", flush=True)

    lineage_path: Path | None = args.lineage_json
    if args.profile == PROFILE_FIXTURE_CI:
        lineage_path = None

    lock_path = args.environment_lock_json
    if args.profile == PROFILE_FIXTURE_CI and lock_path is not None:
        print("warning: --environment-lock-json is ignored for fixture_ci profile", flush=True)
        lock_path = None

    sealed, _rep, c_path, r_path = emit_checkpoint_lineage_manifest(
        args.output_dir,
        profile=args.profile,
        lineage_path=lineage_path,
        environment_lock_path=lock_path,
    )
    print(f"wrote {c_path}")
    print(f"wrote {r_path}")
    print(f"{_SEAL}={sealed.get(_SEAL, '')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
