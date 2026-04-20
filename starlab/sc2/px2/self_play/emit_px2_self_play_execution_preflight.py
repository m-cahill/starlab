"""CLI: emit operator-local execution preflight JSON (PX2-M03 slice 3)."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from starlab.sc2.px2.self_play.execution_preflight import run_execution_preflight
from starlab.sc2.px2.self_play.run_artifacts import write_json


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(
        description="PX2 operator-local execution preflight (readiness receipt only).",
    )
    p.add_argument("--output-dir", type=Path, required=True)
    p.add_argument("--corpus-root", type=Path, required=True)
    p.add_argument("--run-id", default=None)
    p.add_argument("--torch-seed", type=int, default=42)
    p.add_argument("--device-intent", default="cpu", help="cpu | cuda_optional")
    p.add_argument("--map-location", default="cpu")
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--init-only", action="store_true", help="Deterministic init; no weights file.")
    g.add_argument("--weights", type=Path, help="Path to torch state_dict file.")
    p.add_argument(
        "--weight-bundle-ref",
        default=None,
        help="Optional sealed-bundle note (audit); does not replace --weights when not init-only.",
    )
    args = p.parse_args(argv)

    run_id = args.run_id or f"px2_pf_{Path(args.output_dir).resolve().name}"
    weights_path = None if args.init_only else args.weights
    init_only = bool(args.init_only)

    ok, preflight, report, errors = run_execution_preflight(
        corpus_root=args.corpus_root.resolve(),
        output_dir=args.output_dir.resolve(),
        init_only=init_only,
        weights_path=weights_path,
        weight_bundle_ref=args.weight_bundle_ref,
        torch_seed=args.torch_seed,
        run_id=run_id,
        device_intent=args.device_intent,
        map_location=args.map_location,
    )
    out = args.output_dir.resolve()
    write_json(out / "px2_self_play_execution_preflight.json", preflight)
    write_json(out / "px2_self_play_execution_preflight_report.json", report)
    if not ok:
        print("preflight failed: " + "; ".join(errors), file=sys.stderr)
        return 1
    print(f"preflight ok preflight_sha256={preflight['preflight_sha256']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
