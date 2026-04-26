# V15-M11 — Human panel execution and bounded human-benchmark claim decision (runtime contract v1)

**Contract ids:** `starlab.v15.human_panel_execution.v1`, `starlab.v15.human_benchmark_claim_decision.v1`  
**Milestone:** `V15-M11` — **implementation** (governance **surface**; not a completed operator human-panel run).  
**Authority:** `docs/starlab-v1.5.md` (M11 non-claims block).

## Relationship to V15-M06 (human-panel protocol)

**M06** freezes the **human panel benchmark protocol** (`starlab.v15.human_panel_benchmark.v1` / `starlab.v15.human_panel_benchmark_protocol.v1` vocabulary) and fixture emission. **M11** **consumes** M06 **JSON** and binds it by **canonical JSON SHA-256** only. M11 **does not** redefine M06 participant tier, privacy, or threshold **vocabularies**; it reuses them via imports in code and optional **panel** evidence fields.

## Relationship to V15-M09 (checkpoint promotion)

**M09** `starlab.v15.checkpoint_promotion_decision.v1` records **promotion posture**. M11 binds a promotion JSON by SHA-256. If the public honest posture is **not promoted** (e.g. **`blocked`**, **`evaluated_not_promoted`**), M11 default gates and claim decisions remain **blocked** on **missing promoted checkpoint** — same honest dependency chain as M10.

## Relationship to V15-M10 (XAI demonstration / reporting)

**M10** `starlab.v15.replay_native_xai_demonstration.v1` is the replay-native XAI **demonstration and reporting** surface. M11 binds a M10 **demonstration** JSON by SHA-256 for **H10** (XAI sample binding) as **metadata and SHA wiring only** — not real XAI inference, not faithfulness proof.

## Default fixture / honest posture

- `human_panel_status`: `fixture_contract_only` and/or `blocked_missing_promoted_checkpoint` (as recorded)
- `human_panel_execution_performed`, `benchmark_execution_performed`, `human_benchmark_claim_authorized`, `v2_authorized`, etc.: **false** in repository defaults
- **No** fabricated participants, **no** real match table in public **register** **rows** by default

## Required operator inputs (non-default paths)

**Operator declared** (M06 + M09 + M10 + **panel** evidence JSON):

- `v15_human_panel_benchmark.json` (M06) — `contract_id` and `protocol_profile_id` must match
- `v15_checkpoint_promotion_decision.json` (M09)
- `v15_replay_native_xai_demonstration.json` (M10)
- **Panel evidence** JSON: only **public-allowlisted** keys (see code `PANEL_EVIDENCE_ALLOWED_KEYS`): aggregate counts, tier summary, `threshold_policy_id`, `threshold_frozen`, `privacy_profile_id`, `anonymized_participant_ids`, `replay_capture_status`, `operator_notes` (redacted on emit)

**Operator preflight** (adds M08, M05, M03 **SHA** bindings; **dry-run** / validation and gate computation only; **not** campaign execution, **not** real panel execution):

- Same as **operator declared** plus:
- `v15_long_gpu_campaign_receipt.json` (M08)
- `v15_strong_agent_scorecard.json` (M05)
- `v15_checkpoint_lineage_manifest.json` (M03)

## Privacy and participant redaction

Emitters **redact** absolute paths, obvious **emails** / **phone-like** / **handle-like** substrings, and operator notes per shared redaction policy. **Public** **artifacts** must not contain: real **names**; **emails**; **phone** numbers; **Discord** or unsanitized **Battle.net** handles; home/location; **raw** consent; **raw** private notes; **raw** **replay** / **video** / **local** paths. **Private** **material** **belongs** under **`out/`** or **local** `docs/company_secrets/**` and must stay **untracked** (not committed).

## Emitted public artifacts (default names)

- `v15_human_panel_execution.json` — sealed **execution** **artifact** (`human_panel_execution_sha256`)
- `v15_human_panel_execution_report.json` — **report** (digest, seal check, `redaction_events` where applicable)
- `v15_human_benchmark_claim_decision.json` — **claim** **decision** (`human_benchmark_claim_decision_sha256`) — read **only** from the **sealed** execution JSON; **not** a second M06/M09/M10 file binder
- `v15_human_benchmark_claim_decision_report.json` — **report**

## Validation gates (H0–H12)

See code constants: `H0_artifact_integrity` … `H12_non_claim_boundary`. **Gate statuses:** `pass`, `warning`, `fail`, `blocked`, `not_evaluated`, `not_applicable`. Default **CI** and **fixture** path leaves many gates **blocked** on **missing** **promotion**, **M08** **receipt**, **replay** / **roster** / **threshold** **freeze** **evidence**, etc. — as honest **non-executing** posture.

## Claim-decision vocabulary

**Labels** (non-exhaustive; see `human_panel_execution_models.py`): e.g. `evaluated_not_authorized`, `blocked_missing_promoted_checkpoint`, `blocked_missing_threshold_freeze`, `authorized_bounded_human_benchmark_claim` (only with explicit `authorization_flags` in a **non-default** evidence posture — not default / fixture).

**Authorization flags** default **false** in code (`human_panel_execution_performed`, `human_benchmark_claim_authorized`, `strong_agent_claim_authorized`, `checkpoint_promoted_for_human_panel`, `xai_sample_bound`, `ladder_claim_authorized`, `v2_authorized`, etc.).

## Public / private boundary and non-claims

- **Non-claim language (M11, required):** V15-M11 does not recruit human participants; does not run human-panel matches in CI; does not run live SC2 by default; does not promote a checkpoint; does not train a checkpoint; does not prove a strong-agent benchmark; does not authorize “beats most humans,” ladder, strong-agent, or v2 claims on the default path; and does not commit participant identities, raw replays, videos, checkpoint blobs, weights, private operator paths, or private human-panel notes.
- A **stronger** **status** is allowed only with explicit **non-default** operator evidence, separate review, and still **bounded** public **claim** **text** under declared STARLAB benchmark **rules** and **non-claims**.

## CLI examples (fixture, CI-safe)

**Human panel execution (fixture):**

```bash
python -m starlab.v15.emit_v15_human_panel_execution --output-dir out/v15_m11_human_panel
```

**Human-benchmark claim decision (reads execution JSON from previous step):**

```bash
python -m starlab.v15.emit_v15_human_benchmark_claim_decision \
  --human-panel-execution-json out/v15_m11_human_panel/v15_human_panel_execution.json \
  --output-dir out/v15_m11_human_panel
```

**Optional strict validation on claim decision (requires real SHA bindings, not all-zero placeholder):**

```bash
python -m starlab.v15.emit_v15_human_benchmark_claim_decision \
  --human-panel-execution-json out/v15_m11_human_panel/v15_human_panel_execution.json \
  --output-dir out/v15_m11_human_panel \
  --strict
```

**Operator preflight (M06/M09/M10 + M08/M05/M03 + panel evidence; SHA-only):**

```bash
python -m starlab.v15.emit_v15_human_panel_execution \
  --profile operator_preflight \
  --m06-human-panel-protocol-json path/to/v15_human_panel_benchmark.json \
  --m09-promotion-decision-json path/to/v15_checkpoint_promotion_decision.json \
  --m10-xai-demonstration-json path/to/v15_replay_native_xai_demonstration.json \
  --m08-campaign-receipt-json path/to/v15_long_gpu_campaign_receipt.json \
  --m05-scorecard-json path/to/v15_strong_agent_scorecard.json \
  --m03-checkpoint-lineage-json path/to/v15_checkpoint_lineage_manifest.json \
  --panel-evidence-json path/to/panel_evidence.json \
  --output-dir out/v15_m11_preflight
```

---

**V15-M12** (*Showcase Agent Release Pack*): **not** started in this public record; **M11** does not ship a release pack or v2 **authorization** unless **separately** **evidenced** under later **milestones**.
