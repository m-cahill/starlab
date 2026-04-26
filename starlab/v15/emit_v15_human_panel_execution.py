"""CLI: emit v15_human_panel_execution.json + report (V15-M11)."""

from __future__ import annotations

import argparse
from pathlib import Path

from starlab.v15.human_panel_execution_io import (
    emit_v15_human_panel_execution_fixture,
    emit_v15_human_panel_execution_operator_declared,
    emit_v15_human_panel_execution_operator_preflight,
)
from starlab.v15.human_panel_execution_models import (
    PROFILE_FIXTURE_CI,
    PROFILE_OPERATOR_DECLARED,
    PROFILE_OPERATOR_PREFLIGHT,
    SEAL_KEY_HUMAN_PANEL_EXECUTION,
)

_SEAL = SEAL_KEY_HUMAN_PANEL_EXECUTION
_PROFILES = (PROFILE_FIXTURE_CI, PROFILE_OPERATOR_DECLARED, PROFILE_OPERATOR_PREFLIGHT)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Emit governed STARLAB v1.5 human panel execution + report JSON (V15-M11). "
            "Binds M06 / M09 / M10 (and preflight: M08 / M05 / M03) by canonical JSON SHA-256. "
            "Does not run live SC2, human-panel matches, or recruit participants. "
            "Default: fixture_ci."
        ),
    )
    parser.add_argument(
        "--output-dir",
        required=True,
        type=Path,
        help="Output directory for v15_human_panel_execution.json and report",
    )
    parser.add_argument(
        "--profile",
        choices=_PROFILES,
        default=PROFILE_FIXTURE_CI,
        help="fixture_ci (default), operator_declared, or operator_preflight",
    )
    parser.add_argument(
        "--m06-human-panel-protocol-json",
        type=Path,
        default=None,
        help="M06 v15_human_panel_benchmark.json (operator_declared / preflight)",
    )
    parser.add_argument(
        "--m09-promotion-decision-json",
        type=Path,
        default=None,
        help="M09 v15_checkpoint_promotion_decision.json (operator_declared / preflight)",
    )
    parser.add_argument(
        "--m10-xai-demonstration-json",
        type=Path,
        default=None,
        help="M10 v15_replay_native_xai_demonstration.json (operator_declared / preflight)",
    )
    parser.add_argument(
        "--panel-evidence-json",
        type=Path,
        default=None,
        help="Operator panel evidence summary JSON (public-safe keys only; operator paths)",
    )
    parser.add_argument(
        "--m08-campaign-receipt-json",
        type=Path,
        default=None,
        help="M08 v15_long_gpu_campaign_receipt.json (operator_preflight only)",
    )
    parser.add_argument(
        "--m05-scorecard-json",
        type=Path,
        default=None,
        help="M05 v15_strong_agent_scorecard.json (operator_preflight only)",
    )
    parser.add_argument(
        "--m03-checkpoint-lineage-json",
        type=Path,
        default=None,
        help="M03 v15_checkpoint_lineage_manifest.json (operator_preflight only)",
    )
    args = parser.parse_args(argv)

    if args.profile == PROFILE_FIXTURE_CI:
        for label, p in [
            ("--m06-human-panel-protocol-json", args.m06_human_panel_protocol_json),
            ("--m09-promotion-decision-json", args.m09_promotion_decision_json),
            ("--m10-xai-demonstration-json", args.m10_xai_demonstration_json),
            ("--panel-evidence-json", args.panel_evidence_json),
            ("--m08-campaign-receipt-json", args.m08_campaign_receipt_json),
            ("--m05-scorecard-json", args.m05_scorecard_json),
            ("--m03-checkpoint-lineage-json", args.m03_checkpoint_lineage_json),
        ]:
            if p is not None:
                print(f"warning: {label} is ignored for fixture_ci profile", flush=True)
        sealed, _r, _rc, p1, p2 = emit_v15_human_panel_execution_fixture(args.output_dir)
        print(f"wrote {p1}", flush=True)
        print(f"wrote {p2}", flush=True)
        print(f"{_SEAL}={sealed.get(_SEAL, '')}", flush=True)
        return 0

    if args.profile == PROFILE_OPERATOR_DECLARED:
        m06, m09, m10, pan = (
            args.m06_human_panel_protocol_json,
            args.m09_promotion_decision_json,
            args.m10_xai_demonstration_json,
            args.panel_evidence_json,
        )
        if m06 is None or m09 is None or m10 is None or pan is None:
            print(
                "error: --m06-human-panel-protocol-json, --m09-promotion-decision-json, "
                "--m10-xai-demonstration-json, and --panel-evidence-json are required "
                "for operator_declared",
                flush=True,
            )
            return 2
        if not all(p.is_file() for p in (m06, m09, m10, pan)):
            print("error: all input JSON paths must be existing files", flush=True)
            return 2
        for label, p in [
            ("--m08-campaign-receipt-json", args.m08_campaign_receipt_json),
            ("--m05-scorecard-json", args.m05_scorecard_json),
            ("--m03-checkpoint-lineage-json", args.m03_checkpoint_lineage_json),
        ]:
            if p is not None:
                print(
                    f"warning: {label} is ignored for operator_declared (use operator_preflight)",
                    flush=True,
                )
        sealed, _r, rc, p1, p2 = emit_v15_human_panel_execution_operator_declared(
            args.output_dir, m06, m09, m10, pan
        )
        print(f"wrote {p1}", flush=True)
        print(f"wrote {p2}", flush=True)
        print(f"redaction_count={rc}", flush=True)
        print(f"{_SEAL}={sealed.get(_SEAL, '')}", flush=True)
        return 0

    req = [
        ("--m06-human-panel-protocol-json", args.m06_human_panel_protocol_json),
        ("--m09-promotion-decision-json", args.m09_promotion_decision_json),
        ("--m10-xai-demonstration-json", args.m10_xai_demonstration_json),
        ("--m08-campaign-receipt-json", args.m08_campaign_receipt_json),
        ("--m05-scorecard-json", args.m05_scorecard_json),
        ("--m03-checkpoint-lineage-json", args.m03_checkpoint_lineage_json),
        ("--panel-evidence-json", args.panel_evidence_json),
    ]
    for label, p in req:
        if p is None or not p.is_file():
            print(f"error: {label} must be an existing file for operator_preflight", flush=True)
            return 2
    sealed, _r, rc, p1, p2 = emit_v15_human_panel_execution_operator_preflight(
        args.output_dir,
        args.m06_human_panel_protocol_json,
        args.m09_promotion_decision_json,
        args.m10_xai_demonstration_json,
        args.m08_campaign_receipt_json,
        args.m05_scorecard_json,
        args.m03_checkpoint_lineage_json,
        args.panel_evidence_json,
    )
    print(f"wrote {p1}", flush=True)
    print(f"wrote {p2}", flush=True)
    print(f"redaction_count={rc}", flush=True)
    print(f"{_SEAL}={sealed.get(_SEAL, '')}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
