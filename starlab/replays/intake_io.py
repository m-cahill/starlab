"""Replay hashing, metadata loading, and governed JSON emission (M07)."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from starlab.replays.intake_models import (
    POLICY_VERSION,
    RECEIPT_SCHEMA_VERSION,
    REPORT_SCHEMA_VERSION,
    NormalizedReplayIntakeMetadata,
    parse_replay_intake_metadata,
)
from starlab.replays.intake_policy import PolicyOutcome, evaluate_intake_policy
from starlab.runs.canonical_run_artifact import load_canonical_manifest
from starlab.runs.json_util import canonical_json_dumps, sha256_hex_of_canonical_json
from starlab.runs.replay_binding import load_replay_binding, load_run_identity


def _sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_replay_intake_metadata_file(
    path: Path,
) -> tuple[NormalizedReplayIntakeMetadata | None, str | None]:
    """Load ``replay_intake_metadata.json`` or return ``(None, error)``."""

    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        return None, str(exc)
    if not isinstance(raw, dict):
        return None, "metadata root must be a JSON object"
    try:
        return parse_replay_intake_metadata(raw), None
    except ValueError as exc:
        return None, str(exc)


def load_optional_replay_binding(path: Path | None) -> tuple[dict[str, Any] | None, str | None]:
    if path is None:
        return None, None
    try:
        return load_replay_binding(path), None
    except (OSError, UnicodeError, ValueError, json.JSONDecodeError) as exc:
        return None, str(exc)


def load_optional_run_identity(path: Path | None) -> tuple[dict[str, Any] | None, str | None]:
    if path is None:
        return None, None
    try:
        return load_run_identity(path), None
    except (OSError, UnicodeError, ValueError, json.JSONDecodeError) as exc:
        return None, str(exc)


def load_optional_manifest(path: Path | None) -> tuple[dict[str, Any] | None, str | None]:
    if path is None:
        return None, None
    try:
        return load_canonical_manifest(path), None
    except (OSError, UnicodeError, ValueError, json.JSONDecodeError) as exc:
        return None, str(exc)


def read_replay_opaque(replay_path: Path) -> tuple[str | None, int | None, str | None]:
    """Return ``(sha256_hex, size_bytes, read_error)``."""

    try:
        data = replay_path.read_bytes()
    except OSError as exc:
        return None, None, str(exc)
    digest = hashlib.sha256(data).hexdigest()
    return digest, len(data), None


def intake_metadata_sha256(meta: NormalizedReplayIntakeMetadata) -> str:
    """Deterministic hash over normalized metadata (canonical JSON, no trailing newline)."""

    return sha256_hex_of_canonical_json(meta.to_mapping())


def build_receipt(
    *,
    meta: NormalizedReplayIntakeMetadata | None,
    metadata_path: Path,
    replay_path: Path,
    replay_sha256: str | None,
    replay_size_bytes: int | None,
    linked_sha256: dict[str, str | None],
) -> dict[str, Any]:
    """``replay_intake_receipt.json`` body."""

    normalized: dict[str, Any] | None
    if meta is None:
        normalized = None
    else:
        normalized = meta.to_mapping()

    intake_hash: str | None
    if meta is None:
        try:
            raw_meta = json.loads(metadata_path.read_text(encoding="utf-8"))
            intake_hash = (
                sha256_hex_of_canonical_json(raw_meta) if isinstance(raw_meta, dict) else None
            )
        except (OSError, UnicodeError, json.JSONDecodeError):
            intake_hash = None
    else:
        intake_hash = intake_metadata_sha256(meta)

    return {
        "intake_metadata_sha256": intake_hash,
        "linked_artifacts": {
            "replay_binding.json": linked_sha256.get("replay_binding"),
            "run_artifact_manifest.json": linked_sha256.get("manifest"),
            "run_identity.json": linked_sha256.get("run_identity"),
        },
        "normalized_metadata": normalized,
        "observed_filename": replay_path.name,
        "policy_version": POLICY_VERSION,
        "replay_content_sha256": replay_sha256,
        "replay_size_bytes": replay_size_bytes,
        "schema_version": RECEIPT_SCHEMA_VERSION,
    }


def build_report(
    *,
    outcome: PolicyOutcome,
    replay_sha256: str | None,
) -> dict[str, Any]:
    """``replay_intake_report.json`` body."""

    checks = [dict(c) for c in outcome.check_results]
    return {
        "advisory_notes": list(outcome.advisory_notes),
        "canonical_review_eligible": outcome.canonical_review_eligible,
        "check_results": checks,
        "intake_status": outcome.intake_status,
        "local_processing_allowed": outcome.local_processing_allowed,
        "policy_version": POLICY_VERSION,
        "public_redistribution_allowed": outcome.public_redistribution_allowed,
        "reason_codes": list(outcome.reason_codes),
        "replay_content_sha256": replay_sha256,
        "schema_version": REPORT_SCHEMA_VERSION,
    }


def run_replay_intake(
    *,
    replay_path: Path,
    metadata_path: Path,
    replay_binding_path: Path | None,
    run_identity_path: Path | None,
    manifest_path: Path | None,
) -> tuple[PolicyOutcome, dict[str, Any], dict[str, Any]]:
    """Load inputs, evaluate policy, return outcome + receipt + report bodies."""

    meta, metadata_error = load_replay_intake_metadata_file(metadata_path)
    replay_sha256, replay_size, replay_read_error = read_replay_opaque(replay_path)

    rb, rb_err = load_optional_replay_binding(replay_binding_path)
    ri, ri_err = load_optional_run_identity(run_identity_path)
    mf, mf_err = load_optional_manifest(manifest_path)

    outcome = evaluate_intake_policy(
        manifest=mf,
        manifest_error=mf_err,
        metadata_error=metadata_error,
        meta=meta,
        replay_binding=rb,
        replay_binding_error=rb_err,
        replay_path=replay_path,
        replay_read_error=replay_read_error,
        replay_sha256=replay_sha256,
        run_identity=ri,
        run_identity_error=ri_err,
    )

    linked_sha256: dict[str, str | None] = {}
    for key, p in (
        ("replay_binding", replay_binding_path),
        ("run_identity", run_identity_path),
        ("manifest", manifest_path),
    ):
        if p is not None:
            try:
                linked_sha256[key] = _sha256_file(p)
            except OSError:
                linked_sha256[key] = None
        else:
            linked_sha256[key] = None

    receipt = build_receipt(
        linked_sha256=linked_sha256,
        meta=meta,
        metadata_path=metadata_path,
        replay_path=replay_path,
        replay_sha256=replay_sha256,
        replay_size_bytes=replay_size,
    )
    report = build_report(outcome=outcome, replay_sha256=replay_sha256)
    return outcome, receipt, report


def write_intake_artifacts(
    *,
    output_dir: Path,
    receipt: dict[str, Any],
    report: dict[str, Any],
) -> tuple[Path, Path]:
    """Write deterministic JSON files with trailing newlines."""

    output_dir.mkdir(parents=True, exist_ok=True)
    receipt_path = output_dir / "replay_intake_receipt.json"
    report_path = output_dir / "replay_intake_report.json"
    receipt_path.write_text(canonical_json_dumps(receipt), encoding="utf-8")
    report_path.write_text(canonical_json_dumps(report), encoding="utf-8")
    return receipt_path, report_path


def exit_code_for_status(status: str) -> int:
    """CLI exit code mapping for ``intake_status``."""

    if status == "eligible_for_canonical_review":
        return 0
    if status == "accepted_local_only":
        return 2
    if status == "quarantined":
        return 3
    if status == "rejected":
        return 4
    msg = f"unknown intake status: {status!r}"
    raise ValueError(msg)
