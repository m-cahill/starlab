"""CLI: bounded session transition + current-candidate carry-forward (PX2-M03 slice 10)."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from starlab.sc2.px2.self_play.current_candidate import (
    DEFAULT_SLICE10_CAMPAIGN_ID,
    run_bounded_operator_local_session_transition_with_current_candidate,
)


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(
        description=(
            "PX2 slice-10 bounded transition + current-candidate carry-forward; "
            "not PX2-M04; not merge-gate CI."
        ),
    )
    p.add_argument("--corpus-root", type=Path, required=True)
    p.add_argument("--campaign-id", default=DEFAULT_SLICE10_CAMPAIGN_ID)
    p.add_argument(
        "--base-dir",
        type=Path,
        default=None,
        help="Directory containing out/ (default: current working directory).",
    )
    p.add_argument(
        "--transition",
        choices=("promotion", "rollback"),
        required=True,
        help="Passed through to slice-9 transition stub.",
    )
    p.add_argument(
        "--run-ids",
        nargs="+",
        default=None,
        help="At least two distinct run ids (default: px2_sess_run_00, …).",
    )
    p.add_argument("--run-count", type=int, default=2, help="Used when --run-ids omitted (>=2).")
    p.add_argument("--torch-seed", type=int, default=42)
    p.add_argument("--steps", type=int, default=2, help="Continuity steps per run (clamped 2–3).")
    p.add_argument("--device-intent", default="cpu")
    p.add_argument("--map-location", default="cpu")
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--init-only", action="store_true")
    g.add_argument("--weights", type=Path)
    p.add_argument("--weight-bundle-ref", default=None)
    args = p.parse_args(argv)

    try:
        summary = run_bounded_operator_local_session_transition_with_current_candidate(
            corpus_root=args.corpus_root.resolve(),
            transition_kind=args.transition,
            campaign_id=args.campaign_id,
            base_dir=args.base_dir.resolve() if args.base_dir else None,
            init_only=bool(args.init_only),
            weights_path=None if args.init_only else args.weights,
            weight_bundle_ref=args.weight_bundle_ref,
            run_ids=list(args.run_ids) if args.run_ids else None,
            run_count=int(args.run_count),
            torch_seed=args.torch_seed,
            continuity_step_count=args.steps,
            device_intent=args.device_intent,
            map_location=args.map_location,
        )
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    print(f"current_candidate_sha256={summary['current_candidate_sha256']}")
    ots = summary["operator_local_session_transition_sha256"]
    print(f"operator_local_session_transition_sha256={ots}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
