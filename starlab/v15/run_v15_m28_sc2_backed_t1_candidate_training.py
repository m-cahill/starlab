"""V15-M28 — SC2 rollout JSON → feature-conditioned bounded T1 candidate training."""

from __future__ import annotations

import argparse
import sys
import time
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from starlab.v15.sc2_backed_t1_candidate_training_io import (
    build_fixture_m27_like_dict_for_ci,
    sc2_rollout_feature_vector_from_m27_episodes,
    seal_m28_body,
    validate_m27_outcome_strict,
    verify_m27_rollout_json,
    write_m28_artifacts,
)
from starlab.v15.sc2_backed_t1_candidate_training_models import (
    CONTRACT_ID,
    EXPECTED_M27_CONTRACT_ID,
    M20_M21_DEFERRED,
    MILESTONE_LABEL,
    NON_CLAIM_DEFAULTS,
    OUTCOME_BLOCKED_MISSING_M27,
    OUTCOME_BLOCKED_SHA_MISMATCH,
    OUTCOME_BLOCKED_TRAINING_LOOP,
    OUTCOME_FIXTURE_ONLY,
    OUTCOME_STARTED_FAILED,
    OUTCOME_WITH_CHECKPOINT,
    OUTCOME_WITHOUT_CHECKPOINT,
    PROFILE_FIXTURE_CI,
    PROFILE_OPERATOR_LOCAL,
    RUN_TIER_T1_30_MIN,
    TRAINING_CONDITION_LABEL,
)
from starlab.v15.sc2_backed_t1_training_execution import run_bounded_rollout_feature_training


def _stamp_emit_ts(body: dict[str, Any]) -> dict[str, Any]:
    stamped = dict(body)
    stamped["emit_timestamp_utc"] = datetime.now(UTC).isoformat().replace("+00:00", "Z")
    return stamped


def _emit_blocked(
    output_dir: Path,
    *,
    m28_outcome: str,
    detail: dict[str, Any],
) -> int:
    """Write minimal sealed artifact for blocked branches."""

    output_dir.mkdir(parents=True, exist_ok=True)
    body_pre: dict[str, Any] = {
        "contract_id": CONTRACT_ID,
        "milestone": MILESTONE_LABEL,
        "profile": PROFILE_OPERATOR_LOCAL,
        "m28_outcome": m28_outcome,
        "upstream_m27_rollout": detail.get("upstream_m27_rollout", {}),
        "training_attempt": {
            "run_tier": RUN_TIER_T1_30_MIN,
            "max_wall_clock_minutes": detail.get("max_wall_clock_minutes", 0),
            "sc2_backed_features_used": False,
            "training_update_count": 0,
            "wall_clock_seconds": 0.0,
            "checkpoint_count": 0,
            "candidate_checkpoint_sha256": None,
            "training_condition_label": TRAINING_CONDITION_LABEL,
            "blocked_reason": detail.get("blocked_reason"),
        },
        "candidate_checkpoint": {
            "produced": False,
            "sha256": None,
            "promotion_status": "not_promoted_candidate_only",
        },
        "m20_m21_gate_integration": M20_M21_DEFERRED,
        "non_claims": list(NON_CLAIM_DEFAULTS),
    }
    sealed = seal_m28_body(_stamp_emit_ts(body_pre))
    write_m28_artifacts(output_dir, sealed)
    return 3 if "blocked" in m28_outcome else 1


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="python -m starlab.v15.run_v15_m28_sc2_backed_t1_candidate_training",
        description=(
            "V15-M28 — consume governed M27 SC2 rollout JSON, derive rollout features, "
            "run bounded PyTorch training updates (candidate checkpoint optional)."
        ),
    )
    parser.add_argument(
        "--fixture-only",
        action="store_true",
        help="CI-safe: synthetic M27-shaped inputs + tiny training budget (no upstream path).",
    )
    parser.add_argument(
        "--allow-operator-local-execution",
        action="store_true",
        help="Guard: required with --authorize-* for operator-local GPU training path.",
    )
    parser.add_argument(
        "--authorize-sc2-backed-t1-candidate-training",
        action="store_true",
        help="Guard: authorizes bounded SC2-backed candidate training attempt.",
    )
    parser.add_argument(
        "--m27-sc2-rollout-json",
        type=Path,
        default=None,
        help=(
            "Path to v15_sc2_rollout_training_loop_integration.json "
            "(required unless --fixture-only)."
        ),
    )
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--max-wall-clock-minutes", type=float, default=30.0)
    parser.add_argument("--min-training-updates", type=int, default=10)
    parser.add_argument("--max-training-updates", type=int, default=200)
    parser.add_argument("--checkpoint-cadence-updates", type=int, default=50)
    parser.add_argument(
        "--device",
        choices=("auto", "cuda", "cpu"),
        default="auto",
        help="Training device preference (default: auto).",
    )
    parser.add_argument("--seed", type=int, default=20260428)
    parser.add_argument(
        "--allow-partial-m27-outcome",
        action="store_true",
        help="Allow non-completed m27_outcome when governance explicitly permits.",
    )
    args = parser.parse_args(argv)

    out_dir = args.output_dir.resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    wall_secs = float(args.max_wall_clock_minutes) * 60.0

    if args.fixture_only:
        m27 = build_fixture_m27_like_dict_for_ci()
        profile = PROFILE_FIXTURE_CI
        m27_path_note = "fixture_inline_m27_shape"
    else:
        if (
            not args.allow_operator_local_execution
            or not args.authorize_sc2_backed_t1_candidate_training
        ):
            sys.stderr.write(
                "error: operator-local path requires "
                "--allow-operator-local-execution and "
                "--authorize-sc2-backed-t1-candidate-training\n",
            )
            return 2
        if args.m27_sc2_rollout_json is None:
            sys.stderr.write("error: --m27-sc2-rollout-json is required\n")
            return 2
        m27_path = args.m27_sc2_rollout_json.resolve()
        m27_raw, err = verify_m27_rollout_json(m27_path)
        if err == "missing_file":
            return _emit_blocked(
                out_dir,
                m28_outcome=OUTCOME_BLOCKED_MISSING_M27,
                detail={
                    "upstream_m27_rollout": {
                        "path_role": "missing",
                        "expected_contract": EXPECTED_M27_CONTRACT_ID,
                    },
                    "blocked_reason": "missing_m27_json",
                    "max_wall_clock_minutes": args.max_wall_clock_minutes,
                },
            )
        if err == "sha_mismatch":
            return _emit_blocked(
                out_dir,
                m28_outcome=OUTCOME_BLOCKED_SHA_MISMATCH,
                detail={
                    "upstream_m27_rollout": {
                        "path_role": "operator_local_input",
                        "resolved_path": str(m27_path),
                    },
                    "blocked_reason": "m27_canonical_seal_mismatch",
                    "max_wall_clock_minutes": args.max_wall_clock_minutes,
                },
            )
        if m27_raw is None:
            return _emit_blocked(
                out_dir,
                m28_outcome=OUTCOME_BLOCKED_TRAINING_LOOP,
                detail={
                    "blocked_reason": err or "m27_validation_failed",
                    "max_wall_clock_minutes": args.max_wall_clock_minutes,
                },
            )
        m27 = m27_raw
        profile = PROFILE_OPERATOR_LOCAL
        m27_path_note = str(m27_path)

    ok_outcome, posture_note = validate_m27_outcome_strict(
        m27,
        allow_partial=bool(args.allow_partial_m27_outcome),
    )
    if not ok_outcome:
        return _emit_blocked(
            out_dir,
            m28_outcome=OUTCOME_BLOCKED_TRAINING_LOOP,
            detail={
                "upstream_m27_rollout": {"m27_outcome": posture_note},
                "blocked_reason": "m27_outcome_not_completed",
                "max_wall_clock_minutes": args.max_wall_clock_minutes,
            },
        )

    episodes = m27.get("episodes") or []
    if not isinstance(episodes, list) or not episodes:
        return _emit_blocked(
            out_dir,
            m28_outcome=OUTCOME_BLOCKED_TRAINING_LOOP,
            detail={
                "blocked_reason": "no_episodes_in_m27_json",
                "max_wall_clock_minutes": args.max_wall_clock_minutes,
            },
        )

    feats, feat_meta = sc2_rollout_feature_vector_from_m27_episodes(
        list(episodes), bind_from_json=m27
    )

    ck_dir = out_dir / "checkpoints"
    t_run = time.monotonic()

    min_u = int(args.min_training_updates)
    max_u = int(args.max_training_updates)
    cadence = int(args.checkpoint_cadence_updates)
    if args.fixture_only:
        min_u = 3
        max_u = 12
        cadence = 6

    train_rec = run_bounded_rollout_feature_training(
        feats,
        min_updates=min_u,
        max_updates=max_u,
        checkpoint_cadence=cadence,
        checkpoint_dir=ck_dir,
        wall_budget_seconds=wall_secs,
        seed=int(args.seed),
        device_pref=args.device,
    )
    wall_obs = time.monotonic() - t_run

    upd = int(train_rec.get("training_update_count") or 0)
    cp_list = train_rec.get("checkpoint_paths_with_sha256") or []

    fr = str(train_rec.get("failure_reason") or "")
    if fr.startswith("torch_import_failed") or fr == "torch_missing":
        body_fail = {
            "contract_id": CONTRACT_ID,
            "milestone": MILESTONE_LABEL,
            "profile": profile,
            "m28_outcome": OUTCOME_STARTED_FAILED,
            "upstream_m27_rollout": _upstream_block(m27, m27_path_note),
            "training_attempt": _training_block(
                args,
                upd,
                wall_obs,
                feats_used=True,
                cp_count=0,
                cand_sha=None,
                train_rec=train_rec,
            ),
            "candidate_checkpoint": {
                "produced": False,
                "sha256": None,
                "promotion_status": "not_promoted_candidate_only",
            },
            "feature_derivation": feat_meta,
            "m20_m21_gate_integration": M20_M21_DEFERRED,
            "non_claims": list(NON_CLAIM_DEFAULTS),
        }
        sealed = seal_m28_body(_stamp_emit_ts(body_fail))
        write_m28_artifacts(out_dir, sealed)
        return 4

    sc2_used = True
    failure = train_rec.get("failure_reason")

    if failure == "cuda_unavailable" and args.device == "cuda":
        return _emit_blocked(
            out_dir,
            m28_outcome=OUTCOME_BLOCKED_TRAINING_LOOP,
            detail={
                "blocked_reason": "cuda_requested_but_unavailable",
                "max_wall_clock_minutes": args.max_wall_clock_minutes,
            },
        )

    if upd < min_u:
        m28_outcome = OUTCOME_BLOCKED_TRAINING_LOOP if failure else OUTCOME_STARTED_FAILED
        body_bad = {
            "contract_id": CONTRACT_ID,
            "milestone": MILESTONE_LABEL,
            "profile": profile,
            "m28_outcome": m28_outcome,
            "upstream_m27_rollout": _upstream_block(m27, m27_path_note),
            "training_attempt": _training_block(
                args,
                upd,
                wall_obs,
                feats_used=sc2_used,
                cp_count=len(cp_list),
                cand_sha=(cp_list[-1]["sha256"] if cp_list else None),
                train_rec=train_rec,
            ),
            "candidate_checkpoint": {
                "produced": bool(cp_list),
                "sha256": cp_list[-1]["sha256"] if cp_list else None,
                "promotion_status": "not_promoted_candidate_only",
            },
            "feature_derivation": feat_meta,
            "m20_m21_gate_integration": M20_M21_DEFERRED,
            "non_claims": list(NON_CLAIM_DEFAULTS),
        }
        sealed = seal_m28_body(_stamp_emit_ts(body_bad))
        write_m28_artifacts(out_dir, sealed)
        return 6

    primary_sha = cp_list[-1]["sha256"] if cp_list else None
    if cp_list:
        m28_outcome = OUTCOME_WITH_CHECKPOINT
    else:
        m28_outcome = OUTCOME_WITHOUT_CHECKPOINT

    if args.fixture_only:
        m28_outcome = OUTCOME_FIXTURE_ONLY

    body_ok: dict[str, Any] = {
        "contract_id": CONTRACT_ID,
        "milestone": MILESTONE_LABEL,
        "profile": profile,
        "m28_outcome": m28_outcome,
        "upstream_m27_rollout": _upstream_block(m27, m27_path_note),
        "training_attempt": _training_block(
            args,
            upd,
            wall_obs,
            feats_used=sc2_used,
            cp_count=len(cp_list),
            cand_sha=primary_sha,
            train_rec=train_rec,
        ),
        "candidate_checkpoint": {
            "produced": bool(cp_list),
            "sha256": primary_sha,
            "promotion_status": "not_promoted_candidate_only",
        },
        "feature_derivation": feat_meta,
        "m20_m21_gate_integration": M20_M21_DEFERRED,
        "non_claims": list(NON_CLAIM_DEFAULTS),
    }
    sealed_ok = seal_m28_body(_stamp_emit_ts(body_ok))
    write_m28_artifacts(out_dir, sealed_ok)
    return 0


def _upstream_block(m27: dict[str, Any], path_note: str) -> dict[str, Any]:
    eps = m27.get("episodes") or []
    action_summary: list[int] = []
    if isinstance(eps, list):
        for e in eps:
            if isinstance(e, dict):
                action_summary.append(int(e.get("action_count") or 0))
    bind = m27.get("training_loop_binding") or {}
    artifact_sha = str(m27.get("artifact_sha256") or "")
    return {
        "path_role": "operator_local_input"
        if path_note != "fixture_inline_m27_shape"
        else "fixture_ci_inline",
        "resolved_path": path_note,
        "contract_id": str(m27.get("contract_id") or ""),
        "sha256": artifact_sha,
        "outcome": str(m27.get("m27_outcome") or ""),
        "action_count_summary": action_summary,
        "training_loop_binding_status": str(bind.get("status") or ""),
        "rollup_features_sha256": str(bind.get("rollup_features_sha256") or ""),
    }


def _training_block(
    args: argparse.Namespace,
    upd: int,
    wall_obs: float,
    *,
    feats_used: bool,
    cp_count: int,
    cand_sha: str | None,
    train_rec: dict[str, Any],
) -> dict[str, Any]:
    return {
        "run_tier": RUN_TIER_T1_30_MIN,
        "max_wall_clock_minutes": float(args.max_wall_clock_minutes),
        "sc2_backed_features_used": feats_used,
        "training_update_count": upd,
        "wall_clock_seconds": round(
            float(train_rec.get("wall_clock_seconds_observed") or wall_obs), 3
        ),
        "checkpoint_count": cp_count,
        "candidate_checkpoint_sha256": cand_sha,
        "training_condition_label": TRAINING_CONDITION_LABEL,
        "checkpoint_cadence_updates": int(args.checkpoint_cadence_updates),
        "min_training_updates": int(args.min_training_updates),
        "max_training_updates": int(args.max_training_updates),
        "device_observed": train_rec.get("device"),
        "loss_tail": train_rec.get("loss_tail"),
    }


if __name__ == "__main__":
    raise SystemExit(main())
