"""CLI: emit campaign_observability_index.json + report (PV1-M01)."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from starlab.runs.json_util import canonical_json_dumps
from starlab.training.pv1_campaign_observability_models import (
    CAMPAIGN_OBSERVABILITY_INDEX_FILENAME,
    CAMPAIGN_OBSERVABILITY_INDEX_REPORT_FILENAME,
)
from starlab.training.pv1_campaign_observability_scan import load_campaign_id_from_contract_path
from starlab.training.pv1_campaign_observability_views import build_campaign_observability_index


def write_campaign_observability_index_artifacts(
    *,
    campaign_root: Path,
    output_dir: Path,
    campaign_contract: Path | None,
) -> tuple[Path, Path]:
    override: str | None = None
    if campaign_contract is not None and campaign_contract.is_file():
        override = load_campaign_id_from_contract_path(campaign_contract)

    index_body, report = build_campaign_observability_index(
        campaign_root=campaign_root,
        campaign_id_override=override,
    )
    output_dir.mkdir(parents=True, exist_ok=True)
    p1 = output_dir / CAMPAIGN_OBSERVABILITY_INDEX_FILENAME
    p2 = output_dir / CAMPAIGN_OBSERVABILITY_INDEX_REPORT_FILENAME
    p1.write_text(canonical_json_dumps(index_body), encoding="utf-8")
    p2.write_text(canonical_json_dumps(report), encoding="utf-8")
    return p1, p2


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="python -m starlab.training.emit_campaign_observability_index",
        description=(
            "PV1-M01: emit campaign_observability_index.json + report by scanning an existing "
            "campaign tree (inspection helper — does not fabricate missing receipts)."
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
        help="Directory for outputs (default: --campaign-root)",
    )
    parser.add_argument(
        "--campaign-contract",
        type=Path,
        default=None,
        help="Optional: alternate contract path for campaign_id label only",
    )
    args = parser.parse_args(argv)
    out = args.output_dir if args.output_dir is not None else args.campaign_root
    try:
        p1, p2 = write_campaign_observability_index_artifacts(
            campaign_root=args.campaign_root,
            output_dir=out,
            campaign_contract=args.campaign_contract,
        )
    except (OSError, ValueError) as exc:
        print(str(exc), file=sys.stderr)
        return 2
    print(f"wrote {p1}")
    print(f"wrote {p2}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
