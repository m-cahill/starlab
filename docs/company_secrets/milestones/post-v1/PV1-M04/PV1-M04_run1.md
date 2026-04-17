# PV1-M04 — CI / workflow analysis (run 1)

**Milestone:** PV1-M04 — Post-Campaign Analysis / Comparative Readout  
**Mode:** Open-milestone implementation merge (**not** milestone closeout)

---

## 1. Workflow identity

| Field | Value |
| --- | --- |
| **Workflow** | `CI` (`.github/workflows/ci.yml`) |
| **PR** | [PR #79](https://github.com/m-cahill/starlab/pull/79) — `docs(governance): add PV1-M04 post-campaign comparative readout` |
| **Trigger** | `pull_request` (feature branch), then `push` to `main` (merge boundary) |
| **Final PR head SHA** | `819cc2ea57b1fe3d27d09296aaebf6008577560c` |
| **Merge commit (`main`)** | `d5280ee9cc69f8d7750546b7ed597e2de466f8a7` |

---

## 2. Authoritative PR-head run(s)

| Run ID | Result | Notes |
| --- | --- | --- |
| [`24548939513`](https://github.com/m-cahill/starlab/actions/runs/24548939513) | **success** | **Authoritative** — final branch head after coverage repair commit. Jobs: quality, smoke, tests+coverage, flagship, fieldtest, security, governance — **all passed**. |
| [`24548853149`](https://github.com/m-cahill/starlab/actions/runs/24548853149) | **failure** | **Superseded** — `tests` job: branch-aware **TOTAL** coverage **77.99%** vs required **78.0%** (`fail_under` in `pyproject.toml`). Root cause: new **`emit_pv1_post_campaign_readout.py`** CLI had **0%** line coverage in full-suite run. **Not** merge authority. |

**Repair:** Added tests invoking `emit_readout_main()` success + error paths in `tests/test_pv1_post_campaign_readout.py` — total coverage **~78.3%** locally; CI **green** on [`24548939513`](https://github.com/m-cahill/starlab/actions/runs/24548939513).

---

## 3. Merge-boundary `main` run

| Run ID | Result |
| --- | --- |
| [`24548992189`](https://github.com/m-cahill/starlab/actions/runs/24548992189) | **success** — push to `main` from merge of PR #79 |

---

## 4. Job inventory (authoritative PR-head)

| Job | Merge-blocking | Result |
| --- | --- | --- |
| quality (Ruff + Mypy) | yes | pass |
| smoke | yes | pass |
| tests + coverage | yes | pass |
| flagship | yes | pass |
| fieldtest | yes | pass |
| security | yes | pass |
| governance (aggregate) | yes | pass |

**Informational:** Node.js 20 deprecation annotations on actions — not a failing signal in this run.

---

## 5. Verdict

- **CI:** **Green** on authoritative PR head and on merge-boundary `main`.
- **PR #79:** **Merged** to `main`.
- **Merge-ready:** **Yes** after coverage repair; no further fix required for this milestone scope.

---

## 6. Explicit scope

- **PV1-M04** remains **open** on `main` — this run is **not** milestone closeout (no `PV1-M04_summary.md` / `PV1-M04_audit.md` as closed artifacts).
- **No new execution evidence**; bounded campaign truth unchanged (**Tranche A/B within scope**; **`threshold-not-met`**).

