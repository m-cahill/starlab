"""CLI: M45 self-play / RL bootstrap run + report (+ optional local updated joblib bundle)."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import cast

from starlab.sc2.local_live_play_validation_models import RuntimeMode
from starlab.training.self_play_rl_bootstrap_pipeline import run_self_play_rl_bootstrap


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="python -m starlab.training.emit_self_play_rl_bootstrap_run",
        description=(
            "M45: bounded bootstrap rollouts via M44 local live-play validation; "
            "optional weighted sklearn re-fit (local-only joblib)."
        ),
    )
    parser.add_argument(
        "--hierarchical-training-run-dir",
        required=True,
        type=Path,
        metavar="DIR",
        help="Directory containing hierarchical_training_run.json and weights/ (M43).",
    )
    parser.add_argument(
        "--match-config",
        required=True,
        type=Path,
        help=(
            "M02 match config JSON (adapter=fake for fixture_stub_ci; burnysc2 for local_live_sc2)."
        ),
    )
    parser.add_argument(
        "--output-dir",
        required=True,
        type=Path,
        help="Bootstrap run root (e.g. out/rl_bootstrap_runs/<run_id>/).",
    )
    parser.add_argument(
        "--runtime-mode",
        required=True,
        choices=("fixture_stub_ci", "local_live_sc2"),
        help="M44 runtime mode (fixture_stub_ci for CI-safe paths).",
    )
    parser.add_argument(
        "--episodes",
        type=int,
        default=None,
        help="Episode count (default: 1 for fixture_stub_ci, 5 for local_live_sc2).",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help=(
            "Bootstrap base seed: per-episode M02 match config seed is seed+episode_index; "
            "also random_state for weighted re-fit LogisticRegression when --emit-updated-bundle."
        ),
    )
    parser.add_argument(
        "--weights",
        type=Path,
        default=None,
        help="Override path to hierarchical_training_sklearn_bundle.joblib.",
    )
    parser.add_argument(
        "--dataset",
        type=Path,
        default=None,
        help="M26 replay_training_dataset.json (required with --emit-updated-bundle).",
    )
    parser.add_argument(
        "--bundle-dir",
        action="append",
        dest="bundle_dirs",
        default=None,
        type=Path,
        help="M14 bundle directory (repeatable; required with --emit-updated-bundle).",
    )
    parser.add_argument(
        "--emit-updated-bundle",
        action="store_true",
        help="Run weighted re-fit and write updated_policy/rl_bootstrap_candidate_bundle.joblib.",
    )
    parser.add_argument(
        "--mirror-self-play",
        action="store_true",
        help="Reserved for mirror self-play (not implemented in M45 v1).",
    )
    args = parser.parse_args(argv)

    runtime_mode = cast(RuntimeMode, args.runtime_mode)
    episodes = args.episodes
    if episodes is None:
        episodes = 1 if runtime_mode == "fixture_stub_ci" else 5

    bundle_dirs: list[Path] | None = args.bundle_dirs
    if args.emit_updated_bundle:
        if args.dataset is None:
            sys.stderr.write("--emit-updated-bundle requires --dataset\n")
            return 1
        if not bundle_dirs:
            sys.stderr.write("--emit-updated-bundle requires at least one --bundle-dir\n")
            return 1

    try:
        run_self_play_rl_bootstrap(
            bundle_dirs=bundle_dirs,
            dataset_path=args.dataset,
            emit_updated_bundle=args.emit_updated_bundle,
            episodes=episodes,
            hierarchical_training_run_dir=args.hierarchical_training_run_dir,
            match_config_path=args.match_config,
            mirror_self_play=args.mirror_self_play,
            output_dir=args.output_dir,
            runtime_mode=runtime_mode,
            seed=args.seed,
            weights_path=args.weights,
        )
    except (NotImplementedError, OSError, ValueError, RuntimeError) as exc:
        sys.stderr.write(f"{exc}\n")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
