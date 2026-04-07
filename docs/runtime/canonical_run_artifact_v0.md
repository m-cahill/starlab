# Canonical run artifact v0 (M05)

**Status:** STARLAB-owned packaging boundary (Phase I).  
**Related:** M03 (`run_identity.json`, `lineage_seed.json`), M04 (`replay_binding.json`).

---

## What M05 proves

M05 proves that STARLAB can take **already-derived** M03 and M04 JSON records and emit a **deterministic, content-addressed directory bundle** — the first **canonical run artifact v0** — with:

- stable **per-record canonical JSON** re-emission (not raw byte copy of caller files),
- a **manifest** describing the bundle without wall-clock timestamps,
- **hashes** including a **`run_artifact_id`** derived from canonical JSON over sorted artifact hashes,
- **cross-artifact coherence** validation (fail fast on mismatched IDs).

---

## What M05 does not prove

M05 does **not** prove:

- replay parser correctness, replay semantic equivalence, or replay event extraction,
- replay provenance finalization beyond what M04 already records,
- benchmark integrity or leaderboard claims,
- cross-host reproducibility or cross-install portability,
- new live SC2 execution in CI (CI remains fixture-driven),
- inclusion of raw replay bytes, raw proof JSON, or raw match config in the bundle.

M05 proves **canonical packaging of STARLAB-owned run records**, not the full replay/data plane.

---

## Bundle layout

A canonical run artifact v0 is a **directory** (not `.zip` / `.tar.gz` in M05):

```text
<output-dir>/
  manifest.json
  run_identity.json
  lineage_seed.json
  replay_binding.json
  hashes.json
```

Raw replay bytes and raw proof/config files are **not** included. External references are recorded only via fields such as `replay_content_sha256` inside `replay_binding.json` / `manifest.json`.

---

## Manifest (`manifest.json`)

- **`schema_version`:** `starlab.canonical_run_artifact.v0`
- **`bundle_mode`:** `starlab_owned_records_only`
- **Identity fields:** `run_spec_id`, `execution_id`, `lineage_seed_id`, `replay_binding_id`, `proof_artifact_hash`, `replay_content_sha256` (aligned with M03/M04)
- **`included_artifacts`:** fixed **order-sensitive** list:

  `run_identity.json`, `lineage_seed.json`, `replay_binding.json`

  The builder **rejects** manifests (or internal construction) where this list does not match the canonical v0 shape exactly — package shape cannot drift silently.
- **`external_references`:** `proof_json_included: false`, `replay_bytes_included: false` in v0
- **`parent_references`:** `[]` in v0 (no richer lineage semantics smuggled into M05)
- **`later_milestones`:** static roadmap pointers (not claims)
- **No wall-clock timestamps** in the manifest (repeat runs with identical logical inputs must yield identical bundle identity).

---

## Hashes (`hashes.json`)

- **`schema_version`:** `starlab.canonical_run_artifact.hashes.v0`
- **`artifact_hashes`:** maps **bundle JSON filenames** (including `manifest.json`) to **SHA-256 hex** strings.
- **`run_artifact_id`:** SHA-256 hex over **compact canonical JSON** of:

  ```json
  {
    "artifact_hashes": {
      "lineage_seed.json": "<hex>",
      "manifest.json": "<hex>",
      "replay_binding.json": "<hex>",
      "run_identity.json": "<hex>"
    },
    "kind": "starlab.canonical_run_artifact.v0"
  }
  ```

  Keys under `artifact_hashes` are sorted lexicographically in JSON. **`hashes.json` itself is excluded** from the hashed payload (avoids circularity).

---

## Per-file hash rule

For each emitted JSON object, the per-file hash is **SHA-256 (hex) of compact canonical JSON** of that object (same semantics as `sha256_hex_of_canonical_json` in `starlab.runs.json_util`: sorted keys, `separators=(",", ":")`, UTF-8, no trailing newline). On-disk files use **pretty** canonical JSON with a trailing newline for reviewability; **identity hashes use the compact canonical form** so formatting choices do not affect IDs.

---

## Coherence rules (upstream)

Before writing output, the builder validates:

1. M03 `run_identity.json` schema (`starlab.run_identity.v1`)
2. M03 `lineage_seed.json` schema (`starlab.lineage_seed.v1`)
3. M04 `replay_binding.json` schema (`starlab.replay_binding.v1`), `binding_mode` = `opaque_content_sha256`, and internal **`replay_binding_id`** consistency
4. **`run_spec_id`** matches across all three artifacts
5. **`execution_id`** matches across all three artifacts
6. **`lineage_seed_id`** matches between `lineage_seed.json` and `replay_binding.json`
7. **`proof_artifact_hash`** matches across all three artifacts

**Failure posture:** explicit `ValueError` / CLI non-zero exit; no partial bundle claim; **no overwrite** of an existing `--output-dir` (M05).

---

## CLI

```bash
python -m starlab.runs.build_canonical_run_artifact \
  --run-identity path/to/run_identity.json \
  --lineage-seed path/to/lineage_seed.json \
  --replay-binding path/to/replay_binding.json \
  --output-dir path/to/out
```

The CLI accepts **only** those three JSON paths plus `--output-dir`. It does **not** accept replay, proof, or config paths (those boundaries remain M03/M04).

---

## Relationship to other milestones

| Milestone | Role |
|-----------|------|
| M03 | Non-canonical seed records; deterministic IDs |
| M04 | Narrow replay binding record (opaque bytes); input to M05 |
| **M05** | **Canonical directory bundle** over M03 + M04 JSON |
| M06 | Environment drift & runtime smoke matrix |
| M07 | Replay intake policy & provenance enforcement |
| M08 | Replay parser substrate |

---

## Worked fixture example (CI)

The test suite derives **M03** artifacts from `tests/fixtures/m02_match_config.json` + `tests/fixtures/m02_match_execution_proof.json`, builds **M04** `replay_binding.json` using `tests/fixtures/replay_m07_generated.SC2Replay`, then builds **M05** output and checks **`manifest.json` / `hashes.json`** against golden files under `tests/fixtures/m05_expected/`.
