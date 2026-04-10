# STARLAB Operating Manual (v0 draft)

**Status:** Draft / non-canonical operating manual scaffold — **subordinate** to `docs/starlab.md` and `docs/runtime/*` contracts until a later promotion milestone.  
**Authority:** Do not override the ledger or runtime contracts with this document.

---

## 1. Executive identity

STARLAB is a **governed, replay-native RTS research lab** (StarCraft II first) producing deterministic JSON artifacts, schemas, and CI-backed evidence — see `docs/starlab-vision.md` and `docs/starlab.md`.

## 2. What STARLAB is / is not

- **Is:** Milestone-driven substrate, artifact-first, benchmark posture without overclaiming.  
- **Is not:** A ladder bot product, consumer game mod, or implied “strongest agent” program.

## 3. Core mental model

**Runs → lineage → replay-derived planes → state → observation → evaluation surfaces.** External SC2/parser stacks are **untrusted boundaries**; owned claims are on STARLAB artifacts and tests.

## 4. Architecture overview

See `docs/architecture.md` for packages and boundaries.

## 5. Installation and quick reference

See `docs/getting_started_clone_to_run.md` and repository `Makefile` targets (`install-dev`, `lint`, `typecheck`, `test`, `smoke`, `coverage`, `audit`, `fieldtest`).

## 6. Clone-to-run smoke procedure

See `docs/runtime/clone_to_run_smoke_v1.md`.

## 7. Common failure modes / debugging

- **Python version:** Use 3.11 only (`pyproject.toml` pin).  
- **Missing dev extras:** Re-run `pip install -e ".[dev]"`.  
- **Smoke vs full suite:** Use `pytest -m smoke` for a fast lane; full `pytest` for merge parity.

## 8. Governance and authority hierarchy

Per `docs/starlab.md` §2: vision → BICETB → this ledger → README → code.

## 9. Frozen vs changing surfaces

Artifact schemas and runtime contracts change **only** under milestone governance; watch `docs/starlab.md` changelog and `docs/audit/DeferredIssuesRegistry.md`.

## 10. Field-test checklist

See `docs/diligence/field_test_checklist.md`.

## 11. Extension guidance

Add new artifact planes behind explicit milestones; keep adapters isolated; extend tests and ledger in the same milestone.

## 12. Source-of-truth references

- `docs/starlab.md`  
- `docs/bicetb.md`  
- `docs/runtime/*.md`  
- `docs/audit/DeferredIssuesRegistry.md`
