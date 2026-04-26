# V15-M12 — Showcase Agent Release Pack (runtime contract v1)

**Milestone:** `V15-M12`  
**Contract:** `starlab.v15.showcase_agent_release_pack.v1`  
**Optional operator evidence bundle:** `starlab.v15.showcase_operator_release_evidence_declared.v1`  
**Status:** Governance / packaging surface — **not** a showcase-agent product release on the default path.

## 1. Purpose

V15-M12 answers whether STARLAB can **package** the evidence required for a future **showcase-agent release decision** into a **single, deterministic, CI-safe release-pack artifact** with explicit gates, SHA bindings, and non-claims.

**Default honest answer:** the **release-pack surface exists**, but **release remains blocked** because required **real operator evidence** (completed long GPU campaign, promoted checkpoint, executed strong-agent benchmark, real XAI demonstration, authorized human-benchmark claim, rights clearance, etc.) is **not** present on the **fixture / default public path**.

## 2. Relationship to upstream milestones

| Upstream | Role in M12 |
| --- | --- |
| **M08** — long GPU campaign receipt (`starlab.v15.long_gpu_campaign_receipt.v1`) | **R1** — campaign receipt binding; M12 does **not** execute the campaign. |
| **M09** — checkpoint promotion decision (`starlab.v15.checkpoint_promotion_decision.v1`) | **R2** — checkpoint promotion binding; M12 does **not** promote a checkpoint. |
| **M10** — replay-native XAI demonstration (`starlab.v15.replay_native_xai_demonstration.v1`) | **R5** — XAI demonstration binding; M12 does **not** run XAI inference. |
| **M11** — human-benchmark claim decision (`starlab.v15.human_benchmark_claim_decision.v1`) | **R6** — human-benchmark claim binding; M12 does **not** run human-panel matches. |
| **M05** — strong-agent scorecard (`starlab.v15.strong_agent_scorecard.v1`) | **R4** — strong-agent scorecard binding; M12 does **not** run benchmarks or live SC2. |
| **M03** — checkpoint lineage manifest (`starlab.v15.checkpoint_lineage_manifest.v1`) | **R3** — checkpoint lineage binding; M12 does **not** read checkpoint blobs. |

## 3. Release-pack inputs (operator modes)

**operator_preflight** and **operator_declared** require JSON file paths for:

- `v15_long_gpu_campaign_receipt.json` (M08)  
- `v15_checkpoint_promotion_decision.json` (M09)  
- `v15_replay_native_xai_demonstration.json` (M10)  
- `v15_human_benchmark_claim_decision.json` (M11)  
- `v15_strong_agent_scorecard.json` (M05)  
- `v15_checkpoint_lineage_manifest.json` (M03)  

**operator_declared** additionally requires **`starlab.v15.showcase_operator_release_evidence_declared.v1`** JSON (`--release-evidence-json`) with allowed keys:

- `contract_id`, `evidence_bundle_id` (required), `operator_public_notes` (optional), `rights_clearance_operator_declared` (optional bool).

M12 **binds** each file by **canonical JSON SHA-256** only. It **never** inspects checkpoint weight blobs, **never** parses replay binaries, **never** runs live SC2, **never** performs XAI inference, and **never** executes human-panel logic.

## 4. Default posture (fixture / honest path)

Expected defaults:

- `showcase_release_status`: `fixture_contract_only` with secondary blockers including `blocked_missing_promoted_checkpoint`  
- `showcase_agent_release_authorized`: **false**  
- `public_showcase_claim_authorized`: **false**  
- `strong_agent_claim_authorized`: **false**  
- `human_benchmark_claim_authorized`: **false**  
- `ladder_claim_authorized`: **false**  
- `v2_authorized`: **false**  

## 5. Release gates (R0–R14)

| Gate ID | Intent |
| --- | --- |
| `R0_artifact_integrity` | Schema / contract integrity |
| `R1_campaign_receipt_binding` | M08 receipt posture |
| `R2_checkpoint_promotion_binding` | M09 promotion posture |
| `R3_checkpoint_lineage_binding` | M03 lineage bound |
| `R4_strong_agent_scorecard_binding` | M05 benchmark / claim posture |
| `R5_xai_demonstration_binding` | M10 demonstration posture |
| `R6_human_benchmark_claim_binding` | M11 claim authorization |
| `R7_rights_and_register_posture` | Rights / register clearance |
| `R8_public_private_boundary` | Redaction / public-safe emission |
| `R9_release_manifest_completeness` | Release manifest completeness |
| `R10_claim_text_boundary` | Claim vs non-claim language |
| `R11_reproducibility_and_sha_bindings` | SHA reproducibility |
| `R12_raw_asset_exclusion` | No raw weights / replays / paths in pack |
| `R13_operator_notes_redaction` | Operator notes redacted |
| `R14_v2_boundary` | v2 deferred to **V15-M13** |

Gate **status** vocabulary: `pass`, `warning`, `fail`, `blocked`, `not_evaluated`, `not_applicable`.

## 6. Required non-claim language (M12)

V15-M12 does not train a checkpoint; does not promote a checkpoint; does not execute a long GPU campaign; does not run strong-agent benchmarks; does not run live SC2; does not run XAI inference; does not run human-panel matches; does not authorize showcase-agent, strong-agent, human-benchmark, ladder, or v2 claims on the default path; and does not commit model weights, checkpoint blobs, raw replays, videos, saliency tensors, participant records, private operator notes, or private paths.

## 7. Public / private boundary

**May appear** in public pack / brief: contract IDs, SHA-256 bindings, logical candidate IDs, release status, gate statuses, sanitized operator summaries, non-claims, public-safe claim text.

**Must not appear**: raw weights, checkpoint blobs, raw replays, replay paths, match videos, saliency tensors, participant identities, private notes, absolute paths, credential-like strings, contact information.

## 8. CLI

Default fixture:

```bash
python -m starlab.v15.emit_v15_showcase_agent_release_pack --output-dir out/v15_m12_showcase_release
```

Operator preflight:

```bash
python -m starlab.v15.emit_v15_showcase_agent_release_pack \
  --profile operator_preflight \
  --m08-campaign-receipt-json <path> \
  --m09-promotion-decision-json <path> \
  --m10-xai-demonstration-json <path> \
  --m11-human-benchmark-claim-decision-json <path> \
  --m05-scorecard-json <path> \
  --m03-checkpoint-lineage-json <path> \
  --output-dir <dir>
```

Operator declared:

```bash
python -m starlab.v15.emit_v15_showcase_agent_release_pack \
  --profile operator_declared \
  --release-evidence-json <path> \
  --m08-campaign-receipt-json <path> \
  --m09-promotion-decision-json <path> \
  --m10-xai-demonstration-json <path> \
  --m11-human-benchmark-claim-decision-json <path> \
  --m05-scorecard-json <path> \
  --m03-checkpoint-lineage-json <path> \
  --output-dir <dir>
```

## 9. Emitted files

- `v15_showcase_agent_release_pack.json`  
- `v15_showcase_agent_release_pack_report.json`  
- `v15_showcase_agent_release_brief.md`  

## 10. Downstream: V15-M13

**V15-M13 — v2 Go / No-Go Decision** consumes **governed evidence** and explicit program posture; **M12 does not** authorize **v2**. **`R14_v2_boundary`** records that separation.
