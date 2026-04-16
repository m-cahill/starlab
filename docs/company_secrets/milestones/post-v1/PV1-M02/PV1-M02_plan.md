# PV1-M02 — Tranche A Execution Evidence

**Status:** **Implementation in progress** — public ledger updated on branch `pv1-m02-tranche-a-execution-evidence` (integration PR → `main`).  
**Title:** **PV1-M02 — Tranche A Execution Evidence**  
**Branch:** `pv1-m02-tranche-a-execution-evidence`

**Kickoff freeze (2026-04-16):** `campaign_id` **`pv1_m02_tranche_a_2026_04_16`**; `execution_id` **`pv1_m02_exec_001`**; `tranche_id` **`tranche_a`**; `checkpoint_id` **`tranche_a_close`**; `runtime_mode` **`local_live_sc2`** (requires **`STARLAB_SC2_ROOT`**); M51 **`--post-bootstrap-protocol-phases`** **in scope**; operator note **`tranche_a_operator_note.md`** at campaign root.

**Operator-local evidence:** `out/training_campaigns/pv1_m02_tranche_a_2026_04_16/` — **not** committed; execution **completed** with PV1-M01 index/checkpoint **`complete`**.

---

## A. Milestone purpose

- **First substantive post-v1 execution milestone** under **PV1 — Long Industrial Campaign & Scaling Evidence** (`PV1-MNN`, **not** M62, **not** “Phase VIII”).
- Produce **honest, artifact-backed evidence** that a **Tranche A** slice of a governed campaign was **actually executed** under the existing **M49 → M50 → (optional M51)** machinery — not merely chartered or preflighted.
- Remain **bounded**: evidence is **operator-local** and **campaign-scoped**; it does **not** upgrade global claims preserved since v1 (benchmark integrity, universal replay↔execution equivalence, ladder/public strength, merge-gate live SC2).
- **Depends on PV1-M01** only as **inspection helpers** — PV1-M01 did **not** execute a campaign; PV1-M02 is where **execution evidence** appears if the operator run completes and is archived honestly.

---

## B. Exact scope

### B.1 Milestone shape: **mixed** (repo + operator-local)

| Layer | Role |
| --- | --- |
| **Operator-local (primary proof)** | Run `execute_full_local_training_campaign` (and optional M51 phases per charter) for a **declared** campaign id; archive outputs under `out/training_campaigns/<campaign_id>/` with stable `campaign_runs/<execution_id>/` trees. |
| **Repo (governance + auditability)** | Tighten **documentation** and **minimal tests** so Tranche A closeout is **checklist-defensible**: what files must exist, what “Tranche A complete” means vs “not complete,” and how PV1-M01 emitters fit the review path. **No** default CI execution of live SC2 or long campaigns. |

### B.2 Definition of **Tranche A** (for PV1-M02)

Operational definition for this milestone (to be fixed in charter text before execution):

- **Tranche A** = the **first substantive** `bootstrap_episodes` (or equivalent) **protocol phase block** that the operator treats as “Tranche A” in the M49 `campaign_protocol` (commonly the phase named `tranche_a` in the default protocol, or an explicitly named equivalent in a custom `--campaign-protocol-json`).
- Evidence must tie to **one** primary **`execution_id`** under `campaign_runs/<execution_id>/` that **covers** completion of that phase’s planned work **or** documents **honest** `paused` / `incomplete` / `failed` posture with receipts (no silent gaps).
- **Campaign identity** = `campaign_id` from `full_local_training_campaign_contract.json` + `campaign_sha256`.  
- **Tranche identity** = operator-declared label (e.g. `tranche_a`) consistent with protocol phase naming and **checkpoint receipts** / notes.

### B.3 In scope (PV1-M02)

- At least one **governed operator-local** run that **intends** to complete Tranche A under a sealed M49 contract (or explicit documented partial outcome with honest artifacts).
- **Emit / archive** (under the campaign root, not necessarily in git):
  - `full_local_training_campaign_contract.json` + `campaign_preflight_receipt.json`
  - `campaign_runs/<execution_id>/hidden_rollout_campaign_run.json` (+ report), manifest, heartbeat/resume as applicable
  - Per-phase **`phase_receipt.json`** where M51 paths apply
  - **Replay bindings** and **M44** watchable validation artifacts **where the campaign contract and protocol require them** for Tranche A closure
  - **PV1-M01**: `campaign_observability_index.json` (+ report) and at least one **`tranche_checkpoint_receipt`** at **Tranche A boundary** (`--tranche-id` / `--checkpoint-id` chosen by operator)
  - **Operator continuation/stop note** (text file under campaign root or referenced path, e.g. `OPERATOR_TRANCHE_A_CLOSEOUT.txt` — naming is operator convention; plan should pick one canonical name in runtime doc)
- **Repo deliverables** (implementation milestone, not this planning pass):
  - Runtime doc update (new or extended): **`docs/runtime/pv1_tranche_a_execution_evidence_v1.md`** (or a clearly named sibling) describing the **minimum evidence package**, **closeout checklist**, and **non-claims**
  - `docs/starlab.md` updates **when the milestone is opened/closed** via normal governance (not during planning-only passes)
  - **Minimal** governance tests that lock **ledger language** when PV1-M02 is **open/closed** (pattern: `test_governance_ci.py` PV1 rows)
  - Optional: thin **fixture** test that proves **checklist / path binding** logic only — **no** live SC2 in CI

### B.4 Out of scope (PV1-M02)

- **PV1-M03** / **PV1-M04** / full-run threshold satisfaction
- Tranche B or “full campaign” completion
- New benchmark-integrity or equivalence **proofs**
- Live SC2 **in default merge CI**
- Committing large `out/` trees or raw replays to `main` (paths + hashes in summary/audit only, unless project policy explicitly allows)

---

## C. Required evidence package (minimum)

Align with **PV1-M00** §11 evidence classes and **PV1-M01** default presence checks. For Tranche A **close**, the following must be **demonstrable** from archived artifacts (operator-local; reviewer can reproduce layout checks via PV1-M01):

| # | Evidence class | Typical artifacts / refs |
| --- | --- | --- |
| 1 | Campaign identity / contract | `full_local_training_campaign_contract.json` at `out/training_campaigns/<campaign_id>/` |
| 2 | Preflight | `campaign_preflight_receipt.json` (and execution preflight if used: `campaign_execution_preflight_receipt.json`) |
| 3 | Execution summary | `campaign_runs/<execution_id>/hidden_rollout_campaign_run.json` + report; execution manifest |
| 4 | Phase receipts | `**/phase_receipt.json` for executed phases in scope; aggregate on run v2 when applicable |
| 5 | Tranche checkpoint | PV1-M01 **`tranche_checkpoint_receipt.json`** for Tranche A boundary (e.g. tranche close) |
| 6 | Observability index | PV1-M01 **`campaign_observability_index.json`** showing inventory + `index_status` honest vs missing |
| 7 | Watchable validation | At least one **`local_live_play_validation_run.json`** **if** Tranche A protocol includes operator-review surfaces per charter / M51 (charter: at least one per closed tranche when beyond offline-only — document exact expectation for this run) |
| 8 | Replay binding | **`replay_binding.json`** where contract binds lineage for episodes in scope |
| 9 | Operator gate | Explicit **continue / pause / stop** note with rationale |
| 10 | Tranche A posture | Operator statement: **Tranche A completed** vs **not completed** (paused / failed / incomplete), **without** claiming full-run threshold |

**Threshold posture:** PV1-M02 **does not** require meeting the **full training run** block in PV1-M00 §8 unless explicitly deferred to PV1-M03; it **does** require a clear **Tranche A** outcome statement.

---

## D. Honest non-claims (PV1-M02)

PV1-M02 **still does not** prove:

- Global or universal **benchmark integrity**
- **Replay↔execution equivalence** (gameplay-semantic or universal)
- **Ladder / public** strength
- **Live SC2 in CI** as merge norm
- Statistical **significance** of learning
- That Tranche A success **generalizes** beyond the chartered campaign
- **Full-run** or **PV1-M03** threshold satisfaction

---

## E. Repo / documentation changes (when milestone is implemented — not now)

| Area | Change |
| --- | --- |
| **`docs/starlab.md`** | When opening: set **current milestone** to PV1-M02; roadmap row **open**; §11 stub; §23 changelog. When closing: flip to **closed** with PR + CI IDs; **current milestone** → **None** or next placeholder; **do not** open PV1-M03 unless chartered. |
| **Runtime** | Add **`docs/runtime/pv1_tranche_a_execution_evidence_v1.md`** (or agreed name): evidence package, naming conventions for operator notes, pointer to M49/M50/M51 + PV1-M01. |
| **Tests** | Governance tests for ledger strings; optional fixture tests for checklist helpers only. |
| **`docs/company_secrets/.../PV1-M02/`** | `PV1-M02_runN.md`, `PV1-M02_summary.md`, `PV1-M02_audit.md` at closeout. |

**Planning-only constraint:** **No** `docs/starlab.md` edit in the planning pass that opens PV1-M02.

---

## F. Validation / CI posture

| Check | Where |
| --- | --- |
| **Ruff / Mypy / Pytest** | Default CI — unchanged; **no** new expensive lanes. |
| **Fixture-only** | Any new tests use synthetic trees under `tests/fixtures/` — **no** live SC2. |
| **Operator-local** | Real Tranche A evidence remains **out of default CI**; documented in milestone audit. |

---

## G. Closeout expectations (when PV1-M02 is eventually merged)

- **`PV1-M02_run1.md`** (and increments if needed) — PR-head + merge-boundary CI IDs
- **`PV1-M02_summary.md`** — factual; operator campaign id / execution id as **references** (not necessarily committing secrets)
- **`PV1-M02_audit.md`** — delta audit; explicit non-claims
- **Ledger** — §1, §7 PV1 table, §11, §23
- **No** silent opening of **PV1-M03**

---

## H. Preconditions assessment — can PV1-M02 open next?

### Verdict: **No repository blocker**

**Rationale:**

- **M49** contract + preflight, **M50** executor, **M51** optional phases, and **PV1-M01** observability emitters exist on `main` and are internally consistent with `docs/runtime/full_local_training_campaign_v1.md`, `industrial_hidden_rollout_mode_v1.md`, and `pv1_campaign_observability_checkpoint_discipline_v1.md`.
- Tranche A is **defined** in charter terms (PV1-M00 §9); numeric thresholds for a **full run** remain **TBD** and belong to **later** milestones — not a prerequisite to **open** PV1-M02 for Tranche A evidence.

**Non-repo gates (must be explicit in kickoff, not invented here):**

- Operator **authorization** to spend wall-clock / compute on a real local run
- **SC2** install / `local_live_sc2` (or agreed runtime mode) available for the chosen contract
- **Frozen scope** for Tranche A (campaign id, execution id naming, phase boundaries)

**Conclusion:** PV1-M02 **can** be opened as the next substantive milestone **when** a governance PR explicitly opens it; there is **no** need to wait for additional repo machinery **solely** for planning purposes.

---

## I. Follow-on recommendations

1. **First PR when opening PV1-M02:** governance-only branch that updates **`docs/starlab.md`** + seeds runtime checklist doc **without** claiming execution evidence until operator evidence exists.
2. **Operator handoff:** single-page checklist in runtime doc linking **PV1-M01** CLI commands for pre-close and post-close scans.
3. **Optional ledger improvement (later):** when PV1-M02 closes, add a **PV1 Tranche A evidence** row under the PV1 evidence surfaces table (parallel to PV1-M01 subtable) — **not** in this planning pass.

---

## J. References (repo)

- `docs/starlab.md` — Post-v1 (PV1) section, §11, quick scan
- `docs/runtime/full_local_training_campaign_v1.md` — M49
- `docs/runtime/industrial_hidden_rollout_mode_v1.md` — M50/M51
- `docs/runtime/pv1_campaign_observability_checkpoint_discipline_v1.md` — PV1-M01
- `starlab.training.execute_full_local_training_campaign` — executor entry
- `starlab.training.emit_*` — preflight, contract, PV1-M01 index / checkpoint receipts
- `docs/company_secrets/milestones/post-v1/PV1-M00/PV1-M00_charter.md` — tranche/evidence model
