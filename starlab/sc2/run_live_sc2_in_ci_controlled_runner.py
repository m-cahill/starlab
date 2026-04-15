"""CLI: M57 controlled runner — one M44 validation + receipt/report JSON."""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

from starlab.runs.json_util import canonical_json_dumps
from starlab.sc2.live_sc2_ci_controlled_runner import run_m57_controlled_runner
from starlab.sc2.live_sc2_ci_models import (
    LIVE_SC2_IN_CI_CONTROLLED_RUNNER_RECEIPT_FILENAME,
    LIVE_SC2_IN_CI_CONTROLLED_RUNNER_RECEIPT_REPORT_FILENAME,
)


def _parse_labels(raw: str | None) -> list[str]:
    if not raw or not raw.strip():
        return []
    return [x.strip() for x in raw.split(",") if x.strip()]


def _workflow_trigger_default() -> str:
    return os.environ.get("GITHUB_EVENT_NAME", "cli")


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(
        description=(
            "M57 controlled runner: one bounded M44 local_live_play_validation run + "
            "live_sc2_in_ci_controlled_runner receipt JSON."
        )
    )
    p.add_argument("--m43-run", required=True, type=Path, help="M43 hierarchical training run dir")
    p.add_argument("--weights", type=Path, default=None, help="Explicit joblib weights path")
    p.add_argument("--match-config", required=True, type=Path, help="M02 match config JSON")
    p.add_argument("--output-dir", required=True, type=Path, help="M44 output root + receipt dir")
    p.add_argument(
        "--runtime-mode",
        required=True,
        choices=("fixture_stub_ci", "local_live_sc2"),
        help="Must match M44 semantics; adapter must match mode (fake vs burnysc2).",
    )
    p.add_argument(
        "--requested-runner-posture",
        default="cli_manual",
        choices=("cli_manual", "github_workflow_dispatch"),
        help="Requested posture; resolved posture may differ when workflow_dispatch is used.",
    )
    p.add_argument(
        "--workflow-trigger",
        default=None,
        help="Override workflow trigger string (default: GITHUB_EVENT_NAME or 'cli').",
    )
    p.add_argument(
        "--runner-labels",
        default=None,
        help="Comma-separated runner labels (e.g. self-hosted, sc2).",
    )
    p.add_argument(
        "--skip-live-when-prereqs-missing",
        action="store_true",
        help=(
            "If local_live_sc2 and SC2 binary is unavailable, emit skipped_by_policy receipt "
            "instead of failing. (Env STARLAB_M57_SKIP_LIVE_WHEN_PREREQS_MISSING=1 is equivalent.)"
        ),
    )
    args = p.parse_args(argv)

    wf = args.workflow_trigger if args.workflow_trigger is not None else _workflow_trigger_default()
    try:
        result = run_m57_controlled_runner(
            match_config=args.match_config,
            m43_run_dir=args.m43_run,
            output_dir=args.output_dir,
            requested_runner_posture=args.requested_runner_posture,
            runner_labels=_parse_labels(args.runner_labels),
            runtime_mode=args.runtime_mode,
            skip_live_when_prereqs_missing=args.skip_live_when_prereqs_missing,
            weights=args.weights,
            workflow_trigger=wf,
        )
    except (OSError, RuntimeError, ValueError) as exc:
        sys.stderr.write(f"{exc}\n")
        return 1

    out = args.output_dir
    out.mkdir(parents=True, exist_ok=True)
    rp = out / LIVE_SC2_IN_CI_CONTROLLED_RUNNER_RECEIPT_FILENAME
    rr = out / LIVE_SC2_IN_CI_CONTROLLED_RUNNER_RECEIPT_REPORT_FILENAME
    rp.write_text(canonical_json_dumps(result.receipt), encoding="utf-8")
    rr.write_text(canonical_json_dumps(result.report), encoding="utf-8")
    print(f"Wrote {rp}")
    print(f"Wrote {rr}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
