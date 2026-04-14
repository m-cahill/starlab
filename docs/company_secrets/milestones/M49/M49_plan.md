# M49 Plan — Full Local Training / Bootstrap Campaign Charter & Evidence Protocol

**Status:** Complete — closed on `main` (see `M49_run1.md`, `M49_summary.md`, `M49_audit.md`)  
**Phase:** VI  
**Milestone number:** M49  
**Type:** Small governance/runtime milestone with operator-local follow-on evidence

## Why this milestone exists

STARLAB already has the core training and validation surfaces on `main`:

* **M40** training-program charter
* **M41** replay-imitation training
* **M42** learned-agent comparison
* **M43** hierarchical training
* **M44** local live-play validation
* **M45** self-play / RL bootstrap
* **M46** bounded live semantics
* **M47** bootstrap episode distinctness / operator ergonomics
* **M48** learned-agent comparison contract-path alignment

The next high-value problem is no longer “can STARLAB train anything?” It is:

**How do we run a substantial local training / bootstrap campaign in a governed, auditable, reproducible, operator-friendly way without hiding a long local run inside milestone product scope?**

This milestone defines that campaign clearly, keeps CI truthful, and prepares the actual long operator run to happen under a strong evidence protocol.

## Milestone title

**M49 — Full Local Training / Bootstrap Campaign Charter & Evidence Protocol**

## Objective

Create the governed contract, preflight, and evidence protocol for a substantial **operator-local** full training / bootstrap campaign over the existing Phase VI surfaces.

## Milestone posture

* **M49 product scope:** charter, contract artifact, preflight, docs, and tests
* **M49 operator follow-on:** the actual long local run under that charter
* **CI posture:** fixture-only, no live SC2, no long local campaign in CI

## Deliverables (implementation)

* `docs/runtime/full_local_training_campaign_v1.md` — normative runtime / contract document
* `starlab.training` — `full_local_training_campaign_*` modules; emitters:
  * `python -m starlab.training.emit_full_local_training_campaign_contract`
  * `python -m starlab.training.emit_full_local_training_campaign_preflight`
* Artifacts under `out/training_campaigns/<campaign_id>/`: `full_local_training_campaign_contract.json`, `full_local_training_campaign_contract_report.json`, `campaign_preflight_receipt.json`
* Cross-links from `docs/runtime/self_play_rl_bootstrap_v1.md`, `docs/runtime/agent_training_program_contract_v1.md`, `docs/runtime/learned_agent_comparison_harness_v1.md`, and `docs/diligence/phase_vi_integrated_test_campaign.md`
* Tests: `tests/test_m49_full_local_training_campaign.py`

## Acceptance criteria

1. A governed full local campaign contract can be emitted deterministically (same inputs + same output paths → same `campaign_sha256`).
2. A deterministic preflight surface clearly states whether the local campaign is ready.
3. The runtime docs clearly define protocol phases, refit eligibility, and non-claims.
4. The contract distinguishes planning/preflight from execution and from success.
5. CI stays fixture-only and green.

## Explicit non-claims (M49)

M49 does **not** prove: benchmark integrity, replay↔execution equivalence, live SC2 in CI, ladder performance, strong learning gains, or that a long local campaign will produce a strong policy by default.

It proves: the full campaign is **governed, preflighted, and evidence-ready**.

## Recommended branch name

`m49-full-local-training-campaign-charter`

## Closeout (when authorized)

* Summary / audit per prompts; update `docs/starlab.md` fully
* Seed **M50** stub (`M50_plan.md`, `M50_toolcalls.md`)
