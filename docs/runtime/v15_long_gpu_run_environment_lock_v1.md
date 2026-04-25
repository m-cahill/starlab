# V15-M02 — Long GPU Run Environment Lock (v1)

**Contract id:** `starlab.v15.long_gpu_environment_lock.v1`  
**Milestone:** V15-M02  
**Status:** Governed environment-lock *surface* — **not** a training execution milestone.

**Merge record (governance):** **V15-M02** implementation merged to `main` as [PR #118](https://github.com/m-cahill/starlab/pull/118) (merge commit `3f7e226ff0402cbb91b831e7c9397080cc8a77aa`). Authoritative **PR-head** CI [`24918006750`](https://github.com/m-cahill/starlab/actions/runs/24918006750); merge-boundary [`main` CI `24918563270`](https://github.com/m-cahill/starlab/actions/runs/24918563270). This closure **does not** assert long GPU **environment readiness** from fixture output and **does not** record training execution.

## 1. Purpose

V15-M02 defines and emits a **deterministic environment-lock contract** for STARLAB v1.5. It records *what* must be known about the repository, Python stack, dependencies, CUDA/PyTorch, GPU, SC2, map pool, disk, and path posture **before** a long GPU run can be treated as *governed* program work.

This milestone **does not** run GPU training, **does not** run a GPU shakedown, **does not** prove portability across machines, **does not** approve datasets or weights, and **does not** itself *green-light* a long GPU run. It supplies **evidence structure** and **vocabulary** only.

> A fixture-only environment lock is not an operator-local RTX 5090 environment lock.

## 2. Relationship to V15-M00 gates (A–G)

Long GPU training (program-valid) is gated in **`docs/starlab-v1.5.md`** (Gate **A**–**G**). V15-M02 supports **Gate B — Environment** (GPU, CUDA/PyTorch, SC2, maps, disk, dependency pins) by defining **how** to record and normalize environment facts — **not** by satisfying the gate in CI.

## 3. Relationship to V15-M01 (registers / provenance)

V15-M01 provides **register templates** and `starlab.v15.training_asset_registers.v1`. The environment lock **references** the same public/private discipline: operator-local absolute paths, raw SC2 client paths, and map paths are **not** public-by-default. Environment facts may point at register rows in later milestones; M02 does **not** populate claim-critical register rows.

## 4. Gate B — environment categories (field groups)

| Group | Intent |
| --- | --- |
| **repo_identity** | `git_sha`, `branch`, `dirty_tree_policy`, `repository` |
| **python_environment** | `python_version`, `implementation`, `platform`, `venv_policy` |
| **dependency_environment** | `requirements_source`, `lockfile_paths`, `dependency_fingerprint`, `pip_audit_status`, `sbom_status` |
| **cuda_environment** | `cuda_available`, `cuda_version`, `driver_version`, `nvidia_smi_status` |
| **pytorch_environment** | `torch_installed`, `torch_version`, `torch_cuda_version`, `cuda_device_count` |
| **gpu_environment** | `gpu_present`, `gpu_name`, `gpu_memory_total_bytes`, `gpu_compute_capability`, `gpu_driver` |
| **sc2_environment** | `sc2_client_declared`, `sc2_version`, `sc2_path_disclosure`, `sc2_probe_status` |
| **map_pool_environment** | `map_pool_id`, `required_maps`, `maps_present`, `map_probe_status` |
| **disk_environment** | `output_root_policy`, `free_bytes_required`, `free_bytes_observed`, `disk_probe_status` |
| **path_disclosure_policy** | Public vs private path posture (see status vocabulary) |
| **operator_notes** | Free text; may be `null` in fixture profile |

M02 does **not** execute `nvidia-smi`, does **not** scan SC2 install paths, and does **not** inspect on-disk maps. Those facts enter only via **operator-declared** `--probe-json` (or later milestones).

## 5. CI fixture vs operator-local evidence

| Mode | `profile` | GPU/CUDA/SC2 required? | What it proves |
| --- | --- | --- | --- |
| **CI fixture** | `fixture_ci` (default) | **No** | Schema, seal, and governance strings are stable; `environment_lock_status` is `fixture_only`. |
| **Operator** | `operator_local` + optional `--probe-json` | **No** (CLI does not auto-probe) | Normalizes and evaluates **supplied** operator fields; may reach `operator_local_ready` if required checks pass. Still **not** program authorization. |

**Required default posture (governance):**

- CI fixture **status** column: treat as `fixture` (or `not_applicable` where the table uses check semantics).
- Operator-local **status** default: `not_evaluated` until a probe is supplied.
- **Long GPU authorization** field in the JSON: **always `false` in M02** — the milestone never grants long-run approval.

## 6. Status vocabulary (contract)

- `environment_lock_status`: `fixture_only` | `operator_local_ready` | `operator_local_incomplete` | `blocked` | `not_evaluated`
- `check_status` (per required check): `pass` | `fail` | `warning` | `not_applicable` | `not_evaluated` | `fixture`
- `path_disclosure` (policy fields): `public_safe` | `redacted` | `logical_reference_only` | `private_local_only` | `forbidden_public`
- `evidence_scope`: `ci_fixture` | `operator_local_probe` | `operator_declared` | `not_evaluated`

## 7. Non-claims (M02)

The emitted JSON `non_claims` list is authoritative for machine checking. In prose, V15-M02:

- May validate fixture CI mechanics and may normalize operator-local environment evidence when supplied.
- Does **not** execute GPU training, does **not** run a GPU shakedown, does **not** prove a long-run environment is globally portable, does **not** approve datasets or weights, does **not** implement checkpoint lineage, does **not** run benchmarks, does **not** run human evaluation, does **not** freeze XAI contracts, does **not** open v2, and does **not** open PX2-M04/PX2-M05.

Accepting `--probe-json` does **not** by itself mean the environment is **ready**; `operator_local_ready` is **only** “required fields satisfied per M02 rules,” not “safe to begin long training.”

## 8. `--probe-json` minimal schema (non-authoritative)

Top-level object only. Allowed keys (unknown keys are rejected):

- `evidence_scope` (string, optional)
- `repo_identity`, `python_environment`, `dependency_environment`, `cuda_environment`, `pytorch_environment`, `gpu_environment`, `sc2_environment`, `map_pool_environment`, `disk_environment` (objects; each merged over an internal default)
- `path_disclosure_policy` (object, optional)
- `operator_notes` (string or omitted)

Each subsection follows the field shapes in §4. Partial probes may yield `operator_local_incomplete` and `not_evaluated` checks. Absolute path-like strings in values are **redacted** in emitted JSON (`<REDACTED_ABSOLUTE_PATH>`).

## 9. CLI

```bash
python -m starlab.v15.emit_v15_long_gpu_environment_lock --output-dir <path>
```

Options:

- `--profile fixture_ci` (default) or `--profile operator_local`
- `--probe-json <path>` (only meaningful with `operator_local`)

**Artifacts:** `v15_long_gpu_environment_lock.json`, `v15_long_gpu_environment_lock_report.json` (report includes `long_gpu_environment_lock_sha256`).

## 10. V15-M02 claim discipline (for PRs / reviews)

V15-M02 defines and emits the long GPU run environment-lock surface. It may validate fixture CI mechanics and may normalize operator-local environment evidence when supplied, but it does not execute GPU training, does not run a GPU shakedown, does not prove a long-run environment is globally portable, does not approve datasets or weights, does not implement checkpoint lineage, does not run benchmarks, does not run human evaluation, does not freeze XAI contracts, does not open v2, and does not open PX2-M04/PX2-M05.
