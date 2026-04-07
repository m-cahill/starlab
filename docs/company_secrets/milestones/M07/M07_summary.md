# 📌 Milestone Summary — M07: Replay Intake Policy & Provenance Enforcement

**Project:** STARLAB  
**Phase:** II — Replay Intake, Provenance, and Data Plane  
**Milestone:** M07 — Replay Intake Policy & Provenance Enforcement  
**Timeframe:** 2026-04-06 → 2026-04-07  
**Status:** Closed  

---

## 1. Milestone Objective

Establish a **narrow, deterministic, CI-safe replay intake gate** over **opaque replay bytes** and **operator-declared** metadata: hash replay files, validate declared provenance and redistribution posture, enforce a deterministic policy, and emit governed **`replay_intake_receipt.json`** and **`replay_intake_report.json`**, with **optional** consistency checks against governed **M04/M05** JSON when supplied — **without** replay parsing, benchmark claims, or live SC2 execution in CI.

---

## 2. Scope Definition

### In Scope

- Contract: `docs/runtime/replay_intake_policy.md` (`policy_version`: `starlab.replay_intake_policy.v1`)
- Code: `starlab/replays/` (`intake_models.py`, `intake_policy.py`, `intake_io.py`, `intake_cli.py`)
- `load_canonical_manifest` in `starlab/runs/canonical_run_artifact.py` (M05 manifest reader for optional cross-check)
- Reuse of `load_replay_binding`, `load_run_identity` from `starlab.runs.replay_binding`
- Fixture-driven tests; SC2-free CI

### Out of Scope

- Replay parser substrate, replay semantic extraction, build-order/timeline extraction
- Benchmark integrity, live SC2 execution in CI
- Legal certification of third-party replay rights as a matter of law (declared posture only)

---

## 3. Work Executed

- Implemented metadata schema `starlab.replay_intake_metadata.v1`, receipt/report schemas, four intake statuses, ordered checks, CLI exit codes (0/2/3/4)
- Added synthetic opaque replay fixtures and unit/CLI/governance tests
- Updated public ledger (`docs/starlab.md`), M08 stubs, milestone plan/toolcalls

---

## 4. Validation & Evidence

- **Authoritative PR-head CI:** [`24065819186`](https://github.com/m-cahill/starlab/actions/runs/24065819186) (**success**) — final PR head `a5188ad88bab688ab40136dea77a8b4d3caa0495`
- **Post-merge `main` CI:** [`24066550699`](https://github.com/m-cahill/starlab/actions/runs/24066550699) (**success**) — merge commit `1c7bb0c0381c0f3c8a3eab354ca53e3e503d8d2a`
- **PR:** [#8](https://github.com/m-cahill/starlab/pull/8); merged `2026-04-07T05:50:09Z`; remote branch **deleted**

---

## 5. What M07 Proves (narrow)

- Deterministic **SHA-256** over opaque replay bytes
- Normalization and validation of **declared** intake metadata (governed enums)
- Deterministic **intake policy** outcome and **governed JSON** emission (`replay_intake_receipt.json`, `replay_intake_report.json`)
- Optional **consistency** checking against supplied **M04** `replay_binding.json` and **M05** `manifest.json` / **M03** `run_identity.json` via canonical loaders

---

## 6. What M07 Does Not Prove

- Replay parser correctness; replay semantic extraction; build-order extraction
- Replay↔execution semantic equivalence; benchmark integrity
- Live SC2 execution in CI
- Legal certainty beyond **declared** operator posture

---

## 7. Exit Criteria

Met — contract + code + tests on `main`, PR #8 merged, PR-head and post-merge CI green, ledger updated.

---

## 8. Final Verdict

**Milestone closed** on `main` in the **narrow replay-intake / declared-provenance** sense documented in `docs/runtime/replay_intake_policy.md`.

---

## 9. Canonical References

- PR: [#8](https://github.com/m-cahill/starlab/pull/8)
- Merge commit: `1c7bb0c0381c0f3c8a3eab354ca53e3e503d8d2a`
- Final PR head: `a5188ad88bab688ab40136dea77a8b4d3caa0495`
- Run analysis: `M07_run1.md`
- Audit: `M07_audit.md`
