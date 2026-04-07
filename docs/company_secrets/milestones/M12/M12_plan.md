# M12 Plan — Combat, Scouting, and Visibility Windows

**Milestone:** M12  
**Title:** Combat, Scouting, and Visibility Windows  
**Phase:** II — Replay Intake, Provenance, and Data Plane  
**Suggested branch:** `m12-combat-scouting-visibility-windows`  
**Suggested PR title:** `M12: combat scouting and visibility windows`  
**Target tag:** `v0.0.12-m12`

## Objective

Deliver STARLAB’s first governed **combat / scouting / visibility plane** with deterministic artifacts over governed upstream JSON only (`replay_timeline.json`, `replay_build_order_economy.json`, optional lineage, optional `replay_raw_parse.json` v2 supplemental).

## Layering

- **Required:** `replay_timeline.json`, `replay_build_order_economy.json` (consume M11 JSON directly; do not re-derive full macro from scratch).
- **Optional:** reports, metadata, raw parse v2 for identity / position / explicit visibility fields only.
- **No** `s2protocol`, **no** parser CLIs, **no** replay bytes in M12 modules.

## Fixed constants

- `COMBAT_WINDOW_GAP_LOOPS = 160` (documented; non-configurable in M12).

## Deliverables (implementation)

- `docs/runtime/replay_combat_scouting_visibility_extraction.md`
- `starlab/replays/combat_scouting_visibility_*.py`, `extract_replay_combat_scouting_visibility.py`
- `tests/fixtures/m12/`, `tests/test_replay_combat_scouting_visibility*.py`
- Governance / `docs/starlab.md` references updated for the contract and Phase II row.

## Closeout (post-merge, separate step)

- Green PR-head + merge-boundary `main` CI in `M12_run1.md`
- Ledger proved vs not proved, changelog, M13 stubs
- Audit/summary per prompts

**Status:** Implementation complete on branch pending review/merge; closeout artifacts follow merge discipline.
