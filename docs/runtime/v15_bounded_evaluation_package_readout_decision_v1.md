# STARLAB runtime — V15-M56: Bounded Evaluation Package Readout / Decision v1

**Contract ids:**

- `starlab.v15.bounded_evaluation_package_readout_decision.v1`
- `starlab.v15.bounded_evaluation_package_readout_decision_report.v1`
- `starlab.v15.m56.bounded_evaluation_package_readout_decision.v1`

**Milestone:** `V15-M56`  
**Emitter:** `python -m starlab.v15.emit_v15_m56_bounded_evaluation_package_readout_decision`

## Purpose

**V15-M56** is a **bounded readout / decision surface** over sealed **V15-M55** bounded evaluation package preflight artifacts. It does **not** execute evaluation, compute benchmark pass/fail, produce scorecard results, evaluate strength, promote checkpoints, invoke `torch.load`, load checkpoint blobs, run live SC2, run GPU inference, run XAI, run human-panel evaluation, release a showcase agent, authorize v2, or execute T2–T5.

It answers:

> Given the sealed M55 preflight, is the package ready for a future governed evaluation step, blocked, or in need of remediation?

**Strongest allowed claim:** V15-M56 can read sealed V15-M55 preflight artifacts and emit a bounded readout / decision indicating whether the package is ready, blocked, or requires remediation for a future governed evaluation step. It does not execute evaluation or authorize benchmark/pass/promotion claims.

## Immediate upstream

**V15-M55 — Bounded Evaluation Package Preflight** — primary input:

- `v15_bounded_evaluation_package_preflight.json` (sealed; `artifact_sha256` must verify per STARLAB canonical JSON sealing).

**M55 seal verification (operator paths):** `artifact_sha256 = sha256(canonical JSON body without artifact_sha256)`. Malformed or missing seal **blocks** readout.

## Cross-check anchors (registry)

| Anchor | SHA-256 |
| --- | --- |
| Canonical sealed **V15-M54** package | `bbe08673aa85beb0ae7e51a627a68c67fd95a930176d174d2c60bb96e4a278d6` |
| **V15-M53** run artifact (canonical) | `18a1e6c39bb372c3f7edc595919963d12442467a74dd329e56f7cf0d0c816ec8` |
| Latest produced candidate checkpoint | `7c91a4b7cec6b14d160c00bec768c4fb3199bd8bf0228b2436bd7fbc5dc6ea90` |

Optional **`--m54-readiness-json`:** sealed `v15_twelve_hour_run_package_readiness.json` whose `artifact_sha256` matches the expected M54 package digest. When provided, **M53** artifact digest and **produced candidate** digest are read from `m53_binding.artifact_sha256` and `candidate_checkpoint_binding.produced_candidate_checkpoint_sha256` and compared to CLI expectations. When omitted, **M53** / **candidate** CLI expectations are compared to the canonical registry values only, with a **warning** that independent cross-check from an M54 file was not used.

## V15-M56A context (non-gating)

Optional **`--m56a-context-json`:** governed watchability confirmation JSON. **M56A is context only** — it does **not** gate M56. Absent context keeps `ready_for_future_governed_evaluation` with a non-gating warning. Invalid JSON yields a **warning**, not a block.

## Primary artifacts

| File | Role |
| --- | --- |
| `v15_bounded_evaluation_package_readout_decision.json` | Sealed main readout (`artifact_sha256` over canonical body without that field). |
| `v15_bounded_evaluation_package_readout_decision_report.json` | Report companion. |
| `v15_bounded_evaluation_package_readout_decision_checklist.md` | Operator checklist. |

## Profiles

| Profile | Behavior |
| --- | --- |
| `fixture_ci` | Deterministic synthetic readout; **no** filesystem dependency on real `out/`. |
| `operator_preflight` | Loads and strictly verifies M55 seal; checks M55 `preflight_status == ready_for_bounded_readout`; optional M54 readiness file for M53/candidate cross-check. |
| `operator_declared` | Validates declared readout metadata JSON against M55 seal and honesty; **no** execution. |

**No runner** in M56.

## Route recommendation (not executed)

- **Route:** `route_to_future_governed_evaluation_design_or_execution_gate`
- **`route_status`:** `recommended_not_executed`
- **Recommended next milestone:** `V15-M57 — Governed Evaluation Execution Charter / Dry-Run Gate`

## Standing non-claims

- No benchmark execution.
- No benchmark pass/fail.
- No scorecard results.
- No strength evaluation.
- No checkpoint promotion.
- No checkpoint rejection as a strength decision.
- No `torch.load`.
- No checkpoint blob loading.
- No live SC2.
- No GPU inference.
- No XAI execution.
- No human-panel evaluation.
- No showcase release.
- No v2 authorization.
- No T2–T5 execution.
- No raw `out/`, replay, video, checkpoint, or private operator evidence committed on the public path.

## Sample commands

Fixture (CI-safe):

```bash
python -m starlab.v15.emit_v15_m56_bounded_evaluation_package_readout_decision \
  --profile fixture_ci \
  --output-dir out/v15_m56_fixture
```

Operator preflight (M55 + expected SHAs; optional M54 / M56A):

```bash
python -m starlab.v15.emit_v15_m56_bounded_evaluation_package_readout_decision \
  --profile operator_preflight \
  --output-dir out/v15_m56_operator_preflight \
  --m55-preflight-json <path-to-v15_bounded_evaluation_package_preflight.json> \
  --expected-m54-package-sha256 bbe08673aa85beb0ae7e51a627a68c67fd95a930176d174d2c60bb96e4a278d6 \
  --expected-m53-run-artifact-sha256 18a1e6c39bb372c3f7edc595919963d12442467a74dd329e56f7cf0d0c816ec8 \
  --expected-candidate-sha256 7c91a4b7cec6b14d160c00bec768c4fb3199bd8bf0228b2436bd7fbc5dc6ea90
```

Optional: `--m54-readiness-json <sealed-M54-json>` , `--m56a-context-json <M56A-json>`.

Operator declared:

```bash
python -m starlab.v15.emit_v15_m56_bounded_evaluation_package_readout_decision \
  --profile operator_declared \
  --output-dir out/v15_m56_operator_declared \
  --declared-readout-json <path> \
  --m55-preflight-json <path> \
  --expected-candidate-sha256 7c91a4b7cec6b14d160c00bec768c4fb3199bd8bf0228b2436bd7fbc5dc6ea90
```

Exit codes: **`0`** success / fixture / forbidden-flag bundle written; **`2`** CLI usage; **`3`** blocked readout bundle emitted.
