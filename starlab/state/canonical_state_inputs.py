"""Load and verify M14 replay bundle JSON for canonical state materialization (M16)."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from starlab._io import load_json_object
from starlab.replays.replay_bundle_generation import (
    compute_bundle_id,
    compute_lineage_root,
    verify_replay_plane_lineage,
)
from starlab.replays.replay_bundle_models import (
    PRIMARY_ARTIFACT_FILENAMES,
    SECONDARY_REPORT_FILENAMES,
)
from starlab.runs.json_util import sha256_hex_of_canonical_json


@dataclass(frozen=True)
class M14BundleInputs:
    """Governed M14 bundle members required for M16 (hashes verified at load)."""

    bundle_dir: Path
    manifest: dict[str, Any]
    lineage: dict[str, Any]
    contents: dict[str, Any]
    replay_metadata: dict[str, Any]
    replay_timeline: dict[str, Any]
    replay_build_order_economy: dict[str, Any]
    replay_combat_scouting_visibility: dict[str, Any]
    replay_slices: dict[str, Any]
    secondary_reports: dict[str, dict[str, Any]]


def _require_same_bundle_id(
    *,
    manifest: dict[str, Any],
    lineage: dict[str, Any],
    contents: dict[str, Any],
) -> str | None:
    mid = manifest.get("bundle_id")
    lid = lineage.get("bundle_id")
    cid = contents.get("bundle_id")
    if not isinstance(mid, str) or not mid:
        return "replay_bundle_manifest.json: missing or invalid bundle_id"
    if mid != lid:
        return "bundle_id mismatch: manifest vs replay_bundle_lineage.json"
    if mid != cid:
        return "bundle_id mismatch: manifest vs replay_bundle_contents.json"
    return None


def load_m14_bundle(bundle_dir: Path) -> tuple[M14BundleInputs | None, str | None]:
    """Load M14 bundle JSON from ``bundle_dir``; verify hashes and lineage closure."""

    bundle_dir = bundle_dir.resolve()
    mp = bundle_dir / "replay_bundle_manifest.json"
    lp = bundle_dir / "replay_bundle_lineage.json"
    cp = bundle_dir / "replay_bundle_contents.json"

    manifest, merr = load_json_object(mp)
    if manifest is None:
        return None, f"replay_bundle_manifest.json: {merr}"
    lineage, lerr = load_json_object(lp)
    if lineage is None:
        return None, f"replay_bundle_lineage.json: {lerr}"
    contents, cerr = load_json_object(cp)
    if contents is None:
        return None, f"replay_bundle_contents.json: {cerr}"

    err = _require_same_bundle_id(manifest=manifest, lineage=lineage, contents=contents)
    if err:
        return None, err

    hashes = manifest.get("artifact_hashes")
    if not isinstance(hashes, dict):
        return None, "replay_bundle_manifest.json: artifact_hashes must be an object"

    loaded: dict[str, dict[str, Any]] = {}
    for fname in sorted(hashes.keys()):
        if not isinstance(fname, str) or not fname:
            return None, "replay_bundle_manifest.json: invalid artifact_hashes key"
        expected = hashes[fname]
        if not isinstance(expected, str) or len(expected) != 64:
            return None, f"replay_bundle_manifest.json: bad hash for {fname}"
        p = bundle_dir / fname
        obj, rerr = load_json_object(p)
        if obj is None:
            return None, f"{fname}: {rerr}"
        got = sha256_hex_of_canonical_json(obj)
        if got.lower() != expected.lower():
            m = expected[:16]
            g = got[:16]
            return None, f"artifact hash mismatch for {fname}: manifest={m}… file={g}…"

        loaded[fname] = obj

    for name in PRIMARY_ARTIFACT_FILENAMES:
        if name not in loaded:
            return None, f"missing primary governed artifact after load: {name}"

    primary_objects = {n: loaded[n] for n in PRIMARY_ARTIFACT_FILENAMES}
    secondary_reports: dict[str, dict[str, Any]] = {}
    for name in SECONDARY_REPORT_FILENAMES:
        if name in loaded:
            secondary_reports[name] = loaded[name]

    timeline_report = secondary_reports.get("replay_timeline_report.json")
    boe_report = secondary_reports.get("replay_build_order_economy_report.json")
    csv_report = secondary_reports.get("replay_combat_scouting_visibility_report.json")
    metadata_report = secondary_reports.get("replay_metadata_report.json")

    lineage_err = verify_replay_plane_lineage(
        build_order_economy=primary_objects["replay_build_order_economy.json"],
        build_order_economy_report=boe_report,
        combat_scouting_visibility=primary_objects["replay_combat_scouting_visibility.json"],
        combat_scouting_visibility_report=csv_report,
        metadata=primary_objects["replay_metadata.json"],
        metadata_report=metadata_report,
        replay_slices=primary_objects["replay_slices.json"],
        timeline=primary_objects["replay_timeline.json"],
        timeline_report=timeline_report,
    )
    if lineage_err is not None:
        return None, f"replay plane lineage verification failed: {lineage_err}"

    primary_hashes = {
        n: sha256_hex_of_canonical_json(primary_objects[n]) for n in PRIMARY_ARTIFACT_FILENAMES
    }
    lr_computed = compute_lineage_root(primary_hashes=primary_hashes)
    lr_manifest = manifest.get("lineage_root")
    if not isinstance(lr_manifest, str) or not lr_manifest:
        return None, "replay_bundle_manifest.json: missing lineage_root"
    if lr_computed.lower() != lr_manifest.lower():
        return None, "lineage_root mismatch: recomputed from primary artifacts vs manifest"

    gen_params = manifest.get("generation_parameters")
    if not isinstance(gen_params, dict):
        return None, "replay_bundle_manifest.json: generation_parameters must be an object"
    bid_computed = compute_bundle_id(lineage_root=lr_computed, generation_parameters=gen_params)
    bid_manifest = manifest.get("bundle_id")
    if not isinstance(bid_manifest, str) or bid_computed.lower() != bid_manifest.lower():
        return (
            None,
            "bundle_id mismatch: recomputed from lineage_root + generation_parameters vs manifest",
        )

    # Optional: ensure contents lists align with manifest (soft check)
    prim_list = manifest.get("primary_artifacts")
    prim_strs = [str(x) for x in prim_list] if isinstance(prim_list, list) else []
    expected_order = list(PRIMARY_ARTIFACT_FILENAMES)
    if isinstance(prim_list, list) and prim_strs != expected_order:
        # Order may differ; require same set
        if set(prim_strs) != set(PRIMARY_ARTIFACT_FILENAMES):
            return (
                None,
                "replay_bundle_manifest.json: primary_artifacts does not match M14 primaries",
            )

    return (
        M14BundleInputs(
            bundle_dir=bundle_dir,
            contents=contents,
            lineage=lineage,
            manifest=manifest,
            replay_build_order_economy=primary_objects["replay_build_order_economy.json"],
            replay_combat_scouting_visibility=primary_objects[
                "replay_combat_scouting_visibility.json"
            ],
            replay_metadata=primary_objects["replay_metadata.json"],
            replay_slices=primary_objects["replay_slices.json"],
            replay_timeline=primary_objects["replay_timeline.json"],
            secondary_reports=secondary_reports,
        ),
        None,
    )
