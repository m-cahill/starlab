"""CLI: emit replay explorer surface + report (M31)."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from starlab.explorer.replay_explorer_builder import build_replay_explorer_artifacts
from starlab.explorer.replay_explorer_io import (
    write_replay_explorer_report,
    write_replay_explorer_surface,
)
from starlab.explorer.replay_explorer_models import DEFAULT_MAX_PANELS


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Emit replay_explorer_surface.json + report (M31).")
    p.add_argument("--bundle-dir", type=Path, required=True, help="M14 replay bundle directory")
    p.add_argument(
        "--agent-path", type=Path, required=True, help="replay_hierarchical_imitation_agent.json"
    )
    p.add_argument(
        "--output-dir", type=Path, required=True, help="Output directory for JSON artifacts"
    )
    p.add_argument(
        "--max-panels",
        type=int,
        default=DEFAULT_MAX_PANELS,
        help=f"Maximum panels (default {DEFAULT_MAX_PANELS})",
    )
    p.add_argument("--slice-id", type=str, default=None, help="Optional single slice_id filter")
    args = p.parse_args(argv)

    out = args.output_dir
    out.mkdir(parents=True, exist_ok=True)

    try:
        surface, report = build_replay_explorer_artifacts(
            bundle_dir=args.bundle_dir.resolve(),
            agent_path=args.agent_path.resolve(),
            max_panels=max(1, int(args.max_panels)),
            slice_id_filter=args.slice_id,
        )
    except (OSError, ValueError, KeyError) as exc:
        print(f"emit_replay_explorer_surface: {exc}", file=sys.stderr)
        return 1

    write_replay_explorer_surface(out, surface)
    write_replay_explorer_report(out, report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
