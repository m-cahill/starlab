# M26 Plan — Replay Corpus Governance & Training Dataset Contract

**Milestone:** M26  
**Phase:** V — Learning Paths, Evidence Surfaces, and Flagship Proof  
**Status:** **Complete** — product merged to `main` ([PR #32](https://github.com/m-cahill/starlab/pull/32)); ledger closeout on `main` records milestone artifacts and **M27** stubs.

## Objective

Prove a **deterministic, offline, governed replay-training-dataset layer** that packages replay-derived imitation examples as **stable references** over already-governed **M14** replay bundle artifacts — **without** training a model and **without** **M27** imitation-baseline product code.

## Scope

### In scope

- Runtime contract for **`replay_training_dataset.json`** / **`replay_training_dataset_report.json`**
- Deterministic corpus selection over governed bundle inputs
- Deterministic **train / validation / test** split (`sha256(example_id)` modulo 100; 80/10/10)
- Coarse **action-type** label vocabulary (not raw M10 `semantic_kind`)
- Canonical JSON + sorted warnings / non-claims
- Fixture-backed tests + goldens; **AST import guard** (no `starlab.sc2`, `s2protocol`, `starlab.replays`)
- Optional M07 intake: **absent** → warning; **present** + `quarantined`/`rejected` → hard fail
- Ledger update: **33 → 35** milestones planned arc; **OD-007** → **M34**

### Out of scope

- Model training, imitation quality claims, hierarchical control, benchmark integrity, replay↔execution equivalence, live SC2 in CI, raw replay parsing, **M27+** product code.

## Deliverables

- `docs/runtime/replay_training_dataset_v1.md`
- `starlab/imitation/dataset_models.py`, `dataset_views.py`, `emit_replay_training_dataset.py`
- `tests/fixtures/m26/` (goldens + `replay_intake_receipt_quarantined.json` negative aid)
- `tests/test_replay_training_dataset.py`
- `docs/starlab.md` (35-milestone arc, Phase V/VI, §11, §23, OD-007)

## CLI

```bash
python -m starlab.imitation.emit_replay_training_dataset --bundle PATH --output-dir OUT
```

## Definition of done

- [x] Contract doc + deterministic emitters + tests green + ledger checklist satisfied.
- [x] Authoritative PR-head CI + merge-boundary `main` CI recorded (`M26_run1.md`, §18).
- [x] Milestone summary + audit + closeout ledger (`M26_summary.md`, `M26_audit.md`, §23).
