# M36 Plan — Audit Closure V: Governance Surface Rationalization and Documentation Density Control

## Milestone identity

- **Milestone:** M36
- **Name:** **Audit Closure V — Governance Surface Rationalization and Documentation Density Control**
- **Phase:** V — Learning Paths, Evidence Surfaces, and Flagship Proof
- **Branch:** `m36-audit-closure-v-governance-surface-rationalization-doc-density-control`

## Why this milestone exists

Post-M35 structural work reduced code-level audit drag; remaining friction is largely **documentation and governance surface density** (ledger length, repetitive milestone assertions, duplicated boilerplate). M36 is the **second** of two pre-flagship corrective milestones (after M35), intended to **reduce overhead without weakening** truthfulness, CI discipline, or auditability.

This is **not** Public Flagship Proof Pack (M37) work.

## In scope

### 1. Rationalize `docs/starlab.md` density

- Move older **§7 milestone table notes** (M01–M27) verbatim to `docs/starlab_archive.md`.
- Keep `docs/starlab.md` authoritative: milestone table, archival policy sentence, full inline notes for **M28–M35** (recent audit-closure + Phase V proof boundaries), and all other ledger obligations unchanged.
- **Do not** delete important history; **do not** reduce the ledger to “table + pointer only.”

### 2. Reduce governance surface overhead (bounded)

- Consolidate repetitive patterns in `tests/test_governance_milestones.py` and remove obvious duplication in `tests/test_governance_runtime.py` (e.g. duplicate fixture assertions).
- **Do not** rewrite test architecture; preserve coverage intent.

### 3. Documentation density control

- Centralize repeated explanations where the value is clear (archive + pointer).
- Optional: short guardrails in governance tests so `docs/starlab_archive.md` and ledger cross-references stay aligned.

### 4. Closeout hygiene (light touch)

- §23 changelog entry for this branch’s governance/doc changes.
- **Do not** add bureaucracy for its own sake.

## Explicit non-goals

- No **M37 Public Flagship Proof Pack** product code
- No benchmark-integrity claim upgrades
- No live SC2 in CI
- No operating manual v1 promotion
- No broad architecture rewrite
- No replay/data provenance expansion unless needed for audit clarity
- No license overhaul (unless a tiny doc clarification is strictly necessary)
- No weakening of milestone evidence or CI truthfulness
- **Do not** modify `docs/company_secrets/prompts/*` except a tiny fix that blocks workflow (default: leave as-is)
- **Do not** edit or rewrite `M35_fullaudit.md` / `M35_fullaudit.json`

## Deliverables (this implementation branch)

- `docs/starlab_archive.md`
- Tightened `docs/starlab.md` §7 / §11 / §10 (Phase V row) / §23 as appropriate
- Focused governance test updates (`test_governance_milestones.py`, `test_governance_runtime.py`, `test_governance_docs.py`)
- This plan + `M36_toolcalls.md` updated

## Closeout artifacts (after merge to `main`)

- `M36_run1.md`, `M36_summary.md`, `M36_audit.md`
- Final ledger updates per normal milestone closeout
- Workflow report per `docs/company_secrets/prompts/workflowprompt.md`

## Acceptance criteria

1. `docs/starlab.md` is materially more readable as a current-state ledger.
2. Historical milestone truth is preserved in `docs/starlab_archive.md` or remains in the ledger where kept inline.
3. Governance/doc duplication is reduced without weakening evidence posture.
4. Governance tests remain truthful and green.
5. CI topology and required checks remain unchanged and truthful.
6. Coverage floor **75.4** is preserved or improved (do **not** lower the configured gate).
7. No M37 product work was added.
8. Ledger still records: M35 closed on `main`; M36 current; M37 after M36; 40-milestone arc (M00–M39) intact.

## Validation (local)

Run at minimum:

- `ruff check starlab tests`
- `ruff format --check starlab tests`
- `mypy starlab tests`
- `pytest -q -m smoke`
- `pytest -q`
- `pytest -q --cov=starlab`
- `make fieldtest`

## Status

- **Complete** on `main` — see **Closeout** below.

---

## Closeout (merged to `main`)

- **PR:** [#47](https://github.com/m-cahill/starlab/pull/47)
- **Final PR head SHA:** `63fe1168e8a4bb7961948526589aba3c0a01c9ba`
- **Authoritative PR-head CI:** [`24266877684`](https://github.com/m-cahill/starlab/actions/runs/24266877684) — success
- **Merge commit:** `e73a53b28a4b6eeb3a2c19dd358d928c64806e89`
- **Merge-boundary `main` CI:** [`24266906173`](https://github.com/m-cahill/starlab/actions/runs/24266906173) — success
- **Tag:** `v0.0.36-m36` on merge commit
- **Superseded PR-head (not merge authority):** none recorded on final head
- **Closeout docs:** `M36_run1.md`, `M36_summary.md`, `M36_audit.md`
- **Post-merge doc closeout:** ledger + milestone artifacts may land in additional `main` commits after the merge commit — **not** substitute CI authority for the M36 implementation merge (authoritative remains **`24266877684`** + **`24266906173`**).
- **Current program stub milestone:** **M37** (see `docs/starlab.md` §7 / §11).
