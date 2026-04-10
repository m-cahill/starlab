"""Typed boundary for loading M14 replay bundles into evaluation (M35).

``learned_agent_evaluation`` must not import ``starlab.state.canonical_state_inputs``
directly; the default implementation delegates there.
"""

from __future__ import annotations

from pathlib import Path
from typing import Protocol

from starlab.state.canonical_state_inputs import M14BundleInputs, load_m14_bundle


class M14BundleLoader(Protocol):
    """Load a governed M14 bundle directory; same contract as ``load_m14_bundle``."""

    def __call__(self, bundle_dir: Path) -> tuple[M14BundleInputs | None, str | None]: ...


def default_load_m14_bundle(bundle_dir: Path) -> tuple[M14BundleInputs | None, str | None]:
    """Default loader — delegates to ``starlab.state.canonical_state_inputs.load_m14_bundle``."""

    return load_m14_bundle(bundle_dir)
