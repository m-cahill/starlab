"""CLI: emit V15-M09 checkpoint promotion decision from a sealed or unsealed evaluation JSON."""

from __future__ import annotations

import argparse
from pathlib import Path

from starlab.v15.checkpoint_evaluation_io import emit_v15_checkpoint_promotion_decision


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Emit v15 checkpoint promotion decision from a checkpoint evaluation JSON.",
    )
    parser.add_argument(
        "--evaluation-json", required=True, type=Path, help="v15_checkpoint_evaluation.json"
    )
    parser.add_argument(
        "--output-dir", required=True, type=Path, help="Directory for promotion decision JSON."
    )
    parser.add_argument(
        "--allow-operator-local-promotion-decision",
        action="store_true",
        help="Optional guard acknowledgement (emission still bounded by M09).",
    )
    parser.add_argument(
        "--authorize-checkpoint-promotion-decision",
        action="store_true",
        help="Optional second guard acknowledgement.",
    )
    args = parser.parse_args(argv)
    a = args.allow_operator_local_promotion_decision
    b = args.authorize_checkpoint_promotion_decision
    if a != b:
        print(
            "error: if using guards, pass both --allow-operator-local-promotion-decision and "
            "--authorize-checkpoint-promotion-decision",
            flush=True,
        )
        return 2
    if not args.evaluation_json.is_file():
        print(f"error: --evaluation-json not found: {args.evaluation_json}", flush=True)
        return 2
    _s, _r, _c, _r2, rc = emit_v15_checkpoint_promotion_decision(
        args.output_dir, args.evaluation_json
    )
    print(f"redaction_count={rc}", flush=True)
    if a and b:
        print(
            "info: operator promotion guards recorded on CLI; artifact remains governance-bounded",
            flush=True,
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
