# Milestone Audit — M12: Combat, Scouting, and Visibility Windows

**Milestone:** M12 — Combat, Scouting, and Visibility Windows  
**Mode:** DELTA AUDIT  
**Range:** `38c15302badd49966b17f9195ddb139f6ae9a9b4` (pre-M12 `main` @ M11 merge) → `78528958a616177b564e603c193fb0d7f8af734e` (M12 merge commit)  
**PR:** [#13](https://github.com/m-cahill/starlab/pull/13)  
**CI Status:** Green PR-head on final tip ([`24109242392`](https://github.com/m-cahill/starlab/actions/runs/24109242392)); green merge-push `main` on merge commit ([`24109269513`](https://github.com/m-cahill/starlab/actions/runs/24109269513))  
**Audit Verdict:** — **M12 scope** delivered with explicit non-claims; **merge-gate CI posture** matches M11 (green PR-head on final tip).

---

## Executive Summary

**Improvements**

- **Governed combat/scouting/visibility contract** (`docs/runtime/replay_combat_scouting_visibility_extraction.md`) with deterministic `replay_combat_scouting_visibility.json` / `replay_combat_scouting_visibility_report.json`.
- **Pure extraction** over M10 + M11 JSON; optional supplemental **`replay_raw_parse.json` v2** for identity / position / explicit visibility fields only; **no** `s2protocol` in M12 modules.
- **PR merge discipline:** successful merge-gate `pull_request` workflow on **final** PR head before merge.

**Risks**

- **Conservative** combat clustering and visibility labeling — downstream consumers must not treat proxies as ground-truth FOW.
- **Local mypy** may differ on some Windows hosts; **CI Mypy** is authoritative (M12 pre-merge mypy issues were fixed before PR-head green).

**Next action:** Proceed under **M13** for replay slice generation only per plan; **no** M13 product code without milestone governance.

---

## Delta Map & Blast Radius

| Area | Change |
| ---- | ------ |
| Contracts | `docs/runtime/replay_combat_scouting_visibility_extraction.md` |
| Code | `starlab/replays/combat_scouting_visibility_*.py`, `extract_replay_combat_scouting_visibility.py` |
| CI / fixtures | `tests/fixtures/m12/*`; `tests/test_replay_combat_scouting_visibility*.py` |

**Risk zones:** catalog drift, identity lookup misses, governance tests on §11 current milestone.

---

## Architecture & Modularity

### Keep

- Extraction separate from I/O; deterministic canonical JSON; timeline ordering authority documented; fixed combat gap constant documented.

### Fix Now (≤ 90 min)

- None blocking after green merge-push `main`.

---

## CI & Evidence Posture

| Check | Result |
| ----- | ------ |
| PR-head `59adce3…` | [`24109242392`](https://github.com/m-cahill/starlab/actions/runs/24109242392) — **success** |
| Merge-push `main` `7852895…` | [`24109269513`](https://github.com/m-cahill/starlab/actions/runs/24109269513) — **success** |

---

## Verdict

**Narrow M12 claims** are consistent with code and contracts; **strategic or full-simulation claims** beyond the artifact contract are excluded. **Current milestone** advances to **M13** (stub) after ledger closeout commit.
