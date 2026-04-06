"""SC2 runtime surface helpers (M01): typed probe models and path detection only."""

from __future__ import annotations

from typing import Any

from starlab.sc2.models import InterfaceModeSupport, Sc2ProbeResult, Sc2RuntimeSpec

__all__ = [
    "InterfaceModeSupport",
    "Sc2ProbeResult",
    "Sc2RuntimeSpec",
    "probe_result_to_json",
    "run_probe",
]


def __getattr__(name: str) -> Any:
    if name == "run_probe":
        from starlab.sc2.env_probe import run_probe as run_probe_impl

        return run_probe_impl
    if name == "probe_result_to_json":
        from starlab.sc2.env_probe import probe_result_to_json as probe_result_to_json_impl

        return probe_result_to_json_impl
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
