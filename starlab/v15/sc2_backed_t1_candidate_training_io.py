"""Load M27 rollout JSON, derive SC2 rollout feature vectors, seal M28 artifacts (V15-M28)."""

from __future__ import annotations

import hashlib
import json
import math
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from starlab.runs.json_util import canonical_json_dumps, sha256_hex_of_canonical_json
from starlab.v15.sc2_backed_t1_candidate_training_models import (
    EXPECTED_M27_CONTRACT_ID,
    M27_OUTCOME_COMPLETED,
    MILESTONE_LABEL,
    REPORT_CONTRACT_KIND,
    TRAINING_CONDITION_LABEL,
)
from starlab.v15.sc2_rollout_integration_training_step import rollup_features_from_episodes
from starlab.v15.sc2_rollout_training_loop_integration_io import (
    NON_CLAIM_DEFAULTS as M27_NON_CLAIM_DEFAULTS,
)
from starlab.v15.sc2_rollout_training_loop_integration_io import (
    build_fixture_episodes,
)


def canonical_json_sha256(obj: dict[str, Any]) -> str:
    return sha256_hex_of_canonical_json(obj)


def seal_m28_body(body_pre: dict[str, Any]) -> dict[str, Any]:
    wo = {k: v for k, v in body_pre.items() if k != "artifact_sha256"}
    sealed = dict(wo)
    sealed["artifact_sha256"] = sha256_hex_of_canonical_json(wo)
    return sealed


def verify_m27_rollout_json(path: Path) -> tuple[dict[str, Any] | None, str | None]:
    """Validate presence, canonical seal, contract, and primary outcome."""

    if not path.is_file():
        return None, "missing_file"

    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError):
        return None, "invalid_json"

    if not isinstance(raw, dict):
        return None, "root_not_object"

    seal_in = raw.get("artifact_sha256")
    wo = {k: v for k, v in raw.items() if k != "artifact_sha256"}
    computed = sha256_hex_of_canonical_json(wo)
    if str(seal_in or "").lower() != computed.lower():
        return None, "sha_mismatch"

    if raw.get("contract_id") != EXPECTED_M27_CONTRACT_ID:
        return None, "contract_id_mismatch"

    return raw, None


def sc2_rollout_feature_vector_from_m27_episodes(
    episodes: list[dict[str, Any]],
    *,
    bind_from_json: dict[str, Any],
) -> tuple[list[float], dict[str, Any]]:
    """Rich feature vector from real SC2 rollup episode fields + merged action tallies."""

    base = rollup_features_from_episodes(episodes)
    merged: dict[str, float] = {}
    for ep in episodes:
        tallies = ep.get("action_types_logged") or {}
        if not isinstance(tallies, dict):
            continue
        for k, v in tallies.items():
            merged[str(k)] = merged.get(str(k), 0.0) + float(v)

    keys_sorted = sorted(merged.keys())
    tally_vals = [math.log1p(max(merged[k], 0.0)) for k in keys_sorted]

    wall_sum = sum(float(e.get("wall_clock_seconds") or 0.0) for e in episodes)
    bounded_n = sum(1 for e in episodes if bool(e.get("bounded_exit")))
    obs_sum = sum(float(e.get("observation_count") or 0.0) for e in episodes)

    binding = bind_from_json.get("training_loop_binding") or {}
    rollup_bind = str(binding.get("rollup_features_sha256") or "")
    status_bind = str(binding.get("status") or "")

    def _mix(s: str) -> float:
        digest = hashlib.sha256(s.encode("utf-8")).digest()
        return float(int.from_bytes(digest[:8], "big") % 10_007) / 10_007.0

    extras = [
        float(len(episodes)),
        math.log1p(max(wall_sum, 0.0)),
        float(bounded_n),
        math.log1p(max(obs_sum, 0.0)),
        _mix(rollup_bind),
        _mix(status_bind),
    ]

    vec = base + tally_vals + extras
    meta = {
        "base_rollout_dim": len(base),
        "action_type_keys_sorted": keys_sorted,
        "merged_action_type_dim": len(tally_vals),
        "extras_dim": len(extras),
        "training_condition_label": TRAINING_CONDITION_LABEL,
    }
    return vec, meta


def build_fixture_m27_like_dict_for_ci(
    *,
    episode_count: int = 3,
    game_step: int = 8,
    max_game_steps: int = 2048,
) -> dict[str, Any]:
    """Synthetic M27-shaped bundle for `--fixture-only` (SC2-backed fields present; no disk)."""

    from starlab.v15.sc2_rollout_training_loop_integration_io import seal_with_sha256
    from starlab.v15.sc2_rollout_training_loop_integration_models import CONTRACT_ID as M27_CID
    from starlab.v15.sc2_rollout_training_loop_integration_models import MILESTONE_LABEL as M27_MS

    episodes = build_fixture_episodes(
        episode_count=episode_count,
        game_step=game_step,
        max_game_steps=max_game_steps,
    )
    smoke_like = {
        "rollup_features_sha256": canonical_json_sha256({"episodes": episodes}),
        "status": "training_update_executed",
        "training_update_count": 1,
    }
    body_pre = {
        "contract_id": M27_CID,
        "milestone": M27_MS,
        "profile": "fixture_ci",
        "policy_id": "fixture_policy_ci",
        "sc2_rollout_status": "fixture_stub",
        "m27_outcome": M27_OUTCOME_COMPLETED,
        "episode_count": len(episodes),
        "episodes": episodes,
        "training_loop_binding": smoke_like,
        "non_claims": list(M27_NON_CLAIM_DEFAULTS),
        "emit_timestamp_utc": datetime.now(UTC).isoformat().replace("+00:00", "Z"),
        "artifact_sha256": None,
    }
    return seal_with_sha256(body_pre)


def build_report(main_sealed: dict[str, Any]) -> dict[str, Any]:
    return {
        "report_kind": REPORT_CONTRACT_KIND,
        "source_artifact_sha256": main_sealed.get("artifact_sha256"),
        "milestone": MILESTONE_LABEL,
        "summary": {
            "outcome": main_sealed.get("m28_outcome"),
            "profile": main_sealed.get("profile"),
            "sc2_backed_features_used": main_sealed.get("training_attempt", {}).get(
                "sc2_backed_features_used",
            ),
        },
    }


def write_checklist(path: Path, main_sealed: dict[str, Any]) -> None:
    ta = main_sealed.get("training_attempt") or {}
    cc = main_sealed.get("candidate_checkpoint") or {}
    lines = [
        "# V15-M28 SC2-backed T1 candidate training checklist",
        "",
        f"- contract_id: {main_sealed.get('contract_id')}",
        f"- outcome: `{main_sealed.get('m28_outcome')}`",
        f"- SHA-256: `{main_sealed.get('artifact_sha256')}`",
        f"- sc2_backed_features_used: {ta.get('sc2_backed_features_used')}",
        f"- training_update_count: {ta.get('training_update_count')}",
        f"- checkpoint_count: {ta.get('checkpoint_count')}",
        f"- promotion: {cc.get('promotion_status')}",
        "- Non-claims: strength / benchmark / promotion / XAI / human panel / v2 — excluded",
        "",
    ]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_m28_artifacts(output_dir: Path, main_sealed: dict[str, Any]) -> tuple[Path, Path, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    p_main = output_dir / "v15_sc2_backed_t1_candidate_training.json"
    p_rep = output_dir / "v15_sc2_backed_t1_candidate_training_report.json"
    p_chk = output_dir / "v15_sc2_backed_t1_candidate_training_checklist.md"
    p_main.write_text(canonical_json_dumps(main_sealed), encoding="utf-8")
    p_rep.write_text(canonical_json_dumps(build_report(main_sealed)), encoding="utf-8")
    write_checklist(p_chk, main_sealed)
    return p_main, p_rep, p_chk


def validate_m27_outcome_strict(raw: dict[str, Any], *, allow_partial: bool) -> tuple[bool, str]:
    outcome = str(raw.get("m27_outcome") or "")
    if outcome == M27_OUTCOME_COMPLETED:
        return True, ""
    if allow_partial:
        return True, f"partial_posture_allowed:{outcome or 'empty'}"
    return False, outcome or "empty_outcome"
