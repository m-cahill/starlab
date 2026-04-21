"""First bounded substantive operator-local execution (PX2-M03 post–slice-16, not a micro-slice)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Final

from starlab.sc2.px2.self_play.bounded_substantive_execution_record import (
    BOUNDED_SUBSTANTIVE_RULE_STUB,
    SUBSTANTIVE_LINEAGE_CAMPAIGN_ROOT_ONLY,
    SUBSTANTIVE_LINEAGE_OPTIONAL_BOTH,
    SUBSTANTIVE_LINEAGE_OPTIONAL_SLICE15_HANDOFF,
    SUBSTANTIVE_LINEAGE_OPTIONAL_SLICE16_ANCHORED,
    build_px2_self_play_bounded_substantive_execution_artifacts,
)
from starlab.sc2.px2.self_play.campaign_continuity import EXECUTION_KIND_BOUNDED_SUBSTANTIVE
from starlab.sc2.px2.self_play.campaign_root import run_slice5_operator_local_campaign
from starlab.sc2.px2.self_play.continuation_run import (
    merge_campaign_root_manifest_after_continuation_run,
)
from starlab.sc2.px2.self_play.handoff_anchored_run import ANCHORED_OK, HANDOFF_ANCHORED_RUN_JSON
from starlab.sc2.px2.self_play.opponent_selection import OPPONENT_SELECTION_ROUND_ROBIN
from starlab.sc2.px2.self_play.pointer_seeded_handoff import HANDOFF_OK, POINTER_SEEDED_HANDOFF_JSON
from starlab.sc2.px2.self_play.run_artifacts import write_json
from starlab.sc2.px2.self_play.weight_loading import WEIGHT_MODE_INIT_ONLY, WEIGHT_MODE_WEIGHTS_FILE

BOUNDED_SUBSTANTIVE_PROFILE_ID: Final[str] = (
    "px2_m03_bounded_substantive_operator_local_execution_v1"
)

BOUNDED_SUBSTANTIVE_EXECUTION_JSON: Final[str] = "px2_self_play_bounded_substantive_execution.json"

DEFAULT_BOUNDED_SUBSTANTIVE_CONTINUITY_STEPS: Final[int] = 15


def _collect_optional_substantive_lineage(root: Path) -> tuple[str, str, str]:
    """Return ``(mode, ho_sha, ha_sha)`` for optional slice-15/16 artifacts when present and OK."""

    ho_sha = ""
    ha_sha = ""
    ho_path = root / POINTER_SEEDED_HANDOFF_JSON
    ha_path = root / HANDOFF_ANCHORED_RUN_JSON
    if ho_path.is_file():
        try:
            ho = json.loads(ho_path.read_text(encoding="utf-8"))
            if str(ho.get("handoff_status", "")) == HANDOFF_OK:
                ho_sha = str(ho.get("pointer_seeded_handoff_sha256", ""))
        except (OSError, TypeError, ValueError, json.JSONDecodeError):
            ho_sha = ""
    if ha_path.is_file():
        try:
            ha = json.loads(ha_path.read_text(encoding="utf-8"))
            if str(ha.get("anchoring_status", "")) == ANCHORED_OK:
                ha_sha = str(ha.get("handoff_anchored_run_sha256", ""))
        except (OSError, TypeError, ValueError, json.JSONDecodeError):
            ha_sha = ""

    if ho_sha and ha_sha:
        return SUBSTANTIVE_LINEAGE_OPTIONAL_BOTH, ho_sha, ha_sha
    if ho_sha:
        return SUBSTANTIVE_LINEAGE_OPTIONAL_SLICE15_HANDOFF, ho_sha, ""
    if ha_sha:
        return SUBSTANTIVE_LINEAGE_OPTIONAL_SLICE16_ANCHORED, "", ha_sha
    return SUBSTANTIVE_LINEAGE_CAMPAIGN_ROOT_ONLY, "", ""


def run_bounded_substantive_operator_local_execution(
    *,
    corpus_root: Path,
    campaign_root: Path,
    campaign_id: str,
    substantive_run_id: str,
    init_only: bool = True,
    weights_path: Path | None = None,
    weight_bundle_ref: str | None = None,
    continuity_step_count: int = DEFAULT_BOUNDED_SUBSTANTIVE_CONTINUITY_STEPS,
    torch_seed: int = 103,
    device_intent: str = "cpu",
    map_location: str = "cpu",
) -> dict[str, Any]:
    """Bounded substantive continuity under campaign root; optional slice-15/16 lineage binding.

    **Not** industrial self-play; **not** **PX2-M04** exploit closure; **not** merge-gate CI.

    Real-weights mode requires ``weights_path``; otherwise raises ``ValueError``.
    """

    if not init_only and weights_path is None:
        msg = (
            "bounded substantive execution: real weights mode requires an explicit weights path "
            "(e.g. PX2-M02 bootstrap state_dict); refusing init_only=False without weights_path"
        )
        raise ValueError(msg)

    root = campaign_root.resolve()
    man_path = root / "px2_self_play_campaign_root_manifest.json"
    has_existing_manifest = man_path.is_file()

    wm = WEIGHT_MODE_INIT_ONLY if init_only else WEIGHT_MODE_WEIGHTS_FILE
    base_non_claims = [
        "Bounded substantive operator-local execution — post–slice-16; deeper continuity than "
        "2–3 step micro-runs; default 15 steps is a bounded default, not a scientific claim.",
        "Not industrial self-play; not Blackwell-scale; not ladder strength; not PX2-M04 exploit "
        "closure; not merge-gate default CI proof.",
        "Optional slice-15/16 artifacts bind only when present and status-OK; otherwise "
        "campaign-root-only lineage.",
    ]

    inner = run_slice5_operator_local_campaign(
        corpus_root=corpus_root,
        campaign_root=root,
        init_only=init_only,
        weights_path=weights_path,
        weight_bundle_ref=weight_bundle_ref,
        campaign_id=campaign_id,
        campaign_profile_id=BOUNDED_SUBSTANTIVE_PROFILE_ID,
        torch_seed=torch_seed,
        run_id=substantive_run_id,
        continuity_step_count=continuity_step_count,
        device_intent=device_intent,
        map_location=map_location,
        opponent_selection_rule_id=OPPONENT_SELECTION_ROUND_ROBIN,
        execution_kind=EXECUTION_KIND_BOUNDED_SUBSTANTIVE,
        write_campaign_root_manifest=not has_existing_manifest,
    )

    new_cont_sha = str(inner["continuity_sha256"])
    updated_man_sha = inner.get("campaign_root_manifest_sha256")

    if has_existing_manifest:
        man_before = json.loads(man_path.read_text(encoding="utf-8"))
        opp_rule = str(man_before.get("opponent_selection_rule_id", OPPONENT_SELECTION_ROUND_ROBIN))
        updated_sha, _, _ = merge_campaign_root_manifest_after_continuation_run(
            root,
            campaign_id=campaign_id,
            new_run_id=substantive_run_id,
            new_continuity_sha256=new_cont_sha,
            opponent_selection_rule_id=opp_rule,
            execution_kind=EXECUTION_KIND_BOUNDED_SUBSTANTIVE,
        )
        updated_man_sha = updated_sha

    cont_path = root / "runs" / substantive_run_id / "px2_self_play_campaign_continuity.json"
    cont = json.loads(cont_path.read_text(encoding="utf-8"))
    n_req = int(continuity_step_count)
    n_eff = int(cont.get("continuity_step_count", n_req))

    lin_mode, ho_s, ha_s = _collect_optional_substantive_lineage(root)

    tm, tr = build_px2_self_play_bounded_substantive_execution_artifacts(
        campaign_root_resolved=root,
        execution_kind=EXECUTION_KIND_BOUNDED_SUBSTANTIVE,
        campaign_id=campaign_id,
        campaign_profile_id=BOUNDED_SUBSTANTIVE_PROFILE_ID,
        bounded_substantive_rule_id=BOUNDED_SUBSTANTIVE_RULE_STUB,
        substantive_run_id=substantive_run_id,
        continuity_step_count_requested=n_req,
        continuity_step_count_effective=n_eff,
        resulting_continuity_sha256=new_cont_sha,
        updated_campaign_root_manifest_sha256=str(updated_man_sha or ""),
        weight_mode_declared=wm,
        substantive_lineage_mode=lin_mode,
        optional_pointer_seeded_handoff_sha256=ho_s,
        optional_handoff_anchored_run_sha256=ha_s,
        non_claims=base_non_claims,
    )
    write_json(root / BOUNDED_SUBSTANTIVE_EXECUTION_JSON, tm)
    write_json(root / "px2_self_play_bounded_substantive_execution_report.json", tr)

    return {
        "campaign_root": str(root),
        "bounded_substantive_execution_sha256": tm["bounded_substantive_execution_sha256"],
        "substantive_run_id": substantive_run_id,
        "continuity_step_count_requested": n_req,
        "continuity_step_count_effective": n_eff,
        "resulting_continuity_sha256": new_cont_sha,
        "updated_campaign_root_manifest_sha256": updated_man_sha,
        "weight_mode_declared": wm,
        "substantive_lineage_mode": lin_mode,
    }
