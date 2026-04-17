"""CLI: emit pv1_post_campaign_readout.json + report (PV1-M04)."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from starlab.training.pv1_post_campaign_readout import write_pv1_post_campaign_readout_artifacts


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="python -m starlab.training.emit_pv1_post_campaign_readout",
        description=(
            "PV1-M04: emit deterministic post-campaign readout JSON + report from an existing "
            "campaign tree (aggregation only — does not execute campaigns or reinterpret "
            "thresholds)."
        ),
    )
    parser.add_argument(
        "--campaign-root",
        required=True,
        type=Path,
        help="Campaign directory (e.g. out/training_campaigns/<campaign_id>/)",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=None,
        help="Directory for readout outputs (default: same as --campaign-root)",
    )
    args = parser.parse_args(argv)
    out = args.output_dir if args.output_dir is not None else args.campaign_root
    try:
        p1, p2 = write_pv1_post_campaign_readout_artifacts(
            campaign_root=args.campaign_root,
            output_dir=out,
        )
    except (OSError, ValueError) as exc:
        print(str(exc), file=sys.stderr)
        return 2
    print(f"wrote {p1}")
    print(f"wrote {p2}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
