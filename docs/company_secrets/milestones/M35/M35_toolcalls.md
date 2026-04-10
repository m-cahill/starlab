# M35 toolcalls log

---

## Implementation branch (PR #46)

| Commit | Summary |
| ------ | ------- |
| `c02eec6` | feat(M35): structural decoupling, module splits, 40-milestone ledger arc |
| `d3a47f9` | style(M35): ruff format m14_bundle_loader (CI quality gate) |
| `91e45dd` | fix(M35): export load_json_object in dataset_views __all__ (mypy tests) |

### Superseded PR-head CI (not merge authority)

* [`24264929015`](https://github.com/m-cahill/starlab/actions/runs/24264929015) — Ruff format failure → fixed by `d3a47f9`
* [`24264963434`](https://github.com/m-cahill/starlab/actions/runs/24264963434) — Mypy failure → fixed by `91e45dd`

### Authoritative PR-head CI

* [`24265022396`](https://github.com/m-cahill/starlab/actions/runs/24265022396) — success on `91e45dd…`

### Merge + tag

* Merge commit: `5b4d24b0eca578b70f2963f1561b99bc89fef033` — [PR #46](https://github.com/m-cahill/starlab/pull/46)
* Merge-boundary `main` CI: [`24265056432`](https://github.com/m-cahill/starlab/actions/runs/24265056432) — success
* Tag: **`v0.0.35-m35`** on merge commit

### Closeout (ledger + milestone docs on `main`)

* This commit updates `docs/starlab.md`, `M35_plan.md` (closeout block), `M35_run1.md`, `M35_summary.md`, `M35_audit.md`, `M35_toolcalls.md` (this file), and `tests/test_governance_ci.py` (current milestone = M36).

---

Stub created at **M34** closeout — superseded by implementation and merge above.
