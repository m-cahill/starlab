"""CLI: emit v15_v2_go_no_go_decision.json + report + Markdown brief (V15-M13)."""

from __future__ import annotations

import argparse
from pathlib import Path

from starlab.v15.v2_decision_io import (
    emit_v15_v2_go_no_go_decision_fixture,
    emit_v15_v2_go_no_go_decision_operator_declared,
    emit_v15_v2_go_no_go_decision_operator_preflight,
)
from starlab.v15.v2_decision_models import (
    PROFILE_FIXTURE_CI,
    PROFILE_OPERATOR_DECLARED,
    PROFILE_OPERATOR_PREFLIGHT,
    SEAL_KEY_V2_GO_NO_GO_DECISION,
)

_SEAL = SEAL_KEY_V2_GO_NO_GO_DECISION
_PROFILES = (PROFILE_FIXTURE_CI, PROFILE_OPERATOR_PREFLIGHT, PROFILE_OPERATOR_DECLARED)


def _must_file(p: Path | None, label: str) -> Path:
    if p is None:
        raise SystemExit(f"error: {label} is required for this profile")
    if not p.is_file():
        raise SystemExit(f"error: {label} must be an existing file ({p})")
    return p


def _optional_paths_from_args(args: argparse.Namespace) -> dict[str, Path | None]:
    return {
        "m08_campaign_receipt": args.m08_campaign_receipt_json,
        "m09_promotion_decision": args.m09_promotion_decision_json,
        "m10_xai_demonstration": args.m10_xai_demonstration_json,
        "m11_human_benchmark_claim": args.m11_human_benchmark_claim_decision_json,
        "m05_strong_agent_scorecard": args.m05_scorecard_json,
        "m03_checkpoint_lineage": args.m03_checkpoint_lineage_json,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Emit STARLAB v1.5 v2 go/no-go decision JSON + report + Markdown brief (V15-M13). "
            "Binds M12 showcase release-pack JSON by canonical SHA-256; optional upstream "
            "JSON files cross-checked against M12 bindings. Does not read checkpoint blobs, "
            "weights, or replay binaries; does not run SC2, GPU training, XAI inference, or "
            "human-panel matches. Default: fixture_ci."
        ),
    )
    parser.add_argument(
        "--output-dir",
        required=True,
        type=Path,
        help="Directory for decision JSON, report JSON, and Markdown brief",
    )
    parser.add_argument(
        "--profile",
        choices=_PROFILES,
        default=PROFILE_FIXTURE_CI,
        help="fixture_ci (default), operator_preflight, or operator_declared",
    )
    parser.add_argument(
        "--m12-showcase-release-pack-json",
        type=Path,
        default=None,
        help="M12 v15_showcase_agent_release_pack.json (operator_preflight / operator_declared)",
    )
    parser.add_argument(
        "--m08-campaign-receipt-json",
        type=Path,
        default=None,
        help="Optional cross-check: M08 campaign receipt JSON (must match M12 binding SHA)",
    )
    parser.add_argument(
        "--m09-promotion-decision-json",
        type=Path,
        default=None,
        help="Optional cross-check: M09 promotion decision JSON",
    )
    parser.add_argument(
        "--m10-xai-demonstration-json",
        type=Path,
        default=None,
        help="Optional cross-check: M10 replay-native XAI demonstration JSON",
    )
    parser.add_argument(
        "--m11-human-benchmark-claim-decision-json",
        type=Path,
        default=None,
        help="Optional cross-check: M11 human-benchmark claim decision JSON",
    )
    parser.add_argument(
        "--m05-scorecard-json",
        type=Path,
        default=None,
        help="Optional cross-check: M05 strong-agent scorecard JSON",
    )
    parser.add_argument(
        "--m03-checkpoint-lineage-json",
        type=Path,
        default=None,
        help="Optional cross-check: M03 checkpoint lineage manifest JSON",
    )
    parser.add_argument(
        "--decision-evidence-json",
        type=Path,
        default=None,
        help=(
            "Operator decision-evidence bundle "
            "(starlab.v15.v2_decision_operator_evidence_declared.v1; "
            "required for operator_declared)"
        ),
    )
    args = parser.parse_args(argv)
    opt = _optional_paths_from_args(args)

    if args.profile == PROFILE_FIXTURE_CI:
        for label, p in [
            ("--m12-showcase-release-pack-json", args.m12_showcase_release_pack_json),
            ("--m08-campaign-receipt-json", args.m08_campaign_receipt_json),
            ("--m09-promotion-decision-json", args.m09_promotion_decision_json),
            ("--m10-xai-demonstration-json", args.m10_xai_demonstration_json),
            (
                "--m11-human-benchmark-claim-decision-json",
                args.m11_human_benchmark_claim_decision_json,
            ),
            ("--m05-scorecard-json", args.m05_scorecard_json),
            ("--m03-checkpoint-lineage-json", args.m03_checkpoint_lineage_json),
            ("--decision-evidence-json", args.decision_evidence_json),
        ]:
            if p is not None:
                print(f"warning: {label} is ignored for fixture_ci profile", flush=True)
        sealed, _rep, p_j, p_r, p_m = emit_v15_v2_go_no_go_decision_fixture(args.output_dir)
        print(f"wrote {p_j}", flush=True)
        print(f"wrote {p_r}", flush=True)
        print(f"wrote {p_m}", flush=True)
        print(f"{_SEAL}={sealed.get(_SEAL, '')}", flush=True)
        return 0

    m12 = _must_file(args.m12_showcase_release_pack_json, "--m12-showcase-release-pack-json")

    if args.profile == PROFILE_OPERATOR_PREFLIGHT:
        if args.decision_evidence_json is not None:
            print(
                "warning: --decision-evidence-json is ignored for operator_preflight",
                flush=True,
            )
        sealed, _rep, p_j, p_r, p_m = emit_v15_v2_go_no_go_decision_operator_preflight(
            args.output_dir, m12, opt
        )
        print(f"wrote {p_j}", flush=True)
        print(f"wrote {p_r}", flush=True)
        print(f"wrote {p_m}", flush=True)
        print(f"{_SEAL}={sealed.get(_SEAL, '')}", flush=True)
        return 0

    dev = _must_file(args.decision_evidence_json, "--decision-evidence-json")
    sealed, _rep, rc, p_j, p_r, p_m = emit_v15_v2_go_no_go_decision_operator_declared(
        args.output_dir, m12, dev, opt
    )
    print(f"wrote {p_j}", flush=True)
    print(f"wrote {p_r}", flush=True)
    print(f"wrote {p_m}", flush=True)
    print(f"{_SEAL}={sealed.get(_SEAL, '')}", flush=True)
    print(f"redaction_count={rc}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
