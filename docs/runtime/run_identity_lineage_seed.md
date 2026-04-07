# Run identity and lineage seed (M03)

This document defines the **M03** contract: deterministic **run spec identity**, **execution identity**, and **lineage seed** records built on top of the **M02** execution proof surface.

**These records are not the canonical run artifact (M05).** They are **seed** artifacts that STARLAB can emit without replay binding (M04) or full run packaging.

---

## What M03 proves

- STARLAB can assign **three distinct deterministic identities** to a completed execution proof plus its match configuration:
  - **run spec ID** — identity of the *intended* run shape (config + runtime boundary label, path-stable).
  - **execution ID** — identity of the *realized* execution proof (derived from the STARLAB `artifact_hash`, not from timestamps or filenames).
  - **lineage seed ID** — identity of the STARLAB-owned **linkage record** tying run spec to execution (hashed normalized seed payload).
- STARLAB can serialize **`run_identity.json`** and **`lineage_seed.json`** deterministically (stable key order, stable hashing rules).
- The derivation path is **CI-safe**: it operates on JSON artifacts and does not require StarCraft II execution.

---

## What M03 does not prove

- **Replay binding** (attaching or cryptographically binding replay bytes to run identity) — **M04**.
- **Canonical run artifact v0** (full governed run package) — **M05**.
- **Cross-host reproducibility** of execution or hashes — still not claimed; M02’s harness claim remains **narrow** (see `docs/starlab.md` §10).
- **Environment completeness**: the optional **environment fingerprint** is a **hint**, not a portability lock.

---

## Definitions

### Run spec ID

**Meaning:** Deterministic identity of the **intended** run configuration under a named **runtime boundary** (for example the M01 control/observation surface label).

**Source inputs:**

- Normalized **match config** (see *Normalization*): adapter, seed, bounded horizon, interface flags, **path-stable** map selection, replay-save intent, replay filename **basename** only (if present).
- **`runtime_boundary_label`**: STARLAB boundary name (for example from the proof’s `runtime_boundary_name` when deriving from a proof/config pair).

**Hashing:** SHA-256 over canonical JSON (UTF-8) of:

```json
{
  "kind": "starlab.run_spec.v1",
  "match_config": { ... normalized ... },
  "runtime_boundary_label": "<string>"
}
```

**Output:** 64 lowercase hex characters (same format as other STARLAB content hashes in this doc).

---

### Execution ID

**Meaning:** Deterministic identity of the **realized** execution proof — distinct from raw file bytes and distinct from **run spec ID**.

**Source inputs:**

- The M02 **`artifact_hash`** field: SHA-256 over the STARLAB-normalized proof payload **excluding** the `artifact_hash` field itself (see `docs/runtime/match_execution_harness.md` and `starlab.sc2.artifacts`).

**Hashing:** SHA-256 over canonical JSON of:

```json
{
  "kind": "starlab.execution.v1",
  "artifact_hash": "<M02 artifact_hash hex>"
}
```

**Rationale:** `execution_id` is **not** an alias of `artifact_hash`; it is a separate STARLAB identity in a dedicated namespace so audits can treat “execution” as a first-class object in later milestones.

---

### Lineage seed ID

**Meaning:** Deterministic identity of the **lineage seed record** that links run spec to execution for a single proof/config pair.

**Source inputs (hashed payload):**

- `run_spec_id`
- `execution_id`
- `config_hash` (SHA-256 over normalized match config body; see *Normalization*)
- `proof_artifact_hash` (the M02 `artifact_hash` value carried for explicit linkage)

**Hashing:** SHA-256 over canonical JSON of:

```json
{
  "kind": "starlab.lineage_seed.v1",
  "config_hash": "<hex>",
  "execution_id": "<hex>",
  "proof_artifact_hash": "<hex>",
  "run_spec_id": "<hex>"
}
```

**Note:** Optional **input** and **artifact** references in `lineage_seed.json` (file paths, optional content digests) are **not** part of this hash unless explicitly added in a later milestone. M03 keeps the hashed lineage payload **small and stable**.

---

## Normalization rules (match config)

Goal: **no absolute user-specific paths** enter hashed identity inputs.

- **Map selection**
  - `discover_under_maps_dir: true` → stable mode token only (no host paths).
  - `path: "<path>"` → record **`basename`** only (e.g. `MyMap.SC2Map`), not the full path.
  - `battle_net_map_name` → record the string as the logical name.
- **Replay filename** (if present) → **basename** only.
- **Field order** in canonical JSON: sorted keys at every object level (`sort_keys=True`).

---

## Normalization rules (execution proof)

For **execution ID**, M03 relies on the **existing M02** hash pipeline:

- Parse JSON to `ExecutionProofRecord`.
- Compute or verify `artifact_hash` via `compute_artifact_hash` / `proof_record_to_hash_input_dict`.

Do **not** hash raw JSON bytes for `execution_id` — STARLAB-owned normalized content only.

---

## Environment fingerprint (optional)

**Purpose:** Capture **what is known** from M01/M02 (probe, harness) without claiming a full lock.

**Model (conceptual):**

| Field | Required | Notes |
| ----- | -------- | ----- |
| `runtime_boundary_label` | yes | Same notion as run spec / proof |
| `adapter_name` | yes | e.g. `fake`, `burnysc2` |
| `base_build` | no | May be unknown (`null`) |
| `data_version` | no | May be unknown (`null`) |
| `platform_string` | no | Only if explicitly supplied (e.g. for local notes) |
| `probe_digest` | no | Optional normalized digest string if provided |

**Posture:**

- Helpful for **lineage** and human review.
- **Not** a portability guarantee between machines.
- **Not** a replacement for `docs/runtime/environment_lock.md`.

---

## Emitted artifacts (M03)

### `run_identity.json` (minimum)

- `schema_version` — e.g. `starlab.run_identity.v1`
- `run_spec_id`, `execution_id`
- `proof_artifact_hash`, `config_hash`
- `adapter_name`, `runtime_boundary_label`, `seed`
- `normalized_map_reference` — logical map key from the proof (e.g. `map_logical_key`)
- `interface_summary` — interface flags from the proof
- `bounded_horizon` — `step_policy` from the proof (or config horizon; they should agree for valid runs)
- `environment_fingerprint` — optional object

### `lineage_seed.json` (minimum)

- `schema_version` — e.g. `starlab.lineage_seed.v1`
- `lineage_seed_id`, `run_spec_id`, `execution_id`
- `config_hash`, `proof_artifact_hash`
- `input_references` — logical labels + optional `content_sha256` for inputs
- `artifact_references` — e.g. emitted filenames (not hashed into `lineage_seed_id` in M03)
- `parent_references` — typically `[]` in M03
- `later_milestones` — short text: M04 replay binding, M05 canonical artifact (placeholders only)

---

## Relationship to M02 proof artifacts

- **Input:** `match_execution_proof.json` (schema `match_execution_proof.v1`) and the matching **match config** JSON (`schema_version: "1"`).
- **Proof hash:** M02 `artifact_hash` is the bridge between the harness output and **execution ID**.
- **Adapter alignment:** For a coherent run identity line, `MatchConfig.adapter` should match `ExecutionProofRecord.adapter_name`. The CLI validates this.

---

## Relationship to later milestones

| Milestone | What it adds relative to M03 |
| --------- | ------------------------------ |
| **M04 — Replay binding** | Binds replay file identity (and optionally replay hash) to **run identity** / lineage; may extend `lineage_seed` or successor records. |
| **M05 — Canonical run artifact v0** | First **canonical** packaged run artifact boundary; M03 seeds remain non-canonical inputs, not replacements. |

---

## Worked example (M02-shaped, fake adapter)

**Config (excerpt):** `adapter: "fake"`, `seed: 4242`, `max_game_steps: 10`, map mode `discover_under_maps_dir`.

**Proof (excerpt):** `runtime_boundary_name: "s2client_proto_sc2api"`, `map_logical_key: "fake://deterministic"`, `artifact_hash` set per M02 rules.

**Derived identities:**

1. Compute **`config_hash`** from normalized match config (path-stable map mode, sorted keys).
2. Compute **`run_spec_id`** from `{ kind: starlab.run_spec.v1, match_config: …, runtime_boundary_label: "s2client_proto_sc2api" }`.
3. Take **`artifact_hash`** from the proof → compute **`execution_id`** from `{ kind: starlab.execution.v1, artifact_hash: "<hex>" }`.
4. Compute **`lineage_seed_id`** from `{ kind: starlab.lineage_seed.v1, run_spec_id, execution_id, config_hash, proof_artifact_hash }`.

**CLI (reference):**

```bash
python -m starlab.runs.seed_from_proof \
  --proof tests/fixtures/m02_match_execution_proof.json \
  --config tests/fixtures/m02_match_config.json \
  --output-dir /tmp/m03_out
```

No StarCraft II execution is required for this example.

---

## See also

- `docs/runtime/match_execution_harness.md` — M02 proof artifact and hashing
- `docs/runtime/environment_lock.md` — environment lock (separate from M03 fingerprint)
- `docs/starlab.md` — public ledger (proved vs not yet proved)
