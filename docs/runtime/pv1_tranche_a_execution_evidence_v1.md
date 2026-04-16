# PV1 Tranche A execution evidence (v1)

## Purpose

This contract defines **what counts as Tranche A** for **PV1-M02 — Tranche A Execution Evidence**: the first **substantive post-v1** milestone that records **real operator-local** governed campaign execution on the closed **M49 / M50 / M51** machinery, with **PV1-M01** inspection artifacts at the tranche boundary.

**PV1** is post-v1 recharter (**not** “Phase VIII” of v1). There is **no M62**.

## Canonical operator note

Use a **single stable basename** at the campaign root:

- **`tranche_a_operator_note.md`**

Do not rely on ad hoc filenames for Tranche A closeout; audits and the ledger point here by convention.

## Kickoff freeze (required before execution)

Record and honor:

| Item | Description |
| --- | --- |
| `campaign_id` | Stable id in `full_local_training_campaign_contract.json` |
| `execution_id` | Primary execution under `campaign_runs/<execution_id>/` |
| `tranche_id` | Operator label (recommended: `tranche_a`) aligned with protocol phase naming |
| `checkpoint_id` | Tranche-boundary checkpoint (recommended: `tranche_a_close`) for PV1-M01 **`emit_tranche_checkpoint_receipt`** |
| `runtime_mode` | `fixture_stub_ci` or `local_live_sc2` — must match M02 adapter policy |
| M51 scope | Declare whether **`--post-bootstrap-protocol-phases`** is in scope (refit / M42 skip / watchable M44) |
| Stop / pause rules | When the operator stops, pauses, or treats the tranche as incomplete |
| Watchable validation | If declared in scope, M44 / `local_live_play_validation_run.json` expectations apply |

## What Tranche A means (PV1-M02)

**Tranche A** is the **first substantive bounded** operator-local slice under **PV1**, tied to **one** primary `execution_id`, large enough to be meaningful, **not** silently a full-run or **PV1-M03** claim.

Typical shape:

- One **`bootstrap_episodes`** protocol phase block the operator treats as Tranche A (often `phase`: `tranche_a` in `campaign_protocol`), **or** an explicitly named equivalent in custom protocol JSON.
- Optional **M51** post-bootstrap phases only if **frozen as in scope** at kickoff.

## Minimum evidence package

At minimum, the following must be **honestly** present under `out/training_campaigns/<campaign_id>/` (paths local by default; **not** committed to `main` unless policy explicitly allows):

| Class | Artifacts |
| --- | --- |
| Campaign identity | `full_local_training_campaign_contract.json` (+ sealed `campaign_sha256`) |
| Preflight | `campaign_preflight_receipt.json` |
| Execution | `campaign_runs/<execution_id>/hidden_rollout_campaign_run.json` (+ report); `campaign_execution_preflight_receipt.json` when produced |
| Phase receipts | `**/phase_receipt.json` for phases actually run (M51 order when `--post-bootstrap-protocol-phases`) |
| PV1-M01 (inspection only) | `campaign_observability_index.json` / `campaign_observability_index_report.json`; `tranche_checkpoint_receipt.json` / `tranche_checkpoint_receipt_report.json` at the declared tranche checkpoint |
| Operator gate | **`tranche_a_operator_note.md`** — explicit **completed / not completed within scope**, plus **continue / pause / stop** |
| Conditional | **`local_live_play_validation_run.json`** (and replay binding chain) **if** watchable M44 / live validation is in scope |

If something is missing, **do not fabricate it**. PV1-M01 helpers report gaps; they **do not** heal evidence.

## PV1-M01 helpers (inspection / reference only)

Use:

```bash
python -m starlab.training.emit_campaign_observability_index --campaign-root out/training_campaigns/<campaign_id>
python -m starlab.training.emit_tranche_checkpoint_receipt --campaign-root out/training_campaigns/<campaign_id> --tranche-id <id> --checkpoint-id <id>
```

Semantics: **`docs/runtime/pv1_campaign_observability_checkpoint_discipline_v1.md`**. These tools **do not** execute campaigns or substitute for operator-local execution evidence.

## “Tranche A completed” vs “not completed” (this milestone)

- **Completed within scope:** frozen kickoff satisfied; executor run matches declared scope; evidence package coherently present; operator note states completion **without** claiming full-run / Tranche B / PV1 completion.
- **Not completed within scope (honest):** operator note explicitly states **not completed** (paused, stopped, failed, or material evidence gap). **No silent retries** to “make it look perfect.”

## What PV1-M02 still does not prove

- Global benchmark integrity  
- Universal replay↔execution equivalence  
- Ladder / public strength  
- Live SC2 in CI as default merge norm  
- Full-run threshold or **PV1-M03** completion  
- Tranche B execution  

## Related runtime docs

- `docs/runtime/full_local_training_campaign_v1.md` (M49)  
- `docs/runtime/industrial_hidden_rollout_mode_v1.md` (M50 / M51)  
- `docs/runtime/pv1_campaign_observability_checkpoint_discipline_v1.md` (PV1-M01)  

## Reproducible protocol fixture (reference)

For **PV1-M02**, the repo includes a sealed protocol JSON used with **`emit_full_local_training_campaign_contract --campaign-protocol-json`**:

- `tests/fixtures/pv1_m02/pv1_m02_campaign_protocol.json`

Campaign contract output remains **operator-local** under `out/training_campaigns/`.
