"""CLI: emit replay_execution_equivalence_evidence.json + report (M53)."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from starlab.equivalence.equivalence_evidence import (
    replay_execution_equivalence_evidence_bundle_for_profile,
)
from starlab.equivalence.equivalence_models import EVIDENCE_FILENAME, EVIDENCE_REPORT_FILENAME
from starlab.runs.json_util import canonical_json_dumps


def write_replay_execution_equivalence_evidence_artifacts(
    *,
    profile_id: str,
    output_dir: Path,
    run_identity: Path | None,
    lineage_seed: Path | None,
    replay_binding: Path | None,
) -> tuple[Path, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    evidence, report = replay_execution_equivalence_evidence_bundle_for_profile(
        profile_id=profile_id,
        lineage_seed_path=lineage_seed,
        replay_binding_path=replay_binding,
        run_identity_path=run_identity,
    )
    ev_path = output_dir / EVIDENCE_FILENAME
    rep_path = output_dir / EVIDENCE_REPORT_FILENAME
    ev_path.write_text(canonical_json_dumps(evidence), encoding="utf-8")
    rep_path.write_text(canonical_json_dumps(report), encoding="utf-8")
    return ev_path, rep_path


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(
        description=(
            "Emit deterministic replay-vs-execution equivalence evidence JSON "
            "(M53 bounded profile)."
        )
    )
    p.add_argument(
        "--profile",
        required=True,
        help="Comparison profile id (e.g. starlab.m53.profile.identity_binding_v1).",
    )
    p.add_argument(
        "--output-dir", type=Path, default=Path("."), help="Directory for evidence + report JSON."
    )
    p.add_argument("--run-identity", type=Path, help="Path to run_identity.json (M03).")
    p.add_argument("--lineage-seed", type=Path, help="Path to lineage_seed.json (M03).")
    p.add_argument("--replay-binding", type=Path, help="Path to replay_binding.json (M04).")
    args = p.parse_args(argv)
    ev, rep = write_replay_execution_equivalence_evidence_artifacts(
        lineage_seed=args.lineage_seed,
        output_dir=args.output_dir,
        profile_id=args.profile,
        replay_binding=args.replay_binding,
        run_identity=args.run_identity,
    )
    print(f"Wrote {ev}")
    print(f"Wrote {rep}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
