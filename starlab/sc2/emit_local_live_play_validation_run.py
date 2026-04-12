"""CLI: emit M44 local_live_play_validation_run JSON + report + replay binding."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from starlab.sc2.local_live_play_validation_harness import run_local_live_play_validation


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="python -m starlab.sc2.emit_local_live_play_validation_run",
        description=(
            "Run bounded local live-play validation for an M43 hierarchical training run: "
            "M02 match harness, M43 sklearn inference, M04 replay binding, M44 validation JSON."
        ),
    )
    parser.add_argument(
        "--hierarchical-training-run-dir",
        required=True,
        type=Path,
        metavar="DIR",
        help="Directory containing hierarchical_training_run.json and weights/ (M43)",
    )
    parser.add_argument(
        "--match-config",
        required=True,
        type=Path,
        help=(
            "M02 match config JSON (adapter=fake for fixture_stub_ci; burnysc2 for local_live_sc2)"
        ),
    )
    parser.add_argument(
        "--output-dir",
        required=True,
        type=Path,
        help="Run root (e.g. out/live_validation_runs/<run_id>/)",
    )
    parser.add_argument(
        "--runtime-mode",
        required=True,
        choices=("fixture_stub_ci", "local_live_sc2"),
        help="fixture_stub_ci: fake adapter + deterministic stub replay (CI). "
        "local_live_sc2: burnysc2 adapter + local SC2 (operator machine).",
    )
    parser.add_argument(
        "--weights",
        type=Path,
        default=None,
        help=(
            "Override path to hierarchical_training_sklearn_bundle.joblib "
            "(default: <run-dir>/weights/)"
        ),
    )
    parser.add_argument(
        "--optional-video",
        type=Path,
        default=None,
        help=(
            "Optional externally captured video file for supplementary metadata "
            "(hashed, not parsed)."
        ),
    )
    parser.add_argument(
        "--run-id",
        default=None,
        metavar="ID",
        help="Optional validation run id override (default: deterministic hash)",
    )
    parser.add_argument(
        "--no-environment-fingerprint",
        action="store_true",
        help="Omit environment_fingerprint from run_identity (passed through to seed_from_proof)",
    )
    parser.add_argument(
        "--env-json",
        type=Path,
        default=None,
        help="Optional environment JSON for seed_from_proof",
    )
    args = parser.parse_args(argv)

    try:
        run_local_live_play_validation(
            env_json_path=args.env_json,
            hierarchical_training_run_dir=args.hierarchical_training_run_dir,
            include_environment_fingerprint=not args.no_environment_fingerprint,
            match_config_path=args.match_config,
            optional_video_path=args.optional_video,
            output_dir=args.output_dir,
            run_id=args.run_id,
            runtime_mode=args.runtime_mode,
            weights_path=args.weights,
        )
    except (OSError, ValueError, RuntimeError) as exc:
        sys.stderr.write(f"{exc}\n")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
