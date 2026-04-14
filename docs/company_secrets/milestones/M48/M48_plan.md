# M48 Plan — Learned-Agent Comparison Contract-Path Alignment

**Milestone:** M48  
**Phase:** VI — Governed Agent Training, Comparison, and Local Validation  
**Branch (implementation):** `m48-learned-agent-comparison-contract-path-alignment`  
**Status:** **Closed** on `main` — merge commit `cdd023cb388ae99c3649978857e07af04c17df50` ([PR #59](https://github.com/m-cahill/starlab/pull/59)); see `M48_run1.md` / `M48_summary.md` / `M48_audit.md`.

**Deferred from:** Prior **M47** stub topic (recharter **2026-04-13**); **M47** closed as **Bootstrap Episode Distinctness & Operator Ergonomics** — see `docs/starlab.md` §23.

---

## 1. Problem statement

**M42** (`starlab.evaluation.emit_learned_agent_comparison`) compares **M27** and **M41** candidates on the shared **M28** offline metric surface. Two different **contract** surfaces are involved:

| Surface | Role | Typical artifact |
| ------- | ---- | ---------------- |
| **M20** | Benchmark contract JSON used by **M28** / **M42** for metric definitions and validation (`_validate_m28_benchmark_contract`) | User-supplied JSON; CLI flag `--contract` loads this **from disk** |
| **M40** | Training-program charter (`agent_training_program_contract` semantics) — program posture, allowed upstreams, non-claims | Today **built in-process** via `build_agent_training_program_contract()`; **not** loaded from the operator’s on-disk `agent_training_program_contract.json` |

**Mismatch:**

1. **Operator confusion:** The CLI flag name **`--contract`** and runtime doc phrasing point to the **M20 benchmark** path, while Phase VI language often says “contract” for the **M40** charter. That overloads one word for two governed documents.
2. **Binding gap:** **M41** run JSON records `training_program_contract_sha256` / `training_program_contract_version` from the contract object used at training time (defaults to `build_agent_training_program_contract()`). **M42** always rebuilds the M40 contract in-process for the emitted comparison. If an operator compares runs that were produced against a **specific on-disk** M40 JSON (or expects strict identity with the M41-recorded SHA), the current harness does not accept an explicit **M40 file path** or **fail-closed** check that “comparison M40 == each M41 run’s recorded charter identity.”
3. **Governance / audit:** For enterprise-grade traceability, comparison artifacts should make it **obvious** which **M20 benchmark** and which **M40 charter** identities were used, and **whether** they match the **M41** candidates’ recorded `training_program_contract_sha256` (policy: warn vs error — to be chosen in implementation, defaulting to **strict** where safety is higher).

**Prior art in repo:** `docs/diligence/m44_bounded_live_final_status_recharter.md` §1 explicitly lists the **M42 `--contract` path** issue (M40 charter JSON vs M20 benchmark contract) as **out of scope** for M46 — that follow-on is **this milestone**.

---

## 2. Narrow scope (in)

- **CLI & naming:** Introduce an unambiguous flag for the **M20 benchmark contract** file (e.g. `--benchmark-contract`, retaining `--contract` as a **deprecated alias** for one milestone with stderr warning, or document-only change if alias is too noisy — **prefer** dual support + tests).
- **Optional M40 path:** Add `--training-program-contract` (Path, optional) to load **M40** charter JSON from disk; if omitted, preserve current behavior (`build_agent_training_program_contract()`).
- **Consistency checks:** When **M41** candidates are present, validate loaded M40 charter SHA/version against each run’s `training_program_contract_sha256` / `training_program_contract_version` (exact policy in implementation: **fail** vs **warn**; document in runtime doc and `non_claims`).
- **Artifacts:** Ensure `learned_agent_comparison.json` continues to record both benchmark and training-program identities clearly (field names already separate; adjust only if a governance gap is found).
- **Documentation:** Update `docs/runtime/learned_agent_comparison_harness_v1.md` and cross-references in `docs/runtime/agent_training_program_contract_v1.md` / `docs/runtime/benchmark_contract_scorecard_v1.md` so **M20 vs M40** is unmistakable.
- **Tests:** Extend `tests/test_m42_learned_agent_comparison.py` (fixtures) for new flags and mismatch behavior.

---

## 3. Out of scope (explicit non-claims)

- **Not** benchmark integrity, stronger M28 metrics, or new scorecard semantics (**M20** family unchanged except binding clarity).
- **Not** changing **M41** training algorithm, weights format, or **M43+** pipelines.
- **Not** live SC2, replay↔execution equivalence, ladder claims.
- **Not** reopening **M47** (episode distinctness / bootstrap ergonomics).
- **Not** large refactors of `starlab.evaluation` beyond the contract-path binding.

---

## 4. Likely files / surfaces to touch

| Area | Paths |
| ---- | ----- |
| CLI | `starlab/evaluation/emit_learned_agent_comparison.py` |
| Harness | `starlab/evaluation/learned_agent_comparison_harness.py` (`write_learned_agent_comparison_from_paths`, validation helpers) |
| Runtime docs | `docs/runtime/learned_agent_comparison_harness_v1.md`, small cross-links in `agent_training_program_contract_v1.md`, `benchmark_contract_scorecard_v1.md` |
| Tests | `tests/test_m42_learned_agent_comparison.py` |
| Ledger (at **closeout only**) | `docs/starlab.md` §6–§8, §11, §7 row M48, §18, §23 — **not** in this planning pass on `main` |

---

## 5. Acceptance criteria

1. **Unambiguous inputs:** Operators can specify **M20 benchmark contract** and (optionally) **M40 training-program contract** paths without naming collision; help text and runtime doc match behavior.
2. **Traceability:** Emitted comparison JSON/reports remain deterministic and record **benchmark** and **training-program** identities; M41 **SHA/version** consistency is enforced or warned per documented policy.
3. **Backward compatibility:** Existing scripts using `--contract` for the M20 file **continue to work** (alias or unchanged primary name with added long-form flag).
4. **CI:** Full `ruff check`, `ruff format`, `mypy`, `pytest` green; **no** new live SC2 or GPU requirements.
5. **Governance:** Milestone closeout (when chartered) updates ledger + secret milestone artifacts per project rules.

---

## 6. Validation expectations

- Local: run M42 emitter against existing fixture layout in tests; add cases for optional M40 path + mismatch.
- CI: existing **quality** / **smoke** / **tests** / **governance** lanes unchanged in intent.

---

## 7. CI / governance risks

| Risk | Mitigation |
| ---- | ---------- |
| **Ruff format** drift on multiline argparse | Run `ruff format` on touched Python before push; match project line-length conventions |
| **Governance tests** (`test_governance_*.py`) if §7 M48 row flips to “In progress” | Update only on **closeout** branch / PR; avoid gratuitous `starlab.md` edits mid-implementation |
| **Alias deprecation noise** | Prefer additive flags first; deprecation warnings only if explicitly approved |

---

## 8. Guardrails (avoid needless churn)

- Prefer **one** focused PR for M48 product + tests; batch **ledger** updates with closeout unless governance requires early “In progress” (follow existing M46/M47 patterns).
- **Do not** touch `out/` in commits; keep fixtures under `tests/` / `testdata` conventions.
- Run **ruff format** + **pytest** locally before pushing to reduce red **quality** runs on `main`.

---

## 9. Future closeout workflow (when M48 closes — do not execute now)

When closing **M48** on `main`, the operator / Cursor run should:

1. Create **`M48_summary.md`** using `docs/company_secrets/prompts/summaryprompt.md` (if present in repo; otherwise follow the same structure as prior milestones).
2. Create **`M48_audit.md`** using `docs/company_secrets/prompts/unifiedmilestoneauditpromptV2.md`.
3. Use `docs/company_secrets/prompts/workflowprompt.md` for **workflow-run / CI** analysis when applicable.
4. **Ensure all documentation** (`docs/starlab.md`, runtime docs touched in M48, README pointers if any) is updated coherently with merge + CI evidence.

---

## 10. Readiness checklist (pre-implementation)

- [ ] Branch `m48-learned-agent-comparison-contract-path-alignment` checked out from current `main`
- [ ] This plan reviewed against `learned_agent_comparison_harness_v1.md` + `emit_learned_agent_comparison.py` once more at implementation time
- [ ] Policy chosen: **fail** vs **warn** on M41 vs M40 charter mismatch (record in plan at implementation kickoff)
