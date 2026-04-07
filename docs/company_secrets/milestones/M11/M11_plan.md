# M11 Plan — Build-Order & Economy Plane

**Milestone:** M11  
**Title:** Build-Order & Economy Plane  
**Phase:** II — Replay Intake, Provenance, and Data Plane  
**Suggested branch:** `m11-build-order-economy-plane`  
**Suggested PR title:** `M11: build-order & economy plane`  
**Target tag:** `v0.0.11-m11`

## 1. Objective

Deliver STARLAB’s first governed **build-order and economy-relevant structure** over replay-derived timeline artifacts.

M11 should prove only that STARLAB can:

* consume governed upstream replay artifacts from the existing chain,
* derive a **bounded, deterministic build-order surface**,
* derive a **bounded, deterministic economy checkpoint surface**,
* emit stable JSON artifacts and a governed report,
* validate all of the above in fixture-driven CI.

## 2. Layering rule

M11 should be a **pure extraction milestone over governed upstream artifacts**, not a new parser milestone.

**Required primary input:**

* `replay_timeline.json`

**Optional lineage/context inputs may include:**

* `replay_timeline_report.json`
* `replay_metadata.json`
* `replay_metadata_report.json`

**Supplemental entity identity (Option A — locked):**

* `replay_raw_parse.json` schema **`starlab.replay_raw_parse.v2`** with optional **`raw_event_streams`**, used **only** to recover **non-PII entity identity** (names) needed for conservative classification.

M10’s public timeline contract is **privacy-scrubbed** and does not carry string fields such as `m_unitTypeName` / `m_upgradeTypeName` in public payloads. M11 therefore **may** read `replay_raw_parse.json` v2 `raw_event_streams` as a governed supplemental source for identity lookup **without** importing `s2protocol` or touching raw replay bytes.

**Ordering rule (locked):** When `replay_timeline.json` and supplemental `raw_event_streams` are both present, **timeline ordering wins** for all sequencing and step indexing. Supplemental raw-parse data is used **only** as an identity lookup aid keyed by `(source_stream, source_event_index)` (aligned to the timeline entry’s `source_stream` and `source_event_index`). M11 must not reinterpret parser semantics or substitute alternate event ordering from raw streams.

Do **not** make M11 depend directly on `s2protocol`, raw replay bytes, or direct event-stream decoding. M10 already established the public event/timeline plane; M11 sits on top of that chain.

## 3. Scope

### In scope

* A new runtime contract doc for governed build-order/economy extraction.
* Deterministic public artifacts for M11.
* Conservative classification of a bounded set of units / structures / upgrades into build-order and economy-relevant categories.
* Deterministic build-order steps per player.
* Deterministic economy checkpoints per player.
* Ordered reporting of unknown or unclassified entities rather than guessing.
* Fixture-driven tests and CLI.

### Explicitly out of scope

* Combat, scouting, and visibility windows — M12.
* Precise resource-stockpile reconstruction.
* Replay↔execution equivalence.
* Benchmark integrity.
* Broad Blizzard parser correctness.
* Live SC2 execution in CI.
* Full strategic interpretation of openings or matchup theory.
* Human-readable “coach” commentary or narrative inference.

## 4. Milestone sizing posture

Keep M11 intentionally conservative.

Do **not** attempt full macro-state simulation.
Do **not** attempt exact minerals / gas / larva / energy accounting.
Do **not** attempt “true strategy classification.”

Instead, make M11 prove a smaller but valuable surface:

* **build-order steps**
* **economy checkpoints**
* **category counts and milestone timings**
* **unknown surfacing**

## 5. Deliverables

### 5.1 Contract / docs

* `docs/runtime/replay_build_order_economy_extraction.md`

### 5.2 Product code

* `starlab/replays/build_order_economy_models.py`
* `starlab/replays/build_order_economy_extraction.py`
* `starlab/replays/build_order_economy_io.py`
* `starlab/replays/extract_replay_build_order_economy.py`

Optional:

* `starlab/replays/build_order_economy_catalog.py`

### 5.3 Test assets

* `tests/fixtures/m11/`
* `tests/test_replay_build_order_economy.py`
* `tests/test_replay_build_order_economy_cli.py`

Update governance expectations only where necessary.

## 6. Artifact contract (summary)

Public artifact names:

* `replay_build_order_economy.json`
* `replay_build_order_economy_report.json`

Identifiers:

* `build_order_economy_contract_version`: `starlab.replay_build_order_economy_contract.v1`
* `build_order_economy_profile`: `starlab.replay_build_order_economy.m11.v1`

See `docs/runtime/replay_build_order_economy_extraction.md` for field-level details.

## 7. Conservative classification model

Suggested categories:

* `worker`
* `townhall`
* `gas_structure`
* `supply_provider`
* `production_structure`
* `tech_structure`
* `economy_upgrade`
* `tech_upgrade`
* `combat_or_other`
* `unknown`

Guidelines:

* `worker`, `townhall`, `gas_structure`, `supply_provider`, `production_structure`, and `tech_structure` are the core economy/build-order surface.
* `combat_or_other` should be allowed as a reported category, but do not overuse it for milestone claims.
* `unknown` must be preserved and reported, never silently reclassified.

## 8. Event-to-build-order mapping

Use M10 timeline entries **in `timeline_index` order** and map them conservatively.

Recommended mapping:

* `unit_init` on a classified structure → `phase = started`
* `unit_born` on a classified unit/structure → `phase = completed`
* `upgrade_completed` on a classified upgrade → `phase = completed`
* `unit_type_changed` only where a curated, explicit morph rule exists → `entity_kind = morph`, `phase = completed`
* `command_issued`, `message_event`, `ping_event`, `unit_owner_changed`, `unit_died` should **not** become build-order steps unless there is an explicit, documented reason

## 9. Economy checkpoint semantics

Economy checkpoints should be **event-driven cumulative snapshots**, not simulated resource states.

Create a checkpoint when a build-order step affects one of:

* worker count
* townhall count
* gas structure count
* supply provider count
* production structure count
* tech structure count
* economy upgrade count

## 10. Unknown handling

Unknowns must be first-class.

Do not guess when:

* a unit name is not in the catalog
* an upgrade name is not in the catalog
* a morph cannot be classified safely
* an upstream timeline entry lacks required fields

Instead:

* omit the derived step if necessary,
* count it deterministically,
* report it in the report artifact,
* surface warnings.

## 11. Implementation phases

* **Phase A — Contract and taxonomy lock** — runtime contract doc.
* **Phase B — Curated catalog** — hand-maintained, narrow.
* **Phase C — Extractor + report + CLI** — deterministic steps, checkpoints, lineage, optional linkage validation.
* **Phase D — Fixtures, tests, governance** — synthetic fixtures + CI.

## 12. Test plan

Required tests:

* deterministic golden-output tests for both JSON artifacts
* category/classification mapping test
* unknown entity reporting test
* ordering stability test
* economy checkpoint accumulation test
* optional lineage hash-check test
* CLI success-path test
* CLI malformed-input / contract-failure test

## 13. Acceptance criteria

M11 is done when all of the following are true:

1. `docs/runtime/replay_build_order_economy_extraction.md` exists and matches implementation.
2. STARLAB emits deterministic `replay_build_order_economy.json` and `replay_build_order_economy_report.json`.
3. M11 depends on governed timeline artifacts; supplemental raw-parse v2 is optional and identity-only.
4. Unknown units/upgrades are reported deterministically, not guessed.
5. Economy output is explicitly checkpoint-based and does **not** claim exact resource-state reconstruction.
6. CI remains fixture-driven and green.
7. `docs/starlab.md` is updated narrowly and honestly at closeout.
8. M11 summary/audit/run docs are produced.
9. M12 stubs are seeded after M11 closeout.
10. No M12 product code lands in M11.

## 14. Guardrails for Cursor

* Do **not** import `s2protocol` or raw parser code into M11 modules.
* Do **not** widen into combat/scouting/visibility.
* Do **not** claim exact mineral / gas / larva / energy accounting.
* Do **not** silently classify unknown entities.
* Do **not** weaken CI or governance checks.
* Do **not** add live SC2 execution to CI.
* Keep extraction logic separate from I/O and CLI.

## 15. CI / merge discipline guardrail

* Do **not** merge M11 while the final `pull_request` CI run is pending or cancelled;
* require a witnessed **green PR-head CI** on the final tip before merge;
* after merge, record the authoritative merge-boundary `main` CI separately from any repair or doc-only pushes.

## 16. Closeout discipline

Reuse the tightened closeout rule:

* one post-merge `main` closeout/docs commit at most;
* any further fixes go on the next milestone branch.

Also keep `M11_run1.md` capped and avoid infinite non-merge-boundary CI tables.

## 17. Required ledger updates at closeout

At M11 closeout, update `docs/starlab.md` at minimum in:

* header/status
* Phase II artifact contract table
* milestone table
* proved vs not yet proved
* current milestone section
* closeout ledger
* score trend
* changelog

Advance the current milestone to M12 after closeout.

## 18. Suggested `docs/starlab.md` improvements (at or after closeout)

1. Add a compact **CI authority glossary** near the closeout section.
2. Add a compact **Phase II layering chain** to the parser/timeline glossary.

---

**Status:** Execution plan — replace stub only when superseded by milestone governance.
