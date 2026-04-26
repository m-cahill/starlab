"""CLI: emit v15_human_benchmark_claim_decision.json + report (V15-M11)."""

from __future__ import annotations

import argparse
from pathlib import Path

from starlab.v15.human_panel_execution_io import emit_v15_human_benchmark_claim_decision
from starlab.v15.human_panel_execution_models import SEAL_KEY_HUMAN_BENCHMARK_CLAIM_DECISION

_SEAL = SEAL_KEY_HUMAN_BENCHMARK_CLAIM_DECISION


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Emit STARLAB v1.5 human-benchmark claim decision from a sealed "
            "v15_human_panel_execution.json (V15-M11). Deterministic, read-only over the execution "
            "artifact; does not re-bind upstream M06/M09/M10 JSON. Optional --strict requires "
            "non-placeholder SHA bindings."
        ),
    )
    parser.add_argument(
        "--human-panel-execution-json",
        required=True,
        type=Path,
        help="Sealed v15_human_panel_execution.json from emit_v15_human_panel_execution",
    )
    parser.add_argument(
        "--output-dir",
        required=True,
        type=Path,
        help="Directory for claim decision JSON + report",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Require non-placeholder M06/M09/M10 SHA bindings in the execution JSON",
    )
    args = parser.parse_args(argv)
    pex = args.human_panel_execution_json
    if not pex.is_file():
        print("error: --human-panel-execution-json must be an existing file", flush=True)
        return 2
    sealed, _r, p1, p2 = emit_v15_human_benchmark_claim_decision(
        args.output_dir, pex, strict=args.strict
    )
    print(f"wrote {p1}", flush=True)
    print(f"wrote {p2}", flush=True)
    print(f"{_SEAL}={sealed.get(_SEAL, '')}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
