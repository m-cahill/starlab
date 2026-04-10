"""Load governed replay JSON; validate lineage; emit bundle artifacts (M14)."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from starlab._io import load_json_object
from starlab.replays.replay_bundle_generation import RunStatus, build_replay_bundle_envelope
from starlab.replays.replay_bundle_models import (
    PRIMARY_ARTIFACT_FILENAMES,
    SECONDARY_REPORT_FILENAMES,
)
from starlab.runs.json_util import canonical_json_dumps


def exit_code_for_replay_bundle_run(status: RunStatus) -> int:
    if status == "completed":
        return 0
    if status == "lineage_failed":
        return 5
    if status == "load_failed":
        return 4
    msg = f"unknown replay bundle run status: {status!r}"
    raise ValueError(msg)


def collect_secondary_reports_from_dir(input_dir: Path) -> dict[str, dict[str, Any]]:
    """Load optional ``*_report.json`` files present under ``input_dir``."""

    out: dict[str, dict[str, Any]] = {}
    for name in SECONDARY_REPORT_FILENAMES:
        p = input_dir / name
        if not p.is_file():
            continue
        obj, err = load_json_object(p)
        if obj is None:
            raise ValueError(f"{name}: {err}")
        out[name] = obj
    return out


def write_replay_bundle_artifacts(
    *,
    output_dir: Path,
    manifest: dict[str, Any],
    lineage: dict[str, Any],
    contents: dict[str, Any],
) -> tuple[Path, Path, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    mp = output_dir / "replay_bundle_manifest.json"
    lp = output_dir / "replay_bundle_lineage.json"
    cp = output_dir / "replay_bundle_contents.json"
    mp.write_text(canonical_json_dumps(manifest), encoding="utf-8")
    lp.write_text(canonical_json_dumps(lineage), encoding="utf-8")
    cp.write_text(canonical_json_dumps(contents), encoding="utf-8")
    return mp, lp, cp


def extract_replay_bundle_from_paths(
    *,
    input_dir: Path,
    output_dir: Path,
    optional_intake_receipt_path: Path | None = None,
    optional_parse_receipt_path: Path | None = None,
    bundle_created_from: str | None = None,
    generation_parameters: dict[str, Any] | None = None,
) -> tuple[RunStatus, str | None, dict[str, Any], dict[str, Any], dict[str, Any]]:
    """Load primary JSON from ``input_dir``; optional reports if present; emit bundle JSON."""

    primary_objects: dict[str, dict[str, Any]] = {}
    for name in PRIMARY_ARTIFACT_FILENAMES:
        p = input_dir / name
        obj, err = load_json_object(p)
        if obj is None:
            return "load_failed", f"{name}: {err}", {}, {}, {}
        primary_objects[name] = obj

    try:
        secondary_reports = collect_secondary_reports_from_dir(input_dir)
    except ValueError as exc:
        return "load_failed", str(exc), {}, {}, {}

    optional_intake: dict[str, Any] | None = None
    optional_parse: dict[str, Any] | None = None
    if optional_intake_receipt_path is not None:
        optional_intake, ierr = load_json_object(optional_intake_receipt_path)
        if optional_intake is None:
            return "load_failed", f"replay_intake_receipt.json: {ierr}", {}, {}, {}
    if optional_parse_receipt_path is not None:
        optional_parse, perr = load_json_object(optional_parse_receipt_path)
        if optional_parse is None:
            return "load_failed", f"replay_parse_receipt.json: {perr}", {}, {}, {}

    created = bundle_created_from or f"input_dir:{input_dir.name}"

    status, err, manifest, lineage, contents = build_replay_bundle_envelope(
        bundle_created_from=created,
        generation_parameters=generation_parameters,
        optional_intake_receipt=optional_intake,
        optional_parse_receipt=optional_parse,
        primary_objects=primary_objects,
        secondary_reports=secondary_reports,
    )
    if status != "completed":
        return status, err, {}, {}, {}

    write_replay_bundle_artifacts(
        contents=contents,
        lineage=lineage,
        manifest=manifest,
        output_dir=output_dir,
    )
    return status, None, manifest, lineage, contents
