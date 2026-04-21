"""CLI: bounded pointer-seeded operator-local run (PX2-M03 slice 14)."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from starlab.sc2.px2.self_play.pointer_seeded_run import (
    run_bounded_pointer_seeded_operator_local_run,
)


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(
        description=(
            "PX2 slice-14 bounded run whose declared seed is the latest "
            "`px2_self_play_current_candidate.json`; not industrial campaign; not PX2-M04; "
            "not merge-gate CI."
        ),
    )
    p.add_argument("--corpus-root", type=Path, required=True)
    p.add_argument("--campaign-root", type=Path, required=True)
    p.add_argument("--campaign-id", type=str, required=True)
    p.add_argument("--pointer-seeded-run-id", type=str, default="slice14_pointer_seeded")
    p.add_argument("--torch-seed", type=int, default=101)
    p.add_argument("--steps", type=int, default=2, help="Continuity steps per run (clamped 2–3).")
    p.add_argument("--device-intent", default="cpu")
    p.add_argument("--map-location", default="cpu")
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--init-only", action="store_true")
    g.add_argument("--weights", type=Path)
    p.add_argument("--weight-bundle-ref", default=None)
    args = p.parse_args(argv)

    steps = max(2, min(3, int(args.steps)))

    try:
        summary = run_bounded_pointer_seeded_operator_local_run(
            corpus_root=args.corpus_root.resolve(),
            campaign_root=args.campaign_root.resolve(),
            campaign_id=args.campaign_id,
            pointer_seeded_run_id=args.pointer_seeded_run_id,
            init_only=bool(args.init_only),
            weights_path=None if args.init_only else args.weights,
            weight_bundle_ref=args.weight_bundle_ref,
            torch_seed=args.torch_seed,
            continuity_step_count=steps,
            device_intent=args.device_intent,
            map_location=args.map_location,
        )
    except (RuntimeError, ValueError) as exc:
        print(str(exc), file=sys.stderr)
        return 1
    print(f"seeding_status={summary['seeding_status']}")
    print(f"pointer_seeded_run_sha256={summary['pointer_seeded_run_sha256']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
