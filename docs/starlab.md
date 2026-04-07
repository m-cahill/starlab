# STARLAB — Canonical Project Ledger

**Status:** Active — M00–**M08** merged to `main` ([PR #1](https://github.com/m-cahill/starlab/pull/1) through [PR #9](https://github.com/m-cahill/starlab/pull/9)). **M08** merge commit `b99233e807177d65737beaba5246efa67a3edce2` — authoritative post-merge `main` CI on merge push [`24070602968`](https://github.com/m-cahill/starlab/actions/runs/24070602968) (**success**). **M07** merge commit `1c7bb0c0381c0f3c8a3eab354ca53e3e503d8d2a` — authoritative post-merge `main` CI on merge push [`24066550699`](https://github.com/m-cahill/starlab/actions/runs/24066550699) (**success**). **M06** merge commit `4953d7a5bbe0713ba82e03ea8f89da49a2f4147a` — post-merge `main` CI on merge push [`24064229874`](https://github.com/m-cahill/starlab/actions/runs/24064229874) (**success**). **M05** merge commit `bad27db36c135fd772e38dcafa64d6fa59577db0` — post-merge `main` CI [`24062610358`](https://github.com/m-cahill/starlab/actions/runs/24062610358) (**success**). **M05** closeout / ledger push on `main` (`6edeb8af845d9cbfaed5c329c1c9a3398acac9dd`): CI [`24062664914`](https://github.com/m-cahill/starlab/actions/runs/24062664914) (**success**). Follow-up ledger cross-reference (`ebca1e964c0539c78165bfab72c249a2157402cc`): CI [`24062700534`](https://github.com/m-cahill/starlab/actions/runs/24062700534) (**success**) — **not** merge-boundary events. **Replay intake / provenance enforcement** (narrow, M07) and **governed replay parser substrate** (narrow, M08 — deterministic parse artifacts; `s2protocol` isolated) are **proved on `main`**; **stable normalized replay metadata** (public contract, M09), **event/timeline semantics** (M10), **build-order extraction**, **replay↔execution equivalence**, and **benchmark integrity** remain **not** proved.  
**License:** Source-available (evaluation and verification only); see `LICENSE`  
**Governance Model:** Milestone-Driven, CI-Enforced  
**Audit Posture:** Active Governance Signal  
**Primary document:** `docs/starlab.md`

---

## Start Here

1. Read `docs/starlab-vision.md` for the moonshot framing and long-range thesis.  
2. Read `docs/bicetb.md` for licensing, provenance, and diligence posture (“clean enough to buy”).  
3. Read this file for current status, phase structure, milestone history, and project rules.  
4. Read governance docs: `docs/public_private_boundary.md`, `docs/replay_data_provenance.md`, `docs/rights_register.md`, `docs/branding_and_naming.md`, `docs/deployment/deployment_posture.md`, `docs/runtime/sc2_runtime_surface.md`, `docs/runtime/environment_lock.md`, `docs/runtime/match_execution_harness.md` (M02 proof surface), `docs/runtime/run_identity_lineage_seed.md` (M03 run identity / lineage seed contract), `docs/runtime/replay_binding.md` (M04 replay binding contract), `docs/runtime/canonical_run_artifact_v0.md` (M05 canonical run package boundary), `docs/runtime/environment_drift_smoke_matrix.md` (M06 environment drift / smoke matrix contract), `docs/runtime/replay_intake_policy.md` (M07 replay intake / provenance gate), and `docs/runtime/replay_parser_substrate.md` (M08 replay parser substrate contract).  
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
- deterministic match execution harness (**M02** — complete on `main`)
- run identity and lineage seed (**M03** — complete on `main`); replay binding (**M04** — complete on `main`); canonical run artifact v0 (**M05** — complete on `main`)
- environment drift and runtime smoke matrix (**M06** — complete on `main`)

#### Phase I — artifact contracts by milestone (compact)

| Milestone | Primary artifact(s) | Binds to / upstream | Included vs external (Phase I boundary) | Explicitly **not** proved here |
| --------- | -------------------- | --------------------- | ---------------------------------------- | ------------------------------ |
| M02 | `match_execution_proof` (normalized hash / proof record) | M01 runtime boundary + harness | Proof record only (no replay package) | Replay binding, canonical run package, cross-host reproducibility |
| M03 | `run_identity.json`, `lineage_seed.json` | M02 proof + match config (deterministic IDs) | STARLAB JSON artifacts | Replay binding, canonical run artifact v0, benchmarks |
| M04 | `replay_binding.json` | M03 `run_identity` / `lineage_seed` + opaque replay bytes (`replay_content_sha256`) | M03 JSON + `replay_binding.json` (replay bytes hashed, not shipped) | Replay parser semantics, replay↔proof equivalence, canonical run artifact v0, benchmarks |
| M05 | `manifest.json`, `hashes.json`, plus M03/M04 JSON (directory bundle) | M03 + M04 JSON only | **Included:** STARLAB-owned JSON only. **External:** raw replay bytes, raw proof/config (never in bundle) | Parser substrate (M08), full benchmark semantics (later) |
| M06 | `runtime_smoke_matrix.json`, `environment_drift_report.json` | M01 probe JSON; optional M03 `environment_fingerprint` | STARLAB JSON artifacts (fixture-driven in CI) | Replay parser, provenance closure, benchmark integrity, cross-host portability, live SC2 in CI |

#### Phase II — artifact contracts by milestone (compact)

| Milestone | Primary artifact(s) | Binds to / upstream | Included vs external (Phase II boundary) | Explicitly **not** proved here |
| --------- | -------------------- | --------------------- | ---------------------------------------- | ------------------------------ |
| M07 | `replay_intake_receipt.json`, `replay_intake_report.json` | Opaque replay bytes + declared intake metadata; optional M03/M04/M05 JSON | STARLAB JSON artifacts; replay bytes hashed, not parsed | Replay parser semantics, semantic extraction, benchmark integrity, cross-host portability, live SC2 in CI |
| M08 | `replay_parse_receipt.json`, `replay_parse_report.json`, `replay_raw_parse.json` | M07 intake artifacts (optional hash linkage); M04 `replay_binding` (optional); `s2protocol` via adapter | STARLAB JSON; fixture-driven CI default; raw sections + capability flags | Stable normalized metadata contract (M09), timeline/event semantics (M10), broad parser correctness, build-order extraction, benchmark integrity, live SC2 in CI |

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
| M02 | Deterministic Match Execution Harness | I | Complete | v0.0.2-m02 | — |
| M03 | Run Identity & Lineage Seed | I | Complete | v0.0.3-m03 | — |
| M04 | Replay Binding to Run Identity | I | Complete | v0.0.4-m04 | — |
| M05 | Canonical Run Artifact v0 | I | Complete | v0.0.5-m05 | — |
| M06 | Environment Drift & Runtime Smoke Matrix | I | Complete | v0.0.6-m06 | — |
| M07 | Replay Intake Policy & Provenance Enforcement | II | Complete | v0.0.7-m07 | — |
| M08 | Replay Parser Substrate | II | Complete | v0.0.8-m08 | — |
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

**M01 note:** M01 is **merged** to `main` (see §18). “Complete” in the table reflects closed milestone scope on `main`.

**M02 note:** M02 is **merged** to `main` (see §18). “Complete” reflects **bounded harness + deterministic proof artifact + CI** on `main`; the **narrow** same-machine harness claim is documented in `docs/company_secrets/milestones/M02/` (not a cross-host or replay-binding claim).

**M03 note:** M03 is **merged** to `main` (see §18). “Complete” reflects **deterministic run spec / execution / lineage seed IDs**, stable **`run_identity.json` / `lineage_seed.json`** from normalized proof + config (fixtures in CI), and **`starlab/runs/`** + contract doc on `main` — **not** (by itself) replay binding, **not** canonical run artifact v0, **not** benchmark validity. **Replay binding** is **M04** (see §18).

**M04 note:** M04 is **merged** to `main` (see §18). “Complete” reflects **narrow, deterministic `replay_binding.json`** from **opaque replay bytes** + existing M03 artifacts (fixture-driven, **SC2-free** CI) — **not** replay parser correctness, **not** replay semantic equivalence to execution proof, **not** canonical run artifact v0, **not** benchmark validity.

**M05 note:** M05 is **merged** to `main` (see §18). “Complete” reflects **narrow canonical packaging** (`manifest.json` / `hashes.json` + canonical M03/M04 JSON; **no** raw replay bytes, **no** raw proof/config in-bundle) — **not** replay parser substrate, **not** benchmark validity, **not** replay semantic equivalence.

**M06 note:** M06 is **merged** to `main` (see §18). “Complete” reflects **deterministic smoke matrix + environment drift report** from **fixture-driven** M01 probe JSON (optional M03 `environment_fingerprint` hint) — **not** cross-host portability, **not** replay parser correctness, **not** replay provenance finalization, **not** benchmark validity, **not** replay semantic extraction, **not** new live SC2 execution in CI.

**M07 note:** M07 is **merged** to `main` (see §18). “Complete” reflects **bounded replay intake + declared provenance posture** — deterministic `replay_intake_receipt.json` / `replay_intake_report.json` from **opaque** replay bytes + **declared** intake metadata; optional consistency checks against governed M04/M05 artifacts — see `docs/runtime/replay_intake_policy.md`, `starlab/replays/`. **Not** replay parser correctness, **not** replay semantic extraction, **not** build-order extraction, **not** replay↔execution equivalence, **not** benchmark integrity, **not** live SC2 in CI, **not** legal certification of third-party replay rights as a matter of law.

**M08 note:** M08 is **merged** to `main` (see §18). “Complete” reflects **governed replay parser substrate** — deterministic `replay_parse_receipt.json`, `replay_parse_report.json`, `replay_raw_parse.json`; **`s2protocol` isolated** behind `starlab/replays/s2protocol_adapter.py`; **raw parser-owned sections** and **event-stream availability flags** only — see `docs/runtime/replay_parser_substrate.md`, `starlab/replays/parse_replay.py`. **Not** broad replay parser correctness, **not** stable **public** normalized metadata (M09), **not** event/timeline semantics (M10), **not** build-order extraction, **not** replay↔execution equivalence, **not** benchmark integrity, **not** live SC2 in CI, **not** legal certification of replay rights.

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

### Intake status glossary (M07)

| Status | Meaning |
| ------ | ------- |
| `eligible_for_canonical_review` | Declared metadata and optional lineage evidence satisfy the **narrow** review bar for further governance review; **not** automatic corpus promotion. |
| `accepted_local_only` | Structurally valid; suitable for **local/private** experimentation only; **not** sufficient for canonical-review corpus posture. |
| `quarantined` | Structurally valid input, but **policy conflict** or **unsafe** posture (for example **forbidden** redistribution or **evidence conflict**). |
| `rejected` | Hard failure: unreadable replay, invalid metadata, hash mismatch, or malformed linked artifact. |

See `docs/runtime/replay_intake_policy.md`.

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
| Controlled deterministic match execution | **Proved (narrow sense only):** same machine, same committed config, two successful proof-producing runs, matching normalized STARLAB `artifact_hash` — see `docs/company_secrets/milestones/M02/` (M02). **Not** proved: cross-host reproducibility, cross-install portability, or equivalence to replay bytes. |
| Run identity + lineage seed records (deterministic `run_identity.json` / `lineage_seed.json` from proof + config) | **Proved (narrow, M03):** deterministic IDs and stable JSON emission from normalized proof + config inputs — see `docs/runtime/run_identity_lineage_seed.md`, `starlab/runs/`, `docs/company_secrets/milestones/M03/`. **Does not** (by itself) claim replay binding, canonical run artifact v0, or benchmark validity. |
| Replay binding (opaque replay bytes → `replay_binding.json` linked to M03 IDs) | **Proved (narrow, M04):** deterministic `replay_content_sha256` + `replay_binding_id` from M03 `run_identity` / `lineage_seed` + opaque replay file bytes — see `docs/runtime/replay_binding.md`, `starlab/runs/replay_binding.py`, `starlab/runs/bind_replay.py`, `docs/company_secrets/milestones/M04/`. **Does not** claim replay parser correctness, replay↔proof semantic equivalence, replay event extraction, canonical run artifact v0, benchmark validity, cross-host reproducibility, or new live SC2 execution in CI (fixtures only). |
| Canonical run artifacts | **Proved (narrow, M05):** deterministic directory bundle (`manifest.json`, `hashes.json`, canonical M03/M04 JSON only; `run_artifact_id`) — see `docs/runtime/canonical_run_artifact_v0.md`, `starlab/runs/canonical_run_artifact.py`, `starlab/runs/build_canonical_run_artifact.py`, `docs/company_secrets/milestones/M05/`. **Does not** claim replay parser semantics, replay↔proof equivalence, replay event extraction, **raw replay bytes or raw proof/config in the bundle**, benchmark validity, cross-host reproducibility, or new live SC2 execution in CI. |
| Environment drift / runtime smoke matrix | **Proved (narrow, M06):** deterministic `runtime_smoke_matrix.json` + `environment_drift_report.json` from validated M01 probe JSON; optional advisory comparison with M03 `environment_fingerprint` — see `docs/runtime/environment_drift_smoke_matrix.md`, `starlab/sc2/environment_drift.py`, `starlab/sc2/evaluate_environment_drift.py`, `docs/company_secrets/milestones/M06/`. **Does not** claim cross-host portability, cross-install portability, replay parser correctness, replay semantic extraction, replay provenance finalization, benchmark integrity, or new live SC2 execution in CI. |
| Replay intake policy & provenance gate | **Proved (narrow, M07):** deterministic `replay_intake_receipt.json` + `replay_intake_report.json` from opaque replay bytes + declared intake metadata; optional M03/M04/M05 cross-check — see `docs/runtime/replay_intake_policy.md`, `starlab/replays/`, `docs/company_secrets/milestones/M07/`. **Does not** claim replay parser correctness, replay semantic extraction, build-order extraction, replay equivalence to execution proof, benchmark integrity, cross-host portability, live SC2 in CI, or legal certification of third-party rights as a matter of law. |
| Parser substrate (governed replay parse artifacts) | **Proved (narrow, M08):** deterministic `replay_parse_receipt.json`, `replay_parse_report.json`, `replay_raw_parse.json`; deterministic normalization of parser-native output to JSON-safe trees; **`s2protocol` isolated** behind adapter — see `docs/runtime/replay_parser_substrate.md`, `starlab/replays/`, `docs/company_secrets/milestones/M08/`. **Does not** claim broad parser correctness, stable **public** normalized metadata (M09), event/timeline semantics (M10), build-order extraction, replay↔execution equivalence, benchmark integrity, live SC2 in CI, or legal certification of replay rights. |
| Stable normalized replay metadata (public contract) | Not yet proved (M09) |
| Benchmark integrity | Not yet proved |
| Learning or agent capability | Not yet proved |

**Local harness vs portability:** a **local deterministic harness proof** (same machine, same config, normalized STARLAB artifact hash) is a **narrower** claim than **cross-host reproducibility** or **cross-install portability**. The ledger uses “controlled deterministic match execution” **only** in that **narrow harness-scoped** sense for M02.

**Execution / substrate claims (split for audits):**

| Subclaim | Milestone | Notes |
| -------- | --------- | ----- |
| Runtime boundary + environment lock | M01 | Probe + docs; not full execution proof |
| Deterministic match harness + M02 proof artifact | M02 | Narrow same-machine harness claim only |
| Run identity + lineage seed primitives | M03 | **On `main`** — narrow claim; distinct from replay binding and canonical run packaging |
| Replay binding to run identity | M04 | **On `main`** — **narrow** opaque-bytes binding to M03 records; not parser/canonical-run/benchmark claims |
| Canonical run artifact v0 | M05 | **On `main`** — narrow packaging only; see `docs/runtime/canonical_run_artifact_v0.md` |
| Environment drift / smoke matrix | M06 | **On `main`** — fixture-driven probe + drift report; not portability/parser/benchmark claims |
| Replay intake / provenance gate | M07 | **On `main`** — opaque bytes + declared metadata; governed receipts/reports; not parser/build-order/benchmark/live-SC2/legal claims |
| Parser substrate (replay parse artifacts) | M08 | **On `main`** — raw sections + availability flags; deterministic artifacts; not normalized-metadata/event-semantics claims |

### Parser glossary (M08–M10)

| Term | Meaning |
| ---- | ------- |
| **Raw parse blocks** | Parser-owned sections lowered deterministically into `replay_raw_parse.json` (e.g. `header`, `details`, `init_data`, optional `attribute_events`). **M08** exposes structure and normalization — **not** a stable public “game metadata” contract. |
| **Normalized metadata** | A **future public contract** for stable, comparable replay fields derived from raw blocks — **M09** scope, **not** established by M08. |
| **Event semantics** | Ordered interpretation of game/message/tracker streams (timeline, unit births, commands) — **M10+** scope; M08 may record **availability** only. |

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

### M09 — Replay Metadata Extraction

**Status:** **Planned** — **current** milestone; **M08** is **closed** on `main` (see §18). **M08** closeout artifacts live under `docs/company_secrets/milestones/M08/`.

**Goal (high level):** Define and implement a **stable normalized replay metadata** contract derived from M08 raw parse blocks — **without** claiming event/timeline semantics (M10) or benchmark integrity unless separately governed.

**Primary references:** `docs/company_secrets/milestones/M09/M09_plan.md` (stub); `docs/starlab.md` §10 (proved vs not yet proved); `docs/runtime/replay_parser_substrate.md` (M08 substrate baseline).

**Note:** **M08** parser substrate (`replay_parse_receipt.json`, `replay_parse_report.json`, `replay_raw_parse.json`) is **proved on `main`** (narrow). **Normalized metadata as a public contract** is **not** proved until M09 closes.

#### Current milestone — explicit non-claims (standing)

Until a milestone explicitly closes a claim, treat the following as **not proved** for **M09** planning:

- **Event/timeline semantics** (M10).
- **Benchmark integrity** / leaderboard claims (**not** a Phase II default proof).
- **New live SC2 execution proof in CI** (CI remains **fixture-driven** unless a milestone explicitly changes that posture).

---

## 12. Open decisions

| ID     | Decision                         | Status   | Target Milestone | Notes                                                              |
| ------ | -------------------------------- | -------- | ---------------- | ------------------------------------------------------------------ |
| OD-001 | License posture                  | Resolved | M00              | Custom source-available terms in `LICENSE` (evaluation/verification); public/private surfaces governed by `docs/public_private_boundary.md` |
| OD-002 | Public/private boundary          | Resolved | M00              | `docs/public_private_boundary.md`                                  |
| OD-003 | Replay/data provenance policy    | Resolved | M07 | Governed intake gate (`docs/runtime/replay_intake_policy.md`, `starlab/replays/`); interim policy remains in `docs/replay_data_provenance.md` for broader context |
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
| Raw replay bytes (third-party / ladder) | Local-only; **not** committed; rights per Blizzard / pack terms; quarantine if unclear; **M07** records **declared** posture only | Governed (M07) |
| Replay intake receipts / reports (`replay_intake_*.json`) | STARLAB **governed** JSON; operator-declared metadata + policy outcome; **not** legal certification | Governed (M07) |
| Canonical-reviewed corpus assets | **No** corpus promotion without explicit provenance + redistribution posture; see `docs/replay_data_provenance.md`, `docs/rights_register.md`, and M07 intake statuses | Governed (M01 / M07) |
| Replay/data rights (interim policy) | `docs/replay_data_provenance.md` + M07 intake contract | Resolved (M07) |
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
| M02       | 2026-04-06    | [#3](https://github.com/m-cahill/starlab/pull/3) | `53a24a4a6106168afe79e0a70d51a20bfef4ea18` | Deterministic match harness, proof artifact, fake + BurnySc2 adapters; merged to `main`; narrow local harness evidence in `docs/company_secrets/milestones/M02/`; see CI evidence below |
| M03       | 2026-04-07    | [#4](https://github.com/m-cahill/starlab/pull/4) | `6bfe6a7b32a004f62a491bf31573e12cd211118a` | Run identity + lineage seed (`starlab/runs/`), runtime contract, fixtures/tests; merged to `main`; narrow claims only — see CI evidence below |
| M04       | 2026-04-07    | [#5](https://github.com/m-cahill/starlab/pull/5) | `c38de5d920ca9fb18cef46da9be7f0ef812ed7ed` | Replay binding (`replay_binding.json`), `docs/runtime/replay_binding.md`, synthetic replay fixture, tests/CLI; merged to `main`; narrow opaque-bytes claim only — see CI evidence below |
| M05       | 2026-04-07    | [#6](https://github.com/m-cahill/starlab/pull/6) | `bad27db36c135fd772e38dcafa64d6fa59577db0` | Canonical run artifact v0 (`manifest.json` / `hashes.json` + M03/M04 JSON); merged to `main`; narrow packaging only — see CI evidence below |
| M06       | 2026-04-07    | [#7](https://github.com/m-cahill/starlab/pull/7) | `4953d7a5bbe0713ba82e03ea8f89da49a2f4147a` | Environment drift + smoke matrix (`runtime_smoke_matrix.json` / `environment_drift_report.json`); merged to `main`; narrow fixture-driven claims only — see CI evidence below |
| M07       | 2026-04-07    | [#8](https://github.com/m-cahill/starlab/pull/8) | `1c7bb0c0381c0f3c8a3eab354ca53e3e503d8d2a` | Replay intake policy (`replay_intake_receipt.json` / `replay_intake_report.json`); merged to `main`; narrow opaque-bytes + declared-metadata claims only — see CI evidence below |
| M08       | 2026-04-07    | [#9](https://github.com/m-cahill/starlab/pull/9) | `b99233e807177d65737beaba5246efa67a3edce2` | Replay parser substrate (`replay_parse_receipt.json` / `replay_parse_report.json` / `replay_raw_parse.json`); merged to `main`; narrow substrate + deterministic artifacts only — see CI evidence below |

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

**M02 merge:** [PR #3](https://github.com/m-cahill/starlab/pull/3) merged **2026-04-06** (UTC `2026-04-06T23:35:21Z`) via **merge commit** `53a24a4a6106168afe79e0a70d51a20bfef4ea18`. Remote branch `m02-deterministic-match-execution-harness` was **deleted** after merge. Final PR head before merge: `e88ca20424410cd99f834eeec92a5ec5d8034284`.

**M02 CI evidence (PR-head run — authoritative merge gate)**

| Commit (short) | Workflow run | Conclusion | URL |
| -------------- | ------------ | ---------- | --- |
| `e88ca20…` | `24055678613` | success | https://github.com/m-cahill/starlab/actions/runs/24055678613 |

**M02 CI evidence (post-merge `main`)**

| Event | Workflow run | Conclusion | URL |
| ----- | ------------ | ---------- | --- |
| `main` after M02 merge (`53a24a4…`) | `24056523452` | success | https://github.com/m-cahill/starlab/actions/runs/24056523452 |

*M02 closeout documentation push:* `main` @ `d81a0952335cbc93d2144da1c428a42287561793` — workflow run `24056595358` (success): https://github.com/m-cahill/starlab/actions/runs/24056595358

*Further documentation-only pushes to `main` after this row may produce additional green CI runs; distinguish them in §23 if they record ledger-only updates.*

**M02 milestone artifacts:** `docs/company_secrets/milestones/M02/` (`M02_plan.md`, `M02_toolcalls.md`, `M02_run1.md`, `M02_summary.md`, `M02_audit.md`, `M02_local_execution_note.md`, `M02_determinism_check.md`, `M02_execution_proof_redacted.json`, `m02_local_config.json`, etc.)

**M03 merge:** [PR #4](https://github.com/m-cahill/starlab/pull/4) merged **2026-04-07** (UTC `2026-04-07T01:10:32Z`) via **merge commit** `6bfe6a7b32a004f62a491bf31573e12cd211118a`. Remote branch `m03-run-identity-lineage-seed` was **deleted** after merge. Final PR head before merge: `884055c34b78f182c704df5a10a9eced5515fa78`.

**M03 CI evidence (PR-head run — authoritative merge gate)**

| Commit (short) | Workflow run | Conclusion | URL |
| -------------- | ------------ | ---------- | --- |
| `884055c…` | `24059095399` | success | https://github.com/m-cahill/starlab/actions/runs/24059095399 |

**M03 CI evidence (post-merge `main`)**

| Event | Workflow run | Conclusion | URL |
| ----- | ------------ | ---------- | --- |
| `main` after M03 merge (`6bfe6a7…`) | `24059246337` | success | https://github.com/m-cahill/starlab/actions/runs/24059246337 |
| `main` after M03 closeout / ledger + M04 stubs (`43d99f6…`) | `24059294330` | success | https://github.com/m-cahill/starlab/actions/runs/24059294330 |

*Further documentation-only pushes to `main` after these rows may produce additional green CI runs; distinguish them in §23.*

**M03 milestone artifacts:** `docs/company_secrets/milestones/M03/` (`M03_plan.md`, `M03_toolcalls.md`, `M03_run1.md`, `M03_summary.md`, `M03_audit.md`, etc.)

**M04 merge:** [PR #5](https://github.com/m-cahill/starlab/pull/5) merged **2026-04-07** (UTC `2026-04-07T02:17:04Z`) via **merge commit** `c38de5d920ca9fb18cef46da9be7f0ef812ed7ed`. Remote branch `m04-replay-binding-to-run-identity` was **deleted** after merge. Final PR head before merge: `6991978cb35172edda75f721149b1558d7ead226`.

**M04 CI evidence (PR-head run — authoritative merge gate)**

| Commit (short) | Workflow run | Conclusion | URL |
| -------------- | ------------ | ---------- | --- |
| `6991978…` | `24060734950` | success | https://github.com/m-cahill/starlab/actions/runs/24060734950 |

**M04 CI evidence (post-merge `main`)**

| Event | Workflow run | Conclusion | URL |
| ----- | ------------ | ---------- | --- |
| `main` after M04 merge (`c38de5d…`) | `24060997255` | success | https://github.com/m-cahill/starlab/actions/runs/24060997255 |
| `main` after M04 closeout / ledger + M05 stubs (`c099752…`) | `24061285459` | success | https://github.com/m-cahill/starlab/actions/runs/24061285459 |

*Further documentation-only pushes to `main` after these rows may produce additional green CI runs; distinguish them in §23.*

**M04 milestone artifacts:** `docs/company_secrets/milestones/M04/` (`M04_plan.md`, `M04_toolcalls.md`, `M04_run1.md`, `M04_summary.md`, `M04_audit.md`, etc.)

**M05 merge:** [PR #6](https://github.com/m-cahill/starlab/pull/6) merged **2026-04-07** (UTC `2026-04-07T03:20:10Z`) via **merge commit** `bad27db36c135fd772e38dcafa64d6fa59577db0`. Remote branch `m05-canonical-run-artifact-v0` was **deleted** after merge. Final PR head before merge: `53ace08e2ec9d29c780f31593bd945e82e1dfcac`.

**M05 CI evidence (PR-head run — authoritative merge gate)**

| Commit (short) | Workflow run | Conclusion | URL |
| -------------- | ------------ | ---------- | --- |
| `53ace08…` | `24062592376` | success | https://github.com/m-cahill/starlab/actions/runs/24062592376 |

**M05 CI evidence (post-merge `main`)**

| Event | Workflow run | Conclusion | URL |
| ----- | ------------ | ---------- | --- |
| `main` after M05 merge (`bad27db…`) | `24062610358` | success | https://github.com/m-cahill/starlab/actions/runs/24062610358 |
| `main` after M05 closeout / ledger + M06 stubs (`6edeb8a…`) | `24062664914` | success | https://github.com/m-cahill/starlab/actions/runs/24062664914 |

*Further documentation-only pushes to `main` after these rows may produce additional green CI runs (e.g. ledger cross-reference update `ebca1e9…` — run `24062700534`); distinguish them in §23 — **not** merge-boundary events.*

**M05 milestone artifacts:** `docs/company_secrets/milestones/M05/` (`M05_plan.md`, `M05_toolcalls.md`, `M05_run1.md`, `M05_summary.md`, `M05_audit.md`, etc.)

**M06 merge:** [PR #7](https://github.com/m-cahill/starlab/pull/7) merged **2026-04-07** (UTC `2026-04-07T04:26:10Z`) via **merge commit** `4953d7a5bbe0713ba82e03ea8f89da49a2f4147a`. Remote branch `m06-environment-drift-runtime-smoke-matrix` was **deleted** after merge. Final PR head before merge: `6f9ef463f90abe914f3c98c8977d49f8da0102cb`.

**M06 CI evidence (PR-head run — authoritative merge gate)**

| Commit (short) | Workflow run | Conclusion | URL |
| -------------- | ------------ | ---------- | --- |
| `6f9ef46…` | `24064200725` | success | https://github.com/m-cahill/starlab/actions/runs/24064200725 |

**Superseded (not merge authority):** earlier PR-head run `24064181198` failed at **Ruff format** — fixed on tip `6f9ef46…`.

**M06 CI evidence (post-merge `main`)**

| Event | Workflow run | Conclusion | URL |
| ----- | ------------ | ---------- | --- |
| `main` after M06 merge (`4953d7a…`) | `24064229874` | success | https://github.com/m-cahill/starlab/actions/runs/24064229874 |

*Further documentation-only pushes to `main` after these rows may produce additional green CI runs; distinguish them in §23 — **not** merge-boundary events unless they record ledger closeout for M06.*

**M06 milestone artifacts:** `docs/company_secrets/milestones/M06/` (`M06_plan.md`, `M06_toolcalls.md`, `M06_run1.md`, `M06_summary.md`, `M06_audit.md`, etc.)

**M07 merge:** [PR #8](https://github.com/m-cahill/starlab/pull/8) merged **2026-04-07** (UTC `2026-04-07T05:50:09Z`) via **merge commit** `1c7bb0c0381c0f3c8a3eab354ca53e3e503d8d2a`. Remote branch `m07-replay-intake-policy-provenance-enforcement` was **deleted** after merge. Final PR head before merge: `a5188ad88bab688ab40136dea77a8b4d3caa0495`.

**M07 CI evidence (PR-head run — authoritative merge gate)**

| Commit (short) | Workflow run | Conclusion | URL |
| -------------- | ------------ | ---------- | --- |
| `a5188ad…` | `24065819186` | success | https://github.com/m-cahill/starlab/actions/runs/24065819186 |

**M07 CI evidence (post-merge `main`)**

| Event | Workflow run | Conclusion | URL |
| ----- | ------------ | ---------- | --- |
| `main` after M07 merge (`1c7bb0c…`) | `24066550699` | success | https://github.com/m-cahill/starlab/actions/runs/24066550699 |
| `main` after M07 closeout docs (`2ccac7e…`) | `24066606427` | success | https://github.com/m-cahill/starlab/actions/runs/24066606427 |
| `main` after M07 doc CI cross-reference (`20a1870…`) | `24066644075` | success | https://github.com/m-cahill/starlab/actions/runs/24066644075 |

*Rows `24066606427` and `24066644075` are **ledger / documentation only** — **not** merge-boundary events. Merge-boundary post-merge `main` CI for M07 remains `24066550699` on merge commit `1c7bb0c…`.*

*Further documentation-only pushes to `main` after these rows may produce additional green CI runs; distinguish them in §23 — **not** merge-boundary unless the event is a PR merge.*

**M07 milestone artifacts:** `docs/company_secrets/milestones/M07/` (`M07_plan.md`, `M07_toolcalls.md`, `M07_run1.md`, `M07_summary.md`, `M07_audit.md`, etc.)

**M08 merge:** [PR #9](https://github.com/m-cahill/starlab/pull/9) merged **2026-04-07** (UTC `2026-04-07T07:52:12Z`) via **merge commit** `b99233e807177d65737beaba5246efa67a3edce2`. Remote branch `m08-replay-parser-substrate` was **deleted** after merge. Final PR head before merge: `a65fabfa7fd76d94a250208fe20c2c4dfdf57105`.

**M08 CI evidence (PR-head run — authoritative merge gate)**

| Commit (short) | Workflow run | Conclusion | URL |
| -------------- | ------------ | ---------- | --- |
| `a65fabf…` | `24069974048` | success | https://github.com/m-cahill/starlab/actions/runs/24069974048 |

**Superseded (not merge authority):** [`24069652969`](https://github.com/m-cahill/starlab/actions/runs/24069652969) — **failure** at Pytest (M05 golden vs Linux replay hash — CRLF/LF); fixed before final tip.

**M08 CI evidence (post-merge `main`)**

| Event | Workflow run | Conclusion | URL |
| ----- | ------------ | ---------- | --- |
| `main` after M08 merge (`b99233e…`) | `24070602968` | success | https://github.com/m-cahill/starlab/actions/runs/24070602968 |
| `main` after M08 closeout docs (`a089f18…`) | `24070704576` | failure | https://github.com/m-cahill/starlab/actions/runs/24070704576 |
| `main` after M08 governance test fix (`c3b6f2c…`) | `24070774045` | success | https://github.com/m-cahill/starlab/actions/runs/24070774045 |
| `main` after M08 ledger CI record sync (`1cca021…`) | `24070813310` | success | https://github.com/m-cahill/starlab/actions/runs/24070813310 |

*Rows `24070704576`, `24070774045`, and `24070813310` are **not** merge-boundary events — closeout documentation + governance test alignment + ledger CI hygiene after M08 merge. **Authoritative** merge-boundary post-merge `main` CI for M08 remains `24070602968` on merge commit `b99233e…`.*

*Further documentation-only pushes to `main` after these rows may produce additional green CI runs; distinguish them in §23 — **not** merge-boundary unless the event is a PR merge.*

**M08 milestone artifacts:** `docs/company_secrets/milestones/M08/` (`M08_plan.md`, `M08_toolcalls.md`, `M08_run1.md`, `M08_summary.md`, `M08_audit.md`, etc.)

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
| M02       | 3.5  | +          | +        | +   | +         | +    | 4.5     |
| M03       | 3.5  | +          | +        | +   | +         | +    | 4.5     |
| M04       | 3.5  | +          | +        | +   | +         | +    | 4.5     |
| M05       | 3.5  | +          | +        | +   | +         | +    | 4.5     |
| M06       | 3.5  | +          | +        | +   | +         | +    | 4.5     |
| M07       | 3.5  | +          | +        | +   | +         | +    | 4.5     |
| M08       | 3.5  | +          | +        | +   | +         | +    | 4.5     |

**M02 note:** Evidence column reflects **narrow** local harness proof + CI; not benchmark or cross-host certification.

**M03 note:** Evidence column reflects **fixture/proof-driven** identity + lineage seed + CI on `main`; not replay binding, canonical artifact v0, or benchmark certification.

**M04 note:** Evidence column reflects **fixture-driven replay binding** (`replay_binding.json`) + CI on `main`; **not** replay parser semantics, replay↔proof equivalence, canonical run artifact v0, or benchmark certification.

**M05 note:** Evidence column reflects **fixture-driven canonical bundle** (`manifest.json` / `hashes.json` + M03/M04 JSON) **on `main`**; **not** replay parser semantics, raw replay/proof shipping, benchmark validity, or cross-host reproducibility.

**M06 note:** Evidence column reflects **fixture-driven** smoke matrix + drift report + CI on `main`; **not** replay parser semantics, portability certification, benchmark validity, provenance closure, or live SC2 execution in CI.

**M07 note:** Evidence column reflects **fixture-driven** replay intake receipt/report + CI **on `main`**; **not** replay parser semantics, build-order extraction, benchmark validity, live SC2 execution in CI, or legal certification of third-party replay rights as a matter of law.

**M08 note:** Evidence column reflects **fixture-driven** parser substrate + deterministic parse artifacts + CI **on `main`**; **not** stable normalized metadata (M09), event semantics (M10), broad parser correctness, benchmark validity, or live SC2 execution in CI.

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

### 2026-04-07 — M08 merged to `main` (PR #9) + closeout

- Merged [PR #9](https://github.com/m-cahill/starlab/pull/9) to `main` at **2026-04-07T07:52:12Z**; merge commit `b99233e807177d65737beaba5246efa67a3edce2` (merge method: **merge commit**); remote branch `m08-replay-parser-substrate` **deleted**
- Final PR head `a65fabfa7fd76d94a250208fe20c2c4dfdf57105` — **authoritative PR-head CI:** [`24069974048`](https://github.com/m-cahill/starlab/actions/runs/24069974048) (**success**)
- **Authoritative post-merge `main` CI** on merge commit: [`24070602968`](https://github.com/m-cahill/starlab/actions/runs/24070602968) (**success**)
- §7 / §10 / §11 / §18 / §20 / §23 updated: **governed replay parser substrate** (narrow) **proved on `main`**; Phase II artifact row (M08); parser glossary (raw blocks vs normalized metadata vs event semantics); **current milestone** → **M09** (stub only)
- Milestone closeout: `M08_run1.md`, `M08_summary.md`, `M08_audit.md`, `M08_plan.md` (**Status: Complete**), `M08_toolcalls.md`; **M09** remains stub-only (`M09_plan.md`, `M09_toolcalls.md`)
- **Non-merge-boundary** `main` CI — closeout commit `a089f18dfa1306ab041b32430dcbfbf2339eb8de`: [`24070704576`](https://github.com/m-cahill/starlab/actions/runs/24070704576) (**failure** — Pytest: governance test expected §11 **M08**); fix commit `c3b6f2c25efe2252d27d2d78065035f8965edc48`: [`24070774045`](https://github.com/m-cahill/starlab/actions/runs/24070774045) (**success**); ledger CI record commit `1cca0219350237c7288ceb2d5d814bb1b5224a03`: [`24070813310`](https://github.com/m-cahill/starlab/actions/runs/24070813310) (**success**) — **authoritative** merge-boundary post-merge `main` CI remains [`24070602968`](https://github.com/m-cahill/starlab/actions/runs/24070602968) on merge commit `b99233e807177d65737beaba5246efa67a3edce2`

### 2026-04-07 — M07 merged to `main` (PR #8) + closeout

- Merged [PR #8](https://github.com/m-cahill/starlab/pull/8) to `main` at **2026-04-07T05:50:09Z**; merge commit `1c7bb0c0381c0f3c8a3eab354ca53e3e503d8d2a` (merge method: **merge commit**); remote branch `m07-replay-intake-policy-provenance-enforcement` **deleted**
- Final PR head `a5188ad88bab688ab40136dea77a8b4d3caa0495` — **authoritative PR-head CI:** [`24065819186`](https://github.com/m-cahill/starlab/actions/runs/24065819186) (**success**)
- **Authoritative post-merge `main` CI** on merge commit: [`24066550699`](https://github.com/m-cahill/starlab/actions/runs/24066550699) (**success**)
- §7 / §10 / §11 / §16 / §18 / §20 / §23 updated: **replay intake / provenance gate** (narrow) **proved on `main`**; **current milestone** → **M08** (stub only); **replay parser substrate** — **not** proved
- Milestone closeout: `M07_run1.md`, `M07_summary.md`, `M07_audit.md`, `M07_plan.md` (**Status: Complete**), `M07_toolcalls.md`; **M08** remains stub-only (`M08_plan.md`, `M08_toolcalls.md`)
- **Non-merge-boundary** `main` CI — closeout commit `2ccac7ed1d9d3fc3c466916f41f1c4d6e9d6a2cc`: [`24066606427`](https://github.com/m-cahill/starlab/actions/runs/24066606427) (**success**); ledger/CI-ID hygiene commit `20a18706fe0c7338fbe4e1922e1a84ae7dc800d9`: [`24066644075`](https://github.com/m-cahill/starlab/actions/runs/24066644075) (**success**) — both **doc-only**; **authoritative** merge-boundary post-merge `main` CI remains [`24066550699`](https://github.com/m-cahill/starlab/actions/runs/24066550699) on merge commit `1c7bb0c0381c0f3c8a3eab354ca53e3e503d8d2a`

### 2026-04-06 — M07 replay intake policy & provenance enforcement (pre-merge branch; superseded by PR #8 merge)

- **Historical:** development log before **PR #8** merged **2026-04-07**; authoritative merge + CI — see §18 and changelog entry **2026-04-07 — M07 merged to `main` (PR #8) + closeout**
- **Branch:** `m07-replay-intake-policy-provenance-enforcement`; **superseded:** merged via [PR #8](https://github.com/m-cahill/starlab/pull/8)
- **Contract:** `docs/runtime/replay_intake_policy.md`; **policy version** `starlab.replay_intake_policy.v1`
- **Code:** `starlab/replays/` (`intake_models.py`, `intake_policy.py`, `intake_io.py`, `intake_cli.py`); `load_canonical_manifest` in `starlab/runs/canonical_run_artifact.py`
- **Artifacts:** `replay_intake_receipt.json`, `replay_intake_report.json` (deterministic JSON; exit codes 0/2/3/4)
- **Tests:** `tests/test_replay_intake.py`, `tests/test_replay_intake_cli.py`; fixtures `replay_m07_sample.SC2Replay`, `replay_m07_generated.SC2Replay`
- **Ledger:** Phase II artifact-contract row (M07), intake status glossary (§9), rights/provenance tracker split (§16), **OD-003** resolved (M07); **§11** current milestone → **M08**; **M08** stubs under `docs/company_secrets/milestones/M08/`
- **Explicit non-proofs:** replay parser, replay semantic extraction, benchmark integrity, live SC2 in CI, legal certification of third-party rights
- **Closeout docs:** finalized in **2026-04-07** entry after merge — `M07_run1.md`, `M07_summary.md`, `M07_audit.md`, `M07_plan.md` (**Status: Complete**)

### 2026-04-07 — M06 merged to `main` (PR #7) + closeout

- Merged [PR #7](https://github.com/m-cahill/starlab/pull/7) to `main` at **2026-04-07T04:26:10Z**; merge commit `4953d7a5bbe0713ba82e03ea8f89da49a2f4147a` (merge method: **merge commit**); remote branch `m06-environment-drift-runtime-smoke-matrix` **deleted**
- Final PR head `6f9ef463f90abe914f3c98c8977d49f8da0102cb` — authoritative PR-head CI: [`24064200725`](https://github.com/m-cahill/starlab/actions/runs/24064200725) (**success**); superseded failed run [`24064181198`](https://github.com/m-cahill/starlab/actions/runs/24064181198) (Ruff format only — fixed before merge)
- Post-merge `main` CI on merge commit: [`24064229874`](https://github.com/m-cahill/starlab/actions/runs/24064229874) (**success**)
- §10 updated: **environment drift / smoke matrix** (narrow) **proved on `main`** — deterministic `runtime_smoke_matrix.json` + `environment_drift_report.json` from M01 probe surface + optional M03 `environment_fingerprint` hint; **cross-host portability**, **replay parser substrate**, **replay semantic extraction**, **replay provenance finalization**, **benchmark integrity**, **new live SC2 execution in CI** — **not** proved
- M07 stubs seeded: `docs/company_secrets/milestones/M07/M07_plan.md`, `M07_toolcalls.md` — **no** M07 implementation
- Milestone artifacts: `M06_run1.md`, `M06_summary.md`, `M06_audit.md`; contract `docs/runtime/environment_drift_smoke_matrix.md`; modules `starlab/sc2/runtime_smoke_matrix.py`, `environment_drift.py`, `evaluate_environment_drift.py`
- M06 post-closeout documentation push on `main` (`1f5bbc2…`): CI [`24064323510`](https://github.com/m-cahill/starlab/actions/runs/24064323510) (**success**) — **not** a merge-boundary event; ledger / M07 stubs / governance tests

### 2026-04-07 — M05 merged to `main` (PR #6) + closeout

- Merged [PR #6](https://github.com/m-cahill/starlab/pull/6) to `main` at **2026-04-07T03:20:10Z**; merge commit `bad27db36c135fd772e38dcafa64d6fa59577db0` (merge method: **merge commit**); remote branch `m05-canonical-run-artifact-v0` **deleted**
- Final PR head `53ace08e2ec9d29c780f31593bd945e82e1dfcac` — authoritative PR-head CI: [`24062592376`](https://github.com/m-cahill/starlab/actions/runs/24062592376) (**success**)
- Post-merge `main` CI on merge commit: [`24062610358`](https://github.com/m-cahill/starlab/actions/runs/24062610358) (**success**)
- M05 closeout documentation push on `main` (`6edeb8af845d9cbfaed5c329c1c9a3398acac9dd`): CI [`24062664914`](https://github.com/m-cahill/starlab/actions/runs/24062664914) (**success**) — **not** a merge-boundary event; ledger / milestone artifacts / M06 stubs
- M05 §18/§23 post-closeout CI evidence cross-reference (`ebca1e964c0539c78165bfab72c249a2157402cc`): CI [`24062700534`](https://github.com/m-cahill/starlab/actions/runs/24062700534) (**success**) — **not** a merge-boundary event
- §10 updated: **canonical run artifact v0** (narrow) **proved on `main`** — deterministic M03/M04 JSON bundle + `run_artifact_id`; **raw replay bytes and raw proof/config files are not included** in the bundle; **replay parser substrate**, **replay semantic equivalence**, **benchmark validity**, **cross-host reproducibility**, **new live SC2 execution in CI** — **not** proved
- M06 stubs seeded: `docs/company_secrets/milestones/M06/M06_plan.md`, `M06_toolcalls.md` — **no** M06 implementation
- Milestone artifacts: `M05_run1.md`, `M05_summary.md`, `M05_audit.md`; `docs/runtime/run_identity_lineage_seed.md` — note on `seed_from_proof` path/JSON digest portability

### 2026-04-06 — M05 canonical run artifact v0 (pre-merge branch work; superseded by PR #6 merge)

- Development on `m05-canonical-run-artifact-v0`; landed via **PR #6** — see entry above for authoritative merge + CI

### 2026-04-07 — M04 merged to `main` (PR #5) + closeout

- Merged [PR #5](https://github.com/m-cahill/starlab/pull/5) to `main` at **2026-04-07T02:17:04Z**; merge commit `c38de5d920ca9fb18cef46da9be7f0ef812ed7ed` (merge method: **merge commit**); remote branch `m04-replay-binding-to-run-identity` **deleted**
- Final PR head `6991978cb35172edda75f721149b1558d7ead226` — authoritative PR-head CI: [`24060734950`](https://github.com/m-cahill/starlab/actions/runs/24060734950) (**success**)
- Post-merge `main` CI on merge commit: [`24060997255`](https://github.com/m-cahill/starlab/actions/runs/24060997255) (**success**)
- §10 updated: **replay binding** (opaque replay bytes → `replay_binding.json` linked to M03 IDs) **proved on `main` (narrow)**; **canonical run artifact v0**, **replay parser substrate**, **benchmark validity**, **replay semantic equivalence**, **new live SC2 execution in CI** — **not** proved
- M05 stubs seeded: `docs/company_secrets/milestones/M05/M05_plan.md`, `M05_toolcalls.md` — **no** M05 implementation
- M04 closeout documentation push on `main` (`c099752…`): CI [`24061285459`](https://github.com/m-cahill/starlab/actions/runs/24061285459) (**success**) — **not** a merge-boundary event; ledger / milestone artifacts update

### 2026-04-07 — M03 merged to `main` (PR #4) + closeout

- Merged [PR #4](https://github.com/m-cahill/starlab/pull/4) to `main` at **2026-04-07T01:10:32Z**; merge commit `6bfe6a7b32a004f62a491bf31573e12cd211118a` (merge method: **merge commit**); remote branch `m03-run-identity-lineage-seed` **deleted**
- Final PR head `884055c34b78f182c704df5a10a9eced5515fa78` — authoritative PR-head CI: [`24059095399`](https://github.com/m-cahill/starlab/actions/runs/24059095399) (**success**)
- Post-merge `main` CI on merge commit: [`24059246337`](https://github.com/m-cahill/starlab/actions/runs/24059246337) (**success**)
- §10 updated: **run identity + lineage seed** (narrow) **proved on `main`** from proof/config inputs; **replay binding**, **canonical run artifact v0**, **benchmark validity** — **not** proved
- M04 stubs seeded: `docs/company_secrets/milestones/M04/M04_plan.md`, `M04_toolcalls.md` — **no** M04 implementation
- M03 closeout documentation push on `main` (`43d99f6…`): CI [`24059294330`](https://github.com/m-cahill/starlab/actions/runs/24059294330) (**success**)

### 2026-04-06 — M02 merged to `main` (PR #3) + closeout

- Merged [PR #3](https://github.com/m-cahill/starlab/pull/3) to `main` at **2026-04-06T23:35:21Z**; merge commit `53a24a4a6106168afe79e0a70d51a20bfef4ea18` (merge method: **merge commit**); remote branch `m02-deterministic-match-execution-harness` **deleted**
- Final PR head `e88ca20424410cd99f834eeec92a5ec5d8034284` — authoritative PR-head CI: [`24055678613`](https://github.com/m-cahill/starlab/actions/runs/24055678613) (**success**)
- Post-merge `main` CI on merge commit: [`24056523452`](https://github.com/m-cahill/starlab/actions/runs/24056523452) (**success**)
- Closeout doc push on `main` (`d81a095…`): CI [`24056595358`](https://github.com/m-cahill/starlab/actions/runs/24056595358) (**success**)
- Local evidence (narrow same-machine harness): two `burnysc2` runs, matching normalized `artifact_hash` — `docs/company_secrets/milestones/M02/`
- §10 updated: **controlled deterministic match execution** proved **only** in that narrow sense; replay binding, canonical run artifact v0, benchmark validity, cross-host reproducibility — **not** proved
- M03 stubs seeded: `docs/company_secrets/milestones/M03/M03_plan.md`, `M03_toolcalls.md` — **no** M03 implementation

### 2026-04-06 — M02 local evidence recovery (map path + two successful burny runs)

- **Recovery session:** placed a real `.SC2Map` file (pysc2 mini-game `MoveToBeacon`; see `M02_local_execution_note.md`) under gitignored `_local_maps/`; fixed explicit map path resolution to **absolute** paths in `starlab.sc2.maps` so python-sc2 does not mis-resolve repo-relative paths under install `Maps/`.
- **Result:** two `python -m starlab.sc2.run_match … --redact` runs with the same committed config — **exit 0**; **matching** `artifact_hash` recorded in `M02_determinism_check.md`; redacted proof JSON committed as `M02_execution_proof_redacted.json`.
- **Not merged** to `main` in this update; PR **#3** remains the merge vehicle when review completes.

### 2026-04-06 — M02 harness: PR #3 opened (pre-merge; not closed on `main`)

- Opened [PR #3](https://github.com/m-cahill/starlab/pull/3) (**M02: deterministic match execution harness**) from `m02-deterministic-match-execution-harness`; current PR head `290304a3ad3986029879c183f4e40159e7f5792c` (supersede with current branch tip after pushes; early local evidence in commit `5ec0ccb…` was **blocked** — see milestone files)
- **Authoritative PR-head CI** for that tip: workflow **CI** run [`24054732181`](https://github.com/m-cahill/starlab/actions/runs/24054732181) — **success** (earlier green runs on older tips: `24054586191` on `c03691b…`; `24054529734` on `5ec0ccb…`; `24053526611` on `061c212…`; `24053475644` on `bfab038…`; `24053430560` on `3952c40…`; `24053381609` on `08fb582…`; `24053317502` on `10a2b13…`; `24053264747` on `22b2b57…`; `24053218335` on `d80ae12…`; `24052325999` on `f457cf5…`; `24052291273` on `79b341a…`; `24052230417` on `5f5c8a5…`; `24052172714` on `59dcf15…`; `24052112581` on `1bd98f1…`; `24052043305` on `8884078…`)
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
