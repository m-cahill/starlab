# M13 Plan — Replay Slice Generator

## Milestone identity

**Milestone:** M13 — Replay Slice Generator  
**Phase:** II — Replay Intake, Provenance, and Data Plane  
**Recommended branch:** `m13-replay-slice-generator`

## Objective

Implement a **deterministic, governed replay slice-definition plane** that turns existing governed replay artifacts into **reusable temporal slice records**.

**What M13 should prove, narrowly:** STARLAB can deterministically derive **addressable temporal spans** from governed replay JSON surfaces and emit stable slice artifacts with lineage, reporting, and fixture-backed CI.

**What M13 must not claim:** raw `.SC2Replay` clipping, benchmark integrity, replay↔execution equivalence, fog-of-war truth, full simulation, or live SC2 in CI. M12’s standing guardrails still apply: timeline ordering remains authoritative, and `observation_proxy` remains a conservative replay-visible signal rather than certified vision truth.

## Resolved defaults

1. **Artifacts:** `replay_slices.json`, `replay_slices_report.json`
2. **Contract/profile names:** Contract `starlab.replay_slices_contract.v1`; Profile `starlab.replay_slices.m13.v1`
3. **M13 is metadata-only** — a slice is a **temporal span definition** over governed artifacts; no clipped replay bytes, sub-replay files, videos, tensors, or M14-style bundles.
4. **Required inputs:** `replay_timeline.json` (M10), `replay_build_order_economy.json` (M11), `replay_combat_scouting_visibility.json` (M12)
5. **Optional inputs:** timeline/BOE/CSV reports; metadata + metadata report — lineage/report enrichment and optional bounds check only.
6. **No raw parse dependency in M13 v1** — do not read `replay_raw_parse.json`.
7. **Slice families in v1:** `combat_window`, `scouting_observation`
8. **Visibility in v1:** overlap/context only; no separate `visibility_window` slice family.
9. **Fixed padding:** `SLICE_PADDING_PRE_LOOPS = 160`, `SLICE_PADDING_POST_LOOPS = 160`
10. **Combat `anchor_gameloop`:** locked to **combat window start** (M12 window start).
11. **`slice_id`:** canonical JSON → SHA-256 over **stable semantic fields** only; **exclude** overlap lists and overlap-derived tags so report enrichment does not churn IDs (see `docs/runtime/replay_slice_generation.md`).
12. **`replay_slice_catalog.py`:** included (M11/M12 catalog pattern).

## In scope

1. Runtime contract: `docs/runtime/replay_slice_generation.md`
2. Product code: `replay_slice_models.py`, `replay_slice_generation.py`, `replay_slice_io.py`, `replay_slice_catalog.py`, `extract_replay_slices.py`
3. Deterministic artifacts: `replay_slices.json`, `replay_slices_report.json`
4. Fixtures/tests: `tests/fixtures/m13/`, `tests/test_replay_slices.py`, `tests/test_replay_slices_cli.py`
5. Governance: `tests/test_governance.py`
6. **`docs/starlab.md`:** update at **closeout only** (Phase II artifact row for M13; glossary: M13 **slice** vs M14 **bundle**; short “Phase II slice/bundle boundary” note under layering chain)

## Out of scope

Raw replay byte slicing, `s2protocol`, parser CLI, benchmark labels, simulation, full FOW, bundle packaging (M14), live SC2 in CI, extra slice kinds beyond the two families.

## Proposed artifact shape (summary)

`replay_slices.json`: `contract`, `profile`, source hashes (timeline, BOE, CSV), `generation_parameters`, `slices[]` with `slice_id`, `slice_kind`, spans, `anchor_ref`, tags, overlap IDs.

`replay_slices_report.json`: counts, clipping counts, overlap summary, omitted candidates, duration summary, optional enrichment hashes.

## Acceptance criteria

1. Golden deterministic outputs from fixture inputs.
2. Pure over governed JSON — no `s2protocol`, parser CLIs, raw bytes.
3. Fail fast on lineage/hash mismatch.
4. Combat + scouting happy-path and edge tests.
5. Visibility = contextual overlap only in v1.
6. CLI + fixture-driven CLI tests.
7. CI green (Ruff, format, Mypy, Pytest, pip-audit, SBOM, Gitleaks).
8. Governance tests reflect M13.
9. `docs/starlab.md` closeout with exact M13 proof / non-proof language.
10. After closeout: seed M14 `M14_plan.md` and `M14_toolcalls.md` (stub-only).

## Explicit non-claims (summary/audit)

> M13 proves deterministic, lineage-linked replay slice definitions over governed replay artifacts.  
> M13 does not prove raw replay clipping, benchmark integrity, replay↔execution equivalence, fog-of-war truth, live SC2 in CI, or replay bundle packaging.

## Status

**In progress** — implementation branch (replace with PR/CI IDs at closeout).
