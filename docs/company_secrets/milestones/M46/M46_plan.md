# M46 Plan — Bounded Live Validation Final-Status Semantics

**Milestone:** M46  
**Phase:** VI — Governed Agent Training, Comparison, and Local Validation  
**Branch:** `recharter/m44-bounded-live-final-status-semantics`  
**Status:** Complete on branch (pending merge to `main`; see §23 changelog / PR when opened)

## Objective

Resolve the **bounded live** asymmetry where **burnysc2** emitted literal SC2 `Result` strings (e.g. `Defeat`) in `match_execution.final_status` while the **fixture/fake** path emitted **`ok`**, blocking **M45** reward (`final_status == "ok"`) and operator pass rules despite healthy bounded harness completion.

## Recommendation (locked)

**Option A** — For bounded harness runs that complete the contract (step cap / `bounded_exit` in proof `status_sequence`), emit **`final_status="ok"`** as governed validation success. Preserve the literal SC2 outcome in **`sc2_game_result`** for forensics.

## Deliverables

- `starlab/sc2/adapters/burnysc2_adapter.py` — map bounded completion to `final_status="ok"`; set `sc2_game_result` from `run_game` result.
- `starlab/sc2/artifacts.py` — optional `sc2_game_result` on execution proof; hash behavior unchanged for legacy proofs without the field.
- `starlab/sc2/local_live_play_validation_harness.py` — surface `sc2_game_result` on `match_execution` when present.
- Runtime docs: `docs/runtime/local_live_play_validation_harness_v1.md`, `docs/runtime/self_play_rl_bootstrap_v1.md`.
- Ledger: `docs/starlab.md` (§1, §7, §8, §23, quick scan).
- Tests: `tests/test_m46_bounded_live_validation_semantics.py`, `tests/test_sc2_artifacts.py` — **fixture-only**; no live SC2 in CI.

## Acceptance

- Bounded **burnysc2** completion with `bounded_exit` yields **`final_status="ok"`** consistent with fake/fixture.
- **M45** `compute_episode_reward_validation_outcome_v1` treats that run as primary reward **1.0** when `final_status=="ok"`.
- Literal outcome remains inspectable via **`sc2_game_result`**.
- Non-claims explicit in docs/tests: **not** game victory, ladder, benchmark integrity, replay↔execution equivalence, live SC2 in CI.

## Explicit non-claims

No benchmark integrity, replay↔execution equivalence, ladder performance, or “agent won” semantics. **M42** contract-path mismatch is **out of scope** (separate follow-on).
