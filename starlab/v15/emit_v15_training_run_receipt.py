"""CLI: emit v15_training_run_receipt + report (V15-M07; not long GPU campaign)."""

from __future__ import annotations

import argparse
from pathlib import Path

from starlab.v15.training_run_receipt_io import emit_v15_training_run_receipt
from starlab.v15.training_run_receipt_models import (
    PROFILE_FIXTURE_CI,
    PROFILE_OPERATOR_DECLARED,
    PROFILE_OPERATOR_LOCAL_SHORT_GPU,
    SEAL_KEY_TRAINING_RUN_RECEIPT,
)

_SEAL = SEAL_KEY_TRAINING_RUN_RECEIPT


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Emit governed STARLAB v1.5 M07 training run receipt (fixture / declared / short GPU). "
            "Default: fixture_ci (no PyTorch, no SC2, no checkpoint blob read). "
            "Does not run the V15-M08 long GPU campaign."
        ),
    )
    parser.add_argument(
        "--output-dir",
        required=True,
        type=Path,
        help=("Run directory: v15_training_run_receipt.json, report, and (operator_local) .pt"),
    )
    parser.add_argument(
        "--profile",
        choices=(PROFILE_FIXTURE_CI, PROFILE_OPERATOR_DECLARED, PROFILE_OPERATOR_LOCAL_SHORT_GPU),
        default=PROFILE_FIXTURE_CI,
        help="fixture_ci (default) | operator_declared | operator_local_short_gpu",
    )
    parser.add_argument(
        "--receipt-json",
        type=Path,
        default=None,
        help="Declared receipt (metadata). Required for operator_declared.",
    )
    parser.add_argument(
        "--allow-operator-local-execution",
        action="store_true",
        help="Required for operator_local_short_gpu; guard against accidental shakedown runs.",
    )
    parser.add_argument(
        "--run-id",
        type=str,
        default=None,
        help="Run id (operator_local_short_gpu; default: time-based).",
    )
    parser.add_argument(
        "--max-steps",
        type=int,
        default=10,
        help="Synthetic training steps cap (operator_local_short_gpu; default 10).",
    )
    parser.add_argument(
        "--device",
        choices=("cuda", "cpu"),
        default="cuda",
        help=("operator_local_short_gpu: cuda=GPU shakedown, cpu=smoke (not GPU shakedown)."),
    )
    # Optional canonical JSON SHA-256 binding files (M02, M03, M04, M05, M06, configs)
    for arg, h in (
        (
            "--environment-lock-json",
            "Optional v15_long_gpu_environment_lock.json (M02); canonical JSON SHA-256 only.",
        ),
        (
            "--checkpoint-lineage-json",
            "Optional v15_checkpoint_lineage_manifest.json (M03).",
        ),
        (
            "--xai-evidence-json",
            "Optional v15_xai_evidence_pack.json (M04).",
        ),
        (
            "--strong-agent-scorecard-json",
            "Optional v15_strong_agent_scorecard.json (M05).",
        ),
        (
            "--human-panel-benchmark-json",
            "Optional v15_human_panel_benchmark.json (M06).",
        ),
        (
            "--training-config-json",
            "Optional training config JSON; hashed canonically.",
        ),
        (
            "--dataset-manifest-json",
            "Optional dataset manifest JSON.",
        ),
        (
            "--rights-provenance-json",
            "Optional rights / provenance note JSON.",
        ),
    ):
        parser.add_argument(arg, type=Path, default=None, help=h)
    args = parser.parse_args(argv)

    if args.profile == PROFILE_OPERATOR_DECLARED and args.receipt_json is None:
        print("error: --receipt-json is required for operator_declared", flush=True)
        return 2
    if (
        args.profile == PROFILE_OPERATOR_DECLARED
        and args.receipt_json is not None
        and not args.receipt_json.is_file()
    ):
        print(f"error: --receipt-json not found: {args.receipt_json}", flush=True)
        return 2
    if args.profile == PROFILE_FIXTURE_CI:
        for label, p in (
            ("--receipt-json", args.receipt_json),
            ("--allow-operator-local-execution", None),
            ("--run-id", args.run_id),
        ):
            if p is not None and label == "--receipt-json":
                print(f"warning: {label} is ignored for fixture_ci profile", flush=True)
        for label, p in (
            ("--environment-lock-json", args.environment_lock_json),
            ("--checkpoint-lineage-json", args.checkpoint_lineage_json),
            ("--xai-evidence-json", args.xai_evidence_json),
            ("--strong-agent-scorecard-json", args.strong_agent_scorecard_json),
            ("--human-panel-benchmark-json", args.human_panel_benchmark_json),
            ("--training-config-json", args.training_config_json),
            ("--dataset-manifest-json", args.dataset_manifest_json),
            ("--rights-provenance-json", args.rights_provenance_json),
        ):
            if p is not None:
                print(f"warning: {label} is ignored for fixture_ci profile", flush=True)
        el = cl = xai = sasc = hpb = tc = dm = rt = None
    else:
        el, cl, xai, sasc, hpb, tc, dm, rt = (
            args.environment_lock_json,
            args.checkpoint_lineage_json,
            args.xai_evidence_json,
            args.strong_agent_scorecard_json,
            args.human_panel_benchmark_json,
            args.training_config_json,
            args.dataset_manifest_json,
            args.rights_provenance_json,
        )

    if args.profile == PROFILE_FIXTURE_CI:
        sealed, _rep, _rc, c_path, r_path = emit_v15_training_run_receipt(
            args.output_dir,
            profile=PROFILE_FIXTURE_CI,
        )
    elif args.profile == PROFILE_OPERATOR_DECLARED:
        sealed, _rep, _rc, c_path, r_path = emit_v15_training_run_receipt(
            args.output_dir,
            profile=PROFILE_OPERATOR_DECLARED,
            declared_receipt_path=args.receipt_json,
            environment_lock_path=el,
            checkpoint_lineage_path=cl,
            xai_evidence_path=xai,
            strong_agent_scorecard_path=sasc,
            human_panel_benchmark_path=hpb,
            training_config_path=tc,
            dataset_manifest_path=dm,
            rights_provenance_path=rt,
        )
    else:
        sealed, _rep, _rc, c_path, r_path = emit_v15_training_run_receipt(
            args.output_dir,
            profile=PROFILE_OPERATOR_LOCAL_SHORT_GPU,
            allow_operator_local=args.allow_operator_local_execution,
            declared_receipt_path=None,
            run_id=args.run_id,
            max_steps=args.max_steps,
            device=args.device,
            environment_lock_path=el,
            checkpoint_lineage_path=cl,
            xai_evidence_path=xai,
            strong_agent_scorecard_path=sasc,
            human_panel_benchmark_path=hpb,
            training_config_path=tc,
            dataset_manifest_path=dm,
            rights_provenance_path=rt,
        )

    print(f"wrote {c_path}", flush=True)
    print(f"wrote {r_path}", flush=True)
    print(f"redaction_count={_rc}", flush=True)
    print(f"{_SEAL}={sealed.get(_SEAL, '')}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
