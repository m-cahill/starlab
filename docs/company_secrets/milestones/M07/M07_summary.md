# Milestone Summary — M07: Replay Intake Policy & Provenance Enforcement

**Project:** STARLAB  
**Phase:** II — Replay Intake, Provenance, and Data Plane  
**Milestone:** M07 — Replay Intake Policy & Provenance Enforcement  
**Status:** Pending merge to `main` (finalize after PR merge and green CI)

---

## Objective (narrow)

Implement deterministic **replay intake** over **opaque** replay bytes and **declared** operator metadata, emitting `replay_intake_receipt.json` and `replay_intake_report.json`, with optional cross-check of M04/M05 artifacts.

---

## Proved (narrow)

* Deterministic intake policy evaluation and JSON emission (`starlab.replays`, fixture-driven tests, SC2-free CI).
* `policy_version` **`starlab.replay_intake_policy.v1`**.

## Not proved

* Replay parser correctness, replay semantic extraction, benchmark integrity, live SC2 execution in CI, legal certification of third-party replay rights.

---

## Canonical references

* Plan: `docs/company_secrets/milestones/M07/M07_plan.md`
* Contract: `docs/runtime/replay_intake_policy.md`
* CI: `M07_run1.md` (after merge)
