"""CLI: emit `live_sc2_in_ci_preflight_receipt.json` + report (M58)."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import cast

from starlab.runs.json_util import canonical_json_dumps
from starlab.sc2.live_sc2_ci_models import (
    LIVE_SC2_IN_CI_PREFLIGHT_RECEIPT_FILENAME,
    LIVE_SC2_IN_CI_PREFLIGHT_RECEIPT_REPORT_FILENAME,
)
from starlab.sc2.live_sc2_ci_preflight import (
    build_lock_denied_preflight_receipt,
    build_preflight_receipt_report,
    evaluate_live_sc2_in_ci_preflight,
)
from starlab.sc2.live_sc2_ci_preflight_lock import (
    release_m58_live_sc2_preflight_lock,
    try_acquire_m58_live_sc2_preflight_lock,
)
from starlab.sc2.local_live_play_validation_models import RuntimeMode


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Emit M58 live SC2-in-CI preflight receipt JSON.")
    p.add_argument("--m43-run", required=True, type=Path, help="M43 hierarchical training run dir")
    p.add_argument("--weights", required=True, type=Path, help="Explicit joblib weights path")
    p.add_argument("--match-config", required=True, type=Path, help="M02 match config JSON")
    p.add_argument(
        "--runtime-mode",
        required=True,
        choices=("fixture_stub_ci", "local_live_sc2"),
        help="Must align with M44 / match adapter policy.",
    )
    p.add_argument(
        "--workflow-trigger",
        default="workflow_dispatch",
        help="Expected trigger string (default: workflow_dispatch).",
    )
    p.add_argument(
        "--runner-labels",
        required=True,
        help='Comma-separated labels (e.g. "Windows,self-hosted,starlab-sc2").',
    )
    p.add_argument(
        "--timeout-minutes",
        required=True,
        type=int,
        help="Must be <= M58 guardrail max (30).",
    )
    p.add_argument(
        "--artifact-retention-days",
        required=True,
        type=int,
        help="Must be <= M58 guardrail max (7) for policy alignment in receipts.",
    )
    p.add_argument(
        "--live-sc2-confirmed",
        choices=("true", "false"),
        default="false",
        help='Must be "true" when runtime-mode is local_live_sc2.',
    )
    p.add_argument(
        "--output-dir",
        required=True,
        type=Path,
        help="Writes receipt/report JSON + uses advisory lock in this directory.",
    )
    p.add_argument(
        "--skip-advisory-lock",
        action="store_true",
        help="Test hook: do not acquire the M58 advisory lock (not for production workflows).",
    )
    args = p.parse_args(argv)

    live_ok = args.live_sc2_confirmed == "true"
    mode = cast(RuntimeMode, args.runtime_mode)

    out = args.output_dir
    out.mkdir(parents=True, exist_ok=True)

    if args.skip_advisory_lock:
        ok_eval, receipt, report, _ = evaluate_live_sc2_in_ci_preflight(
            m43_run_dir=args.m43_run,
            weights_path=args.weights,
            match_config=args.match_config,
            runtime_mode=mode,
            workflow_trigger=args.workflow_trigger,
            runner_labels_csv=args.runner_labels,
            timeout_minutes=args.timeout_minutes,
            artifact_retention_days=args.artifact_retention_days,
            live_sc2_confirmed=live_ok,
        )
        receipt["lock_acquired"] = False
        receipt["lock_denial_message"] = None
        report = build_preflight_receipt_report(receipt_obj=receipt)
        rp = out / LIVE_SC2_IN_CI_PREFLIGHT_RECEIPT_FILENAME
        rr = out / LIVE_SC2_IN_CI_PREFLIGHT_RECEIPT_REPORT_FILENAME
        rp.write_text(canonical_json_dumps(receipt), encoding="utf-8")
        rr.write_text(canonical_json_dumps(report), encoding="utf-8")
        print(f"Wrote {rp}")
        print(f"Wrote {rr}")
        return 0 if ok_eval else 1

    ok_lock, lock_path, lmsg = try_acquire_m58_live_sc2_preflight_lock(output_dir=out)
    if not ok_lock:
        receipt, report = build_lock_denied_preflight_receipt(
            workflow_trigger=args.workflow_trigger,
            runner_labels_csv=args.runner_labels,
            lock_denial_message=lmsg,
        )
        rp = out / LIVE_SC2_IN_CI_PREFLIGHT_RECEIPT_FILENAME
        rr = out / LIVE_SC2_IN_CI_PREFLIGHT_RECEIPT_REPORT_FILENAME
        rp.write_text(canonical_json_dumps(receipt), encoding="utf-8")
        rr.write_text(canonical_json_dumps(report), encoding="utf-8")
        print(f"Wrote {rp}")
        print(f"Wrote {rr}")
        return 1

    try:
        ok_eval, receipt, report, _ = evaluate_live_sc2_in_ci_preflight(
            m43_run_dir=args.m43_run,
            weights_path=args.weights,
            match_config=args.match_config,
            runtime_mode=mode,
            workflow_trigger=args.workflow_trigger,
            runner_labels_csv=args.runner_labels,
            timeout_minutes=args.timeout_minutes,
            artifact_retention_days=args.artifact_retention_days,
            live_sc2_confirmed=live_ok,
        )
    finally:
        release_m58_live_sc2_preflight_lock(lock_path)

    rp = out / LIVE_SC2_IN_CI_PREFLIGHT_RECEIPT_FILENAME
    rr = out / LIVE_SC2_IN_CI_PREFLIGHT_RECEIPT_REPORT_FILENAME
    rp.write_text(canonical_json_dumps(receipt), encoding="utf-8")
    rr.write_text(canonical_json_dumps(report), encoding="utf-8")
    print(f"Wrote {rp}")
    print(f"Wrote {rr}")
    return 0 if ok_eval else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
