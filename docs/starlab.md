# STARLAB — Canonical Project Ledger

**Status:** Active — M00–**M20** merged to `main` ([PR #1](https://github.com/m-cahill/starlab/pull/1) through [PR #21](https://github.com/m-cahill/starlab/pull/21)). **M10** merge commit `cb3e581f70f85653477081eb1ef4772229f05983` — merge-push `main` CI [`24104111851`](https://github.com/m-cahill/starlab/actions/runs/24104111851) (**failure** — Mypy); **authoritative green `main`** after M10 repair (`cf2074e10ec8a38b22bd7b75ffeb4ec22a71485b`): [`24104197912`](https://github.com/m-cahill/starlab/actions/runs/24104197912) (**success**). **M09** merge commit `fc9b442d66abe9a2922e93051c7d0a22ccb133d1` — authoritative post-merge `main` CI on merge push [`24101900950`](https://github.com/m-cahill/starlab/actions/runs/24101900950) (**success**). **M08** merge commit `b99233e807177d65737beaba5246efa67a3edce2` — authoritative post-merge `main` CI [`24070602968`](https://github.com/m-cahill/starlab/actions/runs/24070602968) (**success**). **M07** merge commit `1c7bb0c0381c0f3c8a3eab354ca53e3e503d8d2a` — authoritative post-merge `main` CI on merge push [`24066550699`](https://github.com/m-cahill/starlab/actions/runs/24066550699) (**success**). **M06** merge commit `4953d7a5bbe0713ba82e03ea8f89da49a2f4147a` — post-merge `main` CI on merge push [`24064229874`](https://github.com/m-cahill/starlab/actions/runs/24064229874) (**success**). **M05** merge commit `bad27db36c135fd772e38dcafa64d6fa59577db0` — post-merge `main` CI [`24062610358`](https://github.com/m-cahill/starlab/actions/runs/24062610358) (**success**). **M05** closeout / ledger push on `main` (`6edeb8af845d9cbfaed5c329c1c9a3398acac9dd`): CI [`24062664914`](https://github.com/m-cahill/starlab/actions/runs/24062664914) (**success**). Follow-up ledger cross-reference (`ebca1e964c0539c78165bfab72c249a2157402cc`): CI [`24062700534`](https://github.com/m-cahill/starlab/actions/runs/24062700534) (**success**) — **not** merge-boundary events. **Replay intake / provenance enforcement** (narrow, M07), **governed replay parser substrate** (narrow, M08 — deterministic parse artifacts; `s2protocol` isolated), **stable normalized replay metadata** (narrow, M09 — pure extraction over M08 artifacts), and **governed event/timeline extraction** (narrow, M10 — deterministic timeline artifacts; optional `raw_event_streams` on `replay_raw_parse.json` v2) are **proved on `main`** (M10 merge-push CI failed Mypy; **green `main`** restored on repair commit — see §18). **Governed build-order / economy plane** (narrow, M11 — `replay_build_order_economy.json` / `replay_build_order_economy_report.json`; [PR #12](https://github.com/m-cahill/starlab/pull/12) merge commit `38c15302badd49966b17f9195ddb139f6ae9a9b4`; **authoritative green PR-head CI** [`24106029320`](https://github.com/m-cahill/starlab/actions/runs/24106029320) (**success**); **merge-boundary post-merge `main` CI** [`24106124347`](https://github.com/m-cahill/starlab/actions/runs/24106124347) (**success**)) is **proved on `main`**. **Governed combat / scouting / visibility windows** (narrow, M12 — `replay_combat_scouting_visibility.json` / `replay_combat_scouting_visibility_report.json`; [PR #13](https://github.com/m-cahill/starlab/pull/13) merge commit `78528958a616177b564e603c193fb0d7f8af734e`; **authoritative green PR-head CI** [`24109242392`](https://github.com/m-cahill/starlab/actions/runs/24109242392) (**success**); **merge-boundary post-merge `main` CI** [`24109269513`](https://github.com/m-cahill/starlab/actions/runs/24109269513) (**success**)) is **proved on `main`**. **Governed replay slice definitions** (narrow, M13 — `replay_slices.json` / `replay_slices_report.json`; [PR #14](https://github.com/m-cahill/starlab/pull/14) merge commit `f86e36837e81b8552639c5a885a13a773b96215c`; **authoritative green PR-head CI** [`24112526047`](https://github.com/m-cahill/starlab/actions/runs/24112526047) (**success**); **merge-boundary post-merge `main` CI** [`24112556177`](https://github.com/m-cahill/starlab/actions/runs/24112556177) (**success**)) is **proved on `main`**. **Governed replay bundle & lineage contract** (narrow, M14 — `replay_bundle_manifest.json` / `replay_bundle_lineage.json` / `replay_bundle_contents.json`; [PR #15](https://github.com/m-cahill/starlab/pull/15) merge commit `8a0439a9a2970a74f3a5087390fc080f02852246`; **authoritative green PR-head CI** [`24118622373`](https://github.com/m-cahill/starlab/actions/runs/24118622373) (**success**); **merge-boundary post-merge `main` CI** [`24118654909`](https://github.com/m-cahill/starlab/actions/runs/24118654909) (**success**)) is **proved on `main`**. **Governed canonical state schema v1** (narrow, M15 — `canonical_state_schema.json` / `canonical_state_schema_report.json`; [PR #16](https://github.com/m-cahill/starlab/pull/16) merge commit `b0f7132a54508f35d54406011cd3b37bce776927`; **authoritative green PR-head CI** [`24122064141`](https://github.com/m-cahill/starlab/actions/runs/24122064141) (**success**); **merge-boundary post-merge `main` CI** [`24122092800`](https://github.com/m-cahill/starlab/actions/runs/24122092800) (**success**)) is **proved on `main`**. **Governed structured state pipeline** (narrow, M16 — `canonical_state.json` / `canonical_state_report.json` from M14 bundles; [PR #17](https://github.com/m-cahill/starlab/pull/17) merge commit `dd9546f88ebcf9b454498eec83a14d742d17d070`; **authoritative green PR-head CI** [`24160830775`](https://github.com/m-cahill/starlab/actions/runs/24160830775) (**success**); **merge-boundary post-merge `main` CI** [`24160871811`](https://github.com/m-cahill/starlab/actions/runs/24160871811) (**success**)) is **proved on `main`**. **Governed observation surface contract** (narrow, M17 — `observation_surface_schema.json` / `observation_surface_schema_report.json`; [PR #18](https://github.com/m-cahill/starlab/pull/18) merge commit `f63c8e93cb0a2943b9149f4384dbde68b74f9e76`; **authoritative green PR-head CI** [`24164045530`](https://github.com/m-cahill/starlab/actions/runs/24164045530) (**success**); **merge-boundary post-merge `main` CI** [`24164075167`](https://github.com/m-cahill/starlab/actions/runs/24164075167) (**success**)) is **proved on `main`**. **Governed perceptual bridge prototype** (narrow, M18 — deterministic `observation_surface.json` / `observation_surface_report.json` from M16 `canonical_state.json`; [PR #19](https://github.com/m-cahill/starlab/pull/19) merge commit `59d2d6e2af08852d63e0c91a984000c11decfece`; **authoritative green PR-head CI** [`24165977039`](https://github.com/m-cahill/starlab/actions/runs/24165977039) (**success**); **merge-boundary post-merge `main` CI** [`24166004479`](https://github.com/m-cahill/starlab/actions/runs/24166004479) (**success**)) is **proved on `main`**. **Governed cross-mode reconciliation audit** (narrow, M19 — deterministic `observation_reconciliation_audit.json` / `observation_reconciliation_audit_report.json` for one paired M16 `canonical_state.json` + M18 `observation_surface.json`; [PR #20](https://github.com/m-cahill/starlab/pull/20) merge commit `9e855329fc50f4f00db9c857f982d18ef93e4e65`; **authoritative green PR-head CI** [`24168988693`](https://github.com/m-cahill/starlab/actions/runs/24168988693) (**success**); **merge-boundary post-merge `main` CI** [`24169013104`](https://github.com/m-cahill/starlab/actions/runs/24169013104) (**success**); see §18 / `M19_run1.md`) is **proved on `main`**. **Governed benchmark contract + scorecard schemas** (narrow, M20 — `benchmark_contract_schema.json` / `benchmark_contract_schema_report.json` / `benchmark_scorecard_schema.json` / `benchmark_scorecard_schema_report.json`; [PR #21](https://github.com/m-cahill/starlab/pull/21); **authoritative green PR-head CI** [`24173251270`](https://github.com/m-cahill/starlab/actions/runs/24173251270) (**success**); **merge-boundary post-merge `main` CI** [`24173270201`](https://github.com/m-cahill/starlab/actions/runs/24173270201) (**success**); see §18 / `M20_run1.md`) is **proved on `main`**. **Superseded** red PR-head [`24160804226`](https://github.com/m-cahill/starlab/actions/runs/24160804226) (Ruff format — **not** merge authority, **M16**). **Replay↔execution equivalence** and **benchmark integrity** remain **not** proved.  
**License:** Source-available (evaluation and verification only); see `LICENSE`  
**Governance Model:** Milestone-Driven, CI-Enforced  
**Audit Posture:** Active Governance Signal  
**Primary document:** `docs/starlab.md`

---

## Start Here

1. Read `docs/starlab-vision.md` for the moonshot framing and long-range thesis.  
2. Read `docs/bicetb.md` for licensing, provenance, and diligence posture (“clean enough to buy”).  
3. Read this file for current status, phase structure, milestone history, and project rules.  
4. Read governance docs: `docs/public_private_boundary.md`, `docs/replay_data_provenance.md`, `docs/rights_register.md`, `docs/branding_and_naming.md`, `docs/deployment/deployment_posture.md`, `docs/runtime/sc2_runtime_surface.md`, `docs/runtime/environment_lock.md`, `docs/runtime/match_execution_harness.md` (M02 proof surface), `docs/runtime/run_identity_lineage_seed.md` (M03 run identity / lineage seed contract), `docs/runtime/replay_binding.md` (M04 replay binding contract), `docs/runtime/canonical_run_artifact_v0.md` (M05 canonical run package boundary), `docs/runtime/environment_drift_smoke_matrix.md` (M06 environment drift / smoke matrix contract), `docs/runtime/replay_intake_policy.md` (M07 replay intake / provenance gate), `docs/runtime/replay_parser_substrate.md` (M08 replay parser substrate contract), `docs/runtime/replay_metadata_extraction.md` (M09 replay metadata extraction contract), `docs/runtime/replay_timeline_event_extraction.md` (M10 replay timeline / event extraction contract), `docs/runtime/replay_build_order_economy_extraction.md` (M11 build-order / economy contract), `docs/runtime/replay_combat_scouting_visibility_extraction.md` (M12 combat / scouting / visibility contract), and `docs/runtime/replay_slice_generation.md` (M13 replay slice definitions contract), and `docs/runtime/replay_bundle_lineage_contract.md` (M14 replay bundle / lineage packaging contract), and `docs/runtime/canonical_state_schema_v1.md` (M15 canonical state schema contract), and `docs/runtime/canonical_state_pipeline_v1.md` (M16 canonical state pipeline contract), and `docs/runtime/observation_surface_contract_v1.md` (M17 observation surface contract), and `docs/runtime/perceptual_bridge_prototype_v1.md` (M18 perceptual bridge prototype contract), and `docs/runtime/observation_reconciliation_audit_v1.md` (M19 cross-mode reconciliation audit contract), and `docs/runtime/benchmark_contract_scorecard_v1.md` (M20 benchmark contract + scorecard contract).  
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
| M09 | `replay_metadata.json`, `replay_metadata_report.json` | M08 `replay_raw_parse.json` (+ optional parse receipt/report for linkage) | STARLAB JSON; fixture-driven CI default; smaller public metadata surface than raw parse | Event/timeline semantics (M10), build-order extraction (M11), broad parser correctness, benchmark integrity, live SC2 in CI |
| M10 | `replay_timeline.json`, `replay_timeline_report.json` | M08 `replay_raw_parse.json` (v2 `raw_event_streams` + optional lineage receipts) | STARLAB JSON; fixture-driven CI default; bounded semantic kinds | Build-order / economy (M11), combat/scouting, broad parser correctness, replay↔execution equivalence, benchmark integrity, live SC2 in CI |
| M11 | `replay_build_order_economy.json`, `replay_build_order_economy_report.json` | M10 `replay_timeline.json` (primary); optional M08 v2 `replay_raw_parse.json` `raw_event_streams` for entity identity only | STARLAB JSON; fixture-driven CI default; conservative catalog | Combat/scouting (M12), exact resource reconstruction, replay↔execution equivalence, benchmark integrity, live SC2 in CI |
| M12 | `replay_combat_scouting_visibility.json`, `replay_combat_scouting_visibility_report.json` | M10 `replay_timeline.json` + M11 `replay_build_order_economy.json` (required); optional M08 v2 `replay_raw_parse.json` for identity / position / explicit visibility fields only | STARLAB JSON; fixture-driven CI default; conservative combat/scouting/proxy visibility | Replay slice definitions (M13), true fog-of-war certification, replay↔execution equivalence, benchmark integrity, live SC2 in CI |
| M13 | `replay_slices.json`, `replay_slices_report.json` | M10 `replay_timeline.json` + M11 `replay_build_order_economy.json` + M12 `replay_combat_scouting_visibility.json` (required); optional reports/metadata for enrichment only; **no** `replay_raw_parse.json` in M13 v1 | STARLAB JSON; fixture-driven CI default; metadata-only temporal spans | Replay bundle / lineage packaging (M14), raw replay clipping, benchmark integrity, replay↔execution equivalence, fog-of-war truth, live SC2 in CI |
| M14 | `replay_bundle_manifest.json`, `replay_bundle_lineage.json`, `replay_bundle_contents.json` | M09–M13 primary governed JSON (required); optional `*_report.json`; optional M07/M08 receipts for lineage context only | STARLAB JSON only; **no** raw replay bytes, **no** `replay_raw_parse.json`, **no** archive requirement in v1 | Structured state pipeline (M16+), replay↔execution equivalence, benchmark integrity, live SC2 in CI |

#### Phase III — artifact contracts by milestone (compact)

| Milestone | Primary artifact(s) | Binds to / upstream | Included vs external (Phase III boundary) | Explicitly **not** proved here |
| --------- | -------------------- | --------------------- | ---------------------------------------- | ------------------------------ |
| M15 | `canonical_state_schema.json`, `canonical_state_schema_report.json` | JSON Schema + report for one **canonical state frame** at one `gameloop`; semantics bounded to M09–M14 replay-derived posture (counts, categories, proxy visibility — not exact banked resources or fog-of-war truth) | STARLAB JSON; emitted deterministically; validated in CI with `jsonschema`; **no** `s2protocol`, **no** parser CLI, **no** raw replay bytes in M15 modules | Replay-to-state **materialization** (M16), observation surface contract (M17), perceptual bridge (M18), replay↔execution equivalence, benchmark integrity, live SC2 in CI |
| M16 | `canonical_state.json`, `canonical_state_report.json` | M14 bundle (`replay_bundle_*.json`) + M09–M13 primary JSON; validates emitted state against M15 schema; one frame per CLI invocation | STARLAB JSON; **no** raw replay bytes, **no** `replay_raw_parse.json`, **no** `s2protocol` in M16 modules | Observation surface (M17), perceptual bridge (M18), multi-frame tensors / action masks, replay↔execution equivalence, benchmark integrity, exact banked resources, certified fog-of-war truth, live SC2 in CI |
| M17 | `observation_surface_schema.json`, `observation_surface_schema_report.json` | M16 **`canonical_state.json`** (semantic upstream for observation design); one **player-relative** observation frame at one `gameloop`; optional `canonical_state_report.json` for provenance hashes only | STARLAB JSON; emitted deterministically; validated in CI with `jsonschema`; **no** raw replay bytes, **no** `replay_raw_parse.json`, **no** `s2protocol`, **no** M14 bundle load in M17 modules, **no** canonical→observation **materialization** pipeline | Perceptual bridge prototype (M18), tensor materialization, replay↔execution equivalence, benchmark integrity, exact resources, certified fog-of-war truth, mask legality computation, live SC2 in CI |
| M18 | `observation_surface.json`, `observation_surface_report.json` | M16 **`canonical_state.json`** (required); optional **`canonical_state_report.json`** for hash cross-check + warning propagation; one player-relative observation frame per CLI invocation | STARLAB JSON; validates emitted observation against **M17** JSON Schema; **no** M14 bundle load, **no** raw replay bytes, **no** `replay_raw_parse.json`, **no** `s2protocol` in M18 observation modules | Full mask legality / SC2 action coverage, multi-frame tensors, replay↔execution equivalence, benchmark integrity, certified fog-of-war truth, live SC2 in CI |
| M19 | `observation_reconciliation_audit.json`, `observation_reconciliation_audit_report.json` | One M16 **`canonical_state.json`** + one M18 **`observation_surface.json`** (same `gameloop` / `perspective_player_index`); optional **`canonical_state_report.json`** and **`observation_surface_report.json`** for hash cross-checks + upstream warnings | STARLAB JSON; **no** replay parsing, **no** M14 bundle load, **no** `s2protocol` in M19 observation modules | Benchmark integrity, replay↔execution equivalence, certified fog-of-war truth, live SC2 in CI, **M20** benchmark contract semantics |

#### Phase IV — artifact contracts by milestone (compact)

| Milestone | Primary artifact(s) | Binds to / upstream | Included vs external (Phase IV boundary) | Explicitly **not** proved here |
| --------- | -------------------- | --------------------- | ---------------------------------------- | ------------------------------ |
| M20 | `benchmark_contract_schema.json`, `benchmark_contract_schema_report.json`, `benchmark_scorecard_schema.json`, `benchmark_scorecard_schema_report.json` | Governed JSON Schemas + reports for one benchmark contract and one scorecard (`jsonschema` validation); optional fixture hashes in reports | STARLAB JSON; **no** `starlab.replays`, **no** `starlab.sc2`, **no** `s2protocol` in M20 `starlab/benchmarks/` modules | Scripted baselines (**M21**), heuristic baselines (**M22**), evaluation runner (**M23**), tournament harness, benchmark integrity, replay↔execution equivalence, live SC2 in CI |

**Phase II slice / bundle boundary (M13 vs M14):** an M13 **slice** is a **metadata-defined temporal span** over already-governed JSON (addressable `[start_gameloop, end_gameloop]` with lineage). **M14** is where **bundle packaging** and **lineage contract v1** for replay bundles belong — not M13. M13 does not ship clipped replay bytes or M14-style bundles.

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
| M09 | Replay Metadata Extraction | II | Complete | v0.0.9-m09 | — |
| M10 | Timeline & Event Extraction | II | Complete | v0.0.10-m10 | — |
| M11 | Build-Order & Economy Plane | II | Complete | v0.0.11-m11 | — |
| M12 | Combat, Scouting, and Visibility Windows | II | Complete | v0.0.12-m12 | — |
| M13 | Replay Slice Generator | II | Complete | v0.0.13-m13 | — |
| M14 | Replay Bundle & Lineage Contract v1 | II | Complete | v0.0.14-m14 | — |
| M15 | Canonical State Schema v1 | III | Complete | v0.0.15-m15 | — |
| M16 | Structured State Pipeline | III | Complete | v0.0.16-m16 | — |
| M17 | Observation Surface Contract | III | Complete | v0.0.17-m17 | — |
| M18 | Perceptual Bridge Prototype | III | Complete | v0.0.18-m18 | — |
| M19 | Cross-Mode Reconciliation & Representation Audit | III | Complete | v0.0.19-m19 | — |
| M20 | Benchmark Contract & Scorecard Semantics | IV | Complete | v0.0.20-m20 | — |
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

**M08 note:** M08 is **merged** to `main` (see §18). “Complete” reflects **governed replay parser substrate** — deterministic `replay_parse_receipt.json`, `replay_parse_report.json`, `replay_raw_parse.json`; **`s2protocol` isolated** behind `starlab/replays/s2protocol_adapter.py`; **raw parser-owned sections** and **event-stream availability flags** only — see `docs/runtime/replay_parser_substrate.md`, `starlab/replays/parse_replay.py`. **Not** broad replay parser correctness, **not** the **public** normalized metadata contract by itself (that is **M09**), **not** event/timeline semantics (M10), **not** build-order extraction, **not** replay↔execution equivalence, **not** benchmark integrity, **not** live SC2 in CI, **not** legal certification of replay rights.

**M09 note:** M09 is **merged** to `main` (see §18). “Complete” reflects **stable normalized replay metadata** — deterministic `replay_metadata.json`, `replay_metadata_report.json` from M08 `replay_raw_parse.json` (optional parse receipt/report linkage); **no** `s2protocol` in M09 — see `docs/runtime/replay_metadata_extraction.md`, `starlab/replays/extract_replay_metadata.py`. **Not** event/timeline semantics (M10), **not** build-order extraction (M11), **not** replay↔execution equivalence, **not** benchmark integrity, **not** broad Blizzard parser correctness beyond the explicit mapping, **not** live SC2 in CI, **not** legal certification of replay rights.

**M10 note:** M10 is **merged** to `main` (see §18). “Complete” reflects **governed timeline & event extraction** — deterministic `replay_timeline.json`, `replay_timeline_report.json`; `replay_raw_parse.json` may use schema `starlab.replay_raw_parse.v2` with M10-owned `raw_event_streams` lowered inside the existing parser boundary; **merged timeline order is a deterministic canonicalization policy, not a proof of exact intra-gameloop causality** — see `docs/runtime/replay_timeline_event_extraction.md`, `starlab/replays/extract_replay_timeline.py`. **Not** build-order / economy (M11), **not** combat/scouting semantics, **not** benchmark integrity, **not** broad upstream parser certification, **not** live SC2 in CI, **not** player display names or raw chat text in the public timeline contract.

**M11 note:** M11 is **merged** to `main` (see §18). “Complete” reflects **governed build-order / economy extraction** — deterministic `replay_build_order_economy.json`, `replay_build_order_economy_report.json` from M10 `replay_timeline.json` with optional supplemental `replay_raw_parse.json` v2 `raw_event_streams` for entity identity only; **no** `s2protocol` in M11 — see `docs/runtime/replay_build_order_economy_extraction.md`, `starlab/replays/extract_replay_build_order_economy.py`. **Not** combat/scouting (M12), **not** exact resource reconstruction, **not** replay↔execution equivalence, **not** benchmark integrity, **not** broad upstream parser certification, **not** live SC2 in CI, **not** legal certification of replay rights.

**M12 note:** M12 is **merged** to `main` (see §18). “Complete” reflects **governed combat / scouting / visibility extraction** — deterministic `replay_combat_scouting_visibility.json`, `replay_combat_scouting_visibility_report.json` from M10 `replay_timeline.json` + M11 `replay_build_order_economy.json` with optional supplemental `replay_raw_parse.json` v2 for identity / position / explicit visibility fields only; **no** `s2protocol` in M12 — see `docs/runtime/replay_combat_scouting_visibility_extraction.md`, `starlab/replays/extract_replay_combat_scouting_visibility.py`. **Not** replay slice **definition artifacts** (M13), **not** replay bundle / lineage packaging (M14), **not** true fog-of-war certification, **not** replay↔execution equivalence, **not** benchmark integrity, **not** live SC2 in CI, **not** legal certification of replay rights.

**M13 note:** M13 is **merged** to `main` (see §18). “Complete” reflects **governed replay slice definitions** — deterministic `replay_slices.json`, `replay_slices_report.json` from M10+M11+M12 governed JSON with lineage checks; **no** `replay_raw_parse.json` in M13 v1; **no** `s2protocol` in M13 modules — see `docs/runtime/replay_slice_generation.md`, `starlab/replays/extract_replay_slices.py`. **Not** raw replay clipping, **not** benchmark integrity, **not** replay↔execution equivalence, **not** fog-of-war truth, **not** live SC2 in CI, **not** legal certification of replay rights; **not** M14-style bundle packaging (M14 is a separate milestone).

**M14 note:** M14 is **merged** to `main` (see §18). “Complete” reflects **governed replay bundle packaging + lineage contract v1** — deterministic `replay_bundle_manifest.json`, `replay_bundle_lineage.json`, `replay_bundle_contents.json` over M09–M13 primary governed JSON (+ optional reports); **no** raw replay bytes, **no** `replay_raw_parse.json` in bundle, **no** `s2protocol` in M14 modules — see `docs/runtime/replay_bundle_lineage_contract.md`, `starlab/replays/extract_replay_bundle.py`. **Not** raw replay clipping, **not** replay↔execution equivalence, **not** benchmark integrity, **not** live SC2 in CI, **not** legal certification of replay rights, **not** structured state pipeline (**M16**).

**M15 note:** M15 is **merged** to `main` (see §18). “Complete” reflects **governed canonical state schema v1** — deterministic `canonical_state_schema.json` + `canonical_state_schema_report.json`, fixture validation with **`jsonschema`**, runtime contract `docs/runtime/canonical_state_schema_v1.md`, product code under `starlab/state/`; **no** replay-to-state materialization, **no** `s2protocol`, **no** raw replay bytes in M15 modules — see §6 Phase III artifact row. **Not** structured state pipeline (**M16**), observation surface (**M17**), perceptual bridge (**M18**), replay↔execution equivalence, benchmark integrity, live SC2 in CI, exact mineral/gas bank reconstruction (M11 non-claim extends to schema field choices), or certified fog-of-war truth (M12 non-claim extends to visibility fields).

**M16 note:** M16 is **merged** to `main` (see §18). “Complete” reflects **governed structured state pipeline** — deterministic `canonical_state.json` + `canonical_state_report.json` from a **complete M14 replay bundle** at one requested `gameloop`, **`jsonschema`** validation against M15 schema, runtime contract `docs/runtime/canonical_state_pipeline_v1.md`, pipeline modules + CLI under `starlab/state/`; **no** raw replay bytes, **no** `replay_raw_parse.json`, **no** `s2protocol` in M16 modules — see §6 Phase III artifact row. **Not** observation surface (**M17**), perceptual bridge (**M18**), multi-frame tensors / action masks, replay↔execution equivalence, benchmark integrity, exact banked resource truth beyond prior bounded planes, certified fog-of-war truth, or live SC2 in CI.

**M17 note:** M17 is **merged** to `main` (see §18). “Complete” reflects **governed observation surface contract v1** — deterministic `observation_surface_schema.json` + `observation_surface_schema_report.json`, runtime contract `docs/runtime/observation_surface_contract_v1.md`, contract modules under `starlab/observation/`; **semantic upstream is M16 `canonical_state.json`** (not replay bundles directly); **no** canonical-state→observation **materialization** in M17 scope (that narrow proof is **M18**), **no** replay parsing / bundle loading in M17 contract modules — see §6 Phase III artifact row. **Not** mask legality computation, full SC2 action coverage, benchmark integrity, replay↔execution equivalence, exact banked resources, certified fog-of-war truth, or live SC2 in CI.

**M18 note:** M18 is **merged** to `main` (see §18). “Complete” reflects **governed perceptual bridge prototype** — deterministic `observation_surface.json` + `observation_surface_report.json` from one M16 `canonical_state.json` per CLI invocation, optional `canonical_state_report.json` provenance cross-check, **`jsonschema`** validation against the M17 observation schema, runtime contract `docs/runtime/perceptual_bridge_prototype_v1.md`, materialization modules + CLI under `starlab/observation/`; **no** replay parsing, **no** M14 bundle load, **no** `s2protocol` in M18 observation modules — see §6 Phase III artifact row. **Not** full action legality, benchmark integrity, replay↔execution equivalence, certified fog-of-war truth, exact banked resources beyond prior bounded planes, live SC2 in CI, or **M19** cross-mode reconciliation (M19 is a separate proof).

**M19 note:** M19 is **merged** to `main` (see §18). “Complete” reflects **governed cross-mode reconciliation audit** — deterministic `observation_reconciliation_audit.json` + `observation_reconciliation_audit_report.json` from one paired M16 `canonical_state.json` + M18 `observation_surface.json` per CLI invocation, optional `canonical_state_report.json` and `observation_surface_report.json` provenance cross-checks, runtime contract `docs/runtime/observation_reconciliation_audit_v1.md`, audit modules + CLI under `starlab/observation/`; **no** replay parsing, **no** M14 bundle load, **no** `s2protocol` in M19 observation modules — see §6 Phase III artifact row. **Not** action legality upgrades, benchmark integrity, replay↔execution equivalence, certified fog-of-war truth, live SC2 in CI, or **M20** benchmark contract semantics.

**M20 note:** M20 is **merged** to `main` (see §18). “Complete” reflects **governed benchmark contract + scorecard JSON Schemas** — deterministic `benchmark_contract_schema.json` + `benchmark_contract_schema_report.json` + `benchmark_scorecard_schema.json` + `benchmark_scorecard_schema_report.json`, fixture-backed validation with `jsonschema`, runtime contract `docs/runtime/benchmark_contract_scorecard_v1.md`, modules + CLI under `starlab/benchmarks/`; **no** `starlab.replays`, **no** `starlab.sc2`, **no** `s2protocol` in M20 benchmark modules — see §6 Phase IV artifact row. **Not** scripted baselines (**M21**), heuristic baselines (**M22**), evaluation runner (**M23**), tournament harness, benchmark integrity, replay↔execution equivalence, or live SC2 in CI.

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
| M16 | Materialize one canonical state frame per gameloop from M14 bundles |
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
| Parser substrate (governed replay parse artifacts) | **Proved (narrow, M08):** deterministic `replay_parse_receipt.json`, `replay_parse_report.json`, `replay_raw_parse.json`; deterministic normalization of parser-native output to JSON-safe trees; **`s2protocol` isolated** behind adapter — see `docs/runtime/replay_parser_substrate.md`, `starlab/replays/`, `docs/company_secrets/milestones/M08/`. **Does not** claim broad parser correctness, stable **public** normalized metadata (delivered in **M09**), event/timeline semantics (M10), build-order extraction, replay↔execution equivalence, benchmark integrity, live SC2 in CI, or legal certification of replay rights. |
| Stable normalized replay metadata (public contract) | **Proved (narrow, M09):** deterministic `replay_metadata.json` + `replay_metadata_report.json` from M08 `replay_raw_parse.json` (optional parse receipt/report linkage); **no** `s2protocol` in M09 — see `docs/runtime/replay_metadata_extraction.md`, `starlab/replays/`, `docs/company_secrets/milestones/M09/`. **Does not** claim event/timeline semantics (M10), build-order extraction (M11), replay↔execution equivalence, benchmark integrity, broad Blizzard parser correctness beyond the mapping, live SC2 in CI, or legal certification of replay rights. |
| Governed replay timeline (public contract) | **Proved (narrow, M10):** deterministic `replay_timeline.json` + `replay_timeline_report.json` from `replay_raw_parse.json` (v1 or v2; v2 includes `raw_event_streams`); fixture-driven CI — see `docs/runtime/replay_timeline_event_extraction.md`, `starlab/replays/`, `docs/company_secrets/milestones/M10/`. **Does not** claim build-order/economy (that is **M11**), combat/scouting, benchmark integrity, upstream semantic certification, replay↔execution equivalence, live SC2 in CI, or legal certification of replay rights. |
| Governed build-order / economy plane | **Proved (narrow, M11):** deterministic `replay_build_order_economy.json` + `replay_build_order_economy_report.json` from M10 `replay_timeline.json` with optional supplemental `replay_raw_parse.json` v2 identity lookup only — see `docs/runtime/replay_build_order_economy_extraction.md`, `starlab/replays/`, `docs/company_secrets/milestones/M11/`. **Does not** claim combat/scouting (M12), exact resource reconstruction, replay↔execution equivalence, benchmark integrity, live SC2 in CI, or legal certification of replay rights. |
| Governed combat / scouting / visibility plane | **Proved (narrow, M12):** deterministic `replay_combat_scouting_visibility.json` + `replay_combat_scouting_visibility_report.json` from M10 `replay_timeline.json` + M11 `replay_build_order_economy.json` with optional supplemental `replay_raw_parse.json` v2 for identity / position / explicit visibility fields only — see `docs/runtime/replay_combat_scouting_visibility_extraction.md`, `starlab/replays/`, `docs/company_secrets/milestones/M12/`. **Does not** claim replay slice definition artifacts (M13), replay bundle packaging (M14), true fog-of-war certification, replay↔execution equivalence, benchmark integrity, live SC2 in CI, or legal certification of replay rights. |
| Governed replay slice definitions (metadata-only temporal spans) | **Proved (narrow, M13):** deterministic `replay_slices.json` + `replay_slices_report.json` from M10+M11+M12 governed JSON with lineage; **no** `replay_raw_parse.json` in M13 v1 — see `docs/runtime/replay_slice_generation.md`, `starlab/replays/`, `docs/company_secrets/milestones/M13/`. **Does not** claim raw replay clipping, benchmark integrity, replay↔execution equivalence, fog-of-war truth, live SC2 in CI, legal certification of replay rights, or **M14** replay bundle / lineage packaging. |
| Replay bundle & lineage packaging (manifest + graph + inventory) | **Proved (narrow, M14):** deterministic `replay_bundle_manifest.json` + `replay_bundle_lineage.json` + `replay_bundle_contents.json` over M09–M13 primary governed JSON (+ optional `*_report.json`); **no** raw replay bytes, **no** `replay_raw_parse.json` in bundle, **no** archive requirement in v1 — see `docs/runtime/replay_bundle_lineage_contract.md`, `starlab/replays/`, `docs/company_secrets/milestones/M14/`. **`bundle_id` / `lineage_root`** are **packaging identities only** — **not** replay↔execution equivalence, benchmark integrity, live SC2 in CI, canonical state semantics, or legal certification of replay rights. |
| Canonical state schema (single frame) + validation | **Proved (narrow, M15):** deterministic `canonical_state_schema.json` + `canonical_state_schema_report.json`; validation of example state JSON against the schema (`jsonschema`); contract `docs/runtime/canonical_state_schema_v1.md`, `starlab/state/` — see `docs/company_secrets/milestones/M15/`. **Does not** prove replay-to-state **materialization** (M16), observation surface (M17), perceptual bridge (M18), stronger economy or visibility semantics than M11/M12, replay↔execution equivalence, benchmark integrity, or live SC2 in CI. |
| Structured state pipeline (one frame from M14 bundle) | **Proved (narrow, M16):** deterministic `canonical_state.json` + `canonical_state_report.json` from a **complete M14 replay bundle** + M09–M13 primary JSON at one requested `gameloop`; validates against M15 schema; contract `docs/runtime/canonical_state_pipeline_v1.md`, `starlab/state/` — see `docs/company_secrets/milestones/M16/`. **Does not** prove agent-facing **observation surface contract** (M17), perceptual bridge (M18), multi-frame sequences, replay↔execution equivalence, benchmark integrity, exact banked mineral/gas truth beyond prior bounded planes, certified fog-of-war truth, or live SC2 in CI. |
| Observation surface contract (single frame, JSON Schema + validation) | **Proved (narrow, M17):** deterministic `observation_surface_schema.json` + `observation_surface_schema_report.json`; validation of example observation JSON against the schema (`jsonschema`); contract `docs/runtime/observation_surface_contract_v1.md`, `starlab/observation/` — semantic upstream is **M16 `canonical_state.json`** (not replay bundles directly). **Does not** prove canonical-state→observation **materialization** (that is **M18**), mask **legality** / dynamic mask generation, full SC2 action coverage, replay↔execution equivalence, benchmark integrity, exact banked resources, certified fog-of-war truth, or live SC2 in CI. |
| Prototype perceptual bridge (M16 canonical state → one M17-shaped observation instance) | **Proved (narrow, M18):** deterministic `observation_surface.json` + `observation_surface_report.json` per CLI invocation from one `canonical_state.json`; optional `canonical_state_report.json` hash cross-check; validates emitted observation against M17 schema; contract `docs/runtime/perceptual_bridge_prototype_v1.md`, materialization modules under `starlab/observation/` — **no** replay parsing or M14 bundle load in those modules. **Does not** prove full action legality, benchmark integrity, replay↔execution equivalence, certified fog-of-war truth, exact banked resources beyond prior bounded planes, multi-frame tensors, live SC2 in CI, or **M19** cross-mode reconciliation (M19 is a separate proof). |
| Cross-mode reconciliation audit (canonical state vs observation instance) | **Proved (narrow, M19):** deterministic `observation_reconciliation_audit.json` + `observation_reconciliation_audit_report.json` per CLI invocation from paired `canonical_state.json` + `observation_surface.json`; optional upstream reports; contract `docs/runtime/observation_reconciliation_audit_v1.md`, audit modules under `starlab/observation/` — **no** replay parsing or M14 bundle load in M19 modules. **Does not** prove benchmark integrity, replay↔execution equivalence, certified fog-of-war truth, live SC2 in CI, or **M20** benchmark contract semantics. |
| Benchmark contract + scorecard schemas | **Proved (narrow, M20):** deterministic `benchmark_contract_schema.json` + `benchmark_contract_schema_report.json` + `benchmark_scorecard_schema.json` + `benchmark_scorecard_schema_report.json`; fixture validation with `jsonschema`; contract `docs/runtime/benchmark_contract_scorecard_v1.md`, modules under `starlab/benchmarks/` — **no** `starlab.replays`, **no** `starlab.sc2`, **no** `s2protocol` in M20 benchmark modules. **Does not** prove benchmark integrity, scripted/heuristic baselines (**M21–M22**), evaluation runner (**M23**), replay↔execution equivalence, or live SC2 in CI. |
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
| Normalized replay metadata (public contract) | M09 | **On `main`** — small deterministic projection from M08 raw parse; not event semantics or build-order claims |
| Governed timeline / event extraction | M10 | **On `main`** — bounded semantic kinds + deterministic merge; not build-order or benchmark claims |
| Build-order / economy plane | M11 | **On `main`** — narrow extraction over timeline (+ optional raw-parse identity); not combat/scouting or benchmark claims |
| Combat / scouting / visibility plane | M12 | **On `main`** — narrow extraction over timeline + BOE (+ optional raw-parse supplemental); not replay slice definitions or FOW truth |
| Replay slice definitions (metadata-only) | M13 | **On `main`** — narrow temporal spans over governed M10–M12 JSON; not raw clipping or M14 bundles |
| Replay bundle / lineage packaging | M14 | **On `main`** — narrow manifest + lineage + contents over governed M09–M13 JSON; not raw bytes, raw parse in bundle, or execution equivalence |
| Canonical state schema v1 (single frame) | M15 | **On `main`** — narrow JSON Schema + report + fixture validation; not materialization pipeline, sequences, tensors, or observation API |
| Structured state pipeline (bundle → one frame) | M16 | **On `main`** — narrow M14 bundle load + deterministic derivation + schema validation + report; not observation surface contract proof, tensors, or replay↔execution equivalence |
| Observation surface contract v1 (single player-relative frame) | M17 | **On `main`** — narrow JSON Schema + report + fixture validation; upstream M16 canonical state; **not** materialization proof (M18), replay↔execution equivalence |
| Prototype perceptual bridge (canonical state → observation instance) | M18 | **On `main`** — narrow prototype materialization + report; **not** legality, benchmark integrity, M19 reconciliation, or replay↔execution equivalence |
| Cross-mode reconciliation audit (canonical vs observation) | M19 | **On `main`** — narrow deterministic audit + report; **not** benchmark integrity, M20 benchmark contract, or replay↔execution equivalence |
| Benchmark contract + scorecard schemas | M20 | **On `main`** — narrow JSON Schemas + reports + fixture validation; **not** baselines (**M21–M22**), runner (**M23**), benchmark integrity, or replay↔execution equivalence |

### Slice vs bundle glossary (M13–M14)

| Term | Meaning |
| ---- | ------- |
| **Slice (M13)** | A **metadata-defined temporal span** (`replay_slices.json`): addressable `[start_gameloop, end_gameloop]` anchored to M12 combat or scouting signals, with lineage to governed upstream JSON — **not** clipped replay bytes. |
| **Bundle / lineage packaging (M14)** | **M14** scope: packaging and **lineage contract v1** for replay bundles — distinct from M13 slice **definitions**. |
| **Primary governed replay artifacts (M14)** | The five required JSON data artifacts: `replay_metadata.json`, `replay_timeline.json`, `replay_build_order_economy.json`, `replay_combat_scouting_visibility.json`, `replay_slices.json`. |
| **Report artifacts (M14)** | Optional secondary `*_report.json` companions when present — not interchangeable with primary data artifacts. |
| **Excluded raw/parser artifacts (M14)** | Raw `.SC2Replay` bytes, `replay_raw_parse.json`, parser blobs — **not** bundle members in M14 v1. |
| **`bundle_id` / `lineage_root` (M14)** | Deterministic **packaging identity** over hashes of governed JSON — **not** replay↔execution equivalence, benchmark integrity, or legal certification of replay rights. |

### Phase III schema / pipeline / observation glossary (M15–M19)

| Term | Meaning |
| ---- | ------- |
| **M15 canonical state schema** | The **governed JSON Schema** (`canonical_state_schema.json`) and **report** (`canonical_state_schema_report.json`) for a **single** replay-derived state **frame** at one `gameloop` — **schema + validation only**; **not** materialization from replay bundles (that is **M16**). |
| **M16 structured state pipeline** | **Proved on `main`:** **materialize** exactly one M15-shaped `canonical_state.json` per CLI invocation from a **complete M14 bundle** + governed upstream JSON, with `jsonschema` validation and `canonical_state_report.json` — **not** an observation **contract proof** by itself (**M17**), **not** perceptual bridge (**M18**) by itself. |
| **M17 observation surface contract** | **Proved (narrow, in-repo):** deterministic JSON Schema + report for one **player-relative** observation frame at one `gameloop`, bound to **M16 canonical state** as upstream — **contract + validation only**; materialization is **M18** (separate proof). **Proxy visibility** remains bounded (M12/M16 non-claims), not certified fog-of-war truth. |
| **M18 perceptual bridge prototype** | **Proved on `main`:** deterministic **prototype** materialization from one M16 `canonical_state.json` to one M17-shaped `observation_surface.json` + `observation_surface_report.json` (fixture-backed tests; optional report hash cross-check) — **not** replay parsing in `starlab/observation/`, **not** mask legality or benchmark claims, **not** M19 reconciliation by itself. |
| **M19 cross-mode reconciliation audit** | **Proved on `main`:** deterministic audit of one M16 `canonical_state.json` against one M18 `observation_surface.json` (same frame identity), emitting `observation_reconciliation_audit.json` + `observation_reconciliation_audit_report.json` — **not** benchmark integrity, **not** replay↔execution equivalence, **not** M20 benchmark semantics. |

### Phase III reconciliation status glossary (M19)

| Status | Meaning |
| ------ | ------- |
| `exact` | Observation field matches M18 deterministic expectation and is a direct carry-through (or faithful omission of zero-valued aggregates). |
| `derived` | Matches expectation from a deterministic transform (list lengths, prototype action-mask heuristics). |
| `bounded_lossy` | Matches expectation but remains explicitly bounded / proxy / category-level — not full game truth. |
| `unavailable_by_design` | Signal intentionally absent or null when upstream cannot supply it under the contract. |
| `mismatch` | Observation does not match M18 deterministic expectation from the supplied canonical state — audit **failure** when unexpected. |

### Phase IV scorecard glossary (M20)

| Term | Meaning |
| ---- | ------- |
| `scored` | Metric values are populated under the benchmark contract’s scoring rules. |
| `unscored` | No scored metric values (e.g. contract-only or not yet evaluated). |
| `disqualified` | Subject or run excluded from scored comparison (policy or gating). |
| `comparable` | Results may be compared under stated assumptions (still **not** a proof of benchmark integrity). |
| `provisional` | Comparison is tentative or incomplete. |
| `non_comparable` | Results must not be treated as comparable across subjects or runs. |

### Phase III progression (compact)

| Milestone | What it proves (Phase III) |
| --------- | -------------------------- |
| **M15** | Canonical **state schema** only (no bundle materialization). |
| **M16** | **Bundle → one canonical state frame** (replay-derived JSON planes → `canonical_state.json`). |
| **M17** | **Canonical frame → agent-facing observation contract** (schema/report; upstream is **M16**, not raw replay bundles). |
| **M18** | **Prototype perceptual bridge** — canonical state → one M17-shaped observation instance (**proved** on `main`; see §18 / PR #19). |
| **M19** | **Cross-mode reconciliation audit** — canonical state vs observation instance under explicit classification (**proved** on `main`; see §18 / PR #20). |

### Phase IV progression (compact)

| Milestone | What it proves (Phase IV) |
| --------- | ------------------------- |
| **M20** | **Benchmark contract + scorecard schemas** — deterministic JSON Schemas + reports + fixture validation (**proved** on `main`; see §18 / PR #21). |

### Parser glossary (M08–M12)

| Term | Meaning |
| ---- | ------- |
| **Raw parse blocks** | Parser-owned sections lowered deterministically into `replay_raw_parse.json` (e.g. `header`, `details`, `init_data`, optional `attribute_events`). **M08** exposes structure and normalization — **not** the small public metadata API. |
| **Normalized metadata** | **M09** public contract: stable comparable fields in `replay_metadata.json` derived from M08 raw blocks — **not** event semantics. |
| **Event semantics** | Ordered interpretation of game/message/tracker streams (timeline, unit births, commands) — **M10+** scope; M08 may record **availability** only. |
| **Normalized timeline entry** | One row in `replay_timeline.json` `entries[]` after deterministic merge, semantic mapping, and privacy scrub — **M10** public contract. |
| **Event semantic** | The `semantic_kind` field — a small STARLAB enum mapped conservatively from Blizzard `_event` typenames. |
| **Strategic derivation** | Build order / economy plane — **M11** (`replay_build_order_economy.json`); combat / scouting / visibility — **M12** (`replay_combat_scouting_visibility.json`); not the M10 timeline contract by itself. |

### Phase II layering chain (compact)

M08 raw parse → M09 metadata → M10 timeline → **M11 build-order/economy** (primary: `replay_timeline.json`; optional: `replay_raw_parse.json` v2 for identity only) → **M12 combat/scouting/visibility** (primary: `replay_timeline.json` + `replay_build_order_economy.json`; optional: `replay_raw_parse.json` v2 supplemental) → **M13 replay slice definitions** (M10+M11+M12 governed JSON only; **no** `replay_raw_parse.json` in M13 v1) → **M14** bundle / lineage packaging (**not** M13).

### Phase II signal planes (compact)

- **M10** — merged event timeline (`replay_timeline.json`).  
- **M11** — macro / build-order economy (`replay_build_order_economy.json`).  
- **M12** — combat windows, scouting first-seen signals, visibility proxies (`replay_combat_scouting_visibility.json`).  
- **M13** — metadata-only replay slice definitions (`replay_slices.json`).  
- **M14** — replay bundle manifest + lineage + contents (`replay_bundle_manifest.json`, `replay_bundle_lineage.json`, `replay_bundle_contents.json`).

### Visibility glossary (M12)

| Term | Meaning |
| ---- | ------- |
| **Explicit visibility** | Visibility state or transitions **directly** supported by governed upstream fields; M12 emits `explicit_visibility` only when unambiguous. |
| **Observation proxy** | Conservative presence interval from timeline/replay-visible signals (e.g. `unit_tag` span); **not** certified fog-of-war truth and **not** implied when observer identity is absent. |

### Metadata field glossary (M09)

| Category | Meaning |
| -------- | ------- |
| **Replay identity** | `replay_content_sha256` (opaque replay bytes); `source_raw_parse_sha256` (canonical hash of the M08 raw parse object); ties metadata to lineage without shipping raw bytes. |
| **Protocol metadata** | `protocol.base_build`, `protocol.data_build`, `protocol.data_version` — mapped from `protocol_context` / `header.m_version` only; no inference beyond M08 fields. |
| **Map / game metadata** | `map.map_name` (from `details.m_title`); `game.game_length_loops`, `game.player_count`, `game.event_streams_available` — **copied or mapped** from M08 raw sections; **no** timeline semantics from event bodies. |
| **Player metadata** | Per-player `player_index`, `player_kind`, `race_requested`, `race_actual`, `result` — from `details.m_playerList` with conservative enums; **no** display names or PII in the M09 contract. |
| **Deferred (event plane)** | Game / message / tracker **streams** and their interpretation — **M10**; not part of M09 metadata extraction. |

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

### M21 — Scripted Baseline Suite

**Status:** **Planned** — **current** milestone; **M20** is **closed** on `main` (see §18). **Phase IV** continues (benchmark / evaluation plane); **M21** is **stub-only** until authorized (`docs/company_secrets/milestones/M21/`).

**Goal (high level):** **M21** introduces a **scripted baseline suite** — **not** started in M20; see `docs/company_secrets/milestones/M21/M21_plan.md` (stub).

**Primary references:** `docs/company_secrets/milestones/M21/M21_plan.md`; `docs/starlab.md` §6 / §10.

**Note:** **M20** proves only **governed benchmark contract + scorecard JSON Schemas + reports** (`docs/runtime/benchmark_contract_scorecard_v1.md`, `starlab/benchmarks/`) — **not** scripted baselines, **not** heuristic baselines, **not** evaluation runner / tournament harness (**M21–M23**).

#### Current milestone — explicit non-claims (standing)

Until **M21** explicitly closes a claim, treat the following as **not proved** for **M21** planning:

- **Benchmark integrity** / leaderboard claims (**not** a default proof).
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

**Closeout hygiene:** Prefer **at most one** post-merge `main` documentation-only commit per milestone closeout; if further fixes are needed afterward, land them on the **next milestone branch** rather than repeated doc-only churn on `main` (see M09 run-record footnotes on merge-boundary vs non-merge-boundary CI).

### CI authority glossary (compact)

| Term | Meaning |
| ---- | ------- |
| **Authoritative green PR-head CI** | A completed **success** `pull_request` workflow run on the **final PR head SHA** before merge — primary **merge-gate** evidence when present. |
| **Merge-boundary `main` CI** | First `push` workflow run to `main` triggered by merging a PR (merge commit or squash), before unrelated follow-up commits. |
| **Repaired green `main` CI** | A later `main` run that fixes red merge-boundary CI (e.g. M10 Mypy repair) — **not** a substitute for PR-head green when citing merge discipline. |
| **Non-merge-boundary runs** | Doc-only, ledger, or chore pushes to `main` after the merge boundary — **not** merge authority; keep tables capped (M09 lesson). |

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
| M09       | 2026-04-07    | [#10](https://github.com/m-cahill/starlab/pull/10) | `fc9b442d66abe9a2922e93051c7d0a22ccb133d1` | Replay metadata extraction (`replay_metadata.json` / `replay_metadata_report.json`); merged to `main`; narrow pure extraction over M08 artifacts — see CI evidence below |
| M10       | 2026-04-07    | [#11](https://github.com/m-cahill/starlab/pull/11) | `cb3e581f70f85653477081eb1ef4772229f05983` | Timeline & event extraction (`replay_timeline.json` / `replay_timeline_report.json`, optional `replay_raw_parse` v2 `raw_event_streams`); merge-push CI failed Mypy — repaired on `main` (`cf2074e10ec8a38b22bd7b75ffeb4ec22a71485b`); see §18 / `M10_run1.md` |
| M11       | 2026-04-07    | [#12](https://github.com/m-cahill/starlab/pull/12) | `38c15302badd49966b17f9195ddb139f6ae9a9b4` | Build-order & economy plane (`replay_build_order_economy.json` / `replay_build_order_economy_report.json`); **green PR-head** [`24106029320`](https://github.com/m-cahill/starlab/actions/runs/24106029320); **green merge-push `main`** [`24106124347`](https://github.com/m-cahill/starlab/actions/runs/24106124347); see §18 / `M11_run1.md` |
| M12       | 2026-04-07    | [#13](https://github.com/m-cahill/starlab/pull/13) | `78528958a616177b564e603c193fb0d7f8af734e` | Combat/scouting/visibility (`replay_combat_scouting_visibility.json` / `replay_combat_scouting_visibility_report.json`); **green PR-head** [`24109242392`](https://github.com/m-cahill/starlab/actions/runs/24109242392); **green merge-push `main`** [`24109269513`](https://github.com/m-cahill/starlab/actions/runs/24109269513); see §18 / `M12_run1.md` |
| M13       | 2026-04-08    | [#14](https://github.com/m-cahill/starlab/pull/14) | `f86e36837e81b8552639c5a885a13a773b96215c` | Replay slice definitions (`replay_slices.json` / `replay_slices_report.json`); **green PR-head** [`24112526047`](https://github.com/m-cahill/starlab/actions/runs/24112526047); **green merge-push `main`** [`24112556177`](https://github.com/m-cahill/starlab/actions/runs/24112556177); see §18 / `M13_run1.md` |
| M14       | 2026-04-08    | [#15](https://github.com/m-cahill/starlab/pull/15) | `8a0439a9a2970a74f3a5087390fc080f02852246` | Replay bundle + lineage (`replay_bundle_manifest.json` / `replay_bundle_lineage.json` / `replay_bundle_contents.json`); **green PR-head** [`24118622373`](https://github.com/m-cahill/starlab/actions/runs/24118622373); **green merge-push `main`** [`24118654909`](https://github.com/m-cahill/starlab/actions/runs/24118654909); see §18 / `M14_run1.md` |
| M15       | 2026-04-08    | [#16](https://github.com/m-cahill/starlab/pull/16) | `b0f7132a54508f35d54406011cd3b37bce776927` | Canonical state schema v1 (`canonical_state_schema.json` / `canonical_state_schema_report.json`); **green PR-head** [`24122064141`](https://github.com/m-cahill/starlab/actions/runs/24122064141); **green merge-push `main`** [`24122092800`](https://github.com/m-cahill/starlab/actions/runs/24122092800); see §18 / `M15_run1.md` |
| M16       | 2026-04-08    | [#17](https://github.com/m-cahill/starlab/pull/17) | `dd9546f88ebcf9b454498eec83a14d742d17d070` | Structured state pipeline (`canonical_state.json` / `canonical_state_report.json`); **green PR-head** [`24160830775`](https://github.com/m-cahill/starlab/actions/runs/24160830775); **green merge-push `main`** [`24160871811`](https://github.com/m-cahill/starlab/actions/runs/24160871811); superseded red PR-head [`24160804226`](https://github.com/m-cahill/starlab/actions/runs/24160804226) (Ruff format — **not** merge authority); see §18 / `M16_run1.md` |
| M17       | 2026-04-08    | [#18](https://github.com/m-cahill/starlab/pull/18) | `f63c8e93cb0a2943b9149f4384dbde68b74f9e76` | Observation surface contract (`observation_surface_schema.json` / `observation_surface_schema_report.json`); **green PR-head** [`24164045530`](https://github.com/m-cahill/starlab/actions/runs/24164045530); **green merge-push `main`** [`24164075167`](https://github.com/m-cahill/starlab/actions/runs/24164075167); see §18 / `M17_run1.md` |
| M18       | 2026-04-09    | [#19](https://github.com/m-cahill/starlab/pull/19) | `59d2d6e2af08852d63e0c91a984000c11decfece` | Perceptual bridge prototype (`observation_surface.json` / `observation_surface_report.json`); **green PR-head** [`24165977039`](https://github.com/m-cahill/starlab/actions/runs/24165977039); **green merge-push `main`** [`24166004479`](https://github.com/m-cahill/starlab/actions/runs/24166004479); see §18 / `M18_run1.md` |
| M19       | 2026-04-09    | [#20](https://github.com/m-cahill/starlab/pull/20) | `9e855329fc50f4f00db9c857f982d18ef93e4e65` | Cross-mode reconciliation audit (`observation_reconciliation_audit.json` / `observation_reconciliation_audit_report.json`); **green PR-head** [`24168988693`](https://github.com/m-cahill/starlab/actions/runs/24168988693) on `1453eee…`; **green merge-push `main`** [`24169013104`](https://github.com/m-cahill/starlab/actions/runs/24169013104) on `9e85532…`; see §18 / `M19_run1.md` |
| M20       | 2026-04-09    | [#21](https://github.com/m-cahill/starlab/pull/21) | `cf1bee980756b3b59d4db2620c041a23f14eba18` | Benchmark contract + scorecard schemas (`benchmark_contract_schema.json` / `benchmark_contract_schema_report.json` / `benchmark_scorecard_schema.json` / `benchmark_scorecard_schema_report.json`); **green PR-head** [`24173251270`](https://github.com/m-cahill/starlab/actions/runs/24173251270) on `5c22336…`; **green merge-push `main`** [`24173270201`](https://github.com/m-cahill/starlab/actions/runs/24173270201) on `cf1bee9…`; see §18 / `M20_run1.md` |

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

**M09 merge:** [PR #10](https://github.com/m-cahill/starlab/pull/10) merged **2026-04-07** (UTC `2026-04-07T20:05:59Z`) via **merge commit** `fc9b442d66abe9a2922e93051c7d0a22ccb133d1`. Remote branch `m09-replay-metadata-extraction` was **deleted** after merge. Final PR head before merge: `3f161dea12a9b7ffb6dbe01c73b01f351a7219da`.

**M09 CI evidence (PR-head run — authoritative merge gate)**

| Commit (short) | Workflow run | Conclusion | URL |
| -------------- | ------------ | ---------- | --- |
| `3f161de…` | `24101861888` | success | https://github.com/m-cahill/starlab/actions/runs/24101861888 |

**Superseded PR-head runs:** none observed for the final merge tip — single green `pull_request` run at `3f161de…` is merge authority.

**M09 CI evidence (post-merge `main`)**

| Event | Workflow run | Conclusion | URL |
| ----- | ------------ | ---------- | --- |
| `main` after M09 merge (`fc9b442…`) | `24101900950` | success | https://github.com/m-cahill/starlab/actions/runs/24101900950 |

*Further documentation-only pushes to `main` after this row may produce additional green CI runs; distinguish them in §23 — **not** merge-boundary unless the event is a PR merge.*

**M09 milestone artifacts:** `docs/company_secrets/milestones/M09/` (`M09_plan.md`, `M09_toolcalls.md`, `M09_run1.md`, `M09_summary.md`, `M09_audit.md`, etc.)

**M10 merge:** [PR #11](https://github.com/m-cahill/starlab/pull/11) merged **2026-04-07** (UTC `2026-04-07T20:58:46Z`) via **merge commit** `cb3e581f70f85653477081eb1ef4772229f05983`. Remote branch `m10-timeline-event-extraction` was **deleted** after merge. Final PR head before merge: `cb066fe3f09b07f3390e85928c88f65a6e75cd6f`.

**M10 CI evidence (PR-head run — merge gate)**

| Commit (short) | Workflow run | Conclusion | URL |
| -------------- | ------------ | ---------- | --- |
| `cb066fe…` | `24104110934` | cancelled | https://github.com/m-cahill/starlab/actions/runs/24104110934 |

**Authoritative green PR-head CI:** **none** — the only witnessed `pull_request` run on the final merge tip was **cancelled** (merge landed while the workflow was starting).

**M10 CI evidence (post-merge `main`)**

| Event | Workflow run | Conclusion | URL |
| ----- | ------------ | ---------- | --- |
| `main` after M10 merge (`cb3e581…`) | `24104111851` | failure | https://github.com/m-cahill/starlab/actions/runs/24104111851 |
| `main` after M10 Mypy repair (`cf2074e…`) | `24104197912` | success | https://github.com/m-cahill/starlab/actions/runs/24104197912 |

*Merge-push on `cb3e581…` failed **Mypy**; **authoritative green `main`** for current governance is **`24104197912`** on `cf2074e…` (repair — **not** a merge-boundary event). Further documentation-only pushes after closeout may produce additional green runs; distinguish them in §23 — **not** merge-boundary unless the event is a PR merge. Prefer **at most one** post-merge doc-only churn per closeout hygiene.*

**M10 milestone artifacts:** `docs/company_secrets/milestones/M10/` (`M10_plan.md`, `M10_toolcalls.md`, `M10_run1.md`, `M10_summary.md`, `M10_audit.md`, etc.)

**M11 merge:** [PR #12](https://github.com/m-cahill/starlab/pull/12) merged **2026-04-07** (UTC `2026-04-07T21:49:23Z`) via **merge commit** `38c15302badd49966b17f9195ddb139f6ae9a9b4`. Remote branch `m11-build-order-economy-plane` was **deleted** after merge. Final PR head before merge: `88ce7f9615c6c462b76674e1afb0734fc3dcc5be`.

**M11 CI evidence (PR-head run — authoritative merge gate)**

| Commit (short) | Workflow run | Conclusion | URL |
| -------------- | ------------ | ---------- | --- |
| `88ce7f9…` | `24106029320` | success | https://github.com/m-cahill/starlab/actions/runs/24106029320 |

**Authoritative green PR-head CI:** [`24106029320`](https://github.com/m-cahill/starlab/actions/runs/24106029320) — **success** on final tip `88ce7f9…` (contrast M10 cancelled merge-gate run).

**M11 CI evidence (post-merge `main` — merge boundary)**

| Event | Workflow run | Conclusion | URL |
| ----- | ------------ | ---------- | --- |
| `main` after M11 merge (`38c1530…`) | `24106124347` | success | https://github.com/m-cahill/starlab/actions/runs/24106124347 |

*Closeout / ledger documentation pushes after this row may produce additional green `main` runs; distinguish them in §23 — **not** merge-boundary unless the event is a PR merge. Prefer **at most one** post-merge doc-only commit per closeout hygiene.*

**M11 milestone artifacts:** `docs/company_secrets/milestones/M11/` (`M11_plan.md`, `M11_toolcalls.md`, `M11_run1.md`, `M11_summary.md`, `M11_audit.md`, etc.)

**M12 merge:** [PR #13](https://github.com/m-cahill/starlab/pull/13) merged **2026-04-07** (UTC `2026-04-07T23:23:48Z`) via **merge commit** `78528958a616177b564e603c193fb0d7f8af734e`. Remote branch `m12-combat-scouting-visibility-windows` was **deleted** after merge. Final PR head before merge: `59adce3422a840692a4961278c995c5029da43bb`.

**M12 CI evidence (PR-head run — authoritative merge gate)**

| Commit (short) | Workflow run | Conclusion | URL |
| -------------- | ------------ | ---------- | --- |
| `59adce3…` | `24109242392` | success | https://github.com/m-cahill/starlab/actions/runs/24109242392 |

**Authoritative green PR-head CI:** [`24109242392`](https://github.com/m-cahill/starlab/actions/runs/24109242392) — **success** on final tip `59adce3…`.

**M12 CI evidence (post-merge `main` — merge boundary)**

| Event | Workflow run | Conclusion | URL |
| ----- | ------------ | ---------- | --- |
| `main` after M12 merge (`7852895…`) | `24109269513` | success | https://github.com/m-cahill/starlab/actions/runs/24109269513 |

*Closeout / ledger documentation pushes after this row may produce additional green `main` runs; distinguish them in §23 — **not** merge-boundary unless the event is a PR merge. Prefer **at most one** post-merge doc-only commit per closeout hygiene.*

**M12 milestone artifacts:** `docs/company_secrets/milestones/M12/` (`M12_plan.md`, `M12_toolcalls.md`, `M12_run1.md`, `M12_summary.md`, `M12_audit.md`, etc.)

**M13 merge:** [PR #14](https://github.com/m-cahill/starlab/pull/14) merged **2026-04-08** (UTC `2026-04-08T01:20:38Z`) via **merge commit** `f86e36837e81b8552639c5a885a13a773b96215c`. Remote branch `m13-replay-slice-generator` was **deleted** after merge. Final PR head before merge: `6231b19cd7067130fd3324dcd3070172333ba766`.

**M13 CI evidence (PR-head run — authoritative merge gate)**

| Commit (short) | Workflow run | Conclusion | URL |
| -------------- | ------------ | ---------- | --- |
| `6231b19…` | `24112526047` | success | https://github.com/m-cahill/starlab/actions/runs/24112526047 |

**Authoritative green PR-head CI:** [`24112526047`](https://github.com/m-cahill/starlab/actions/runs/24112526047) — **success** on final tip `6231b19…`.

**M13 CI evidence (post-merge `main` — merge boundary)**

| Event | Workflow run | Conclusion | URL |
| ----- | ------------ | ---------- | --- |
| `main` after M13 merge (`f86e368…`) | `24112556177` | success | https://github.com/m-cahill/starlab/actions/runs/24112556177 |

*Closeout / ledger documentation pushes after this row may produce additional green `main` runs; distinguish them in §23 — **not** merge-boundary unless the event is a PR merge. Prefer **at most one** post-merge doc-only commit per closeout hygiene.*

**M13 milestone artifacts:** `docs/company_secrets/milestones/M13/` (`M13_plan.md`, `M13_toolcalls.md`, `M13_run1.md`, `M13_summary.md`, `M13_audit.md`, etc.)

**M14 merge:** [PR #15](https://github.com/m-cahill/starlab/pull/15) merged **2026-04-08** (UTC `2026-04-08T05:00:41Z`) via **merge commit** `8a0439a9a2970a74f3a5087390fc080f02852246`. Remote branch `m14-replay-bundle-lineage-contract-v1` was **deleted** after merge. Final PR head before merge: `42e29f2a64fa4672dbd2df435a04836c379b5258`.

**M14 CI evidence (PR-head run — authoritative merge gate)**

| Commit (short) | Workflow run | Conclusion | URL |
| -------------- | ------------ | ---------- | --- |
| `42e29f2…` | `24118622373` | success | https://github.com/m-cahill/starlab/actions/runs/24118622373 |

**Authoritative green PR-head CI:** [`24118622373`](https://github.com/m-cahill/starlab/actions/runs/24118622373) — **success** on final tip `42e29f2…`.

**M14 CI evidence (post-merge `main` — merge boundary)**

| Event | Workflow run | Conclusion | URL |
| ----- | ------------ | ---------- | --- |
| `main` after M14 merge (`8a0439a…`) | `24118654909` | success | https://github.com/m-cahill/starlab/actions/runs/24118654909 |

*Closeout / ledger documentation pushes after this row may produce additional green `main` runs; distinguish them in §23 — **not** merge-boundary unless the event is a PR merge. Prefer **at most one** post-merge doc-only commit per closeout hygiene.*

**M14 milestone artifacts:** `docs/company_secrets/milestones/M14/` (`M14_plan.md`, `M14_toolcalls.md`, `M14_run1.md`, `M14_summary.md`, `M14_audit.md`, etc.)

**M15 merge:** [PR #16](https://github.com/m-cahill/starlab/pull/16) merged **2026-04-08** (UTC `2026-04-08T06:51:06Z`) via **merge commit** `b0f7132a54508f35d54406011cd3b37bce776927`. Remote branch `m15-canonical-state-schema-v1` was **deleted** after merge. Final PR head before merge: `abc8ffcd223536568fcf134b1e21273915cf1d4d`.

**M15 CI evidence (PR-head run — authoritative merge gate)**

| Commit (short) | Workflow run | Conclusion | URL |
| -------------- | ------------ | ---------- | --- |
| `abc8ffc…` | `24122064141` | success | https://github.com/m-cahill/starlab/actions/runs/24122064141 |

**Authoritative green PR-head CI:** [`24122064141`](https://github.com/m-cahill/starlab/actions/runs/24122064141) — **success** on final tip `abc8ffc…`.

**Superseded (not merge authority):** [`24121376545`](https://github.com/m-cahill/starlab/actions/runs/24121376545) — **failure** at **Mypy** (`import-untyped` for `jsonschema`); fixed on tip `abc8ffc…` with `types-jsonschema`.

**M15 CI evidence (post-merge `main` — merge boundary)**

| Event | Workflow run | Conclusion | URL |
| ----- | ------------ | ---------- | --- |
| `main` after M15 merge (`b0f7132…`) | `24122092800` | success | https://github.com/m-cahill/starlab/actions/runs/24122092800 |

*Closeout / ledger documentation pushes after this row may produce additional green `main` runs; distinguish them in §23 — **not** merge-boundary unless the event is a PR merge. Prefer **at most one** post-merge doc-only commit per closeout hygiene.*

**M15 milestone artifacts:** `docs/company_secrets/milestones/M15/` (`M15_plan.md`, `M15_toolcalls.md`, `M15_run1.md`, `M15_summary.md`, `M15_audit.md`, etc.)

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
| M09       | 3.5  | +          | +        | +   | +         | +    | 4.5     |
| M10       | 3.5  | +          | +        | +   | +         | +    | 4.5     |
| M11       | 3.5  | +          | +        | +   | +         | +    | 4.5     |
| M12       | 3.5  | +          | +        | +   | +         | +    | 4.5     |
| M13       | 3.5  | +          | +        | +   | +         | +    | 4.5     |
| M14       | 3.5  | +          | +        | +   | +         | +    | 4.5     |
| M15       | 3.5  | +          | +        | +   | +         | +    | 4.5     |
| M16       | 3.5  | +          | +        | +   | +         | +    | 4.5     |
| M17       | 3.5  | +          | +        | +   | +         | +    | 4.5     |
| M18       | 3.5  | +          | +        | +   | +         | +    | 4.5     |
| M19       | 3.5  | +          | +        | +   | +         | +    | 4.5     |
| M20       | 3.5  | +          | +        | +   | +         | +    | 4.5     |

**M02 note:** Evidence column reflects **narrow** local harness proof + CI; not benchmark or cross-host certification.

**M03 note:** Evidence column reflects **fixture/proof-driven** identity + lineage seed + CI on `main`; not replay binding, canonical artifact v0, or benchmark certification.

**M04 note:** Evidence column reflects **fixture-driven replay binding** (`replay_binding.json`) + CI on `main`; **not** replay parser semantics, replay↔proof equivalence, canonical run artifact v0, or benchmark certification.

**M05 note:** Evidence column reflects **fixture-driven canonical bundle** (`manifest.json` / `hashes.json` + M03/M04 JSON) **on `main`**; **not** replay parser semantics, raw replay/proof shipping, benchmark validity, or cross-host reproducibility.

**M06 note:** Evidence column reflects **fixture-driven** smoke matrix + drift report + CI on `main`; **not** replay parser semantics, portability certification, benchmark validity, provenance closure, or live SC2 execution in CI.

**M07 note:** Evidence column reflects **fixture-driven** replay intake receipt/report + CI **on `main`**; **not** replay parser semantics, build-order extraction, benchmark validity, live SC2 execution in CI, or legal certification of third-party replay rights as a matter of law.

**M08 note:** Evidence column reflects **fixture-driven** parser substrate + deterministic parse artifacts + CI **on `main`**; **not** stable normalized metadata (M09), event semantics (M10), broad parser correctness, benchmark validity, or live SC2 execution in CI.

**M09 note:** Evidence column reflects **fixture-driven** metadata extraction + deterministic metadata artifacts + CI **on `main`**; **not** event/timeline semantics (M10), build-order extraction (M11), or benchmark validity.

**M10 note:** Evidence column reflects **fixture-driven** timeline extraction + deterministic timeline artifacts + CI **on `main`** (merge-push on merge commit failed Mypy — **authoritative green `main`** on repair `cf2074e…`, run `24104197912`); **not** build-order/economy (M11), combat/scouting, benchmark validity, or live SC2 execution in CI.

**M11 note:** Evidence column reflects **fixture-driven** build-order/economy extraction + deterministic artifacts + CI **on `main`** (**green PR-head** [`24106029320`](https://github.com/m-cahill/starlab/actions/runs/24106029320) on `88ce7f9…`; **green merge-push** [`24106124347`](https://github.com/m-cahill/starlab/actions/runs/24106124347) on `38c1530…`); **not** combat/scouting (M12), exact resource reconstruction, benchmark validity, replay↔execution equivalence, or live SC2 execution in CI.

**M12 note:** Evidence column reflects **fixture-driven** combat/scouting/visibility extraction + deterministic artifacts + CI **on `main`** (**green PR-head** [`24109242392`](https://github.com/m-cahill/starlab/actions/runs/24109242392) on `59adce3…`; **green merge-push** [`24109269513`](https://github.com/m-cahill/starlab/actions/runs/24109269513) on `7852895…`); **not** replay slice definitions (M13), true fog-of-war certification, benchmark validity, replay↔execution equivalence, or live SC2 execution in CI.

**M13 note:** Evidence column reflects **fixture-driven** replay slice definition extraction + deterministic artifacts + CI **on `main`** (**green PR-head** [`24112526047`](https://github.com/m-cahill/starlab/actions/runs/24112526047) on `6231b19…`; **green merge-push** [`24112556177`](https://github.com/m-cahill/starlab/actions/runs/24112556177) on `f86e368…`); **not** raw replay clipping, benchmark validity, replay↔execution equivalence, fog-of-war truth, or live SC2 execution in CI.

**M14 note:** Evidence column reflects **fixture-driven** replay bundle packaging + lineage + contents + CI **on `main`** (**green PR-head** [`24118622373`](https://github.com/m-cahill/starlab/actions/runs/24118622373) on `42e29f2…`; **green merge-push** [`24118654909`](https://github.com/m-cahill/starlab/actions/runs/24118654909) on `8a0439a…`); **not** raw replay clipping, replay↔execution equivalence, benchmark validity, canonical state schema (M15), live SC2 execution in CI, or legal certification of replay rights.

**M15 note:** Evidence column reflects **schema + report emission**, **jsonschema** validation over fixtures, and full governance CI **on `main`** (**green PR-head** [`24122064141`](https://github.com/m-cahill/starlab/actions/runs/24122064141) on `abc8ffc…`; **green merge-push** [`24122092800`](https://github.com/m-cahill/starlab/actions/runs/24122092800) on `b0f7132…`); **not** replay-to-state materialization (M16), observation contract (M17), perceptual bridge (M18), stronger economy or visibility claims than M11/M12, replay↔execution equivalence, benchmark integrity, or live SC2 in CI.

**M16 note:** Evidence column reflects **M14 bundle → one `canonical_state.json` + report**, **jsonschema** validation against M15 schema, and full governance CI **on `main`** (**green PR-head** [`24160830775`](https://github.com/m-cahill/starlab/actions/runs/24160830775) on `11fb080…`; **green merge-push** [`24160871811`](https://github.com/m-cahill/starlab/actions/runs/24160871811) on `dd9546f…`); **superseded** red PR-head [`24160804226`](https://github.com/m-cahill/starlab/actions/runs/24160804226) (Ruff format — **not** merge authority); **not** observation tensors / action masks (M17), perceptual bridge (M18), replay↔execution equivalence, benchmark integrity, exact banked resources, certified fog-of-war truth, or live SC2 in CI.

**M17 note:** Evidence column reflects **observation surface schema + report emission**, **jsonschema** validation over fixtures, and full governance CI **on `main`** (**green PR-head** [`24164045530`](https://github.com/m-cahill/starlab/actions/runs/24164045530) on `801af8b…`; **green merge-push `main`** [`24164075167`](https://github.com/m-cahill/starlab/actions/runs/24164075167) on `f63c8e9…`); **not** canonical-state→observation materialization (that is **M18**), mask legality computation, replay↔execution equivalence, benchmark integrity, exact banked resources, certified fog-of-war truth, or live SC2 in CI.

**M18 note:** Evidence column reflects **prototype materialization** from M16 `canonical_state.json` to M17-shaped `observation_surface.json` + report, **jsonschema** validation on emitted observation, and full governance CI **on `main`** (**green PR-head** [`24165977039`](https://github.com/m-cahill/starlab/actions/runs/24165977039) on `8d9f9e1…`; **green merge-push `main`** [`24166004479`](https://github.com/m-cahill/starlab/actions/runs/24166004479) on `59d2d6e…`); **not** full action legality, benchmark integrity, replay↔execution equivalence, certified fog-of-war truth, exact banked resources, live SC2 in CI, or **M19** reconciliation (M19 is a separate proof).

**M19 note:** Evidence column reflects **cross-mode reconciliation audit** over paired M16 `canonical_state.json` + M18 `observation_surface.json` (fixture-backed goldens under `tests/fixtures/m19/`) + full governance CI **on `main`** (**green PR-head** [`24168988693`](https://github.com/m-cahill/starlab/actions/runs/24168988693) on `1453eee…`; **green merge-push `main`** [`24169013104`](https://github.com/m-cahill/starlab/actions/runs/24169013104) on `9e85532…`). **Not** benchmark integrity, replay↔execution equivalence, live SC2 in CI, or **M20** benchmark contract semantics.

**M20 note:** Evidence column reflects **benchmark contract + scorecard JSON Schema emission** + fixture validation + full governance CI **on `main`** (**green PR-head** [`24173251270`](https://github.com/m-cahill/starlab/actions/runs/24173251270) on `5c22336…`; **green merge-push `main`** [`24173270201`](https://github.com/m-cahill/starlab/actions/runs/24173270201) on `cf1bee9…`; see §18 / `M20_run1.md`). **Not** scripted/heuristic baselines (**M21–M22**), evaluation runner (**M23**), benchmark integrity, replay↔execution equivalence, or live SC2 in CI.

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

### 2026-04-09 — M20 merged to `main` (PR #21) + closeout

- Merged [PR #21](https://github.com/m-cahill/starlab/pull/21) to `main` at **2026-04-09T04:59:35Z**; merge commit `cf1bee980756b3b59d4db2620c041a23f14eba18` (merge method: **merge commit**); remote branch `m20-benchmark-contract-scorecard-semantics` **deleted**
- Final PR head `5c2233690a3dc6d352dd9b06be16430b3d73b6e8` — **authoritative green PR-head CI:** [`24173251270`](https://github.com/m-cahill/starlab/actions/runs/24173251270) (**success**)
- **Merge-push `main` CI** on merge commit: [`24173270201`](https://github.com/m-cahill/starlab/actions/runs/24173270201) (**success**)
- Product: `docs/runtime/benchmark_contract_scorecard_v1.md`, `starlab/benchmarks/` (contract models + JSON Schema builders + `python -m starlab.benchmarks.emit_benchmark_contracts`), `tests/fixtures/m20/`, `tests/test_benchmark_contracts.py`; **357** pytest on authoritative CI (one pre-existing `s2protocol` deprecation warning in replay CLI test — not M20)
- Phase IV artifact row + Phase IV scorecard glossary (`scored` / `unscored` / `disqualified` / `comparable` / `provisional` / `non_comparable`)
- §3 / §6 / §10 / §11 / §18 / §20 / §23: **governed benchmark contract + scorecard schemas** (narrow) **proved on `main`**; **current milestone** → **M21** (stub); closeout ledger M20 row; score trend M20 note
- Milestone closeout: `M20_run1.md`, `M20_summary.md`, `M20_audit.md`, `M20_plan.md` (**closed**), `M20_toolcalls.md`; **M21** stubs (`M21_plan.md`, `M21_toolcalls.md`) — **no** M21 product code

### 2026-04-09 — M18 merged to `main` (PR #19) + closeout

- Merged [PR #19](https://github.com/m-cahill/starlab/pull/19) to `main` at **2026-04-09T00:32:06Z**; merge commit `59d2d6e2af08852d63e0c91a984000c11decfece` (merge method: **merge commit**); remote branch `m18-perceptual-bridge-prototype` **deleted**
- Final PR head `8d9f9e1f8343120dd32916fb23668fd0ecee3fa0` — **authoritative green PR-head CI:** [`24165977039`](https://github.com/m-cahill/starlab/actions/runs/24165977039) (**success**)
- **Merge-push `main` CI** on merge commit: [`24166004479`](https://github.com/m-cahill/starlab/actions/runs/24166004479) (**success**)
- Product: `docs/runtime/perceptual_bridge_prototype_v1.md`, `starlab/observation/` materialization modules + CLI, `tests/fixtures/m18/`, `tests/test_observation_surface_pipeline.py`; **322** pytest on authoritative CI (one pre-existing `s2protocol` deprecation warning in replay CLI test — not M18)
- §3 / §6 / §7 / §10 / §11 / §18 / §20 / §23: **governed perceptual bridge prototype** (narrow) **proved on `main`**; Phase III progression (M15 schema / M16 bundle→frame / M17 observation contract / **M18 prototype bridge**); **current milestone** → **M19** (stub); closeout ledger M18 row; score trend M18 note
- Milestone closeout: `M18_run1.md`, `M18_summary.md`, `M18_audit.md`, `M18_plan.md` (**closed**), `M18_toolcalls.md`; **M19** stubs (`M19_plan.md`, `M19_toolcalls.md`) — **no** M19 product code
- **Non-merge-boundary** `main` CI — closeout commit `977b625f09ab3db893c26a31e6c3c0e730a9fea4`: [`24166079739`](https://github.com/m-cahill/starlab/actions/runs/24166079739) (**success**) — milestone docs + ledger only; **authoritative** M18 product merge evidence remains PR-head [`24165977039`](https://github.com/m-cahill/starlab/actions/runs/24165977039) + merge-boundary [`24166004479`](https://github.com/m-cahill/starlab/actions/runs/24166004479)

### 2026-04-08 — M17 merged to `main` (PR #18) + closeout

- Merged [PR #18](https://github.com/m-cahill/starlab/pull/18) to `main` at **2026-04-08T23:30:53Z**; merge commit `f63c8e93cb0a2943b9149f4384dbde68b74f9e76` (merge method: **merge commit**); remote branch `m17-observation-surface-contract` **deleted**
- Final PR head `801af8b9c1a525e19fe3804cb7ed968e80d8b0f6` — **authoritative green PR-head CI:** [`24164045530`](https://github.com/m-cahill/starlab/actions/runs/24164045530) (**success**)
- **Merge-push `main` CI** on merge commit: [`24164075167`](https://github.com/m-cahill/starlab/actions/runs/24164075167) (**success**)
- Product: `docs/runtime/observation_surface_contract_v1.md`, `starlab/observation/` (contract-only), `tests/fixtures/m17/`, observation tests; **310** pytest on authoritative CI
- §3 / §6 / §7 / §10 / §11 / §18 / §20 / §23: **governed observation surface contract** (narrow) **proved on `main`**; Phase III progression (M15 schema / M16 bundle→frame / **M17 observation contract** / M18 bridge stub); **current milestone** → **M18**; closeout ledger M17 row; score trend M17 note
- Milestone closeout: `M17_run1.md`, `M17_summary.md`, `M17_audit.md`, `M17_plan.md` (**closed**), `M17_toolcalls.md`; **M18** stubs (`M18_plan.md`, `M18_toolcalls.md`) — **no** M18 product code
- **Non-merge-boundary** `main` CI — closeout commit `87fd04617ad06522efca8d6a89e31d74c83e12cb`: [`24164136804`](https://github.com/m-cahill/starlab/actions/runs/24164136804) (**success**) — milestone docs + ledger only; **authoritative** M17 product merge evidence remains PR-head [`24164045530`](https://github.com/m-cahill/starlab/actions/runs/24164045530) + merge-boundary [`24164075167`](https://github.com/m-cahill/starlab/actions/runs/24164075167)

### 2026-04-08 — M16 merged to `main` (PR #17) + closeout

- Merged [PR #17](https://github.com/m-cahill/starlab/pull/17) to `main` at **2026-04-08T21:58:44Z**; merge commit `dd9546f88ebcf9b454498eec83a14d742d17d070` (merge method: **merge commit**); remote branch `m16-structured-state-pipeline` **deleted**
- Final PR head `11fb0803b8fa0343c08d9c3bda06929092a437d1` — **authoritative green PR-head CI:** [`24160830775`](https://github.com/m-cahill/starlab/actions/runs/24160830775) (**success**); superseded red PR-head [`24160804226`](https://github.com/m-cahill/starlab/actions/runs/24160804226) (Ruff format — **not** merge authority)
- **Merge-push `main` CI** on merge commit: [`24160871811`](https://github.com/m-cahill/starlab/actions/runs/24160871811) (**success**)
- §3 / §6 / §7 / §8 / §10 / §11 / §18 / §20 / §23 updated: **governed structured state pipeline** (narrow) **proved on `main`**; Phase III artifact row (M16); Phase III glossary (M15 schema-only vs M16 pipeline vs M17 observation); **current milestone** → **M17** (stub); closeout ledger M16 row + compact table M16 row; score trend M16 note
- Milestone closeout: `M16_run1.md`, `M16_summary.md`, `M16_audit.md`, `M16_plan.md` (**Status: Complete**), `M16_toolcalls.md`; **M17** stubs present (`M17_plan.md`, `M17_toolcalls.md`) — **no** M17 product code in this pass
- **Non-merge-boundary** `main` CI — closeout commit `a6a3ea62e8bfa036b87727e1d8e93a60176c4ef8` (short `a6a3ea6…`): [`24160991810`](https://github.com/m-cahill/starlab/actions/runs/24160991810) (**success**) — ledger + milestone artifacts + governance tests only; **authoritative** PR-head / merge-boundary CI for M16 product merge remains [`24160830775`](https://github.com/m-cahill/starlab/actions/runs/24160830775) / [`24160871811`](https://github.com/m-cahill/starlab/actions/runs/24160871811)
- **Non-merge-boundary** `main` CI — follow-up commit `7b1731f151a3ae75006f039a0b79cdec48561289` (short `7b1731f…`): [`24161024608`](https://github.com/m-cahill/starlab/actions/runs/24161024608) (**success**) — changelog row for prior closeout run; **not** merge authority

### 2026-04-08 — M15 merged to `main` (PR #16) + closeout

- Merged [PR #16](https://github.com/m-cahill/starlab/pull/16) to `main` at **2026-04-08T06:51:06Z**; merge commit `b0f7132a54508f35d54406011cd3b37bce776927` (merge method: **merge commit**); remote branch `m15-canonical-state-schema-v1` **deleted**
- Final PR head `abc8ffcd223536568fcf134b1e21273915cf1d4d` — **authoritative green PR-head CI:** [`24122064141`](https://github.com/m-cahill/starlab/actions/runs/24122064141) (**success**); superseded red PR-head [`24121376545`](https://github.com/m-cahill/starlab/actions/runs/24121376545) (Mypy — **not** merge authority)
- **Merge-push `main` CI** on merge commit: [`24122092800`](https://github.com/m-cahill/starlab/actions/runs/24122092800) (**success**)
- §3 / §6 / §7 / §10 / §11 / §18 / §20 / §23 updated: **governed canonical state schema v1** (narrow) **proved on `main`**; Phase III artifact row (M15); Phase III glossary (M15 vs M16 vs M17); **current milestone** → **M16** (stub); closeout ledger M15 row + compact table M14/M15 rows; score trend M15 note
- Milestone closeout: `M15_run1.md`, `M15_summary.md`, `M15_audit.md`, `M15_plan.md` (**Status: Complete**), `M15_toolcalls.md`; **M16** stubs seeded (`M16_plan.md`, `M16_toolcalls.md`)
- **Non-merge-boundary** `main` CI — closeout commit `1c1e89ed8137c5df9d2c0d7e0ee4e5ff886c00e0` (short `1c1e89e…`): [`24122183559`](https://github.com/m-cahill/starlab/actions/runs/24122183559) (**success**) — ledger + milestone artifacts only; **authoritative** PR-head / merge-boundary CI for M15 product merge remains [`24122064141`](https://github.com/m-cahill/starlab/actions/runs/24122064141) / [`24122092800`](https://github.com/m-cahill/starlab/actions/runs/24122092800)
- **Non-merge-boundary** `main` CI — follow-up commit `0764cae100848b52eb18933ce630daa7629c5ac3`: [`24122213663`](https://github.com/m-cahill/starlab/actions/runs/24122213663) (**success**) — changelog row for prior closeout run; **not** merge authority

### 2026-04-08 — M14 merged to `main` (PR #15) + closeout

- Merged [PR #15](https://github.com/m-cahill/starlab/pull/15) to `main` at **2026-04-08T05:00:41Z**; merge commit `8a0439a9a2970a74f3a5087390fc080f02852246` (merge method: **merge commit**); remote branch `m14-replay-bundle-lineage-contract-v1` **deleted**
- Final PR head `42e29f2a64fa4672dbd2df435a04836c379b5258` — **authoritative green PR-head CI:** [`24118622373`](https://github.com/m-cahill/starlab/actions/runs/24118622373) (**success**)
- **Merge-push `main` CI** on merge commit: [`24118654909`](https://github.com/m-cahill/starlab/actions/runs/24118654909) (**success**)
- §3 / §6 / §7 / §10 / §11 / §18 / §20 / §23 updated: **governed replay bundle packaging + lineage contract v1** (narrow) **proved on `main`**; Phase II artifact row (M14); **current milestone** → **M15** (stub); closeout ledger M14 row; score trend M14 note; Phase II complete with M14
- Milestone closeout: `M14_run1.md`, `M14_summary.md`, `M14_audit.md`, `M14_plan.md` (**Status: Complete**), `M14_toolcalls.md`; **M15** stubs seeded (`M15_plan.md`, `M15_toolcalls.md`)
- **Non-merge-boundary** `main` CI — closeout commit `680d966b5115e22cb67fee76da15c9a2c261de10` (short `680d966…`): [`24118726116`](https://github.com/m-cahill/starlab/actions/runs/24118726116) (**success**) — ledger + milestone artifacts only; **authoritative** PR-head / merge-boundary CI for M14 product merge remains [`24118622373`](https://github.com/m-cahill/starlab/actions/runs/24118622373) / [`24118654909`](https://github.com/m-cahill/starlab/actions/runs/24118654909)

### 2026-04-08 — M13 merged to `main` (PR #14) + closeout

- Merged [PR #14](https://github.com/m-cahill/starlab/pull/14) to `main` at **2026-04-08T01:20:38Z**; merge commit `f86e36837e81b8552639c5a885a13a773b96215c` (merge method: **merge commit**); remote branch `m13-replay-slice-generator` **deleted**
- Final PR head `6231b19cd7067130fd3324dcd3070172333ba766` — **authoritative green PR-head CI:** [`24112526047`](https://github.com/m-cahill/starlab/actions/runs/24112526047) (**success**)
- **Merge-push `main` CI** on merge commit: [`24112556177`](https://github.com/m-cahill/starlab/actions/runs/24112556177) (**success**)
- §3 / §6 / §7 / §10 / §11 / §18 / §20 / §23 updated: **governed replay slice definitions** (narrow) **proved on `main`**; Phase II artifact row (M13); slice/bundle glossary + Phase II boundary note; **current milestone** → **M14** (stub); closeout ledger M13 row; score trend M13 note
- Milestone closeout: `M13_run1.md`, `M13_summary.md`, `M13_audit.md`, `M13_plan.md` (**Status: Complete**), `M13_toolcalls.md`; **M14** stubs seeded (`M14_plan.md`, `M14_toolcalls.md`)

### 2026-04-07 — M12 merged to `main` (PR #13) + closeout

- Merged [PR #13](https://github.com/m-cahill/starlab/pull/13) to `main` at **2026-04-07T23:23:48Z**; merge commit `78528958a616177b564e603c193fb0d7f8af734e` (merge method: **merge commit**); remote branch `m12-combat-scouting-visibility-windows` **deleted**
- Final PR head `59adce3422a840692a4961278c995c5029da43bb` — **authoritative green PR-head CI:** [`24109242392`](https://github.com/m-cahill/starlab/actions/runs/24109242392) (**success**)
- **Merge-push `main` CI** on merge commit: [`24109269513`](https://github.com/m-cahill/starlab/actions/runs/24109269513) (**success**)
- §3 / §6 / §7 / §10 / §11 / §18 / §20 / §23 updated: **governed combat / scouting / visibility plane** (narrow) **proved on `main`**; **current milestone** → **M13** (stub); closeout ledger M12 row; score trend M12 note
- Milestone closeout: `M12_run1.md`, `M12_summary.md`, `M12_audit.md`, `M12_plan.md` (**Status: Complete**), `M12_toolcalls.md`; **M13** stubs seeded (`M13_plan.md`, `M13_toolcalls.md`)
- **Non-merge-boundary** `main` CI — closeout commit `87ab90fd9bec523409c609c9adb8d5465406f9c1`: [`24109339683`](https://github.com/m-cahill/starlab/actions/runs/24109339683) (**success**) — ledger + milestone artifacts only; **authoritative** PR-head / merge-boundary CI for M12 product merge remains [`24109242392`](https://github.com/m-cahill/starlab/actions/runs/24109242392) / [`24109269513`](https://github.com/m-cahill/starlab/actions/runs/24109269513)

### 2026-04-07 — M11 merged to `main` (PR #12) + closeout

- Merged [PR #12](https://github.com/m-cahill/starlab/pull/12) to `main` at **2026-04-07T21:49:23Z**; merge commit `38c15302badd49966b17f9195ddb139f6ae9a9b4` (merge method: **merge commit**); remote branch `m11-build-order-economy-plane` **deleted**
- Final PR head `88ce7f9615c6c462b76674e1afb0734fc3dcc5be` — **authoritative green PR-head CI:** [`24106029320`](https://github.com/m-cahill/starlab/actions/runs/24106029320) (**success**)
- **Merge-push `main` CI** on merge commit: [`24106124347`](https://github.com/m-cahill/starlab/actions/runs/24106124347) (**success**)
- §3 / §6 / §7 / §10 / §11 / §18 / §20 / §23 updated: **governed build-order / economy plane** (narrow) **proved on `main`**; **current milestone** → **M12** (stub); closeout ledger M11 row; score trend M11 note; Phase II layering chain + parser glossary alignment
- Milestone closeout: `M11_run1.md`, `M11_summary.md`, `M11_audit.md`, `M11_plan.md` (**Status: Complete**), `M11_toolcalls.md`; **M12** stubs seeded (`M12_plan.md`, `M12_toolcalls.md`)
- **Non-merge-boundary** `main` CI — closeout commit `0ebc81b6044c39809aa94f5e7f04915936b00e1e`: [`24106210049`](https://github.com/m-cahill/starlab/actions/runs/24106210049) (**success**) — ledger + milestone artifacts only; **authoritative** PR-head / merge-boundary CI for M11 product merge remains [`24106029320`](https://github.com/m-cahill/starlab/actions/runs/24106029320) / [`24106124347`](https://github.com/m-cahill/starlab/actions/runs/24106124347)

### 2026-04-07 — M10 merged to `main` (PR #11) + closeout

- Merged [PR #11](https://github.com/m-cahill/starlab/pull/11) to `main` at **2026-04-07T20:58:46Z**; merge commit `cb3e581f70f85653477081eb1ef4772229f05983` (merge method: **merge commit**); remote branch `m10-timeline-event-extraction` **deleted**
- Final PR head `cb066fe3f09b07f3390e85928c88f65a6e75cd6f` — **witnessed PR-head CI:** [`24104110934`](https://github.com/m-cahill/starlab/actions/runs/24104110934) (**cancelled** — no green merge-gate run on final tip)
- **Merge-push `main` CI** on merge commit: [`24104111851`](https://github.com/m-cahill/starlab/actions/runs/24104111851) (**failure** — Mypy)
- **Mypy repair** `cf2074e10ec8a38b22bd7b75ffeb4ec22a71485b` — **authoritative green `main` CI:** [`24104197912`](https://github.com/m-cahill/starlab/actions/runs/24104197912) (**success**) — **not** a merge-boundary event
- §3 / §6 / §7 / §10 / §11 / §18 / §20 / §23 updated: **governed event/timeline extraction** (narrow) **proved on `main`**; **current milestone** → **M11** (stub); closeout ledger M10 row; score trend M10 note
- Milestone closeout: `M10_run1.md`, `M10_summary.md`, `M10_audit.md`, `M10_plan.md` (**Status: Complete**), `M10_toolcalls.md`; **M11** remains stub-only (`M11_plan.md`, `M11_toolcalls.md`)
- **Non-merge-boundary** `main` CI — closeout commit `f78a435e50e27b725b34548d0037771d3bfccf49`: [`24104280039`](https://github.com/m-cahill/starlab/actions/runs/24104280039) (**success**) — **not** merge-boundary; **authoritative** green repair `main` remains `cf2074e…` / [`24104197912`](https://github.com/m-cahill/starlab/actions/runs/24104197912)

### 2026-04-07 — M10: timeline & event extraction (pre-merge implementation log)

- **Historical:** development log before **PR #11** merged **2026-04-07**; authoritative merge + CI — see changelog entry **2026-04-07 — M10 merged to `main` (PR #11) + closeout**
- **M10** delivers governed **`replay_timeline.json`** / **`replay_timeline_report.json`**, **`docs/runtime/replay_timeline_event_extraction.md`**, parser-boundary extension **`raw_event_streams`** on **`replay_raw_parse.json`** schema **`starlab.replay_raw_parse.v2`** (when the adapter lowers streams), extraction modules + CLI (`python -m starlab.replays.extract_replay_timeline`), and fixture-driven tests under `tests/fixtures/m10/`.
- **M09** accepts raw-parse schema **v1** or **v2** for metadata extraction linkage.

### 2026-04-07 — M09 merged to `main` (PR #10) + closeout

- Merged [PR #10](https://github.com/m-cahill/starlab/pull/10) to `main` at **2026-04-07T20:05:59Z**; merge commit `fc9b442d66abe9a2922e93051c7d0a22ccb133d1` (merge method: **merge commit**); remote branch `m09-replay-metadata-extraction` **deleted**
- Final PR head `3f161dea12a9b7ffb6dbe01c73b01f351a7219da` — **authoritative PR-head CI:** [`24101861888`](https://github.com/m-cahill/starlab/actions/runs/24101861888) (**success**)
- **Authoritative post-merge `main` CI** on merge commit: [`24101900950`](https://github.com/m-cahill/starlab/actions/runs/24101900950) (**success**)
- §3 / §6 / §7 / §10 / §11 / §18 / §20 / §23 updated: **stable normalized replay metadata** (narrow) **proved on `main`**; Phase II artifact row (M09); metadata field glossary; **current milestone** → **M10** (stub only)
- Milestone closeout: `M09_run1.md`, `M09_summary.md`, `M09_audit.md`, `M09_plan.md` (**Status: Complete**), `M09_toolcalls.md`; **M10** stubs seeded (`M10_plan.md`, `M10_toolcalls.md`).
- **Non-merge-boundary** `main` CI — closeout commit `147b1f4810ad2e0dbb926c7a971748c4db68bdbc`: [`24102029092`](https://github.com/m-cahill/starlab/actions/runs/24102029092) (**success**) — ledger + milestone artifacts only; **authoritative** merge-boundary post-merge `main` CI for M09 remains [`24101900950`](https://github.com/m-cahill/starlab/actions/runs/24101900950) on merge commit `fc9b442d66abe9a2922e93051c7d0a22ccb133d1`.
- **Non-merge-boundary** `main` CI — follow-up commit `44a0bce631854e6039442ca49609228a0650adf3`: [`24102071251`](https://github.com/m-cahill/starlab/actions/runs/24102071251) (**success**) — ledger / `M09_run1` non-merge-boundary row hygiene — **not** a merge-boundary event; **authoritative** merge-boundary post-merge `main` CI for M09 remains [`24101900950`](https://github.com/m-cahill/starlab/actions/runs/24101900950) on merge commit `fc9b442d66abe9a2922e93051c7d0a22ccb133d1`.
- **Non-merge-boundary** `main` CI — follow-up commit `2d3bc95d97b14a01d40d41b84565f270ca6b22ab`: [`24102113672`](https://github.com/m-cahill/starlab/actions/runs/24102113672) (**success**) — §23 / `M09_run1` sync for prior non-merge-boundary row — **not** a merge-boundary event; **authoritative** merge-boundary post-merge `main` CI for M09 remains [`24101900950`](https://github.com/m-cahill/starlab/actions/runs/24101900950) on merge commit `fc9b442d66abe9a2922e93051c7d0a22ccb133d1`.
- **Non-merge-boundary** `main` CI — follow-up commit `bdd75b95af1de4fae1ee1bf3f5dea0d0d6aabaec`: [`24102151912`](https://github.com/m-cahill/starlab/actions/runs/24102151912) (**success**) — ledger / `M09_run1` sync for `2d3bc95…` CI row — **not** a merge-boundary event; **authoritative** merge-boundary post-merge `main` CI for M09 remains [`24101900950`](https://github.com/m-cahill/starlab/actions/runs/24101900950) on merge commit `fc9b442d66abe9a2922e93051c7d0a22ccb133d1`.
- **Non-merge-boundary** `main` CI — follow-up commit `cedcd410b829261bc479ef4eb2a3faab2a07fd0c`: [`24102190259`](https://github.com/m-cahill/starlab/actions/runs/24102190259) (**success**) — ledger / `M09_run1` sync for `bdd75b9…` CI row — **not** a merge-boundary event; **authoritative** merge-boundary post-merge `main` CI for M09 remains [`24101900950`](https://github.com/m-cahill/starlab/actions/runs/24101900950) on merge commit `fc9b442d66abe9a2922e93051c7d0a22ccb133d1`.
- **Non-merge-boundary** `main` CI — follow-up commit `887037bb6af16cf3205423fc33ef71cd619d040d`: [`24102230285`](https://github.com/m-cahill/starlab/actions/runs/24102230285) (**success**) — ledger / `M09_run1` sync for `cedcd41…` CI row — **not** a merge-boundary event; **authoritative** merge-boundary post-merge `main` CI for M09 remains [`24101900950`](https://github.com/m-cahill/starlab/actions/runs/24101900950) on merge commit `fc9b442d66abe9a2922e93051c7d0a22ccb133d1`.
- **Non-merge-boundary** `main` CI — follow-up commit `b4c5cfc55b9c5203deee8adc3e113f2233d13ffe`: [`24102263459`](https://github.com/m-cahill/starlab/actions/runs/24102263459) (**success**) — final ledger / `M09_run1` sync for `887037b…` CI row (see `M09_run1` footnote on capping doc/CI rows) — **not** a merge-boundary event; **authoritative** merge-boundary post-merge `main` CI for M09 remains [`24101900950`](https://github.com/m-cahill/starlab/actions/runs/24101900950) on merge commit `fc9b442d66abe9a2922e93051c7d0a22ccb133d1`.
- **Non-merge-boundary** `main` CI — follow-up commit `f4d47ac2267b7993da6e2a94d47b5eb0c2402f08`: [`24102304889`](https://github.com/m-cahill/starlab/actions/runs/24102304889) (**success**) — `M09_run1` table cap + doc/CI loop-stop footnote (no new table row per that footnote) — **not** a merge-boundary event; **authoritative** merge-boundary post-merge `main` CI for M09 remains [`24101900950`](https://github.com/m-cahill/starlab/actions/runs/24101900950) on merge commit `fc9b442d66abe9a2922e93051c7d0a22ccb133d1`.

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
