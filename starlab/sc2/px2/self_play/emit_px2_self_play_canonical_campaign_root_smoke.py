"""CLI: canonical operator-local campaign-root smoke (PX2-M03 slice 6)."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from starlab.sc2.px2.self_play.canonical_operator_local_run import (
    run_canonical_operator_local_campaign_root_smoke,
)


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(
        description=(
            "PX2 slice-6 canonical campaign-root smoke: writes "
            "out/px2_self_play_campaigns/<campaign_id>/... (local-first; not merge-gate CI)."
        ),
    )
    p.add_argument("--corpus-root", type=Path, required=True)
    p.add_argument("--campaign-id", default="px2_m03_slice6_canonical_smoke")
    p.add_argument(
        "--base-dir",
        type=Path,
        default=None,
        help="Directory containing out/ (default: current working directory).",
    )
    p.add_argument("--run-id", default=None)
    p.add_argument("--torch-seed", type=int, default=42)
    p.add_argument("--steps", type=int, default=2, help="Continuity steps (clamped 2–3).")
    p.add_argument("--device-intent", default="cpu")
    p.add_argument("--map-location", default="cpu")
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--init-only", action="store_true")
    g.add_argument("--weights", type=Path)
    p.add_argument("--weight-bundle-ref", default=None)
    args = p.parse_args(argv)

    try:
        summary = run_canonical_operator_local_campaign_root_smoke(
            corpus_root=args.corpus_root.resolve(),
            campaign_id=args.campaign_id,
            base_dir=args.base_dir.resolve() if args.base_dir else None,
            init_only=bool(args.init_only),
            weights_path=None if args.init_only else args.weights,
            weight_bundle_ref=args.weight_bundle_ref,
            torch_seed=args.torch_seed,
            run_id=args.run_id,
            continuity_step_count=args.steps,
            device_intent=args.device_intent,
            map_location=args.map_location,
        )
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    print(f"campaign_root_manifest_sha256={summary['campaign_root_manifest_sha256']}")
    print(f"continuity_sha256={summary['continuity_sha256']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
