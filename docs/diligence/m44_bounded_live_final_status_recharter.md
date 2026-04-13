# Recharter package — M44/M45 bounded live `final_status` semantics

**Status:** Planning only — not implemented on this document’s landing branch until milestone execution.  
**Branch:** `recharter/m44-bounded-live-final-status-semantics`  
**Milestone placeholder:** **M46** — *Bounded live validation final-status semantics* (working title; numbering subject to program governance).

---

## 1. Problem statement

The Phase VI operator-local campaign (`phase_vi_2026_04_13_a`) proved that **live** M44 (`runtime_mode=local_live_sc2`, `adapter=burnysc2`) can run end-to-end: SC2 launches, a bounded game executes, required JSON artifacts and replay binding are emitted, and the CLI exits successfully.

However, **`match_execution.final_status`** in the emitted run artifact is **`"Defeat"`** (SC2’s literal game result), while the **fixture** path (`adapter=fake`) records **`"ok"`**.

Cause in product code:

- `burnysc2_adapter` sets `final_status` from `python-sc2`’s `run_game` result name (e.g. `Defeat`) after the bounded harness bot exits voluntarily at the step cap (`await self.client.leave()` after `max_game_steps`).
- `FakeMatchHarnessAdapter` hardcodes `final_status="ok"` for deterministic CI.

Downstream, **M45** reward policy (`starlab.m45.reward.validation_outcome_v1`) treats **`final_status == "ok"`** as the primary reward gate; any other string yields `reward_primary = 0.0`.

Operator runbooks and campaign **pass** rules that require **`match_execution.final_status == "ok"`** for live M44 therefore **cannot** be satisfied with the current bounded live behavior, even when the harness is healthy and artifacts are complete. This is **not** an operator error; it is a **semantic mismatch** between fixture success, live SC2 result strings, and validation/gating expectations.

**Out of scope for this recharter:** the separate **M42 `--contract` path** issue (M40 charter JSON vs M20 benchmark contract). Document only as a known follow-on; do not bundle fixes.

---

## 2. Recommended milestone title

**M46 — Bounded live validation final-status semantics (M44/M45 alignment)**

Single objective: align **governed** definitions of “success” for bounded live-play validation with **auditable** fields so fixture and live paths are comparable without inventing gameplay claims.

---

## 3. Tight milestone plan

1. **Inventory** — Enumerate every consumer of `match_execution.final_status` and M44 `local_live_play_validation_run` success semantics (M44 harness, M45 bootstrap, reward policy, docs/runbooks, tests).
2. **Design decision** — Choose **Option A** or **Option B** (see §6) with explicit governance rationale and non-claims.
3. **Contract** — Update runtime contract text (`docs/runtime/local_live_play_validation_harness_v1.md` and, if needed, `docs/runtime/self_play_rl_bootstrap_v1.md`) with stable field definitions and versioning notes.
4. **Implementation** — Minimal code change in `starlab.sc2` and/or `starlab.training` per chosen option; extend tests (fixture + one bounded live path test where feasible without CI live SC2).
5. **Ledger** — Update `docs/starlab.md` milestone table and status paragraph per project rules.
6. **CI** — Remain fixture-first; no requirement for live SC2 in CI.

---

## 4. Decision memo — two resolution families

### Option A — Normalize bounded voluntary live termination to a governed success status

**Idea:** For **bounded harness runs** that complete the contract (step cap reached, harness exits cleanly, proof record valid), emit a **single governed string** for validation success (e.g. keep `final_status="ok"` for this mode, or introduce a dedicated `validation_outcome` / `bounded_run_status` that is always `"ok"` when bounded completion criteria hold).

**Pros:** One field to gate on; aligns with fixture/fake; minimal change to M45 reward policy if `final_status` remains the gate.  
**Cons:** `final_status` would no longer equal SC2’s literal `Result` enum for bounded runs; must document **narrowly** that this applies only to bounded validation, not “won the game.”

### Option B — Preserve literal SC2 result; gate on separate bounded-completion signal

**Idea:** Keep `match_execution.final_status` as **literal** SC2 outcome (`Defeat`, `Victory`, etc.). Add or reuse a separate field (e.g. `bounded_harness_completed: true`, `bounded_exit_reason: "step_cap"`) and change M44/M45 **success and reward** logic to require **bounded completion + proof validity**, not `final_status == "ok"`.

**Pros:** Preserves forensic fidelity to SC2’s reported result; clearer separation between “game outcome” and “validation harness succeeded.”  
**Cons:** Touches more surfaces (M45 reward policy, possibly JSON schema, runbooks); more tests and doc updates.

---

## 5. Recommendation (with rationale)

**Recommend Option A** for a **small** first milestone, if governance accepts that **bounded validation success** is not the same claim as **match outcome**.

**Rationale:**

- **Auditability:** One primary status field for “did the bounded validation contract complete?” matches existing operator runbooks and M45 reward wiring.
- **Scope:** Smallest diff to `compute_episode_reward_validation_outcome_v1` and campaign pass criteria (often unchanged if `final_status` becomes `"ok"` when bounded exit criteria are met).
- **Explicit non-claim:** Document that for `adapter=burnysc2` bounded runs, `final_status="ok"` means **harness completed per step policy**, not ladder performance or victory.

If the program prefers **maximum literalism** for SC2 results, **Option B** is the correct long-term shape; accept larger schema and consumer churn in M46 or split M46 into “field addition” + “consumer migration.”

---

## 6. Audit and risk notes

| Risk | Mitigation |
|------|------------|
| Over-claiming “success” | Non-claims and contract text must state bounded validation ≠ win/loss skill, ≠ benchmark integrity. |
| Schema drift | Bump or version fields per `docs/starlab.md` rules if JSON shape changes. |
| CI vs local | CI stays fixture-only; live behavior covered by unit tests around mapping logic + optional manual operator evidence. |
| Replay semantics unchanged | This milestone does not claim replay↔execution equivalence. |

---

## 7. Exact evidence justifying the recharter (operator campaign)

From the **post-M45 operator-local** run (local artifacts under operator machine; not committed):

- **CLI:** `python -m starlab.sc2.emit_local_live_play_validation_run` with `--runtime-mode local_live_sc2`, same M43 lineage as fixture chain, **`--match-config`** using `adapter=burnysc2` and map discovery against a resolvable `.SC2Map`.
- **Outcome:** Process exit code **0**; SC2 log showed game creation, `in_game`, bounded steps, client leave, result **Defeat**.
- **Artifacts present:** `local_live_play_validation_run.json`, report JSON, `replay_binding.json`, `replay/validation.SC2Replay`, plus M02/M03/M04 companions as designed.
- **Blocking field:** In `local_live_play_validation_run.json`, **`runtime_mode`: `"local_live_sc2"`** and **`match_execution.final_status`: `"Defeat"`** (not `"ok"`).

Code references (repo):

```137:189:starlab/sc2/adapters/burnysc2_adapter.py
    final = getattr(result, "name", str(result))
    ...
    return ExecutionProofRecord(
        ...
        final_status=final,
```

```37:55:starlab/sc2/adapters/fake.py
        return ExecutionProofRecord(
            ...
            final_status="ok",
```

```75:95:starlab/training/self_play_rl_bootstrap_pipeline.py
def compute_episode_reward_validation_outcome_v1(validation_run: dict[str, Any]) -> dict[str, Any]:
    ...
    reward_primary = 1.0 if final_status == "ok" else 0.0
```

---

## Acceptance criteria (M46 definition of done)

- [ ] Governed semantics for bounded live vs fixture `final_status` (or successor fields) are documented and **versioned** in runtime contracts.
- [ ] M45 reward / gating logic matches the chosen option without contradicting explicit non-claims.
- [ ] Tests cover the new behavior without requiring live SC2 in default CI.
- [ ] `docs/starlab.md` updated with M46 closeout narrative and **honest** non-claims (no benchmark integrity, no ladder claim).
- [ ] Operator runbook / integrated campaign criteria updated so live M44 pass/fail rules match implementation.

---

## Non-claims (preserved)

M46 does **not** prove: benchmark integrity; replay↔execution equivalence; live SC2 in CI; ladder or public performance; full RL product readiness. It only aligns **validation success semantics** for bounded harness runs.

---

## Ledger follow-up

**Should `docs/starlab.md` later gain a note on bounded live validation semantics after the fix lands?**

**Yes.** Per `.cursorrules` and project practice, any milestone that changes contract behavior or evaluation semantics should update the public ledger with a short, explicit paragraph on **what changed**, **what is still not claimed**, and **how fixture vs live bounded runs are interpreted**. This avoids future operator campaigns rediscovering the same asymmetry.

---

## Proposed branch name (this package)

- **Branch:** `recharter/m44-bounded-live-final-status-semantics` (created for this commit).

## Summary table

| Item | Value |
|------|--------|
| Proposed milestone | **M46** (placeholder) — bounded live final-status semantics |
| Recommended option | **Option A** (normalize bounded success to governed `ok` or equivalent single gate), unless program mandates literal SC2 results (**Option B**) |
| Scope | M44/M45 alignment only; **M42 contract path out of scope** |
