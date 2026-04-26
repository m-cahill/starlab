# V15-M15 — Operator evidence collection preflight (contract v1)

**Milestone:** `V15-M15`  
**Status:** **opened** / **implementation** on `main` (merge / CI to be recorded at **closeout**).  
**Contract:** `starlab.v15.operator_evidence_collection_preflight.v1`  
**Authority:** `docs/starlab-v1.5.md` (M15 non-claims, milestone table, artifact family)

## Purpose

V15-M15 answers:

> Before collecting operator-local evidence, what inputs, private path conventions, prerequisite artifact classes, register checks, redaction rules, and go/no-go *preflight* gates must be satisfied?

This milestone is **preflight and sequencing** only. It **does not** collect operator evidence, **does not** run GPU or SC2 workloads, and **does not** authorize v2.

## Dependencies

- **M13 (no-go / defer):** Default public record remains **v2 not authorized**; M13 provides `starlab.v15.v2_go_no_go_decision.v1` for optional SHA binding. The preflight artifact preserves `v2_authorized: false` and `v2_recharter_authorized: false` on fixture and honest default paths. Optional CLI input: `--m13-v2-decision-json` (must be contract-valid; `v2_authorized` must not be `true` for M15 defaults).
- **M14 (remediation plan):** M14 closeout `remediation_plan_ready`, `operator_evidence_not_collected`, and gap/gate inventory are the **planning** dependency. Optional binding: `--m14-remediation-plan-json` (must list all **10** gap IDs, **E0–E13** remediation gates, and retain **operator evidence not collected** posture).

## Emitter

```bash
python -m starlab.v15.emit_v15_operator_evidence_collection_preflight \
  --output-dir out/v15_m15_operator_evidence_preflight
```

Optional bindings (SHA-only; no blob reads):

```bash
python -m starlab.v15.emit_v15_operator_evidence_collection_preflight \
  --output-dir out/v15_m15_operator_evidence_preflight \
  --m13-v2-decision-json path/to/v15_v2_go_no_go_decision.json \
  --m14-remediation-plan-json path/to/v15_evidence_remediation_plan.json
```

Default path is **CI-safe**: no operator files required. Emitted JSON uses placeholder SHA-256 for missing optional inputs.

## Emitted files

| File | Role |
| --- | --- |
| `v15_operator_evidence_collection_preflight.json` | Sealed preflight contract (`artifact_sha256`) |
| `v15_operator_evidence_collection_preflight_report.json` | Report (seal check, filenames) |
| `v15_operator_evidence_collection_checklist.md` | Deterministic operator checklist (Markdown) |

## Expected input binding semantics

- **M13 file:** `contract_id` must be `starlab.v15.v2_go_no_go_decision.v1`. Canonical JSON SHA-256 is stored in `m13_binding`. If `authorization_flags.v2_authorized` is `true`, emit **fails** (inconsistent with M15 honest defaults).
- **M14 file:** `contract_id` must be `starlab.v15.evidence_remediation_plan.v1`. All **10** gap IDs and **E0–E13** gate IDs must be present. `remediation_status_secondary` must include `operator_evidence_not_collected`. `authorization_flags.v2_authorized` must not be `true` when present.

## Preflight gate table (P0–P14)

Definition-only gates (not “evidence success” gates). Default statuses are `pass` / `pass_or_fixture` for fixture/definition posture.

| ID | Name (summary) |
| --- | --- |
| P0 | M13 no-go / defer context bound or fixture placeholder used |
| P1 | M14 remediation plan bound or fixture placeholder used |
| P2 | Operator-private workspace convention declared |
| P3 | Private path commit prohibition recorded |
| P4 | Required input classes inventoried |
| P5 | Rights / register touchpoints declared |
| P6 | M16 environment/short-GPU preflight defined |
| P7 | M17 long-GPU preflight defined |
| P8 | M18 checkpoint/eval preflight defined |
| P9 | M19 XAI preflight defined |
| P10 | M20 human-panel preflight defined |
| P11 | Showcase release input expectations preserved |
| P12 | v2 reconsideration remains blocked until evidence |
| P13 | No operator execution in M15 |
| P14 | Docs and governance tests aligned |

## Evidence sequence (S0–S10)

Deterministic **sequencing** rows (each includes `default_status` and `non_claims` — not “evidence collected”):

- S0_m13_m14_context_binding  
- S1_private_workspace_preflight  
- S2_environment_and_short_gpu_inputs  
- S3_training_asset_and_rights_inputs  
- S4_long_gpu_campaign_inputs  
- S5_checkpoint_lineage_and_resume_inputs  
- S6_evaluation_and_promotion_inputs  
- S7_xai_pack_inputs  
- S8_human_panel_inputs  
- S9_showcase_release_inputs  
- S10_v2_reconsideration_inputs  

## Future milestone map (V15-M16–V15-M21)

**Sequencing targets** only; not completed evidence:

| Milestone | Purpose | M15 posture (summary) |
| --- | --- | --- |
| V15-M16 | Short GPU / environment evidence | Blocked until M15 preflight gates pass |
| V15-M17 | Long GPU campaign evidence | Blocked until M16 + required inputs pass |
| V15-M18 | Checkpoint / eval evidence | Blocked until long-run/checkpoint class inputs exist |
| V15-M19 | XAI evidence | Blocked until candidate/XAI preconditions |
| V15-M20 | Human / bounded human benchmark | Blocked until protocol, rights, participants |
| V15-M21 | v2 reconsideration | Blocked until M16–M20 or explicit defer |

## Public / private boundary

- **Public-safe:** contract IDs, SHA bindings, logical artifact names, milestone and gate ids, non-claims, redacted path conventions, register **names** (as doc paths).  
- **Private / local by default:** absolute paths, SC2 client paths, map packs, replays, weights, checkpoint blobs, saliency, videos, human identities, consent, session notes, local logs, raw `out/` campaign trees.

## Register touchpoints (docs paths)

- `docs/rights_register.md`  
- `docs/training_asset_register.md`  
- `docs/replay_corpus_register.md`  
- `docs/model_weight_register.md`  
- `docs/checkpoint_asset_register.md`  
- `docs/xai_evidence_register.md`  
- `docs/human_benchmark_register.md`  

M15 **does not** add claim-critical public register **rows**.

## Non-claims

- No operator evidence collection, no long/short GPU execution, no checkpoint promotion, no benchmark, XAI, human-panel, or showcase **execution** in M15.  
- No v2 and no v2 recharter authorization on default/fixture path.  
- V15-M16–M21 entries in the artifact are **labels**, not completed work.  
- See `docs/starlab-v1.5.md` M15 non-claims block for full text.

## Closeout expectations (on `main` after implementation PR)

Record PR, PR-head CI, merge commit, merge `main` CI, and set this doc’s top status to **closed**; **V15-M16** remains **proposed** until opened. Private summary/audit under `docs/company_secrets/milestones/post-v1/V15-M15/` (untracked) per project workflow. Intended prompt sources: `summaryprompt.md`, `unifiedmilestoneauditpromptV2.md` (if present locally).
