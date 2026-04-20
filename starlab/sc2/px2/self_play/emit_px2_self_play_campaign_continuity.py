"""CLI: bounded multi-step operator-local continuity (PX2-M03 slice 4)."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from starlab.sc2.px2.self_play.campaign_continuity import run_operator_local_campaign_continuity


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(
        description=("PX2 slice-4 multi-step continuity (local-first; not default merge-gate CI)."),
    )
    p.add_argument("--output-dir", type=Path, required=True)
    p.add_argument("--corpus-root", type=Path, required=True)
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
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--init-only", action="store_true")
    g.add_argument(
        "--weights",
        type=Path,
        help="Torch state_dict file (required if not --init-only).",
    )
    p.add_argument("--weight-bundle-ref", default=None)
    args = p.parse_args(argv)

    try:
        summary = run_operator_local_campaign_continuity(
            corpus_root=args.corpus_root.resolve(),
            output_dir=args.output_dir.resolve(),
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
    print(f"continuity_sha256={summary['continuity_sha256']}")
    print(f"continuity_chain_sha256={summary['continuity_chain_sha256']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
