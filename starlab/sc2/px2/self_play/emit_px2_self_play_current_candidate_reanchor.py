"""CLI: post-continuation current-candidate re-anchoring (PX2-M03 slice 12)."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from starlab.sc2.px2.self_play.current_candidate_reanchor import (
    run_bounded_current_candidate_reanchor_after_continuation,
)


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(
        description=(
            "PX2 slice-12 re-anchor current-candidate pointer after consumed_ok "
            "continuation; not industrial campaign; not PX2-M04; not merge-gate CI."
        ),
    )
    p.add_argument("--campaign-root", type=Path, required=True)
    p.add_argument("--campaign-id", type=str, required=True)
    args = p.parse_args(argv)

    try:
        summary = run_bounded_current_candidate_reanchor_after_continuation(
            campaign_root=args.campaign_root.resolve(),
            campaign_id=args.campaign_id,
        )
    except RuntimeError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    print(f"reanchor_status={summary['reanchor_status']}")
    print(f"current_candidate_reanchor_sha256={summary['current_candidate_reanchor_sha256']}")
    rfs = summary.get("refreshed_current_candidate_sha256")
    if rfs:
        print(f"refreshed_current_candidate_sha256={rfs}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
