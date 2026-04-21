"""CLI: bounded handoff-anchored operator-local run (PX2-M03 slice 16)."""

from __future__ import annotations

import argparse
from pathlib import Path

from starlab.sc2.px2.self_play.handoff_anchored_run import (
    ANCHORED_OK,
    run_bounded_handoff_anchored_operator_local_run,
)


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(
        description=(
            "PX2 slice-16 bounded run anchored on `px2_self_play_pointer_seeded_handoff.json` "
            "(slice-15 handed_off_ok); not industrial campaign; not PX2-M04; not merge-gate CI."
        ),
    )
    p.add_argument("--corpus-root", type=Path, required=True)
    p.add_argument("--campaign-root", type=Path, required=True)
    p.add_argument("--campaign-id", type=str, required=True)
    p.add_argument("--handoff-anchored-run-id", type=str, default="slice16_ha")
    p.add_argument("--torch-seed", type=int, default=103)
    p.add_argument("--steps", type=int, default=2, help="Continuity steps per run (clamped 2–3).")
    p.add_argument("--device-intent", default="cpu")
    p.add_argument("--map-location", default="cpu")
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--init-only", action="store_true")
    g.add_argument("--weights", type=Path)
    p.add_argument("--weight-bundle-ref", default=None)
    args = p.parse_args(argv)

    steps = max(2, min(3, int(args.steps)))

    summary = run_bounded_handoff_anchored_operator_local_run(
        corpus_root=args.corpus_root.resolve(),
        campaign_root=args.campaign_root.resolve(),
        campaign_id=args.campaign_id,
        handoff_anchored_run_id=args.handoff_anchored_run_id,
        init_only=bool(args.init_only),
        weights_path=None if args.init_only else args.weights,
        weight_bundle_ref=args.weight_bundle_ref,
        torch_seed=args.torch_seed,
        continuity_step_count=steps,
        device_intent=args.device_intent,
        map_location=args.map_location,
    )
    print(f"anchoring_status={summary['anchoring_status']}")
    print(f"handoff_anchored_run_sha256={summary['handoff_anchored_run_sha256']}")
    return 0 if summary["anchoring_status"] == ANCHORED_OK else 1


if __name__ == "__main__":
    raise SystemExit(main())
