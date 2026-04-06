# M02 — Local real-execution note

**Status:** **RECORDED — 2026-04-06 (local session on Windows).**  
This session used the real **`burnysc2`** adapter path and a committed config file. **Both harness invocations failed** before writing `match_execution_proof.json` because the **configured map file did not exist on disk** (no `Maps/` tree with that tutorial map under the install). This is **honest negative evidence**: the environment is partially ready (binary resolved) but **not** sufficient for two successful proof-producing runs.

---

## Session metadata

- **Date/time (UTC):** 2026-04-06 (local session; exact clock not material to the failure mode)
- **Machine:** same Windows host as development; two attempts on **same machine**, **same config file**
- **Optional extra install:** `python -m pip install -e ".[sc2-harness]"` — **exit 0** (editable `starlab` + `burnysc2` already satisfied)

---

## Environment posture (paths redacted where useful)

- **`STARLAB_SC2_ROOT`:** set for the session to the standard x86 install root (Battle.net-style layout). **Redacted in prose:** `C:/Program Files (x86)/StarCraft II` (public default path pattern).
- **`STARLAB_SC2_MAPS_DIR`:** not set separately; probe derived `Maps` path under root.
- **Probe (`python -m starlab.sc2 --redact`):** `root` and `binary` **present**; **`maps_dir` / `present.maps_dir`:** **false** (no `Maps` directory at expected location on this install). `base_build` / `data_version`: **null** in probe output.

---

## Map resolution mode

- **`explicit_path`** — single `.SC2Map` path in `m02_local_config.json` (see repo path below).

---

## Config used (committed)

- **Path:** `docs/company_secrets/milestones/M02/m02_local_config.json`
- **Adapter:** `burnysc2`
- **Seed:** `424242`
- **Horizon:** `max_game_steps` 100, `game_step` 1
- **Interfaces:** raw + score only; feature/render **false**
- **`save_replay`:** `false`

---

## Commands (exact)

**Environment for both runs:**

```text
$env:STARLAB_SC2_ROOT = "C:\Program Files (x86)\StarCraft II"
```

**Run 1:**

```text
python -m starlab.sc2.run_match --config docs/company_secrets/milestones/M02/m02_local_config.json --output-dir docs/company_secrets/milestones/M02/_local_runs/run1
```

**Run 2:**

```text
python -m starlab.sc2.run_match --config docs/company_secrets/milestones/M02/m02_local_config.json --output-dir docs/company_secrets/milestones/M02/_local_runs/run2
```

---

## Outcome

- **Run 1:** **failed** — process exit code **2**; stderr: `configured map path not found: …\Maps\Tutorial\Tutorial01.SC2Map`. **No** `match_execution_proof.json` written.
- **Run 2:** **failed** — **same** error; **No** proof file.

**Conclusion:** This session **does not** establish the narrow same-machine deterministic harness claim (no normalized `artifact_hash` pair). **Next step for a future session:** install or place at least one valid `.SC2Map` at the configured path (or update the config to an existing map path), then repeat two runs.

**Do not** commit SC2 binaries, maps, or replay files — this note references only standard install layout and repo-local config.
