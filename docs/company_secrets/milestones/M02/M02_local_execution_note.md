# M02 — Local real-execution note

**Status:** **RECORDED — 2026-04-06 (recovery session on Windows).**  
This session used the real **`burnysc2`** adapter path and the committed `m02_local_config.json`. **Two** harness invocations **succeeded** and each wrote `match_execution_proof.json` with the **same** normalized `artifact_hash`. This documents **honest positive evidence** for the **narrow** same-machine harness slice (fixed seed, bounded horizon, normalized proof hash). It is **not** a replay-binding proof, canonical run artifact v0, benchmark claim, or cross-host reproducibility claim.

---

## Session metadata

- **Date/time (UTC):** 2026-04-06 (local session)
- **Machine:** same Windows host as development; two attempts on **same machine**, **same config file**
- **Optional extra install:** `python -m pip install -e ".[sc2-harness]"` — **exit 0** when used (editable `starlab` + `burnysc2`)

---

## Prior blocker (superseded for this session)

An earlier 2026-04-06 session failed because no valid tutorial map existed under the install `Maps/` tree and a ProgramData cache path was not accepted by `CreateGame`. **This session** recovered by using a **real** `.SC2Map` **file** (see below) and a code fix that **resolves explicit map paths to absolute paths** before passing them to python-sc2 (relative paths were incorrectly joined under install `Maps/`).

---

## Map source (not committed to git)

- **Source:** [google-deepmind/pysc2](https://github.com/google-deepmind/pysc2) — `pysc2/maps/mini_games/MoveToBeacon.SC2Map` (research / Apache-2.0 project; map retrieved via HTTPS raw URL).
- **Local placement (raw path):** `C:\coding\starlab\docs\company_secrets\milestones\M02\_local_maps\MoveToBeacon.SC2Map` (gitignored directory `_local_maps/`; **do not** commit the binary).
- **Redacted / portable reference in config:** `docs/company_secrets/milestones/M02/_local_maps/MoveToBeacon.SC2Map` (relative to repository root; run CLI with working directory at repo root so resolution matches).

---

## Environment posture (paths redacted where useful)

- **`STARLAB_SC2_ROOT`:** set for the session to the standard x86 install root. **Redacted pattern:** `C:/Program Files (x86)/StarCraft II`.
- **`STARLAB_SC2_MAPS_DIR`:** not set; install **does not** ship a populated `Maps/` tree on this host (probe may still report `maps_dir` absent or empty).
- **Probe (`python -m starlab.sc2 --redact`):** used for earlier diagnostics; harness runs below used explicit map path to the pysc2 mini-game file.

---

## Map resolution mode

- **`explicit_path`** — `.SC2Map` file path in `m02_local_config.json` (repo-relative path as committed).

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

**Working directory:** repository root (`starlab` clone).

**Run 1:**

```text
python -m starlab.sc2.run_match --config docs/company_secrets/milestones/M02/m02_local_config.json --output-dir docs/company_secrets/milestones/M02/_local_runs/run1 --redact
```

**Run 2:**

```text
python -m starlab.sc2.run_match --config docs/company_secrets/milestones/M02/m02_local_config.json --output-dir docs/company_secrets/milestones/M02/_local_runs/run2 --redact
```

---

## Outcome

- **Run 1:** **exit 0** — `match_execution_proof.json` written under `_local_runs/run1/`.
- **Run 2:** **exit 0** — `match_execution_proof.json` written under `_local_runs/run2/`.
- **Normalized `artifact_hash` (both runs):** `b23172cb457b7645d796c30cf36baf96229efa3af954190788370ba5ea464e53`

**Conclusion:** On this host, with this config and map file, the **narrow** STARLAB normalized proof hash **matched** across two successive runs. **`M02_execution_proof_redacted.json`** in this folder is a copy of the redacted JSON from run 1 (equivalent hash content to run 2).

**Do not** commit SC2 binaries, map binaries, or replay files — the map file stays under gitignored `_local_maps/`; this note references retrieval steps only.
