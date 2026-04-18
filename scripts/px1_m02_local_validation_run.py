"""PX1-M02: single M44 local_live_play_validation with M51 refit weights (sidecar mismatch allowed).

Calls ``run_local_live_play_validation(..., enforce_weights_sidecar_sha256=False)`` so the
PX1-M01 optional weighted-refit joblib is usable without matching ``hierarchical_training_run``
weights_sidecar — same honest pattern as PX1-M01 campaign M44 on refit weights.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from starlab.sc2.local_live_play_validation_harness import run_local_live_play_validation
from starlab.sc2.local_live_play_validation_models import RuntimeMode


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(
        description="PX1-M02: one bounded local_live_play_validation run (refit weights OK).",
    )
    p.add_argument(
        "--hierarchical-training-run-dir",
        type=Path,
        required=True,
        help="M43 dir containing hierarchical_training_run.json",
    )
    p.add_argument(
        "--weights",
        type=Path,
        required=True,
        help="Path to hierarchical_training_sklearn_bundle.joblib (e.g. M51 refit bundle)",
    )
    p.add_argument("--match-config", type=Path, required=True, help="M02 match config JSON")
    p.add_argument("--output-dir", type=Path, required=True, help="M44 output root")
    p.add_argument(
        "--runtime-mode",
        choices=("local_live_sc2", "fixture_stub_ci"),
        default="local_live_sc2",
    )
    p.add_argument(
        "--optional-video",
        type=Path,
        default=None,
        help="Optional video file for optional_media_registration (watchable evidence)",
    )
    args = p.parse_args(argv)

    mode: RuntimeMode = args.runtime_mode  # type: ignore[assignment]
    try:
        run_local_live_play_validation(
            enforce_weights_sidecar_sha256=False,
            hierarchical_training_run_dir=args.hierarchical_training_run_dir,
            match_config_path=args.match_config,
            optional_video_path=args.optional_video,
            output_dir=args.output_dir,
            runtime_mode=mode,
            weights_path=args.weights,
        )
    except (OSError, RuntimeError, ValueError) as exc:
        sys.stderr.write(f"{exc}\n")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
