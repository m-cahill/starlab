# PV1-M00 — Plan (archival handoff)

**Milestone:** PV1-M00 — Post-v1 Industrial Campaign Charter & Success Criteria  
**Type:** Governance-first recharter — **not** runtime execution, **not** product expansion.

This document preserves the milestone intent so the `PV1-M00/` folder stands alone without relying on chat history. **`docs/starlab.md`** remains the **authoritative public** record of PV1 status; this path under `docs/company_secrets/` is **operator / local working surface**, not the public source of truth.

---

## 1. Goal

- Formally open the **post-v1** program line as **PV1** under ids **`PV1-MNN`** (distinct from **M00–M61**; **no M62**).
- Define charter, success criteria, and a **public** PV1 roadmap in **`docs/starlab.md`**.
- Preserve **M00–M61** as the **closed, historical** v1 arc without rewriting v1 claims.
- Avoid silent expansion of STARLAB claims (benchmark, equivalence, ladder, live CI, multi-env).

---

## 2. Non-goals (explicit)

- No long-run campaign execution as merge evidence; no new ladder-strength, benchmark-integrity, or replay↔execution claims.
- No live SC2 in CI expansion; no broad architecture rewrite; no multi-game chartering in PV1-M00.
- No silent mutation of the meaning of **M00–M61**.
- No new **PV1** git tag naming convention in this milestone (deferred).
- No seeding **PV1-M01** / **PV1-M02** folders until those milestones are **explicitly opened** under separate governance.

---

## 3. Required `docs/starlab.md` updates (public source of truth)

Completed expectations:

1. **Boundary language:** **PV1** is **not** “Phase VIII” of the original v1 phase map; **no M62**; **M00–M61** remain **closed** and **historical**.
2. **Separated addendum:** A **Post-v1 (PV1)** section (placed after the §7 milestone table) with phase identity, one-sentence charter, tagging deferred, and **no** `docs/company_secrets/**` links as authoritative.
3. **Roadmap table:** **PV1-M00** through **PV1-M04** with statuses **current** / **planned** / **optional** / **not yet opened** as applicable; **roadmap disclaimer** that rows are placeholders until milestones are opened and closed under governance.
4. **Navigation:** Quick-scan table + **Start Here** pointer so new readers find PV1 without reading the entire ledger.
5. **§11 Current milestone:** **PV1-M00** entry at top; **M61** and prior milestones remain **closed** narrative below.
6. **§23 Changelog:** Entry for **PV1-M00** governance closeout.

---

## 4. Charter requirements (`PV1-M00_charter.md`)

The private charter artifact must define (and does define), at minimum:

- Milestone and phase identity; why post-v1 exists; **reused substrate** (M49/M50/M51 — not a new engine).
- **Full training run** threshold **structure** (field names); numeric values **TBD** / operator-set in **Open operator-set values**.
- **Tranche model** (identity, start, close evidence, authorization, failed/paused/incomplete).
- **Checkpoint cadence**; **evidence model** (campaign identity, preflight, execution summary, checkpoints, watchable validation, replay-binding where required, operator notes, final threshold declaration).
- **Watchable validation** minimums; **operator decision gates**; **resumption vs new campaign identity**.
- **Explicit non-claims** (benchmark, equivalence, ladder, live CI merge norm, multi-env).
- **Prior `out/` work:** may be cited as **context only** — **not** proof of the PV1 full-run model.
- **Exit criteria** for opening **PV1-M01** vs **PV1-M02** (see §16 of charter).

---

## 5. Acceptance criteria (milestone done when)

1. `docs/company_secrets/milestones/post-v1/PV1-M00/` contains `PV1-M00_plan.md`, `PV1-M00_charter.md`, and closeout `PV1-M00_summary.md` / `PV1-M00_audit.md` when the branch is finalized.
2. `docs/starlab.md` contains the Post-v1 (PV1) addendum and roadmap; v1 ledger integrity preserved.
3. Charter defines threshold **shape**, tranches, checkpoints, evidence, gates, non-claims; no invented numeric thresholds.
4. CI / governance tests green; **no** new product code for PV1-M00.

---

## 6. Closeout instructions

- Generate **`PV1-M00_summary.md`** and **`PV1-M00_audit.md`** after validation is green.
- **Do not** treat roadmap rows as approved work; **do not** auto-open the next milestone when PV1-M00 merges.
- **PV1-M01** opens only if a **concrete** observability or checkpoint **tooling** gap is documented and justified; otherwise keep **PV1-M01** closed and plan the next **substantive** opening as **PV1-M02** when the operator authorizes execution evidence work.
- Seed **PV1-M01** or **PV1-M02** milestone folders only on a **follow-on branch** when that milestone is actually opened (avoid post-close churn).

---

## 7. Branch and commit posture

- **Branch:** `pv1-m00-charter-post-v1-industrial-campaign`
- **Suggested conventional commit:** `docs(governance): charter PV1-M00 post-v1 industrial campaign phase`

---

## 8. Tooling / observability gap assessment (PV1-M00 final pass)

**Result:** No **concrete** repository tooling gap was identified in this documentation-only milestone that **requires** opening **PV1-M01** (Campaign Observability & Checkpoint Discipline). Existing M49/M50/M51 campaign artifacts and operator workflows are unchanged by PV1-M00; any future gap should be **documented with evidence** before **PV1-M01** is opened.

**Recommendation:** Hold **PV1-M01** closed unless/until a real gap is filed; next substantive milestone when authorized: **PV1-M02** (Tranche A Execution Evidence).
