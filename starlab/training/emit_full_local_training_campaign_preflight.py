"""CLI: run M49 full local training campaign preflight and emit receipt."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from starlab.training.full_local_training_campaign_preflight import (
    run_campaign_preflight,
    write_preflight_receipt,
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Deterministic preflight for a full_local_training_campaign_contract.json. "
            "Emits campaign_preflight_receipt.json under --output-dir."
        ),
    )
    parser.add_argument(
        "--campaign-contract",
        required=True,
        type=Path,
        help="Path to full_local_training_campaign_contract.json",
    )
    parser.add_argument(
        "--output-dir",
        required=True,
        type=Path,
        help="Directory for campaign_preflight_receipt.json (e.g. same as campaign root).",
    )
    args = parser.parse_args(argv)

    try:
        ok, receipt = run_campaign_preflight(contract_path=args.campaign_contract)
    except (OSError, ValueError) as e:
        print(f"error: {e}", file=sys.stderr)
        return 2

    out_path = write_preflight_receipt(output_dir=args.output_dir, receipt=receipt)
    print(f"wrote {out_path}")
    print(f"preflight_ok={receipt['preflight_ok']}")
    return 0 if ok else 3


if __name__ == "__main__":
    raise SystemExit(main())
