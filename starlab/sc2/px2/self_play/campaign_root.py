"""Operator-local campaign root layout + slice-5 orchestration (PX2-M03)."""

from __future__ import annotations

import uuid
from pathlib import Path
from typing import Any, Final

from starlab.sc2.px2.self_play.campaign_continuity import (
    EXECUTION_KIND_SLICE5,
    EXECUTION_KIND_SLICE6,
    EXECUTION_KIND_SLICE7,
    EXECUTION_KIND_SLICE8,
    EXECUTION_KIND_SLICE11,
    EXECUTION_KIND_SLICE13,
    EXECUTION_KIND_SLICE14,
    EXECUTION_KIND_SLICE16,
    run_operator_local_campaign_continuity,
)
from starlab.sc2.px2.self_play.campaign_root_manifest import (
    build_px2_self_play_campaign_root_manifest_artifacts,
)
from starlab.sc2.px2.self_play.opponent_selection import (
    OPPONENT_SELECTION_ROUND_ROBIN,
    OPPONENT_SELECTION_WEIGHTED_FROZEN_STUB,
)
from starlab.sc2.px2.self_play.run_artifacts import (
    default_operator_local_slice4_subdirs,
    write_json,
)
from starlab.sc2.px2.self_play.snapshot_pool import (
    DEFAULT_SLICE5_WEIGHTED_FROZEN_WEIGHTS,
    OpponentPoolStub,
    build_slice5_opponent_pool,
    opponent_battle_ref_ids,
    opponent_pool_identity_sha256,
    opponent_pool_to_json_dict,
)

DEFAULT_CAMPAIGN_ROOT_SUBDIRS: Final[tuple[str, ...]] = ("runs", "opponent_pool")


def recommended_operator_out_campaign_root_path(campaign_id: str) -> str:
    """Documentary path under ``out/`` (not committed); operators mirror under temp dirs in CI."""

    safe = campaign_id.strip() or "px2_campaign"
    return f"out/px2_self_play_campaigns/{safe}/"


def default_operator_local_campaign_root_subdirs() -> dict[str, str]:
    """Top-level directories under a PX2 operator-local campaign root."""

    return {"runs": "runs", "opponent_pool": "opponent_pool"}


def ensure_operator_local_campaign_root_layout(campaign_root: Path) -> dict[str, Path]:
    """Create ``runs/`` and ``opponent_pool/`` under ``campaign_root``."""

    out: dict[str, Path] = {}
    for key, rel in default_operator_local_campaign_root_subdirs().items():
        p = (campaign_root / rel).resolve()
        p.mkdir(parents=True, exist_ok=True)
        out[key] = p
    return out


def write_opponent_pool_metadata(opponent_pool_dir: Path, pool: OpponentPoolStub) -> dict[str, Any]:
    """Emit ``px2_opponent_pool_metadata.json`` with identity seal."""

    meta: dict[str, Any] = {
        "opponent_pool_metadata_version": "starlab.px2.opponent_pool_metadata.v1",
        "opponent_pool": opponent_pool_to_json_dict(pool),
        "opponent_pool_identity_sha256": opponent_pool_identity_sha256(pool),
        "non_claims": [
            "Slice-5 opponent-pool metadata — bookkeeping only; not industrial opponent roster.",
        ],
    }
    write_json(opponent_pool_dir / "px2_opponent_pool_metadata.json", meta)
    return meta


def run_slice5_operator_local_campaign(
    *,
    corpus_root: Path,
    campaign_root: Path,
    init_only: bool,
    weights_path: Path | None = None,
    weight_bundle_ref: str | None = None,
    campaign_id: str = "px2_m03_slice5_operator_local",
    campaign_profile_id: str = "px2_m03_slice5_campaign_root_v1",
    torch_seed: int = 42,
    run_id: str | None = None,
    continuity_step_count: int = 3,
    device_intent: str = "cpu",
    map_location: str = "cpu",
    opponent_selection_rule_id: str = OPPONENT_SELECTION_ROUND_ROBIN,
    opponent_selection_weights: tuple[int, ...] | None = None,
    pool: OpponentPoolStub | None = None,
    execution_kind: str = EXECUTION_KIND_SLICE5,
    write_campaign_root_manifest: bool = True,
) -> dict[str, Any]:
    """Bounded slice-5 path: layout, continuity under ``runs/<run_id>/``, sealed root manifest."""

    root = campaign_root.resolve()
    ensure_operator_local_campaign_root_layout(root)
    pool_use = (
        pool
        if pool is not None
        else build_slice5_opponent_pool(campaign_tag=campaign_id.replace("/", "_"))
    )
    battle_refs = opponent_battle_ref_ids(pool_use)
    weights_for_continuity: tuple[int, ...] | None = opponent_selection_weights
    if opponent_selection_rule_id == OPPONENT_SELECTION_WEIGHTED_FROZEN_STUB:
        w = weights_for_continuity or DEFAULT_SLICE5_WEIGHTED_FROZEN_WEIGHTS
        if len(w) != len(battle_refs):
            msg = "opponent_selection_weights must match battle ref count for weighted_frozen_stub"
            raise ValueError(msg)
        weights_for_continuity = w
    elif opponent_selection_weights is not None:
        msg = "opponent_selection_weights only valid for weighted_frozen_stub"
        raise ValueError(msg)

    opp_dir = root / default_operator_local_campaign_root_subdirs()["opponent_pool"]
    write_opponent_pool_metadata(opp_dir, pool_use)

    rid = run_id or f"px2_slice5_{uuid.uuid4().hex[:12]}"
    run_dir = root / "runs" / rid
    run_dir.mkdir(parents=True, exist_ok=True)

    cont = run_operator_local_campaign_continuity(
        corpus_root=corpus_root,
        output_dir=run_dir,
        init_only=init_only,
        weights_path=weights_path,
        weight_bundle_ref=weight_bundle_ref,
        campaign_id=campaign_id,
        campaign_profile_id=campaign_profile_id,
        torch_seed=torch_seed,
        run_id=rid,
        continuity_step_count=continuity_step_count,
        device_intent=device_intent,
        map_location=map_location,
        opponent_pool=pool_use,
        opponent_selection_rule_id=opponent_selection_rule_id,
        opponent_selection_weights=weights_for_continuity,
        opponent_rotation_ref_ids=battle_refs,
        execution_kind=execution_kind,
    )

    sub4 = default_operator_local_slice4_subdirs()
    root_non_claims = (
        [
            "Slice-6 canonical campaign-root smoke — not industrial self-play campaign.",
            "Bounded continuity; not Blackwell-scale; not merge-gate default CI proof.",
        ]
        if execution_kind == EXECUTION_KIND_SLICE6
        else [
            "Slice-7 bounded operator-local real run — not industrial self-play campaign.",
            "Real filesystem tree; minutes-scale; not merge-gate default CI proof.",
        ]
        if execution_kind == EXECUTION_KIND_SLICE7
        else [
            "Slice-8 bounded operator-local multi-run session — not industrial self-play campaign.",
            "Multiple bounded runs under one root; not Blackwell-scale; not merge-gate CI proof.",
        ]
        if execution_kind == EXECUTION_KIND_SLICE8
        else [
            "Slice-11 bounded continuation run consuming current-candidate pointer — "
            "not industrial self-play campaign.",
            "Candidate consumption bookkeeping; not PX2-M04 exploit closure; "
            "not merge-gate CI proof.",
        ]
        if execution_kind == EXECUTION_KIND_SLICE11
        else [
            "Slice-13 bounded second-hop continuation — post-slice-12 current-candidate pointer; "
            "not industrial self-play campaign.",
            "Repeatability; not PX2-M04 exploit closure; not merge-gate default CI proof.",
        ]
        if execution_kind == EXECUTION_KIND_SLICE13
        else [
            "Slice-14 bounded pointer-seeded run — declared seed from current-candidate JSON; "
            "not industrial self-play campaign.",
            "Not PX2-M04 exploit closure; not merge-gate default CI proof.",
        ]
        if execution_kind == EXECUTION_KIND_SLICE14
        else [
            "Slice-16 bounded handoff-anchored run — declared anchor from slice-15 handoff JSON; "
            "not industrial self-play campaign.",
            "Not PX2-M04 exploit closure; not merge-gate default CI proof.",
        ]
        if execution_kind == EXECUTION_KIND_SLICE16
        else [
            "Slice-5 operator-local campaign-root manifest — not industrial self-play campaign.",
            "Continuity runs are bounded; not Blackwell-scale; not merge-gate default CI proof.",
        ]
    )
    if write_campaign_root_manifest:
        manifest, report = build_px2_self_play_campaign_root_manifest_artifacts(
            campaign_id=campaign_id,
            campaign_contract_sha256=str(cont["campaign_sha256"]),
            root_path_expected=recommended_operator_out_campaign_root_path(campaign_id),
            allowed_subdirectories=DEFAULT_CAMPAIGN_ROOT_SUBDIRS,
            run_subdirectory_receipt_layout=dict(sub4),
            continuity_run_references=(
                {
                    "run_id": rid,
                    "continuity_sha256": str(cont["continuity_sha256"]),
                    "relative_path": f"runs/{rid}/",
                    "run_manifest_relative_path": f"runs/{rid}/run_manifest.json",
                },
            ),
            opponent_pool_identity_sha256=opponent_pool_identity_sha256(pool_use),
            opponent_selection_rule_id=opponent_selection_rule_id,
            non_claims=root_non_claims,
        )
        write_json(root / "px2_self_play_campaign_root_manifest.json", manifest)
        write_json(root / "px2_self_play_campaign_root_manifest_report.json", report)

    manifest_sha256_out: str | None = None
    if write_campaign_root_manifest:
        manifest_sha256_out = str(manifest["campaign_root_manifest_sha256"])

    return {
        "campaign_root": str(root),
        "run_id": rid,
        "continuity_sha256": cont["continuity_sha256"],
        "continuity_chain_sha256": cont["continuity_chain_sha256"],
        "preflight_sha256": cont["preflight_sha256"],
        "campaign_root_manifest_sha256": manifest_sha256_out,
        "campaign_contract_sha256": cont["campaign_sha256"],
        "opponent_pool_identity_sha256": opponent_pool_identity_sha256(pool_use),
    }
