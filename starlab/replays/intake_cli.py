"""CLI: replay intake policy gate (M07).

Treats replay files as opaque bytes. Does not parse replay semantics (M08+).
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from starlab.replays.intake_io import (
    exit_code_for_status,
    run_replay_intake,
    write_intake_artifacts,
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Evaluate replay intake metadata and emit governed receipt/report JSON (M07). "
            "Replay bytes are opaque; no parser semantics."
        ),
    )
    parser.add_argument(
        "--replay",
        required=True,
        type=Path,
        help="Path to replay file (opaque bytes)",
    )
    parser.add_argument(
        "--metadata",
        required=True,
        type=Path,
        help="Path to replay_intake_metadata.json",
    )
    parser.add_argument(
        "--output-dir",
        required=True,
        type=Path,
        help="Directory to write replay_intake_receipt.json and replay_intake_report.json",
    )
    parser.add_argument(
        "--replay-binding",
        type=Path,
        default=None,
        help="Optional path to M04 replay_binding.json",
    )
    parser.add_argument(
        "--run-identity",
        type=Path,
        default=None,
        help="Optional path to M03 run_identity.json",
    )
    parser.add_argument(
        "--run-artifact-manifest",
        type=Path,
        default=None,
        help="Optional path to M05 manifest.json",
    )
    ns = parser.parse_args(argv)

    outcome, receipt, report = run_replay_intake(
        manifest_path=ns.run_artifact_manifest,
        metadata_path=ns.metadata,
        replay_binding_path=ns.replay_binding,
        replay_path=ns.replay,
        run_identity_path=ns.run_identity,
    )
    write_intake_artifacts(output_dir=ns.output_dir, receipt=receipt, report=report)
    code = exit_code_for_status(outcome.intake_status)
    return code


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
