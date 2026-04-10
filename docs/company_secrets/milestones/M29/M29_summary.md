# Milestone Summary — M29: Hierarchical Agent Interface Layer

**Project:** STARLAB  
**Phase:** V — Learning Paths, Evidence Surfaces, and Flagship Proof  
**Milestone:** M29 — Hierarchical Agent Interface Layer  
**Timeframe:** 2026-04-09 — 2026-04-10 (merge)  
**Status:** **Closed on `main`** ([PR #35](https://github.com/m-cahill/starlab/pull/35); merge commit `187d9ddd8e6b5234245923200c3a396d602e7b06`; **authoritative PR-head** [`24221769054`](https://github.com/m-cahill/starlab/actions/runs/24221769054); **merge-boundary `main`** [`24221791088`](https://github.com/m-cahill/starlab/actions/runs/24221791088))

## 1. What M29 proved

M29 proves a **contract-first**, **offline**, **frame-scoped**, **two-level** (manager → worker) hierarchical trace document with:

* Deterministic primary artifacts **`hierarchical_agent_interface_schema.json`** and **`hierarchical_agent_interface_schema_report.json`** (emit CLI + validation tests).
* Runtime contract **`docs/runtime/hierarchical_agent_interface_v1.md`**.
* Worker response carries **`semantic_coarse_label`** in an **M29-owned** coarse semantic enum aligned **1:1** with **`starlab.m26.label.coarse_action_v1`**, plus **`label_policy_id`** on the worker response.

**M30** remains the first milestone allowed to instantiate a **learned hierarchical agent**; M29 adds **no** M30 product code.

## 2. Primary artifacts

| Artifact | Role |
| -------- | ---- |
| `hierarchical_agent_interface_schema.json` | JSON Schema for the hierarchical interface trace |
| `hierarchical_agent_interface_schema_report.json` | Deterministic validation report |

## 3. Scope discipline

* Contract-first only; offline only; frame-scoped only; two-level hierarchy only.
* No training; no benchmark semantics; no live SC2 execution claims.
* No raw action or legality semantics.

## 4. Delivered (implementation)

* `starlab/hierarchy/` (`hierarchical_interface_models.py`, `hierarchical_interface_schema.py`, `hierarchical_interface_io.py`, `emit_hierarchical_agent_interface.py`)
* `tests/fixtures/m29/`, `tests/test_hierarchical_agent_interface.py`
* Governance: `docs/runtime/hierarchical_agent_interface_v1.md` listed in `tests/test_governance.py`

## 5. Explicit non-claims

* **No** learned hierarchical agent (reserved for **M30**).
* **No** benchmark integrity or tournament semantics.
* **No** live SC2 substrate claims.
* **No** raw action / legality semantics.

## 6. Next milestone

**M30** — First Learned Hierarchical Agent — **stub-only** (`M30_plan.md`, `M30_toolcalls.md`) until chartered.

---

*Summary structure aligned with project milestone practice; CI evidence cross-checked with `docs/company_secrets/prompts/workflowprompt.md` and ledger §18 / §23.*
