"""CLI: emit slice-2 campaign execution skeleton artifacts under --output-dir."""

from __future__ import annotations

import argparse
from pathlib import Path

from starlab.sc2.px2.self_play.campaign_run import run_px2_campaign_execution_skeleton


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(
        description=(
            "Run bounded PX2 self-play campaign execution skeleton (fixture CPU; slice 2)."
        )
    )
    p.add_argument("--output-dir", type=Path, required=True)
    p.add_argument("--corpus-root", type=Path, required=True)
    p.add_argument("--campaign-id", default="px2_m03_skeleton_campaign_001")
    p.add_argument("--campaign-profile-id", default="px2_m03_slice2_skeleton_v1")
    p.add_argument("--run-id", default=None, help="Deterministic id recommended for audits.")
    p.add_argument("--torch-seed", type=int, default=42)
    p.add_argument("--episodes", type=int, default=3)
    p.add_argument("--checkpoint-cadence-episodes", type=int, default=2)
    p.add_argument("--eval-cadence-episodes", type=int, default=2)
    args = p.parse_args(argv)

    summary = run_px2_campaign_execution_skeleton(
        corpus_root=args.corpus_root.resolve(),
        output_dir=args.output_dir.resolve(),
        campaign_id=args.campaign_id,
        campaign_profile_id=args.campaign_profile_id,
        run_id=args.run_id,
        torch_seed=args.torch_seed,
        fixture_episode_count=args.episodes,
        checkpoint_episode_cadence=args.checkpoint_cadence_episodes,
        eval_episode_cadence=args.eval_cadence_episodes,
    )
    print(f"wrote skeleton under {summary['output_dir']}")
    print(f"run_id={summary['run_id']} run_sha256={summary['run_sha256']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
