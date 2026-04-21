"""CLI: bounded substantive operator-local execution (PX2-M03 — not a lineage micro-slice)."""

from __future__ import annotations

import argparse
from pathlib import Path

from starlab.sc2.px2.self_play.bounded_substantive_execution import (
    DEFAULT_BOUNDED_SUBSTANTIVE_CONTINUITY_STEPS,
    run_bounded_substantive_operator_local_execution,
)


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(
        description=(
            "PX2-M03 bounded substantive operator-local execution: default 15 continuity steps; "
            "not industrial campaign; not PX2-M04; not merge-gate CI. "
            "Real weights: pass --weights (explicit path required)."
        ),
    )
    p.add_argument("--corpus-root", type=Path, required=True)
    p.add_argument("--campaign-root", type=Path, required=True)
    p.add_argument("--campaign-id", type=str, required=True)
    p.add_argument("--substantive-run-id", type=str, default="bounded_substantive_001")
    p.add_argument(
        "--steps",
        type=int,
        default=DEFAULT_BOUNDED_SUBSTANTIVE_CONTINUITY_STEPS,
        help=(
            f"Continuity steps (default {DEFAULT_BOUNDED_SUBSTANTIVE_CONTINUITY_STEPS}; "
            "clamped to [2, 20] for bounded substantive execution)."
        ),
    )
    p.add_argument("--torch-seed", type=int, default=103)
    p.add_argument("--device-intent", default="cpu")
    p.add_argument("--map-location", default="cpu")
    p.add_argument("--weight-bundle-ref", default=None)
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--init-only", action="store_true")
    g.add_argument("--weights", type=Path)
    args = p.parse_args(argv)

    try:
        summary = run_bounded_substantive_operator_local_execution(
            corpus_root=args.corpus_root.resolve(),
            campaign_root=args.campaign_root.resolve(),
            campaign_id=args.campaign_id,
            substantive_run_id=args.substantive_run_id,
            init_only=bool(args.init_only),
            weights_path=None if args.init_only else args.weights,
            weight_bundle_ref=args.weight_bundle_ref,
            continuity_step_count=int(args.steps),
            torch_seed=args.torch_seed,
            device_intent=args.device_intent,
            map_location=args.map_location,
        )
    except ValueError as exc:
        print(f"error: {exc}")
        return 2
    print(f"bounded_substantive_execution_sha256={summary['bounded_substantive_execution_sha256']}")
    print(f"substantive_lineage_mode={summary['substantive_lineage_mode']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
