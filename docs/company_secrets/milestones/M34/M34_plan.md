# M34 Plan — Audit Closure III: Structural Hygiene, Deferred-Issue Closure, and Operating Manual Promotion Prep

## Milestone identity

| Field | Value |
| ----- | ----- |
| **Milestone** | M34 |
| **Name** | Audit Closure III — Structural Hygiene, Deferred-Issue Closure, and Operating Manual Promotion Prep |
| **Phase** | V — Learning Paths, Evidence Surfaces, and Flagship Proof |
| **Recommended branch** | `m34-audit-closure-iii-structural-hygiene-manual-prep` |

## Goal

Structural-hygiene and diligence closure: shared I/O extraction where appropriate, governance test split / maintainability, dependency automation posture, deferred-issue closure that belongs in this tier, and **prep** for operating-manual promotion — **without** flagship proof-pack product work.

## What M34 must not claim

- **M35** public flagship proof pack completion  
- Benchmark integrity or leaderboard validity  
- Live SC2 in CI  
- Operating manual promoted to canonical **v1** (M34 is **prep** unless explicitly scoped otherwise)  
- Replay↔execution equivalence  

## Deliverables (see repo)

- `starlab/_io.py`, migrated callers, governance split (`tests/test_governance_*.py`), `tests/test_m34_audit_closure.py`, `.github/dependabot.yml`, `pyproject.toml` dev caps, `docs/diligence/operating_manual_promotion_readiness.md`, `docs/audit/broad_exception_boundaries.md`, registry + `docs/starlab.md` updates.

## Acceptance criteria

1. Single shared JSON helper; duplicated DIR-003 tuple loaders removed or wrapped.  
2. `test_governance.py` replaced by split modules; coverage intent preserved.  
3. DIR-005: documentation/validation closure documented.  
4. DIR-006: caps + Dependabot.  
5. Manual prep doc states v0 non-canonical status.  
6. CI topology unchanged (`CI` / `governance`); `fail_under = 75.4`.

## Status

**Complete on branch** — merge evidence (PR, SHAs, tag `v0.0.34-m34`) **TBD** at merge; see `M34_run1.md`, `M34_summary.md`, `M34_audit.md`.
