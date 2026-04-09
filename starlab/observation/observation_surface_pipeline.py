"""Emit validated observation_surface.json + materialization report (M18)."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from starlab.observation.observation_surface_derivation import derive_observation_surface_frame
from starlab.observation.observation_surface_inputs import (
    canonical_state_sha256,
    load_canonical_state,
    load_canonical_state_report,
    provenance_report_matches_state,
)
from starlab.observation.observation_surface_models import (
    OBSERVATION_MATERIALIZATION_REPORT_VERSION,
    OBSERVATION_SURFACE_ARTIFACT_FILENAME,
    OBSERVATION_SURFACE_MATERIALIZATION_REPORT_FILENAME,
    PERCEPTUAL_BRIDGE_PROTOTYPE_CONTRACT,
    PERCEPTUAL_BRIDGE_PROTOTYPE_PROFILE,
)
from starlab.observation.observation_surface_schema import validate_observation_surface_frame
from starlab.runs.json_util import canonical_json_dumps, sha256_hex_of_canonical_json


def materialize_observation_surface(
    *,
    canonical_state: dict[str, Any],
    perspective_player_index: int,
    canonical_state_report: dict[str, Any] | None = None,
) -> tuple[dict[str, Any], dict[str, Any], list[str]]:
    """Return ``(observation, materialization_report, warnings)``."""

    state_sha = canonical_state_sha256(canonical_state)
    if canonical_state_report is not None:
        err = provenance_report_matches_state(state=canonical_state, report=canonical_state_report)
        if err:
            raise ValueError(err)

    frame, warn = derive_observation_surface_frame(
        canonical_state,
        perspective_player_index=perspective_player_index,
        source_canonical_state_sha256=state_sha,
    )

    report_warnings = list(warn)
    if canonical_state_report is not None:
        rw = canonical_state_report.get("warnings")
        if isinstance(rw, list):
            for w in rw:
                if isinstance(w, str):
                    report_warnings.append(f"upstream canonical_state_report: {w}")

    errs = validate_observation_surface_frame(frame)
    if errs:
        msg = "observation surface validation failed: " + "; ".join(errs)
        raise ValueError(msg)

    obs_sha = sha256_hex_of_canonical_json(frame)

    crosscheck: dict[str, Any] = {
        "canonical_state_report_supplied": canonical_state_report is not None,
        # If a report was supplied, provenance already matched or we would have raised.
        "canonical_state_report_hash_match": canonical_state_report is not None,
    }

    materialization_report: dict[str, Any] = {
        "action_mask_posture": (
            "prototype_heuristic_family_masks — not legality, not full SC2 action coverage."
        ),
        "contract": PERCEPTUAL_BRIDGE_PROTOTYPE_CONTRACT,
        "gameloop": frame["metadata"]["gameloop"],
        "non_claims": [
            "Prototype materialization only — not benchmark integrity or agent capability.",
            "Action masks are coarse heuristics from M16 summaries — not legality computation.",
            (
                "Spatial planes are structural shape metadata only — not replay/map-grounded "
                "positional truth."
            ),
            "Visibility remains proxy-bounded — not certified fog-of-war truth.",
            "Does not prove replay↔execution equivalence or live SC2 in CI.",
        ],
        "observation_surface_sha256": obs_sha,
        "perspective_player_index": perspective_player_index,
        "profile": PERCEPTUAL_BRIDGE_PROTOTYPE_PROFILE,
        "provenance_crosscheck": crosscheck,
        "report_version": OBSERVATION_MATERIALIZATION_REPORT_VERSION,
        "source_canonical_state_sha256": state_sha,
        "spatial_plane_posture": (
            "prototype_structural_only — placeholder plane family; no M09 map binding."
        ),
        "warnings": sorted(set(report_warnings)),
    }

    return frame, materialization_report, report_warnings


def emit_observation_surface_artifacts(
    *,
    canonical_state_path: Path,
    output_dir: Path,
    perspective_player_index: int,
    canonical_state_report_path: Path | None = None,
) -> tuple[Path, Path]:
    """Load state, materialize, write ``observation_surface.json`` + report."""

    state, err = load_canonical_state(canonical_state_path)
    if state is None:
        msg = err or "failed to load canonical state"
        raise ValueError(msg)

    report_obj: dict[str, Any] | None = None
    if canonical_state_report_path is not None:
        report_obj, rerr = load_canonical_state_report(canonical_state_report_path)
        if report_obj is None:
            msg = rerr or "failed to load canonical state report"
            raise ValueError(msg)

    frame, mat_report, _warnings = materialize_observation_surface(
        canonical_state=state,
        perspective_player_index=perspective_player_index,
        canonical_state_report=report_obj,
    )

    output_dir.mkdir(parents=True, exist_ok=True)
    op = output_dir / OBSERVATION_SURFACE_ARTIFACT_FILENAME
    rp = output_dir / OBSERVATION_SURFACE_MATERIALIZATION_REPORT_FILENAME
    op.write_text(canonical_json_dumps(frame), encoding="utf-8")
    rp.write_text(canonical_json_dumps(mat_report), encoding="utf-8")
    return op, rp
