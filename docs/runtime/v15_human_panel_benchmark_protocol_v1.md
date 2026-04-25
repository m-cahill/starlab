# STARLAB v1.5 — Human panel benchmark protocol (V15-M06)

**Milestone:** `V15-M06` — *Human Panel Benchmark Protocol*  
**Document type:** public runtime / narrative (protocol contract only)  
**Primary contract id:** `starlab.v15.human_panel_benchmark.v1`  
**Protocol profile id (in JSON):** `starlab.v15.human_panel_benchmark_protocol.v1`  
**Emitter:** `python -m starlab.v15.emit_v15_human_panel_benchmark --output-dir <path>`

> **V15-M06 freezes the human-panel benchmark protocol, privacy posture, and evidence vocabulary. It does not run a human panel, recruit participants, or authorize a “beats most humans” claim.**

**Implementation status:** **closed** on `main` ([PR #127](https://github.com/m-cahill/starlab/pull/127); merge `994f24e605e32c0738f34eb4d09be2020d543c3c`). **Authoritative PR-head CI:** [`24924293130`](https://github.com/m-cahill/starlab/actions/runs/24924293130); **merge-boundary `main` CI:** [`24924371412`](https://github.com/m-cahill/starlab/actions/runs/24924371412) — **success**. This document and the emitters are **protocol and fixture only**; they are **not** evidence of human-benchmark **execution** or **pass/fail** outcomes. **`benchmark_execution_performed`**, **`human_panel_execution_performed`**, **`human_benchmark_claim_authorized`**, **`strong_agent_claim_authorized`**, and **`long_gpu_run_authorized`** stay **false** in emitted M06 contracts.

---

## 1. Purpose of V15-M06

M06 establishes the **governed vocabulary and contract shape** for how STARLAB v1.5 will later declare a **human-panel** benchmark: participant tiers, consent/privacy posture, session and match rules, map pool policy, threshold policy, evidence class requirements, claim boundaries, and **non-claims** — **before** any real participants or matches. It is the successor to the **E7** `reserved_human_panel_section` in the M05 strong-agent scorecard: **M05** reserved human-panel work for **M06+**; **M06** supplies the **protocol** artifact family.

---

## 2. Relationship to V15-M05 strong-agent benchmark protocol

- M05’s **`reserved_human_panel_section`** points to **M06+**; M06 is the first milestone that emits a **human-panel benchmark** contract id.
- M06 **may** bind optional **canonical JSON SHA-256** only for: M02 environment lock, M03 checkpoint lineage, M05 strong-agent scorecard, M04 XAI pack — same SHA-only posture as M04/M05. **No** blob reads, **no** replay I/O, **no** XAI inference.

---

## 3. Relationship to V15-M11 execution

- **M06** = protocol freeze + `fixture_ci` + optional `operator_declared` metadata validation.
- **M11** — *Human Panel / Bounded Human Benchmark* — is where **real** (or operator-declared) human-panel **execution** and result reporting would occur under this protocol. **M06 does not start M11.**

---

## 4. Human panel protocol fields (summary)

The emitted `v15_human_panel_benchmark.json` includes at minimum: `contract_id`, `contract_version`, `protocol_profile_id`, milestone and emitter identity, **authorization booleans** (all **false** in default fixture), `participant_privacy_profile`, `participant_tiers`, eligibility/consent/session/match rules, map pool policy, agent and checkpoint **binding** requirements, replay capture requirements, `result_policy`, `threshold_policy`, `evidence_requirements`, `claim_boundary` (allowed + disallowed claim shapes), `non_claims`, `redaction_policy`, and `optional_bindings` (SHA-only).

---

## 5. Participant tiers (strict vocabulary)

Fixture and protocol use deterministic tier ids (examples): `casual_unranked`, `bronze_silver_equivalent`, `gold_platinum_equivalent`, `diamond_plus_equivalent`, `unknown_self_reported`, `observer_or_non_competing`. Unverifiable skill must be tagged **unknown** or **self-reported** in real execution (M11+).

---

## 6. Consent and privacy model (strict)

Core posture values include: `private_identity_required`, `public_identity_forbidden_by_default`, `pseudonymous_participant_id_required`, `raw_contact_info_forbidden_in_public_artifacts`, `consent_record_required_for_execution`. These are **enum-like** in the contract; they are not free-form. Optional operator notes go to **`operator_notes`** or **`operator_extension_flags`** and do **not** replace required posture rows.

---

## 7. Public / private boundary

- **Public** fixtures: **no** real names, emails, Battle.net tags, Discord handles, IPs, or contact info.
- **Private** by default: participant rosters, consent receipts, raw replays, and private session records — under `docs/company_secrets/` or operator-local storage; **not** committed in M06.

---

## 8. Match / session rules (declared, not executed)

The protocol encodes **declared** fields for Terran-first 1v1, predeclared **game count**, **map pool** frozen before execution, **replay capture** required for the execution milestone, and placeholders for disconnect/pause/observer/rematch/forfeit **policies** — all **vocabulary and schema** in M06; **no** live SC2 in merge-gate CI.

---

## 9. Evidence requirements (classes, not results)

Required **evidence class** tags include: `protocol_manifest`, `participant_roster_private`, `participant_tier_summary_public`, `consent_receipts_private`, `agent_checkpoint_identity`, `checkpoint_lineage_manifest_sha256`, `environment_lock_sha256`, `match_replay_manifest`, `match_result_manifest`, `session_operator_note`, `human_panel_result_report`, `xai_pack_sample_requirement`, `non_claims`. M06 lists **requirement** rows only; it does not assert that evidence **exists** or **passes** review.

---

## 10. Threshold policy

Supported options in vocabulary include: `majority_threshold_gt_50`, `supermajority_threshold_gte_65`, `tier_scoped_majority`, `no_claim_without_threshold_freeze`. M06 does **not** assert that any threshold is **met**.

---

## 11. Allowed future claim shape (protocol-bound)

The **allowed** bounded claim text is fixed in the contract as:

> The STARLAB v1.5 Showcase Agent exceeds the declared human-panel threshold under fixed Terran-first 1v1 rules, declared maps, fixed checkpoint identity, replay capture, participant-tier disclosure, and recorded non-claims.

**Disallowed** unbounded shapes are listed in `claim_boundary.disallowed_shapes` (e.g. “beats all humans”, “ladder-proven”, “solved StarCraft II”, “globally superior SC2 agent”, “human-like reasoning proven”, “v2-ready by default”).

---

## 12. Non-claims (M06)

A human-panel **protocol** contract is **not** evidence that a human benchmark was **run** or **passed**. M06 does not recruit, does not run matches, does not authorize strong-agent or human-benchmark **claims**, does not run GPU training or shakedown, does not open v2 or **PX2-M04** / **PX2-M05**, and does not add real rows to public registers. See `docs/starlab-v1.5.md` for the full **M06 non-claims** block.

---

## 13. CLI reference

```bash
python -m starlab.v15.emit_v15_human_panel_benchmark --output-dir <dir>
```

Optional:

```text
--profile fixture_ci
--profile operator_declared
--protocol-json <path>
--environment-lock-json <path>
--checkpoint-lineage-json <path>
--strong-agent-scorecard-json <path>
--xai-evidence-json <path>
```

Default: **`fixture_ci`**. The fixture profile requires **no** GPU, SC2, real participants, checkpoint blobs, raw replays, or XAI inference.

---

## 14. Emitted artifacts

- `v15_human_panel_benchmark.json` — contract body + `human_panel_benchmark_sha256` seal.  
- `v15_human_panel_benchmark_report.json` — `artifact_sha256` (seal echo), counts, `claim_authorized`, `execution_performed`, `redaction_count`, `optional_binding_keys`.

**Contract id:** `starlab.v15.human_panel_benchmark.v1`  
**Protocol profile id:** `starlab.v15.human_panel_benchmark_protocol.v1`
