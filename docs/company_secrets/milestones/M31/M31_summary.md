# Milestone Summary — M31: Replay Explorer / Operator Evidence Surface

**Project:** STARLAB  
**Phase:** V — Learning Paths, Evidence Surfaces, and Flagship Proof  
**Milestone:** M31 — Replay Explorer / Operator Evidence Surface  
**Timeframe:** 2026-04-10 (merge)  
**Status:** **Closed on `main`** ([PR #37](https://github.com/m-cahill/starlab/pull/37); merge commit `41d62056e1956627b63152221932dc9c2423429c`; **authoritative PR-head** [`24225153475`](https://github.com/m-cahill/starlab/actions/runs/24225153475); **merge-boundary `main`** [`24226308356`](https://github.com/m-cahill/starlab/actions/runs/24226308356))

## 1. What M31 proved

M31 proves a **deterministic, offline, operator-facing replay explorer evidence surface** over already-governed STARLAB artifacts:

* **Panels** derived from governed **M13** `replay_slices.json` under selection policy **`starlab.m31.selection.slice_anchor_v1`** (stable ordering; anchor = integer midpoint of each slice window).
* **Bounded excerpts** from **M10** timeline, **M11** build-order/economy, **M12** combat/scouting — fixed caps (8 / 6 / 6) documented in `docs/runtime/replay_explorer_surface_v1.md`.
* **One anchor frame** each of **M16** canonical state (projected excerpt) and **M18** observation (projected excerpt) via the existing **M16 → M18** in-process seam (`materialize_observation_for_observation_request`).
* **M30 hierarchical traces:** `FrozenHierarchicalImitationPredictor` + `build_context_signature`; emitted documents validated to **M29** hierarchical trace schema where materialization succeeds; failed slices emit warnings without fabricating traces.
* **Primary JSON:** `replay_explorer_surface.json` (`surface_version` `starlab.replay_explorer_surface.v1`) and `replay_explorer_surface_report.json` (`report_version` `starlab.replay_explorer_surface_report.v1`).
* **Import posture:** listed `starlab/explorer/` modules do not import `starlab.replays`, `starlab.sc2`, or `s2protocol` (AST + tests).

## 2. Primary artifacts

| Artifact | Role |
| -------- | ---- |
| `replay_explorer_surface.json` | Bounded panels, excerpts, hierarchical trace documents, `non_claims`, bundle identity |
| `replay_explorer_surface_report.json` | Panel counts, delegate/label frequencies, excerpt policy, `governed_asset_classes` |

| Contract | Path |
| -------- | ---- |
| Runtime | `docs/runtime/replay_explorer_surface_v1.md` |

| CLI | `python -m starlab.explorer.emit_replay_explorer_surface` |

## 3. Explicit non-claims

* **No** benchmark integrity or leaderboard validity.  
* **No** live SC2 or replay↔execution equivalence.  
* **No** raw SC2 action legality.  
* **No** full replay browser / hosted UI / deployment readiness.  
* **No** M32 flagship proof-pack product semantics.  
* **No** new training or replay parser work in M31 scope.

## 4. Delivered (implementation)

* `docs/runtime/replay_explorer_surface_v1.md`  
* `starlab/explorer/` (`replay_explorer_models.py`, `replay_explorer_selection.py`, `replay_explorer_builder.py`, `replay_explorer_io.py`, `emit_replay_explorer_surface.py`)  
* `tests/fixtures/m31/`, `tests/test_replay_explorer_surface.py`  
* Ledger / governance updates in `docs/starlab.md` and `tests/test_governance.py` (closeout)

## 5. Next milestone

**M32** — Public Flagship Proof Pack — **stub-only** (`M32_plan.md`, `M32_toolcalls.md`); **no** M32 product code in M31 closeout.

---

*Summary aligned with milestone closeout practice; CI evidence cross-checked with `M31_run1.md` and ledger §18 / §23.*
