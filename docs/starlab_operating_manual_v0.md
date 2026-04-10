# STARLAB Operating Manual (v0 draft)

**Status:** Draft / non-canonical operating manual — **subordinate** to `docs/starlab.md` and `docs/runtime/*` contracts until a later promotion milestone.  
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

See `docs/architecture.md` for packages, dependency direction, CI tier map, and validation steps.

## 5. Installation and quick reference

See `docs/getting_started_clone_to_run.md` and repository `Makefile` targets (`install-dev`, `lint`, `typecheck`, `test`, `smoke`, `coverage`, `audit`, `fieldtest`).

## 6. CI tier meanings

The **`CI`** workflow runs parallel jobs; the final **`governance`** job aggregates success. See **`docs/runtime/ci_tiering_field_test_readiness_v1.md`** for names, artifacts, and non-claims.

| Tier | Operator takeaway |
| ---- | ----------------- |
| `quality` | Fix Ruff / Mypy before re-running full suite. |
| `smoke` | Fast PR feedback; does not replace full `pytest`. |
| `tests` | Authoritative coverage + JUnit for merge parity. |
| `security` | Dependency audit, SBOM, secret scan — do not silence. |
| `fieldtest` | Fixture-only M31 explorer; uploads `out/fieldtest/` in CI. |

## 7. Clone-to-run smoke procedure

See `docs/runtime/clone_to_run_smoke_v1.md`.

## 8. Field-test operator workflow

1. Install dev deps (`make install-dev`).  
2. Run `make fieldtest` (or the equivalent `python -m starlab.explorer.emit_replay_explorer_surface …` from `docs/getting_started_clone_to_run.md`).  
3. Confirm **`replay_explorer_surface.json`** and **`replay_explorer_surface_report.json`** under `out/fieldtest/`.  
4. For diligence sessions, copy **`docs/diligence/field_test_session_template.md`** and record SHA, commands, and pass/fail.  
5. **Non-claims:** no live SC2, no benchmark integrity, no flagship proof pack — see checklist.

## 9. How to inspect field-test outputs

- **Local:** open `out/fieldtest/*.json` after `make fieldtest`.  
- **CI:** download artifact **`fieldtest-output`** from the workflow run; same JSON files are required inside.  
- **Contract:** `docs/runtime/replay_explorer_surface_v1.md`.

## 10. Smoke vs full-suite guidance

- **`make smoke`** / `pytest -q -m smoke` — bounded fast lane (~25–32 tests); use during iteration.  
- **`make test`** / `pytest -q` — full suite; must pass before merge; matches the **`tests`** CI job.  
- Do not merge on smoke alone if full suite is red.

## 11. Common CI failure triage

| Failure location | Likely cause |
| ---------------- | ------------ |
| `quality` | Formatting, lint, or type errors — run `make lint` / `make typecheck` locally. |
| `smoke` | Missing marker or broken import — run `pytest -q -m smoke -v`. |
| `tests` | Test or coverage regression — run `pytest -q --cov=starlab`; check `fail_under` in `pyproject.toml`. |
| `security` | Vulnerable dependency or secret pattern — address or document in `DeferredIssuesRegistry` with governance. |
| `fieldtest` | Explorer CLI or fixture path — run `make fieldtest` locally. |
| `governance` | One of the upstream tiers failed — inspect that job’s log first. |

## 12. Coverage gate interpretation

- Line coverage is **`fail_under`** in `[tool.coverage.report]` (`pyproject.toml`); current baseline is **75.4%** (M32).  
- **Do not** lower the threshold without ledger + `docs/audit/DeferredIssuesRegistry.md` rationale.  
- **Measured** coverage in CI is reported in `coverage.xml` artifact.

## 13. Deferred issues registry

Use **`docs/audit/DeferredIssuesRegistry.md`** to track known gaps and exit criteria. M33 may resolve **DIR-001/002/007** when CI tiering and docs land; structural items (e.g. **DIR-003–006**) remain **M34** unless trivial.

## 14. Common failure modes / debugging (local)

- **Python version:** Use 3.11 only (`pyproject.toml` pin).  
- **Missing dev extras:** Re-run `pip install -e ".[dev]"`.  
- **Smoke vs full suite:** See §10.

## 15. Governance and authority hierarchy

Per `docs/starlab.md` §2: vision → BICETB → ledger → README → code.

## 16. Frozen vs changing surfaces

Artifact schemas and runtime contracts change **only** under milestone governance; watch `docs/starlab.md` changelog and `docs/audit/DeferredIssuesRegistry.md`.

## 17. Field-test checklist

See `docs/diligence/field_test_checklist.md`.

## 18. Extension guidance

Add new artifact planes behind explicit milestones; keep adapters isolated; extend tests and ledger in the same milestone.

## 19. Source-of-truth references

- `docs/starlab.md`  
- `docs/bicetb.md`  
- `docs/runtime/*.md`  
- `docs/runtime/ci_tiering_field_test_readiness_v1.md`  
- `docs/audit/DeferredIssuesRegistry.md`
