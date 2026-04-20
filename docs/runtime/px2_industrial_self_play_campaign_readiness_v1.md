# PX2 Industrial Self-Play Campaign — Readiness / Preflight (v1)

**Contract type:** Public runtime / governance decision record (preflight only).  
**Milestone context:** Between **closed** **PX2-M02** (replay-bootstrap) and **opening** **PX2-M03** (industrial self-play campaign).

---

## 1. Purpose

This document is a **short, bounded readiness pass**: it records what was reviewed and whether **PX2-M03** may be **opened** on `main` as the **current milestone** without implying that a Blackwell-class campaign has run or that self-play evidence exists.

**PX2-M03 requires a positive readiness/preflight decision after PX2-M02; it does not auto-open merely because PX2-M02 closed.**

---

## 2. Inputs reviewed

| Input | Role |
| ----- | ---- |
| `docs/runtime/px2_autonomous_full_game_agent_charter_v1.md` | Phase charter; industrial campaign rules; promotion ladder |
| `docs/runtime/px2_full_terran_runtime_action_surface_v1.md` | **PX2-M01** Terran core v1 — actions, legality, `compile_terran_action` |
| `docs/runtime/px2_neural_bootstrap_from_replays_v1.md` | **PX2-M02** replay-bootstrap — policy substrate, eval posture |
| `docs/runtime/full_local_training_campaign_v1.md` (M49) | Campaign charter vocabulary, phases, preflight discipline |
| `docs/runtime/industrial_hidden_rollout_mode_v1.md` (M50) | Hidden rollout execution + supervision patterns |
| M51 post-bootstrap orchestration (see M49/M50 docs and §7 Phase VI table in `docs/starlab.md`) | Phase receipts, optional weighted refit path — **governance reference** for PX2-M03 |
| `docs/starlab.md` | Public ledger truths, PX2 roadmap, current milestone |

---

## 3. Readiness dimensions

### 3.1 Policy → runtime handoff

**PX2-M02** delivers a **`torch`** **`BootstrapTerranPolicy`** trained offline; actions are expressed as **`TerranAction`** and evaluated with **legality-aware decode** and **`compile_terran_action`** on **M01** snapshots. That is a **credible** handoff path for feeding learned logits into the governed runtime for future live or self-play loops.

**Posture:** The **semantic** chain (M18/M16 → features → policy → `TerranAction` → compile) is **governed and tested** at fixture scale. Wiring that policy into a **long-running** self-play driver is **PX2-M03 implementation work**, not proved by M02 alone.

### 3.2 Campaign substrate reuse (M49 / M50 / M51)

The v1 **M49–M51** stack (`full_local_training_campaign`, `execute_full_local_training_campaign`, post-bootstrap phases) provides **useful governance patterns**: checkpoint/receipt discipline, campaign directory layout, phased execution, operator-local **`out/`** trees, and separation of **fixture CI** vs **local GPU** work.

**Direct executor compatibility** with the **PX2 `torch`** policy loop and **sklearn-era** M41/M43/M45 pipelines is **not yet proved**. That is a **known implementation gap for PX2-M03**, not a blocker to **opening** the milestone: **reuse the governance discipline, not necessarily the exact executor unchanged.**

### 3.3 Checkpoint / eval / promotion / rollback (opening sketch)

The PX2 charter (§9) requires resumable checkpoints, periodic eval, retention, promotion/rollback rules, and artifact discipline. For **opening** PX2-M03, the **minimum planned posture** is:

| Concept | Opening-level intent |
| --- | --- |
| **Checkpoint cadence** | Time- and/or step-bounded saves of policy weights + run metadata under a declared campaign root (`out/` or equivalent); resumable restarts |
| **Eval cadence** | Periodic fixed-protocol matches vs a declared eval snapshot pool (not ladder proof) |
| **Promotion** | Explicit rule for “candidate becomes primary train weight” (e.g. eval win-rate vs prior + no regression gates) — **PX2-M04** refines promotion/exploit closure |
| **Rollback** | Ability to revert to last promoted checkpoint if eval or collapse signals fail |
| **Operator-local artifacts** | Weights, configs, eval JSON/reports, operator notes — **not** default merge-gate CI |

This is **concrete enough to govern M03 honestly**; full contract JSON and automation are **in-milestone** obligations.

### 3.4 Opponent pool / anti-collapse (stub — partial)

**PX2-M02** has a **single** bootstrap policy — no league or rotating opponent pool yet. The charter still requires **bounded self-play** with **opponent pool** and **anti-collapse** posture for the industrial regime.

**Minimum opening rules (stub, not full implementation):**

- **Snapshot pool:** retain **N** frozen policy checkpoints (including M02 bootstrap) as opponents; versioned ids in campaign config.
- **Self-play opponent selection:** mix **self** (current policy), **frozen snapshots**, and optional **scripted** baselines where declared — rotation schedule TBD in M03 implementation.
- **Anti-collapse guardrails:** monitor collapse metrics (e.g. action entropy, build diversity, eval vs prior); **halt or rollback** on scripted thresholds; log warnings per **M47-style** distinctness discipline where applicable.

**Posture:** **Partial** — requirement is **recognized and framed**; **implementation** is **PX2-M03** scope.

### 3.5 Dependency / security / environment

**`torch`** is pinned **`>=2.8,<3`**; **CI** runs **pip-audit**; **Python 3.11** locked. **Blackwell** remains **operator-local** intent per ledger — **not** default CI. No new blocker identified for **opening**; ongoing obligation to keep dependencies audit-clean on bumps.

### 3.6 Artifact discipline (operator-local outputs)

Follow existing **local-first** norms: large weights and campaign trees under **`out/`** (gitignored by convention); **governed JSON** for eval and receipts where emitters exist; **no** claim that merge-gate CI reproduces industrial runs.

---

## 4. Decision table

| Dimension | Current posture | Ready? | Notes | Blocker? |
| --------- | ---------------- | ------ | ----- | -------- |
| Policy → runtime handoff | M02 policy + M01 compile path; fixture-tested | **yes** | Long-run driver wiring is M03 work | — |
| Campaign substrate (M49–M51) | Strong governance reference; not torch/sklearn-unified | **yes** | **Known gap:** new adapter/executor for PX2 — **not** a no-open blocker | — |
| Checkpoint / eval / promotion / rollback | Charter + opening sketch above | **yes** | Full automation in M03 | — |
| Opponent pool / anti-collapse | Stub rules only; not implemented | **partial** | Carried into M03 implementation | — |
| Dependency / security / env | torch pin; pip-audit; local GPU posture | **yes** | Maintain on changes | — |
| Artifact discipline | Ledger + `out/` conventions | **yes** | Operator discipline | — |

---

## 5. Opening rule

- If **no dimension** is **“not ready”** in a way that would make **opening PX2-M03 misleading**, and **partial** rows are **explicitly** carried as **M03 obligations**, then **PX2-M03 may be opened** on `main` as the **current milestone**.
- If a **credible blocker** appeared (e.g. no path from policy to `TerranAction` at all), **PX2-M03** would remain **planned only**.

**Readiness verdict (this pass):** **Ready to open PX2-M03**, with **campaign implementation obligations explicitly carried into the milestone** (including opponent-pool/anti-collapse implementation and any PX2-native campaign executor).

---

## 6. Non-claims

- **Not** industrial self-play **execution** or Blackwell **evidence**
- **Not** strength, ladder, or benchmark proof
- **Not** automatic **PX2-M04** / **v2** / **PX1-M05** opening
- **Not** a substitute for operator-local campaign artifacts
