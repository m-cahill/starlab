"""CLI: emit tranche_checkpoint_receipt.json + report (PV1-M01)."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from starlab.runs.json_util import canonical_json_dumps
from starlab.training.pv1_campaign_observability_models import (
    TRANCHE_CHECKPOINT_RECEIPT_FILENAME,
    TRANCHE_CHECKPOINT_RECEIPT_REPORT_FILENAME,
)
from starlab.training.pv1_campaign_observability_scan import load_campaign_id_from_contract_path
from starlab.training.pv1_campaign_observability_views import build_tranche_checkpoint_receipt


def write_tranche_checkpoint_receipt_artifacts(
    *,
    campaign_root: Path,
    output_dir: Path,
    tranche_id: str,
    checkpoint_id: str,
    operator_paused: bool,
    operator_incomplete: bool,
    operator_note: str | None,
    operator_note_ref: str | None,
    campaign_contract: Path | None,
) -> tuple[Path, Path]:
    override: str | None = None
    if campaign_contract is not None and campaign_contract.is_file():
        override = load_campaign_id_from_contract_path(campaign_contract)

    receipt, report = build_tranche_checkpoint_receipt(
        campaign_root=campaign_root,
        tranche_id=tranche_id,
        checkpoint_id=checkpoint_id,
        operator_paused=operator_paused,
        operator_incomplete=operator_incomplete,
        operator_note=operator_note,
        operator_note_ref=operator_note_ref,
        campaign_id_override=override,
    )
    output_dir.mkdir(parents=True, exist_ok=True)
    p1 = output_dir / TRANCHE_CHECKPOINT_RECEIPT_FILENAME
    p2 = output_dir / TRANCHE_CHECKPOINT_RECEIPT_REPORT_FILENAME
    p1.write_text(canonical_json_dumps(receipt), encoding="utf-8")
    p2.write_text(canonical_json_dumps(report), encoding="utf-8")
    return p1, p2


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="python -m starlab.training.emit_tranche_checkpoint_receipt",
        description=(
            "PV1-M01: emit tranche_checkpoint_receipt.json + "
            "tranche_checkpoint_receipt_report.json by scanning an existing campaign tree "
            "(inspection helper — does not create execution evidence)."
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
    parser.add_argument("--tranche-id", required=True, help="Tranche label (e.g. tranche_a)")
    parser.add_argument("--checkpoint-id", required=True, help="Checkpoint name (e.g. close_001)")
    parser.add_argument(
        "--campaign-contract",
        type=Path,
        default=None,
        help="Optional: alternate full_local_training_campaign_contract.json for campaign_id only",
    )
    parser.add_argument(
        "--paused",
        action="store_true",
        help="Operator-declared pause posture at this checkpoint",
    )
    parser.add_argument(
        "--incomplete",
        action="store_true",
        help="Operator-declared incomplete posture at this checkpoint",
    )
    parser.add_argument("--operator-note", default=None, help="Inline operator note string")
    parser.add_argument(
        "--operator-note-ref",
        type=Path,
        default=None,
        help="Relative path to an operator note file under campaign root (stored as POSIX string)",
    )
    args = parser.parse_args(argv)

    out = args.output_dir if args.output_dir is not None else args.campaign_root
    note_ref: str | None = None
    if args.operator_note_ref is not None:
        try:
            note_ref = args.operator_note_ref.as_posix()
        except ValueError:
            note_ref = str(args.operator_note_ref)

    try:
        p1, p2 = write_tranche_checkpoint_receipt_artifacts(
            campaign_root=args.campaign_root,
            output_dir=out,
            tranche_id=args.tranche_id,
            checkpoint_id=args.checkpoint_id,
            operator_paused=args.paused,
            operator_incomplete=args.incomplete,
            operator_note=args.operator_note,
            operator_note_ref=note_ref,
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
