"""CLI: emit px1_demo_readiness_evidence.json + report (PX1-M03)."""

from __future__ import annotations

import argparse
import hashlib
import sys
from pathlib import Path

from starlab._io import load_json_object_strict
from starlab.runs.json_util import canonical_json_dumps
from starlab.sc2.px1_demo_readiness_evidence import px1_demo_readiness_evidence_bundle
from starlab.sc2.px1_demo_readiness_models import (
    PX1_DEMO_READINESS_EVIDENCE_FILENAME,
    PX1_DEMO_READINESS_EVIDENCE_REPORT_FILENAME,
)


def _sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def write_px1_demo_readiness_evidence_artifacts(
    *,
    protocol_path: Path,
    evaluation_input_path: Path,
    output_dir: Path,
) -> tuple[Path, Path]:
    protocol_obj = load_json_object_strict(protocol_path)
    raw = evaluation_input_path.read_bytes()
    eval_sha = _sha256_bytes(raw)
    eval_obj = load_json_object_strict(evaluation_input_path)
    evidence, report = px1_demo_readiness_evidence_bundle(
        protocol_obj=protocol_obj,
        evaluation_input_obj=eval_obj,
        evaluation_input_sha256=eval_sha,
    )
    output_dir.mkdir(parents=True, exist_ok=True)
    e_path = output_dir / PX1_DEMO_READINESS_EVIDENCE_FILENAME
    r_path = output_dir / PX1_DEMO_READINESS_EVIDENCE_REPORT_FILENAME
    e_path.write_text(canonical_json_dumps(evidence), encoding="utf-8")
    r_path.write_text(canonical_json_dumps(report), encoding="utf-8")
    return e_path, r_path


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(
        description=(
            "Emit deterministic px1_demo_readiness_evidence.json + report from a protocol artifact "
            "and an evaluation-results JSON file (PX1-M03)."
        ),
    )
    p.add_argument(
        "--protocol",
        type=Path,
        required=True,
        help="Path to px1_demo_readiness_protocol.json (emitted by protocol emitter).",
    )
    p.add_argument(
        "--evaluation-input",
        type=Path,
        required=True,
        help="JSON file with evaluation_series_id, candidates_evaluated, selection.",
    )
    p.add_argument(
        "--output-dir",
        type=Path,
        default=Path("."),
        help="Directory for evidence + report JSON (default: cwd).",
    )
    args = p.parse_args(argv)
    try:
        e, r = write_px1_demo_readiness_evidence_artifacts(
            output_dir=args.output_dir,
            protocol_path=args.protocol,
            evaluation_input_path=args.evaluation_input,
        )
    except (OSError, TypeError, ValueError) as exc:
        print(str(exc), file=sys.stderr)
        return 1
    print(f"Wrote {e}")
    print(f"Wrote {r}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
