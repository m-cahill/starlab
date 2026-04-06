"""Typed SC2 runtime probe models — path/config only; no SC2 execution (M01)."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field


@dataclass(frozen=True, slots=True)
class Sc2RuntimeSpec:
    """Canonical STARLAB labeling for the selected runtime surfaces (M01 decision)."""

    control_observation_surface: str = "s2client_proto_sc2api"
    replay_decode_surface: str = "s2protocol"


@dataclass(frozen=True, slots=True)
class InterfaceModeSupport:
    """Documented API capabilities (informational; not probed by executing SC2)."""

    raw_interface: bool = True
    feature_layer_interface: bool = True
    rendered_interface: bool = True


@dataclass(frozen=True, slots=True)
class Sc2ProbeResult:
    """Deterministic probe output: resolved paths, presence flags, optional version hints."""

    spec: Sc2RuntimeSpec
    interface_modes: InterfaceModeSupport
    paths: Mapping[str, str | None]
    present: Mapping[str, bool]
    base_build: str | None
    data_version: str | None
    notes: tuple[str, ...] = field(default_factory=tuple)
