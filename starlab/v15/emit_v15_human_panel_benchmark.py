"""CLI: emit v15_human_panel_benchmark + report (V15-M06; protocol only; no human execution)."""

from __future__ import annotations

import argparse
from pathlib import Path

from starlab.v15.human_panel_benchmark_io import emit_v15_human_panel_benchmark
from starlab.v15.human_panel_benchmark_models import (
    PROFILE_FIXTURE_CI,
    PROFILE_OPERATOR_DECLARED,
    SEAL_KEY_HUMAN_PANEL,
)

_SEAL = SEAL_KEY_HUMAN_PANEL


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Emit governed STARLAB v1.5 human panel benchmark protocol + report (V15-M06). "
            "Protocol and governance metadata only — no human panel execution, no real identities, "
            "no live SC2, no GPU. Default profile is fixture_ci (CI-safe, deterministic)."
        ),
    )
    parser.add_argument(
        "--output-dir",
        required=True,
        type=Path,
        help="Directory for v15_human_panel_benchmark.json and report",
    )
    parser.add_argument(
        "--profile",
        choices=(PROFILE_FIXTURE_CI, PROFILE_OPERATOR_DECLARED),
        default=PROFILE_FIXTURE_CI,
        help="fixture_ci (default) or operator_declared (requires --protocol-json)",
    )
    parser.add_argument(
        "--protocol-json",
        type=Path,
        default=None,
        help="Operator human-panel protocol JSON (metadata only). Required for operator_declared.",
    )
    parser.add_argument(
        "--environment-lock-json",
        type=Path,
        default=None,
        help="Optional M02 v15_long_gpu_environment_lock.json; canonical JSON SHA-256 only.",
    )
    parser.add_argument(
        "--checkpoint-lineage-json",
        type=Path,
        default=None,
        help="Optional M03 v15_checkpoint_lineage_manifest.json; canonical JSON SHA-256 only.",
    )
    parser.add_argument(
        "--strong-agent-scorecard-json",
        type=Path,
        default=None,
        help="Optional M05 v15_strong_agent_scorecard.json; canonical JSON SHA-256 only.",
    )
    parser.add_argument(
        "--xai-evidence-json",
        type=Path,
        default=None,
        help="Optional M04 v15_xai_evidence_pack.json; canonical JSON SHA-256 only.",
    )
    args = parser.parse_args(argv)

    if args.profile == PROFILE_OPERATOR_DECLARED and args.protocol_json is None:
        print("error: --protocol-json is required for operator_declared", flush=True)
        return 2

    if args.profile == PROFILE_FIXTURE_CI and args.protocol_json is not None:
        print("warning: --protocol-json is ignored for fixture_ci profile", flush=True)

    proto = args.protocol_json
    if args.profile == PROFILE_FIXTURE_CI:
        proto = None
        for label, p in (
            ("--environment-lock-json", args.environment_lock_json),
            ("--checkpoint-lineage-json", args.checkpoint_lineage_json),
            ("--strong-agent-scorecard-json", args.strong_agent_scorecard_json),
            ("--xai-evidence-json", args.xai_evidence_json),
        ):
            if p is not None:
                print(f"warning: {label} is ignored for fixture_ci profile", flush=True)

    lock = args.environment_lock_json
    lineage = args.checkpoint_lineage_json
    score = args.strong_agent_scorecard_json
    xai = args.xai_evidence_json
    if args.profile == PROFILE_FIXTURE_CI:
        lock = None
        lineage = None
        score = None
        xai = None

    sealed, _rep, _rc, c_path, r_path = emit_v15_human_panel_benchmark(
        args.output_dir,
        profile=args.profile,
        protocol_path=proto,
        environment_lock_path=lock,
        checkpoint_lineage_path=lineage,
        strong_agent_scorecard_path=score,
        xai_evidence_path=xai,
    )
    print(f"wrote {c_path}")
    print(f"wrote {r_path}")
    print(f"redaction_count={_rc}")
    print(f"{_SEAL}={sealed.get(_SEAL, '')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
