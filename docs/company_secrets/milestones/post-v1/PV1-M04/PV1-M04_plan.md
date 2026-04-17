# PV1-M04 — Post-Campaign Analysis / Comparative Readout

**Status:** **Implementation aligned with locked intent** — public ledger (`docs/starlab.md`) updated to **`current milestone` = `PV1-M04` — `open`** on **`main`** with this milestone’s implementation PR (**record PR number + CI run IDs at merge**). This file is the **canonical private plan** for PV1-M04; earlier planning sections below are **retained** for history.  
**Title:** **PV1-M04 — Post-Campaign Analysis / Comparative Readout**  
**Branch:** `pv1-m04-post-campaign-readout` (recommended)

**Grounding campaign (reference):** the PV1 industrial campaign that completed **PV1-M02** + **PV1-M03** with **`campaign_id`** **`pv1_m02_tranche_a_2026_04_16`**, **`pv1_m02_exec_001`** (Tranche A) + **`pv1_m03_exec_001`** (Tranche B), and honest **`threshold-not-met`** on the frozen **`full_run_duration_target`**. PV1-M04 **does not** re-execute that campaign; it **reads** archived operator-local trees and public contracts.

---

## A. Milestone purpose

- **Optional** post-campaign milestone after **PV1-M03** is **closed** on `main`, when the program wants a **single governed readout** that:
  - **Summarizes** what the PV1 campaign **actually achieved** under sealed contracts (not aspirations).
  - **Packages** Tranche A + Tranche B + **threshold outcome** into one **coherent comparative narrative** — separating **tranche execution posture** from **full-run threshold posture** (same separation as PV1-M03 closeout).
  - Stays **bounded and honest**: analysis and synthesis only; **no** new training, no new live SC2 runs required for milestone completion.
  - **Does not** stealth-widen v1-preserved boundaries: no new claims of global benchmark integrity, universal replay↔execution equivalence, ladder/public strength, live SC2 in CI as merge norm, or multi-environment readiness.

---

## B. Exact scope

### B.1 Milestone shape: **mixed** (documentation + optional thin tooling)

| Layer | In scope | Out of scope |
| --- | --- | --- |
| **Documentation (primary)** | **`docs/runtime/pv1_post_campaign_readout_v1.md`** — readout contract, inputs, outputs, non-claims. | Prose that implies **threshold-met** or new product proof. |
| **Tooling (small)** | **`python -m starlab.training.emit_pv1_post_campaign_readout`** → **`pv1_post_campaign_readout.json`** + **`pv1_post_campaign_readout_report.json`** — **aggregation only**, composes PV1-M01 index + operator markdown pointers. | Heavy analytics, ML on replays, auto-“grading” of operator judgment. |
| **Repo / governance** | Minimal **fixture tests** if a new emitter exists; **ledger tests** only when milestone is **opened/closed** via normal PR (not this planning pass). | Operator-local trees committed to `main`. |

**Decision for implementers:** Either **(1)** docs-only readout (markdown template + checklist) **or** **(2)** docs + **one** small emitter that composes **existing** artifacts (`campaign_observability_index*.json`, `hidden_rollout_campaign_run.json` pointers, operator note paths) into **`pv1_campaign_readout.json`** / **`pv1_campaign_readout_report.json`** with explicit **`non_claims`** field — mirroring PV1-M01 patterns.

### B.2 In scope (PV1-M04)

- **Comparative readout** across:
  - **Tranche A vs Tranche B** — execution ids, phase shapes, bootstrap episode counts, M51 tail (refit / M42 skip / watchable M44) where present.
  - **Execution completeness vs threshold outcome** — e.g. both tranches “within scope” vs **`threshold-not-met`** on **`full_run_duration_target`** (and any other threshold fields explicitly declared in `full_run_threshold_declaration.md`).
  - **Checkpoint / evidence completeness** — PV1-M01 **`index_status`**, checkpoint receipt counts/locations (including subdirectory preservation pattern `checkpoints/tranche_a_close/`, `checkpoints/tranche_b_close/`).
  - **Operator decision trail** — pointers to `tranche_a_operator_note.md`, `tranche_b_operator_note.md`, `full_run_threshold_declaration.md` (content not fabricated; readout cites paths + key enumerated fields).
  - **Watchable validation footprint** — counts/paths from observability scan + `local_live_play_validation_run.json` refs per execution (presence/layout level; same honesty as PV1-M01).
  - **Bounded lessons** — explicit “what we learned” / “what remains” for **later PV1** or **v2** planning, labeled as **hypotheses and governance lessons**, not empirical generalization beyond this campaign.

### B.3 Out of scope

- **New** campaign execution, re-runs, or “fixing” **`threshold-not-met`**.
- Claiming **global** benchmark integrity, **universal** replay↔execution equivalence, ladder/public performance, **live SC2 in CI** as default merge gate.
- **PV1-M05** or v2 charter execution.
- Committing raw `out/` campaign trees to `main` (unless project policy explicitly changes).

---

## C. Readout targets (what to compare or summarize)

1. **Tranche A vs Tranche B (structural):** protocol phases completed/skipped; `execution_id`; skip-bootstrap continuation semantics (`skip_bootstrap_phases_prior_tranche_completed_in_other_execution`).
2. **Tranche posture vs threshold posture:** restate **completed within scope** for each tranche vs **`threshold-not-met`** and **which** threshold field(s) failed (duration only vs others — must match `full_run_threshold_declaration.md`).
3. **Evidence completeness:** observability index summary (`execution_count`, `checkpoint_receipt_count`, `watchable_validation_count`, `index_status`); checkpoint receipt layout.
4. **Operator trail:** ordered references to operator notes + threshold declaration (no rewriting history).
5. **Watchable / replay footprint:** per-tranche presence of watchable phase + replay bindings (from index scan).
6. **Bounded lessons:** 3–7 bullets max — e.g. continuity across sessions, env probe discipline (`STARLAB_SC2_BIN`), governance value of separating tranche success from full-run threshold — **explicitly not** statistical or ladder claims.

---

## D. Required evidence inputs (minimum set PV1-M04 consumes)

| Source | Artifacts |
| --- | --- |
| **PV1-M02 surfaces** | `docs/runtime/pv1_tranche_a_execution_evidence_v1.md`; operator **`tranche_a_operator_note.md`**; `campaign_runs/pv1_m02_exec_001/hidden_rollout_campaign_run.json` |
| **PV1-M03 surfaces** | `docs/runtime/pv1_tranche_b_full_run_threshold_evidence_v1.md`; **`tranche_b_operator_note.md`**; **`full_run_threshold_declaration.md`**; `campaign_runs/pv1_m03_exec_001/hidden_rollout_campaign_run.json` |
| **PV1-M01** | `campaign_observability_index.json` + `campaign_observability_index_report.json`; `tranche_checkpoint_receipt.json` (+ reports) under campaign root and/or `checkpoints/tranche_a_close/`, `checkpoints/tranche_b_close/` |
| **M49** | `full_local_training_campaign_contract.json`, `campaign_preflight_receipt.json` |
| **Ledger / governance** | `docs/starlab.md` (quick scan, §11 PV1 stubs, §23 changelog entries for PV1-M02/M03); optional private PV1-M03 closeout artifacts for narrative consistency |
| **Fixtures (CI only)** | Extend **`tests/fixtures/pv1_m01`**-style pattern or add **`tests/fixtures/pv1_m04_readout/`** with a **minimal synthetic tree** if an emitter is added — **no** live SC2 |

---

## E. Honest non-claims (binding for PV1-M04)

PV1-M04 **still does not** prove or imply:

- Global **benchmark integrity** or ranking validity beyond this campaign’s sealed scope.
- **Universal** replay↔execution equivalence or gameplay-semantic guarantees.
- **Ladder / public** strength or deployability.
- **Live SC2 in CI** as default merge norm or global proof.
- **Multi-environment** readiness or transfer.
- That **`threshold-not-met`** was “wrong” or that duration semantics can be reinterpreted without a **new charter / governance decision**.

Readout may cite **PV1-M01** counts as **layout/presence** only — same non-claims as `pv1_campaign_observability_checkpoint_discipline_v1.md`.

---

## F. Repo / documentation changes required (when milestone is implemented — not this planning pass)

| Surface | Change |
| --- | --- |
| **`docs/starlab.md`** | **Only** when PV1-M04 is **opened/closed** via governance PR: quick scan, §11 stub, roadmap row, §23 changelog — **current milestone None** until explicitly opened. |
| **Runtime docs** | New **`docs/runtime/pv1_post_campaign_readout_v1.md`** (or equivalent name): purpose, inputs, output schema (if any), non-claims, relationship to PV1-M01–M03 docs. |
| **`starlab.training`** (optional) | Thin emitter module + CLI entry point; reuse `pv1_campaign_observability_scan` / views where possible — **no** duplicate campaign execution logic. |
| **Governance tests** | If ledger language changes: extend **`tests/test_governance_ci.py`** patterns; if emitter added: **fixture-only** tests under `tests/test_pv1_campaign_readout.py` (mirroring `test_pv1_campaign_observability.py`). |
| **Fixtures** | `tests/fixtures/pv1_m04/` minimal campaign tree for emitter tests. |

---

## G. Validation / CI posture

- **Ruff / mypy / pytest** on touched Python; **fixture-only** paths for any new emitter.
- **No** operator-local execution in CI; **no** live SC2; **no** GPU training.
- Governance tests: **ledger substring** checks only when milestone is formally opened/closed in a future PR.
- Optional: **determinism test** — same campaign fixture → same readout JSON hash (if emitter emits canonical JSON like PV1-M01).

---

## H. Closeout expectations (if PV1-M04 is implemented and closed)

- **Private (committed under `docs/company_secrets/milestones/post-v1/PV1-M04/`):** `PV1-M04_run1.md`, `PV1-M04_summary.md`, `PV1-M04_audit.md` per project prompts; `PV1-M04_toolcalls.md` filled with CI run IDs.
- **Public:** §23 changelog + §11 section **closed**; runtime doc header aligned.
- **Workflow:** Authoritative **PR-head CI** + **merge-boundary `main` CI** recorded in changelog (same discipline as PV1-M03 closeout).

---

## I. Reuse vs invent (substrate review)

- **Reuse:** `emit_campaign_observability_index`, `emit_tranche_checkpoint_receipt`, `build_campaign_observability_index`, `scan_campaign_observability_tree` — already produce counts, refs, and `index_status`.
- **Invent only if needed:** A **readout-specific** JSON schema that **aggregates** two execution summaries + links to operator markdown paths — **not** a second observability scan with different semantics; prefer **composition** of existing JSON + explicit **`readout_non_claims`** block.

---

## J. Assessment recorded here (planning pass)

- **Worth opening:** **Yes**, if the program wants a **named, auditable** comparative readout artifact and/or runtime contract; **No**, if **ledger + existing runtime docs + private PV1-M03 closeout** are deemed sufficient and no extra JSON/checklist is needed.
- **Program decision:** proceed with **docs-first** milestone + thin emitter; ledger opens **PV1-M04** with implementation PR.

---

## K. Locked implementation intent (merge supplement)

1. **`PV1-M04_plan.md`:** Merged (this section); **not** a blind replace of prior content.
2. **Output location:** Primary input **`--campaign-root`**; default output directory = campaign root (`--output-dir` optional for CI/fixtures).
3. **Emitter:** `python -m starlab.training.emit_pv1_post_campaign_readout`.
4. **Tests:** Fully synthetic **`tests/fixtures/pv1_m04/`** only for CI — **no** committed operator **`out/`** snapshot dependence.
5. **Ledger:** **PV1 campaign outcome** line in **quick-scan** table; **canonical PV1 operator artifacts** subtable under **Post-v1 (PV1)** — **not** overloaded into quick-scan beyond the one outcome line.
6. **Bounded truth preserved** in readout synthesis: Tranche A **completed_within_scope**; Tranche B **completed_within_scope**; **`threshold-not-met`** with **`full_run_duration_target`** as declared — **no** reinterpretation.
7. **`campaign_result_summary`:** Stable **`summary_line`** + structured **`tuple`** in **`pv1_post_campaign_readout.json`** for fresh-chat recovery.

## L. Implemented surfaces (map to repo)

| Planned | In repo |
| --- | --- |
| Runtime readout contract | `docs/runtime/pv1_post_campaign_readout_v1.md` |
| Deterministic JSON pair | `pv1_post_campaign_readout.json`, `pv1_post_campaign_readout_report.json` (via emitter) |
| Emitter CLI | `starlab/training/emit_pv1_post_campaign_readout.py` |
| Builder | `starlab/training/pv1_post_campaign_readout.py` |
| Fixture tests | `tests/fixtures/pv1_m04/minimal_campaign/`, `tests/test_pv1_post_campaign_readout.py` |
| Ledger / governance | `docs/starlab.md`, `tests/test_governance_ci.py` |
