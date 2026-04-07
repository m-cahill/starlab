# M10 Plan — Timeline & Event Extraction

**Milestone:** M10  
**Title:** Timeline & Event Extraction  
**Phase:** II — Replay Intake, Provenance, and Data Plane  
**Suggested branch:** `m10-timeline-event-extraction`  
**Suggested PR title:** `M10: timeline & event extraction`  
**Target tag:** `v0.0.10-m10`  
**Status:** Complete — merged to `main` ([PR #11](https://github.com/m-cahill/starlab/pull/11)); merge commit `cb3e581f70f85653477081eb1ef4772229f05983`; merge-push CI failed Mypy — repaired on `cf2074e10ec8a38b22bd7b75ffeb4ec22a71485b` (green `main` [`24104197912`](https://github.com/m-cahill/starlab/actions/runs/24104197912)); see `M10_run1.md`.

## 1. Objective

Deliver STARLAB’s first **governed event plane** by defining and implementing a **stable, deterministic replay timeline contract** over replay event streams, with narrow, conservative semantics and explicit non-claims.

This milestone proves only that STARLAB can:

1. Source replay event streams through the existing replay-parse boundary (extended with M10-owned `raw_event_streams` on `replay_raw_parse.json` v2 when lowered).
2. Normalize a bounded set of event families into a stable public contract.
3. Emit deterministic JSON artifacts and a governed extraction report.
4. Validate all of the above in **fixture-driven CI**.

## 2. Scope

### In scope

* Contract doc: `docs/runtime/replay_timeline_event_extraction.md`
* Deterministic public artifacts: `replay_timeline.json`, `replay_timeline_report.json`
* Conservative semantic extraction for the first semantic family set (see §6)
* Deterministic merge/order policy across event streams
* Optional lineage to prior artifacts (`replay_parse_receipt.json`, `replay_parse_report.json`, `replay_metadata.json`, `replay_metadata_report.json`)
* Fixture-driven tests and CLI
* Governance / ledger updates

### Out of scope

* Build-order / economy extraction → M11
* Combat, scouting, visibility windows → later
* Broad parser correctness claims; replay↔execution equivalence; benchmark integrity; live SC2 in CI
* Exhaustive raw event coverage
* Player display names, raw chat text, or other unnecessary PII-like surfaces in public artifacts

## 3. Key planning rule

M08 proves raw parse artifacts plus event-stream **availability flags** only. M10 adds **event stream lowering** behind the **same** parser boundary (`s2protocol_adapter` + `parser_io`) and keeps **semantic mapping** in pure extraction modules (M09 pattern: substrate + extraction).

## 4. Deliverables (implemented)

- `docs/runtime/replay_timeline_event_extraction.md`
- `starlab/replays/timeline_models.py`, `timeline_extraction.py`, `timeline_io.py`, `extract_replay_timeline.py`
- Parser boundary: `RawEventStreams`, `raw_event_streams` on successful parse → schema `starlab.replay_raw_parse.v2` when streams are lowered; v1 unchanged when adapter does not supply streams (fixture adapters).
- `tests/fixtures/m10/`, `tests/test_replay_timeline.py`, `tests/test_replay_timeline_cli.py`
- M09 accepts raw-parse schema v1 or v2 for metadata extraction.

## 5. Merge policy (determinism)

Sort by `gameloop` ascending, then fixed stream precedence `game`, `message`, `tracker`, then `source_event_index`. **This is canonical merge order for artifact determinism, not proof of exact intra-gameloop causality** (also stated in the runtime contract and ledger).

## 6. First semantic family set

`command_issued`, `unit_init`, `unit_born`, `unit_died`, `unit_owner_changed`, `unit_type_changed`, `upgrade_completed`, `message_event`, `ping_event` (chat/ping as metadata-only where applicable).

## 7. Closeout discipline

At most **one** post-merge `main` closeout/docs commit after merge; further doc-only churn should not recurse on `main` (see §17 ledger). **M10_run1.md** is authoritative on PR-head CI and merge-boundary `main` CI after merge.

## 8. Acceptance

See `docs/starlab.md` §10 / §11 / §23 and `docs/runtime/replay_timeline_event_extraction.md`. **Proof on `main`** is recorded when the M10 PR merges and §18 / CI rows are filled with merge commit and workflow run IDs.
