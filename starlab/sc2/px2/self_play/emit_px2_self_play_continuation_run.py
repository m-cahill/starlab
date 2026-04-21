"""CLI: bounded continuation run consuming current-candidate pointer (PX2-M03 slice 11)."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from starlab.sc2.px2.self_play.continuation_run import (
    run_bounded_continuation_run_consuming_current_candidate,
)


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(
        description=(
            "PX2 slice-11 bounded continuation run that validates and consumes "
            "px2_self_play_current_candidate.json; not industrial campaign; "
            "not PX2-M04; not merge-gate CI."
        ),
    )
    p.add_argument("--corpus-root", type=Path, required=True)
    p.add_argument("--campaign-root", type=Path, required=True)
    p.add_argument("--campaign-id", type=str, required=True)
    p.add_argument("--continuation-run-id", type=str, required=True)
    p.add_argument("--torch-seed", type=int, default=99)
    p.add_argument("--steps", type=int, default=2, help="Continuity steps per run (clamped 2–3).")
    p.add_argument("--device-intent", default="cpu")
    p.add_argument("--map-location", default="cpu")
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--init-only", action="store_true")
    g.add_argument("--weights", type=Path)
    p.add_argument("--weight-bundle-ref", default=None)
    args = p.parse_args(argv)

    try:
        summary = run_bounded_continuation_run_consuming_current_candidate(
            corpus_root=args.corpus_root.resolve(),
            campaign_root=args.campaign_root.resolve(),
            campaign_id=args.campaign_id,
            continuation_run_id=args.continuation_run_id,
            init_only=bool(args.init_only),
            weights_path=None if args.init_only else args.weights,
            weight_bundle_ref=args.weight_bundle_ref,
            torch_seed=args.torch_seed,
            continuity_step_count=args.steps,
            device_intent=args.device_intent,
            map_location=args.map_location,
        )
    except (RuntimeError, ValueError) as exc:
        print(str(exc), file=sys.stderr)
        return 1
    print(f"consumption_status={summary['consumption_status']}")
    print(f"continuation_run_sha256={summary['continuation_run_sha256']}")
    if summary["consumption_status"] == "consumed_ok":
        print(f"continuation_continuity_sha256={summary['continuation_continuity_sha256']}")
        print(
            f"updated_campaign_root_manifest_sha256={summary['updated_campaign_root_manifest_sha256']}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
