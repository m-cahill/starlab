"""CLI: emit ladder_public_evaluation_evidence.json + report (M59)."""

from __future__ import annotations

import argparse
import hashlib
import sys
from pathlib import Path

from starlab._io import load_json_object_strict
from starlab.runs.json_util import canonical_json_dumps
from starlab.sc2.ladder_public_evaluation_evidence import ladder_public_evaluation_evidence_bundle
from starlab.sc2.ladder_public_evaluation_models import (
    LADDER_PUBLIC_EVALUATION_EVIDENCE_FILENAME,
    LADDER_PUBLIC_EVALUATION_EVIDENCE_REPORT_FILENAME,
)


def _sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def write_ladder_public_evaluation_evidence_artifacts(
    *,
    protocol_path: Path,
    result_rows_path: Path,
    output_dir: Path,
) -> tuple[Path, Path]:
    protocol_obj = load_json_object_strict(protocol_path)
    raw = result_rows_path.read_bytes()
    result_sha256 = _sha256_bytes(raw)
    result_input_obj = load_json_object_strict(result_rows_path)
    evidence, report = ladder_public_evaluation_evidence_bundle(
        protocol_obj=protocol_obj,
        result_input_obj=result_input_obj,
        result_input_sha256=result_sha256,
    )
    output_dir.mkdir(parents=True, exist_ok=True)
    e_path = output_dir / LADDER_PUBLIC_EVALUATION_EVIDENCE_FILENAME
    r_path = output_dir / LADDER_PUBLIC_EVALUATION_EVIDENCE_REPORT_FILENAME
    e_path.write_text(canonical_json_dumps(evidence), encoding="utf-8")
    r_path.write_text(canonical_json_dumps(report), encoding="utf-8")
    return e_path, r_path


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(
        description=(
            "Emit deterministic ladder_public_evaluation_evidence.json + report from a protocol "
            "artifact and a result-rows JSON file (M59 — descriptive evidence only)."
        )
    )
    p.add_argument(
        "--protocol",
        type=Path,
        required=True,
        help="Path to ladder_public_evaluation_protocol.json (emitted by protocol emitter).",
    )
    p.add_argument(
        "--result-rows",
        type=Path,
        required=True,
        help="JSON file with evidence_session_id and result_rows array.",
    )
    p.add_argument(
        "--output-dir",
        type=Path,
        default=Path("."),
        help="Directory for evidence + report JSON (default: cwd).",
    )
    args = p.parse_args(argv)
    try:
        e, r = write_ladder_public_evaluation_evidence_artifacts(
            output_dir=args.output_dir,
            protocol_path=args.protocol,
            result_rows_path=args.result_rows,
        )
    except (OSError, TypeError, ValueError) as exc:
        print(str(exc), file=sys.stderr)
        return 1
    print(f"Wrote {e}")
    print(f"Wrote {r}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
