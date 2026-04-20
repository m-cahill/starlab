"""Bounded operator-local multi-run session wrapper (PX2-M03 slice 8).

Runs two or more tiny bounded continuity passes under one campaign root, then seals a
session record plus a single campaign-root manifest listing every run.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Final

from starlab.sc2.px2.self_play.campaign_continuity import EXECUTION_KIND_SLICE8
from starlab.sc2.px2.self_play.campaign_root import (
    recommended_operator_out_campaign_root_path,
    run_slice5_operator_local_campaign,
)
from starlab.sc2.px2.self_play.campaign_root_manifest import (
    build_px2_self_play_campaign_root_manifest_artifacts,
)
from starlab.sc2.px2.self_play.canonical_operator_local_run import resolve_canonical_campaign_root
from starlab.sc2.px2.self_play.operator_local_real_run_record import (
    build_px2_self_play_operator_local_real_run_artifacts,
)
from starlab.sc2.px2.self_play.operator_local_session_record import (
    build_px2_self_play_operator_local_session_artifacts,
)
from starlab.sc2.px2.self_play.opponent_selection import OPPONENT_SELECTION_ROUND_ROBIN
from starlab.sc2.px2.self_play.run_artifacts import (
    default_operator_local_slice4_subdirs,
    write_json,
)
from starlab.sc2.px2.self_play.weight_loading import WEIGHT_MODE_INIT_ONLY, WEIGHT_MODE_WEIGHTS_FILE

DEFAULT_SLICE8_CAMPAIGN_ID: Final[str] = "px2_m03_slice8_bounded_session"
SLICE8_CAMPAIGN_PROFILE_ID: Final[str] = "px2_m03_slice8_bounded_operator_local_session_v1"


def run_bounded_operator_local_session(
    *,
    corpus_root: Path,
    campaign_id: str = DEFAULT_SLICE8_CAMPAIGN_ID,
    base_dir: Path | None = None,
    init_only: bool = True,
    weights_path: Path | None = None,
    weight_bundle_ref: str | None = None,
    run_ids: list[str] | None = None,
    run_count: int = 2,
    torch_seed: int = 42,
    run_torch_seeds: list[int] | None = None,
    continuity_step_count: int = 2,
    device_intent: str = "cpu",
    map_location: str = "cpu",
) -> dict[str, Any]:
    """Two or more bounded runs under one operator-local campaign root + session record.

    **Not** industrial self-play; **not** merge-gate default CI proof.
    """

    n = max(2, int(run_count))
    rids: tuple[str, ...]
    if run_ids is not None:
        if len(run_ids) < 2:
            msg = "operator-local session requires at least two distinct run_ids"
            raise ValueError(msg)
        rids = tuple(run_ids)
    else:
        rids = tuple(f"px2_sess_run_{i:02d}" for i in range(n))

    seeds = run_torch_seeds if run_torch_seeds is not None else [torch_seed] * len(rids)
    if len(seeds) != len(rids):
        msg = "run_torch_seeds length must match run_ids length"
        raise ValueError(msg)

    root = resolve_canonical_campaign_root(campaign_id, base_dir=base_dir)
    inners: list[dict[str, Any]] = []
    for i, rid in enumerate(rids):
        inner = run_slice5_operator_local_campaign(
            corpus_root=corpus_root,
            campaign_root=root,
            init_only=init_only,
            weights_path=weights_path,
            weight_bundle_ref=weight_bundle_ref,
            campaign_id=campaign_id,
            campaign_profile_id=SLICE8_CAMPAIGN_PROFILE_ID,
            torch_seed=seeds[i],
            run_id=rid,
            continuity_step_count=continuity_step_count,
            device_intent=device_intent,
            map_location=map_location,
            execution_kind=EXECUTION_KIND_SLICE8,
            write_campaign_root_manifest=False,
        )
        inners.append(inner)

    campaign_contract_sha256 = str(inners[0]["campaign_contract_sha256"])
    opp_sha = str(inners[0]["opponent_pool_identity_sha256"])
    sub4 = default_operator_local_slice4_subdirs()
    refs: list[dict[str, str]] = []
    for inn in inners:
        rid = str(inn["run_id"])
        refs.append(
            {
                "run_id": rid,
                "continuity_sha256": str(inn["continuity_sha256"]),
                "relative_path": f"runs/{rid}/",
                "run_manifest_relative_path": f"runs/{rid}/run_manifest.json",
            },
        )

    root_non_claims = [
        "Slice-8 bounded operator-local multi-run session — not industrial self-play campaign.",
        "Multiple bounded runs under one root; not Blackwell-scale; not merge-gate CI proof.",
    ]
    manifest, root_report = build_px2_self_play_campaign_root_manifest_artifacts(
        campaign_id=campaign_id,
        campaign_contract_sha256=campaign_contract_sha256,
        root_path_expected=recommended_operator_out_campaign_root_path(campaign_id),
        allowed_subdirectories=("runs", "opponent_pool"),
        run_subdirectory_receipt_layout=dict(sub4),
        continuity_run_references=tuple(refs),
        opponent_pool_identity_sha256=opp_sha,
        opponent_selection_rule_id=OPPONENT_SELECTION_ROUND_ROBIN,
        non_claims=root_non_claims,
    )
    write_json(root / "px2_self_play_campaign_root_manifest.json", manifest)
    write_json(root / "px2_self_play_campaign_root_manifest_report.json", root_report)
    man_sha = str(manifest["campaign_root_manifest_sha256"])

    per_run_tuples: list[dict[str, str]] = []
    per_run_seals: list[str] = []
    for inn in inners:
        rid = str(inn["run_id"])
        run_dir = root / "runs" / rid
        cont_path = run_dir / "px2_self_play_campaign_continuity.json"
        cont_body = json.loads(cont_path.read_text(encoding="utf-8"))
        weight_identity = cont_body.get("weight_identity")
        if not isinstance(weight_identity, dict):
            msg = "continuity JSON missing weight_identity"
            raise RuntimeError(msg)
        rr_non_claims = [
            "Slice-8 session member real-run row — not industrial self-play campaign.",
            "Seal covers logical seal-basis fields only.",
        ]
        rr_m, rr_rep = build_px2_self_play_operator_local_real_run_artifacts(
            campaign_id=campaign_id,
            campaign_profile_id=SLICE8_CAMPAIGN_PROFILE_ID,
            run_id=rid,
            torch_seed=int(cont_body["torch_seed"]),
            continuity_step_count=int(cont_body["continuity_step_count"]),
            campaign_root_resolved=root,
            campaign_contract_sha256=campaign_contract_sha256,
            preflight_sha256=str(inn["preflight_sha256"]),
            continuity_sha256=str(inn["continuity_sha256"]),
            continuity_chain_sha256=str(inn["continuity_chain_sha256"]),
            campaign_root_manifest_sha256=man_sha,
            opponent_pool_identity_sha256=opp_sha,
            weight_identity=weight_identity,
            non_claims=rr_non_claims,
            execution_kind=EXECUTION_KIND_SLICE8,
        )
        write_json(run_dir / "px2_self_play_operator_local_real_run.json", rr_m)
        write_json(run_dir / "px2_self_play_operator_local_real_run_report.json", rr_rep)
        seal = str(rr_m["operator_local_real_run_sha256"])
        per_run_seals.append(seal)
        per_run_tuples.append(
            {
                "run_id": rid,
                "operator_local_real_run_sha256": seal,
                "continuity_sha256": str(inn["continuity_sha256"]),
                "continuity_chain_sha256": str(inn["continuity_chain_sha256"]),
                "preflight_sha256": str(inn["preflight_sha256"]),
                "relative_run_path": f"runs/{rid}/",
                "operator_local_real_run_relative_path": (
                    f"runs/{rid}/px2_self_play_operator_local_real_run.json"
                ),
            },
        )

    session_non_claims = [
        "Slice-8 bounded operator-local multi-run session — not industrial self-play.",
        "Ordered bookkeeping only; not Blackwell-scale; not ladder strength.",
        "Not merge-gate default CI proof.",
    ]
    sess_m, sess_rep = build_px2_self_play_operator_local_session_artifacts(
        campaign_id=campaign_id,
        campaign_profile_id=SLICE8_CAMPAIGN_PROFILE_ID,
        campaign_root_resolved=root,
        campaign_contract_sha256=campaign_contract_sha256,
        opponent_pool_identity_sha256=opp_sha,
        campaign_root_manifest_sha256=man_sha,
        ordered_run_ids=rids,
        per_run=tuple(per_run_tuples),
        non_claims=session_non_claims,
    )
    write_json(root / "px2_self_play_operator_local_session.json", sess_m)
    write_json(root / "px2_self_play_operator_local_session_report.json", sess_rep)

    return {
        "campaign_root": str(root),
        "ordered_run_ids": list(rids),
        "campaign_root_manifest_sha256": man_sha,
        "operator_local_session_sha256": sess_m["operator_local_session_sha256"],
        "per_run_operator_local_real_run_sha256": per_run_seals,
        "campaign_contract_sha256": campaign_contract_sha256,
        "opponent_pool_identity_sha256": opp_sha,
        "weight_mode_declared": (WEIGHT_MODE_INIT_ONLY if init_only else WEIGHT_MODE_WEIGHTS_FILE),
    }
