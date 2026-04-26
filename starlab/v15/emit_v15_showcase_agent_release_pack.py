"""CLI: emit v15_showcase_agent_release_pack.json + report + Markdown brief (V15-M12)."""

from __future__ import annotations

import argparse
from pathlib import Path

from starlab.v15.showcase_release_io import (
    emit_v15_showcase_agent_release_pack_fixture,
    emit_v15_showcase_agent_release_pack_operator_declared,
    emit_v15_showcase_agent_release_pack_operator_preflight,
)
from starlab.v15.showcase_release_models import (
    PROFILE_FIXTURE_CI,
    PROFILE_OPERATOR_DECLARED,
    PROFILE_OPERATOR_PREFLIGHT,
    SEAL_KEY_SHOWCASE_RELEASE_PACK,
)

_SEAL = SEAL_KEY_SHOWCASE_RELEASE_PACK
_PROFILES = (PROFILE_FIXTURE_CI, PROFILE_OPERATOR_PREFLIGHT, PROFILE_OPERATOR_DECLARED)


def _must_file(p: Path | None, label: str) -> Path:
    if p is None:
        raise SystemExit(f"error: {label} is required for this profile")
    if not p.is_file():
        raise SystemExit(f"error: {label} must be an existing file ({p})")
    return p


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Emit STARLAB v1.5 showcase agent release-pack JSON + report + Markdown brief "
            "(V15-M12). "
            "Binds upstream milestone JSON by canonical SHA-256 only. Does not read checkpoint "
            "blobs, weights, or replay binaries; does not run SC2, GPU training, XAI inference, "
            "or human-panel matches. Default: fixture_ci."
        ),
    )
    parser.add_argument(
        "--output-dir",
        required=True,
        type=Path,
        help="Directory for pack JSON, report JSON, and Markdown brief",
    )
    parser.add_argument(
        "--profile",
        choices=_PROFILES,
        default=PROFILE_FIXTURE_CI,
        help="fixture_ci (default), operator_preflight, or operator_declared",
    )
    parser.add_argument(
        "--m08-campaign-receipt-json",
        type=Path,
        default=None,
        help="M08 v15_long_gpu_campaign_receipt.json (operator_preflight / operator_declared)",
    )
    parser.add_argument(
        "--m09-promotion-decision-json",
        type=Path,
        default=None,
        help="M09 v15_checkpoint_promotion_decision.json (operator_preflight / operator_declared)",
    )
    parser.add_argument(
        "--m10-xai-demonstration-json",
        type=Path,
        default=None,
        help=(
            "M10 v15_replay_native_xai_demonstration.json (operator_preflight / operator_declared)"
        ),
    )
    parser.add_argument(
        "--m11-human-benchmark-claim-decision-json",
        type=Path,
        default=None,
        help="M11 v15_human_benchmark_claim_decision.json (operator_preflight / operator_declared)",
    )
    parser.add_argument(
        "--m05-scorecard-json",
        type=Path,
        default=None,
        help="M05 v15_strong_agent_scorecard.json (operator_preflight / operator_declared)",
    )
    parser.add_argument(
        "--m03-checkpoint-lineage-json",
        type=Path,
        default=None,
        help="M03 v15_checkpoint_lineage_manifest.json (operator_preflight / operator_declared)",
    )
    parser.add_argument(
        "--release-evidence-json",
        type=Path,
        default=None,
        help=(
            "Operator release-evidence bundle "
            "(starlab.v15.showcase_operator_release_evidence_declared.v1; "
            "required for operator_declared)"
        ),
    )
    args = parser.parse_args(argv)

    if args.profile == PROFILE_FIXTURE_CI:
        for label, p in [
            ("--m08-campaign-receipt-json", args.m08_campaign_receipt_json),
            ("--m09-promotion-decision-json", args.m09_promotion_decision_json),
            ("--m10-xai-demonstration-json", args.m10_xai_demonstration_json),
            (
                "--m11-human-benchmark-claim-decision-json",
                args.m11_human_benchmark_claim_decision_json,
            ),
            ("--m05-scorecard-json", args.m05_scorecard_json),
            ("--m03-checkpoint-lineage-json", args.m03_checkpoint_lineage_json),
            ("--release-evidence-json", args.release_evidence_json),
        ]:
            if p is not None:
                print(f"warning: {label} is ignored for fixture_ci profile", flush=True)
        sealed, _rep, p_j, p_r, p_m = emit_v15_showcase_agent_release_pack_fixture(args.output_dir)
        print(f"wrote {p_j}", flush=True)
        print(f"wrote {p_r}", flush=True)
        print(f"wrote {p_m}", flush=True)
        print(f"{_SEAL}={sealed.get(_SEAL, '')}", flush=True)
        return 0

    m08 = _must_file(args.m08_campaign_receipt_json, "--m08-campaign-receipt-json")
    m09 = _must_file(args.m09_promotion_decision_json, "--m09-promotion-decision-json")
    m10 = _must_file(args.m10_xai_demonstration_json, "--m10-xai-demonstration-json")
    m11 = _must_file(
        args.m11_human_benchmark_claim_decision_json, "--m11-human-benchmark-claim-decision-json"
    )
    m05 = _must_file(args.m05_scorecard_json, "--m05-scorecard-json")
    m03 = _must_file(args.m03_checkpoint_lineage_json, "--m03-checkpoint-lineage-json")

    if args.profile == PROFILE_OPERATOR_PREFLIGHT:
        if args.release_evidence_json is not None:
            print("warning: --release-evidence-json is ignored for operator_preflight", flush=True)
        sealed, _rep, p_j, p_r, p_m = emit_v15_showcase_agent_release_pack_operator_preflight(
            args.output_dir, m08, m09, m10, m11, m05, m03
        )
        print(f"wrote {p_j}", flush=True)
        print(f"wrote {p_r}", flush=True)
        print(f"wrote {p_m}", flush=True)
        print(f"{_SEAL}={sealed.get(_SEAL, '')}", flush=True)
        return 0

    rev = _must_file(args.release_evidence_json, "--release-evidence-json")
    sealed, _rep, rc, p_j, p_r, p_m = emit_v15_showcase_agent_release_pack_operator_declared(
        args.output_dir, rev, m08, m09, m10, m11, m05, m03
    )
    print(f"wrote {p_j}", flush=True)
    print(f"wrote {p_r}", flush=True)
    print(f"wrote {p_m}", flush=True)
    print(f"{_SEAL}={sealed.get(_SEAL, '')}", flush=True)
    print(f"redaction_count={rc}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
