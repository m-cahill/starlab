# M01 Plan — SC2 Runtime Surface Decision & Environment Lock

## Milestone identity

* **Milestone:** M01
* **Title:** **SC2 Runtime Surface Decision & Environment Lock**
* **Phase:** I — Governance, Runtime Surface, and Deterministic Run Substrate
* **Suggested branch:** `m01-sc2-runtime-surface-env-lock`
* **Suggested tag on closeout:** `v0.0.1-m01`

## Objective

Resolve **OD-005** by selecting STARLAB's canonical SC2 runtime surface, defining the environment lock posture, and producing enough typed/documented/probed infrastructure that M02 can build a deterministic execution harness without reopening foundational boundary decisions. M00 already established the governance baseline, but OD-005 is still open, replay provenance is only conditionally resolved, and the SC2 runtime is explicitly treated as an untrusted boundary; M01 exists to turn that into an explicit, owned contract.   

## Success statement

At M01 closeout, STARLAB should be able to say:

> We have an explicit, evidence-backed SC2 runtime boundary, a documented environment lock, a deterministic environment probe/spec surface, updated provenance/rights posture, and an updated canonical ledger.
> We do **not** yet claim controlled match execution, replay parsing correctness, or benchmark validity.

## Working decision target

Unless implementation uncovers materially better evidence, use this as the **default target architecture**:

* **Canonical control/observation boundary:** Blizzard official SC2 API / protocol (`s2client-proto` / SC2API)
* **Canonical replay decode boundary:** Blizzard `s2protocol`
* **Optional ergonomics adapter:** `python-sc2`, behind a STARLAB adapter boundary only
* **Deferred/non-canonical RL environment layer:** PySC2 or equivalent, not the substrate contract in M01

Rationale: the official Blizzard surface explicitly covers scripted bots, ML bots, replay analysis, Linux clients, and raw / feature-layer / rendered interfaces; `s2protocol` is the reference replay decoder; `python-sc2` states it covers the raw scripted interface only; and PySC2 is a Linux-oriented RL environment rather than the canonical substrate boundary. ([GitHub][1])

## Scope

### In scope

* Resolve OD-005 with a clear decision record
* Define the canonical SC2 runtime boundary and non-canonical adapter boundaries
* Define environment lock posture for local development and future execution work
* Add a deterministic environment probe/spec surface in code
* Update rights/provenance docs for SC2 runtime packages, maps, and replay sources
* Update `docs/starlab.md` to the new 33-milestone map and M01 reality
* Keep CI green without weakening gates
* Produce M01 evidence that is truthful and audit-friendly

### Out of scope

* Full match execution harness
* Bot-vs-bot orchestration
* Replay parsing implementation
* Corpus ingestion
* Benchmarking
* Learned agents
* Live hosted services
* Committing SC2 binaries, map packs, or replay packs into the repo

## Hard guardrails

* **Do not start M02 inside M01.** No "just enough" match harness beyond probe/spec-level work.
* **Do not add heavyweight SC2 runtime dependencies unless strictly required.** Prefer docs + typed models + probe tooling in M01; actual runtime integration can land in M02.
* **Do not commit Blizzard client binaries, maps, replay packs, or any questionable-rights assets.**
* **Do not weaken CI.** No reduced checks, no `continue-on-error`, no scope creep into unrelated CI cleanup.
* **Keep claims bounded.** M01 proves a decision and lock posture, not execution success.

## Required deliverables

### 1) Runtime decision documents

Create:

* `docs/runtime/sc2_runtime_surface.md`
* `docs/runtime/environment_lock.md`

`docs/runtime/sc2_runtime_surface.md` must include:

* candidate set evaluated:

  * official SC2 API / `s2client-proto`
  * `s2protocol`
  * `python-sc2`
  * PySC2
* evaluation criteria:

  * upstream authority
  * interface coverage
  * replay relevance
  * headless/Linux posture
  * contract stability
  * Python ergonomics
  * auditability
  * lockability
* final decision
* what is **canonical**
* what is **allowed but non-canonical**
* what is **deferred**
* assumed vs owned guarantees for the selected surface
* explicit statement that community wrappers do not become STARLAB's canonical contract

`docs/runtime/environment_lock.md` must include:

* canonical local dev host posture for M01/M02
* Python version posture
* package/dependency posture for the chosen surface
* required environment variables and path conventions
* asset acquisition procedure without committing licensed assets
* what CI does and does not validate
* local-only optional evidence procedure
* a section titled **"Environment lock is not execution proof"**

### 2) Typed runtime spec + probe tooling

Create a small `starlab/sc2/` package with at least:

* `starlab/sc2/models.py`
* `starlab/sc2/env_probe.py`

Recommended contents:

* typed models for:

  * runtime choice
  * binary path
  * maps path
  * replays path
  * base build / data version fields
  * interface mode support flags
  * probe result
* deterministic JSON serialization for probe output
* path normalization
* environment variable precedence rules
* probe behavior that works **without** requiring SC2 in CI

Recommended env vars:

* `STARLAB_SC2_ROOT`
* `STARLAB_SC2_BIN`
* `STARLAB_SC2_MAPS_DIR`
* `STARLAB_SC2_REPLAYS_DIR`
* `STARLAB_SC2_BASE_BUILD` (optional)
* `STARLAB_SC2_DATA_VERSION` (optional)

If helpful, also add a lightweight CLI entry such as:

```bash
python -m starlab.sc2.env_probe --json
```

The probe should:

* detect configured paths
* report presence/absence
* avoid executing matches
* be deterministic under fixture-based tests
* support a redacted output mode for milestone artifacts

### 3) Tests

Add tests such as:

* `tests/test_sc2_runtime_models.py`
* `tests/test_sc2_env_probe.py`
* `tests/test_ledger_runtime_alignment.py`

Minimum required test coverage:

* deterministic serialization of the probe result
* env var precedence and normalization
* path detection with temporary fixture directories
* missing-path / partial-config behavior
* ledger alignment checks for:

  * current milestone title
  * 33-milestone map presence
  * OD-005 resolution after implementation
  * M01/M02 handoff correctness at closeout

If a governance test file already exists, extend it instead of proliferating shallow tests.

### 4) Rights and provenance updates

Update:

* `docs/rights_register.md`
* `docs/replay_data_provenance.md`

Required content:

* record the Blizzard SC2 client/runtime surface as a governed dependency surface
* record the license/terms posture for Linux packages / map packs / replay packs
* record that runtime assets are acquired locally under applicable Blizzard terms and are **not** repo-committed
* clarify that replay/map assets with unclear rights remain quarantine-only
* make sure no canonical corpus language outruns current evidence

Blizzard's official SC2 API materials explicitly point to Linux packages, map packs, and replay packs, and note that access requires agreement to Blizzard's AI and Machine Learning License; this needs to be reflected in STARLAB's rights/provenance docs. ([GitHub][1])

### 5) README and contributor-surface alignment

Update `README.md` only as needed so it stays aligned with the new M01 title and current status, while remaining shorter than `docs/starlab.md`.

Do **not** let README become the canonical runtime decision document.

---

## Required `docs/starlab.md` updates

`docs/starlab.md` is the living public ledger and must be updated during M01 work and again at closeout. Keep M00 history intact and preserve historical truth. 

### A. Early-in-branch updates

Before or alongside implementation, update `docs/starlab.md` to:

1. **Adopt the new phase naming**

   * Phase I — Governance, Runtime Surface, and Deterministic Run Substrate
   * Phase II — Replay Intake, Provenance, and Data Plane
   * Phase III — State, Representation, and Perception Bridge
   * Phase IV — Benchmark Contracts, Baselines, and Evaluation
   * Phase V — Learning Paths, Evidence Surfaces, and Flagship Proof
   * Phase VI — Expansion Decision and Platform Boundary Review

2. **Replace the milestone table with the 33-milestone map below**

3. **Rename M01 in the ledger**

   * from "Environment Lock & Runtime Baseline"
   * to **"SC2 Runtime Surface Decision & Environment Lock"**

4. **Update §11 Current milestone**

   * show M01 as the active milestone on the branch

5. **Keep OD-005 open until the decision is actually documented**

6. **Add a canonical corpus promotion rule**

   * no replay, map, ladder-derived asset, or derived label enters a canonical STARLAB corpus without explicit provenance status and redistribution posture recorded

### B. Exact milestone map to put into `docs/starlab.md`

Use this map in §7 and §8.

#### Phase I

* **M00** Governance Bootstrap & Ledger Initialization
* **M01** SC2 Runtime Surface Decision & Environment Lock
* **M02** Deterministic Match Execution Harness
* **M03** Run Identity & Lineage Seed
* **M04** Replay Binding to Run Identity
* **M05** Canonical Run Artifact v0
* **M06** Environment Drift & Runtime Smoke Matrix

#### Phase II

* **M07** Replay Intake Policy & Provenance Enforcement
* **M08** Replay Parser Substrate
* **M09** Replay Metadata Extraction
* **M10** Timeline & Event Extraction
* **M11** Build-Order & Economy Plane
* **M12** Combat, Scouting, and Visibility Windows
* **M13** Replay Slice Generator
* **M14** Replay Bundle & Lineage Contract v1

#### Phase III

* **M15** Canonical State Schema v1
* **M16** Structured State Pipeline
* **M17** Observation Surface Contract
* **M18** Perceptual Bridge Prototype
* **M19** Cross-Mode Reconciliation & Representation Audit

#### Phase IV

* **M20** Benchmark Contract & Scorecard Semantics
* **M21** Scripted Baseline Suite
* **M22** Heuristic Baseline Suite
* **M23** Evaluation Runner & Tournament Harness
* **M24** Attribution, Diagnostics, and Failure Views
* **M25** Baseline Evidence Pack

#### Phase V

* **M26** Replay-Derived Imitation Baseline
* **M27** Hierarchical Agent Interface Layer
* **M28** First Learned Hierarchical Agent
* **M29** Replay Explorer / Operator Evidence Surface
* **M30** Public Flagship Proof Pack

#### Phase VI

* **M31** SC2 Substrate Review & Expansion Decision
* **M32** Platform Boundary Review & Multi-Environment Charter

### C. Closeout updates to `docs/starlab.md`

At M01 closeout, update:

* §7 milestone table:

  * M01 → Complete
  * M02 → Planned / next
* §11 current milestone:

  * switch to **M02 — Deterministic Match Execution Harness**
* §12 open decisions:

  * mark **OD-005 resolved**
  * summarize the selected runtime posture
* §16 rights/provenance tracker:

  * add/update rows reflecting SC2 runtime assets and license posture
* §18 milestone closeout ledger:

  * add PR / merge SHA / CI evidence for M01
* §20 score trend table:

  * add M01 score
* §23 changelog:

  * add M01 closeout entry

If the milestone proves the environment lock sufficiently, update the "proved vs not yet proved" area so "environment stability / lock posture" advances honestly, without overstating match execution or replay correctness.

---

## Implementation sequence

### Step 1 — Replace the stub plan

* Replace the current stub in `docs/company_secrets/milestones/M01/M01_plan.md` with this plan.
* Preserve and use `M01_toolcalls.md` for implementation logging.

### Step 2 — Update the ledger first

* Update `docs/starlab.md` early so the branch reflects the new milestone map and the active M01 framing.
* Do **not** close OD-005 yet.

### Step 3 — Write the decision record

* Build the candidate matrix in `docs/runtime/sc2_runtime_surface.md`
* Record the chosen stack and rejected/deferred options
* Make the contract boundary explicit

### Step 4 — Write the environment lock

* Define local host posture, CI posture, env vars, acquisition procedure, and non-commit rules in `docs/runtime/environment_lock.md`

### Step 5 — Implement the typed spec and probe

* Add the small `starlab/sc2/` package
* Keep it lightweight and deterministic
* No actual match execution

### Step 6 — Extend tests

* Add/extend governance and probe tests
* Ensure docs/code alignment is checked in CI

### Step 7 — Update provenance/rights docs

* Reflect the chosen runtime surface and asset terms
* Keep redistribution claims conservative

### Step 8 — Align README

* Update status wording only as needed

### Step 9 — Run CI and fix only M01-scoped issues

* Keep scope tight
* Do not sneak in unrelated infrastructure work

---

## Acceptance criteria

M01 is done only if all of the following are true:

1. **OD-005 is resolved** with an evidence-backed decision document
2. `docs/runtime/sc2_runtime_surface.md` exists and contains a scored candidate matrix plus final decision
3. `docs/runtime/environment_lock.md` exists and defines the lock posture clearly
4. A deterministic `starlab/sc2` probe/spec surface exists in code
5. Tests cover probe determinism, env var precedence, partial-config behavior, and ledger/doc alignment
6. `docs/rights_register.md` and `docs/replay_data_provenance.md` are updated conservatively and correctly
7. `docs/starlab.md` is updated:

   * new phase map
   * new 33-milestone table
   * M01 renamed and reflected as current
   * OD-005 resolved at closeout
8. CI is green with no weakened gates
9. No SC2 binaries, maps, or replay packs are committed
10. The repo makes **no claim** that controlled match execution has already been proved

---

## Evidence requirements

Required evidence for closeout:

* green PR-head CI
* green post-merge CI
* diff showing `docs/starlab.md` updated truthfully
* M01 summary and audit
* runtime decision doc
* environment lock doc
* test evidence for probe/spec behavior

Optional but valuable:

* a **redacted local probe sample** in M01 milestone artifacts if a compliant local SC2 installation exists
* a short note documenting whether the local machine has the necessary SC2 assets available for M02

If local SC2 is not available in Cursor's environment, **do not block M01**. Finish the docs/spec/probe work and leave actual execution proof for M02.

---

## Audit posture for M01

Design M01 so it can plausibly score **4.5–5.0** on governance/docs/diligence:

* explicit decision
* explicit non-goals
* typed probe surface
* truthful CI
* rights/provenance discipline
* no overstated runtime claims

Unresolved issues must be explicitly deferred, not hidden.

---

## Notes for Cursor

* Favor **official-protocol-first** design, with wrappers treated as adapters rather than STARLAB's public contract. The official protocol is websocket/protobuf-based, supports replay processing, and exposes raw / feature-layer / rendered interfaces; that makes it the best canonical boundary for a lab-first substrate. ([GitHub][2])
* `python-sc2` is useful, but its own README says it covers only the raw scripted interface, so it should not define STARLAB's canonical substrate contract. ([GitHub][3])
* `s2protocol` is the right replay-decode reference surface, but it is intentionally low-level and "the first tool in the chain," so M01 should document it as the replay boundary, not mistake it for full replay analysis. ([GitHub][4])
* Keep M01 small, reversible, and enterprise-grade.

---

If you want, I can also generate the exact `docs/starlab.md` replacement sections for §6–§12 so Cursor can paste them directly.

[1]: https://github.com/blizzard/s2client-proto "GitHub - Blizzard/s2client-proto: StarCraft II Client - protocol definitions used to communicate with StarCraft II. · GitHub"
[2]: https://github.com/Blizzard/s2client-proto/blob/master/docs/protocol.md "s2client-proto/docs/protocol.md at master · Blizzard/s2client-proto · GitHub"
[3]: https://github.com/BurnySc2/python-sc2 "GitHub - BurnySc2/python-sc2: A StarCraft II bot api client library for Python 3 · GitHub"
[4]: https://github.com/Blizzard/s2protocol "GitHub - Blizzard/s2protocol: Python library to decode StarCraft II replay protocols · GitHub"
