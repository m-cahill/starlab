"""Tests for T1 synthetic CUDA training phase helpers."""

from __future__ import annotations

from starlab.training.t1_synthetic_cuda_training import (
    PHASE_KIND_T1_SYNTHETIC_CUDA,
    t1_synthetic_cuda_phases_in_order,
)


def test_t1_synthetic_cuda_phases_in_order_filters_kind() -> None:
    protocol = {
        "phases": [
            {"kind": "gate", "phase": "preflight"},
            {"kind": PHASE_KIND_T1_SYNTHETIC_CUDA, "phase": "p_cuda"},
            {"kind": "bootstrap_episodes", "phase": "b"},
        ],
    }
    got = t1_synthetic_cuda_phases_in_order(protocol)
    assert len(got) == 1
    assert got[0]["phase"] == "p_cuda"


def test_t1_synthetic_cuda_phases_empty_without_protocol() -> None:
    assert t1_synthetic_cuda_phases_in_order({}) == []
