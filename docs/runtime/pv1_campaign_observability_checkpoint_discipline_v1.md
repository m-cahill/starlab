# PV1 campaign observability and checkpoint discipline (v1)

## Purpose

This contract describes **PV1-M01** helper artifacts over existing **M49 / M50 / M51** campaign directory trees. These tools exist to make **tranche checkpoints** and **campaign-level evidence** easier to audit — they are **inspection and reference surfaces only**.

## Non-claims (binding)

These emitters **do not**:

- execute or complete campaigns,
- fabricate missing receipts or “heal” incomplete evidence,
- prove benchmark integrity, replay↔execution equivalence, ladder strength, or live SC2 in CI,
- satisfy a full-run threshold,
- replace operator judgment or operator-local execution evidence.

If files are absent on disk, the helpers **report them as missing**; they never invent paths or upgrade posture.

## Evidence status vocabulary (v1)

Artifacts use a small deterministic enumerated posture (see `ALL_EVIDENCE_STATUSES_V1` in `starlab.training.pv1_campaign_observability_models`):

| Status | Meaning |
| --- | --- |
| `complete` | Required inspected evidence classes are present for the chosen ruleset (index) or checkpoint scan. |
| `incomplete` | Operator-declared incomplete checkpoint posture (`--incomplete` on checkpoint receipt) when objective required evidence is present. |
| `paused` | Operator-declared pause (`--paused`) when objective required evidence is present. |
| `missing_required_evidence` | At least one required evidence class is absent on disk. **Takes precedence** over `--paused` / `--incomplete` when files are missing. |
| `not_evaluable` | Reserved for the vocabulary; index emission uses `complete` vs `missing_required_evidence` for the default ruleset. |

## Artifact filenames

| Filename | Role |
| --- | --- |
| `campaign_observability_index.json` | Canonical machine-readable inventory + `index_sha256`. |
| `campaign_observability_index_report.json` | Short human-oriented summary. |
| `tranche_checkpoint_receipt.json` | Canonical checkpoint receipt + `receipt_sha256`. |
| `tranche_checkpoint_receipt_report.json` | Short human-oriented summary. |

## Required evidence classes (default scan)

For **both** the observability index and the tranche checkpoint receipt, the default ruleset checks presence of:

1. `full_local_training_campaign_contract.json` at the campaign root,
2. `campaign_preflight_receipt.json` at the campaign root,
3. at least one `campaign_runs/<execution_id>/hidden_rollout_campaign_run.json`,
4. at least one `**/phase_receipt.json`,
5. at least one `**/replay_binding.json`,
6. at least one `**/local_live_play_validation_run.json`.

These are **layout / presence** checks only — contents are not validated as correct execution proofs.

## CLI (emitters)

Primary input for both commands:

- `--campaign-root` → `out/training_campaigns/<campaign_id>/`

Optional:

- `--campaign-contract` → alternate path to `full_local_training_campaign_contract.json` used **only** to override the displayed `campaign_id` label (secondary; scanning still uses `--campaign-root`).

```bash
python -m starlab.training.emit_campaign_observability_index --campaign-root out/training_campaigns/<campaign_id>
python -m starlab.training.emit_tranche_checkpoint_receipt --campaign-root out/training_campaigns/<campaign_id> --tranche-id <id> --checkpoint-id <id>
```

Outputs default to `--campaign-root`; use `--output-dir` to redirect.

## Related runtime docs

- `docs/runtime/full_local_training_campaign_v1.md` (M49)
- `docs/runtime/industrial_hidden_rollout_mode_v1.md` (M50)
- Post-v1 charter: **Post-v1 (PV1)** section in `docs/starlab.md`
