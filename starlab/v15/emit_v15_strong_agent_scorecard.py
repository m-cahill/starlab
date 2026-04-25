"""CLI: emit v15_strong_agent_scorecard.json + report (V15-M05; protocol only)."""

from __future__ import annotations

import argparse
from pathlib import Path

from starlab.v15.strong_agent_scorecard_io import emit_v15_strong_agent_scorecard
from starlab.v15.strong_agent_scorecard_models import (
    PROFILE_FIXTURE_CI,
    PROFILE_OPERATOR_DECLARED,
    SEAL_KEY_STRONG_AGENT,
)

_SEAL = SEAL_KEY_STRONG_AGENT


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Emit governed STARLAB v1.5 strong-agent scorecard + report (V15-M05). "
            "Protocol and scorecard contract only — no benchmark execution, no live SC2, "
            "no GPU. Default profile is fixture_ci (CI-safe, deterministic)."
        ),
    )
    parser.add_argument(
        "--output-dir",
        required=True,
        type=Path,
        help="Directory for v15_strong_agent_scorecard.json and report",
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
        help=(
            "Operator protocol declaration JSON (metadata only). "
            "Required for --profile operator_declared."
        ),
    )
    parser.add_argument(
        "--checkpoint-lineage-json",
        type=Path,
        default=None,
        help="Optional M03 v15_checkpoint_lineage_manifest.json; canonical JSON SHA-256 only.",
    )
    parser.add_argument(
        "--xai-evidence-json",
        type=Path,
        default=None,
        help="Optional M04 v15_xai_evidence_pack.json; canonical JSON SHA-256 only.",
    )
    parser.add_argument(
        "--environment-lock-json",
        type=Path,
        default=None,
        help="Optional M02 v15_long_gpu_environment_lock.json; canonical JSON SHA-256 only.",
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
        if args.checkpoint_lineage_json is not None:
            print(
                "warning: --checkpoint-lineage-json is ignored for fixture_ci profile",
                flush=True,
            )
        if args.xai_evidence_json is not None:
            print("warning: --xai-evidence-json is ignored for fixture_ci profile", flush=True)
        if args.environment_lock_json is not None:
            print(
                "warning: --environment-lock-json is ignored for fixture_ci profile",
                flush=True,
            )

    lock = args.environment_lock_json
    lineage = args.checkpoint_lineage_json
    xai = args.xai_evidence_json
    if args.profile == PROFILE_FIXTURE_CI:
        lock = None
        lineage = None
        xai = None

    sealed, _rep, c_path, r_path = emit_v15_strong_agent_scorecard(
        args.output_dir,
        profile=args.profile,
        protocol_path=proto,
        checkpoint_lineage_path=lineage,
        xai_evidence_path=xai,
        environment_lock_path=lock,
    )
    print(f"wrote {c_path}")
    print(f"wrote {r_path}")
    print(f"{_SEAL}={sealed.get(_SEAL, '')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
