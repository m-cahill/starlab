"""Fixture-only self-play smoke: campaign wiring + deterministic artifacts."""

from __future__ import annotations

import random
import shutil
import tempfile
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
from starlab.sc2.px2.self_play.opponent_selection import (
    OPPONENT_SELECTION_ROUND_ROBIN,
    select_opponent_ref,
)
from starlab.sc2.px2.self_play.policy_runtime_bridge import bootstrap_policy_runtime_step
from starlab.sc2.px2.self_play.snapshot_pool import build_default_opponent_pool_stub

PX2_SELF_PLAY_SMOKE_RUN_CONTRACT_ID: Final[str] = "starlab.px2.self_play_smoke_run.v1"
PX2_SELF_PLAY_SMOKE_RUN_REPORT_CONTRACT_ID: Final[str] = "starlab.px2.self_play_smoke_run_report.v1"


def run_px2_fixture_self_play_smoke(
    *,
    corpus_root: Path,
    campaign_id: str = "px2_m03_smoke_fixture_campaign_001",
    campaign_profile_id: str = "px2_m03_slice1_fixture_smoke_v1",
    torch_seed: int = 42,
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    """Emit dataset from M02 corpus, run two bridge steps, build campaign + smoke JSON.

    Returns ``(campaign, campaign_report, smoke_run, smoke_report)``.
    """

    random.seed(torch_seed)
    torch.manual_seed(torch_seed)

    pool = build_default_opponent_pool_stub()
    ref_ids = tuple(r.ref_id for r in pool.snapshot_refs)

    campaign, campaign_report = build_px2_self_play_campaign_artifacts(
        campaign_id=campaign_id,
        campaign_profile_id=campaign_profile_id,
        opponent_pool=pool,
        opponent_selection_rule_id=OPPONENT_SELECTION_ROUND_ROBIN,
        torch_seed=torch_seed,
    )

    tmp_emit = Path(tempfile.mkdtemp(prefix="px2_m03_smoke_dataset_"))
    try:
        emit_from_corpus(corpus_root, tmp_emit)
        examples = load_examples_from_dataset_file(tmp_emit / "px2_replay_bootstrap_dataset.json")
    finally:
        shutil.rmtree(tmp_emit, ignore_errors=True)

    if len(examples) < 2:
        msg = "corpus must yield at least 2 labeled examples for smoke"
        raise ValueError(msg)

    model = BootstrapTerranPolicy(input_dim=observation_feature_dim())
    steps_out: list[dict[str, Any]] = []
    for step_index in range(2):
        ex = examples[step_index]
        obs = ex["observation_surface"]
        gss = ex["game_state_snapshot"]
        opponent_ref = select_opponent_ref(
            step_index=step_index,
            rule_id=OPPONENT_SELECTION_ROUND_ROBIN,
            ref_ids=ref_ids,
        )
        receipt = bootstrap_policy_runtime_step(model, obs, gss)
        steps_out.append(
            {
                "step_index": step_index,
                "example_id": ex.get("example_id"),
                "opponent_snapshot_ref": opponent_ref,
                "bridge": receipt.to_json_dict(),
            }
        )

    smoke_body: dict[str, Any] = {
        "contract_id": PX2_SELF_PLAY_SMOKE_RUN_CONTRACT_ID,
        "campaign_id": campaign_id,
        "campaign_sha256": campaign["campaign_sha256"],
        "linked_campaign_contract_id": PX2_SELF_PLAY_CAMPAIGN_CONTRACT_ID,
        "torch_seed": torch_seed,
        "fixture_corpus_note": "Uses PX2-M02 test corpus observation/snapshot lineage.",
        "steps": steps_out,
        "campaign_decisions_stub": {
            "checkpoint_would_emit": False,
            "evaluation_would_run": False,
            "promotion_deferred_in_smoke": True,
            "rollback_not_triggered_in_smoke": True,
        },
        "non_claims": [
            "Fixture smoke only — not a real SC2 match; not an industrial campaign run.",
            "Does not prove learning quality or strength.",
        ],
    }
    _smoke_body_for_seal = {k: v for k, v in smoke_body.items() if k != "smoke_sha256"}
    seal = sha256_hex_of_canonical_json(_smoke_body_for_seal)
    smoke_run = dict(smoke_body)
    smoke_run["smoke_sha256"] = seal

    smoke_report: dict[str, Any] = {
        "contract_id": PX2_SELF_PLAY_SMOKE_RUN_REPORT_CONTRACT_ID,
        "smoke_sha256": seal,
        "campaign_id": campaign_id,
        "summary": {
            "steps_executed": len(steps_out),
            "all_steps_decode_compile_ok": True,
        },
        "non_claims": smoke_body["non_claims"],
    }
    return campaign, campaign_report, smoke_run, smoke_report


def build_px2_self_play_smoke_run_artifacts(
    *,
    corpus_root: Path,
    campaign_id: str = "px2_m03_smoke_fixture_campaign_001",
    campaign_profile_id: str = "px2_m03_slice1_fixture_smoke_v1",
    torch_seed: int = 42,
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    """Library alias matching emitter naming."""

    return run_px2_fixture_self_play_smoke(
        corpus_root=corpus_root,
        campaign_id=campaign_id,
        campaign_profile_id=campaign_profile_id,
        torch_seed=torch_seed,
    )
