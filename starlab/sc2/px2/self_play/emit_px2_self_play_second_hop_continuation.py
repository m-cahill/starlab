"""CLI: bounded second-hop continuation after slice-12 re-anchor (PX2-M03 slice 13)."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from starlab.sc2.px2.self_play.second_hop_continuation import (
    run_bounded_second_hop_continuation_after_slice12,
)


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(
        description=(
            "PX2 slice-13 bounded second-hop continuation on post-slice-12 current-candidate "
            "pointer; optional symmetric re-anchor; not industrial campaign; not PX2-M04; "
            "not merge-gate CI."
        ),
    )
    p.add_argument("--corpus-root", type=Path, required=True)
    p.add_argument("--campaign-root", type=Path, required=True)
    p.add_argument("--campaign-id", type=str, required=True)
    p.add_argument("--second-hop-continuation-run-id", type=str, default="second_hop_cont")
    p.add_argument("--torch-seed", type=int, default=99)
    p.add_argument("--steps", type=int, default=2, help="Continuity steps per run (clamped 2–3).")
    p.add_argument("--device-intent", default="cpu")
    p.add_argument("--map-location", default="cpu")
    p.add_argument(
        "--no-symmetric-reanchor",
        action="store_true",
        help="Skip slice-13 symmetric re-anchor after consumed_ok second hop.",
    )
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--init-only", action="store_true")
    g.add_argument("--weights", type=Path)
    p.add_argument("--weight-bundle-ref", default=None)
    args = p.parse_args(argv)

    try:
        summary = run_bounded_second_hop_continuation_after_slice12(
            corpus_root=args.corpus_root.resolve(),
            campaign_root=args.campaign_root.resolve(),
            campaign_id=args.campaign_id,
            second_hop_continuation_run_id=args.second_hop_continuation_run_id,
            init_only=bool(args.init_only),
            weights_path=None if args.init_only else args.weights,
            weight_bundle_ref=args.weight_bundle_ref,
            torch_seed=args.torch_seed,
            continuity_step_count=args.steps,
            device_intent=args.device_intent,
            map_location=args.map_location,
            symmetric_reanchor=not args.no_symmetric_reanchor,
        )
    except (RuntimeError, ValueError) as exc:
        print(str(exc), file=sys.stderr)
        return 1
    print(f"second_hop_status={summary['second_hop_status']}")
    print(f"second_hop_continuation_sha256={summary['second_hop_continuation_sha256']}")
    print(f"continuation_consumption_status={summary['continuation_consumption_status']}")
    sr = summary.get("symmetric_reanchor")
    if sr is not None:
        print(f"symmetric_reanchor_status={sr.get('reanchor_status')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
