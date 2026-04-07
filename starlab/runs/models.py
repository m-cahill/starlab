"""STARLAB run identity and lineage seed models (M03) — not canonical run artifact (M05)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

RUN_IDENTITY_SCHEMA_VERSION = "starlab.run_identity.v1"
LINEAGE_SEED_SCHEMA_VERSION = "starlab.lineage_seed.v1"

RUN_SPEC_KIND = "starlab.run_spec.v1"
EXECUTION_KIND = "starlab.execution.v1"
LINEAGE_SEED_KIND = "starlab.lineage_seed.v1"


@dataclass(frozen=True, slots=True)
class EnvironmentFingerprint:
    """Optional context for lineage — not a full environment lock (see docs)."""

    runtime_boundary_label: str
    adapter_name: str
    base_build: str | None = None
    data_version: str | None = None
    platform_string: str | None = None
    probe_digest: str | None = None

    def to_mapping(self) -> dict[str, Any]:
        return {
            "adapter_name": self.adapter_name,
            "base_build": self.base_build,
            "data_version": self.data_version,
            "platform_string": self.platform_string,
            "probe_digest": self.probe_digest,
            "runtime_boundary_label": self.runtime_boundary_label,
        }


@dataclass(frozen=True, slots=True)
class ArtifactReference:
    """Reference to an input or emitted artifact (content hash optional)."""

    logical_name: str
    path: str | None = None
    content_sha256: str | None = None
    role: str | None = None

    def to_mapping(self) -> dict[str, Any]:
        out: dict[str, Any] = {"logical_name": self.logical_name}
        if self.path is not None:
            out["path"] = self.path
        if self.content_sha256 is not None:
            out["content_sha256"] = self.content_sha256
        if self.role is not None:
            out["role"] = self.role
        return out
