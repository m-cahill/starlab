"""CLI: emit v15_replay_native_xai_demonstration.json + report + Markdown (V15-M10)."""

from __future__ import annotations

import argparse
from pathlib import Path

from starlab.v15.xai_demonstration_io import (
    emit_v15_replay_native_xai_demonstration_fixture,
    emit_v15_replay_native_xai_demonstration_operator_declared,
    emit_v15_replay_native_xai_demonstration_operator_preflight,
)
from starlab.v15.xai_demonstration_models import (
    PROFILE_FIXTURE_CI,
    PROFILE_OPERATOR_DECLARED,
    PROFILE_OPERATOR_PREFLIGHT,
    SEAL_KEY_REPLAY_NATIVE_XAI_DEMONSTRATION,
)

_SEAL = SEAL_KEY_REPLAY_NATIVE_XAI_DEMONSTRATION

_PROFILES = (PROFILE_FIXTURE_CI, PROFILE_OPERATOR_DECLARED, PROFILE_OPERATOR_PREFLIGHT)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Emit governed STARLAB v1.5 replay-native XAI demonstration pack + reports (V15-M10). "
            "Binds M04 xai_evidence_pack and M09 promotion decision by canonical JSON SHA-256 when "
            "supplied. Does not run model inference, live SC2, or GPU work. Default: fixture_ci."
        ),
    )
    parser.add_argument(
        "--output-dir",
        required=True,
        type=Path,
        help="Directory for v15_replay_native_xai_demonstration.json, report JSON, and Markdown",
    )
    parser.add_argument(
        "--profile",
        choices=_PROFILES,
        default=PROFILE_FIXTURE_CI,
        help="fixture_ci (default), operator_declared, or operator_preflight",
    )
    parser.add_argument(
        "--m09-promotion-decision-json",
        type=Path,
        default=None,
        help=(
            "M09 v15_checkpoint_promotion_decision.json "
            "(required for operator_declared and preflight)"
        ),
    )
    parser.add_argument(
        "--m04-xai-evidence-pack-json",
        type=Path,
        default=None,
        help="M04 v15_xai_evidence_pack.json (required for operator_declared and preflight)",
    )
    parser.add_argument(
        "--m08-campaign-receipt-json",
        type=Path,
        default=None,
        help="M08 v15_long_gpu_campaign_receipt.json (required for operator_preflight only)",
    )
    parser.add_argument(
        "--m03-checkpoint-lineage-json",
        type=Path,
        default=None,
        help="M03 v15_checkpoint_lineage_manifest.json (required for operator_preflight only)",
    )
    parser.add_argument(
        "--m05-scorecard-json",
        type=Path,
        default=None,
        help="M05 v15_strong_agent_scorecard.json (required for operator_preflight only)",
    )
    args = parser.parse_args(argv)

    if args.profile == PROFILE_FIXTURE_CI:
        for label, p in [
            ("--m09-promotion-decision-json", args.m09_promotion_decision_json),
            ("--m04-xai-evidence-pack-json", args.m04_xai_evidence_pack_json),
            ("--m08-campaign-receipt-json", args.m08_campaign_receipt_json),
            ("--m03-checkpoint-lineage-json", args.m03_checkpoint_lineage_json),
            ("--m05-scorecard-json", args.m05_scorecard_json),
        ]:
            if p is not None:
                print(f"warning: {label} is ignored for fixture_ci profile", flush=True)
        sealed, _rep, p_j, p_r, p_m = emit_v15_replay_native_xai_demonstration_fixture(
            args.output_dir
        )
        print(f"wrote {p_j}")
        print(f"wrote {p_r}")
        print(f"wrote {p_m}")
        print(f"{_SEAL}={sealed.get(_SEAL, '')}")
        return 0

    if args.profile == PROFILE_OPERATOR_DECLARED:
        m09 = args.m09_promotion_decision_json
        m04 = args.m04_xai_evidence_pack_json
        if m09 is None or m04 is None:
            print(
                "error: --m09-promotion-decision-json and --m04-xai-evidence-pack-json "
                "are required for operator_declared",
                flush=True,
            )
            return 2
        if not m09.is_file() or not m04.is_file():
            print("error: M09/M04 JSON paths must be existing files", flush=True)
            return 2
        for label, p in [
            ("--m08-campaign-receipt-json", args.m08_campaign_receipt_json),
            ("--m03-checkpoint-lineage-json", args.m03_checkpoint_lineage_json),
            ("--m05-scorecard-json", args.m05_scorecard_json),
        ]:
            if p is not None:
                print(
                    f"warning: {label} is ignored for operator_declared (use operator_preflight)",
                    flush=True,
                )
        sealed, _rep, rc, p_j, p_r, p_m = (
            emit_v15_replay_native_xai_demonstration_operator_declared(args.output_dir, m09, m04)
        )
        print(f"wrote {p_j}")
        print(f"wrote {p_r}")
        print(f"wrote {p_m}")
        print(f"redaction_count={rc}")
        print(f"{_SEAL}={sealed.get(_SEAL, '')}")
        return 0

    # operator_preflight
    req = [
        ("--m09-promotion-decision-json", args.m09_promotion_decision_json),
        ("--m04-xai-evidence-pack-json", args.m04_xai_evidence_pack_json),
        ("--m08-campaign-receipt-json", args.m08_campaign_receipt_json),
        ("--m03-checkpoint-lineage-json", args.m03_checkpoint_lineage_json),
        ("--m05-scorecard-json", args.m05_scorecard_json),
    ]
    for label, p in req:
        if p is None or not p.is_file():
            print(f"error: {label} must be an existing file for operator_preflight", flush=True)
            return 2
    m09 = args.m09_promotion_decision_json
    m04 = args.m04_xai_evidence_pack_json
    m08 = args.m08_campaign_receipt_json
    m03 = args.m03_checkpoint_lineage_json
    m05 = args.m05_scorecard_json
    assert (
        m09 is not None
        and m04 is not None
        and m08 is not None
        and m03 is not None
        and m05 is not None
    )
    sealed, _rep, p_j, p_r, p_m = emit_v15_replay_native_xai_demonstration_operator_preflight(
        args.output_dir,
        m09,
        m04,
        m08,
        m03,
        m05,
    )
    print(f"wrote {p_j}")
    print(f"wrote {p_r}")
    print(f"wrote {p_m}")
    print(f"{_SEAL}={sealed.get(_SEAL, '')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
