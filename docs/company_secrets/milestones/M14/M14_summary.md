# 📌 Milestone Summary — M14: Replay Bundle & Lineage Contract v1

**Project:** STARLAB  
**Phase:** II — Replay Intake, Provenance, and Data Plane  
**Milestone:** M14 — Replay Bundle & Lineage Contract v1  
**Timeframe:** 2026-04-08 → 2026-04-08  
**Status:** Closed  

---

## 1. Milestone Objective

Establish a **deterministic, governed packaging surface** that turns already-produced **M09–M13 replay JSON artifacts** into a portable **bundle manifest**, **lineage graph**, and **compact contents inventory** — with explicit **primary vs secondary report** membership, hash-linked lineage checks, and CI — **without** raw replay bytes, raw parse in the bundle, archives, or claims of execution equivalence or benchmark integrity.

> Without M14, STARLAB would lack a reproducible **bundle + lineage contract** over the governed replay plane before Phase III state work.

---

## 2. Scope Definition

### In Scope

- Runtime contract: `docs/runtime/replay_bundle_lineage_contract.md`
- Product modules: `replay_bundle_models.py`, `replay_bundle_catalog.py`, `replay_bundle_generation.py`, `replay_bundle_io.py`, `extract_replay_bundle.py`
- Artifacts: `replay_bundle_manifest.json`, `replay_bundle_lineage.json`, `replay_bundle_contents.json`
- Primary members: `replay_metadata.json`, `replay_timeline.json`, `replay_build_order_economy.json`, `replay_combat_scouting_visibility.json`, `replay_slices.json`
- Secondary optional: matching `*_report.json` when present
- Optional contextual lineage only: M07 intake receipt / M08 parse receipt via CLI (not bundle members)
- Fixtures `tests/fixtures/m14/`, tests `test_replay_bundle.py`, `test_replay_bundle_cli.py`, governance updates
- PR [#15](https://github.com/m-cahill/starlab/pull/15); **green PR-head** [`24118622373`](https://github.com/m-cahill/starlab/actions/runs/24118622373); **green merge-push `main`** [`24118654909`](https://github.com/m-cahill/starlab/actions/runs/24118654909)

### Out of Scope

- Raw replay clipping, `.SC2Replay` in bundle, `replay_raw_parse.json` in bundle, zip/tar requirement
- `s2protocol`, parser CLI in M14 modules, benchmark semantics, live SC2 in CI, M15 canonical state schema product code

---

## 3. Work Executed

- Implemented deterministic bundle ID / lineage root, lineage validation across M10–M13 embedded hashes, optional report hash checks, optional M07/M08 contextual nodes, CLI and golden fixtures; updated ledger glossary and Phase II artifact row.

---

## 4. Validation & Evidence

- **Authoritative PR-head CI:** [`24118622373`](https://github.com/m-cahill/starlab/actions/runs/24118622373) — **success** on `42e29f2a64fa4672dbd2df435a04836c379b5258`
- **Merge-boundary `main` CI:** [`24118654909`](https://github.com/m-cahill/starlab/actions/runs/24118654909) — **success** on merge commit `8a0439a9a2970a74f3a5087390fc080f02852246`
- **PR:** [#15](https://github.com/m-cahill/starlab/pull/15); merged `2026-04-08T05:00:41Z`; merge commit `8a0439a9a2970a74f3a5087390fc080f02852246`; remote branch **deleted**

---

## 5. What M14 Proves (narrow)

- **Deterministic replay bundle packaging** and **lineage contract v1** over governed replay JSON, with fixture-backed CI on `main`.

---

## 6. What M14 Does Not Prove

- Raw replay clipping, replay↔execution equivalence, benchmark integrity, live SC2 in CI, canonical state semantics, fog-of-war truth, or legal certification of third-party replay rights.

---

## 7. Standing Non-Claim

**`bundle_id` / `lineage_root`** are **deterministic packaging identities** over hashes of governed JSON — not execution-equivalence, benchmark validity, or legal replay-rights certification.

---

## 8. Authorized Next Step

**M15 — Canonical State Schema v1** (Phase III) — stub only until kickoff; no M15 product code without milestone authorization.

---

## 9. Canonical References

- PR: https://github.com/m-cahill/starlab/pull/15  
- Merge commit: `8a0439a9a2970a74f3a5087390fc080f02852246`  
- PR-head CI: https://github.com/m-cahill/starlab/actions/runs/24118622373  
- Merge `main` CI: https://github.com/m-cahill/starlab/actions/runs/24118654909  
- Contract: `docs/runtime/replay_bundle_lineage_contract.md`  
- Ledger: `docs/starlab.md`
