# Milestone Summary — M10: Timeline & Event Extraction

**Project:** STARLAB  
**Phase:** II — Replay Intake, Provenance, and Data Plane  
**Milestone:** M10 — Timeline & Event Extraction  
**Timeframe:** 2026-04-07 → 2026-04-07  
**Status:** Closed  

---

## 1. Milestone Objective

Define and implement a **governed, deterministic replay timeline contract** (`replay_timeline.json`, `replay_timeline_report.json`) over M08 `replay_raw_parse.json`, including optional **`raw_event_streams`** lowering on schema **`starlab.replay_raw_parse.v2`** behind the existing parser boundary — without claiming build-order/economy (M11), combat/scouting, benchmark integrity, replay↔execution equivalence, or broad upstream parser certification.

---

## 2. Scope Definition

### In Scope

- Contract: `docs/runtime/replay_timeline_event_extraction.md`
- Modules: `timeline_models.py`, `timeline_extraction.py`, `timeline_io.py`, `extract_replay_timeline.py` (CLI); parser boundary updates in `parser_interfaces.py`, `s2protocol_adapter.py`, `parser_io.py`, etc.
- Artifacts: `replay_timeline.json`, `replay_timeline_report.json`
- Bounded semantic kinds, deterministic merge order policy, privacy scrub for public timeline
- Fixture-driven CI under `tests/fixtures/m10/`

### Out of Scope

- Build-order / economy (M11); combat, scouting, visibility
- Replay↔execution equivalence; benchmark integrity
- Live SC2 in CI; broad Blizzard parser correctness certification
- Proof of exact intra-gameloop causality (merged order is **deterministic canonicalization** only)

---

## 3. Work Executed

- Implemented timeline extraction pipeline, linkage checks, deterministic JSON emission, and CLI
- Extended parser substrate with optional v2 `raw_event_streams` when the adapter lowers streams
- Added governance tests and fixtures; ledger and runtime contract docs

---

## 4. Validation & Evidence

- **PR-head:** no green `pull_request` run on final tip — only witnessed run [`24104110934`](https://github.com/m-cahill/starlab/actions/runs/24104110934) (**cancelled**).
- **Merge-push `main` on merge commit `cb3e581…`:** [`24104111851`](https://github.com/m-cahill/starlab/actions/runs/24104111851) (**failure** — Mypy).
- **Authoritative green `main` after Mypy repair:** [`24104197912`](https://github.com/m-cahill/starlab/actions/runs/24104197912) (**success**) on `cf2074e10ec8a38b22bd7b75ffeb4ec22a71485b`.
- **PR:** [#11](https://github.com/m-cahill/starlab/pull/11); merged `2026-04-07T20:58:46Z`; remote branch **deleted**.

---

## 5. What M10 Proves (narrow)

- **Governed timeline artifacts** with deterministic merge order policy and bounded `semantic_kind` mapping
- **Optional** v2 raw event stream lists inside `replay_raw_parse.json` when lowered by the adapter — M08’s historical proof remains narrow; M10 extends the boundary
- **Fixture-driven** validation in CI once `main` is green after the Mypy repair

---

## 6. What M10 Does Not Prove

- Build-order / economy, combat/scouting, benchmark integrity, replay↔execution equivalence, live SC2 in CI, broad parser semantics certification

---

## 7. Standing non-claim

Merged timeline order is a **deterministic canonicalization policy**, not proof of exact intra-gameloop causality across streams.
