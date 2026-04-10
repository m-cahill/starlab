"""Load governed upstream JSON; validate lineage; emit M13 slice artifacts."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from starlab._io import load_json_object
from starlab.replays.replay_slice_generation import RunStatus, generate_replay_slices_envelope
from starlab.runs.json_util import canonical_json_dumps, sha256_hex_of_canonical_json


def _hex_eq(a: str, b: str) -> bool:
    return a.lower() == b.lower()


def exit_code_for_replay_slice_run(status: RunStatus) -> int:
    if status == "completed":
        return 0
    if status == "extraction_failed":
        return 4
    if status == "lineage_failed":
        return 5
    if status == "source_contract_failed":
        return 5
    msg = f"unknown replay slice run status: {status!r}"
    raise ValueError(msg)


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


def _validate_upstream_report_lineage(
    *,
    timeline_report: dict[str, Any] | None,
    build_order_economy: dict[str, Any],
    build_order_economy_report: dict[str, Any] | None,
    combat_scouting_visibility: dict[str, Any],
    combat_scouting_visibility_report: dict[str, Any] | None,
) -> str | None:
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

    return None


def write_replay_slice_artifacts(
    *,
    output_dir: Path,
    artifact: dict[str, Any],
    report: dict[str, Any],
) -> tuple[Path, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    ap = output_dir / "replay_slices.json"
    rp = output_dir / "replay_slices_report.json"
    ap.write_text(canonical_json_dumps(artifact), encoding="utf-8")
    rp.write_text(canonical_json_dumps(report), encoding="utf-8")
    return ap, rp


def extract_replay_slices_from_paths(
    *,
    timeline_path: Path,
    build_order_economy_path: Path,
    combat_scouting_visibility_path: Path,
    output_dir: Path,
    timeline_report_path: Path | None,
    build_order_economy_report_path: Path | None,
    combat_scouting_visibility_report_path: Path | None,
    metadata_path: Path | None,
    metadata_report_path: Path | None,
) -> tuple[RunStatus, dict[str, Any], dict[str, Any]]:
    timeline, terr = load_json_object(timeline_path)
    if timeline is None:
        artifact = {
            "contract": "starlab.replay_slices_contract.v1",
            "profile": "starlab.replay_slices.m13.v1",
            "schema_version": "starlab.replay_slices.v1",
            "slices": [],
        }
        report: dict[str, Any] = {
            "contract": "starlab.replay_slices_contract.v1",
            "lineage_error": str(terr),
            "profile": "starlab.replay_slices.m13.v1",
            "reason_codes": ["timeline_load_failed"],
            "schema_version": "starlab.replay_slices_report.v1",
        }
        write_replay_slice_artifacts(artifact=artifact, output_dir=output_dir, report=report)
        return "extraction_failed", artifact, report

    boe, boerr = load_json_object(build_order_economy_path)
    if boe is None:
        artifact = {
            "contract": "starlab.replay_slices_contract.v1",
            "profile": "starlab.replay_slices.m13.v1",
            "schema_version": "starlab.replay_slices.v1",
            "slices": [],
        }
        report = {
            "contract": "starlab.replay_slices_contract.v1",
            "lineage_error": str(boerr),
            "profile": "starlab.replay_slices.m13.v1",
            "reason_codes": ["build_order_economy_load_failed"],
            "schema_version": "starlab.replay_slices_report.v1",
        }
        write_replay_slice_artifacts(artifact=artifact, output_dir=output_dir, report=report)
        return "extraction_failed", artifact, report

    csv, csverr = load_json_object(combat_scouting_visibility_path)
    if csv is None:
        artifact = {
            "contract": "starlab.replay_slices_contract.v1",
            "profile": "starlab.replay_slices.m13.v1",
            "schema_version": "starlab.replay_slices.v1",
            "slices": [],
        }
        report = {
            "contract": "starlab.replay_slices_contract.v1",
            "lineage_error": str(csverr),
            "profile": "starlab.replay_slices.m13.v1",
            "reason_codes": ["combat_scouting_visibility_load_failed"],
            "schema_version": "starlab.replay_slices_report.v1",
        }
        write_replay_slice_artifacts(artifact=artifact, output_dir=output_dir, report=report)
        return "extraction_failed", artifact, report

    def _load_opt(p: Path | None) -> dict[str, Any] | None:
        if p is None:
            return None
        d, e = load_json_object(p)
        if e is not None:
            raise ValueError(e)
        return d

    try:
        timeline_report = _load_opt(timeline_report_path)
        build_order_economy_report = _load_opt(build_order_economy_report_path)
        combat_scouting_visibility_report = _load_opt(combat_scouting_visibility_report_path)
        metadata = _load_opt(metadata_path)
        metadata_report = _load_opt(metadata_report_path)
    except ValueError as exc:
        artifact_err = {
            "contract": "starlab.replay_slices_contract.v1",
            "profile": "starlab.replay_slices.m13.v1",
            "schema_version": "starlab.replay_slices.v1",
            "slices": [],
        }
        report_err = {
            "contract": "starlab.replay_slices_contract.v1",
            "lineage_error": str(exc),
            "profile": "starlab.replay_slices.m13.v1",
            "reason_codes": ["lineage_load_failed"],
            "schema_version": "starlab.replay_slices_report.v1",
        }
        write_replay_slice_artifacts(
            artifact=artifact_err,
            output_dir=output_dir,
            report=report_err,
        )
        return "lineage_failed", artifact_err, report_err

    lr_err = _validate_upstream_report_lineage(
        build_order_economy=boe,
        build_order_economy_report=build_order_economy_report,
        combat_scouting_visibility=csv,
        combat_scouting_visibility_report=combat_scouting_visibility_report,
        timeline_report=timeline_report,
    )
    if lr_err is not None:
        artifact_l = {
            "contract": "starlab.replay_slices_contract.v1",
            "profile": "starlab.replay_slices.m13.v1",
            "schema_version": "starlab.replay_slices.v1",
            "slices": [],
        }
        report_l = {
            "contract": "starlab.replay_slices_contract.v1",
            "lineage_error": lr_err,
            "profile": "starlab.replay_slices.m13.v1",
            "reason_codes": ["upstream_report_lineage_mismatch"],
            "schema_version": "starlab.replay_slices_report.v1",
        }
        write_replay_slice_artifacts(artifact=artifact_l, output_dir=output_dir, report=report_l)
        return "lineage_failed", artifact_l, report_l

    source_timeline_sha256 = sha256_hex_of_canonical_json(timeline)
    source_build_order_economy_sha256 = sha256_hex_of_canonical_json(boe)
    source_combat_scouting_visibility_sha256 = sha256_hex_of_canonical_json(csv)

    status, body, report_out = generate_replay_slices_envelope(
        build_order_economy=boe,
        build_order_economy_report=build_order_economy_report,
        combat_scouting_visibility=csv,
        combat_scouting_visibility_report=combat_scouting_visibility_report,
        metadata=metadata,
        metadata_report=metadata_report,
        source_build_order_economy_sha256=source_build_order_economy_sha256,
        source_combat_scouting_visibility_sha256=source_combat_scouting_visibility_sha256,
        source_timeline_sha256=source_timeline_sha256,
        timeline=timeline,
        timeline_report=timeline_report,
    )
    write_replay_slice_artifacts(artifact=body, output_dir=output_dir, report=report_out)
    return status, body, report_out
