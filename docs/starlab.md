# STARLAB — Canonical Project Ledger

**Status:** Active / post-M00 (M01 next)  
**License:** Source-available (evaluation and verification only); see `LICENSE`  
**Governance Model:** Milestone-Driven, CI-Enforced  
**Audit Posture:** Active Governance Signal  
**Primary document:** `docs/starlab.md`

---

## Start Here

1. Read `docs/starlab-vision.md` for the moonshot framing and long-range thesis.  
2. Read `docs/bicetb.md` for licensing, provenance, and diligence posture (“clean enough to buy”).  
3. Read this file for current status, phase structure, milestone history, and project rules.  
4. Read governance docs: `docs/public_private_boundary.md`, `docs/replay_data_provenance.md`, `docs/rights_register.md`, `docs/branding_and_naming.md`, and `docs/deployment/deployment_posture.md`.  
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

### Phase I — Foundation & Environment Lock

Focus:

- repo governance
- runtime/environment lock
- replay capture
- deterministic artifact beginnings

### Phase II — Replay & Data Plane

Focus:

- replay metadata
- timeline extraction
- build-order/event extraction
- replay lineage

### Phase III — State & Representation

Focus:

- canonical state surfaces
- structured-state baseline
- perceptual bridge planning
- cross-representation evaluation posture

### Phase IV — Evaluation & Baselines

Focus:

- scripted / heuristic baselines
- benchmark scorecards
- regression harnesses
- replay-grounded evaluation

### Phase V — Learning Agents & Showcase

Focus:

- imitation-learning baseline
- hierarchical agent interfaces
- first learned agent surfaces
- replay explorer / evidence demo

### Phase VI — Platform Expansion (conditional / later)

Focus:

- multi-environment readiness
- optional second environment
- platformization only if earned by milestones below

---

## 7. Milestone table

Planned initial arc:

| Milestone | Name                                          | Phase | Status  | Tag         | Audit Score |
| --------- | --------------------------------------------- | ----- | ------- | ----------- | ----------- |
| M00       | Governance Bootstrap & Ledger Initialization  | I     | Complete | v0.0.0-m00  | —           |
| M01       | Environment Lock & Runtime Baseline           | I     | Planned | v0.0.1-m01  | —           |
| M02       | Match Execution Harness                       | I     | Planned | v0.0.2-m02  | —           |
| M03       | Replay Capture & Binding                      | I     | Planned | v0.0.3-m03  | —           |
| M04       | Canonical Run Artifact                        | I     | Planned | v0.0.4-m04  | —           |
| M05       | Replay Parser Substrate                       | II    | Planned | v0.0.5-m05  | —           |
| M06       | Build-Order & Economy Extraction              | II    | Planned | v0.0.6-m06  | —           |
| M07       | Combat & Scouting Windows                     | II    | Planned | v0.0.7-m07  | —           |
| M08       | Curriculum Slice Generation                   | II    | Planned | v0.0.8-m08  | —           |
| M09       | Replay Bundle & Lineage Surface               | II    | Planned | v0.0.9-m09  | —           |
| M10       | Canonical State Schema                        | III   | Planned | v0.0.10-m10 | —           |
| M11       | Structured-State Pipeline                     | III   | Planned | v0.0.11-m11 | —           |
| M12       | Perceptual-State Bridge (initial)             | III   | Planned | v0.0.12-m12 | —           |
| M13       | Cross-Mode Reconciliation                     | III   | Planned | v0.0.13-m13 | —           |
| M14       | Scripted Baseline Suite                       | IV    | Planned | v0.0.14-m14 | —           |
| M15       | Benchmark Harness & Scorecards                | IV    | Planned | v0.0.15-m15 | —           |
| M16       | Tournament / Evaluation Runner                | IV    | Planned | v0.0.16-m16 | —           |
| M17       | Layer-Wise Attribution & Evaluation Views     | IV    | Planned | v0.0.17-m17 | —           |
| M18       | Baseline Evidence Pack                        | IV    | Planned | v0.0.18-m18 | —           |
| M19       | Replay-Derived Imitation Baseline             | V     | Planned | v0.0.19-m19 | —           |
| M20       | Hierarchical Agent Interface Layer            | V     | Planned | v0.0.20-m20 | —           |
| M21       | First Hierarchical Learned Agent              | V     | Planned | v0.0.21-m21 | —           |
| M22       | Replay Explorer / Operator Evidence Surface   | V     | Planned | v0.0.22-m22 | —           |
| M23       | Public Flagship Proof Pack                    | V     | Planned | v0.0.23-m23 | —           |
| M24       | Platform Boundary Review & Expansion Decision | VI    | Planned | v0.0.24-m24 | —           |

**Rule:** milestone names may tighten over time, but scope should remain small and reversible by default.

---

## 8. Milestone intent map

This section exists so each milestone has a stable “why,” not just a title.

| Milestone | Intent                                                      |
| --------- | ----------------------------------------------------------- |
| M00       | Make the project legible, governed, and safe to start       |
| M01       | Lock the environment and remove avoidable runtime ambiguity |
| M02       | Prove that controlled execution is possible                 |
| M03       | Prove replay capture exists and can be tied to runs         |
| M04       | Establish the first canonical artifact boundary             |
| M05       | Turn replays into a real analyzable substrate               |
| M06       | Extract macro-game structure                                |
| M07       | Extract tactical and scouting structure                     |
| M08       | Turn replays into reusable benchmark slices                 |
| M09       | Package replay evidence coherently                          |
| M10       | Define what the lab considers “state”                       |
| M11       | Build the structured-state baseline                         |
| M12       | Add an initial perceptual path without overcommitting       |
| M13       | Make structured vs perceptual comparisons possible          |
| M14       | Create simple baseline agents                               |
| M15       | Create benchmark and scoring credibility                    |
| M16       | Run controlled comparisons at scale                         |
| M17       | Make evaluation more interpretable                          |
| M18       | Publish a baseline-quality evidence pack                    |
| M19       | Add the first learning-based path safely                    |
| M20       | Prevent agent growth from becoming monolithic               |
| M21       | Demonstrate the first learned hierarchical result           |
| M22       | Make the lab easier to inspect publicly                     |
| M23       | Produce a flagship proof package                            |
| M24       | Decide whether the project has earned platform expansion    |

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
| Environment stability | Not yet proved |
| Replay capture / binding | Not yet proved |
| Canonical run artifacts | Not yet proved |
| Parser substrate | Not yet proved |
| Benchmark integrity | Not yet proved |
| Learning or agent capability | Not yet proved |

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

### M01 — Environment Lock & Runtime Baseline

**Status:** Planned (next)

**Goal:** Lock the environment and remove avoidable runtime ambiguity (see milestone table).

**Note:** M00 closeout details are recorded in §18 and the changelog.

---

## 12. Open decisions

| ID     | Decision                         | Status   | Target Milestone | Notes                                                              |
| ------ | -------------------------------- | -------- | ---------------- | ------------------------------------------------------------------ |
| OD-001 | License posture                  | Resolved | M00              | Custom source-available terms in `LICENSE` (evaluation/verification); public/private surfaces governed by `docs/public_private_boundary.md` |
| OD-002 | Public/private boundary          | Resolved | M00              | `docs/public_private_boundary.md`                                  |
| OD-003 | Replay/data provenance policy    | Conditionally resolved | M00 / M01 | Interim policy in `docs/replay_data_provenance.md`; refine with ingestion in M01+ |
| OD-004 | Naming / brand diligence posture | Resolved | M00              | `docs/branding_and_naming.md`                                      |
| OD-005 | SC2 runtime surface selection    | Open     | M01              | Must remain a boundary decision, not a scattered dependency choice |
| OD-006 | Rights register format           | Resolved | M00              | `docs/rights_register.md` (canonical); this ledger summarizes      |
| OD-007 | Second-environment posture       | Deferred | M24              | Explicitly not a starting decision                                 |

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

**M00 PR head (pre-merge):** `5dcb6cf6f95af23b58c6af202d58a7bcad1d0b91`

**M00 CI evidence (authoritative)**

| Event | Workflow run | Conclusion | URL |
| ----- | ------------ | ---------- | --- |
| PR #1 head | `24015581129` | success | https://github.com/m-cahill/starlab/actions/runs/24015581129 |
| `main` after merge (`f9203dd…`) | `24015599413` | success | https://github.com/m-cahill/starlab/actions/runs/24015599413 |
| `main` after M00 evidence finalization (`523993e…`) | `24015634285` | success | https://github.com/m-cahill/starlab/actions/runs/24015634285 |

**M00 milestone artifacts:** `docs/company_secrets/milestones/M00/` (`M00_summary.md`, `M00_audit.md`, `M00_run1.md`, etc.)

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
