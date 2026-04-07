"""Parser adapter protocol (M08). Implementations stay behind this boundary."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Protocol, runtime_checkable


@dataclass(frozen=True)
class AdapterAvailability:
    """Which optional replay streams exist in the MPQ archive (capability only)."""

    game_events_available: bool
    message_events_available: bool
    tracker_events_available: bool
    attribute_events_available: bool


@dataclass(frozen=True)
class RawParseSections:
    """Parser-native section payloads before STARLAB normalization."""

    header: dict[str, Any] | None
    details: dict[str, Any] | None
    init_data: dict[str, Any] | None
    attribute_events: dict[str, Any] | None


@dataclass(frozen=True)
class RawEventStreams:
    """Decoded game / message / tracker streams (M10-owned lowerings; not public semantics)."""

    game_events: list[dict[str, Any]] | None
    message_events: list[dict[str, Any]] | None
    tracker_events: list[dict[str, Any]] | None


@dataclass(frozen=True)
class AdapterSuccess:
    """Successful adapter decode (pre-normalization)."""

    protocol_context: dict[str, Any]
    raw_sections: RawParseSections
    availability: AdapterAvailability
    raw_event_streams: RawEventStreams | None = None


@dataclass(frozen=True)
class AdapterFailure:
    """Adapter could not produce raw sections."""

    kind: str
    message: str


# Success envelope or failure from ``parse_replay_file``.
AdapterOutcome = AdapterSuccess | AdapterFailure


@runtime_checkable
class ReplayParserAdapter(Protocol):
    """Pluggable replay decoder behind the M08 boundary."""

    def parser_family(self) -> str:
        """Short identifier (e.g. ``s2protocol``)."""

    def parser_version(self) -> str:
        """Implementation / library version string for receipts."""

    def dependency_available(self) -> bool:
        """Whether optional parser dependencies (e.g. ``s2protocol``) imported successfully."""

    def parse_replay_file(self, replay_path: Path) -> AdapterOutcome:
        """Decode replay file bytes via the underlying library."""
