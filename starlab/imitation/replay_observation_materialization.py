"""Governed in-process path: M14 bundle → M16 canonical state → M18 observation (M27 seam).

This module is intentionally small so later milestones (e.g. M28) can reuse the same
materialization surface without rethreading the full imitation baseline pipeline.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from starlab.observation.observation_surface_pipeline import materialize_observation_surface
from starlab.state.canonical_state_inputs import load_m14_bundle
from starlab.state.canonical_state_pipeline import materialize_canonical_state


def materialize_observation_for_observation_request(
    *,
    bundle_dir: Path,
    observation_request: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], list[str]]:
    """Load M14 bundle, emit canonical state + observation for one governed request.

    ``observation_request`` must contain ``bundle_id``, ``lineage_root``, ``gameloop``,
    and ``perspective_player_index`` (M26 dataset shape).

    Returns ``(canonical_state, observation_frame, canonical_state_report, warnings)``.
    """

    bid = observation_request.get("bundle_id")
    lr = observation_request.get("lineage_root")
    gl = observation_request.get("gameloop")
    ppi = observation_request.get("perspective_player_index")

    if not isinstance(bid, str) or not bid:
        msg = "observation_request.bundle_id must be a non-empty string"
        raise ValueError(msg)
    if not isinstance(lr, str) or not lr:
        msg = "observation_request.lineage_root must be a non-empty string"
        raise ValueError(msg)
    if not isinstance(gl, int) or isinstance(gl, bool):
        msg = "observation_request.gameloop must be an integer"
        raise ValueError(msg)
    if not isinstance(ppi, int) or isinstance(ppi, bool) or ppi < 0:
        msg = "observation_request.perspective_player_index must be a non-negative integer"
        raise ValueError(msg)

    bundle, err = load_m14_bundle(bundle_dir)
    if bundle is None:
        msg = err or "failed to load M14 bundle"
        raise ValueError(msg)

    manifest = bundle.manifest
    mbid = manifest.get("bundle_id")
    mlr = manifest.get("lineage_root")
    if not isinstance(mbid, str) or mbid != bid:
        msg = f"bundle_id mismatch: dataset {bid!r} vs bundle manifest {mbid!r}"
        raise ValueError(msg)
    if not isinstance(mlr, str) or mlr != lr:
        msg = f"lineage_root mismatch: dataset {lr!r} vs bundle manifest {mlr!r}"
        raise ValueError(msg)

    canonical_state, canonical_state_report, csw = materialize_canonical_state(
        bundle,
        target_gameloop=gl,
    )
    obs_frame, _mat_report, osw = materialize_observation_surface(
        canonical_state=canonical_state,
        perspective_player_index=ppi,
        canonical_state_report=canonical_state_report,
    )
    warnings = sorted({*csw, *osw})
    return canonical_state, obs_frame, canonical_state_report, warnings


def resolve_bundle_directory(
    *,
    bundle_id: str,
    bundle_dirs: list[Path],
) -> Path:
    """Return the bundle directory whose manifest ``bundle_id`` matches."""

    for d in sorted(bundle_dirs, key=lambda p: str(p.resolve())):
        bundle, err = load_m14_bundle(d)
        if bundle is None:
            msg = err or f"failed to load bundle {d}"
            raise ValueError(msg)
        mid = bundle.manifest.get("bundle_id")
        if isinstance(mid, str) and mid == bundle_id:
            return d.resolve()

    msg = f"no --bundle directory resolves bundle_id {bundle_id!r}"
    raise ValueError(msg)
