"""Build, seal, and validate SC2 rollout integration artifacts (V15-M27)."""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from starlab.runs.json_util import canonical_json_dumps, sha256_hex_of_canonical_json
from starlab.v15.sc2_rollout_integration_training_step import rollup_features_from_episodes
from starlab.v15.sc2_rollout_training_loop_integration_models import (
    CONTRACT_ID,
    MILESTONE_LABEL,
    REPORT_CONTRACT_KIND,
    STATUS_ARTIFACT_EMITTED,
    STATUS_NOT_CONNECTED,
    STATUS_SUMMARY_TO_TRAINING,
    STATUS_TRAINING_UPDATE,
)


def canonical_json_sha256(obj: dict[str, Any]) -> str:
    return sha256_hex_of_canonical_json(obj)


NON_CLAIM_DEFAULTS: tuple[str, ...] = (
    "not_strength_evaluation",
    "not_benchmark_pass",
    "not_checkpoint_promotion",
    "not_xai_execution",
    "not_human_panel_execution",
    "not_showcase_release",
    "not_v2_authorization",
)


def validate_integration_contract_minimum(body: dict[str, Any]) -> None:
    if body.get("contract_id") != CONTRACT_ID:
        msg = "contract_id must be starlab.v15.sc2_rollout_training_loop_integration.v1"
        raise ValueError(msg)
    if body.get("milestone") != MILESTONE_LABEL:
        msg = "milestone must be V15-M27"
        raise ValueError(msg)


def summarize_episode_from_proof(
    *,
    episode_id: str,
    episode_index: int,
    proof_dict: dict[str, Any],
    game_step: int,
    max_game_steps: int,
    wall_seconds: float,
) -> dict[str, Any]:
    """Build one episode rollup from ExecutionProofRecord mapping."""

    seq = tuple(proof_dict.get("status_sequence") or ())
    bounded = any(str(s).find("bounded_exit") >= 0 for s in seq)
    reason = (
        "bounded_exit_max_steps"
        if bounded and "bounded_exit" in str(seq[-1]).lower()
        else "bounded_exit"
        if bounded
        else "not_bounded"
    )
    obs_summ = tuple(proof_dict.get("observation_summaries") or ())
    loops: list[int] = []
    for o in obs_summ:
        if isinstance(o, dict):
            gl = o.get("game_loop")
            if gl is not None:
                loops.append(int(gl))

    tally = proof_dict.get("live_action_tallies")
    action_types_logged: dict[str, int] = {}
    if isinstance(tally, dict):
        action_types_logged = {str(k): int(v) for k, v in tally.items() if int(v) != 0}

    return {
        "episode_id": episode_id,
        "episode_index": episode_index,
        "map": str(proof_dict.get("map_logical_key") or ""),
        "race": "Terran",
        "game_step": game_step,
        "max_game_steps": max_game_steps,
        "observed_game_loops": max(loops) if loops else 0,
        "observation_count": len(obs_summ),
        "action_count": int(proof_dict.get("action_count") or 0),
        "bounded_exit": bounded,
        "bounded_exit_reason": reason,
        "sc2_game_result": str(proof_dict.get("sc2_game_result") or ""),
        "wall_clock_seconds": round(wall_seconds, 3),
        "action_types_logged": action_types_logged,
        "artifact_refs": [],
    }


def build_fixture_episodes(
    *,
    episode_count: int,
    game_step: int,
    max_game_steps: int,
) -> list[dict[str, Any]]:
    """Synthetic episodes for CI — nonzero actions, no SC2."""

    episodes: list[dict[str, Any]] = []
    for i in range(episode_count):
        ac = 4 + i
        episodes.append(
            {
                "episode_id": f"fixture_ep_{i}",
                "episode_index": i,
                "map": "fixture_stub",
                "race": "Terran",
                "game_step": game_step,
                "max_game_steps": max_game_steps,
                "observed_game_loops": min(256 * (i + 1), max_game_steps * 8),
                "observation_count": max_game_steps // 2 + i,
                "action_count": ac,
                "bounded_exit": True,
                "bounded_exit_reason": "bounded_exit_fixture",
                "sc2_game_result": "fixture",
                "wall_clock_seconds": 0.001,
                "action_types_logged": {"fixture_macro_applied": ac},
                "artifact_refs": [],
                "implementation_note": "fixture_stub_ci synthetic episode — no live SC2",
            },
        )
    return episodes


def classify_rollout_success(
    episodes: list[dict[str, Any]],
    *,
    min_episodes_with_actions: int = 2,
) -> tuple[bool, str]:
    nz = sum(1 for e in episodes if int(e.get("action_count") or 0) > 0)
    ok = nz >= min_episodes_with_actions
    if not episodes:
        return False, "no_episodes"
    if not ok:
        return False, "insufficient_nonzero_action_episodes"
    return True, "ok"


def build_main_body(
    *,
    profile: str,
    policy_id: str,
    episode_count: int,
    episodes: list[dict[str, Any]],
    training_binding: dict[str, Any],
    rollout_status: str,
    m27_outcome: str,
    artifact_sha256: str | None = None,
) -> dict[str, Any]:
    body: dict[str, Any] = {
        "contract_id": CONTRACT_ID,
        "milestone": MILESTONE_LABEL,
        "profile": profile,
        "policy_id": policy_id,
        "sc2_rollout_status": rollout_status,
        "m27_outcome": m27_outcome,
        "episode_count": episode_count,
        "episodes": episodes,
        "training_loop_binding": training_binding,
        "non_claims": list(NON_CLAIM_DEFAULTS),
        "artifact_sha256": artifact_sha256,
        "emit_timestamp_utc": datetime.now(UTC).isoformat().replace("+00:00", "Z"),
    }
    return body


def seal_with_sha256(body_pre: dict[str, Any]) -> dict[str, Any]:
    """Add artifact_sha256 over body without that field."""

    wo = {k: v for k, v in body_pre.items() if k != "artifact_sha256"}
    sealed = dict(wo)
    sealed["artifact_sha256"] = sha256_hex_of_canonical_json(wo)
    return sealed


def build_report(main_sealed: dict[str, Any]) -> dict[str, Any]:
    return {
        "report_kind": REPORT_CONTRACT_KIND,
        "source_artifact_sha256": main_sealed.get("artifact_sha256"),
        "milestone": MILESTONE_LABEL,
        "summary": {
            "outcome": main_sealed.get("m27_outcome"),
            "episode_count": main_sealed.get("episode_count"),
            "profile": main_sealed.get("profile"),
            "binding_status": (main_sealed.get("training_loop_binding") or {}).get("status"),
        },
    }


def write_checklist(path: Path, main_sealed: dict[str, Any]) -> None:
    lines = [
        "# V15-M27 SC2 rollout integration checklist",
        "",
        f"- contract_id: {main_sealed.get('contract_id')}",
        f"- outcome: `{main_sealed.get('m27_outcome')}`",
        f"- SHA-256: `{main_sealed.get('artifact_sha256')}`",
        "- Non-claims: strength / benchmark / promotion / XAI / human panel / v2 — excluded",
        "",
    ]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_artifacts(output_dir: Path, main_sealed: dict[str, Any]) -> tuple[Path, Path, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    p_main = output_dir / "v15_sc2_rollout_training_loop_integration.json"
    p_rep = output_dir / "v15_sc2_rollout_training_loop_integration_report.json"
    p_chk = output_dir / "v15_sc2_rollout_training_loop_integration_checklist.md"
    p_main.write_text(canonical_json_dumps(main_sealed), encoding="utf-8")
    rep = build_report(main_sealed)
    p_rep.write_text(canonical_json_dumps(rep), encoding="utf-8")
    write_checklist(p_chk, main_sealed)
    return p_main, p_rep, p_chk


def training_binding_from_smoke(
    smoke: dict[str, Any],
    *,
    rollup_sha256: str,
) -> dict[str, Any]:
    exec_ok = bool(smoke.get("training_update_executed"))
    notes_seed = str(smoke.get("notes", ""))
    note_list: list[str] = [notes_seed] if notes_seed else []
    binding: dict[str, Any] = {
        "status": STATUS_TRAINING_UPDATE if exec_ok else STATUS_SUMMARY_TO_TRAINING,
        "training_update_count": 1 if exec_ok else 0,
        "rollup_features_sha256": rollup_sha256,
        "training_smoke": smoke,
        "notes": note_list,
    }
    if exec_ok:
        note_list.append("integration_torch_sgd_step_from_rollup_features")
    else:
        note_list.append("torch_step_skipped_torch_unavailable")
    return binding


def compute_episodes_rollup_sha(episodes: list[dict[str, Any]]) -> str:
    feats = rollup_features_from_episodes(episodes)
    return sha256_hex_of_canonical_json(
        {"rollup_features": feats, "episode_count": len(episodes)},
    )


def integration_json_for_preflight_checks(path: Path) -> dict[str, Any]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ValueError("integration JSON root must be object")
    validate_integration_contract_minimum(raw)
    bind = raw.get("training_loop_binding") or {}
    status = str(bind.get("status", ""))
    if status not in {
        STATUS_NOT_CONNECTED,
        STATUS_ARTIFACT_EMITTED,
        STATUS_SUMMARY_TO_TRAINING,
        STATUS_TRAINING_UPDATE,
    }:
        raise ValueError("training_loop_binding.status not recognized")
    return raw
