# STARLAB v1.5 — V15-M13 v2 Go / No-Go Decision (runtime v1)

**Milestone:** `V15-M13` (**closed** on `main`; implementation [PR #139](https://github.com/m-cahill/starlab/pull/139); **authoritative PR-head CI** [`24948284106`](https://github.com/m-cahill/starlab/actions/runs/24948284106); **merge-boundary `main` CI** [`24948356222`](https://github.com/m-cahill/starlab/actions/runs/24948356222) on merge `f0af5a62…`)  
**Contract:** `starlab.v15.v2_go_no_go_decision.v1`  
**Optional operator evidence contract:** `starlab.v15.v2_decision_operator_evidence_declared.v1`  
**Emitter:** `python -m starlab.v15.emit_v15_v2_go_no_go_decision`

**Public closeout posture (default / fixture path):** `fixture_decision_only` / `no_go_insufficient_evidence` / `blocked_missing_showcase_release_authorization`; **`v2_authorized`:** false; **`v2_recharter_authorized`:** false; **recommended next step:** `collect_operator_evidence_before_v2` / `v1_5_hardening`. **Not** v2 implementation.

## Purpose

V15-M13 is the **final planned V15 decision milestone**. It emits a deterministic, CI-safe **v2 go / no-go decision surface** that answers whether the governed V15 evidence package justifies opening a **v2 recharter**, **without** implementing v2.

- **Consumes:** primarily the **M12** showcase-agent release-pack JSON (`starlab.v15.showcase_agent_release_pack.v1`), bound by **canonical JSON SHA-256** of the supplied file.
- **Relates to moonshot pillars:** long GPU campaign, strong-agent benchmark, replay-native XAI, bounded human-benchmark claim, and evidence-based v2 decision — M13 **reads governance summaries** from M12; it does **not** execute training, benchmarks, XAI, or human-panel work.
- **Relates to M08–M12:** optional **SHA-only** cross-check of upstream JSON files when paths are supplied; each file must match the corresponding SHA recorded in M12 `upstream_bindings`.

## Default posture (fixture / honest public path)

The default path is **no-go / defer**:

- `v2_decision_status` includes **`fixture_decision_only`**, **`no_go_insufficient_evidence`**, and blockers such as **`blocked_missing_showcase_release_pack`** or **`blocked_missing_showcase_release_authorization`** when M12 does not authorize release.
- All **authorization flags** in the artifact default to **`false`** (including `v2_authorized`, `v2_recharter_authorized`, showcase and claim authorizations).
- **Recommended next step:** **`collect_operator_evidence_before_v2`** (or equivalent defer / v1.5 hardening language in docs).

## Operator-declared mode

**Profile:** `operator_declared` requires:

- `--m12-showcase-release-pack-json`
- `--decision-evidence-json` with `contract_id` **`starlab.v15.v2_decision_operator_evidence_declared.v1`**

Operator evidence is **metadata-only** (allowlisted keys). It must not carry raw paths, participant identities, replay paths, checkpoint paths, credentials, or private notes. Text fields are **redacted** on emit. Operator-declared fields may influence gate **posture** only when public-safe and SHA-bound; they **must not** authorize v2 unless M12 prerequisites and declared rights/scope gates also support authorization.

## Decision gates (D0–D14)

| Gate ID | Intent |
| --- | --- |
| `D0_artifact_integrity` | Parsed JSON, valid contracts, sealed artifact |
| `D1_m12_release_pack_binding` | M12 release pack bound by canonical SHA-256 |
| `D2_campaign_evidence_gate` | Long-campaign evidence (M08 summary via M12) |
| `D3_checkpoint_promotion_gate` | Promotion posture (M09 summary via M12) |
| `D4_strong_agent_benchmark_gate` | Strong-agent / M05 summary via M12 |
| `D5_xai_evidence_gate` | M10 demonstration posture via M12 |
| `D6_human_benchmark_gate` | M11 claim posture via M12 |
| `D7_rights_and_register_gate` | Rights / register / M12 authorization flags |
| `D8_public_private_boundary_gate` | No unsanitized paths or contacts in emitted fields |
| `D9_claim_boundary_gate` | No default public performance authorization |
| `D10_reproducibility_gate` | Optional upstream files match M12 SHA bindings |
| `D11_audit_posture_gate` | No weakening of merge-bar audit / governance |
| `D12_open_risk_disposition_gate` | Open-risk tracking (often `not_evaluated` on fixture path) |
| `D13_v2_recharter_scope_gate` | v2 recharter scope satisfied only with full governed evidence |
| `D14_non_claim_boundary_gate` | Explicit non-claims preserved |

Gate **status** vocabulary: `pass`, `warning`, `fail`, `blocked`, `not_evaluated`, `not_applicable`.

## CLI examples

**Default fixture (CI-safe):**

```bash
python -m starlab.v15.emit_v15_v2_go_no_go_decision \
  --output-dir out/v15_m13_v2_decision
```

**Operator preflight (M12 required):**

```bash
python -m starlab.v15.emit_v15_v2_go_no_go_decision \
  --profile operator_preflight \
  --m12-showcase-release-pack-json path/to/v15_showcase_agent_release_pack.json \
  --output-dir path/to/out
```

**Optional upstream cross-checks (must match M12 bindings):**

```bash
python -m starlab.v15.emit_v15_v2_go_no_go_decision \
  --profile operator_preflight \
  --m12-showcase-release-pack-json path/to/v15_showcase_agent_release_pack.json \
  --m08-campaign-receipt-json path/to/v15_long_gpu_campaign_receipt.json \
  --m09-promotion-decision-json path/to/v15_checkpoint_promotion_decision.json \
  --m10-xai-demonstration-json path/to/v15_replay_native_xai_demonstration.json \
  --m11-human-benchmark-claim-decision-json path/to/v15_human_benchmark_claim_decision.json \
  --m05-scorecard-json path/to/v15_strong_agent_scorecard.json \
  --m03-checkpoint-lineage-json path/to/v15_checkpoint_lineage_manifest.json \
  --output-dir path/to/out
```

**Operator-declared evidence:**

```bash
python -m starlab.v15.emit_v15_v2_go_no_go_decision \
  --profile operator_declared \
  --m12-showcase-release-pack-json path/to/v15_showcase_agent_release_pack.json \
  --decision-evidence-json path/to/v2_decision_operator_evidence.json \
  --output-dir path/to/out
```

## Emitted files

- `v15_v2_go_no_go_decision.json` (sealed with `v2_go_no_go_decision_sha256`)
- `v15_v2_go_no_go_decision_report.json`
- `v15_v2_go_no_go_decision_brief.md`

## Public / private boundary

**Public-safe:** contract IDs, SHA-256 bindings, decision status, gate statuses, recommended next step, sanitized operator-declared summaries, non-claims.

**Not public in this artifact:** raw weights, checkpoint blobs, replay paths, videos, saliency tensors, participant records, private operator notes, absolute paths, credentials.

## Non-claims (required)

V15-M13 does not train a checkpoint; does not promote a checkpoint; does not execute a long GPU campaign; does not run benchmarks; does not run live SC2; does not run XAI inference; does not run human-panel matches; does not release a showcase agent; does not authorize v2 on the default path; and does not commit model weights, checkpoint blobs, raw replays, videos, saliency tensors, participant records, private operator notes, or private paths.

## Closeout expectations

At honest closeout on the default path, the public record should state **v2 not authorized**, **v2 recharter not authorized**, no claim-critical register rows added by M13, and **recommended next step** toward operator evidence collection or v1.5 hardening. A stronger outcome is allowed only when explicitly supported by non-default governed evidence and bounded decision text.
