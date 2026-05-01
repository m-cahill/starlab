"""Bounded match harness — dispatches to fake or BurnySc2 adapter."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from starlab.sc2.adapters.burnysc2_adapter import run_burnysc2_adapter
from starlab.sc2.adapters.fake import FakeMatchHarnessAdapter
from starlab.sc2.artifacts import ExecutionProofRecord
from starlab.sc2.match_config import MatchConfig


@dataclass(frozen=True, slots=True)
class HarnessResult:
    ok: bool
    proof: ExecutionProofRecord | None
    message: str | None = None


def run_match_execution(
    config: MatchConfig,
    *,
    output_dir: Path | None = None,
    hierarchical_sklearn_bundle: dict[str, Any] | None = None,
    m52a_candidate_spike_bundle: dict[str, Any] | None = None,
) -> HarnessResult:
    """Execute one bounded match and build a proof record."""

    try:
        if config.adapter == "fake":
            proof = FakeMatchHarnessAdapter().run(config)
        elif config.adapter == "burnysc2":
            proof = run_burnysc2_adapter(
                config,
                output_dir,
                hierarchical_sklearn_bundle=hierarchical_sklearn_bundle,
                m52a_candidate_spike_bundle=m52a_candidate_spike_bundle,
            )
        else:
            return HarnessResult(
                ok=False, proof=None, message=f"unknown adapter {config.adapter!r}"
            )
    except (OSError, RuntimeError, ValueError, ImportError, KeyError, FileNotFoundError) as e:
        return HarnessResult(ok=False, proof=None, message=str(e))
    except Exception as e:  # noqa: BLE001 — adapter / SC2 failures are surfaced to CLI
        return HarnessResult(ok=False, proof=None, message=f"{type(e).__name__}: {e}")

    return HarnessResult(ok=True, proof=proof, message=None)
