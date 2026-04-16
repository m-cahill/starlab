"""CLI: emit `live_sc2_in_ci_hardening_guardrails.json` + report (M58)."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from starlab.runs.json_util import canonical_json_dumps
from starlab.sc2.live_sc2_ci_guardrails import live_sc2_in_ci_hardening_guardrails_bundle
from starlab.sc2.live_sc2_ci_models import (
    LIVE_SC2_IN_CI_HARDENING_GUARDRAILS_FILENAME,
    LIVE_SC2_IN_CI_HARDENING_GUARDRAILS_REPORT_FILENAME,
)


def write_live_sc2_in_ci_hardening_guardrails_artifacts(output_dir: Path) -> tuple[Path, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    guardrails, report = live_sc2_in_ci_hardening_guardrails_bundle()
    gp = output_dir / LIVE_SC2_IN_CI_HARDENING_GUARDRAILS_FILENAME
    rp = output_dir / LIVE_SC2_IN_CI_HARDENING_GUARDRAILS_REPORT_FILENAME
    gp.write_text(canonical_json_dumps(guardrails), encoding="utf-8")
    rp.write_text(canonical_json_dumps(report), encoding="utf-8")
    return gp, rp


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(
        description="Emit deterministic M58 live SC2-in-CI hardening guardrails JSON."
    )
    p.add_argument(
        "--output-dir",
        type=Path,
        default=Path("."),
        help="Directory for guardrails + report JSON (default: cwd).",
    )
    args = p.parse_args(argv)
    g, r = write_live_sc2_in_ci_hardening_guardrails_artifacts(args.output_dir)
    print(f"Wrote {g}")
    print(f"Wrote {r}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
