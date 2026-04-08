"""Emit validated canonical state JSON + deterministic pipeline report (M16)."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from starlab.runs.json_util import canonical_json_dumps, sha256_hex_of_canonical_json
from starlab.state.canonical_state_derivation import derive_canonical_state_frame
from starlab.state.canonical_state_inputs import M14BundleInputs, load_m14_bundle
from starlab.state.canonical_state_models import (
    CANONICAL_STATE_ARTIFACT_FILENAME,
    CANONICAL_STATE_PIPELINE_CONTRACT,
    CANONICAL_STATE_PIPELINE_PROFILE,
    CANONICAL_STATE_PIPELINE_REPORT_FILENAME,
    CANONICAL_STATE_PIPELINE_REPORT_VERSION,
)
from starlab.state.canonical_state_schema import (
    build_canonical_state_json_schema,
    validate_canonical_state_frame,
)


def materialize_canonical_state(
    bundle: M14BundleInputs,
    *,
    target_gameloop: int,
) -> tuple[dict[str, Any], dict[str, Any], list[str]]:
    """Return ``(canonical_state, report, warnings)``."""

    frame, warnings = derive_canonical_state_frame(bundle, target_gameloop=target_gameloop)
    errs = validate_canonical_state_frame(frame)
    if errs:
        msg = "canonical state validation failed: " + "; ".join(errs)
        raise ValueError(msg)

    schema_obj = build_canonical_state_json_schema()
    schema_sha = sha256_hex_of_canonical_json(schema_obj)
    state_sha = sha256_hex_of_canonical_json(frame)

    manifest = bundle.manifest
    hashes = manifest.get("artifact_hashes")
    source_hashes: dict[str, str] = {}
    if isinstance(hashes, dict):
        for k in sorted(hashes.keys()):
            if isinstance(k, str):
                source_hashes[k] = str(hashes[k])

    report: dict[str, Any] = {
        "canonical_state_schema_sha256": schema_sha,
        "canonical_state_sha256": state_sha,
        "contract": CANONICAL_STATE_PIPELINE_CONTRACT,
        "derivation_summary": {
            "used_build_order_economy": True,
            "used_combat_scouting_visibility": True,
            "used_metadata": True,
            "used_replay_bundle_manifest": True,
            "used_replay_slices": True,
            "used_timeline": True,
        },
        "non_claims": [
            "Does not prove observation surface contract (M17) or perceptual bridge (M18).",
            "Does not prove replay↔execution equivalence, benchmark integrity, or live SC2 in CI.",
            (
                "Economy and visibility fields are conservative replay-derived summaries — "
                "not exact banks or fog-of-war truth."
            ),
        ],
        "profile": CANONICAL_STATE_PIPELINE_PROFILE,
        "report_version": CANONICAL_STATE_PIPELINE_REPORT_VERSION,
        "source_artifact_hashes": source_hashes,
        "source_bundle_id": manifest.get("bundle_id"),
        "source_lineage_root": manifest.get("lineage_root"),
        "target_gameloop": target_gameloop,
        "warnings": warnings,
    }
    return frame, report, warnings


def emit_canonical_state_artifacts(
    *,
    bundle_dir: Path,
    output_dir: Path,
    target_gameloop: int,
) -> tuple[Path, Path]:
    """Load bundle, materialize state, write ``canonical_state.json`` + report."""

    bundle, err = load_m14_bundle(bundle_dir)
    if bundle is None:
        msg = err or "failed to load M14 bundle"
        raise ValueError(msg)

    frame, report, _warnings = materialize_canonical_state(bundle, target_gameloop=target_gameloop)

    output_dir.mkdir(parents=True, exist_ok=True)
    sp = output_dir / CANONICAL_STATE_ARTIFACT_FILENAME
    rp = output_dir / CANONICAL_STATE_PIPELINE_REPORT_FILENAME
    sp.write_text(canonical_json_dumps(frame), encoding="utf-8")
    rp.write_text(canonical_json_dumps(report), encoding="utf-8")
    return sp, rp
