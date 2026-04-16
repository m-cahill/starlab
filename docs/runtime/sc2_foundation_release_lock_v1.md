# SC2 foundation release lock v1 (M61)

**Status (ledger alignment):** **M61 machinery** (proof pack + audit emitters + this contract + tests) is **merged on `main`** ([PR #72](https://github.com/m-cahill/starlab/pull/72); merge commit `35d7734d14113adf206390f153f517a93d7d41ba`; tag **`v0.0.61-m61`**). **Operator-local** industrial campaign evidence packaged into a proof pack, and a release-lock audit reporting **`release_scope_status`: `ready_within_scope`**, remain **pending** — **not** satisfied by default CI or fixture-only tests alone.

**Contract ids:** `starlab.sc2_foundation_v1_proof_pack.v1`, `starlab.sc2_foundation_release_lock_audit.v1`  
**Input contract:** `starlab.sc2_foundation_v1_proof_pack_input.v1` (operator-authored JSON)  
**Scope id:** `starlab.m61.release_scope.sc2_foundation_v1`  
**Evidence profile (mandatory for within-scope readiness):**  
`starlab.m61.campaign_evidence_profile.operator_local_hidden_rollout_with_watchable_validation_v1`

## Release scope

M61 closes the **v1** program arc with a **bounded release-lock evidence surface**: a deterministic proof pack that references prior milestone anchors **and** one **operator-local industrial hidden rollout** campaign executed on the governed **M49 → M50 → M51** path, including **post-bootstrap protocol phases** and **one watchable M44 validation** tied to that execution.

This milestone **does not** broaden claims in **M52–M59**; the proof pack and audit must preserve explicit **non-claims**.

## Required evidence classes

1. **Foundation track refs** — primarily **git milestone tags** (`v0.0.39-m39` … `v0.0.60-m60`) with optional merge SHAs / PR links; string refs only (no obligation to re-parse every historical artifact in CI).
2. **M49 governance** — paths to `full_local_training_campaign_contract.json` and `campaign_preflight_receipt.json` for the **same** campaign as the execution record.
3. **M50/M51 execution** — `hidden_rollout_campaign_run.json` (+ report) from `execute_full_local_training_campaign`, with **`post_bootstrap_protocol_phases_enabled`: true** and phase receipts showing **post-bootstrap phases** executed or honestly skipped per contract.
4. **Watchable M44** — `local_live_play_validation_run.json` for the watchable validation phase, **`replay_binding.json`**, and the **validation replay file** path; replay-backed evidence is the primary watchability proof. Optional video metadata or operator watch notes may be attached but **must not** be the sole basis of proof.
5. **M45 bootstrap report** — path to the relevant bootstrap run report (e.g. `self_play_rl_bootstrap_run_report.json` or campaign-level aggregate the operator declares).
6. **Operator-declared full-run threshold** — `campaign_length_class` must be `operator_declared_full_run`, with `threshold_satisfied: true` and a human-readable `operator_defined_full_run_threshold`.

## Release-lock statuses (`release_scope_status`)

| Value | Meaning |
| ----- | ------- |
| `ready_within_scope` | Proof pack + audit checks satisfied; within-scope v1 release language applies. |
| `not_ready_within_scope` | Missing mandatory campaign/post-bootstrap/watchable evidence, failed threshold, or failed non-claim hygiene. |
| `not_evaluable` | Proof pack integrity or contract id invalid (e.g. SHA mismatch). |

The audit **fails `ready_within_scope`** if the pack lacks: **operator-declared full run** (`operator_declared_full_run` + `threshold_satisfied`), **executed post-bootstrap protocol phases** on the campaign run, or **watchable M44 validation** tied to the campaign path (executed phase + `final_status` on M44).

## Local-only evidence posture

- Raw campaign outputs live under **`out/`** (and similar local roots). **Do not** commit `docs/company_secrets/`, raw `out/` trees, or local weights to the public repo.
- CI proves **emitters + fixture tests** only. **One fresh M61-designated operator-local run** is the default bar for real release-lock evidence (older campaigns may be used only if they cleanly satisfy the same evidence profile without caveats).

## Relationship to other milestones

| Anchor | Role in M61 |
| ------ | ----------- |
| **M39** | Public flagship proof reference (offline substrate narrative). |
| **M49** | Campaign contract + preflight — charter, not automatic execution proof. |
| **M50/M51** | Industrial executor + optional post-bootstrap phases + watchable M44 on refit path. |
| **M44** | Watchable validation harness + replay binding. |
| **M52–M54** | Replay↔execution equivalence charter / evidence / audit — **bounded**, not universal. |
| **M55–M56** | Benchmark integrity charter / gates — **not** global integrity proof. |
| **M57–M58** | Live SC2 in CI posture — **not** default merge-gate live SC2. |
| **M59** | Ladder/public **descriptive** protocol — **not** ladder strength. |
| **M60** | Structural executor split / diligence — stable base for M50/M51 CLI. |

## CLI (file-based)

```bash
python -m starlab.release_lock.emit_sc2_foundation_v1_proof_pack \
  --input proof_pack_input.json \
  --output-dir <dir> \
  [--base-dir <dir>]

python -m starlab.release_lock.emit_sc2_foundation_release_lock_audit \
  --proof-pack <dir>/sc2_foundation_v1_proof_pack.json \
  --output-dir <dir>
```

See `tests/fixtures/m61/proof_pack_input.json` for a minimal **shape** (fixture campaigns are not substitute for a real operator run).

## Explicit non-claims (summary)

M61 does **not** prove: universal benchmark integrity; universal replay↔execution equivalence; live SC2 as default merge CI; ladder/public performance; automated ladder play; or v2/multi-environment scope. It does **not** create **M62** unless the ledger is rechartered.
