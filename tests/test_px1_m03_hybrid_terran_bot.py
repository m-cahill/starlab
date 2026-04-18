"""PX1-M03 hybrid Terran bot — pure helpers (no `sc2` / BurnySc2; CI-safe)."""

from __future__ import annotations

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
