# PX1-M04 — Governed Demo Proof Pack & Winning Video (v1)

**Milestone:** `PX1-M04` — **packaging and proof governance** for evidence already produced under **PX1-M03** (not remediation, not new training).

**Public ledger:** `docs/starlab.md` — **`PX1-M04`** is **closed** on `main`; **`current milestone`** = **None** until a new **`PX1-MNN`** is chartered.

---

## 1. Why PX1-M04 exists

**PX1-M03** closed successfully with **`demo-ready-candidate-selected`** under the **frozen PX1-M03 remediation protocol** for candidate **`px1_m01_weighted_refit_rl_bootstrap_v1`**, including replay-backed wins and **≥1** watchable win with **optional media registration** tied to the same winning run.

**PX1-M04** answers a **different** question:

> Can STARLAB **select, reference, and package** that successful evidence into a **governed, reviewable, clearly bounded** demo proof pack (replay + operator-captured video + declarations + traceability to PX1-M03), without claiming new gameplay remediation or a new campaign?

**PX1-M03** was **remediation**; **PX1-M04** is **presentation and packaging** under explicit non-claims.

---

## 2. What counts as a governed demo proof pack

A **governed demo proof pack** (for this milestone) is **not** a single file in git. It is a **documented bundle of references** (and optionally small metadata sidecars) that together:

1. **Identify** one **primary canonical winning run** (and optionally one backup) drawn from **PX1-M03** authoritative operator-local evidence.
2. **Reference** the **replay artifact** and **optional media registration** (path + content hash where recorded) for that run.
3. **Reference** **`demo_readiness_declaration.md`** / evaluation input that recorded **`demo-ready-candidate-selected`** for the same candidate id.
4. **State proof boundaries** (what the demo shows vs what it does not show).
5. **Prefer operator-local storage** for large binaries; **do not** commit large media unless separately justified.

The pack is **complete** when the private checklist (**`PX1-M04_pack_checklist.md`**) can be honestly checked off and closeout is authorized — **separate PR** from opening.

---

## 3. Artifact inventory (target)

| Kind | Typical location | In git? |
| --- | --- | --- |
| Runtime contract (this doc) | `docs/runtime/px1_governed_demo_proof_pack_v1.md` | Yes |
| Ledger / narrative | `docs/starlab.md` | Yes |
| Canonical selection memo | `docs/company_secrets/milestones/post-v1/PX1-M04/PX1-M04_canonical_demo_selection.md` | If tracked |
| PX1-M03 sealed run JSON | `…/runs/<label>/local_live_play_validation_run.json` | Operator-local |
| Replay | `…/runs/<label>/*.SC2Replay` (or path in run JSON) | Operator-local |
| Operator-captured video | e.g. `out/px1_m03_operator_watchable.mp4` | Operator-local (default) |
| PX1-M03 declaration / evidence | `demo_readiness_declaration.md`, `px1_demo_readiness_evidence.json` | Operator-local series root |

---

## 4. Canonical run / video selection rules

1. **Primary** canonical run must be a **win** (`sc2_game_result` = Victory) that is **replay-backed** and, for the watchable requirement, has **non-null** `optional_media_registration` if that run is the designated **watchable** demo run.
2. Selection must **trace to** a **documented PX1-M03** evaluation series (same **candidate id**).
3. **Rationale** (clearest win, best pacing, strongest chain, alignment with captured video) is recorded in **`PX1-M04_canonical_demo_selection.md`** — not inferred from marketing language.
4. **Changing** the canonical run after selection requires a **documented revision** in the same memo (audit trail).

**Initial documented selection (PR1):** primary **`scripted_01`** under the PX1-M03 watchable-capture series; optional media **`out/px1_m03_operator_watchable.mp4`** — see private **`PX1-M04_canonical_demo_selection.md`**.

---

## 5. Explicit non-claims

PX1-M04 **does not** prove or claim:

- **Ladder** or **public** strength.
- **Benchmark integrity** globally.
- **Replay↔execution equivalence** in the gameplay-semantic sense.
- **Publication** of model weights or full campaign artifacts in-repo.
- **v2** readiness or productization.
- That **every** match or run is equally strong.
- That the **captured video** is the only possible outcome or represents all runs.
- That **PX1-M05** or **v2** opens automatically — they do **not**.

---

## 6. PX1-M05 and v2 do not open automatically

- **`PX1-M05`** remains **optional / not yet opened** until explicitly chartered.
- **`v2`** remains **not opened** until explicitly rechartered (`docs/starlab-vision.md` directions stay out-of-scope for **M00–M61** closure).

---

## 7. Milestone boundaries

| In scope | Out of scope |
| --- | --- |
| Ledger + runtime contract + selection memo + checklist | New gameplay tuning by default |
| Packaging narrative and references | New industrial campaign |
| Honest closeout when pack is verified | Automatic **PX1-M05** / **v2** |

---

## 8. Related runtime docs

- **`docs/runtime/px1_candidate_strengthening_demo_readiness_v1.md`** — PX1-M03 (closed).
- **`docs/runtime/px1_play_quality_demo_candidate_selection_v1.md`** — PX1-M02 (closed).
- **`docs/runtime/px1_full_industrial_campaign_execution_evidence_v1.md`** — PX1-M01 (closed).
