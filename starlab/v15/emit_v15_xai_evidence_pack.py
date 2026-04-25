"""CLI: emit v15_xai_evidence_pack.json + report (V15-M04)."""

from __future__ import annotations

import argparse
from pathlib import Path

from starlab.v15.xai_evidence_io import emit_v15_xai_evidence_pack
from starlab.v15.xai_evidence_models import PROFILE_FIXTURE_CI, PROFILE_OPERATOR_DECLARED

_SEAL = "xai_evidence_pack_sha256"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Emit governed STARLAB v1.5 XAI evidence pack + report (V15-M04). "
            "Metadata and schema only — no model inference, no replay parsing, no checkpoint I/O. "
            "Default profile is fixture_ci (CI-safe, deterministic)."
        ),
    )
    parser.add_argument(
        "--output-dir",
        required=True,
        type=Path,
        help="Directory for v15_xai_evidence_pack.json and report",
    )
    parser.add_argument(
        "--profile",
        choices=(PROFILE_FIXTURE_CI, PROFILE_OPERATOR_DECLARED),
        default=PROFILE_FIXTURE_CI,
        help="fixture_ci (default) or operator_declared (use with --evidence-json)",
    )
    parser.add_argument(
        "--evidence-json",
        type=Path,
        default=None,
        help=(
            "Operator evidence JSON (metadata-only; see "
            "docs/runtime/v15_xai_evidence_contract_v1.md). "
            "Required for --profile operator_declared."
        ),
    )
    parser.add_argument(
        "--checkpoint-lineage-json",
        type=Path,
        default=None,
        help=(
            "Optional M03 v15_checkpoint_lineage_manifest.json (or compatible object). "
            "Canonical JSON SHA-256 is bound into checkpoint_identity; no blob reads."
        ),
    )
    parser.add_argument(
        "--environment-lock-json",
        type=Path,
        default=None,
        help=(
            "Optional M02 v15_long_gpu_environment_lock.json (or compatible object). "
            "Canonical JSON SHA-256 is bound as a logical reference; path is not stored."
        ),
    )
    args = parser.parse_args(argv)

    if args.profile == PROFILE_OPERATOR_DECLARED and args.evidence_json is None:
        print("error: --evidence-json is required for operator_declared", flush=True)
        return 2

    if args.profile == PROFILE_FIXTURE_CI and args.evidence_json is not None:
        print("warning: --evidence-json is ignored for fixture_ci profile", flush=True)

    ev_path: Path | None = args.evidence_json
    if args.profile == PROFILE_FIXTURE_CI:
        ev_path = None

    lock_path = args.environment_lock_json
    lineage_path = args.checkpoint_lineage_json
    if args.profile == PROFILE_FIXTURE_CI:
        if lock_path is not None:
            print("warning: --environment-lock-json is ignored for fixture_ci profile", flush=True)
        if lineage_path is not None:
            print(
                "warning: --checkpoint-lineage-json is ignored for fixture_ci profile",
                flush=True,
            )
        lock_path = None
        lineage_path = None

    sealed, _rep, c_path, r_path = emit_v15_xai_evidence_pack(
        args.output_dir,
        profile=args.profile,
        evidence_path=ev_path,
        environment_lock_path=lock_path,
        checkpoint_lineage_path=lineage_path,
    )
    print(f"wrote {c_path}")
    print(f"wrote {r_path}")
    print(f"{_SEAL}={sealed.get(_SEAL, '')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
