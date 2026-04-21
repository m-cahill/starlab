"""CLI: bounded post–pointer-seeded handoff (PX2-M03 slice 15)."""

from __future__ import annotations

import argparse
from pathlib import Path

from starlab.sc2.px2.self_play.pointer_seeded_handoff import (
    HANDOFF_OK,
    run_bounded_pointer_seeded_handoff,
)


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(
        description=(
            "PX2 slice-15 bounded handoff: validate successful slice-14 "
            "`px2_self_play_pointer_seeded_run.json` and emit governed "
            "`px2_self_play_pointer_seeded_handoff.json`; not industrial campaign; "
            "not PX2-M04; not merge-gate CI."
        ),
    )
    p.add_argument("--campaign-root", type=Path, required=True)
    p.add_argument("--campaign-id", type=str, required=True)
    args = p.parse_args(argv)

    summary = run_bounded_pointer_seeded_handoff(
        campaign_root=args.campaign_root.resolve(),
        campaign_id=args.campaign_id,
    )
    print(f"handoff_status={summary['handoff_status']}")
    print(f"pointer_seeded_handoff_sha256={summary['pointer_seeded_handoff_sha256']}")
    return 0 if summary["handoff_status"] == HANDOFF_OK else 1


if __name__ == "__main__":
    raise SystemExit(main())
