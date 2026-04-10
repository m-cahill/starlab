# M29 Plan — Hierarchical Agent Interface Layer

**Milestone:** M29 — Hierarchical Agent Interface Layer  
**Tag target:** `v0.0.29-m29`  
**Recommended branch:** `m29-hierarchical-agent-interface-layer`  
**Recommended PR title:** `M29: hierarchical agent interface layer`  
**Status:** **Complete** (product on branch; merge PR + `main` CI merge authority pending — record in ledger §18 / §23)

## Objective

Prove the first **deterministic, offline, governed hierarchical interface contract** for STARLAB.

M29 defines a small, machine-readable interface layer for a **two-level hierarchy**:

- a **manager** layer that selects a delegate / option  
- a **worker** layer that returns a bounded semantic decision  

This milestone is **contract-first**, not capability-first. It creates the interface surface that **M30** can later instantiate with the first learned hierarchical agent.

## Scope decisions (locked)

- **Exactly two levels in v1:** one manager, one worker.  
- **Offline only:** no live SC2 execution, no runtime action legality claims.  
- **Frame-scoped only:** one hierarchical decision contract per replay-derived frame / decision point.  
- **No training in M29:** the interface exists before the learned hierarchical agent.  
- **No benchmark semantics in M29:** this is not an evaluation milestone.  
- **Worker output** terminates in an **M29-owned** JSON Schema enum aligned **1:1** with **`starlab.m26.label.coarse_action_v1`** (same set as M26 `target_semantic_kind`); **`label_policy_id`** on `worker_response` anchors the policy family without coupling validation to a particular M27 artifact.  
- **No multi-worker routing** beyond one selected delegate in v1.  
- **No tournament / diagnostics / evidence-pack widening.**  
- **No M30 product code.**

## Primary artifacts

| Artifact | Version string |
| -------- | -------------- |
| `hierarchical_agent_interface_schema.json` | `starlab.hierarchical_agent_interface_schema.v1` |
| `hierarchical_agent_interface_schema_report.json` | `starlab.hierarchical_agent_interface_schema_report.v1` |
| Trace document root `schema_version` | `starlab.hierarchical_agent_interface_trace.v1` |

JSON Schema `$defs`: `frame_ref`, `delegate_descriptor`, `manager_request`, `manager_response`, `worker_request`, `worker_response`, `hierarchical_decision_trace`.

## Product layout (implemented)

- `docs/runtime/hierarchical_agent_interface_v1.md`  
- `starlab/hierarchy/hierarchical_interface_models.py`  
- `starlab/hierarchy/hierarchical_interface_schema.py`  
- `starlab/hierarchy/hierarchical_interface_io.py`  
- `starlab/hierarchy/emit_hierarchical_agent_interface.py`  
- `tests/test_hierarchical_agent_interface.py`, `tests/fixtures/m29/`  

**Import guard:** no `starlab.replays`, `starlab.sc2`, `s2protocol` in listed M29 `starlab/hierarchy/` product modules (AST-tested).

## CLI

```bash
python -m starlab.hierarchy.emit_hierarchical_agent_interface --output-dir OUT
```

## Out of scope / non-claims

First learned hierarchical agent; training; benchmark integrity; leaderboard validity; live SC2; replay↔execution equivalence; raw SC2 action legality; multi-step planning proof; >2 hierarchy levels; tournament/diagnostics/evidence-pack semantics; M30 product code.

## Closeout

- `docs/starlab.md` updated (merge authority fields pending until PR merges)  
- `M29_run1.md`, `M29_summary.md`, `M29_audit.md`  
- **M30** stubs only (`M30_plan.md`, `M30_toolcalls.md`)
