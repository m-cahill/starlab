"""Deterministic replay bundle manifest, lineage, and contents (M14)."""

from __future__ import annotations

from typing import Any, Literal

from starlab.replays.replay_bundle_catalog import (
    PRIMARY_NODE_INFO,
    SECONDARY_REPORT_NODE_INFO,
    bundle_node_id,
    bundle_node_label,
    determinism_notes_v1,
    exclusions_policy_v1,
    included_milestones_primary,
    node_record,
    optional_contextual_ancestry_note,
)
from starlab.replays.replay_bundle_models import (
    PRIMARY_ARTIFACT_FILENAMES,
    REPLAY_BUNDLE_CONTENTS_SCHEMA_VERSION,
    REPLAY_BUNDLE_CONTRACT_VERSION,
    REPLAY_BUNDLE_LINEAGE_SCHEMA_VERSION,
    REPLAY_BUNDLE_MANIFEST_SCHEMA_VERSION,
    REPLAY_BUNDLE_PROFILE,
)
from starlab.runs.json_util import sha256_hex_of_canonical_json

RunStatus = Literal["completed", "lineage_failed", "load_failed"]


def _hex_eq(a: str, b: str) -> bool:
    return a.lower() == b.lower()


def _lineage_report_mismatch_error(
    *,
    embedded: Any,
    computed_sha: str | None,
    label: str,
) -> str | None:
    if embedded is None:
        return None
    if not isinstance(embedded, str) or not embedded:
        return None
    if computed_sha is None:
        return f"{label} required when upstream embeds non-null report hash"
    if not _hex_eq(embedded, computed_sha):
        return f"{label} hash mismatch vs loaded report JSON"
    return None


def _validate_slices_optional_report_hashes(
    *,
    replay_slices: dict[str, Any],
    timeline_report: dict[str, Any] | None,
    build_order_economy_report: dict[str, Any] | None,
    combat_scouting_visibility_report: dict[str, Any] | None,
    metadata: dict[str, Any] | None,
    metadata_report: dict[str, Any] | None,
) -> str | None:
    """If ``replay_slices.json`` embeds optional report hashes, require matching files."""

    tr_sha = sha256_hex_of_canonical_json(timeline_report) if timeline_report is not None else None
    boe_rep_sha = (
        sha256_hex_of_canonical_json(build_order_economy_report)
        if build_order_economy_report is not None
        else None
    )
    csv_rep_sha = (
        sha256_hex_of_canonical_json(combat_scouting_visibility_report)
        if combat_scouting_visibility_report is not None
        else None
    )
    meta_sha = sha256_hex_of_canonical_json(metadata) if metadata is not None else None
    meta_rep_sha = (
        sha256_hex_of_canonical_json(metadata_report) if metadata_report is not None else None
    )

    err = _lineage_report_mismatch_error(
        computed_sha=tr_sha,
        embedded=replay_slices.get("optional_source_timeline_report_sha256"),
        label="replay_timeline_report.json (slices optional_source_timeline_report_sha256)",
    )
    if err:
        return err
    err = _lineage_report_mismatch_error(
        computed_sha=boe_rep_sha,
        embedded=replay_slices.get("optional_source_build_order_economy_report_sha256"),
        label=(
            "replay_build_order_economy_report.json "
            "(slices optional_source_build_order_economy_report_sha256)"
        ),
    )
    if err:
        return err
    err = _lineage_report_mismatch_error(
        computed_sha=csv_rep_sha,
        embedded=replay_slices.get("optional_source_combat_scouting_visibility_report_sha256"),
        label=(
            "replay_combat_scouting_visibility_report.json "
            "(slices optional_source_combat_scouting_visibility_report_sha256)"
        ),
    )
    if err:
        return err
    err = _lineage_report_mismatch_error(
        computed_sha=meta_sha,
        embedded=replay_slices.get("optional_source_metadata_sha256"),
        label="replay_metadata.json (slices optional_source_metadata_sha256)",
    )
    if err:
        return err
    err = _lineage_report_mismatch_error(
        computed_sha=meta_rep_sha,
        embedded=replay_slices.get("optional_source_metadata_report_sha256"),
        label="replay_metadata_report.json (slices optional_source_metadata_report_sha256)",
    )
    if err:
        return err
    return None


def verify_replay_plane_lineage(
    *,
    metadata: dict[str, Any],
    timeline: dict[str, Any],
    build_order_economy: dict[str, Any],
    combat_scouting_visibility: dict[str, Any],
    replay_slices: dict[str, Any],
    timeline_report: dict[str, Any] | None,
    build_order_economy_report: dict[str, Any] | None,
    combat_scouting_visibility_report: dict[str, Any] | None,
    metadata_report: dict[str, Any] | None,
) -> str | None:
    """Return an error string on lineage failure, else ``None``."""

    sha_t = sha256_hex_of_canonical_json(timeline)
    sha_boe = sha256_hex_of_canonical_json(build_order_economy)
    sha_csv = sha256_hex_of_canonical_json(combat_scouting_visibility)
    sha_meta = sha256_hex_of_canonical_json(metadata)

    if not isinstance(build_order_economy.get("source_timeline_sha256"), str) or not _hex_eq(
        str(build_order_economy.get("source_timeline_sha256")),
        sha_t,
    ):
        return "build_order_economy.source_timeline_sha256 mismatch vs canonical timeline hash"
    if not isinstance(combat_scouting_visibility.get("source_timeline_sha256"), str) or not _hex_eq(
        str(combat_scouting_visibility.get("source_timeline_sha256")),
        sha_t,
    ):
        return (
            "combat_scouting_visibility.source_timeline_sha256 mismatch vs canonical timeline hash"
        )
    if not isinstance(
        combat_scouting_visibility.get("source_build_order_economy_sha256"),
        str,
    ) or not _hex_eq(
        str(combat_scouting_visibility.get("source_build_order_economy_sha256")),
        sha_boe,
    ):
        return (
            "combat_scouting_visibility.source_build_order_economy_sha256 mismatch vs "
            "canonical build_order_economy hash"
        )
    if not isinstance(replay_slices.get("source_timeline_sha256"), str) or not _hex_eq(
        str(replay_slices.get("source_timeline_sha256")),
        sha_t,
    ):
        return "replay_slices.source_timeline_sha256 mismatch vs canonical timeline hash"
    if not isinstance(replay_slices.get("source_build_order_economy_sha256"), str) or not _hex_eq(
        str(replay_slices.get("source_build_order_economy_sha256")),
        sha_boe,
    ):
        return (
            "replay_slices.source_build_order_economy_sha256 mismatch vs canonical "
            "build_order_economy hash"
        )
    if not isinstance(
        replay_slices.get("source_combat_scouting_visibility_sha256"),
        str,
    ) or not _hex_eq(
        str(replay_slices.get("source_combat_scouting_visibility_sha256")),
        sha_csv,
    ):
        return (
            "replay_slices.source_combat_scouting_visibility_sha256 mismatch vs canonical "
            "combat_scouting_visibility hash"
        )

    raw_vals: list[tuple[str, str]] = []
    for fname, obj in (
        ("replay_metadata.json", metadata),
        ("replay_timeline.json", timeline),
        ("replay_build_order_economy.json", build_order_economy),
        ("replay_combat_scouting_visibility.json", combat_scouting_visibility),
    ):
        v = obj.get("source_raw_parse_sha256")
        if isinstance(v, str) and v:
            raw_vals.append((fname, v))
    if raw_vals:
        distinct = {x[1].lower() for x in raw_vals}
        if len(distinct) > 1:
            return (
                "source_raw_parse_sha256 values differ across governed replay artifacts: "
                + ", ".join(f"{a}={b[:16]}…" for a, b in sorted(raw_vals))
            )

    tl_rep_sha = (
        sha256_hex_of_canonical_json(timeline_report) if timeline_report is not None else None
    )
    boe_rep_sha = (
        sha256_hex_of_canonical_json(build_order_economy_report)
        if build_order_economy_report is not None
        else None
    )

    err = _lineage_report_mismatch_error(
        computed_sha=tl_rep_sha,
        embedded=build_order_economy.get("source_timeline_report_sha256"),
        label="replay_timeline_report.json (M11 source_timeline_report_sha256)",
    )
    if err:
        return err
    err = _lineage_report_mismatch_error(
        computed_sha=tl_rep_sha,
        embedded=combat_scouting_visibility.get("source_timeline_report_sha256"),
        label="replay_timeline_report.json (M12 source_timeline_report_sha256)",
    )
    if err:
        return err
    err = _lineage_report_mismatch_error(
        computed_sha=boe_rep_sha,
        embedded=combat_scouting_visibility.get("source_build_order_economy_report_sha256"),
        label=(
            "replay_build_order_economy_report.json (M12 source_build_order_economy_report_sha256)"
        ),
    )
    if err:
        return err

    err = _lineage_report_mismatch_error(
        computed_sha=tl_rep_sha,
        embedded=timeline.get("source_metadata_report_sha256"),
        label="replay_metadata_report.json (M10 timeline source_metadata_report_sha256)",
    )
    if err:
        return err
    err = _lineage_report_mismatch_error(
        computed_sha=sha_meta,
        embedded=timeline.get("source_metadata_sha256"),
        label="replay_metadata.json (M10 timeline source_metadata_sha256)",
    )
    if err:
        return err

    err = _validate_slices_optional_report_hashes(
        build_order_economy_report=build_order_economy_report,
        combat_scouting_visibility_report=combat_scouting_visibility_report,
        metadata=metadata,
        metadata_report=metadata_report,
        replay_slices=replay_slices,
        timeline_report=timeline_report,
    )
    if err:
        return err

    return None


def compute_lineage_root(*, primary_hashes: dict[str, str]) -> str:
    """Deterministic hash over sorted primary artifact hashes."""

    payload = {"primary_artifact_hashes": {k: primary_hashes[k] for k in sorted(primary_hashes)}}
    return sha256_hex_of_canonical_json(payload)


def compute_bundle_id(
    *,
    lineage_root: str,
    generation_parameters: dict[str, Any],
) -> str:
    """Stable bundle identity (no timestamps, paths, or secondary reports)."""

    body = {
        "contract": REPLAY_BUNDLE_CONTRACT_VERSION,
        "generation_parameters": generation_parameters,
        "included_milestones": included_milestones_primary(),
        "lineage_root": lineage_root,
        "profile": REPLAY_BUNDLE_PROFILE,
    }
    return sha256_hex_of_canonical_json(body)


def build_replay_bundle_envelope(
    *,
    primary_objects: dict[str, dict[str, Any]],
    secondary_reports: dict[str, dict[str, Any]],
    bundle_created_from: str,
    generation_parameters: dict[str, Any] | None = None,
    optional_intake_receipt: dict[str, Any] | None = None,
    optional_parse_receipt: dict[str, Any] | None = None,
) -> tuple[RunStatus, str | None, dict[str, Any], dict[str, Any], dict[str, Any]]:
    """Return ``(status, error, manifest, lineage, contents)``."""

    for name in PRIMARY_ARTIFACT_FILENAMES:
        if name not in primary_objects:
            return "load_failed", f"missing primary artifact: {name}", {}, {}, {}

    metadata = primary_objects["replay_metadata.json"]
    timeline = primary_objects["replay_timeline.json"]
    boe = primary_objects["replay_build_order_economy.json"]
    csv = primary_objects["replay_combat_scouting_visibility.json"]
    slices = primary_objects["replay_slices.json"]

    timeline_report = secondary_reports.get("replay_timeline_report.json")
    boe_report = secondary_reports.get("replay_build_order_economy_report.json")
    csv_report = secondary_reports.get("replay_combat_scouting_visibility_report.json")
    metadata_report = secondary_reports.get("replay_metadata_report.json")
    err = verify_replay_plane_lineage(
        build_order_economy=boe,
        build_order_economy_report=boe_report,
        combat_scouting_visibility=csv,
        combat_scouting_visibility_report=csv_report,
        metadata=metadata,
        metadata_report=metadata_report,
        replay_slices=slices,
        timeline=timeline,
        timeline_report=timeline_report,
    )
    if err is not None:
        return "lineage_failed", err, {}, {}, {}

    primary_hashes = {
        n: sha256_hex_of_canonical_json(primary_objects[n]) for n in PRIMARY_ARTIFACT_FILENAMES
    }
    secondary_hashes = {
        k: sha256_hex_of_canonical_json(secondary_reports[k])
        for k in sorted(secondary_reports.keys())
    }
    lineage_root = compute_lineage_root(primary_hashes=primary_hashes)

    gen_params = generation_parameters or {
        "replay_bundle_catalog": "starlab.replay_bundle_catalog.m14.v1",
    }

    bundle_id = compute_bundle_id(lineage_root=lineage_root, generation_parameters=gen_params)

    primary_list = list(PRIMARY_ARTIFACT_FILENAMES)
    secondary_list = sorted(secondary_reports.keys())

    artifact_hashes: dict[str, str] = {}
    artifact_hashes.update(primary_hashes)
    artifact_hashes.update(secondary_hashes)

    manifest: dict[str, Any] = {
        "artifact_hashes": {k: artifact_hashes[k] for k in sorted(artifact_hashes)},
        "bundle_created_from": bundle_created_from,
        "bundle_id": bundle_id,
        "contract": REPLAY_BUNDLE_CONTRACT_VERSION,
        "determinism_notes": determinism_notes_v1(),
        "exclusions": exclusions_policy_v1(),
        "generation_parameters": gen_params,
        "included_milestones": included_milestones_primary(),
        "lineage_root": lineage_root,
        "primary_artifacts": primary_list,
        "profile": REPLAY_BUNDLE_PROFILE,
        "schema_version": REPLAY_BUNDLE_MANIFEST_SCHEMA_VERSION,
        "secondary_report_artifacts": secondary_list,
        "source_replay_identity": metadata.get("replay_content_sha256"),
    }

    nodes: list[dict[str, Any]] = []
    edges: list[dict[str, str]] = []

    for fn in primary_list:
        milestone, nid, label = PRIMARY_NODE_INFO[fn]
        nodes.append(
            node_record(
                artifact_filename=fn,
                content_sha256=primary_hashes[fn],
                contextual_ancestry=False,
                label=label,
                milestone=milestone,
                node_id=nid,
                proof_surface_required=True,
            ),
        )

    for fn in secondary_list:
        milestone, nid, label = SECONDARY_REPORT_NODE_INFO[fn]
        nodes.append(
            node_record(
                artifact_filename=fn,
                content_sha256=secondary_hashes[fn],
                contextual_ancestry=False,
                label=label,
                milestone=milestone,
                node_id=nid,
                proof_surface_required=False,
            ),
        )

    nodes.append(
        node_record(
            artifact_filename=None,
            content_sha256=bundle_id,
            contextual_ancestry=False,
            label=bundle_node_label(),
            milestone="M14",
            node_id=bundle_node_id(),
            proof_surface_required=True,
        ),
    )

    chain_ids = [PRIMARY_NODE_INFO[f][1] for f in PRIMARY_ARTIFACT_FILENAMES]
    chain_ids.append(bundle_node_id())
    for i in range(len(chain_ids) - 1):
        edges.append({"from": chain_ids[i], "to": chain_ids[i + 1]})

    lineage_failures: list[str] = []
    optional_nodes: list[dict[str, Any]] = []

    if optional_intake_receipt is not None:
        h = sha256_hex_of_canonical_json(optional_intake_receipt)
        optional_nodes.append(
            node_record(
                artifact_filename="replay_intake_receipt.json",
                content_sha256=h,
                contextual_ancestry=True,
                label="Replay intake (M07 contextual)",
                milestone="M07",
                node_id="m07_replay_intake",
                proof_surface_required=False,
            ),
        )
    if optional_parse_receipt is not None:
        h = sha256_hex_of_canonical_json(optional_parse_receipt)
        optional_nodes.append(
            node_record(
                artifact_filename="replay_parse_receipt.json",
                content_sha256=h,
                contextual_ancestry=True,
                label="Replay parse receipt (M08 contextual)",
                milestone="M08",
                node_id="m08_replay_parse",
                proof_surface_required=False,
            ),
        )

    if optional_nodes:
        nodes.extend(sorted(optional_nodes, key=lambda r: str(r["node_id"])))
        if optional_intake_receipt is not None and optional_parse_receipt is not None:
            edges.append({"from": "m07_replay_intake", "to": "m08_replay_parse"})
            edges.append({"from": "m08_replay_parse", "to": "m09_metadata"})
        elif optional_intake_receipt is not None:
            edges.append({"from": "m07_replay_intake", "to": "m09_metadata"})
        elif optional_parse_receipt is not None:
            edges.append({"from": "m08_replay_parse", "to": "m09_metadata"})

    edges_sorted = sorted(edges, key=lambda e: (e["from"], e["to"]))

    upstream_requirements_satisfied = True

    lineage: dict[str, Any] = {
        "bundle_id": bundle_id,
        "contract": REPLAY_BUNDLE_CONTRACT_VERSION,
        "edges": edges_sorted,
        "lineage_failures": lineage_failures,
        "nodes": sorted(nodes, key=lambda r: str(r["node_id"])),
        "optional_contextual_ancestry_note": optional_contextual_ancestry_note(),
        "profile": REPLAY_BUNDLE_PROFILE,
        "root_hashes": sorted([lineage_root, bundle_id]),
        "schema_version": REPLAY_BUNDLE_LINEAGE_SCHEMA_VERSION,
        "upstream_requirements_satisfied": upstream_requirements_satisfied,
    }

    roles: dict[str, str] = {}
    for fn in primary_list:
        roles[fn] = "primary_governed_data"
    for fn in secondary_list:
        roles[fn] = "secondary_report"

    contents: dict[str, Any] = {
        "artifact_roles": {k: roles[k] for k in sorted(roles)},
        "bundle_id": bundle_id,
        "excluded_artifacts": exclusions_policy_v1(),
        "primary_artifacts": primary_list,
        "profile": REPLAY_BUNDLE_PROFILE,
        "report_artifacts": secondary_list,
        "schema_version": REPLAY_BUNDLE_CONTENTS_SCHEMA_VERSION,
    }

    return "completed", None, manifest, lineage, contents
