"""Read/write M45 self-play / RL bootstrap JSON artifacts."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from starlab.runs.json_util import canonical_json_dumps, sha256_hex_of_canonical_json
from starlab.training.self_play_rl_bootstrap_models import (
    BOOTSTRAP_DATASET_FILENAME,
    EPISODE_MANIFEST_FILENAME,
    SELF_PLAY_RL_BOOTSTRAP_RUN_FILENAME,
    SELF_PLAY_RL_BOOTSTRAP_RUN_REPORT_FILENAME,
    SELF_PLAY_RL_BOOTSTRAP_RUN_REPORT_VERSION,
)


def seal_bootstrap_run_body(body_without_hash: dict[str, Any]) -> dict[str, Any]:
    """Attach ``bootstrap_run_sha256`` over the object without that field."""

    digest = sha256_hex_of_canonical_json(body_without_hash)
    return {**body_without_hash, "bootstrap_run_sha256": digest}


def minimal_report_from_run(run: dict[str, Any]) -> dict[str, Any]:
    """Compact report JSON linked to the run digest."""

    c_raw = run.get("candidate")
    cand: dict[str, Any] = c_raw if isinstance(c_raw, dict) else {}
    s_raw = run.get("reward_summary")
    summ: dict[str, Any] = s_raw if isinstance(s_raw, dict) else {}
    return {
        "report_version": SELF_PLAY_RL_BOOTSTRAP_RUN_REPORT_VERSION,
        "bootstrap_run_sha256": run["bootstrap_run_sha256"],
        "run_id": run["run_id"],
        "bootstrap_mode": run["bootstrap_mode"],
        "runtime_mode": run["runtime_mode"],
        "reward_policy_id": run["reward_policy_id"],
        "update_policy_id": run["update_policy_id"],
        "episode_count_configured": run["episode_count_configured"],
        "updated_policy_bundle_emitted": run.get("updated_policy_bundle") is not None,
        "reward_summary": {
            "mean_episode_reward_total": summ.get("mean_episode_reward_total"),
            "episode_rewards_total": summ.get("episode_rewards_total"),
        },
        "candidate": {
            "hierarchical_training_run_sha256": cand.get("hierarchical_training_run_sha256"),
            "training_run_id": cand.get("training_run_id"),
        },
        "warnings": run.get("warnings", []),
        "caveats": run.get("caveats", []),
        "non_claims": run.get("non_claims", []),
    }


def write_bootstrap_artifacts(
    *,
    run_body: dict[str, Any],
    report_body: dict[str, Any],
    output_dir: Path,
) -> tuple[Path, Path]:
    """Write run + report JSON under ``output_dir``."""

    output_dir.mkdir(parents=True, exist_ok=True)
    run_path = output_dir / SELF_PLAY_RL_BOOTSTRAP_RUN_FILENAME
    rep_path = output_dir / SELF_PLAY_RL_BOOTSTRAP_RUN_REPORT_FILENAME
    run_path.write_text(canonical_json_dumps(run_body), encoding="utf-8")
    rep_path.write_text(canonical_json_dumps(report_body), encoding="utf-8")
    return run_path, rep_path


def write_bootstrap_dataset(*, body: dict[str, Any], output_dir: Path) -> Path:
    p = output_dir / BOOTSTRAP_DATASET_FILENAME
    p.write_text(canonical_json_dumps(body), encoding="utf-8")
    return p


def write_episode_manifest(*, body: dict[str, Any], episodes_dir: Path) -> Path:
    episodes_dir.mkdir(parents=True, exist_ok=True)
    p = episodes_dir / EPISODE_MANIFEST_FILENAME
    p.write_text(canonical_json_dumps(body), encoding="utf-8")
    return p
