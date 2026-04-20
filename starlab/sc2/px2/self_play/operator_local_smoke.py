"""Bounded operator-local campaign smoke (PX2-M03 slice 3)."""

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
from starlab.sc2.px2.self_play.campaign_contract import (
    PX2_SELF_PLAY_CAMPAIGN_CONTRACT_ID,
    build_px2_self_play_campaign_artifacts,
)
from starlab.sc2.px2.self_play.execution_preflight import run_execution_preflight
from starlab.sc2.px2.self_play.opponent_selection import (
    OPPONENT_SELECTION_ROUND_ROBIN,
    select_opponent_ref,
)
from starlab.sc2.px2.self_play.policy_runtime_bridge import bootstrap_policy_runtime_step
from starlab.sc2.px2.self_play.run_artifacts import write_json
from starlab.sc2.px2.self_play.snapshot_pool import build_default_opponent_pool_stub
from starlab.sc2.px2.self_play.weight_loading import build_policy_operator_local

PX2_SELF_PLAY_OPERATOR_LOCAL_SMOKE_CONTRACT_ID: Final[str] = (
    "starlab.px2.self_play_operator_local_smoke.v1"
)
PX2_SELF_PLAY_OPERATOR_LOCAL_SMOKE_REPORT_CONTRACT_ID: Final[str] = (
    "starlab.px2.self_play_operator_local_smoke_report.v1"
)

EXECUTION_KIND_SLICE3: Final[str] = "px2_m03_slice3_operator_local_smoke_v1"


def _seal_smoke_body(body_without_seal: dict[str, Any]) -> str:
    return sha256_hex_of_canonical_json(body_without_seal)


def run_operator_local_campaign_smoke(
    *,
    corpus_root: Path,
    output_dir: Path,
    init_only: bool,
    weights_path: Path | None = None,
    weight_bundle_ref: str | None = None,
    campaign_id: str = "px2_m03_slice3_operator_local",
    campaign_profile_id: str = "px2_m03_slice3_operator_local_v1",
    torch_seed: int = 42,
    run_id: str | None = None,
    episode_budget: int = 2,
    device_intent: str = "cpu",
    map_location: str = "cpu",
) -> dict[str, Any]:
    """Run preflight, then bounded episodes with real weights or init-only policy.

    Writes preflight JSON, operator-local smoke JSON + report under ``output_dir``.
    Local-first; **not** merge-gate CI by default.
    """

    random.seed(torch_seed)
    torch.manual_seed(torch_seed)

    rid = run_id or f"px2_ol_{uuid.uuid4().hex[:12]}"
    ok, preflight, preflight_report, errors = run_execution_preflight(
        corpus_root=corpus_root,
        output_dir=output_dir,
        init_only=init_only,
        weights_path=weights_path,
        weight_bundle_ref=weight_bundle_ref,
        torch_seed=torch_seed,
        run_id=rid,
        device_intent=device_intent,
        map_location=map_location,
    )

    out = output_dir.resolve()
    write_json(out / "px2_self_play_execution_preflight.json", preflight)
    write_json(out / "px2_self_play_execution_preflight_report.json", preflight_report)

    if not ok:
        msg = "execution preflight failed: " + "; ".join(errors)
        raise ValueError(msg)

    model, weight_meta = build_policy_operator_local(
        init_only=init_only,
        weights_path=weights_path,
        torch_seed=torch_seed,
        map_location=map_location,
    )

    pool = build_default_opponent_pool_stub(campaign_tag="slice3")
    ref_ids = tuple(r.ref_id for r in pool.snapshot_refs)
    campaign, _cr = build_px2_self_play_campaign_artifacts(
        campaign_id=campaign_id,
        campaign_profile_id=campaign_profile_id,
        opponent_pool=pool,
        opponent_selection_rule_id=OPPONENT_SELECTION_ROUND_ROBIN,
        torch_seed=torch_seed,
    )
    campaign_sha = str(campaign["campaign_sha256"])

    tmp_emit = Path(tempfile.mkdtemp(prefix="px2_m03_ol_dataset_"))
    try:
        emit_from_corpus(corpus_root, tmp_emit)
        examples = load_examples_from_dataset_file(tmp_emit / "px2_replay_bootstrap_dataset.json")
    finally:
        shutil.rmtree(tmp_emit, ignore_errors=True)

    if len(examples) < 1:
        msg = "corpus must yield at least one labeled example"
        raise ValueError(msg)

    n_ep = max(1, min(episode_budget, 8))
    episodes_out: list[dict[str, Any]] = []
    for ep in range(n_ep):
        ex = examples[ep % len(examples)]
        obs = ex["observation_surface"]
        gss = ex["game_state_snapshot"]
        opponent_ref = select_opponent_ref(
            step_index=ep,
            rule_id=OPPONENT_SELECTION_ROUND_ROBIN,
            ref_ids=ref_ids,
        )
        bridge = bootstrap_policy_runtime_step(model, obs, gss)
        episodes_out.append(
            {
                "episode_index_zero_based": ep,
                "episode_index_one_based": ep + 1,
                "example_id": ex.get("example_id"),
                "opponent_snapshot_ref": opponent_ref,
                "bridge": bridge.to_json_dict(),
            }
        )

    smoke_body: dict[str, Any] = {
        "contract_id": PX2_SELF_PLAY_OPERATOR_LOCAL_SMOKE_CONTRACT_ID,
        "campaign_id": campaign_id,
        "run_id": rid,
        "campaign_sha256": campaign_sha,
        "linked_campaign_contract_id": PX2_SELF_PLAY_CAMPAIGN_CONTRACT_ID,
        "execution_kind": EXECUTION_KIND_SLICE3,
        "preflight_sha256": preflight["preflight_sha256"],
        "torch_seed": torch_seed,
        "episode_budget": n_ep,
        "weight_identity": weight_meta,
        "weight_bundle_ref": weight_bundle_ref.strip() if weight_bundle_ref else None,
        "device_intent": device_intent,
        "episodes": episodes_out,
        "non_claims": [
            "Slice-3 bounded operator-local smoke — not industrial self-play.",
            "Not Blackwell-scale; not merge-gate default CI proof.",
        ],
    }
    seal_body = {k: v for k, v in smoke_body.items() if k != "operator_local_smoke_sha256"}
    seal = _seal_smoke_body(seal_body)
    smoke = dict(smoke_body)
    smoke["operator_local_smoke_sha256"] = seal

    smoke_report: dict[str, Any] = {
        "contract_id": PX2_SELF_PLAY_OPERATOR_LOCAL_SMOKE_REPORT_CONTRACT_ID,
        "operator_local_smoke_sha256": seal,
        "campaign_id": campaign_id,
        "run_id": rid,
        "summary": {
            "episodes_executed": len(episodes_out),
            "preflight_sha256": preflight["preflight_sha256"],
        },
        "non_claims": smoke_body["non_claims"],
    }

    write_json(out / "px2_self_play_operator_local_smoke.json", smoke)
    write_json(out / "px2_self_play_operator_local_smoke_report.json", smoke_report)

    return {
        "output_dir": str(out),
        "run_id": rid,
        "operator_local_smoke_sha256": seal,
        "preflight_sha256": preflight["preflight_sha256"],
        "campaign_sha256": campaign_sha,
        "weight_identity": weight_meta,
        "episode_budget": n_ep,
    }
