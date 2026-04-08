# M14 Plan — Replay Bundle & Lineage Contract v1

## Milestone identity

**Milestone:** M14 — Replay Bundle & Lineage Contract v1  
**Phase:** II — Replay Intake, Provenance, and Data Plane  
**Recommended branch:** `m14-replay-bundle-lineage-contract-v1`  
**Target tag:** `v0.0.14-m14`

## Objective

Implement a **deterministic, governed replay bundle packaging surface** that packages already-governed replay artifacts into a stable bundle with a **lineage contract v1**.

M14 proves, narrowly, that STARLAB can take the Phase II governed replay artifacts and produce a **portable, deterministic bundle manifest plus lineage record** suitable for downstream consumption and audit.

M14 must **not** claim: raw replay clipping, replay↔execution equivalence, benchmark integrity, live SC2 in CI, fog-of-war truth, simulation correctness, state-schema or learning claims.

**Boundary:** M13 defines slices; M14 packages bundles and lineage.

## Resolved defaults

1. **Bundle artifacts:** `replay_bundle_manifest.json`, `replay_bundle_lineage.json`, and **`replay_bundle_contents.json` in v1** (inventory-only; not a second manifest).
2. **Contract/profile:** `starlab.replay_bundle_contract.v1` / `starlab.replay_bundle.m14.v1`
3. **M14 is package-manifest only** — no clipped replay binary, no archive format requirement; directory layout is for deterministic JSON outputs only.
4. **Primary bundle members (required):** `replay_metadata.json` (M09), `replay_timeline.json` (M10), `replay_build_order_economy.json` (M11), `replay_combat_scouting_visibility.json` (M12), `replay_slices.json` (M13).
5. **Secondary members:** matching `*_report.json` when present, clearly separated in the manifest (`primary_artifacts` vs `secondary_report_artifacts`).
6. **Not bundle members in v1:** M07 intake receipt, M08 parse receipt, `replay_binding.json`, M05 run-artifact files — they may appear only as **optional contextual lineage** in `replay_bundle_lineage.json` when supplied via CLI.
7. **No raw replay bytes, no `replay_raw_parse.json` in bundle v1**; no zip/tar requirement.
8. **Manifest:** explicit `primary_artifacts` and `secondary_report_artifacts` fields (not only role strings).
9. **Lineage:** required depth M09–M14; optional M07/M08 nodes are **contextual ancestry**, not part of the required proof surface (see `optional_contextual_ancestry_note` in lineage JSON).

## In scope

1. Runtime contract: `docs/runtime/replay_bundle_lineage_contract.md`
2. Product code: `replay_bundle_models.py`, `replay_bundle_catalog.py`, `replay_bundle_generation.py`, `replay_bundle_io.py`, `extract_replay_bundle.py`
3. Deterministic outputs: manifest, lineage, contents
4. Fixtures/tests: `tests/fixtures/m14/`, `tests/test_replay_bundle.py`, `tests/test_replay_bundle_cli.py`
5. Governance: `tests/test_governance.py`

## Out of scope

Replay clipping, bundle archives with replay bytes, `s2protocol`, parser CLI, raw parse re-ingestion, benchmark semantics, state-schema work, M15 surfaces, live SC2 CI.

## Acceptance criteria

1. Golden deterministic manifest/lineage/contents from fixture inputs.
2. Explicit, deterministic bundle membership; fail fast on lineage/hash mismatch.
3. Clear distinction: slices vs bundle, primary vs secondary vs excluded.
4. No raw replay bytes, no raw parse in bundle, no `s2protocol`, no parser invocation.
5. CLI + fixture tests; CI green (Ruff, format, Mypy, Pytest, pip-audit, SBOM, Gitleaks).
6. Governance tests updated.
7. `docs/starlab.md` ledger closeout with exact M14 proof/non-proof language (on merge/closeout).
8. After closeout: seed M15 stubs per workflow.

## Explicit non-claims (summary/audit)

> M14 proves deterministic replay bundle packaging and lineage contract v1 over governed replay artifacts.  
> M14 does not prove raw replay clipping, replay↔execution equivalence, benchmark integrity, live SC2 in CI, or canonical state semantics.

## Status

**In progress** — implementation on branch `m14-replay-bundle-lineage-contract-v1` (see PR when opened).
