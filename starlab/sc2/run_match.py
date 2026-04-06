"""CLI: bounded match harness (M02)."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from starlab.sc2.artifacts import execution_proof_to_json
from starlab.sc2.harness import run_match_execution
from starlab.sc2.match_config import load_match_config


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="STARLAB bounded SC2 match harness (M02). Use adapter=fake in CI without SC2.",
    )
    parser.add_argument(
        "--config",
        required=True,
        type=Path,
        help="Path to match config JSON file.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=None,
        help="Directory for match_execution_proof.json (and optional replay).",
    )
    parser.add_argument(
        "--redact",
        action="store_true",
        help="Redact replay path fields in written JSON.",
    )
    args = parser.parse_args(argv)

    try:
        cfg = load_match_config(args.config)
    except (OSError, ValueError, json.JSONDecodeError) as e:
        print(f"config error: {e}", file=sys.stderr)
        return 1

    out_dir = args.output_dir
    result = run_match_execution(cfg, output_dir=out_dir)
    if not result.ok or result.proof is None:
        print(result.message or "harness failed", file=sys.stderr)
        return 2

    text = execution_proof_to_json(result.proof, redact=args.redact)
    if out_dir is not None:
        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / "match_execution_proof.json").write_text(text, encoding="utf-8")
    else:
        sys.stdout.write(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
