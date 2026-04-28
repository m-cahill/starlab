"""V15-M27 — operator-local SC2 rollout + training-loop integration artifact runner."""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path
from typing import Any

from starlab.runs.json_util import canonical_json_dumps, sha256_hex_of_canonical_json
from starlab.sc2.artifacts import ExecutionProofRecord
from starlab.sc2.harness import run_match_execution
from starlab.sc2.match_config import (
    BURNYSC2_OPPONENT_MODE_PASSIVE_BOT,
    BURNYSC2_POLICY_PASSIVE,
    BURNYSC2_POLICY_V15_M27_NONTRIVIAL_MACRO_SMOKE_V1,
    match_config_from_mapping,
    match_config_to_mapping,
)
from starlab.v15.sc2_rollout_integration_training_step import (
    execute_rollout_derived_integration_training_smoke,
    rollup_features_from_episodes,
)
from starlab.v15.sc2_rollout_training_loop_integration_io import (
    NON_CLAIM_DEFAULTS,
    build_fixture_episodes,
    build_main_body,
    classify_rollout_success,
    compute_episodes_rollup_sha,
    seal_with_sha256,
    summarize_episode_from_proof,
    training_binding_from_smoke,
    write_artifacts,
)
from starlab.v15.sc2_rollout_training_loop_integration_models import (
    OUTCOME_BLOCKED_POLICY,
    OUTCOME_BLOCKED_RUNTIME,
    OUTCOME_COMPLETED,
    OUTCOME_FIXTURE_ONLY,
    OUTCOME_ROLLOUT_ONLY,
    POLICY_ID_M27_MACRO_SMOKE,
    PROFILE_FIXTURE_CI,
    PROFILE_OPERATOR_LOCAL,
    STATUS_ARTIFACT_EMITTED,
    STATUS_NOT_CONNECTED,
)


def _proof_to_dict(rec: ExecutionProofRecord) -> dict[str, Any]:
    from dataclasses import asdict

    return asdict(rec)


def default_match_base(
    *,
    policy: str,
    seed: int,
    game_step: int,
    max_game_steps: int,
) -> dict[str, Any]:
    """Default discover-maps BurnySc2 config (mirrors harness tests)."""

    return {
        "schema_version": "1",
        "adapter": "burnysc2",
        "seed": seed,
        "bounded_horizon": {"game_step": game_step, "max_game_steps": max_game_steps},
        "map": {"discover_under_maps_dir": True},
        "opponent_mode": BURNYSC2_OPPONENT_MODE_PASSIVE_BOT,
        "burnysc2_policy": policy,
        "computer_difficulty": "Easy",
    }


def run_operator_episodes_default_config(
    *,
    episode_count: int,
    policy_burny: str,
    base_seed: int,
    game_step: int,
    max_game_steps: int,
) -> tuple[list[dict[str, Any]], str | None]:
    episodes: list[dict[str, Any]] = []
    blocker: str | None = None

    for ep in range(episode_count):
        raw = default_match_base(
            policy=policy_burny,
            seed=base_seed + ep,
            game_step=game_step,
            max_game_steps=max_game_steps,
        )
        cfg = match_config_from_mapping(raw)
        t0 = time.perf_counter()
        hres = run_match_execution(cfg, output_dir=None)
        dt = time.perf_counter() - t0
        if not hres.ok or hres.proof is None:
            blocker = hres.message or "match_execution_failed"
            break
        proof_d = _proof_to_dict(hres.proof)
        ep_id = sha256_hex_of_canonical_json(match_config_to_mapping(cfg))[:16]
        episodes.append(
            summarize_episode_from_proof(
                episode_id=ep_id,
                episode_index=ep,
                proof_dict=proof_d,
                game_step=game_step,
                max_game_steps=max_game_steps,
                wall_seconds=dt,
            ),
        )

    return episodes, blocker


def run_operator_match_config_multi_episode(
    *,
    raw_template: dict[str, Any],
    episode_count: int,
) -> tuple[list[dict[str, Any]], str | None]:
    summaries: list[dict[str, Any]] = []
    base_seed = int(raw_template.get("seed", 0))

    for ep in range(episode_count):
        raw_ep = dict(raw_template)
        raw_ep["seed"] = base_seed + ep
        try:
            cfg_ep = match_config_from_mapping(raw_ep)
        except (TypeError, ValueError, KeyError) as exc:
            return summaries, f"match_config_invalid:{exc}"

        t0 = time.perf_counter()
        hres = run_match_execution(cfg_ep, output_dir=None)
        dt = time.perf_counter() - t0
        if not hres.ok or hres.proof is None:
            return summaries, hres.message or "match_execution_failed"

        proof_d = _proof_to_dict(hres.proof)
        seed_cfg = match_config_to_mapping(cfg_ep)
        ep_id = sha256_hex_of_canonical_json(seed_cfg)[:16]
        summaries.append(
            summarize_episode_from_proof(
                episode_id=ep_id,
                episode_index=ep,
                proof_dict=proof_d,
                game_step=cfg_ep.bounded_horizon.game_step,
                max_game_steps=cfg_ep.bounded_horizon.max_game_steps,
                wall_seconds=dt,
            ),
        )

    return summaries, None


def apply_training_smoke_binding(
    episodes: list[dict[str, Any]],
) -> dict[str, Any]:
    rollup_sha = compute_episodes_rollup_sha(episodes)
    feats = rollup_features_from_episodes(episodes)
    smoke = execute_rollout_derived_integration_training_smoke(feats)
    return training_binding_from_smoke(smoke, rollup_sha256=rollup_sha)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="python -m starlab.v15.run_v15_m27_sc2_rollout_training_loop_integration",
        description="V15-M27 SC2 rollout + training-loop integration (operator-local or fixture).",
    )
    parser.add_argument(
        "--allow-operator-local-execution",
        action="store_true",
        help="Guard: required for non-fixture runs that touch SC2 runtime.",
    )
    parser.add_argument(
        "--authorize-sc2-rollout",
        action="store_true",
        help="Guard: authorizes bounded operator-local SC2 rollout.",
    )
    parser.add_argument(
        "--fixture-only",
        action="store_true",
        help="CI-safe path: synthetic episodes + integration smoke (no SC2).",
    )
    parser.add_argument(
        "--policy-id",
        default=POLICY_ID_M27_MACRO_SMOKE,
        help="Governed policy ID (default: v15_m27_nontrivial_macro_smoke_policy_v1).",
    )
    parser.add_argument("--episodes", type=int, default=3)
    parser.add_argument("--game-step", type=int, default=8)
    parser.add_argument("--max-game-steps", type=int, default=2048)
    parser.add_argument("--base-seed", type=int, default=42)
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument(
        "--match-config-json",
        type=Path,
        default=None,
        help="Optional BurnySc2 match JSON per episode (--seed incremented per episode).",
    )
    args = parser.parse_args(argv)

    out_dir = args.output_dir.resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    policy_burny = BURNYSC2_POLICY_V15_M27_NONTRIVIAL_MACRO_SMOKE_V1
    if args.policy_id != POLICY_ID_M27_MACRO_SMOKE:
        sys.stderr.write(
            "error: only v15_m27_nontrivial_macro_smoke_policy_v1 is wired in this milestone\n",
        )
        return 2

    rollout_status = "operator_rollout_failed"
    m27_outcome = OUTCOME_BLOCKED_POLICY
    training_binding: dict[str, Any] = {
        "status": STATUS_NOT_CONNECTED,
        "training_update_count": 0,
        "notes": [],
    }
    episodes_final: list[dict[str, Any]]

    if args.fixture_only:
        episodes_final = build_fixture_episodes(
            episode_count=args.episodes,
            game_step=args.game_step,
            max_game_steps=args.max_game_steps,
        )
        ok_roll, _why = classify_rollout_success(episodes_final)
        rollout_status = "fixture_ci" if ok_roll else "fixture_only"
        training_binding = apply_training_smoke_binding(episodes_final)
        m27_outcome = OUTCOME_FIXTURE_ONLY if ok_roll else OUTCOME_BLOCKED_POLICY
        training_binding.setdefault("notes", []).append("fixture_only_no_live_sc2")

    elif not args.allow_operator_local_execution or not args.authorize_sc2_rollout:
        sys.stderr.write(
            "error: operator SC2 requires --allow-operator-local-execution "
            "and --authorize-sc2-rollout\n",
        )
        return 2

    elif args.match_config_json is not None:
        raw_mc = json.loads(args.match_config_json.read_text(encoding="utf-8"))
        if not isinstance(raw_mc, dict):
            sys.stderr.write("error: match config must be a JSON object\n")
            return 2
        raw_mc.setdefault("burnysc2_policy", policy_burny)
        pol_check = str(raw_mc.get("burnysc2_policy"))
        if pol_check == BURNYSC2_POLICY_PASSIVE:
            episodes_final = []
            training_binding["notes"].append(
                "burnysc2_policy passive yields zero harness actions — use " + policy_burny,
            )
            m27_outcome = OUTCOME_BLOCKED_POLICY
            rollout_status = "operator_rollout_failed"
        else:
            episodes_final, blocker = run_operator_match_config_multi_episode(
                raw_template=dict(raw_mc),
                episode_count=args.episodes,
            )
            if blocker:
                lowered = blocker.lower()
                if "import" in lowered or "probe" in lowered or "not installed" in lowered:
                    m27_outcome = OUTCOME_BLOCKED_RUNTIME
                else:
                    m27_outcome = (
                        OUTCOME_BLOCKED_RUNTIME if "runtime" in lowered else OUTCOME_BLOCKED_POLICY
                    )  # noqa: E501
                rollout_status = "operator_rollout_failed"
                training_binding["notes"].append(blocker)
            else:
                ok_roll, _reason = classify_rollout_success(episodes_final)
                has_zero = any(int(e.get("action_count") or 0) == 0 for e in episodes_final)
                if ok_roll and not has_zero:
                    rollout_status = "operator_rollout_completed"
                    training_binding = apply_training_smoke_binding(episodes_final)
                    m27_outcome = OUTCOME_COMPLETED
                elif ok_roll:
                    rollout_status = "operator_rollout_completed"
                    training_binding = apply_training_smoke_binding(episodes_final)
                    training_binding.setdefault("notes", []).append(
                        "some episode action_count zero — still emitting rollup smoke",
                    )
                    m27_outcome = OUTCOME_COMPLETED
                elif not ok_roll and not has_zero:
                    rollout_status = "operator_rollout_completed"
                    training_binding = apply_training_smoke_binding(episodes_final)
                    m27_outcome = OUTCOME_ROLLOUT_ONLY
                else:
                    rollout_status = "operator_rollout_completed"
                    rollup_sha = compute_episodes_rollup_sha(episodes_final)
                    training_binding = {
                        "status": STATUS_ARTIFACT_EMITTED,
                        "training_update_count": 0,
                        "rollup_features_sha256": rollup_sha,
                        "training_smoke": execute_rollout_derived_integration_training_smoke(
                            rollup_features_from_episodes(episodes_final),
                        ),
                        "notes": ["episodes_below_two_nonzero_action_gate"],
                    }
                    m27_outcome = OUTCOME_ROLLOUT_ONLY

    else:
        episodes_final, blocker = run_operator_episodes_default_config(
            episode_count=args.episodes,
            policy_burny=policy_burny,
            base_seed=args.base_seed,
            game_step=args.game_step,
            max_game_steps=args.max_game_steps,
        )
        if blocker:
            lowered = blocker.lower()
            if (
                "import" in lowered
                or "probe" in lowered
                or "not installed" in lowered
                or "sc2" in lowered
            ):
                m27_outcome = OUTCOME_BLOCKED_RUNTIME
            else:
                m27_outcome = OUTCOME_BLOCKED_POLICY
            rollout_status = "operator_rollout_failed"
            training_binding["notes"].append(blocker)
        elif not episodes_final:
            m27_outcome = OUTCOME_BLOCKED_RUNTIME
            rollout_status = "operator_rollout_failed"
        else:
            ok_roll, _reason = classify_rollout_success(episodes_final)
            has_zero = any(int(e.get("action_count") or 0) == 0 for e in episodes_final)
            if ok_roll and not has_zero:
                rollout_status = "operator_rollout_completed"
                training_binding = apply_training_smoke_binding(episodes_final)
                m27_outcome = OUTCOME_COMPLETED
            elif ok_roll:
                rollout_status = "operator_rollout_completed"
                training_binding = apply_training_smoke_binding(episodes_final)
                m27_outcome = OUTCOME_COMPLETED
            else:
                rollout_status = "operator_rollout_completed"
                rollup_sha = compute_episodes_rollup_sha(episodes_final)
                training_binding = {
                    "status": STATUS_ARTIFACT_EMITTED,
                    "training_update_count": 0,
                    "rollup_features_sha256": rollup_sha,
                    "training_smoke": execute_rollout_derived_integration_training_smoke(
                        rollup_features_from_episodes(episodes_final),
                    ),
                    "notes": ["insufficient_episodes_over_action_threshold"],
                }
                m27_outcome = OUTCOME_ROLLOUT_ONLY

    body_pre = build_main_body(
        profile=PROFILE_FIXTURE_CI if args.fixture_only else PROFILE_OPERATOR_LOCAL,
        policy_id=args.policy_id,
        episode_count=len(episodes_final),
        episodes=episodes_final,
        training_binding=training_binding,
        rollout_status=rollout_status,
        m27_outcome=m27_outcome,
    )
    main_sealed = seal_with_sha256(body_pre)

    write_artifacts(out_dir, main_sealed)

    side = {
        "m27_summary": m27_outcome,
        "fixture_mode": bool(args.fixture_only),
        "policy_id": args.policy_id,
        "non_claims": list(NON_CLAIM_DEFAULTS),
    }
    (out_dir / "v15_m27_run_sidecar.json").write_text(
        canonical_json_dumps(side),
        encoding="utf-8",
    )

    print(f"m27_outcome={m27_outcome}")
    print(f"artifact_sha256={main_sealed.get('artifact_sha256')}")
    print(f"wrote {out_dir}")

    fatal = m27_outcome in {OUTCOME_BLOCKED_POLICY, OUTCOME_BLOCKED_RUNTIME}
    return 1 if fatal else 0


if __name__ == "__main__":
    raise SystemExit(main())
