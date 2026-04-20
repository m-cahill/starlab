"""PX2-native bounded campaign execution skeleton (PX2-M03 slice 2)."""

from __future__ import annotations

import random
import shutil
import tempfile
import uuid
from pathlib import Path
from typing import Any, Final

import torch

from starlab.runs.json_util import sha256_hex_of_canonical_json
from starlab.sc2.px2.bootstrap.dataset_contract import load_examples_from_dataset_file
from starlab.sc2.px2.bootstrap.emit_replay_bootstrap_dataset import emit_from_corpus
from starlab.sc2.px2.bootstrap.feature_adapter import observation_feature_dim
from starlab.sc2.px2.bootstrap.policy_model import BootstrapTerranPolicy
from starlab.sc2.px2.self_play.campaign_contract import (
    PX2_SELF_PLAY_CAMPAIGN_CONTRACT_ID,
    build_px2_self_play_campaign_artifacts,
)
from starlab.sc2.px2.self_play.checkpoint_receipts import build_checkpoint_receipt_artifacts
from starlab.sc2.px2.self_play.evaluation_receipts import build_evaluation_receipt_artifacts
from starlab.sc2.px2.self_play.opponent_selection import (
    OPPONENT_SELECTION_ROUND_ROBIN,
    select_opponent_ref,
)
from starlab.sc2.px2.self_play.policy_runtime_bridge import bootstrap_policy_runtime_step
from starlab.sc2.px2.self_play.run_artifacts import (
    build_run_manifest,
    default_run_subdirs,
    write_json,
)
from starlab.sc2.px2.self_play.snapshot_pool import build_default_opponent_pool_stub

PX2_SELF_PLAY_CAMPAIGN_RUN_CONTRACT_ID: Final[str] = "starlab.px2.self_play_campaign_run.v1"
PX2_SELF_PLAY_CAMPAIGN_RUN_REPORT_CONTRACT_ID: Final[str] = (
    "starlab.px2.self_play_campaign_run_report.v1"
)

EXECUTION_KIND_SLICE2: Final[str] = "px2_m03_slice2_execution_skeleton_v1"


def _seal_campaign_run_body(body_without_seal: dict[str, Any]) -> str:
    return sha256_hex_of_canonical_json(body_without_seal)


def run_px2_campaign_execution_skeleton(
    *,
    corpus_root: Path,
    output_dir: Path,
    campaign_id: str = "px2_m03_skeleton_campaign_001",
    campaign_profile_id: str = "px2_m03_slice2_skeleton_v1",
    run_id: str | None = None,
    torch_seed: int = 42,
    fixture_episode_count: int = 3,
    checkpoint_episode_cadence: int = 2,
    eval_episode_cadence: int = 2,
) -> dict[str, Any]:
    """Run bounded multi-episode skeleton; write run JSON, manifest, checkpoint/eval receipts.

    Returns a summary dict with paths and seals for tests.
    """

    random.seed(torch_seed)
    torch.manual_seed(torch_seed)

    rid = run_id or f"px2_run_{uuid.uuid4().hex[:12]}"
    pool = build_default_opponent_pool_stub()
    ref_ids = tuple(r.ref_id for r in pool.snapshot_refs)

    campaign, _campaign_report = build_px2_self_play_campaign_artifacts(
        campaign_id=campaign_id,
        campaign_profile_id=campaign_profile_id,
        opponent_pool=pool,
        opponent_selection_rule_id=OPPONENT_SELECTION_ROUND_ROBIN,
        torch_seed=torch_seed,
    )
    campaign_sha = str(campaign["campaign_sha256"])

    tmp_emit = Path(tempfile.mkdtemp(prefix="px2_m03_skeleton_dataset_"))
    try:
        emit_from_corpus(corpus_root, tmp_emit)
        examples = load_examples_from_dataset_file(tmp_emit / "px2_replay_bootstrap_dataset.json")
    finally:
        shutil.rmtree(tmp_emit, ignore_errors=True)

    if len(examples) < 1:
        msg = "corpus must yield at least one labeled example"
        raise ValueError(msg)

    model = BootstrapTerranPolicy(input_dim=observation_feature_dim())
    episodes_out: list[dict[str, Any]] = []
    checkpoint_paths: list[str] = []
    eval_paths: list[str] = []

    out = output_dir.resolve()
    sub = default_run_subdirs()
    ckpt_dir = out / sub["checkpoints"]
    eval_dir = out / sub["evaluations"]

    for ep in range(fixture_episode_count):
        ex = examples[ep % len(examples)]
        obs = ex["observation_surface"]
        gss = ex["game_state_snapshot"]
        opponent_ref = select_opponent_ref(
            step_index=ep,
            rule_id=OPPONENT_SELECTION_ROUND_ROBIN,
            ref_ids=ref_ids,
        )
        bridge = bootstrap_policy_runtime_step(model, obs, gss)
        games_done = ep + 1
        episodes_out.append(
            {
                "episode_index_zero_based": ep,
                "episode_index_one_based": games_done,
                "example_id": ex.get("example_id"),
                "opponent_snapshot_ref": opponent_ref,
                "bridge": bridge.to_json_dict(),
            }
        )

        if games_done % checkpoint_episode_cadence == 0:
            ck_r, ck_rep = build_checkpoint_receipt_artifacts(
                campaign_id=campaign_id,
                run_id=rid,
                campaign_sha256=campaign_sha,
                episode_index_one_based=games_done,
                games_completed_in_run=games_done,
                policy_snapshot_note=(
                    "Deterministic BootstrapTerranPolicy; slice-2 skeleton — no weight save."
                ),
            )
            stem = f"ckpt_ep{games_done:03d}"
            p_ck = ckpt_dir / f"{stem}.json"
            p_ck_rep = ckpt_dir / f"{stem}_report.json"
            write_json(p_ck, ck_r)
            write_json(p_ck_rep, ck_rep)
            checkpoint_paths.append(p_ck.relative_to(out).as_posix())

        if games_done % eval_episode_cadence == 0:
            ev_r, ev_rep = build_evaluation_receipt_artifacts(
                campaign_id=campaign_id,
                run_id=rid,
                campaign_sha256=campaign_sha,
                episode_index_one_based=games_done,
                games_completed_in_run=games_done,
                eval_modes=["offline_fixture", "slice2_skeleton"],
                metrics_stub={
                    "decode_compile_ok_rate": 1.0,
                    "episodes_completed": games_done,
                },
            )
            stem = f"eval_ep{games_done:03d}"
            p_ev = eval_dir / f"{stem}.json"
            p_ev_rep = eval_dir / f"{stem}_report.json"
            write_json(p_ev, ev_r)
            write_json(p_ev_rep, ev_rep)
            eval_paths.append(p_ev.relative_to(out).as_posix())

    run_body: dict[str, Any] = {
        "contract_id": PX2_SELF_PLAY_CAMPAIGN_RUN_CONTRACT_ID,
        "campaign_id": campaign_id,
        "run_id": rid,
        "campaign_sha256": campaign_sha,
        "linked_campaign_contract_id": PX2_SELF_PLAY_CAMPAIGN_CONTRACT_ID,
        "execution_kind": EXECUTION_KIND_SLICE2,
        "torch_seed": torch_seed,
        "fixture_episode_count": fixture_episode_count,
        "episodes": episodes_out,
        "checkpoint_receipt_paths": checkpoint_paths,
        "evaluation_receipt_paths": eval_paths,
        "promotion_posture_stub": "deferred_not_enacted_in_skeleton",
        "rollback_posture_stub": "not_triggered_in_skeleton",
        "non_claims": [
            "Slice-2 execution skeleton — not an industrial self-play campaign.",
            "Does not prove strength, ladder performance, or Blackwell completion.",
        ],
    }
    seal = _seal_campaign_run_body({k: v for k, v in run_body.items() if k != "run_sha256"})
    campaign_run = dict(run_body)
    campaign_run["run_sha256"] = seal

    run_report: dict[str, Any] = {
        "contract_id": PX2_SELF_PLAY_CAMPAIGN_RUN_REPORT_CONTRACT_ID,
        "run_sha256": seal,
        "campaign_id": campaign_id,
        "run_id": rid,
        "summary": {
            "episodes_executed": len(episodes_out),
            "checkpoint_artifacts": len(checkpoint_paths),
            "evaluation_artifacts": len(eval_paths),
        },
        "non_claims": run_body["non_claims"],
    }

    manifest = build_run_manifest(
        campaign_id=campaign_id,
        run_id=rid,
        campaign_sha256=campaign_sha,
        execution_kind=EXECUTION_KIND_SLICE2,
        fixture_episode_count=fixture_episode_count,
        checkpoint_episode_cadence=checkpoint_episode_cadence,
        eval_episode_cadence=eval_episode_cadence,
        corpus_note="PX2-M02 fixture corpus lineage.",
        torch_seed=torch_seed,
    )

    write_json(out / "px2_self_play_campaign_run.json", campaign_run)
    write_json(out / "px2_self_play_campaign_run_report.json", run_report)
    write_json(out / "run_manifest.json", manifest)

    return {
        "output_dir": str(out),
        "run_id": rid,
        "run_sha256": seal,
        "campaign_sha256": campaign_sha,
        "checkpoint_paths": checkpoint_paths,
        "evaluation_paths": eval_paths,
        "fixture_episode_count": fixture_episode_count,
    }
