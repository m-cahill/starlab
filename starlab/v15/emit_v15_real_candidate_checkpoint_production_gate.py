"""CLI: emit V15-M20 real candidate checkpoint production gate JSON + report + runbook."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from starlab.v15.real_candidate_checkpoint_production_gate_io import (
    emit_fixture_default,
    emit_operator_preflight_gate,
)
from starlab.v15.real_candidate_checkpoint_production_gate_models import (
    PROFILE_FIXTURE_DEFAULT,
    PROFILE_OPERATOR_PREFLIGHT,
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Emit V15-M20 real candidate checkpoint production gate artifacts. "
            "Default fixture profile is CI-safe (no GPU)."
        ),
    )
    parser.add_argument("--output-dir", required=True, type=Path, help="Output directory.")
    parser.add_argument(
        "--profile",
        choices=(PROFILE_FIXTURE_DEFAULT, PROFILE_OPERATOR_PREFLIGHT),
        default=PROFILE_FIXTURE_DEFAULT,
        help="fixture_default (CI) or operator_preflight input validation.",
    )
    parser.add_argument(
        "--m16-short-gpu-environment-json",
        type=Path,
        default=None,
        help="V15-M16 short GPU environment evidence JSON (operator_preflight).",
    )
    parser.add_argument(
        "--m08-long-gpu-manifest-json",
        type=Path,
        default=None,
        help="V15-M08 long GPU training manifest JSON (operator_preflight).",
    )
    parser.add_argument(
        "--m15-preflight-json",
        type=Path,
        default=None,
        help="V15-M15 operator evidence collection preflight JSON (operator_preflight).",
    )
    args = parser.parse_args(argv)

    if args.profile == PROFILE_OPERATOR_PREFLIGHT:
        missing = []
        for label, p in (
            ("--m16-short-gpu-environment-json", args.m16_short_gpu_environment_json),
            ("--m08-long-gpu-manifest-json", args.m08_long_gpu_manifest_json),
            ("--m15-preflight-json", args.m15_preflight_json),
        ):
            if p is None:
                missing.append(label)
            elif not p.is_file():
                sys.stderr.write(f"error: {label} must exist ({p})\n")
                return 2
        if missing:
            sys.stderr.write(f"error: operator_preflight requires: {', '.join(missing)}\n")
            return 2
        assert args.m16_short_gpu_environment_json is not None
        assert args.m08_long_gpu_manifest_json is not None
        assert args.m15_preflight_json is not None
        emit_operator_preflight_gate(
            args.output_dir,
            m16_path=args.m16_short_gpu_environment_json,
            m08_manifest_path=args.m08_long_gpu_manifest_json,
            m15_preflight_path=args.m15_preflight_json,
        )
        return 0

    emit_fixture_default(args.output_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
