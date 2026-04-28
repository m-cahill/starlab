"""V15-M08: operator-local wrapper around M49–M51 execute_full_local_training_campaign (guarded)."""

from __future__ import annotations

import argparse
import json
import sys
import uuid
from pathlib import Path
from typing import Any

from starlab.runs.json_util import sha256_hex_of_canonical_json
from starlab.v15.long_gpu_training_manifest_io import (
    long_campaign_execution_allowed,
    validate_campaign_plan,
)
from starlab.v15.long_gpu_training_manifest_models import MILESTONE_ID_V15_M08


def _load_manifest(path: Path) -> dict[str, Any]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ValueError("manifest must be a JSON object")
    return raw


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="python -m starlab.v15.run_v15_long_gpu_campaign",
        description=(
            "V15-M08 operator-local long GPU campaign runner. Wraps "
            "starlab.training.execute_full_local_training_campaign. Requires explicit guards."
        ),
    )
    parser.add_argument(
        "--campaign-manifest-json",
        required=True,
        type=Path,
        help="Sealed v15_long_gpu_training_manifest.json from preflight.",
    )
    parser.add_argument(
        "--campaign-plan-json",
        required=True,
        type=Path,
        help="campaign_plan.json (must match manifest campaign_plan_sha256).",
    )
    parser.add_argument(
        "--output-root",
        required=True,
        type=Path,
        help="Campaign output root (e.g. out/v15_m08_campaigns/<campaign_id>).",
    )
    parser.add_argument(
        "--allow-operator-local-execution",
        action="store_true",
        help="Required guard: confirms intentional operator-local execution.",
    )
    parser.add_argument(
        "--authorize-long-gpu-campaign",
        action="store_true",
        help="Required guard: authorizes this milestone's long campaign attempt.",
    )
    parser.add_argument(
        "--max-wall-clock-minutes",
        type=float,
        default=None,
        metavar="MINUTES",
        help="Forwarded to execute_full_local_training_campaign (between-phase budget).",
    )
    parser.add_argument(
        "--run-tier",
        type=str,
        default=None,
        help="Forwarded to execute_full_local_training_campaign (artifact metadata only).",
    )
    parser.add_argument(
        "--governance-override-m07-shakedown",
        action="store_true",
        help=(
            "Explicit governance override when M07 GPU shakedown receipt is absent "
            "(recorded in process environment only — use rarely)."
        ),
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Validate guards + preflight only; do not invoke M50 executor.",
    )
    parser.add_argument(
        "--execution-id",
        type=str,
        default=None,
        help="Optional execution id forwarded to M50 (default: random uuid).",
    )
    parser.add_argument(
        "--post-bootstrap-protocol-phases",
        action="store_true",
        help="Forwarded to execute_full_local_training_campaign when not dry-run.",
    )
    args = parser.parse_args(argv)

    if not args.allow_operator_local_execution or not args.authorize_long_gpu_campaign:
        sys.stderr.write(
            "error: both --allow-operator-local-execution and "
            "--authorize-long-gpu-campaign are required\n",
        )
        return 2

    try:
        manifest = _load_manifest(args.campaign_manifest_json.resolve())
        plan_raw = json.loads(args.campaign_plan_json.read_text(encoding="utf-8"))
        plan = validate_campaign_plan(plan_raw)
    except (OSError, json.JSONDecodeError, ValueError) as e:
        sys.stderr.write(f"error: {e}\n")
        return 1

    if str(manifest.get("milestone", "")) != MILESTONE_ID_V15_M08:
        sys.stderr.write("error: manifest milestone must be V15-M08\n")
        return 1

    plan_sha = sha256_hex_of_canonical_json(plan)
    bound = str(manifest.get("campaign_plan_sha256", ""))
    if bound != plan_sha:
        sys.stderr.write(
            "error: campaign_plan_sha256 mismatch between manifest and campaign_plan.json\n",
        )
        return 1

    gates = manifest.get("gate_statuses")
    if not isinstance(gates, dict):
        sys.stderr.write("error: manifest gate_statuses missing or invalid\n")
        return 1

    ok, blockers = long_campaign_execution_allowed(
        gates,
        governance_override_missing_m07_gpu_shakedown=bool(
            args.governance_override_m07_shakedown,
        ),
    )
    if not ok:
        sys.stderr.write("preflight blocked; gate blockers:\n")
        for b in blockers:
            sys.stderr.write(f"  - {b}\n")
        return 6

    contract_s = plan.get("m49_full_local_training_campaign_contract_path")
    if not isinstance(contract_s, str) or not contract_s.strip():
        sys.stderr.write(
            "error: campaign plan missing m49_full_local_training_campaign_contract_path\n"
        )
        return 1
    contract_path = Path(contract_s)
    if not contract_path.is_file():
        sys.stderr.write(f"error: M49 contract not found: {contract_path}\n")
        return 1

    root_s = plan.get("m49_campaign_root")
    campaign_root = (
        Path(root_s).resolve()
        if isinstance(root_s, str) and root_s.strip()
        else contract_path.parent.resolve()
    )

    args.output_root.mkdir(parents=True, exist_ok=True)

    if args.dry_run:
        sys.stdout.write("dry-run: preflight OK; would invoke M50 executor\n")
        return 0

    execution_id = args.execution_id or str(uuid.uuid4())
    exec_argv = [
        "--campaign-contract",
        str(contract_path.resolve()),
        "--campaign-root",
        str(campaign_root),
        "--execution-id",
        execution_id,
    ]
    if args.post_bootstrap_protocol_phases:
        exec_argv.append("--post-bootstrap-protocol-phases")
    if args.max_wall_clock_minutes is not None:
        exec_argv.extend(["--max-wall-clock-minutes", str(args.max_wall_clock_minutes)])
    if args.run_tier:
        exec_argv.extend(["--run-tier", args.run_tier])

    from starlab.training.execute_full_local_training_campaign import main as m50_main

    return int(m50_main(exec_argv))


if __name__ == "__main__":
    raise SystemExit(main())
