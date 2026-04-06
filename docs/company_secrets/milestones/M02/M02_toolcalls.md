# M02 toolcalls log

Initialize when M02 work begins.

---

## 2026-04-06 — Session start (implementation)

- **Tool:** Write — **Purpose:** Initialize M02 toolcalls log with session start entry for milestone implementation. **Files:** `docs/company_secrets/milestones/M02/M02_toolcalls.md`

---

## 2026-04-06 — M02 harness implementation committed

- **Git:** branch `m02-deterministic-match-execution-harness`, commit `M02: deterministic match harness, proof artifact, BurnySc2 adapter`
- **Deliverables:** `docs/runtime/match_execution_harness.md`, `starlab/sc2/{match_config,maps,artifacts,harness,run_match}.py`, `starlab/sc2/adapters/{fake,burnysc2_adapter}.py`, tests, ledger/README/environment_lock updates, M02 evidence templates under `docs/company_secrets/milestones/M02/`.
- **Next (human):** local `burnysc2` runs ×2, fill `M02_local_execution_note.md`, `M02_determinism_check.md`, redacted proof JSON; then PR + CI + closeout per workflow.

---

## 2026-04-06 — M02 plan confirmation

- **`M02_plan.md`:** Confirmed **full approved plan** present (not a stub); objective, scope, guardrails, acceptance criteria, and BurnySc2 adapter posture are recorded.

---

## 2026-04-06 — Pre-push verification (merge-readiness gate)

**Branch:** `m02-deterministic-match-execution-harness`  
**Commit SHA (pre–closeout-prep verification):** `888407868cbdd00ca124e2b496f9ca14f909b0fc`  
**Commit SHA (current PR tip after ledger alignment):** `c03691b61b8d11aafda55f866232f6d623c70628`

| Command | Result |
|---------|--------|
| `python -m ruff check .` | **All checks passed** (exit 0) |
| `python -m ruff format --check .` | **20 files already formatted** (exit 0) |
| `python -m mypy starlab tests` | **Success: no issues found in 20 source files** (exit 0) |
| `python -m pytest` | **44 passed** (exit 0) |
| `python -m starlab.sc2.run_match --help` | Help rendered; **exit 0** (CI-safe CLI surface) |

**Platform note:** Commands run on **Windows** (developer machine); CI authoritative gate is **ubuntu-latest** (see PR-head run below).

---

## 2026-04-06 — Push & PR

| Field | Value |
|-------|--------|
| Branch | `m02-deterministic-match-execution-harness` |
| PR | **#3** — https://github.com/m-cahill/starlab/pull/3 |
| Title | M02: deterministic match execution harness |
| PR head SHA | `c03691b61b8d11aafda55f866232f6d623c70628` |

---

## 2026-04-06 — Authoritative PR-head CI (merge gating) — **single reference**

| Field | Value |
|-------|--------|
| Workflow | **CI** (`.github/workflows/ci.yml`) |
| Run ID (authoritative, current tip) | **24054586191** |
| URL | https://github.com/m-cahill/starlab/actions/runs/24054586191 |
| Event | `pull_request` |
| Head SHA | `c03691b61b8d11aafda55f866232f6d623c70628` |
| Conclusion | **success** |
| Authoritative for merge? | **Yes** — green run on latest PR tip (verified `gh run list` / `gh pr view 3`) |

**Earlier PR-head runs (older tips; not the current ledger contract):** `24054529734` on `5ec0ccb…`; `24053526611` on `061c212…`; `24053475644` on `bfab038…`; `24053430560` on `3952c40…`; `24053381609` on `08fb582…`; `24053317502` on `10a2b13…`; `24053264747` on `22b2b57…`; `24053218335` on `d80ae12…`; `24052325999` on `f457cf5…`; `24052291273` on `79b341a…`; `24052230417` on `5f5c8a5…`; `24052172714` on `59dcf15…`; `24052112581` on `1bd98f1…`; `24052043305` on `8884078…`.

**Analysis document:** `M02_run1.md`

**Local evidence gap (Case B):** Real SC2 runs **not** performed in CI; `M02_local_execution_note.md` / `M02_determinism_check.md` / redacted proof JSON remain **PENDING** until human completes burny×2 locally.

---

## 2026-04-06 — Local evidence session (burnysc2; blocked — no map file)

**Branch:** `m02-deterministic-match-execution-harness`  
**HEAD at session start (before evidence commit):** `1ce6b42f0e2bc5e2e0470e552d3cf038cafad579`

### Optional harness install

| Command | Result |
|---------|--------|
| `python -m pip install -e ".[sc2-harness]"` | **Exit 0** — editable install; `burnysc2` already present (7.2.1) |

### SC2 environment

| Step | Result |
|------|--------|
| `STARLAB_SC2_ROOT` | Set to standard Windows x86 install root for the session |
| `python -m starlab.sc2 --redact` | JSON: `root` + `binary` **present**; `maps_dir` **not** present on disk (`present.maps_dir`: false); `base_build` / `data_version`: null |

**Note:** CLI is `python -m starlab.sc2` (JSON always; `--redact` for path redaction). There is no separate `env_probe` module entry — probe lives under `starlab.sc2`.

### Config (committed)

- **File:** `docs/company_secrets/milestones/M02/m02_local_config.json`
- **Map mode:** `explicit_path` — `…/Maps/Tutorial/Tutorial01.SC2Map` under install root

### Harness runs (same config, two output dirs)

| Run | Command | Result |
|-----|---------|--------|
| 1 | `python -m starlab.sc2.run_match --config docs/company_secrets/milestones/M02/m02_local_config.json --output-dir docs/company_secrets/milestones/M02/_local_runs/run1` | **Exit 2** — `configured map path not found` |
| 2 | same `--config`; `--output-dir` …`/run2` | **Exit 2** — same error |

**Proof files:** none written. **`_local_runs/`** is gitignored.

### Hash comparison

- **Not applicable** — no `artifact_hash` values produced.

### Evidence files updated

- `M02_local_execution_note.md`, `M02_determinism_check.md`, `M02_execution_proof_redacted.json` — **truthful blocked session** (not a successful determinism proof).

### Follow-up commits (same day)

- **`5ec0ccb…`** — `docs(m02): add local execution evidence and determinism record` (evidence + `m02_local_config.json` + `.gitignore` for `_local_runs/`).
- **`c03691b…`** then tip bump — ledger rows aligned to current PR head + green CI (see authoritative table below).

---

## 2026-04-06 — Case B: ledger alignment to latest PR-head CI (no merge)

- **Tool:** Write — **Purpose:** Align `docs/starlab.md` §11 + §23, `M02_run1.md`, `M02_summary.md`, `M02_audit.md`, `M02_toolcalls.md`, and `docs/runtime/match_execution_harness.md` to authoritative pair **PR head** `f457cf54bb9e49a991de7605bc0c2c87b97c9c6a` + **CI** run `24052325999` (single reference; supersede stale `5f5c8a5…` / `24052230417` rows). **Did not** merge PR #3; local real-execution evidence still **pending**.

---

## 2026-04-06 — Post-push: authoritative pair bumped to doc commit tip

- After push of doc alignment commit `d80ae12322c3d2c45c754bb298ac895a8cbe7335`, GitHub **CI** run **`24053218335`** (success) was the gate for that tip; intermediate tips included **`22b2b57654c9bc5124059227f363b27ccc63ed6f`** + **`24053264747`**, then **`10a2b13ba8115e50037948c014facaa502da6978`** + **`24053317502`**, then **`08fb582fa8fe969a02de82257d64dedfea2ff35f`** + **`24053381609`**, then **`3952c4071d82a77e633b0cd428da19caac2720ff`** + **`24053430560`**, then **`bfab038a8f7a4908a5a909131b402ba7909463da`** + **`24053475644`**. **Current** ledger row (above): **`061c2126cc59b3ce4d662c58240216343c21f71a`** + **`24053526611`**.

---

## 2026-04-06 — Case B: stop doc/CI churn; tip 061c212 + run 24053526611

- **Purpose:** Match §11 / milestone rows to **`gh pr view 3`** head **`061c2126cc59b3ce4d662c58240216343c21f71a`** and successful run **`24053526611`** (witnessed after parent commit **`061c212`**). Further doc-only commits advance the tip; use **`gh pr checks 3`** for merge if the SHA drifts again.

---
