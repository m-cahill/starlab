# PV1-M00 — Post-v1 Industrial Campaign Charter & Success Criteria

## 1. Milestone identity

**PV1-M00 — Post-v1 Industrial Campaign Charter & Success Criteria**

Governance-only milestone: opens the **PV1** phase in the ledger, defines bounded charter language, full-run threshold **shape**, tranche model, evidence expectations, and operator gates — **without** executing a long industrial campaign or widening v1 non-claims.

---

## 2. Why post-v1 exists

**M00–M61** closed the **v1** program arc: a governed, replay-native, local-first SC2 research substrate, release-lock packaging, and bounded milestone evidence surfaces. That work **proved the substrate and the release-lock path** within declared scope — **not** universal benchmark integrity, universal replay↔execution equivalence, ladder/public strength, or merge-gate live SC2.

**PV1** exists to continue **governed industrial-depth use** of that **already-closed** substrate: long-horizon campaigns, explicit tranches, checkpoints, and portable evidence — under **new** post-v1 milestone IDs (**`PV1-MNN`**), not as a hidden **M62**.

---

## 3. Phase identity

**PV1 — Long Industrial Campaign & Scaling Evidence**

This is a **rechartered** phase label. It is **not** “Phase VIII” of the original v1 phase map and **not** an extension of **M00–M61** numbering.

---

## 4. One-sentence charter

**PV1** governs long-run industrial training campaigns on the closed **M49 / M50 / M51** (and related) campaign machinery with explicit tranche boundaries, checkpoint receipts, watchable validation references, and operator decision gates — **without** claiming new global proof of benchmark integrity, replay↔execution equivalence, ladder strength, live SC2 in CI as a merge norm, or multi-environment generalization.

---

## 5. Scope

- Formalize **post-v1** program identity (**PV1**, **`PV1-MNN`**).
- Define **full training run** threshold **structure** (numeric values operator-set later).
- Define **tranche** semantics (start, close, fail, pause, authorization for next tranche).
- Define **checkpoint cadence** and **evidence classes** per tranche and for a declared full run.
- Define **watchable validation** minimums and **operator decision gates** (continue / pause / stop / resume).
- Define **resumption vs invalidation** (when a run may resume under one campaign identity vs when a **new** campaign identity is required).
- Record the **PV1** roadmap publicly in `docs/starlab.md` while keeping private notes under `docs/company_secrets/milestones/post-v1/` as **non-authoritative** working surface.
- **`docs/starlab.md`** is the **only** authoritative public source for **PV1** roadmap **status**; private milestone markdown is supplementary.

---

## 6. Out of scope / explicit non-claims

PV1-M00 and the **PV1** charter **do not** by themselves establish:

| Non-claim | Meaning |
| --- | --- |
| Universal benchmark integrity | Bounded **M55–M56**-style gates do not become global claims by PV1 activity. |
| Universal replay↔execution equivalence | **M52–M54** profiles remain bounded; PV1 campaigns do not prove gameplay-semantic equivalence. |
| Ladder / public strength | **M59** is descriptive protocol/evidence — not ladder performance proof. |
| Live SC2 in CI as default merge norm | **M57–M58** remain optional / manual; PV1 does not normalize live SC2 in default CI. |
| Multi-environment generalization | SC2-first; no second-runtime or multi-game proof. |
| Stealth continuation of v1 | **No M62**; post-v1 work is **`PV1-MNN`** only. |

---

## 7. Reused substrate

PV1 **reuses** the **closed** campaign stack:

- **M49** — campaign contract + preflight (`docs/runtime/full_local_training_campaign_v1.md`).
- **M50** — governed executor, locks, visibility receipts (`docs/runtime/industrial_hidden_rollout_mode_v1.md`).
- **M51** — optional `--post-bootstrap-protocol-phases`, phase receipts, watchable **M44** path when configured.

PV1 **does not** invent a new execution engine; it **governs depth, duration, and evidence** on top of existing machinery.

---

## 8. Definition of “full training run”

A **full training run** is **not** vague “large enough.” It is met only when **all** of the following hold **simultaneously** for a **single** declared **campaign identity** (see evidence model), with thresholds filled in under **Open operator-set values** (§17):

### Full-run threshold block (structure)

| Field | Role |
| --- | --- |
| `full_run_min_tranches` | Minimum count of **completed** tranches (each with tranche-close evidence). |
| `full_run_min_completed_protocol_phases` | Minimum count of **completed** M49/M51 protocol phases **after** bootstrap (e.g. refit, watchable validation) **counted toward** the full run, as defined in the campaign contract for that run. |
| `full_run_min_checkpoint_receipts` | Minimum number of **checkpoint receipts** (artifact-backed) across the campaign. |
| `full_run_min_watchable_validations` | Minimum **watchable** **M44** (or successor) validations **referenced** in evidence. |
| `full_run_min_evidence_completeness` | Minimum **evidence completeness** score or checklist pass (operator-defined schema — e.g. all required artifact classes present and linked). |
| `full_run_scale_target` | Operator-declared **scale** target (e.g. episode count, campaign steps, or bundle volume — **one** primary scalar agreed before the run). |
| `full_run_duration_target` | Operator-declared **wall-clock** or **compute** duration target (or bracket), for planning — **not** a substitute for artifact evidence. |

**Declaration:** The operator publishes a **threshold-met** or **threshold-not-met** statement against this block at end of campaign; **CI does not** evaluate live full runs by default.

---

## 9. Tranche model

| Concept | Definition |
| --- | --- |
| **Tranche identity** | Named slice of work within one **campaign identity** (e.g. Tranche A, Tranche B), recorded in operator notes and tied to execution directories / receipts. |
| **Tranche start** | Operator **authorizes** start after preflight + prior tranche close (or campaign bootstrap for first tranche). |
| **Tranche close evidence** | Minimum set: execution summary for the tranche, checkpoint receipts as required, watchable validation references where applicable, replay-binding references where the campaign contract requires them, continuation or stop note. |
| **Next tranche authorization** | Explicit operator **continue** decision against gates (§13); **no** silent rollover. |
| **Failed / paused / incomplete** | **Failed** — halt with reason; **paused** — intentional stop with resume criteria; **incomplete** — stopped without tranche-close evidence (does not count toward full-run thresholds). |

Expected sequence (typical): **Tranche A** (first substantive long-run) → **Tranche B** (optional second wave toward full-run threshold) — exact naming may follow **`PV1-M02` / `PV1-M03`** roadmap rows.

---

## 10. Checkpoint cadence

Checkpoints are **required**:

- At **every tranche boundary** (mandatory).
- On **operator-defined wall-clock or episode boundaries** during long tranches (at least one mid-tranche checkpoint if a tranche exceeds operator-declared span between checkpoints).
- After **any** protocol phase that emits a **phase receipt** under **M51** (receipt must be archived in campaign evidence).
- Before **resume** after pause or infrastructure change (new checkpoint receipt captures state).

---

## 11. Evidence model

Required evidence **classes** (references, not necessarily committed raw bytes):

1. **Campaign identity / contract** — `full_local_training_campaign` contract + campaign id; links to `out/training_campaigns/<campaign_id>/` layout as produced by tooling.
2. **Preflight receipts** — M49 preflight / extended preflight as used by M50.
3. **Execution summary** — per execution id under `campaign_runs/<execution_id>/` (or successor paths).
4. **Tranche checkpoint receipts** — operator-named checkpoint artifacts tying identity, time, and scope.
5. **Watchable validation references** — **M44** (or explicitly chartered successor) paths + human-review note where required.
6. **Replay-binding references** — where campaign contract binds execution to replay lineage (**M03/M04** chain).
7. **Operator continuation or stop note** — explicit **continue / pause / stop** with rationale.
8. **Final declaration** — **threshold-met** or **threshold-not-met** vs §8 block.

---

## 12. Watchable validation requirements

Minimum expectations:

- At least **one** watchable validation per **closed tranche** that exercised live or operator-review surfaces when the tranche included executable phases beyond offline-only stubs.
- For **M51** post-bootstrap paths involving refit, at least **one** watchable **M44** on the **refit** weights path when refit produced a candidate — **no** silent fallback (consistent with **M51** semantics).
- Watchable artifacts must be **locatable** from the campaign evidence index (paths + hashes where applicable).

---

## 13. Operator decision gates

| Gate | Criteria (illustrative) |
| --- | --- |
| **Continue** | Preflight green; prior tranche evidence complete; resources within budget; no blocking integrity alerts in scope. |
| **Pause** | Planned stop (cost, schedule, hardware); document resume prerequisites. |
| **Stop** | Fail closure; safety; contract violation; evidence cannot be made consistent. |
| **Resume** | Allowed only per §14; may require new checkpoint before execution restarts. |

---

## 14. Allowed resumptions and invalidation conditions

**Resume under same campaign identity** when:

- PID/lock semantics and campaign contract still match; operator documents what resumed.
- No change to **training program contract** binding that would invalidate comparison claims (if comparisons are in scope for that campaign).

**New campaign identity required** when:

- **Training program contract** or benchmark contract binding changes in a way that breaks lineage.
- **Map / opponent / seed policy** changes outside the declared campaign contract amendment process.
- **Irrecoverable** evidence gap (missing lineage, corrupted execution tree) that cannot be bridged with honest receipts.

---

## 15. Success criteria (PV1-M00)

PV1-M00 succeeds when:

1. **PV1** phase and **one-sentence charter** are recorded publicly in `docs/starlab.md` with **M00–M61** preserved as closed v1.
2. **PV1-M00**–**PV1-M04** roadmap rows exist with **explicit** planned/optional/current language — **not** marked complete except **PV1-M00** as current governance milestone during charter PR.
3. This charter defines §8 threshold **shape**, §9 tranches, §10 checkpoints, §11 evidence, §13 gates, §6 non-claims.
4. **No** new product claims are introduced in CI or ledger beyond governance documentation.

---

## 16. Exit criteria for opening the next milestone

| Next milestone | Open when |
| --- | --- |
| **PV1-M01** — Campaign Observability & Checkpoint Discipline | Charter documents a **concrete, justified** tooling/observability gap that blocks honest checkpoints or receipts. |
| **PV1-M02** — Tranche A Execution Evidence | **PV1-M01** is **not** needed **or** explicitly **skipped** with recorded rationale; operator authorizes first substantive tranche under this charter. |

**PV1-M03** / **PV1-M04** open only per public roadmap intent — **not** automatically after **PV1-M02**.

---

## 17. Open operator-set values

Numeric and scalar targets — **TBD** until explicitly set for a concrete campaign (do not invent defaults here):

| Field | Status |
| --- | --- |
| `full_run_min_tranches` | TBD |
| `full_run_min_completed_protocol_phases` | TBD |
| `full_run_min_checkpoint_receipts` | TBD |
| `full_run_min_watchable_validations` | TBD |
| `full_run_min_evidence_completeness` | TBD |
| `full_run_scale_target` | TBD |
| `full_run_duration_target` | TBD |
| Mid-tranche checkpoint span | TBD |
| Cost / compute caps | TBD |

---

## Context note (prior operator work)

Prior **v1** operator-local campaign activity (e.g. under `out/training_campaigns/`) **informed** the decision to formalize tranche and checkpoint discipline. That prior work is **not** retroactive proof of the **PV1** full-run model; **PV1-M00** is the first **governed post-v1** milestone that **explicitly** defines that model.

---

## Tagging

**Deferred:** no new **PV1** git tag convention in **PV1-M00**; **v0.0.NN-m61** line remains the v1 closure. Revisit only if a repo-level need arises.
