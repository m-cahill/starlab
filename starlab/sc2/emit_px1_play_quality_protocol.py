"""CLI: emit px1_play_quality_protocol.json + report (PX1-M02)."""

from __future__ import annotations

import argparse
import hashlib
import sys
from pathlib import Path

from starlab._io import load_json_object_strict
from starlab.runs.json_util import canonical_json_dumps
from starlab.sc2.px1_play_quality_models import (
    PX1_PLAY_QUALITY_PROTOCOL_FILENAME,
    PX1_PLAY_QUALITY_PROTOCOL_REPORT_FILENAME,
)
from starlab.sc2.px1_play_quality_protocol import px1_play_quality_protocol_bundle


def _sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def write_px1_play_quality_protocol_artifacts(
    *,
    input_path: Path,
    output_dir: Path,
) -> tuple[Path, Path]:
    raw = input_path.read_bytes()
    input_sha256 = _sha256_bytes(raw)
    obj = load_json_object_strict(input_path)
    protocol, report = px1_play_quality_protocol_bundle(
        input_obj=obj,
        input_sha256=input_sha256,
    )
    output_dir.mkdir(parents=True, exist_ok=True)
    p_path = output_dir / PX1_PLAY_QUALITY_PROTOCOL_FILENAME
    r_path = output_dir / PX1_PLAY_QUALITY_PROTOCOL_REPORT_FILENAME
    p_path.write_text(canonical_json_dumps(protocol), encoding="utf-8")
    r_path.write_text(canonical_json_dumps(report), encoding="utf-8")
    return p_path, r_path


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(
        description=(
            "Emit deterministic px1_play_quality_protocol.json + report (PX1-M02 — bounded "
            "play-quality evaluation protocol freeze)."
        ),
    )
    p.add_argument(
        "--input",
        type=Path,
        required=True,
        help="JSON file with protocol fields (candidate pool, opponent profiles, frozen params).",
    )
    p.add_argument(
        "--output-dir",
        type=Path,
        default=Path("."),
        help="Directory for protocol + report JSON (default: cwd).",
    )
    args = p.parse_args(argv)
    try:
        out_p, out_r = write_px1_play_quality_protocol_artifacts(
            input_path=args.input,
            output_dir=args.output_dir,
        )
    except (OSError, TypeError, ValueError) as exc:
        print(str(exc), file=sys.stderr)
        return 1
    print(f"Wrote {out_p}")
    print(f"Wrote {out_r}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
