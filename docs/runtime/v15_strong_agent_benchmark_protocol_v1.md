# STARLAB v1.5 — Strong-agent benchmark protocol (V15-M05)

**Milestone:** `V15-M05` — *Strong-Agent Benchmark Protocol*  
**Document type:** public runtime / narrative (protocol contract only)  
**Primary contract id:** `starlab.v15.strong_agent_scorecard.v1`  
**Protocol profile id (embedded in the scorecard JSON):** `starlab.v15.strong_agent_benchmark_protocol.v1`  
**Emitter:** `python -m starlab.v15.emit_v15_strong_agent_scorecard --output-dir <path>`

> **V15-M05 freezes the strong-agent benchmark protocol and scorecard contract. It does not run the benchmark and does not certify any checkpoint as strong.**

**Closure (public):** **V15-M05** is **closed** on `main` ([PR #125](https://github.com/m-cahill/starlab/pull/125); merge `d7daee6e43613daf85e544ac5a25179cb5697c76`). This closure records **governance, contract, and CI** for the **protocol / scorecard** surface only. It is **not** a statement that a benchmark or tournament was **executed**; that a checkpoint was **evaluated** or **promoted**; or that a **strong-agent** claim is **authorized**. **`benchmark_execution_performed`**, **`strong_agent_claim_authorized`**, and **`long_gpu_run_authorized`** remain **false** in the emitted M05 contract.

---

## 1. Purpose of V15-M05

M05 establishes the **governed vocabulary and shapes** for how STARLAB v1.5 will later talk about a **strong-agent** evaluation: evaluation ladder, protocol profile, subject kinds, map/opponent pool metadata, **scorecard field names** (not live values), evidence classes, and explicit **claim boundaries** — **before** any real matches are run. It is the contract surface for **Gate E — Evaluation** in the long GPU run gates and for later V15 evaluation milestones.

---

## 2. Relationship to V15-M00 gates A–G

M05 supports **gate E (Evaluation)**. It does **not** by itself prove any gate is satisfied. The M05 fixture / operator-**declared** scorecard is **not** a statement that the training readiness charter or long-GPU run gates (A–G) are all green; see `v15_training_readiness_charter.json` and `docs/starlab-v1.5.md` §7.

| Gate | M05 role |
| --- | --- |
| A — Governance | Non-claims and contract ids are recorded in the emitted scorecard. |
| B — Environment | May **reference** M02 environment lock by canonical JSON SHA in optional bindings only. |
| C — Data | May reference registers / manifest hashes as **metadata**; no corpus I/O. |
| D — Checkpoints | May reference checkpoint lineage by canonical JSON SHA; **no** weight blob reads. |
| E — Evaluation | **Primary:** ladder, baselines, scorecard fields, gate definitions (no execution). |
| F — XAI | `xai_requirements` and `xai_review_reserved` reference the M04 contract; **no** XAI **review** in M05. |
| G — Operator | `operator_notes` and optional **protocol** JSON; **not** a runbook execution proof. |

---

## 3. Relationship to V15-M01 asset registers

M05 may **reference** logical checkpoint ids, lineage manifest SHA, or other ids that **align** with `docs/*_register.md` and `starlab.v15.training_asset_registers.v1` — it does **not** add public **register rows** and does **not** approve real assets for claim-critical use.

---

## 4. Relationship to V15-M02 environment lock

When `--environment-lock-json` is provided, the emitter binds the **canonical JSON SHA-256** of the M02 environment lock file into `optional_bindings` only. It does **not** read or trust host paths, does **not** run SC2, and does **not** authorize a long GPU run.

---

## 5. Relationship to V15-M03 checkpoint lineage

When `--checkpoint-lineage-json` is provided, the emitter binds the **canonical JSON SHA-256** of the lineage manifest. It does **not** read checkpoint **blobs**, does **not** verify bytes, and does **not** treat lineage as a promotion / strong-agent proof.

---

## 6. Relationship to V15-M04 XAI evidence contract

M05’s `xai_requirements` may cite `starlab.v15.xai_evidence_pack.v1`. With `--xai-evidence-json`, the emitter binds the **SHA-256 of that JSON file** only. M05 does **not** run inference, does **not** verify explanation faithfulness, and does **not** add real XAI register rows. **`xai_review_reserved`** is a **reservation** for **V15-M10+**; real review is out of scope for M05.

---

## 7. Evaluation ladder and stage definitions

Machine-readable **stage_id** values (deterministic) are:

- `E0_artifact_integrity` — Artifacts, manifests, and binding coherence.  
- `E1_fixture_smoke` — CI / wiring smoke; **not** a performance claim.  
- `E2_scripted_baselines` — Scripted baseline suite (M21-class narrative).  
- `E3_heuristic_baselines` — Heuristic baseline suite (M22-class narrative).  
- `E4_prior_starlab_checkpoints` — Prior STARLAB checkpoints.  
- `E5_local_live_sc2_bounded` — Bounded operator-local live SC2 (out of scope for M05 **execution**).  
- `E6_failure_mode_probes` — Failure / exploit-surface **probes** (defined, not run in M05).  
- `E7_human_panel_reserved` — **Reserved** for **V15-M06+**; see `reserved_human_panel_section`.  
- `E8_xai_review_reserved` — **Reserved** for **V15-M10+**; see `xai_review_reserved`.

M05 only **records** `stage_id`, `stage_name`, `stage_status`, and `notes` — it does not execute stages.

---

## 8. Scorecard fields and gate definitions (protocol only)

- **Scorecard field rows** list **field_name**, **type**, and **status** = “defined” / “not evaluated” in fixture — they are **not** populated with live win rates, losses, or tournament aggregates in M05.  
- **Gate threshold rows** define `metric_name`, `comparison`, and `threshold_value` as **declared** or placeholder strings; **no** `passed` / `failed` outcome is asserted in M05.

The following **metric names** are part of the required protocol vocabulary: `win_rate`, `loss_rate`, `draw_or_timeout_rate`, `average_game_length`, `early_loss_rate`, `economy_score`, `production_score`, `combat_score`, `scouting_score`, `expansion_score`, `fallback_action_rate`, `invalid_action_rate`, `xai_trace_coverage`, `critical_decision_trace_count`.

---

## 9. Benchmark protocol profile

- `contract_id`: `starlab.v15.strong_agent_scorecard.v1` — the emitted artifact **family** (JSON contract).  
- `protocol_profile_id`: `starlab.v15.strong_agent_benchmark_protocol.v1` — the **protocol profile** embodied in that contract.

**Do not** conflate a **profile id** in operator JSON with a successful benchmark run. **Do not** treat fixture subjects (`fixture_candidate`, `fixture_scripted_baseline`, …) as evaluated agents.

---

## 10. Subject categories (vocabulary)

| `subject_kind` (examples) | Role in M05 |
| --- | --- |
| `fixture_candidate` | Synthetic protocol row only. |
| `scripted_baseline` | Baseline **family** reference (no match results). |
| `heuristic_baseline` | Baseline **family** reference (no match results). |
| `prior_starlab_checkpoint` | Id / SHA references allowed; no promotion. |
| `candidate_checkpoint` | Id / SHA references allowed; not evaluated in M05. |
| `live_sc2_candidate` | Reserved for later bounded live eval; not executed in M05. |
| `human_panel_reserved` | Tied to human-panel milestone reservation. |

---

## 11. Evidence requirements by stage (summary)

- **E0 / E1:** environment lock + lineage + charter-level integrity **references** (SHA-only bindings when files supplied).  
- **E2–E4:** baseline and checkpoint identity references; no tournament emission in M05.  
- **E5–E6:** local SC2 and probe **stubs** in protocol; execution deferred.  
- **E7:** human panel: **see** `reserved_human_panel_section` — **V15-M06+**.  
- **E8:** XAI review: **see** `xai_review_reserved` — **V15-M10+**.

---

## 12. Non-claims and claim boundaries

- **A strong-agent scorecard contract is not evidence that a strong-agent benchmark has passed.**  
- **A fixture benchmark protocol is schema / wiring evidence only, not a performance result.**  
- M05 may validate **metadata** and **redact** absolute-path-like strings in emitted JSON as `<REDACTED_ABSOLUTE_PATH>`; it does **not** run GPU training, benchmark execution, live SC2, XAI **review** execution, or human-panel **execution**; it does **not** open v2 or **PX2-M04** / **PX2-M05**.

---

## 13. Human panel and XAI review (reserved)

**`reserved_human_panel_section`** includes `reserved: true`, `owner_milestone: V15-M06`, `execution_performed: false`, `claim_authorized: false`, and a **non-claim** string. Human-panel **protocol** and execution are **V15-M06+**.

**`xai_review_reserved`** includes `reserved: true`, `owner_milestone: V15-M10+`, `review_performed: false`, `faithfulness_validated: false`, and a **non-claim** string. Real XAI **review** is **V15-M10+**.

---

## 14. CLI reference

```bash
python -m starlab.v15.emit_v15_strong_agent_scorecard --output-dir <dir>
```

Optional:

```text
--profile fixture_ci
--profile operator_declared
--protocol-json <path>
--checkpoint-lineage-json <path>
--xai-evidence-json <path>
--environment-lock-json <path>
```

Default: **`fixture_ci`**. The default path requires **no** GPU, SC2, real checkpoints, XAI **inference**, or human participants.

---

## 15. Emitted artifacts (public names)

- `v15_strong_agent_scorecard.json` — contract body + `strong_agent_scorecard_sha256` seal.  
- `v15_strong_agent_scorecard_report.json` — summary counts + seal echo.

**Contract id:** `starlab.v15.strong_agent_scorecard.v1`  
**Protocol profile id (inside JSON):** `starlab.v15.strong_agent_benchmark_protocol.v1`
