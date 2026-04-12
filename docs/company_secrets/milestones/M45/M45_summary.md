# 📌 Milestone Summary — M45: Self-Play / RL Bootstrap v1

**Project:** STARLAB  
**Phase:** VI — Governed Agent Training, Comparison, and Local Validation  
**Milestone:** M45 — Self-Play / RL Bootstrap v1  
**Timeframe:** 2026-04-12 (implementation → merge to `main` → closeout)  
**Status:** Closed  

---

## 1. Milestone Objective

STARLAB needed a **first governed self-play / RL bootstrap** artifact surface: load a **M43** hierarchical training run + **local** `joblib`, drive **bounded** rollouts through the **M44** live-play validation harness (fixture stub in CI), emit deterministic **`self_play_rl_bootstrap_run.json`** / **`self_play_rl_bootstrap_run_report.json`** plus **`bootstrap_dataset.json`**, **`episodes/episode_manifest.json`**, and optionally **`updated_policy/rl_bootstrap_candidate_bundle.joblib`** after a **conservative weighted re-fit** — **without** claiming benchmark integrity, replay↔execution equivalence, live SC2 in CI, ladder performance, or completion of the **Phase VI integrated test campaign**.

> Without M45, Phase VI would lack a governed, auditable bootstrap loop and artifact contract bridging **M43** + **M44** into a single training-track closeout milestone.

---

## 2. Scope Definition

### In Scope

- `starlab.training`: `self_play_rl_bootstrap_models.py`, `self_play_rl_bootstrap_io.py`, `self_play_rl_bootstrap_pipeline.py`, `emit_self_play_rl_bootstrap_run.py`; bounded fields `runtime_mode`, `bootstrap_mode`, `reward_policy_id` (e.g. `starlab.m45.reward.validation_outcome_v1`), `update_policy_id`.
- Reuse of **M44** harness as rollout substrate; candidate source **M43** hierarchical run + local `joblib` (same posture as M44).
- Artifacts under `out/rl_bootstrap_runs/<run_id>/`: `self_play_rl_bootstrap_run.json`, `self_play_rl_bootstrap_run_report.json`, `bootstrap_dataset.json`, `episodes/episode_manifest.json`, per-episode M44 outputs; optional `updated_policy/rl_bootstrap_candidate_bundle.joblib`.
- Runtime doc: `docs/runtime/self_play_rl_bootstrap_v1.md`; diligence note `docs/diligence/phase_vi_integrated_test_campaign.md` (framing only).
- Tests: `tests/test_m45_self_play_rl_bootstrap.py` (fixture-only CI path).
- `.gitignore` for `out/rl_bootstrap_runs/`.

### Out of Scope

- Benchmark-integrity or ladder / public performance claims.
- Replay↔execution equivalence claims.
- Live SC2 in CI; committed weights.
- Broad deep-RL framework expansion beyond this bounded bootstrap.
- Assertion that the **full integrated Phase VI test campaign** has been executed (it has **not** as of M45 closeout; it remains **post-M45** operator-local work).

---

## 3. Work Executed

- **[PR #56](https://github.com/m-cahill/starlab/pull/56)** merged to `main` (merge commit `1a585b68ea7413852ce78c220c6512bba6a004d7`; final PR head `0e89081cd786b527951a98eb3e63b7677f8c8c00`).
- One superseded PR-head CI failure ([`24314843956`](https://github.com/m-cahill/starlab/actions/runs/24314843956)) on Ruff format — fixed on final head; **not** merge authority.
- Ledger / README / architecture updates on the feature branch; canonical closeout (ledger, governance tests, `M45_run1.md` / summary / audit, tag) completed on `main` after merge.

---

## 4. Validation & Evidence

- **Authoritative PR-head CI:** [`24314869292`](https://github.com/m-cahill/starlab/actions/runs/24314869292) — success (required jobs: `quality`, `smoke`, `tests`, `security`, `fieldtest`, `flagship`, `governance`).
- **Superseded** failure PR-head — [`24314843956`](https://github.com/m-cahill/starlab/actions/runs/24314843956) on `3b19200…` — documented in `M45_run1.md` (**not** merge authority).
- **Merge-boundary `main` CI:** [`24315311180`](https://github.com/m-cahill/starlab/actions/runs/24315311180) on merge commit `1a585b6…` — success (same required jobs).
- **Local validation:** Ruff, Mypy, full pytest green on final PR head where exercised.

---

## 5. CI / Automation Impact

- No new CI jobs; M45 validated via existing **`tests`** lane (fixture-only CPU path) and standard **`quality`** / **`governance`** gates.
- No gate weakening; `fail_under` unchanged at **78.0**.

---

## 6. Issues & Exceptions

- **24314843956** — Ruff format failure on intermediate PR head; fixed before merge (**superseded**).
- **Node 20** deprecation annotations on Actions — informational (pre-existing).

> No blocking issues remain for the final merged head.

---

## 7. Deferred Work

- **Phase VI integrated test campaign** — deliberate cross-surface operator-local campaign; framed in `docs/diligence/phase_vi_integrated_test_campaign.md`; **not** claimed complete at M45.
- Future recharter items (e.g. OD-007 second-environment posture) remain **beyond** the closed **M00–M45** arc unless a new milestone authorizes them.

---

## 8. Governance Outcomes

- First **governed** self-play / RL **bootstrap** surface and artifact contract on `main`, with explicit bounded fields and non-claims.
- **M00–M45** program arc recorded as **closed** on `main` with PR/CI/tag evidence.
- Superseded PR-head run preserved for audit traceability (**not** merge authority).

---

## 9. Exit Criteria Evaluation

| Criterion | Met / Partial / Not met | Evidence |
| --------- | ------------------------ | -------- |
| Deterministic bootstrap + report JSON emission | Met | `emit_self_play_rl_bootstrap_run`, runtime doc, tests |
| M44 substrate reuse + M43 candidate loading | Met | Pipeline + tests |
| Fixture-only CI validation | Met | `24314869292`, `24315311180` |
| Explicit non-claims preserved | Met | Runtime doc, ledger, this summary |
| Integrated Phase VI test campaign executed | Not met (by design) | Deferred post-M45 |

---

## 10. Final Verdict

**Milestone objectives met for the bounded M45 charter.** Safe to record **M45** **closed** on `main` and to treat the **Phase VI integrated test campaign** as the **next** follow-on workstream (unless separately executed and evidenced elsewhere).

---

## 11. Authorized Next Step

- **Post-M45:** operator-local **Phase VI integrated test campaign** per `docs/diligence/phase_vi_integrated_test_campaign.md` — **not** default CI.
- Any **new** product milestone beyond M45 requires explicit recharter and ledger updates.

---

## 12. Canonical References

- PR [#56](https://github.com/m-cahill/starlab/pull/56); merge commit `1a585b68ea7413852ce78c220c6512bba6a004d7`; final PR head `0e89081cd786b527951a98eb3e63b7677f8c8c00`.
- CI: [`24314869292`](https://github.com/m-cahill/starlab/actions/runs/24314869292) (authoritative PR-head); [`24315311180`](https://github.com/m-cahill/starlab/actions/runs/24315311180) (merge-boundary `main`); [`24314843956`](https://github.com/m-cahill/starlab/actions/runs/24314843956) (superseded — not merge authority).
- `docs/runtime/self_play_rl_bootstrap_v1.md`; `docs/starlab.md`; `M45_plan.md`, `M45_toolcalls.md`, `M45_run1.md`, `M45_audit.md`.
- Tag **`v0.0.45-m45`** on merge commit `1a585b68ea7413852ce78c220c6512bba6a004d7`.
