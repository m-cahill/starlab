# PX1-M00 — implementation plan

**Milestone id:** `PX1-M00`  
**Title:** Full Industrial Run & Demonstration Charter  
**Type:** Governance-first (documentation + ledger + tests). **No** operator campaign execution. **No** demo recording.

---

## Single objective

Open the **PX1** phase in the public ledger with a **durable charter**, a **public runtime document**, a **PX1 roadmap** (only **PX1-M00** open), and **explicit** separation of: industrial-run success, play-quality success, demo/video success — while preserving closed **v1** and **PV1** history.

---

## Deliverables

### Public

1. **`docs/starlab.md`**
   - **Quick scan:** `current milestone` = **PX1-M00**; compact note that **PX1** is the new post-PV1 phase; **v2** deferred until PX1 goals are resolved; **PV1** bounded outcome unchanged.
   - **Start Here:** navigation to **Post-PV1 (PX1)** after **Post-v1 (PV1)**.
   - **New top-level section** after the **Post-v1 (PV1)** block: **Post-PV1 (PX1) — Full Industrial Run & Demonstration Proof** (charter sentence, roadmap table, non-claims, “not yet earned” truths).
   - **§11 Current milestone:** **PX1-M00** as **open** charter milestone at the top; **PV1-M04**–**PV1-M00** remain **closed** subsections below.
   - **§23 Changelog:** new **PX1-M00** entry at top (recharter + roadmap addition; **no** execution).

2. **`docs/runtime/px1_full_industrial_run_demo_charter_v1.md`**  
   Public runtime charter (sections A–E per milestone spec).

### Private (`docs/company_secrets/milestones/post-v1/PX1-M00/`)

3. **`PX1-M00_plan.md`** (this file) — handoff, scope, acceptance criteria.  
4. **`PX1-M00_charter.md`** — durable phase charter text (distinct from plan).  
5. **`PX1-M00_toolcalls.md`** — tool log per `.cursorrules`.

### Tests

6. Update **`tests/test_governance_ci.py`** (and any other tests that pin “current milestone = None”) to assert **PX1-M00** as current public truth.

---

## PX1-M00 definitional content (structure, not final numbers)

### 1. Full industrial run success (schema)

**PX1-M00** specifies structure only; **PX1-M01** freezes concrete threshold values before execution.

| Element | Required content |
| --- | --- |
| **Run identity** | `campaign_id`, `execution_id` (or successor binding), linkage to M49/M50/M51 artifacts as applicable |
| **Session / boundary rules** | What counts as one continuous industrial run vs invalidating split sessions (PX1-specific; does not reinterpret closed PV1 **`threshold-not-met`**) |
| **Threshold block** | Required field **categories** (e.g. duration wall-clock bounds, phase-completion requirements, evidence completeness hooks) — **values TBD in PX1-M01** |
| **Evidence package** | Minimum operator-authored declarations + machine-emitted JSON hooks to be listed in PX1-M01 |
| **Stop / pause / invalidation** | Operator and mechanical halt conditions |
| **Completion predicate** | What “completed industrial run” means in PX1 terms |

### 2. Play-quality success (schema)

| Element | Required content |
| --- | --- |
| **“Plays well”** | Bounded definition tied to declared metrics/surfaces (not open-ended “strong”) |
| **Evaluation surfaces** | Which harnesses/contracts may be cited (e.g. offline M28-style, M44 under declared modes) |
| **Candidate comparison** | Tie-breakers and forbidden comparisons |
| **Selected-opponent posture** | Scripted/heuristic/baselines only as declared |
| **Explicit not-proved** | No ladder universality; no cross-map generalization |

### 3. Demo / video success (schema)

| Element | Required content |
| --- | --- |
| **Valid governed demo** | Checklist: build identity, weights pointer, map/settings, opponent declaration |
| **Replay + video** | What artifacts must exist and how they bind to run identity |
| **Winning** | Literal win condition under demo contract (not “looks good”) |
| **Honesty** | No inflated cuts; no undisclosed conditions |

### 4. Phase-level non-claims

As in public runtime doc and ledger: no ladder/benchmark universality/equivalence universality/live-CI merge norm/v2 auto-readiness/superiority-from-single-demo.

---

## Acceptance criteria (definition of done)

1. Ledger introduces **PX1** without damaging closed **v1** / **PV1** narratives.  
2. **`current milestone` = PX1-M00**; **PX1-M01**–**M04** appear as planned, not opened.  
3. Runtime charter file exists and is coherent.  
4. Private folder contains **plan**, **charter**, **toolcalls**.  
5. Public roadmap table present under **Post-PV1 (PX1)**.  
6. Plan distinguishes three success classes clearly.  
7. **No** new execution/training code in this milestone (tests/docs only).  
8. **`ruff check starlab tests`**, **`mypy starlab tests`**, **`pytest`** green.

---

## Suggested branch / PR

- Branch: `px1-m00-full-industrial-run-demo-charter`  
- PR title: `docs(governance): charter PX1 full industrial run and demonstration phase`

---

## Closeout (after merge + green CI)

Per workflow: run workflow analysis, summary, and audit prompts; state explicitly: PX1 is new post-PV1; no execution in PX1-M00; later PX1 milestones unopened.
