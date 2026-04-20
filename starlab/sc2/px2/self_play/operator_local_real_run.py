"""Bounded operator-local non-Blackwell real-run wrapper (PX2-M03 slice 7).

Uses slice-6 canonical campaign-root layout, slice-7 ``execution_kind``, and emits a governed
top-level real-run record under the campaign root.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Final

from starlab.sc2.px2.self_play.campaign_continuity import EXECUTION_KIND_SLICE7
from starlab.sc2.px2.self_play.campaign_root import run_slice5_operator_local_campaign
from starlab.sc2.px2.self_play.canonical_operator_local_run import resolve_canonical_campaign_root
from starlab.sc2.px2.self_play.operator_local_real_run_record import (
    build_px2_self_play_operator_local_real_run_artifacts,
)
from starlab.sc2.px2.self_play.run_artifacts import write_json
from starlab.sc2.px2.self_play.weight_loading import WEIGHT_MODE_INIT_ONLY, WEIGHT_MODE_WEIGHTS_FILE

DEFAULT_SLICE7_CAMPAIGN_ID: Final[str] = "px2_m03_slice7_bounded_real_run"
SLICE7_CAMPAIGN_PROFILE_ID: Final[str] = "px2_m03_slice7_bounded_operator_local_real_run_v1"


def run_bounded_operator_local_real_run(
    *,
    corpus_root: Path,
    campaign_id: str = DEFAULT_SLICE7_CAMPAIGN_ID,
    base_dir: Path | None = None,
    init_only: bool = True,
    weights_path: Path | None = None,
    weight_bundle_ref: str | None = None,
    torch_seed: int = 42,
    run_id: str | None = None,
    continuity_step_count: int = 2,
    device_intent: str = "cpu",
    map_location: str = "cpu",
) -> dict[str, Any]:
    """One bounded minutes-scale real run: full receipt tree + sealed real-run record JSON.

    Preflight runs inside continuity (init-only or real weights). Writes under
    ``resolve_canonical_campaign_root(...)``.

    **Not** industrial campaign; **not** merge-gate CI proof.
    """

    root = resolve_canonical_campaign_root(campaign_id, base_dir=base_dir)
    inner = run_slice5_operator_local_campaign(
        corpus_root=corpus_root,
        campaign_root=root,
        init_only=init_only,
        weights_path=weights_path,
        weight_bundle_ref=weight_bundle_ref,
        campaign_id=campaign_id,
        campaign_profile_id=SLICE7_CAMPAIGN_PROFILE_ID,
        torch_seed=torch_seed,
        run_id=run_id,
        continuity_step_count=continuity_step_count,
        device_intent=device_intent,
        map_location=map_location,
        execution_kind=EXECUTION_KIND_SLICE7,
    )
    rid = str(inner["run_id"])
    run_dir = root / "runs" / rid
    cont_path = run_dir / "px2_self_play_campaign_continuity.json"
    if not cont_path.is_file():
        msg = "expected continuity JSON after campaign run"
        raise RuntimeError(msg)

    cont_body = json.loads(cont_path.read_text(encoding="utf-8"))
    weight_identity = cont_body.get("weight_identity")
    if not isinstance(weight_identity, dict):
        msg = "continuity JSON missing weight_identity"
        raise RuntimeError(msg)

    non_claims = [
        "Slice-7 bounded operator-local real-run record — not industrial self-play campaign.",
        "Seal covers logical seal-basis fields only; absolute paths are advisory where present.",
        "Not Blackwell-scale; not ladder strength; not merge-gate default CI proof.",
    ]
    manifest, report = build_px2_self_play_operator_local_real_run_artifacts(
        campaign_id=campaign_id,
        campaign_profile_id=SLICE7_CAMPAIGN_PROFILE_ID,
        run_id=rid,
        torch_seed=torch_seed,
        continuity_step_count=int(cont_body["continuity_step_count"]),
        campaign_root_resolved=root,
        campaign_contract_sha256=str(inner["campaign_contract_sha256"]),
        preflight_sha256=str(inner["preflight_sha256"]),
        continuity_sha256=str(inner["continuity_sha256"]),
        continuity_chain_sha256=str(inner["continuity_chain_sha256"]),
        campaign_root_manifest_sha256=str(inner["campaign_root_manifest_sha256"] or ""),
        opponent_pool_identity_sha256=str(inner["opponent_pool_identity_sha256"]),
        weight_identity=weight_identity,
        non_claims=non_claims,
    )
    write_json(root / "px2_self_play_operator_local_real_run.json", manifest)
    write_json(root / "px2_self_play_operator_local_real_run_report.json", report)

    return {
        **inner,
        "operator_local_real_run_sha256": manifest["operator_local_real_run_sha256"],
        "weight_mode_declared": (WEIGHT_MODE_INIT_ONLY if init_only else WEIGHT_MODE_WEIGHTS_FILE),
    }
