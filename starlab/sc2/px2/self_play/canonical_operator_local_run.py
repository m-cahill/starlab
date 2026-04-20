"""Canonical operator-local campaign-root smoke path (PX2-M03 slice 6).

Golden path: ``out/px2_self_play_campaigns/<campaign_id>/`` under a base directory
(typically the repo working directory for operators; temp dirs in CI tests).
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from starlab.sc2.px2.self_play.campaign_continuity import EXECUTION_KIND_SLICE6
from starlab.sc2.px2.self_play.campaign_root import run_slice5_operator_local_campaign


def resolve_canonical_campaign_root(campaign_id: str, *, base_dir: Path | None = None) -> Path:
    """Resolve ``<base>/out/px2_self_play_campaigns/<campaign_id>/`` (operator-local layout)."""

    base = Path.cwd() if base_dir is None else base_dir
    return (base.resolve() / "out" / "px2_self_play_campaigns" / campaign_id.strip()).resolve()


def run_canonical_operator_local_campaign_root_smoke(
    *,
    corpus_root: Path,
    campaign_id: str = "px2_m03_slice6_canonical_smoke",
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
    """Bounded golden-path smoke: slice-5 campaign-root tree + slice-6 execution kind.

    Writes under ``resolve_canonical_campaign_root(...)`` — use ``base_dir`` in tests
    (e.g. ``tmp_path``) so paths stay in temp trees.
    """

    root = resolve_canonical_campaign_root(campaign_id, base_dir=base_dir)
    return run_slice5_operator_local_campaign(
        corpus_root=corpus_root,
        campaign_root=root,
        init_only=init_only,
        weights_path=weights_path,
        weight_bundle_ref=weight_bundle_ref,
        campaign_id=campaign_id,
        campaign_profile_id="px2_m03_slice6_canonical_campaign_root_smoke_v1",
        torch_seed=torch_seed,
        run_id=run_id,
        continuity_step_count=continuity_step_count,
        device_intent=device_intent,
        map_location=map_location,
        execution_kind=EXECUTION_KIND_SLICE6,
    )
