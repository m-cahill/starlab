"""PX1-M03 hybrid Terran bot — pure helpers + factory (no live SC2 match execution)."""

from __future__ import annotations

from typing import Any

from starlab.sc2 import px1_m03_hybrid_terran_bot as m


def test_tally_keys_disjoint_and_cover_init() -> None:
    applied = set(m.TALLY_KEYS_APPLIED)
    attempted = set(m.TALLY_KEYS_ATTEMPTED)
    assert not applied & attempted
    tallies = m._init_tallies()
    assert set(tallies) == applied | attempted
    assert all(tallies[k] == 0 for k in tallies)


def test_bump_increments() -> None:
    t = m._init_tallies()
    m._bump(t, "worker_train_attempted")
    assert t["worker_train_attempted"] == 1
    m._bump(t, "worker_train_applied", 2)
    assert t["worker_train_applied"] == 2


def test_derive_sig_stable_string() -> None:
    s = m._derive_sig(2, 90, 400, 0)
    assert s == "m44_step=2|gameloop=90|minerals=400|vespene=0"


def test_make_hybrid_class_defines_bot_subclass() -> None:
    sink: dict[str, Any] = {"status_sequence": [], "observations": []}
    cls = m.make_px1_m03_hybrid_terran_bot_class(
        max_steps=4,
        game_step=8,
        sink=sink,
        hierarchical_sklearn_bundle={},
    )
    assert cls.__name__ == "_Px1M03HybridTerranBot"
    assert "live_action_tallies" in sink
    assert "live_action_behavior_summary" in sink
    assert all(sink["live_action_tallies"][k] == 0 for k in sink["live_action_tallies"])


def test_make_hybrid_class_rehydrates_empty_tallies() -> None:
    sink: dict[str, Any] = {
        "status_sequence": [],
        "observations": [],
        "live_action_tallies": {},
    }
    m.make_px1_m03_hybrid_terran_bot_class(
        max_steps=1,
        game_step=8,
        sink=sink,
        hierarchical_sklearn_bundle={},
    )
    assert sink["live_action_tallies"]
    assert all(sink["live_action_tallies"][k] == 0 for k in sink["live_action_tallies"])
