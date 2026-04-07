# Replay binding (M04)

This document defines the **M04** contract: deterministic **replay binding** that links a replay file's opaque content identity to the existing **M03** run identity and lineage seed records.

**This record is not the canonical run artifact (M05).** It is a narrow binding that proves STARLAB can attach a replay file's content hash to existing identity records without parsing replay semantics.

---

## What M04 proves

- STARLAB can compute a **deterministic `replay_content_sha256`** from replay file bytes treated as opaque input.
- STARLAB can derive a **deterministic `replay_binding_id`** from the combination of M03 identity records and replay content hash.
- STARLAB can emit a **stable, reviewable `replay_binding.json`** artifact linking replay content to run identity, execution identity, and lineage seed.
- The derivation path is **CI-safe**: it operates on M03 JSON artifacts and a synthetic replay fixture without requiring StarCraft II execution.

---

## What M04 does not prove

- **Replay parser correctness** — M04 treats replays as opaque bytes; no `.SC2Replay` format parsing occurs.
- **Replay semantic equivalence** — M04 does not verify that the replay file corresponds to the execution proof.
- **Replay event extraction** — no timeline, build-order, or game-event data is extracted.
- **Canonical run artifact v0** — full governed run packaging is **M05**.
- **Benchmark integrity** — no evaluation or scoring claims attach to replay binding.
- **Cross-host reproducibility** — still not claimed; M02's harness claim remains narrow.
- **New live SC2 execution proof in CI** — CI remains fixture-driven.

---

## Definitions

### Replay content SHA-256

**Meaning:** SHA-256 hex digest of the replay file's raw bytes, computed without any parsing or transformation.

**Source input:** the complete file content of the replay file, read as binary.

**Output:** 64 lowercase hex characters.

**Posture:** This is the replay-file identity primitive for M04. It is content-first — absolute paths, timestamps, and filenames do not affect the hash.

---

### Replay reference (metadata)

**Meaning:** Human-readable metadata about the replay file, recorded for operator review but **not** part of the identity hash.

**Fields:**

| Field | Type | Notes |
| ----- | ---- | ----- |
| `basename` | string | Filename without directory path |
| `suffix` | string | File extension (e.g. `.SC2Replay`) |
| `size_bytes` | integer | File size in bytes |

**Posture:** Informational only. Changes to basename or suffix do not affect `replay_binding_id` or `replay_content_sha256`.

---

### Replay binding ID

**Meaning:** Deterministic identity of the STARLAB-owned binding record that links replay content to M03 run identity records.

**Source inputs (hashed payload):**

- `run_spec_id` — from M03 `run_identity.json`
- `execution_id` — from M03 `run_identity.json`
- `lineage_seed_id` — from M03 `lineage_seed.json`
- `proof_artifact_hash` — from M03 `run_identity.json`
- `replay_content_sha256` — computed from replay file bytes

**Hashing:** SHA-256 over canonical JSON (UTF-8, sorted keys, compact separators) of:

```json
{
  "execution_id": "<hex>",
  "kind": "starlab.replay_binding.v1",
  "lineage_seed_id": "<hex>",
  "proof_artifact_hash": "<hex>",
  "replay_content_sha256": "<hex>",
  "run_spec_id": "<hex>"
}
```

**Output:** 64 lowercase hex characters.

**Important:** `replay_reference` metadata (basename, suffix, size) is **not** included in the hash payload. Only content-derived and identity-derived values participate.

---

## Emitted artifact

### `replay_binding.json`

```json
{
  "schema_version": "starlab.replay_binding.v1",
  "replay_binding_id": "<hex>",
  "run_spec_id": "<hex>",
  "execution_id": "<hex>",
  "lineage_seed_id": "<hex>",
  "proof_artifact_hash": "<hex>",
  "replay_content_sha256": "<hex>",
  "replay_reference": {
    "basename": "example.SC2Replay",
    "suffix": ".SC2Replay",
    "size_bytes": 1234
  },
  "binding_mode": "opaque_content_sha256",
  "parent_references": [],
  "later_milestones": [
    "M05 canonical run artifact v0",
    "M08 replay parser substrate"
  ]
}
```

**Field summary:**

| Field | Source | Identity input? |
| ----- | ------ | --------------- |
| `schema_version` | static | no (implicit in `kind`) |
| `replay_binding_id` | derived | — (this is the output) |
| `run_spec_id` | M03 `run_identity.json` | **yes** |
| `execution_id` | M03 `run_identity.json` | **yes** |
| `lineage_seed_id` | M03 `lineage_seed.json` | **yes** |
| `proof_artifact_hash` | M03 `run_identity.json` | **yes** |
| `replay_content_sha256` | computed from replay bytes | **yes** |
| `replay_reference` | computed from replay file metadata | no |
| `binding_mode` | static literal | no |
| `parent_references` | `[]` in M04 | no |
| `later_milestones` | static list | no |

---

## Relationship to M03 artifacts

M04 reads existing M03 artifacts as **authoritative upstream inputs**:

- **`run_identity.json`** provides: `run_spec_id`, `execution_id`, `proof_artifact_hash`
- **`lineage_seed.json`** provides: `lineage_seed_id`

M04 does **not** recompute M03 identity values from raw proof/config files. The M03 derivation boundary is closed.

---

## Relationship to later milestones

| Milestone | What it adds relative to M04 |
| --------- | ------------------------------ |
| **M05 — Canonical run artifact v0** | First canonical packaged run artifact; may wrap or reference `replay_binding.json` as an input. |
| **M08 — Replay parser substrate** | Parses `.SC2Replay` format semantics; M04's opaque binding is intentionally below this scope. |

---

## CLI reference

```bash
python -m starlab.runs.bind_replay \
  --run-identity path/to/run_identity.json \
  --lineage-seed path/to/lineage_seed.json \
  --replay path/to/replay.SC2Replay \
  --output-dir path/to/out
```

**Behavior:**

1. Load and validate M03 `run_identity.json` (extract `run_spec_id`, `execution_id`, `proof_artifact_hash`)
2. Load and validate M03 `lineage_seed.json` (extract `lineage_seed_id`)
3. Read replay file as opaque bytes; compute `replay_content_sha256`
4. Collect replay reference metadata (basename, suffix, size)
5. Derive `replay_binding_id` from canonical JSON hash payload
6. Write deterministic `replay_binding.json` to output directory

**Does not accept:** raw proof or config files. M04 CLI operates on M03 artifacts only.

---

## Worked example (synthetic fixture)

**Inputs:**

- `run_identity.json` — generated from M02 fake-adapter fixtures via `seed_from_proof`
- `lineage_seed.json` — generated alongside `run_identity.json`
- `synthetic_opaque_test.SC2Replay` — small deterministic byte fixture (not a real Blizzard replay)

**Flow:**

1. Compute `replay_content_sha256` = SHA-256 of `synthetic_opaque_test.SC2Replay` bytes.
2. Read `run_spec_id`, `execution_id`, `proof_artifact_hash` from `run_identity.json`.
3. Read `lineage_seed_id` from `lineage_seed.json`.
4. Build hash payload with `kind: "starlab.replay_binding.v1"` and sorted keys.
5. Compute `replay_binding_id` = SHA-256 of canonical JSON payload.
6. Emit `replay_binding.json` with all fields.

**Determinism proof:** Re-running with identical inputs produces identical `replay_content_sha256` and identical `replay_binding_id`.

No StarCraft II execution is required for this example.

---

## See also

- `docs/runtime/run_identity_lineage_seed.md` — M03 run identity and lineage seed contract
- `docs/runtime/match_execution_harness.md` — M02 proof artifact and hashing
- `docs/starlab.md` — public ledger (proved vs not yet proved)
