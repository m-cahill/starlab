# V15-M10 — Replay-Native XAI Demonstration (runtime contract v1)

**Contract id:** `starlab.v15.replay_native_xai_demonstration.v1`  
**Milestone:** `V15-M10` **closed** on `main` (implementation [PR #136](https://github.com/m-cahill/starlab/pull/136); merge `a7e9b6e9af7c1cc084d4b73d2a64a2a05ac3cf1f` **2026-04-26T00:10:50Z** UTC; **authoritative PR-head CI** [`24943450910`](https://github.com/m-cahill/starlab/actions/runs/24943450910) head `142e13a8d6933f376818498d1a390cf3ba242101`; **merge-boundary `main` CI** [`24943955088`](https://github.com/m-cahill/starlab/actions/runs/24943955088)). **Public closeout posture:** default **`fixture_contract_only`** / **`blocked_missing_promoted_checkpoint`**; **real XAI inference executed:** **no**; **faithfulness validated:** **no**; **checkpoint promoted for XAI:** **no** on the default path; **strong-agent, ladder, human-benchmark, and v2 claim flags:** **false** in the honest public record; **claim-critical public register rows:** **no**; **raw** media, saliency, replays, weights, checkpoint blobs: **not** committed. **V15-M11:** **not started** / awaits explicit plan.  
**XAI evidence family (M04):** `starlab.v15.xai_evidence_pack.v1` — M10 **consumes and binds** M04-family packs; it does **not** redefine M04 evidence-pack vocabulary except for M10-specific demonstration and reporting fields.

## Relationship to M04

- **M04** = frozen XAI **evidence pack** contract and fixture/metadata emitters.
- **M10** = replay-native XAI **demonstration and reporting** surface: validates artifact shape, records SHA-256 bindings to M09/M04 (and optional preflight JSON), emits JSON reports and a deterministic Markdown explanation report.
- M10 **does not** run model inference, parse replays, read checkpoint weight blobs, or render saliency.

## Relationship to M09

Checkpoint **promotion** is recorded under `starlab.v15.checkpoint_promotion_decision.v1`. M10 may bind a promotion-decision JSON by **canonical JSON SHA-256** only. M09’s public default posture (no M08 campaign receipt, no promotion) **blocks** a real public XAI demo path unless separate operator evidence exists.

## Default posture (fixture / honest path)

On the default and CI fixture path:

- `xai_demonstration_status`: `fixture_contract_only` and/or `blocked_missing_promoted_checkpoint` (as recorded in the artifact).
- `real_inference_executed` / `faithfulness_validated` / program claim flags: **false**.
- No fabricated demonstration over a promoted trained checkpoint in the public repository default.

V15-M10 does not train a checkpoint; does not promote a checkpoint; does not run the long GPU campaign; does not prove explanation faithfulness; does not run a human panel; does not authorize strong-agent, human-benchmark, ladder, or v2 claims; and does not commit raw replays, weights, checkpoints, saliency tensors, videos, or private operator paths.

## Required inputs (real operator-declared / preflight path)

1. **M09** `v15_checkpoint_promotion_decision.json` (contract id must match).
2. **M04** `v15_xai_evidence_pack.json` (contract id must match).
3. **Preflight (optional profile):** additionally `v15_long_gpu_campaign_receipt.json`, `v15_checkpoint_lineage_manifest.json`, `v15_strong_agent_scorecard.json` for SHA-only bindings (no blob reads in M10).

M10 validates JSON object shape and **contract_id** fields; it does not verify on-disk files beyond parsing JSON.

## Emitted public artifacts (default filenames)

- `v15_replay_native_xai_demonstration.json` — sealed primary artifact.
- `v15_replay_native_xai_demonstration_report.json` — machine-readable sidecar (digest, seal check, `redaction_events` where applicable).
- `v15_xai_explanation_report.md` — deterministic Markdown, derived from the demonstration JSON (not a replacement for the JSON report).

## Validation gates (X0–X10)

Gate ids: `X0_artifact_integrity` … `X10_non_claim_boundary` (see code constants).  
Gate statuses: `pass`, `warning`, `fail`, `blocked`, `not_evaluated`, `not_applicable`.

## Scene and decision coverage vocabulary

Scene types include: `opening_build`, `first_scout`, `first_combat`, `expansion_timing`, `defensive_response`, `winning_push`, `loss_or_failure_case`, `counterfactual_decision`.  
Decision classes include: `macro`, `tactical`, `scouting_uncertainty`, `counterfactual`, `economy`, `production`, `movement`, `combat`, `fallback_noop_safety`.

## Authorization flags

All default **false** in repository fixtures: `xai_demo_executed`, `real_inference_executed`, `faithfulness_validated`, `checkpoint_promoted_for_xai`, `strong_agent_claim_authorized`, `human_benchmark_claim_authorized`, `ladder_claim_authorized`, `v2_authorized`.

## Public / private boundary

- **Public-safe:** contract JSON, SHA references, fixture vocabulary, governance Markdown.
- **Not committed by M10:** raw replays, weight blobs, heatmaps, videos, saliency tensors, or unsanitized operator paths. Operator-declared mode **redacts** path-like and contact-like strings in emitted content where the emitter merges operator metadata.

## Non-claims

XAI output is a **governed explanation pack** surface, not proof of causal human-like reasoning. Avoid claiming: full interpretability, global faithfulness, or agent strength. Use guarded phrasing: fixture pack validates artifact shape; report does not prove real inference or faithfulness.

## CLI examples

**Fixture (default, CI-safe):**

```bash
python -m starlab.v15.emit_v15_replay_native_xai_demonstration --output-dir out/v15_m10_xai_demo
```

**Operator-declared (M09 + M04 JSON, SHA binding):**

```bash
python -m starlab.v15.emit_v15_replay_native_xai_demonstration \
  --profile operator_declared \
  --m09-promotion-decision-json path/to/v15_checkpoint_promotion_decision.json \
  --m04-xai-evidence-pack-json path/to/v15_xai_evidence_pack.json \
  --output-dir out/m10_xai
```

**Operator preflight (optional, multi-input SHA binding):**

```bash
python -m starlab.v15.emit_v15_replay_native_xai_demonstration \
  --profile operator_preflight \
  --m09-promotion-decision-json m09.json \
  --m04-xai-evidence-pack-json m04.json \
  --m08-campaign-receipt-json m08.json \
  --m03-checkpoint-lineage-json m03.json \
  --m05-scorecard-json m05.json \
  --output-dir out/m10_preflight
```

## Governance

- No GPU, PyTorch, saliency, or SC2 in this milestone’s default emit path.
- Strengthens CI only via deterministic fixtures; does not add claim-critical public register rows by default.
