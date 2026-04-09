# M19 Plan — Cross-Mode Reconciliation & Representation Audit

**Milestone:** M19  
**Phase:** III — State, Representation, and Perception Bridge  
**Working title:** Cross-Mode Reconciliation & Representation Audit  
**Recommended branch:** `m19-cross-mode-reconciliation-representation-audit`

## Objective

Prove a **narrow, deterministic audit layer** over the existing Phase III surfaces by reconciling **one** M16 `canonical_state.json` with **one** M18 `observation_surface.json` for the **same** `gameloop` and **same** `perspective_player_index`, and by emitting a governed audit artifact that makes representation alignment, bounded loss, and expected non-equivalences explicit.

This milestone exists because M18 proved a prototype materialization path, but did **not** prove reconciliation. Phase III in the ledger explicitly reserves M19 for that audit step.

## Scope interpretation locked for Cursor

For M19, **cross-mode** means:

- **Mode A:** M16 canonical, replay-derived global frame (`canonical_state.json`)
- **Mode B:** M18 player-relative observation instance (`observation_surface.json`)

M19 is **not** a replay milestone, **not** a legality milestone, **not** a benchmark milestone, and **not** a live-runtime milestone. It should audit how Mode B relates to Mode A under STARLAB’s existing bounded claims.

## Narrow objective

Implement a deterministic reconciliation/audit CLI and runtime contract that:

1. loads one canonical-state / observation pair,
2. verifies provenance and identity consistency,
3. classifies each audited representation mapping as one of: `exact`, `derived`, `bounded_lossy`, `unavailable_by_design`, `mismatch`,
4. emits deterministic JSON audit artifacts,
5. fails only on **unexpected** inconsistencies, while preserving explicit warnings for expected prototype limitations.

## In scope

### Runtime contract

- `docs/runtime/observation_reconciliation_audit_v1.md`

This document should define:

- required and optional inputs
- exact output filenames
- deterministic ordering rules
- audit status vocabulary
- failure conditions
- explicit non-claims
- relation to M15/M16/M17/M18 boundaries

### Product code

Add under `starlab/observation/` only:

- `observation_reconciliation_inputs.py`
- `observation_reconciliation_rules.py`
- `observation_reconciliation_pipeline.py`
- `audit_observation_surface.py`

Naming can tighten slightly during implementation, but keep the surface this small.

### Artifacts per CLI invocation

Emit exactly:

- `observation_reconciliation_audit.json`
- `observation_reconciliation_audit_report.json`

### CLI

```text
python -m starlab.observation.audit_observation_surface \
  --canonical-state PATH \
  --observation-surface PATH \
  --output-dir OUT \
  [--canonical-state-report PATH] \
  [--observation-surface-report PATH]
```

### Fixtures and tests

- `tests/fixtures/m19/`
- `tests/test_observation_reconciliation_pipeline.py`

Use fixture-backed goldens only. No live SC2. No replay parsing in M19 modules.

### Governance

Update on closeout:

- `docs/starlab.md`
- `tests/test_governance.py`
- `docs/company_secrets/milestones/M19/` artifacts
- `docs/company_secrets/milestones/M20/` stubs only

## Out of scope

Do **not** add any of the following in M19:

- replay parsing
- M14 bundle loading in M19 observation modules
- `s2protocol` imports in M19 observation modules
- full SC2 action legality
- new mask-generation semantics beyond audit classification
- benchmark integrity / leaderboard claims
- replay↔execution equivalence
- certified fog-of-war truth
- exact banked resource truth beyond prior bounded claims
- multi-frame tensors or sequences
- live SC2 in CI
- M20 product code

## Required audit semantics

### 1. Identity / provenance checks

Must reconcile:

- `gameloop`
- `perspective_player_index`
- `source_canonical_state_sha256` when present
- optional report hash cross-checks
- optional warning propagation from upstream reports

These are hard-fail conditions when contradictory.

### 2. Scalar feature audit

For each observation scalar entry, record:

- observation feature name
- canonical source path(s)
- reconciliation status
- rationale / transformation note

### 3. Entity-row audit

Audit only what M18 actually materializes: `self` aggregated-category rows; `enemy` aggregated-category rows when M16 supports them. No fabricated neutral truth.

### 4. Spatial-plane audit

Audit structural presence, deterministic metadata alignment, prototype status — **not** semantic terrain/control correctness.

### 5. Action-mask audit

Audit coarse prototype families only: family presence/order, bounded upstream signals used; classify as prototype / non-legal — **not** legality claims.

### 6. Summary verdict

The report should include:

- `pass` when identities/provenance reconcile and no unexpected mismatches exist
- `pass_with_warnings` when only expected bounded-loss / unavailable-by-design items appear
- `fail` when there is a provenance, identity, or unexpected mapping mismatch

## Suggested artifact shape

### `observation_reconciliation_audit.json`

Top-level sections:

- `audit_metadata`
- `source_identity`
- `scalar_audit_rows`
- `entity_audit_rows`
- `spatial_audit_rows`
- `action_mask_audit_rows`
- `status_counts`
- `deferred_non_claims`

### `observation_reconciliation_audit_report.json`

Top-level sections:

- `report_version`
- `audit_verdict`
- `failures`
- `warnings`
- `upstream_warnings`
- `summary`

## Deterministic ordering rules

- scalar audit rows ordered by M17 scalar catalog order
- entity audit rows ordered to mirror emitted observation order
- spatial audit rows ordered by plane-family / channel order
- action-mask audit rows ordered by M17 family order
- failures and warnings sorted lexicographically by stable key tuple

## Failure conditions

M19 CLI should exit non-zero for:

- invalid JSON
- invalid canonical/observation schema inputs
- gameloop mismatch
- perspective mismatch
- optional report hash mismatch
- unexpected audit `mismatch`
- emitted audit artifact validation failure

M19 CLI should **not** fail merely because a field is `bounded_lossy` or `unavailable_by_design` when that behavior is explicitly allowed by the contract.

## Acceptance criteria

M19 is complete only when all of the following are true:

- runtime contract exists and is scope-bounded
- CLI emits both audit artifacts deterministically
- audit artifacts are validated in tests
- audit classifies exact/derived/bounded_lossy/unavailable_by_design/mismatch
- hard identity/provenance mismatches fail deterministically
- expected prototype limitations produce warnings, not inflated claims
- fixture-backed tests and goldens exist under `tests/fixtures/m19/`
- M19 observation modules do **not** import replay parsing or `s2protocol`
- `ruff`, `format`, `mypy`, and `pytest` are green locally
- authoritative PR-head CI is green
- merge-boundary `main` CI is green
- `docs/starlab.md` is updated at closeout
- M20 is stubbed only, with no M20 product code

## Copy-paste handoff block

```md
# M19 Plan — Cross-Mode Reconciliation & Representation Audit

Objective:
Prove a narrow, deterministic reconciliation/audit layer between one M16 `canonical_state.json` and one M18 `observation_surface.json` for the same `gameloop` and `perspective_player_index`, producing deterministic audit artifacts that classify representation mappings as exact / derived / bounded_lossy / unavailable_by_design / mismatch, without expanding Phase III claims into legality, benchmark, replay-equivalence, or live-SC2 territory.

In scope:
- `docs/runtime/observation_reconciliation_audit_v1.md`
- `starlab/observation/observation_reconciliation_inputs.py`
- `starlab/observation/observation_reconciliation_rules.py`
- `starlab/observation/observation_reconciliation_pipeline.py`
- `starlab/observation/audit_observation_surface.py`
- CLI to emit:
  - `observation_reconciliation_audit.json`
  - `observation_reconciliation_audit_report.json`
- Fixtures/goldens under `tests/fixtures/m19/`
- `tests/test_observation_reconciliation_pipeline.py`
- governance/doc updates at closeout only

Out of scope:
- replay parsing
- M14 bundle loading in M19 observation modules
- `s2protocol` in M19 observation modules
- full action legality
- benchmark integrity claims
- replay↔execution equivalence
- certified fog-of-war truth
- multi-frame tensors
- live SC2 in CI
- M20 product code
```
