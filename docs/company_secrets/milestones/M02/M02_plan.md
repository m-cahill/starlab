# M02 Plan — Deterministic Match Execution Harness

## Milestone identity

* **Milestone:** M02
* **Title:** **Deterministic Match Execution Harness**
* **Phase:** I — Governance, Runtime Surface, and Deterministic Run Substrate
* **Suggested branch:** `m02-deterministic-match-execution-harness`
* **Suggested tag on closeout:** `v0.0.2-m02`

## Objective

Build the first **real execution proof** for STARLAB by running a controlled StarCraft II match under the M01 boundary and producing a small, STARLAB-owned, deterministic execution artifact.

M02 should prove that STARLAB can:

* launch a configured SC2 runtime
* connect through the approved runtime boundary
* create and join a game in a controlled way
* advance the simulation in a bounded, deterministic manner
* emit a normalized execution proof artifact whose deterministic fields are stable across repeated runs of the same configuration on the same machine

M02 should **not** prove replay analysis, replay binding, canonical run artifacts, or benchmark validity yet.

## Why this is the right M02 scope

M01 locked the canonical boundary as **SC2API / `s2client-proto`** for control and observation, with `s2protocol` reserved as the replay decode reference and `python-sc2` allowed only behind an explicit adapter boundary. The official SC2 API already supports the smallest useful proof slice for M02: a **single-client bot vs built-in AI** flow, single-step execution, observation/action requests, multiple interface modes, and a `random_seed` field in `RequestCreateGame`. That makes a seeded, single-player, bounded execution slice the cleanest milestone-sized proof surface.

## Success statement

At M02 closeout, STARLAB should be able to say:

> On a configured local SC2 installation, STARLAB can run a bounded, seeded SC2 match execution slice under the M01 boundary and emit a deterministic STARLAB-owned execution proof artifact.
> This proves controlled deterministic match execution at the harness layer.
> It does **not** yet prove replay binding, replay parsing correctness, canonical run artifacts, or benchmark integrity.

## Proof target

The M02 proof should be intentionally small:

* **one local SC2 client**
* **single-player bot vs built-in AI**
* **single-step mode**
* **fixed random seed**
* **fixed map selection**
* **bounded execution horizon**
* **deterministic STARLAB proof artifact**
* **repeat the same run twice on the same machine and compare normalized artifact hashes**

## Scope

### In scope

* minimal local execution harness
* explicit adapter boundary for the chosen runtime implementation
* optional SC2 runtime dependencies behind an extra, not the default install
* deterministic STARLAB execution proof artifact
* bounded local proof runs on the developer machine
* CI-safe fake-adapter and unit tests
* updated runtime docs and ledger
* truthful milestone evidence

### Out of scope

* multi-client bot-vs-bot orchestration
* replay parsing or replay file analytics
* replay lineage / replay binding
* canonical run artifact v0
* tournament infrastructure
* benchmarking
* ladder play
* hosted or remote execution
* committing binaries, maps, replays, or Battle.net cache assets

## Hard guardrails

* **Do not start M03, M04, or M05 inside M02.**
* **Do not treat wrapper behavior as STARLAB’s public contract.**
* **Do not commit SC2 binaries, maps, generated replays, or cache assets.**
* **Do not require SC2 in CI.**
* **Do not overclaim portability.** M02 is a **local deterministic harness proof**, not a cross-host reproducibility certification.
* **Do not let execution evidence depend on raw upstream bytes staying stable.** STARLAB-owned claims should attach to STARLAB-owned normalized artifacts, not upstream quirks.

## Implementation posture (locked for this repo)

### Adapter rule

* keep the canonical contract rooted in the **official SC2API**
* allow the implementation to use the **smallest viable adapter**
* **M02 uses `burnysc2` (python-sc2 fork)** behind `starlab/sc2/adapters/`; wrapper-specific types do not leak into public STARLAB surfaces

### Dependency rule

M02 adds an **optional** dependency group `sc2-harness` (`burnysc2`) for the real adapter; default install stays lightweight; CI does not require SC2.

### Map / environment rule

* treat the Battle.net install as **probe-discovered** (`STARLAB_SC2_*` / `run_probe`); do not assume fixed install paths in code or docs
* prefer an explicitly configured local map path; otherwise discover a stable `.SC2Map` under the install `Maps/` tree
* do not require cached ladder map names

### Step horizon (locked)

* default **100** bounded game steps (`game_step=1` in harness) unless documented adjustment is needed

## Required deliverables

1. `docs/runtime/match_execution_harness.md`
2. Harness code: `match_config.py`, `harness.py`, `artifacts.py`, `adapters/` (real + fake), map helper
3. Deterministic proof artifact schema v1 (`match_execution_proof`)
4. CLI: `python -m starlab.sc2.run_match`
5. Tests: config, artifacts, fake harness, map resolution, governance alignment
6. Local evidence under `docs/company_secrets/milestones/M02/` (execution note, redacted proof, determinism check)
7. `docs/starlab.md` updates per milestone workflow (early + closeout)

## Acceptance criteria

1. A real local SC2 execution run succeeds under the M01 boundary (developer machine).
2. The harness supports a bounded, seeded, single-step execution slice.
3. A STARLAB-owned deterministic proof artifact is produced.
4. Same config twice on the same machine → matching normalized proof artifact hashes, or a documented explanation if not.
5. CI remains green without SC2.
6. Adapter-specific dependency is optional and isolated.
7. No Blizzard assets committed.
8. `docs/starlab.md` updated truthfully.
9. M02 does **not** claim replay parsing, replay binding, canonical run artifacts, or benchmark validity.
