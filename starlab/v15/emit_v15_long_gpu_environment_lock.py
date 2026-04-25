"""CLI: emit v15_long_gpu_environment_lock.json + report (V15-M02)."""

from __future__ import annotations

import argparse
from pathlib import Path

from starlab.v15.environment_lock_io import emit_long_gpu_environment_lock
from starlab.v15.environment_lock_models import PROFILE_FIXTURE_CI, PROFILE_OPERATOR_LOCAL


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Emit governed STARLAB v1.5 long GPU run environment lock + report (V15-M02). "
            "Does not run GPU training, nvidia-smi, or SC2. "
            "Default profile is fixture_ci (CI-safe)."
        ),
    )
    parser.add_argument(
        "--output-dir",
        required=True,
        type=Path,
        help="Directory for v15_long_gpu_environment_lock.json and report",
    )
    parser.add_argument(
        "--profile",
        choices=(PROFILE_FIXTURE_CI, PROFILE_OPERATOR_LOCAL),
        default=PROFILE_FIXTURE_CI,
        help="fixture_ci (default) or operator_local with optional --probe-json",
    )
    parser.add_argument(
        "--probe-json",
        type=Path,
        default=None,
        help=(
            "Optional operator-local probe JSON "
            "(see docs/runtime/v15_long_gpu_run_environment_lock_v1.md). "
            "Only used with --profile operator_local."
        ),
    )
    args = parser.parse_args(argv)
    if args.profile == PROFILE_FIXTURE_CI and args.probe_json is not None:
        print("warning: --probe-json is ignored for fixture_ci profile", flush=True)
    probe_path: Path | None = args.probe_json
    if args.profile == PROFILE_FIXTURE_CI:
        probe_path = None

    sealed, _rep, c_path, r_path = emit_long_gpu_environment_lock(
        args.output_dir, profile=args.profile, probe_path=probe_path
    )
    print(f"wrote {c_path}")
    print(f"wrote {r_path}")
    print(f"long_gpu_environment_lock_sha256={sealed['long_gpu_environment_lock_sha256']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
