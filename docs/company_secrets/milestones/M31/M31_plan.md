# M31 Plan — Replay Explorer / Operator Evidence Surface

## Milestone identity

| Field | Value |
| ----- | ----- |
| **Milestone** | M31 |
| **Name** | Replay Explorer / Operator Evidence Surface |
| **Phase** | V — Learning Paths, Evidence Surfaces, and Flagship Proof |
| **Branch (recommended)** | `m31-replay-explorer-operator-evidence-surface` |

## Objective (narrow proof)

Prove a **deterministic, offline, operator-facing replay evidence surface** over artifacts already governed on `main`. For each **evidence panel** derived from a governed **M13** slice, bind **slice context**, **bounded upstream excerpts** (M10–M12), **one anchor frame** of **M16 / M18** materialization, and an **M29-compatible M30 hierarchical decision trace** — emitted as stable JSON plus a summary report and CLI.

**Not in scope:** hosted UI, live SC2, benchmark integrity claims, new training, replay parser work, **M32** flagship proof-pack product code.

## Primary artifacts

| Artifact | Role |
| -------- | ---- |
| `replay_explorer_surface.json` | Bounded panels + excerpts + traces + explicit `non_claims` |
| `replay_explorer_surface_report.json` | Counts, frequencies, excerpt policy, reconciliation hints |

| Contract | Path |
| -------- | ---- |
| Runtime contract v1 | `docs/runtime/replay_explorer_surface_v1.md` |

| CLI | Command |
| --- | ------- |
| Emitter | `python -m starlab.explorer.emit_replay_explorer_surface` |

## Upstream inputs (consume only)

- Governed **M14** bundle directory (manifest + M09–M13 JSON already in bundle contract).
- Frozen **M30** `replay_hierarchical_imitation_agent.json` via `--agent-path`.
- **M16 → M18** in-process materialization via `starlab.imitation.replay_observation_materialization` (same seam as M27/M30).
- **M29** trace validation via `starlab.hierarchy.hierarchical_interface_schema.validate_hierarchical_trace_document`.

**Import rule (M31 explorer modules):** no direct `starlab.replays`, `starlab.sc2`, or `s2protocol` imports — bundle JSON is read as files; materialization uses allowed seams.

## Selection policy

- **ID:** `starlab.m31.selection.slice_anchor_v1`
- **Panel order:** slices sorted by `(start_gameloop ascending, slice_id ascending)`.
- **Anchor:** `anchor_gameloop = (start_gameloop + end_gameloop) // 2` (integer midpoint).
- **`--max-panels`:** default **5**; optional `--slice-id` filters to one slice.

## Bounded excerpts (fixed in contract)

Declared in `docs/runtime/replay_explorer_surface_v1.md` — timeline **8**, economy **6**, combat/scouting **6**; one M16 + one M18 frame at anchor; truncation ordering is deterministic.

## Product layout

```
starlab/explorer/
  replay_explorer_models.py
  replay_explorer_selection.py
  replay_explorer_builder.py
  replay_explorer_io.py
  emit_replay_explorer_surface.py
tests/fixtures/m31/   # goldens + optional inputs
tests/test_replay_explorer_surface.py
```

## Required tests (minimum)

1. Model / IO deterministic serialization  
2. Selection policy determinism (order shuffle in → same panels)  
3. Bounded excerpt determinism  
4. M29 trace compatibility on emitted traces  
5. End-to-end CLI on fixtures  
6. Golden / snapshot JSON comparison  
7. AST import guard on listed explorer modules  
8. Report consistency with surface  
9. `non_claims` preserved on surface + report  

## Acceptance criteria

- Deterministic `replay_explorer_surface.json` + report from governed fixture inputs  
- Panels follow `slice_anchor_v1`; each includes excerpts + M30 trace validated to M29  
- No forbidden imports in explorer modules  
- CI green  
- `docs/starlab.md` updated for M31 chartering (artifacts, glossary, Phase V compact row fix for **M30**)  
- **M32** remains out of scope for product code in this milestone  

## CI / governance

- No new broad CI matrix; add only guards/tests required by M31.  
- Do not weaken existing checks.

## Closeout (after merge + green CI; separate commits per project rules)

- `M31_run1.md`, `M31_summary.md`, `M31_audit.md` under `docs/company_secrets/milestones/M31/`  
- Update `M31_plan.md` status; ledger §6–§8, §10–§11, §18, §20, §23  
- Tag `v0.0.31-m31`  
- **M32** stub only: `M32_plan.md`, `M32_toolcalls.md`  

---

## Status

**Complete on `main`** — merged [PR #37](https://github.com/m-cahill/starlab/pull/37) (merge commit `41d62056e1956627b63152221932dc9c2423429c`; **authoritative PR-head CI** [`24225153475`](https://github.com/m-cahill/starlab/actions/runs/24225153475); **merge-boundary `main` CI** [`24226308356`](https://github.com/m-cahill/starlab/actions/runs/24226308356)); closeout docs `M31_run1.md`, `M31_summary.md`, `M31_audit.md`; ledger `docs/starlab.md` updated; **M32** stubs only.

---

*Plan adapted from M31 charter; preserves M30-reserved narrow proof and explicit non-claims.*
