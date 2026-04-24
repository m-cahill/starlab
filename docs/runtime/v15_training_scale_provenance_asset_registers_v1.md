# STARLAB v1.5 — Training-scale provenance and asset registers (runtime)

**Contract id:** `starlab.v15.training_asset_registers.v1`  
**Milestone:** `V15-M01`  
**Emission:** `python -m starlab.v15.emit_v15_training_asset_registers --output-dir <dir>`

---

## Purpose

This milestone defines the **training-scale provenance and public register surface** needed before STARLAB treats long GPU training, evaluation, XAI, or human-benchmark work as claim-ready. **V15-M01** establishes **schemas, vocabulary, and sparse public register documents** — not approval of any particular asset for claim-critical use.

---

## Relationship to V15-M00

**V15-M00** (`starlab.v15.training_readiness_charter.v1`) freezes goals, non-claims, artifact family names, and **long GPU run gates A–G**. **V15-M01** implements the **register layer and contract** that later milestones use to populate manifests and receipts. Satisfying gates A–G remains **future work**; M01 does **not** green-light a long run.

---

## Asset classes

| Class | Intent |
| --- | --- |
| `code` | Repository and tooling under license / governance |
| `replay_corpus` | Collections of replays used for training or eval |
| `training_dataset` | Derived datasets (features, shards, indices) |
| `label_set` | Labels or supervision derived from replays or human input |
| `model_weight` | Trained parameters / exported weights |
| `checkpoint` | Training checkpoints (may include optimizer state) |
| `benchmark_asset` | Fixtures, ladders, opponent pools, scorecard inputs |
| `xai_evidence` | Explanation packs, traces, reports |
| `human_panel_record` | Human benchmark games, aliases, outcomes |
| `video_or_media` | Demos, captures — rights-sensitive |
| `map_pool` | Map identity and provenance for runs |
| `environment_reference` | SC2 build, CUDA, PyTorch, GPU, dependency identity |

---

## Public vs private rules

- **Public:** Register **structure**, vocabulary, non-claims, and **empty** or template tables until assets are deliberately registered with cleared posture.
- **Private / local default:** Raw weights, large checkpoints, bulk replays, videos, human identities, and uncleared paths stay **out of the public repo**.
- **Sanitized public reference:** Content hashes, contract ids, milestone ids, and pointers to governing docs when rights allow.
- **Forbidden public:** Secrets, uncleared third-party bulk redistribution, and identifiable human-panel data without explicit authorization.

---

## Required fields (every asset row)

Each row in an operator or future machine-readable register should capture at least:

`asset_id`, `asset_class`, `asset_name`, `register_id`, `source_kind`, `owner_or_steward`, `storage_posture`, `public_private_posture`, `rights_posture`, `redistribution_posture`, `hash_policy`, `sha256_or_hash_reference`, `claim_use`, `review_status`, `governing_doc`, `notes`, `non_claims`

Exact vocabulary values are emitted in `v15_training_asset_registers.json`.

---

## Status vocabulary

Row **review** status uses `status_vocabulary` in the JSON contract (e.g. `not_reviewed`, `quarantined`, `accepted_public_reference`). This is **governance state**, not training job status.

---

## Allowed claim-use vocabulary

`claim_use` declares the strongest **intended** use for a row. **M01** public docs default to **no claim-critical rows**. Values include `none`, `readiness_only`, `fixture_only`, through `claim_critical` — see emitted JSON.

---

## Hashing and reference policy

- Prefer **SHA-256** of canonical serialized metadata or of blob content when bytes exist.
- When bytes are not in-repo, record a **declared reference** (e.g. external archive id) and keep detailed paths private.
- Contract JSON self-seal: `training_asset_registers_sha256` covers the body **excluding** the seal field (`starlab.runs.json_util`).

---

## Non-claims (M01)

**V15-M01** establishes training-scale provenance and asset-register surfaces. It does not approve any particular replay corpus, dataset, label set, model weight, checkpoint, human-panel record, XAI pack, or media artifact for claim-critical use. It does not execute GPU training, lock the long-run environment, implement checkpoint resume, run benchmarks, produce XAI inference artifacts, run human evaluation, open v2, or open PX2-M04/PX2-M05.

---

## CLI

```bash
python -m starlab.v15.emit_v15_training_asset_registers --output-dir <dir>
```

Writes `v15_training_asset_registers.json` and `v15_training_asset_registers_report.json`.
