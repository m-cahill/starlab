"""CLI: operator-local campaign root + slice-5 continuity (PX2-M03 slice 5)."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from starlab.sc2.px2.self_play.campaign_root import run_slice5_operator_local_campaign
from starlab.sc2.px2.self_play.opponent_selection import (
    OPPONENT_SELECTION_ROUND_ROBIN,
    OPPONENT_SELECTION_WEIGHTED_FROZEN_STUB,
)


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(
        description=(
            "PX2 slice-5 campaign root: opponent-pool metadata + bounded continuity + "
            "sealed campaign-root manifest (local-first; not default merge-gate CI)."
        ),
    )
    p.add_argument("--campaign-root", type=Path, required=True)
    p.add_argument("--corpus-root", type=Path, required=True)
    p.add_argument("--campaign-id", default="px2_m03_slice5_operator_local")
    p.add_argument("--run-id", default=None)
    p.add_argument("--torch-seed", type=int, default=42)
    p.add_argument(
        "--steps",
        type=int,
        default=3,
        help="Continuity steps (clamped to 2–3 for non-industrial bounds).",
    )
    p.add_argument("--device-intent", default="cpu")
    p.add_argument("--map-location", default="cpu")
    p.add_argument(
        "--opponent-selection",
        choices=("round_robin", "weighted_frozen_stub"),
        default="round_robin",
    )
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--init-only", action="store_true")
    g.add_argument(
        "--weights",
        type=Path,
        help="Torch state_dict file (required if not --init-only).",
    )
    p.add_argument("--weight-bundle-ref", default=None)
    args = p.parse_args(argv)

    rule = (
        OPPONENT_SELECTION_WEIGHTED_FROZEN_STUB
        if args.opponent_selection == "weighted_frozen_stub"
        else OPPONENT_SELECTION_ROUND_ROBIN
    )

    try:
        summary = run_slice5_operator_local_campaign(
            corpus_root=args.corpus_root.resolve(),
            campaign_root=args.campaign_root.resolve(),
            init_only=bool(args.init_only),
            weights_path=None if args.init_only else args.weights,
            weight_bundle_ref=args.weight_bundle_ref,
            campaign_id=args.campaign_id,
            torch_seed=args.torch_seed,
            run_id=args.run_id,
            continuity_step_count=args.steps,
            device_intent=args.device_intent,
            map_location=args.map_location,
            opponent_selection_rule_id=rule,
            opponent_selection_weights=None,
        )
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    print(f"campaign_root_manifest_sha256={summary['campaign_root_manifest_sha256']}")
    print(f"continuity_sha256={summary['continuity_sha256']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
