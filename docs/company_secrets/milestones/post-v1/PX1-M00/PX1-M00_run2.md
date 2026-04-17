# PX1-M00 — CI / workflow analysis (run 2 — closeout)

**Milestone:** PX1-M00 — Full Industrial Run & Demonstration Charter — **governance closeout** only ([PR #84](https://github.com/m-cahill/starlab/pull/84)).  
**Not** operator execution; **not** demo recording; **does not** open **PX1-M01** or **v2**.

---

## 1. Workflow identity

| Field | Value |
| --- | --- |
| Workflow | `CI` (`.github/workflows/ci.yml`) |
| **Authoritative PR-head run (merge gate)** | [`24587767667`](https://github.com/m-cahill/starlab/actions/runs/24587767667) — **success** — validates **final** PR branch tip `c97da264de7669cb7cbb4de26ac772bda38aaba5` |
| **Superseded / prior PR-head runs** | [`24587707730`](https://github.com/m-cahill/starlab/actions/runs/24587707730) — **success** (intermediate head `85a1e52…`); [`24587637877`](https://github.com/m-cahill/starlab/actions/runs/24587637877) — **success** but superseded; [`24587630071`](https://github.com/m-cahill/starlab/actions/runs/24587630071) — **cancelled** (superseded by concurrent push) |
| Trigger | `pull_request` |
| Branch | `px1-m00-closeout-governance` |
| **Final PR head SHA (pre-merge tip)** | `c97da264de7669cb7cbb4de26ac772bda38aaba5` |
| PR | [#84](https://github.com/m-cahill/starlab/pull/84) |

---

## 2. Job inventory (authoritative PR-head run)

All jobs **completed successfully** on run `24587767667`:

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

## 3. Verdict (pre-merge)

- **CI:** **Green** on **final** PR head `c97da26…`.  
- **Merge** executed after green — **no** corrective code change required by CI.

---

## 4. Merge boundary (`main`)

| Field | Value |
| --- | --- |
| **Merge commit on `main`** | `f76919e90470e9d5dc8a43a67f9a15ad5cc0e25e` — *Merge pull request #84 from m-cahill/px1-m00-closeout-governance* |
| **Merge-boundary `main` CI** | [`24587816061`](https://github.com/m-cahill/starlab/actions/runs/24587816061) — **success** (push to `main` for merge commit `f76919e…`) |
