"""CLI: V15-M38 two-hour run remediation & launch rehearsal."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from starlab.v15.m38_two_hour_run_remediation_launch_rehearsal_io import (
    emit_m38_fixture,
    emit_m38_operator_preflight,
    emit_m38_operator_rehearsal,
)


def main(argv: list[str] | None = None) -> int:
    repo_root = Path(__file__).resolve().parents[2]

    parser = argparse.ArgumentParser(
        description=(
            "V15-M38: M37 remediation; freeze M39 launch command/runbook; optional rehearsal. "
            "Does not execute the 2-hour run."
        ),
    )
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument(
        "--fixture-ci",
        action="store_true",
        help="Deterministic fixture artifacts (CI-safe; no operator inputs).",
    )
    mode.add_argument(
        "--profile",
        type=str,
        choices=("operator_preflight", "operator_local_rehearsal"),
        help="Operator-local profile.",
    )
    parser.add_argument(
        "--m37-blocker-discovery-json",
        type=Path,
        default=None,
        help="Sealed M37 v15_two_hour_run_blocker_discovery.json (required for operator profiles).",
    )
    parser.add_argument(
        "--m37-remediation-map",
        type=Path,
        default=None,
        help="Optional M37 v15_m38_remediation_map.md (weak authority vs sealed JSON).",
    )
    parser.add_argument(
        "--m37-m39-runbook-draft",
        type=Path,
        default=None,
        help="Optional M37 v15_m39_candidate_runbook_draft.md.",
    )
    parser.add_argument(
        "--allow-operator-local-execution",
        action="store_true",
        help="Required with rehearsal profile.",
    )
    parser.add_argument(
        "--authorize-m39-launch-rehearsal",
        action="store_true",
        help="Explicit guard for bounded local rehearsal (no training).",
    )
    parser.add_argument(
        "--max-rehearsal-seconds",
        type=float,
        default=60.0,
        help="Upper bound for rehearsal subprocess budget (default 60).",
    )
    parser.add_argument("--output-dir", type=Path, required=True)

    args = parser.parse_args(argv)
    out = args.output_dir.resolve()

    if args.fixture_ci:
        emit_m38_fixture(out, repo_root=repo_root)
        return 0

    if args.m37_blocker_discovery_json is None:
        sys.stderr.write("error: --m37-blocker-discovery-json is required\n")
        return 2

    if args.profile == "operator_preflight":
        emit_m38_operator_preflight(
            out,
            repo_root=repo_root,
            m37_blocker_discovery_json=args.m37_blocker_discovery_json,
            m37_remediation_map_md=args.m37_remediation_map,
            m37_m39_runbook_draft_md=args.m37_m39_runbook_draft,
        )
        return 0

    if args.profile == "operator_local_rehearsal":
        if not (args.allow_operator_local_execution and args.authorize_m39_launch_rehearsal):
            sys.stderr.write(
                "error: rehearsal requires "
                "--allow-operator-local-execution and --authorize-m39-launch-rehearsal\n",
            )
            return 2
        emit_m38_operator_rehearsal(
            out,
            repo_root=repo_root,
            m37_blocker_discovery_json=args.m37_blocker_discovery_json,
            max_rehearsal_seconds=float(args.max_rehearsal_seconds),
            m37_remediation_map_md=args.m37_remediation_map,
            m37_m39_runbook_draft_md=args.m37_m39_runbook_draft,
        )
        return 0

    sys.stderr.write("error: unexpected profile\n")
    return 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
