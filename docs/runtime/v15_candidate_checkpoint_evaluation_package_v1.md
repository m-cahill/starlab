# V15-M19 — Candidate checkpoint evaluation **package** assembly (runtime)

**Milestone:** `V15-M19`  
**Status:** **active** in this repository (see `docs/starlab-v1.5.md` for authoritative program record)  
**Contract:** `starlab.v15.candidate_checkpoint_evaluation_package.v1`

## Role

**M18** is the **readiness / refusal** gate. **M19** is the **evaluation package assembly** gate. M19 **does not** run benchmarks, **does not** load checkpoints, and **does not** measure strength. It assembles, binds, and **cross-checks** governed JSON inputs so a **future** milestone may run **checkpoint-scoped** evaluation when operators supply real artifacts.

- **`evaluation_package_ready`** in the M19 artifact means **`ready_for_future_checkpoint_evaluation` only**. It is **not** a benchmark pass, promotion, or “strong agent” claim.
- The public record keeps these **false** on honest paths: **`strength_evaluated`**, **`checkpoint_promoted`**, **`benchmark_passed`**, **`xai_claim_authorized`**, **`human_benchmark_claim_authorized`**, **`showcase_release_authorized`**, **`v2_authorized`**.
- M19 **must not** hash raw checkpoint **blobs**; it compares **declared** SHA-256 values across **JSON** artifacts (candidate manifest, M03 lineage row, M08 receipt, M18 snapshot) and flags contradictions.
- The default **evaluation protocol** source is the **M05** strong-agent scorecard JSON (`v15_strong_agent_scorecard.json`: **`starlab.v15.strong_agent_scorecard.v1`**, **`protocol_profile_id`** **`starlab.v15.strong_agent_benchmark_protocol.v1`**). If the protocol contract cannot be reconciled, M19 reports a **blocker**; it does **not** introduce a new protocol family here.

## Dependency on M18 and upstream artifacts

- **`--m18-readiness-json`** must use **`contract_id`:** **`starlab.v15.checkpoint_evaluation_readiness.v1`**. A wrong `contract_id` yields **`blocked_invalid_candidate_package`** (reason `invalid_m18_readiness_contract_id`).
- M19 copies a **compact** M18 summary into the report **and** records the full M18 file digest — M19 is readable as a **standalone** package summary, not as SHA-only.
- M19 **independently** validates that checkpoint-related hashes are **mutually consistent** between manifest, M03, M08, and M18; it does **not** trust M18 alone for that consistency check.

## Emitter

**Fixture (CI-safe, no inputs):**

```bash
python -m starlab.v15.emit_v15_candidate_checkpoint_evaluation_package \
  --output-dir out/v15_m19_candidate_checkpoint_evaluation_package
```

**Operator preflight (explicit file paths, bind and validate):**

```bash
python -m starlab.v15.emit_v15_candidate_checkpoint_evaluation_package \
  --output-dir out/v15_m19_candidate_checkpoint_evaluation_package \
  --profile operator_preflight \
  --m18-readiness-json path/to/v15_checkpoint_evaluation_readiness.json \
  --candidate-manifest path/to/candidate_checkpoint_manifest.json \
  --campaign-receipt path/to/v15_long_gpu_campaign_receipt.json \
  --checkpoint-lineage path/to/v15_checkpoint_lineage_manifest.json \
  --environment-manifest path/to/v15_long_gpu_environment_lock.json \
  --dataset-manifest path/to/dataset_manifest.json \
  --evaluation-protocol-json path/to/v15_strong_agent_scorecard.json
```

**Operator declared (package JSON in, metadata-only, path redaction):**

```bash
python -m starlab.v15.emit_v15_candidate_checkpoint_evaluation_package \
  --output-dir out/v15_m19_candidate_checkpoint_evaluation_package \
  --profile operator_declared \
  --package-json path/to/v15_candidate_checkpoint_evaluation_package.json
```

`operator_declared` performs **no** training, **no** evaluation, and **no** checkpoint **blob** I/O.

## Emitted files

- `v15_candidate_checkpoint_evaluation_package.json` (sealed; includes non-claim flags and package status)
- `v15_candidate_checkpoint_evaluation_package_report.json` (M18 summary, SHA bindings, **`recommended_m20_fork`**, inventory)
- `v15_candidate_checkpoint_evaluation_package_checklist.md` (gates **P0–P9** with checkboxes)

## Checklist gates (P0–P9)

| Gate | Theme |
| --- | --- |
| **P0** | M18 readiness binding (contract, compact summary, full-file SHA) |
| **P1** | Candidate manifest present and contract-valid |
| **P2** | Completed M08 campaign receipt present |
| **P3** | Checkpoint lineage binding (M03) |
| **P4** | Environment (M02) binding |
| **P5** | Dataset manifest binding |
| **P6** | Evaluation protocol (M05 strong-agent scorecard) binding |
| **P7** | Cross-artifact SHA consistency (no blob hashing) |
| **P8** | Non-claim / public–private boundary |
| **P9** | M20 fork recommendation (deterministic mapping from `package_status`) |

## Status vocabulary (compact)

- **`blocked_missing_candidate_checkpoint_evidence`** — default **fixture** or missing/invalid campaign completion path.
- **`blocked_incomplete_evaluation_package_inputs`** — partial inputs (e.g. M18 not fully supplied upstream).
- **`blocked_invalid_candidate_package`** — contract mismatch, joblib-only candidate, **SHA** cross-check failure, or invalid M18 contract.
- **`evaluation_package_ready`** — inputs assemble consistently; still **ready_for_future_checkpoint_evaluation** only; **not** a benchmark result.

**XAI and human** execution tracks: if M19 is **blocked** for missing or inconsistent evidence, do **not** treat that as permission to start **M20** showpiece XAI or human work until **`recommended_m20_fork`** and upstream gates say otherwise.

## See also

- `docs/runtime/v15_checkpoint_evaluation_readiness_v1.md` (M18)  
- `docs/runtime/v15_strong_agent_benchmark_protocol_v1.md` (M05)  
- `docs/starlab-v1.5.md` — **M19 non-claims** and milestone table
