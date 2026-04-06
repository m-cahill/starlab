# STARLAB — Canonical Project Ledger

**Status:** Active — M01 on `main` ([PR #2](https://github.com/m-cahill/starlab/pull/2)); **M02** harness in [PR #3](https://github.com/m-cahill/starlab/pull/3) (pre-merge; PR-head CI green; **local real-execution evidence pending**)  
**License:** Source-available (evaluation and verification only); see `LICENSE`  
**Governance Model:** Milestone-Driven, CI-Enforced  
**Audit Posture:** Active Governance Signal  
**Primary document:** `docs/starlab.md`

---

## Start Here

1. Read `docs/starlab-vision.md` for the moonshot framing and long-range thesis.  
2. Read `docs/bicetb.md` for licensing, provenance, and diligence posture (“clean enough to buy”).  
3. Read this file for current status, phase structure, milestone history, and project rules.  
4. Read governance docs: `docs/public_private_boundary.md`, `docs/replay_data_provenance.md`, `docs/rights_register.md`, `docs/branding_and_naming.md`, `docs/deployment/deployment_posture.md`, `docs/runtime/sc2_runtime_surface.md`, `docs/runtime/environment_lock.md`, and (for execution harness scope) `docs/runtime/match_execution_harness.md`.  
5. Treat this document as the public-facing source of truth and update it at every milestone closeout.  
6. Local testing is expected to use an RTX 5090 Blackwell where relevant.

---

## 1. Project identity (one sentence)

STARLAB is a **governed, replay-native RTS research lab** that begins with StarCraft II and aims to create a reproducible, benchmarkable, evidence-first substrate for hierarchical, perception-grounded, multi-agent research.

---

## 2. Authority hierarchy

When documents or implementation disagree, use this order:

1. **`docs/starlab-vision.md`** — moonshot, ambition, thesis, and long-range scope  
2. **`docs/bicetb.md`** — “clean enough to buy” operating rules for ownership, licensing, provenance, and public/private boundaries  
3. **`docs/starlab.md` (this file)** — current project state, milestone status, phase map, authority record  
4. **README** — public front door and short-form project identity  
5. **Implementation** — must satisfy the above; defects are tracked against the docs, not the reverse

**Rule:** this file is the **canonical public ledger**, not the full philosophical brief. The vision document provides altitude; this document records reality.

---

## 3. Vision anchor (brief)

STARLAB treats RTS research as a **systems problem first** and an **agent problem second**.

The project is not just about training an agent. It is about building a lab surface where runs, replays, artifacts, benchmarks, and evaluation can be tied together in a governed and inspectable way.

---

## 4. Build posture (brief)

STARLAB is being built to be **clean enough to buy**.

That means the project should become:

- ownable  
- legible  
- separable  
- defensible  
- maintainable  
- low-friction to diligence  

This posture affects licensing, contributor policy, provenance, documentation, dependency hygiene, and public/private boundary decisions.

---

## 5. Current program surface

As of project initialization, STARLAB is defined as:

- a **research substrate**, not a ladder-first bot effort
- **SC2-first**, with future multi-environment potential
- **replay-native** and **benchmark-first**
- **evidence-first**, with milestone-sized validation
- **acquisition-aware**, but not prematurely over-corporatized

### Working posture

- Lab-first  
- Benchmark-first  
- Evidence-first  
- Small-milestone-first  
- Honest non-claims over inflated capability claims  

### Current hardware posture

- **Local GPU:** RTX 5090 Blackwell (where local GPU-backed work is relevant)

---

## 6. Phase map (high level)

The current program is expected to proceed through the following phases.

### Phase I — Governance, Runtime Surface, and Deterministic Run Substrate

Focus:

- repo governance (M00)
- SC2 runtime boundary decision and environment lock (M01)
- deterministic match execution harness (M02+)
- run identity, replay binding, canonical run artifacts (M03–M05)
- environment drift and runtime smoke matrix (M06)

### Phase II — Replay Intake, Provenance, and Data Plane

Focus:

- replay intake policy and provenance enforcement
- parser substrate and metadata/timeline/event extraction
- build-order/economy and combat/scouting planes
- replay slices, bundles, and lineage contracts

### Phase III — State, Representation, and Perception Bridge

Focus:

- canonical state schema and structured pipeline
- observation surface contract
- perceptual bridge prototype
- cross-mode reconciliation and representation audit

### Phase IV — Benchmark Contracts, Baselines, and Evaluation

Focus:

- benchmark contracts and scorecard semantics
- scripted and heuristic baselines
- evaluation runner and tournament harness
- attribution/diagnostics and baseline evidence packs

### Phase V — Learning Paths, Evidence Surfaces, and Flagship Proof

Focus:

- replay-derived imitation baseline
- hierarchical agent interface and first learned agent
- replay explorer / operator evidence surface
- public flagship proof pack

### Phase VI — Expansion Decision and Platform Boundary Review

Focus:

- SC2 substrate review and expansion decision
- platform boundary review and multi-environment charter (earned only)

---

## 7. Milestone table

Planned program arc (33 milestones, M00–M32):

| Milestone | Name | Phase | Status | Tag | Audit Score |
| --------- | ---- | ----- | ------ | --- | ----------- |
| M00 | Governance Bootstrap & Ledger Initialization | I | Complete | v0.0.0-m00 | — |
| M01 | SC2 Runtime Surface Decision & Environment Lock | I | Complete | v0.0.1-m01 | — |
| M02 | Deterministic Match Execution Harness | I | Planned (PR [#3](https://github.com/m-cahill/starlab/pull/3) open) | v0.0.2-m02 | — |
| M03 | Run Identity & Lineage Seed | I | Planned | v0.0.3-m03 | — |
| M04 | Replay Binding to Run Identity | I | Planned | v0.0.4-m04 | — |
| M05 | Canonical Run Artifact v0 | I | Planned | v0.0.5-m05 | — |
| M06 | Environment Drift & Runtime Smoke Matrix | I | Planned | v0.0.6-m06 | — |
| M07 | Replay Intake Policy & Provenance Enforcement | II | Planned | v0.0.7-m07 | — |
| M08 | Replay Parser Substrate | II | Planned | v0.0.8-m08 | — |
| M09 | Replay Metadata Extraction | II | Planned | v0.0.9-m09 | — |
| M10 | Timeline & Event Extraction | II | Planned | v0.0.10-m10 | — |
| M11 | Build-Order & Economy Plane | II | Planned | v0.0.11-m11 | — |
| M12 | Combat, Scouting, and Visibility Windows | II | Planned | v0.0.12-m12 | — |
| M13 | Replay Slice Generator | II | Planned | v0.0.13-m13 | — |
| M14 | Replay Bundle & Lineage Contract v1 | II | Planned | v0.0.14-m14 | — |
| M15 | Canonical State Schema v1 | III | Planned | v0.0.15-m15 | — |
| M16 | Structured State Pipeline | III | Planned | v0.0.16-m16 | — |
| M17 | Observation Surface Contract | III | Planned | v0.0.17-m17 | — |
| M18 | Perceptual Bridge Prototype | III | Planned | v0.0.18-m18 | — |
| M19 | Cross-Mode Reconciliation & Representation Audit | III | Planned | v0.0.19-m19 | — |
| M20 | Benchmark Contract & Scorecard Semantics | IV | Planned | v0.0.20-m20 | — |
| M21 | Scripted Baseline Suite | IV | Planned | v0.0.21-m21 | — |
| M22 | Heuristic Baseline Suite | IV | Planned | v0.0.22-m22 | — |
| M23 | Evaluation Runner & Tournament Harness | IV | Planned | v0.0.23-m23 | — |
| M24 | Attribution, Diagnostics, and Failure Views | IV | Planned | v0.0.24-m24 | — |
| M25 | Baseline Evidence Pack | IV | Planned | v0.0.25-m25 | — |
| M26 | Replay-Derived Imitation Baseline | V | Planned | v0.0.26-m26 | — |
| M27 | Hierarchical Agent Interface Layer | V | Planned | v0.0.27-m27 | — |
| M28 | First Learned Hierarchical Agent | V | Planned | v0.0.28-m28 | — |
| M29 | Replay Explorer / Operator Evidence Surface | V | Planned | v0.0.29-m29 | — |
| M30 | Public Flagship Proof Pack | V | Planned | v0.0.30-m30 | — |
| M31 | SC2 Substrate Review & Expansion Decision | VI | Planned | v0.0.31-m31 | — |
| M32 | Platform Boundary Review & Multi-Environment Charter | VI | Planned | v0.0.32-m32 | — |

**Rule:** milestone names may tighten over time, but scope should remain small and reversible by default.

**M01 note:** M01 is **merged** to `main` (see §18). “Complete” in the table reflects closed milestone scope on `main`, not deterministic match execution (M02).

---

## 8. Milestone intent map

This section exists so each milestone has a stable “why,” not just a title.

| Milestone | Intent |
| --------- | ------ |
| M00 | Make the project legible, governed, and safe to start |
| M01 | Decide the SC2 runtime boundary and lock the environment posture |
| M02 | Prove deterministic, controlled match execution is possible |
| M03 | Seed run identity and lineage primitives |
| M04 | Bind replays to run identity |
| M05 | Establish the first canonical run artifact boundary |
| M06 | Detect environment drift and define runtime smoke expectations |
| M07 | Enforce replay intake and provenance rules |
| M08 | Stand up replay parsing substrate |
| M09 | Extract replay metadata reliably |
| M10 | Extract timelines and event streams |
| M11 | Extract build-order and economy structure |
| M12 | Extract combat, scouting, and visibility windows |
| M13 | Generate reusable replay slices |
| M14 | Package replay bundles with lineage contract v1 |
| M15 | Define canonical state schema v1 |
| M16 | Build structured state pipeline |
| M17 | Define observation surface contract |
| M18 | Prototype perceptual bridge |
| M19 | Reconcile modes and audit representations |
| M20 | Define benchmark contracts and scorecard semantics |
| M21 | Scripted baseline suite |
| M22 | Heuristic baseline suite |
| M23 | Evaluation runner and tournament harness |
| M24 | Attribution, diagnostics, and failure views |
| M25 | Baseline evidence pack |
| M26 | Replay-derived imitation baseline |
| M27 | Hierarchical agent interface layer |
| M28 | First learned hierarchical agent |
| M29 | Replay explorer / operator evidence surface |
| M30 | Public flagship proof pack |
| M31 | SC2 substrate review and expansion decision |
| M32 | Platform boundary review and multi-environment charter |

---

## 9. Governance rules

1. Every milestone must:
   
   - have a plan
   - have explicit scope
   - be evidence-backed
   - be summarized
   - be audited
   - update this document

2. CI must remain truthful.

3. Required checks may not be weakened without explicit audit rationale.

4. Public claims must be bounded and evidence-backed.

5. Licensing, provenance, and contributor ownership decisions must be tracked explicitly.

6. Public/private boundary decisions must not be left implicit.

7. The project should prefer smaller reversible milestones over sprawling implementation waves.

8. This document must be updated after each milestone closeout.

9. **Canonical corpus promotion:** no replay, map, ladder-derived asset, or derived label enters a canonical STARLAB corpus until explicit provenance status and redistribution posture are recorded (see `docs/replay_data_provenance.md` and `docs/rights_register.md`).

---

## 10. Standing invariants

These rules should hold unless explicitly revised through milestone governance.

- STARLAB remains **lab-first**, not ladder-first.
- SC2 remains the initial proving ground until explicitly expanded.
- Replay and artifact surfaces are treated as first-class evidence.
- The project prefers **benchmark integrity** over leaderboard optics.
- The project should not overclaim capabilities.
- The project should remain clean enough for serious diligence.
- Multi-environment expansion is **earned**, not assumed.
- Public docs should preserve historical truth rather than erase it.

### Untrusted boundary rule

The **SC2 client and runtime surface** (game client, replay parser libraries, protocol adapters, and third-party tooling that touches Blizzard assets) is an **untrusted boundary**. STARLAB does not treat vendor or upstream behavior as a semantic guarantee of the lab.

STARLAB-owned claims attach to **STARLAB artifacts, schemas, lineage, evaluation, and governance** — not to upstream quirks.

### Change control for contract-affecting surfaces

Changes to the following require **explicit milestone governance** (plan, scope, ledger update):

- Artifact schemas and serialization rules  
- Canonical state surface definitions  
- Benchmark scorecards and evaluation semantics  
- Rights / provenance posture  
- Public / private boundary  
- Deployment posture (Netlify / Render or successors)  
- Consumer-facing APIs or public artifact contracts  

### Proved vs not yet proved

| Claim | Status |
|-------|--------|
| Canonical ledger exists | Proved (M00) |
| Milestone governance posture and tracked milestone path exist | Proved (M00) |
| Source-available license posture recorded | Proved (M00) |
| Minimal governance CI is truthful | Proved (M00) |
| SC2 runtime boundary decision + environment lock (documented; typed probe) | Proved (M01) |
| Controlled deterministic match execution | Not yet proved (target M02) |
| Replay capture / binding | Not yet proved |
| Canonical run artifacts | Not yet proved |
| Parser substrate | Not yet proved |
| Benchmark integrity | Not yet proved |
| Learning or agent capability | Not yet proved |

**Local harness vs portability:** a **local deterministic harness proof** (same machine, same config, normalized STARLAB artifact hash) is a **narrower** claim than **cross-host reproducibility** or **cross-install portability**. The ledger uses “controlled deterministic match execution” only in the harness-scoped sense once M02 is closed with evidence.

### Assumed vs owned guarantees

| Class | Meaning |
|-------|---------|
| **Assumed** | Upstream SC2 clients, replays, and tools behave as documented by their owners; behavior may change outside STARLAB control. |
| **Owned** | STARLAB artifact integrity, schema validity, lineage records, scorecards (once they exist), governance, CI truthfulness, and public evidence posture under this repository’s policies. |

### Deployment posture (preparatory only)

Future intent (not active in M00):

- **Netlify** — future home for `frontend/` and optionally static docs or evidence.  
- **Render** — future home for `backend/` services.  

M00 records conventions only. See `docs/deployment/deployment_posture.md` and `docs/deployment/env_matrix.md`.

### Deployment readiness is not deployment

M00 establishes hosting **conventions and governance** only. Naming Netlify and Render does **not** imply live sites, production readiness, or rights-cleared public distribution. Public hosting waits on explicit milestone authorization and provenance posture.

---

## 11. Current milestone

### M02 — Deterministic Match Execution Harness

**Status:** **Pre-merge / merge-readiness** — implementation on branch [`m02-deterministic-match-execution-harness`](https://github.com/m-cahill/starlab/tree/m02-deterministic-match-execution-harness); PR [#3](https://github.com/m-cahill/starlab/pull/3) open; **authoritative PR-head CI** run [`24052172714`](https://github.com/m-cahill/starlab/actions/runs/24052172714) (**success**) on PR head `59dcf15e9912c5f6c1920a495150ff03a5a5af7d`. **Local burny×2 determinism evidence** is **not** yet recorded in-repo (see `docs/company_secrets/milestones/M02/`). **Do not** mark “controlled deterministic match execution” as **proved** in §10 until that evidence exists and closeout is completed on `main`.

**Goal:** Build a deterministic match execution harness that proves controlled execution under the M01 runtime boundary — without claiming full replay analytics or benchmark validity.

**Primary references:** `docs/runtime/match_execution_harness.md`, optional dependency group `sc2-harness` (`burnysc2`), CLI `python -m starlab.sc2.run_match`.

**Note:** M00 and M01 closeout details are recorded in §18 and the changelog. Replay binding, canonical run artifacts, benchmark integrity, and **cross-host reproducibility** remain **not** proved in M02.

---

## 12. Open decisions

| ID     | Decision                         | Status   | Target Milestone | Notes                                                              |
| ------ | -------------------------------- | -------- | ---------------- | ------------------------------------------------------------------ |
| OD-001 | License posture                  | Resolved | M00              | Custom source-available terms in `LICENSE` (evaluation/verification); public/private surfaces governed by `docs/public_private_boundary.md` |
| OD-002 | Public/private boundary          | Resolved | M00              | `docs/public_private_boundary.md`                                  |
| OD-003 | Replay/data provenance policy    | Conditionally resolved | M00 / M07+ | Interim policy in `docs/replay_data_provenance.md`; tighten with replay intake (M07) |
| OD-004 | Naming / brand diligence posture | Resolved | M00              | `docs/branding_and_naming.md`                                      |
| OD-005 | SC2 runtime surface selection    | Resolved | M01              | Canonical: SC2API/`s2client-proto` + `s2protocol`; optional `python-sc2` as adapter only; PySC2 deferred — see `docs/runtime/sc2_runtime_surface.md` |
| OD-006 | Rights register format           | Resolved | M00              | `docs/rights_register.md` (canonical); this ledger summarizes      |
| OD-007 | Second-environment posture       | Deferred | M32              | Explicitly not a starting decision                                 |

---

## 13. Risks and constraints

### Early known risks

- SC2 environment brittleness
- replay/data rights ambiguity
- premature abstraction toward multi-game support
- public/private surface drift
- unclear acquisition posture decisions made too late
- accidental dependency or license contamination
- narrative dilution through overexpansion

### Constraint summary

- project should remain milestone-sized
- public docs should stay honest
- acquisition-aware cleanliness should not turn into bureaucracy
- platform ambition should not outrun substrate proof

---

## 14. Strategic value ladder (target framing)

This ledger uses the following strategic value ladder as a planning aid, not a literal market-price claim.

| Tier | Program State                       | Strategic / Platform-Equivalent Value |
| ---- | ----------------------------------- | ------------------------------------- |
| 1    | Prototype / Early Lab               | $0.5M–$2M                             |
| 2    | Full Lab Substrate                  | $2M–$10M                              |
| 3    | Multi-Environment-Capable Substrate | $10M–$25M                             |
| 4    | Community Benchmark Standard        | $25M–$75M                             |
| 5    | Strategic Internal Asset            | $50M–$150M                            |
| 6    | Field-Defining Platform             | $150M–$300M+                          |

**Interpretation:** early value is most likely to appear as **career signal → strategic internal leverage → platform leverage**, not as immediate direct commercialization.

---

## 15. Public evidence posture

STARLAB should prefer evidence that is:

- milestone-tied
- reproducible
- reviewable
- low on hype
- explicit about both proofs and non-proofs

Examples of good evidence:

- tests
- benchmark reports
- replay-linked artifacts
- milestone summaries
- audit notes
- explicit non-claims
- provenance notes
- dependency disclosures

Examples of weak evidence:

- vague capability claims
- anecdotal performance
- architecture claims without milestone proof
- public statements that outrun documentation

---

## 16. Rights / provenance / diligence tracker (starter)

This section starts simple and should become more explicit as the project matures.

| Surface                            | Current posture                                                | Status                 |
| ---------------------------------- | -------------------------------------------------------------- | ---------------------- |
| Code ownership                     | Expected to be first-party and traceable                       | Initial                |
| Documentation ownership            | Expected to be first-party and traceable                       | Initial                |
| SC2 client / Battle.net runtime    | Acquire under Blizzard terms (EULA / AI & ML license as applicable); **not** redistributed via this repo; see `docs/runtime/*` | Governed (M01) |
| SC2 maps / replay packs            | Local-only; **not** committed; rights per Blizzard / pack terms; quarantine if unclear | Governed (M01) |
| Replay/data rights                 | Interim policy in `docs/replay_data_provenance.md`              | Conditionally resolved |
| Third-party dependency obligations | CI: pip-audit + CycloneDX SBOM artifact (`pyproject.toml` dev) | Initial                |
| Public/private split               | `docs/public_private_boundary.md`                              | Initial                |
| Contributor policy                 | `CONTRIBUTING.md`                                              | Initial                |
| License decision                   | Custom source-available (`LICENSE`)                            | Initial                |

---

## 17. Milestone closeout requirements

Every closed milestone should update this ledger with:

1. milestone status
2. merged branch / PR / SHA (if applicable)
3. CI evidence
4. short summary of what was actually proved
5. explicit non-proofs
6. open decisions changed by the milestone
7. any new risks or deferred items
8. changelog entry

**Rule:** a milestone is not fully closed until this file reflects it.

---

## 18. Milestone closeout ledger

This section should be filled as milestones close.

| Milestone | Closeout Date | PR | Merge commit | Notes |
| --------- | ------------- | -- | ------------ | ----- |
| M00       | 2026-04-06    | [#1](https://github.com/m-cahill/starlab/pull/1) | `f9203dd555ea267bc2d72c3470b174ca35a23788` | Governance bootstrap; merged to `main`; see CI evidence below |
| M01       | 2026-04-06    | [#2](https://github.com/m-cahill/starlab/pull/2) | `4a916033f55c6b8c4a582f985233a64ca039ead3` | SC2 runtime surface decision, environment lock docs, `starlab.sc2` probe; OD-005 resolved; merged to `main`; see CI evidence below |

**M00 PR head (pre-merge):** `5dcb6cf6f95af23b58c6af202d58a7bcad1d0b91`

**M00 CI evidence (authoritative)**

| Event | Workflow run | Conclusion | URL |
| ----- | ------------ | ---------- | --- |
| PR #1 head | `24015581129` | success | https://github.com/m-cahill/starlab/actions/runs/24015581129 |
| `main` after merge (`f9203dd…`) | `24015599413` | success | https://github.com/m-cahill/starlab/actions/runs/24015599413 |
| `main` after M00 evidence finalization (`523993e…`) | `24015634285` | success | https://github.com/m-cahill/starlab/actions/runs/24015634285 |

**M00 milestone artifacts:** `docs/company_secrets/milestones/M00/` (`M00_summary.md`, `M00_audit.md`, `M00_run1.md`, etc.)

**M01 merge:** [PR #2](https://github.com/m-cahill/starlab/pull/2) merged **2026-04-06** (UTC `2026-04-06T20:26:27Z`) via **merge commit** `4a916033f55c6b8c4a582f985233a64ca039ead3`. Remote branch `m01-sc2-runtime-surface-env-lock` was **deleted** after merge.

**M01 CI evidence (PR-head runs witnessed before merge)**

Each row is a green `pull_request` run on branch `m01-sc2-runtime-surface-env-lock` at the listed commit (historical record).

| Commit (short) | Workflow run | Conclusion | URL |
| -------------- | ------------ | ---------- | --- |
| `378c864…` | `24048416111` | success | https://github.com/m-cahill/starlab/actions/runs/24048416111 |
| `260c4e0…` | `24048498203` | success | https://github.com/m-cahill/starlab/actions/runs/24048498203 |
| `88b06db…` | `24048576545` | success | https://github.com/m-cahill/starlab/actions/runs/24048576545 |

Further commits on the PR after `88b06db…` had additional green PR-head runs on GitHub before the final merge tip.

**M01 CI evidence (post-merge `main`)**

| Event | Workflow run | Conclusion | URL |
| ----- | ------------ | ---------- | --- |
| `main` after M01 merge (`4a91603…`) | `24049637412` | success | https://github.com/m-cahill/starlab/actions/runs/24049637412 |
| `main` after M01 merge closeout / ledger update (`c920876…`) | `24049868109` | success | https://github.com/m-cahill/starlab/actions/runs/24049868109 |
| `main` after M01 §18 / `M01_run1` post-merge alignment (`aa46fc4…`) | `24049956985` | success | https://github.com/m-cahill/starlab/actions/runs/24049956985 |

*Later documentation-only pushes to `main` re-run CI; additional green runs after the rows above are not milestone events — the merge boundary for M01 remains PR #2 merge commit `4a91603…`.*

*Additional follow-up (ledger commit recording run 3):* `main` @ `8251cef…` — workflow run `24049998835` (success): https://github.com/m-cahill/starlab/actions/runs/24049998835

**M01 milestone artifacts:** `docs/company_secrets/milestones/M01/` (`M01_plan.md`, `M01_toolcalls.md`, `M01_run1.md`, `M01_summary.md`, `M01_audit.md`, optional redacted probe sample, etc.)

---

## 19. Deferred items / future-only tracks

These are intentionally not current default scope.

| ID      | Item                                         | Status   | Notes                                               |
| ------- | -------------------------------------------- | -------- | --------------------------------------------------- |
| FUT-001 | Multi-environment expansion                  | Deferred | Only after SC2 substrate proves itself              |
| FUT-002 | Audio / AURORA-adjacent modality integration | Deferred | Optional sibling influence, not core starting scope |
| FUT-003 | Broader commercialization posture            | Deferred | Not the near-term goal                              |
| FUT-004 | Community benchmark leadership posture       | Deferred | Must be earned by evidence, not declared early      |

---

## 20. Suggested score trend table

This is a placeholder table for future audit tracking once milestones begin closing.

| Milestone | Arch | Governance | Evidence | CI  | Diligence | Docs | Overall |
| --------- | ---- | ---------- | -------- | --- | --------- | ---- | ------- |
| M00       | 3.5  | +          | +        | +   | +         | +    | 4.0     |
| M01       | 3.5  | +          | +        | +   | +         | +    | 4.5     |

---

## 21. README alignment rule

The README should stay shorter and simpler than this file.

- README = front door  
- `docs/starlab.md` = public ledger / living source of truth  
- Vision = thesis and moonshot  
- `docs/bicetb.md` = operating discipline for cleanliness and diligence  

If those documents drift, this file should record the resolution.

---

## 22. Living document rule

This file is the **public-facing source of truth** for STARLAB’s current state.

It should always answer, with minimal ambiguity:

- what STARLAB is
- what phase it is in
- which milestone is current
- which milestones are closed
- what has actually been proved
- what remains open
- what the project is intentionally not doing yet

---

## 23. Changelog

### 2026-04-06 — M02 harness: PR #3 opened (pre-merge; not closed on `main`)

- Opened [PR #3](https://github.com/m-cahill/starlab/pull/3) (**M02: deterministic match execution harness**) from `m02-deterministic-match-execution-harness`; current PR head `59dcf15e9912c5f6c1920a495150ff03a5a5af7d` (closeout-prep + CI reference alignment)
- **Authoritative PR-head CI** for that tip: workflow **CI** run [`24052172714`](https://github.com/m-cahill/starlab/actions/runs/24052172714) — **success** (earlier green runs: `24052043305` on `8884078…`; `24052112581` on `1bd98f1…`)
- **Not merged** to `main` at this changelog entry; **local real-execution / determinism evidence** for M02 remains **pending** (CI is SC2-free by design)
- Milestone artifacts: `M02_run1.md`, `M02_summary.md`, `M02_audit.md` under `docs/company_secrets/milestones/M02/`

### 2026-04-06 — M01 merged to `main` (PR #2)

- Merged [PR #2](https://github.com/m-cahill/starlab/pull/2) to `main` at **2026-04-06T20:26:27Z**; merge commit `4a916033f55c6b8c4a582f985233a64ca039ead3` (merge method: **merge commit**); remote branch `m01-sc2-runtime-surface-env-lock` **deleted**
- Post-merge `main` CI: workflow run `24049637412` (success) on merge commit `4a91603…`: https://github.com/m-cahill/starlab/actions/runs/24049637412
- Follow-up `main` push for merge closeout documentation (`c920876…`): workflow run `24049868109` (success): https://github.com/m-cahill/starlab/actions/runs/24049868109
- Follow-up `main` push aligning §18 second post-merge row and `M01_run1.md` (`aa46fc4…`): workflow run `24049956985` (success): https://github.com/m-cahill/starlab/actions/runs/24049956985
- Follow-up `main` push recording the third post-merge row + `M01_run1` run 3 (`8251cef…`): workflow run `24049998835` (success): https://github.com/m-cahill/starlab/actions/runs/24049998835
- §18 ledger and this changelog updated with merge/post-merge evidence

### 2026-04-06 — M01 closeout (SC2 runtime surface & environment lock)

- Resolved **OD-005**: canonical control/observation boundary = Blizzard SC2 API / `s2client-proto`; canonical replay decode boundary = `s2protocol`; optional `python-sc2` only behind adapter boundaries; PySC2 deferred for substrate — see `docs/runtime/sc2_runtime_surface.md`
- Added `docs/runtime/environment_lock.md` and deterministic `starlab.sc2` path/config probe (`run_probe`, `probe_result_to_json`); **no** SC2 Python packages added in M01
- Updated `docs/rights_register.md`, `docs/replay_data_provenance.md`, 33-milestone ledger map, phase names, and canonical corpus promotion rule
- **Does not claim:** controlled match execution, replay parsing correctness, or benchmark validity (M02+)
- Witnessed PR-head CI runs before merge: `24048416111` (`378c864…`), `24048498203` (`260c4e0…`), `24048576545` (`88b06db…`) — all success

### 2026-04-06 — M00 evidence finalization (PR #1 merged)

- Merged [PR #1](https://github.com/m-cahill/starlab/pull/1); merge commit `f9203dd555ea267bc2d72c3470b174ca35a23788`; PR head `5dcb6cf6f95af23b58c6af202d58a7bcad1d0b91`
- Authoritative CI: PR-head run `24015581129` (success); post-merge `main` run `24015599413` (success); post–evidence-finalization `main` run `24015634285` (success) on `523993edb22938e13bdbf308bb511c204ddd71a6`
- Completed `M00_summary.md`, `M00_audit.md`, `M00_run1.md` under `docs/company_secrets/milestones/M00/`
- Updated §18 closeout ledger and score trend with concrete evidence

### 2026-04-05 — M00 closeout (Governance bootstrap)

- Hardened ledger: untrusted SC2 boundary, change control, proved/not-proved, assumed/owned, deployment posture (Netlify / Render preparatory), “deployment readiness is not deployment”
- Resolved OD-002, OD-004, OD-006; conditionally resolved OD-003 (interim replay policy)
- Added `docs/public_private_boundary.md`, `docs/replay_data_provenance.md`, `docs/rights_register.md`, `docs/branding_and_naming.md`, `docs/deployment/*`, `CONTRIBUTING.md`, `SECURITY.md`
- Seeded `frontend/`, `backend/`, `ops/` placeholders; non-operative Netlify/Render examples
- Python 3.11 dev tooling + GitHub Actions CI (Ruff, format, Mypy, Pytest, pip-audit, CycloneDX SBOM, Gitleaks)
- Milestone artifacts under `docs/company_secrets/milestones/M00/`; M01 stubs seeded
- `.gitignore` narrowed so `docs/company_secrets/milestones/` is trackable; other company_secrets subfolders remain ignored

### 2026-04-05 — Documentation and license alignment

- Aligned ledger with `LICENSE` (source-available, evaluation-only)
- Resolved OD-001; updated rights tracker
- Removed citation artifacts; named `docs/bicetb.md` in authority hierarchy and README alignment

### 2026-04-05 — Initial ledger seed

- Created canonical project ledger
- Established authority hierarchy
- Added phase map and planned milestone table
- Added open decisions and risk tracker
- Added milestone closeout rules
- Added acquisition-aware but concise posture
- Set ledger up for Cursor-based incremental milestone updates
