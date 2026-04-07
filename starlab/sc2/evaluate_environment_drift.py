"""CLI: evaluate probe JSON against governed runtime smoke matrix (M06)."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from starlab.sc2.environment_drift import emit_m06_artifacts, matrix_to_json, report_to_json
from starlab.sc2.runtime_smoke_matrix import CI_PROFILE, LOCAL_PROFILE


def _load_json_object(path: Path, *, label: str) -> dict[str, Any]:
    raw = path.read_text(encoding="utf-8")
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        msg = f"{label}: invalid JSON ({e})"
        raise ValueError(msg) from e
    if not isinstance(data, dict):
        msg = f"{label}: root must be a JSON object"
        raise ValueError(msg)
    return data


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="STARLAB M06: evaluate environment probe against runtime smoke matrix.",
    )
    parser.add_argument(
        "--probe",
        required=True,
        type=Path,
        help="Path to observed probe_result.json (M01 probe surface)",
    )
    parser.add_argument(
        "--output-dir",
        required=True,
        type=Path,
        help="Directory to write runtime_smoke_matrix.json and environment_drift_report.json",
    )
    parser.add_argument(
        "--run-identity",
        type=Path,
        default=None,
        help="Optional path to run_identity.json for environment_fingerprint comparison",
    )
    parser.add_argument(
        "--profile",
        choices=(CI_PROFILE, LOCAL_PROFILE),
        default=CI_PROFILE,
        help=f"Smoke profile (default: {CI_PROFILE})",
    )
    args = parser.parse_args(argv)

    try:
        probe = _load_json_object(args.probe, label="probe")
        run_identity: dict[str, Any] | None = None
        if args.run_identity is not None:
            run_identity = _load_json_object(args.run_identity, label="run_identity")
        matrix, report = emit_m06_artifacts(
            probe=probe,
            profile=args.profile,
            run_identity=run_identity,
        )
    except (OSError, ValueError) as e:
        print(str(e), file=sys.stderr)
        return 1

    out_dir = args.output_dir
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "runtime_smoke_matrix.json").write_text(
        matrix_to_json(matrix),
        encoding="utf-8",
    )
    (out_dir / "environment_drift_report.json").write_text(
        report_to_json(report),
        encoding="utf-8",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
