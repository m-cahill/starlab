"""CLI: emit full_local_training_campaign_contract.json + report (M49)."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from starlab.training.full_local_training_campaign_io import emit_full_local_training_campaign


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Emit governed full local training / bootstrap campaign contract + report (M49). "
            "Planning artifact only — does not execute the campaign."
        ),
    )
    parser.add_argument("--campaign-id", required=True, help="Stable campaign identifier.")
    parser.add_argument(
        "--output-dir",
        required=True,
        type=Path,
        help="Campaign root (e.g. out/training_campaigns/<campaign_id>/)",
    )
    parser.add_argument(
        "--hierarchical-training-run-dir",
        required=True,
        type=Path,
        help="M43 directory containing hierarchical_training_run.json and weights/",
    )
    parser.add_argument(
        "--benchmark-contract",
        required=True,
        type=Path,
        help="Path to M20 benchmark contract JSON (M28/M42 evaluation surface).",
    )
    parser.add_argument(
        "--match-config",
        required=True,
        type=Path,
        help="M02 match config JSON (adapter must match --runtime-mode).",
    )
    parser.add_argument(
        "--runtime-mode",
        required=True,
        choices=("fixture_stub_ci", "local_live_sc2"),
        help="Planned M44/M45 runtime mode for the campaign.",
    )
    parser.add_argument(
        "--training-program-contract",
        type=Path,
        default=None,
        help=(
            "Path to M40 agent_training_program_contract.json. If omitted, the default "
            "contract is written under output_dir/referenced_artifacts/m40_training_program/."
        ),
    )
    parser.add_argument(
        "--weights",
        type=Path,
        default=None,
        help="Override path to M43 joblib weights (default: <run-dir>/weights/...).",
    )
    parser.add_argument(
        "--dataset",
        type=Path,
        default=None,
        help="M26 replay_training_dataset.json (required with --planned-weighted-refit).",
    )
    parser.add_argument(
        "--bundle-dir",
        action="append",
        dest="bundle_dirs",
        type=Path,
        default=[],
        metavar="PATH",
        help="M14 bundle directory (repeat per bundle; required with --planned-weighted-refit).",
    )
    parser.add_argument(
        "--planned-weighted-refit",
        action="store_true",
        help="Declare planned M45 weighted re-fit (requires --dataset and --bundle-dir).",
    )
    parser.add_argument(
        "--campaign-protocol-json",
        type=Path,
        default=None,
        help="Optional JSON file overriding default campaign_protocol block.",
    )
    args = parser.parse_args(argv)

    protocol: dict[str, object] | None = None
    if args.campaign_protocol_json is not None:
        raw = json.loads(args.campaign_protocol_json.read_text(encoding="utf-8"))
        if not isinstance(raw, dict):
            print("error: --campaign-protocol-json must be a JSON object", file=sys.stderr)
            return 2
        protocol = raw

    try:
        sealed, _rep, c_path, r_path = emit_full_local_training_campaign(
            benchmark_contract_path=args.benchmark_contract,
            bundle_dirs=args.bundle_dirs or None,
            campaign_id=args.campaign_id,
            campaign_protocol=protocol,
            dataset_path=args.dataset,
            hierarchical_training_run_dir=args.hierarchical_training_run_dir,
            match_config_path=args.match_config,
            output_dir=args.output_dir,
            planned_weighted_refit=args.planned_weighted_refit,
            runtime_mode=args.runtime_mode,
            training_program_contract_path=args.training_program_contract,
            weights_path=args.weights,
        )
    except ValueError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2

    print(f"wrote {c_path}")
    print(f"wrote {r_path}")
    print(f"campaign_sha256={sealed['campaign_sha256']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
