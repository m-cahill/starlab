"""Governed bounded operator-local real-run execution record (PX2-M03 slice 7)."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Final

from starlab.runs.json_util import sha256_hex_of_canonical_json
from starlab.sc2.px2.self_play.campaign_continuity import EXECUTION_KIND_SLICE7
from starlab.sc2.px2.self_play.campaign_root import recommended_operator_out_campaign_root_path

PX2_SELF_PLAY_OPERATOR_LOCAL_REAL_RUN_CONTRACT_ID: Final[str] = (
    "starlab.px2.self_play_operator_local_real_run.v1"
)
PX2_SELF_PLAY_OPERATOR_LOCAL_REAL_RUN_REPORT_CONTRACT_ID: Final[str] = (
    "starlab.px2.self_play_operator_local_real_run_report.v1"
)
OPERATOR_LOCAL_REAL_RUN_RECORD_VERSION: Final[str] = "px2_m03_slice7_real_run_record_v1"


def _seal_real_run_body(body_without_seal: dict[str, Any]) -> str:
    return sha256_hex_of_canonical_json(body_without_seal)


def build_operator_local_real_run_seal_basis(
    *,
    campaign_id: str,
    campaign_profile_id: str,
    run_id: str,
    torch_seed: int,
    continuity_step_count: int,
    campaign_contract_sha256: str,
    preflight_sha256: str,
    continuity_sha256: str,
    continuity_chain_sha256: str,
    campaign_root_manifest_sha256: str | None,
    opponent_pool_identity_sha256: str,
    weight_mode: str,
    weights_file_sha256: str | None,
    weights_path_basename: str | None,
    non_claims: list[str],
    execution_kind: str = EXECUTION_KIND_SLICE7,
) -> dict[str, Any]:
    """Identity hashed as ``operator_local_real_run_sha256`` (no absolute filesystem paths)."""

    return {
        "contract_id": PX2_SELF_PLAY_OPERATOR_LOCAL_REAL_RUN_CONTRACT_ID,
        "operator_local_real_run_record_version": OPERATOR_LOCAL_REAL_RUN_RECORD_VERSION,
        "execution_kind": execution_kind,
        "campaign_id": campaign_id,
        "campaign_profile_id": campaign_profile_id,
        "run_id": run_id,
        "torch_seed": torch_seed,
        "continuity_step_count": continuity_step_count,
        "recommended_campaign_root_logical": recommended_operator_out_campaign_root_path(
            campaign_id
        ),
        "campaign_contract_sha256": campaign_contract_sha256,
        "preflight_sha256": preflight_sha256,
        "continuity_sha256": continuity_sha256,
        "continuity_chain_sha256": continuity_chain_sha256,
        "campaign_root_manifest_sha256": campaign_root_manifest_sha256 or "",
        "opponent_pool_identity_sha256": opponent_pool_identity_sha256,
        "weight_mode": weight_mode,
        "weights_file_sha256": weights_file_sha256,
        "weights_path_basename": weights_path_basename,
        "non_claims": non_claims,
    }


def build_px2_self_play_operator_local_real_run_artifacts(
    *,
    campaign_id: str,
    campaign_profile_id: str,
    run_id: str,
    torch_seed: int,
    continuity_step_count: int,
    campaign_root_resolved: Path,
    campaign_contract_sha256: str,
    preflight_sha256: str,
    continuity_sha256: str,
    continuity_chain_sha256: str,
    campaign_root_manifest_sha256: str,
    opponent_pool_identity_sha256: str,
    weight_identity: dict[str, Any],
    non_claims: list[str],
    execution_kind: str = EXECUTION_KIND_SLICE7,
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Return real_run JSON + report with sealed ``operator_local_real_run_sha256``."""

    wpath = weight_identity.get("weights_path_note")
    basename = Path(str(wpath)).name if isinstance(wpath, str) and wpath else None
    wm = str(weight_identity.get("weight_mode", ""))
    wsha = weight_identity.get("weights_file_sha256")

    basis = build_operator_local_real_run_seal_basis(
        campaign_id=campaign_id,
        campaign_profile_id=campaign_profile_id,
        run_id=run_id,
        torch_seed=torch_seed,
        continuity_step_count=continuity_step_count,
        campaign_contract_sha256=campaign_contract_sha256,
        preflight_sha256=preflight_sha256,
        continuity_sha256=continuity_sha256,
        continuity_chain_sha256=continuity_chain_sha256,
        campaign_root_manifest_sha256=campaign_root_manifest_sha256,
        opponent_pool_identity_sha256=opponent_pool_identity_sha256,
        weight_mode=wm,
        weights_file_sha256=wsha if isinstance(wsha, str) else None,
        weights_path_basename=basename,
        non_claims=non_claims,
        execution_kind=execution_kind,
    )
    seal = _seal_real_run_body(basis)
    root_posix = campaign_root_resolved.resolve().as_posix()

    manifest: dict[str, Any] = {
        **basis,
        "operator_local_real_run_sha256": seal,
        "weight_identity": weight_identity,
        "operator_note_convention": (
            "Optional human note (not sealed): "
            f"``{recommended_operator_out_campaign_root_path(campaign_id)}"
            "px2_operator_local_real_run_operator_note.md``"
        ),
    }
    manifest["campaign_root_resolved_posix"] = root_posix

    report: dict[str, Any] = {
        "contract_id": PX2_SELF_PLAY_OPERATOR_LOCAL_REAL_RUN_REPORT_CONTRACT_ID,
        "operator_local_real_run_sha256": seal,
        "campaign_id": campaign_id,
        "run_id": run_id,
        "summary": {
            "record_ok": True,
            "continuity_step_count": continuity_step_count,
        },
        "operator_absolute_paths_advisory": {
            "campaign_root": root_posix,
            "relative_run_path": f"runs/{run_id}/",
        },
        "non_claims": non_claims,
    }
    return manifest, report
