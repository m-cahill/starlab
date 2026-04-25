# V15-M04 — XAI Evidence Contract v1 (runtime narrative)

**Contract id:** `starlab.v15.xai_evidence_pack.v1`  
**Milestone:** `V15-M04` — *XAI Evidence Contract v1*  
**Emitter:** `python -m starlab.v15.emit_v15_xai_evidence_pack --output-dir <path>`

---

## Purpose

V15-M04 establishes the **XAI Evidence Contract v1** for STARLAB v1.5: exact logical artifact names, row-level fields, status vocabulary, identity bindings, and explicit **non-claims** for any future replay-native explanation pack.

**V15-M04 freezes the XAI evidence contract and emits fixture evidence packs. It does not execute XAI inference and does not prove explanation faithfulness.**

A **fixture** XAI evidence pack is **schema / wiring evidence only**, not an explanation of a trained STARLAB agent.

An XAI evidence pack is **not** proof that explanations are causal or faithful unless the explanation faithfulness status says so under a **declared validation path** outside this contract.

---

## Relationship to prior V15 milestones

| Milestone | Relationship to M04 |
| --- | --- |
| **V15-M00** (gates **A–G**) | M04 supports **Gate F — XAI** by freezing contract names, fixture emission, and vocabulary. M00 **does not** satisfy Gate F until later operator/real evidence milestones. |
| **V15-M01** (asset registers) | `docs/xai_evidence_register.md` remains **template-first**; M04 defines the **contract** for future real rows — **no** public register rows for real packs in M04. |
| **V15-M02** (environment lock) | Optional `--environment-lock-json` binds an M02 JSON file by **canonical SHA-256** only (no SC2 execution, no paths in public output). |
| **V15-M03** (checkpoint lineage) | Optional `--checkpoint-lineage-json` binds an M03 lineage manifest file by **canonical SHA-256** only (no checkpoint blob reads). |

---

## Emitted files (M04)

M04 emits **two** JSON files only (compact bundle):

| File | Role |
| --- | --- |
| `v15_xai_evidence_pack.json` | Governed pack: identities, traces, summaries, vocabularies, `required_artifact_names`, `check_results`, non-claims. |
| `v15_xai_evidence_pack_report.json` | Report: counts, seal, contract id, `xai_evidence_pack_sha256`. |

**Logical artifact names** (e.g. `decision_trace.json`, `xai_manifest.json`) are listed under `required_artifact_names` inside the pack — they are **not** materialized as separate files in M04. Real multi-file bundles are reserved for **V15-M10** (or later operator workflows).

---

## CLI

```bash
python -m starlab.v15.emit_v15_xai_evidence_pack --output-dir <dir>
```

**Default profile:** `fixture_ci` — deterministic, CI-safe, no GPU, no inference, no replay or checkpoint file reads.

**Optional:**

| Argument | Purpose |
| --- | --- |
| `--profile fixture_ci` | Default. Ignores `--evidence-json` and optional binding paths. |
| `--profile operator_declared` | Requires `--evidence-json` (metadata-only). |
| `--evidence-json <path>` | Operator metadata; unknown top-level keys rejected. |
| `--checkpoint-lineage-json <path>` | Optional; sets `checkpoint_lineage_manifest_sha256` from file canonical hash. |
| `--environment-lock-json <path>` | Optional; binds M02 environment lock canonical hash into logical `checkpoint_reference` / `notes` (no raw path commit). |

Strings that look like absolute paths are redacted in emitted JSON to `<REDACTED_ABSOLUTE_PATH>`.

---

## Contract fields (summary)

The pack includes at minimum: `contract_id`, `milestone_id`, `generated_by`, `profile`, `xai_evidence_status`, `long_gpu_run_authorized`, `real_xai_inference_executed`, `replay_bound`, `checkpoint_bound`, `checkpoint_bytes_verified`, `explanation_faithfulness_validated`, `evidence_scope`, `xai_pack_identity`, `replay_identity`, `checkpoint_identity`, `decision_trace`, `critical_decision_index`, `attribution_summary`, `concept_activation_summary`, `counterfactual_probe_results`, `alternative_action_rankings`, `uncertainty_report`, `replay_overlay_manifest`, `xai_explanation_report`, `required_artifact_names`, `status_vocabulary`, `scene_type_vocabulary`, `method_vocabulary`, `path_disclosure_vocabulary`, `required_fields`, `check_results`, `non_claims`, `carry_forward_items`, and seal `xai_evidence_pack_sha256`.

Fixture profile sets: `xai_evidence_status: fixture_only`, `real_xai_inference_executed: false`, `replay_bound: false`, `checkpoint_bound: false`, `checkpoint_bytes_verified: false`, `explanation_faithfulness_validated: false`, `long_gpu_run_authorized: false`.

`real_xai_inference_executed` and `explanation_faithfulness_validated` are **not** set to true unless explicitly passed in operator evidence JSON (external declaration). `long_gpu_run_authorized` is **always false** in M04.

---

## Public / private posture

- **Public-safe:** contract id, seal, vocabulary, logical references, fixture rows, attestation text.
- **Private / redacted by default:** absolute filesystem paths; operator notes that leak paths. Use `path_disclosure` vocabulary in rows when describing overlays and reports.

---

## Review / coverage vocabulary (non-claim)

- **Saliency, attribution, concepts, counterfactuals** in a fixture or declared-only pack are **evidence of schema**, not **causal** explanations of a trained policy.
- **Counterfactual rows** are **not** the result of running counterfactual evaluation in M04.
- **Overlay** and **explanation report** metadata rows do **not** imply media was rendered in CI.

---

## Claim discipline (M04)

V15-M04 defines and emits the XAI evidence contract and fixture evidence-pack surface. It may validate fixture metadata and may normalize supplied operator-declared XAI metadata, but it does not execute model inference, does not generate real attribution or saliency maps, does not run counterfactual evaluation, does not parse real replays, does not verify checkpoint bytes, does not prove explanation faithfulness, does not run benchmarks, does not run human evaluation, does not execute GPU training or shakedown, does not authorize a long GPU run, does not approve real XAI assets for claim-critical use, does not open v2, and does not open PX2-M04/PX2-M05.

---

## Next milestones

- **V15-M05+:** Strong-agent benchmark protocol and later gates — not opened by M04.
- **V15-M10:** Replay-native XAI *demonstration* (real packs, where protocol allows) — separate from M04 contract-only scope.

---

## Closure note (governance)

**V15-M04** is **closed** on `main` ([PR #123](https://github.com/m-cahill/starlab/pull/123); merge `3bf4e2ca5343b116e4e979d5dc50213596b7519b`); **authoritative PR-head CI** [`24922143448`](https://github.com/m-cahill/starlab/actions/runs/24922143448); **merge-boundary `main` CI** [`24922278255`](https://github.com/m-cahill/starlab/actions/runs/24922278255). Closure records **contract + fixture emission + CI evidence** only. It does **not** assert that real model inference was executed, that explanation faithfulness was validated, or that real XAI assets were approved for claim-critical use. `long_gpu_run_authorized` remains **false** in this contract.
