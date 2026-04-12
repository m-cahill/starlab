# M44 Plan — Local Live-Play Validation Harness v1

**Milestone:** M44  
**Phase:** VI — Governed Agent Training, Comparison, and Local Validation  
**Status:** Complete — merged to `main`; closeout `M44_run1.md`, `M44_summary.md`, `M44_audit.md` (see `docs/starlab.md` §7 / §11 / §18).

---

## Intent

Deliver the **first governed local live-play validation harness** for STARLAB: load an **M43** hierarchical training run + **local** `joblib` weights, run a **bounded M02** match harness, emit **M44** validation JSON, **replay binding**, deterministic **stub replay** in CI (`runtime_mode=fixture_stub_ci`), optional **video** metadata; **no** live SC2 in CI; **no** benchmark-integrity inflation; **no** **M45** RL.

---

## Locked defaults (implementation)

| Topic | Choice |
| ----- | ------ |
| Scope owner | `starlab.sc2` (+ thin `starlab.hierarchy.m43_sklearn_runtime` loader) |
| Harness shape | New orchestrator `local_live_play_validation_harness.py` **wrapping** existing `run_match_execution` |
| Candidate loading | Real M43 `hierarchical_training_run.json` + `weights/hierarchical_training_sklearn_bundle.joblib` |
| CI fake replay | Deterministic `.SC2Replay` placeholder bytes, hashed + M04 bound |
| Runtime config | Configurable map/opponent via M02 match config; `runtime_mode`: `fixture_stub_ci` \| `local_live_sc2` |
| Video registration | Simple metadata (`path`, `sha256`, `size_bytes`, `duration_seconds`, `format`; optional `resolution`, `codec`) |

---

## Slices (reference)

- **A:** Artifact contract — `local_live_play_validation_run.json` / report; layout under `out/live_validation_runs/<run_id>/`.
- **B:** Harness modules in `starlab.sc2` — models, I/O, harness, emitter CLI.
- **C:** Bounded **semantic-to-live** adapter — `starlab.m44.semantic_live_action_adapter.v1`.
- **D:** Replay binding + optional video registration.
- **E:** CI fixture tests — `tests/test_m44_local_live_play_validation_harness.py`.

---

## Deliverables

- `docs/runtime/local_live_play_validation_harness_v1.md`
- `starlab/sc2/` — `local_live_play_validation_*.py`, `semantic_live_action_adapter.py`, `emit_local_live_play_validation_run.py`
- `starlab/hierarchy/m43_sklearn_runtime.py`
- `tests/test_m44_local_live_play_validation_harness.py`
- `docs/starlab.md`, `README.md`, `docs/architecture.md` updates

---

## Out of scope

Live SC2 in CI; benchmark-integrity claims; replay↔execution equivalence; ladder claims; weights in repo; built-in screen recording; **M45** RL; broad multi-environment expansion.

---

## Acceptance (target)

1. Documented CLI for live-play validation.  
2. Harness supports **M43** hierarchical candidate + weights.  
3. Emits `local_live_play_validation_run.json` + report.  
4. Replay bound via `replay_binding.json`.  
5. Optional video registration.  
6. CI validates stub path without live SC2.  
7. Ledger updated for M44 charter (in progress until merge).  
8. No benchmark-integrity / live-performance claim inflation.
