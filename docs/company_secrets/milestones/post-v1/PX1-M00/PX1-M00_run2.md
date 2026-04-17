# PX1-M00 — CI / workflow analysis (run 2 — closeout)

**Milestone:** PX1-M00 — Full Industrial Run & Demonstration Charter — **governance closeout** only ([PR #84](https://github.com/m-cahill/starlab/pull/84)).  
**Not** operator execution; **not** demo recording; **does not** open **PX1-M01** or **v2**.

---

## 1. Workflow identity

| Field | Value |
| --- | --- |
| Workflow | `CI` (`.github/workflows/ci.yml`) |
| **Authoritative PR-head run** | [`24587707730`](https://github.com/m-cahill/starlab/actions/runs/24587707730) — **success** (final branch head incl. this `PX1-M00_run2.md`) |
| **Superseded runs** | [`24587637877`](https://github.com/m-cahill/starlab/actions/runs/24587637877) — **success** but **superseded** by newer push; [`24587630071`](https://github.com/m-cahill/starlab/actions/runs/24587630071) — **cancelled** (first push, superseded) |
| Trigger | `pull_request` |
| Branch | `px1-m00-closeout-governance` |
| **Final PR head SHA** | `85a1e5293bc75d59663410963a991d0c9312b701` |
| PR | [#84](https://github.com/m-cahill/starlab/pull/84) |

---

## 2. Job inventory (authoritative run)

All jobs **completed successfully** on run `24587707730`:

| Job | Required (merge gate) | Result |
| --- | --- | --- |
| `quality` | yes | success (Ruff check, Ruff format, Mypy) |
| `smoke` | yes | success |
| `tests` | yes | success (pytest + coverage gate) |
| `security` | yes | success |
| `fieldtest` | yes | success |
| `flagship` | yes | success |
| `governance` | yes | success (aggregate) |

**Noise:** Node.js 20 deprecation notices on several actions — **not** failures; no merge impact.

---

## 3. Verdict

- **CI:** **Green** on **final** PR head (incl. `PX1-M00_run2.md`).  
- **Merge-ready:** **Yes** (pending maintainer merge) — **no** corrective code change indicated by this run.  
- **Superseded** runs `24587630071` / `24587637877` are **not** final merge authority for the closeout PR head.

---

## 4. Post-merge (to record after merge to `main`)

After merge, append one line:

- **Merge commit SHA** on `main`  
- **Merge-boundary `main` CI** run ID + URL (push to `main` after merge)
