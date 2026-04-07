"""Typed models and schema constants for replay intake (M07)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Literal

METADATA_SCHEMA_VERSION = "starlab.replay_intake_metadata.v1"
RECEIPT_SCHEMA_VERSION = "starlab.replay_intake_receipt.v1"
REPORT_SCHEMA_VERSION = "starlab.replay_intake_report.v1"
POLICY_VERSION = "starlab.replay_intake_policy.v1"

IntakeStatus = Literal[
    "eligible_for_canonical_review",
    "accepted_local_only",
    "quarantined",
    "rejected",
]

CheckStatus = Literal["pass", "warn", "fail", "not_evaluated"]
CheckSeverity = Literal["required", "warning"]

DECLARED_ORIGIN_CLASSES: frozenset[str] = frozenset(
    {
        "starlab_generated",
        "external",
        "ladder_derived",
        "third_party",
        "unknown",
    },
)

DECLARED_ACQUISITION_CHANNELS: frozenset[str] = frozenset(
    {
        "direct_capture",
        "download",
        "generated",
        "operator_supplied",
        "unknown",
    },
)

DECLARED_PROVENANCE_STATUSES: frozenset[str] = frozenset(
    {
        "asserted",
        "verified",
        "unknown",
    },
)

DECLARED_REDISTRIBUTION_POSTURES: frozenset[str] = frozenset(
    {
        "allowed",
        "forbidden",
        "unknown",
    },
)

CHECK_IDS: tuple[str, ...] = (
    "metadata_schema_valid",
    "replay_file_readable",
    "replay_sha256_computed",
    "origin_class_declared",
    "provenance_status_declared",
    "redistribution_posture_declared",
    "expected_hash_match",
    "binding_hash_match",
    "binding_identity_consistent",
    "canonical_review_requirements_met",
)


@dataclass(frozen=True)
class NormalizedReplayIntakeMetadata:
    """Validated operator-declared intake metadata (enum fields normalized)."""

    schema_version: str
    declared_origin_class: str
    declared_acquisition_channel: str
    declared_provenance_status: str
    declared_redistribution_posture: str
    declared_source_label: str
    declared_source_reference: str | None
    operator_note: str | None
    expected_replay_content_sha256: str | None

    def to_mapping(self) -> dict[str, Any]:
        """JSON-serializable mapping with stable key order (caller sorts for hashing)."""

        return {
            "declared_acquisition_channel": self.declared_acquisition_channel,
            "declared_origin_class": self.declared_origin_class,
            "declared_provenance_status": self.declared_provenance_status,
            "declared_redistribution_posture": self.declared_redistribution_posture,
            "declared_source_label": self.declared_source_label,
            "declared_source_reference": self.declared_source_reference,
            "expected_replay_content_sha256": self.expected_replay_content_sha256,
            "operator_note": self.operator_note,
            "schema_version": self.schema_version,
        }


def _require_str(data: dict[str, Any], key: str) -> str:
    if key not in data:
        msg = f"missing required field: {key!r}"
        raise ValueError(msg)
    val = data[key]
    if not isinstance(val, str) or not val.strip():
        msg = f"{key!r} must be a non-empty string"
        raise ValueError(msg)
    return val.strip()


def _optional_str(data: dict[str, Any], key: str) -> str | None:
    if key not in data or data[key] is None:
        return None
    val = data[key]
    if not isinstance(val, str):
        msg = f"{key!r} must be a string or null"
        raise ValueError(msg)
    stripped = val.strip()
    return stripped if stripped else None


def _optional_sha256(data: dict[str, Any], key: str) -> str | None:
    if key not in data or data[key] is None:
        return None
    val = data[key]
    if not isinstance(val, str):
        msg = f"{key!r} must be a string or null"
        raise ValueError(msg)
    h = val.strip().lower()
    if len(h) != 64 or any(c not in "0123456789abcdef" for c in h):
        msg = f"{key!r} must be 64 lowercase hex characters when present"
        raise ValueError(msg)
    return h


def parse_replay_intake_metadata(raw: dict[str, Any]) -> NormalizedReplayIntakeMetadata:
    """Parse and validate ``replay_intake_metadata.json`` root object."""

    if not isinstance(raw, dict):
        msg = "metadata root must be a JSON object"
        raise ValueError(msg)

    sv = _require_str(raw, "schema_version")
    if sv != METADATA_SCHEMA_VERSION:
        msg = f"unexpected schema_version: {sv!r}"
        raise ValueError(msg)

    origin = _require_str(raw, "declared_origin_class")
    if origin not in DECLARED_ORIGIN_CLASSES:
        msg = f"invalid declared_origin_class: {origin!r}"
        raise ValueError(msg)

    channel = _require_str(raw, "declared_acquisition_channel")
    if channel not in DECLARED_ACQUISITION_CHANNELS:
        msg = f"invalid declared_acquisition_channel: {channel!r}"
        raise ValueError(msg)

    prov = _require_str(raw, "declared_provenance_status")
    if prov not in DECLARED_PROVENANCE_STATUSES:
        msg = f"invalid declared_provenance_status: {prov!r}"
        raise ValueError(msg)

    redist = _require_str(raw, "declared_redistribution_posture")
    if redist not in DECLARED_REDISTRIBUTION_POSTURES:
        msg = f"invalid declared_redistribution_posture: {redist!r}"
        raise ValueError(msg)

    label = _require_str(raw, "declared_source_label")

    return NormalizedReplayIntakeMetadata(
        schema_version=METADATA_SCHEMA_VERSION,
        declared_origin_class=origin,
        declared_acquisition_channel=channel,
        declared_provenance_status=prov,
        declared_redistribution_posture=redist,
        declared_source_label=label,
        declared_source_reference=_optional_str(raw, "declared_source_reference"),
        operator_note=_optional_str(raw, "operator_note"),
        expected_replay_content_sha256=_optional_sha256(raw, "expected_replay_content_sha256"),
    )
