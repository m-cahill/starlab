# PX1-M00 — CI / workflow analysis (run 2 — closeout)

**Milestone:** PX1-M00 — Full Industrial Run & Demonstration Charter — **governance closeout** only ([PR #84](https://github.com/m-cahill/starlab/pull/84)).  
**Not** operator execution; **not** demo recording; **does not** open **PX1-M01** or **v2**.

---

## 1. Workflow identity

| Field | Value |
| --- | --- |
| Workflow | `CI` (`.github/workflows/ci.yml`) |
| **Authoritative PR-head run** | [`24587637877`](https://github.com/m-cahill/starlab/actions/runs/24587637877) — **success** |
| **Superseded run** | [`24587630071`](https://github.com/m-cahill/starlab/actions/runs/24587630071) — **cancelled** (superseded when a newer commit was pushed to the same PR ref) |
| Trigger | `pull_request` |
| Branch | `px1-m00-closeout-governance` |
| **Final PR head SHA** | `d41849b469cef1f60ff367fe6ab7985b6d2b5bb5` |
| PR | [#84](https://github.com/m-cahill/starlab/pull/84) |

---

## 2. Job inventory (authoritative run)

All jobs **completed successfully** on run `24587637877`:

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

- **CI:** **Green** on **final** PR head `d41849b…`.  
- **Merge-ready:** **Yes** (pending maintainer merge) — **no** corrective code change indicated by this run.  
- **Superseded run** `24587630071` is **not** merge authority — treat as **cancelled** due to concurrent PR ref update.

---

## 4. Post-merge (to record after merge to `main`)

After merge, append one line:

- **Merge commit SHA** on `main`  
- **Merge-boundary `main` CI** run ID + URL (push to `main` after merge)
