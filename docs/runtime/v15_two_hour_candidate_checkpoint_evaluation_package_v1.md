# V15-M42 — Two-hour-run candidate checkpoint evaluation package (`starlab.v15.candidate_checkpoint_evaluation_package.v1`)

## Purpose

V15-M42 assembles a **governed candidate checkpoint evaluation package** and **routing artifacts** from the **V15-M41** two-hour-run evaluation-readiness seal. **M41 is mandatory:** the operator success path **requires** a validated sealed **`v15_two_hour_run_package_evaluation_readiness.json`**. Raw **V15-M39** companion JSON may be supplied only for **optional cross-check / enrichment**; M42 **must not** treat direct M39 inputs as a substitute for a governed M41 package.

V15-M42 does not execute benchmark matches, evaluate strength, promote checkpoints, produce scorecard results, run live SC2, run XAI, run human-panel evaluation, release a showcase agent, authorize v2, execute T2/T3, invoke `torch.load`, or load checkpoint blobs.

## Public merge closeout

Authoritative numbered pull-request markdown lives in **`docs/starlab-v1.5.md`** (**§5** table) and **`docs/starlab.md`** (quick-scan). **This runtime doc remains PR-pattern-free** and records **identifier-only** telemetry:

- Merge commit on `main`: **`8c9039a1d535135f6c1e2e910b71db8df903bdd9`** (merged **2026-04-30T07:43:35Z** UTC).
- Final PR-head commit under **authoritative merge-gate CI**: **`a7ad4c5551d1ada195fecbc572f759e529b380d2`**.
- Required merge-gate workflow run on that head: **`25153445769`** — **success** (`https://github.com/m-cahill/starlab/actions/runs/25153445769`).
- Superseded PR-head runs (**not** merge authority): **`25152833597`**, **`25153128543`** — **failure** (coverage `fail_under` gate / threshold boundary on earlier tips).
- Merge-boundary **`main`** workflow run on merge push: **`25153637517`** — **success** (`https://github.com/m-cahill/starlab/actions/runs/25153637517`).

## Contract / profile

- **Contract family:** `starlab.v15.candidate_checkpoint_evaluation_package.v1`
- **Profile:** `starlab.v15.m42.two_hour_run_candidate_checkpoint_evaluation_package.v1`
- **Emitter:** `python -m starlab.v15.emit_v15_m42_two_hour_candidate_checkpoint_evaluation_package`

## Authority chain

1. **M39** sealed operator receipt (**execution receipt** posture).
2. **M41** governed package/readiness (**primary authority** for M42).
3. **M42** evaluation-package assembly / routing (**this milestone**).

If **`--m41-package-json`** is missing or unreadable: classify **`package_blocked_missing_m41_package`** (or invalid M41 posture) — **do not** fall through to “success” using only M39.

## Inputs

| Input | Required | Role |
| --- | --- | --- |
| `--m41-package-json` | **Yes** | Primary authority: canonical seal validated; inherits upstream M39 receipt digest binding when present |
| `--m39-run-json` | No | Optional cross-check / enrichment vs sealed M41 body |
| `--m39-checkpoint-inventory-json` | No | Optional cross-check |
| `--m39-telemetry-summary-json` | No | Optional cross-check |
| `--m05-scorecard-json` | No | Optional M05 protocol metadata bind (**does not** execute scorecard results) |
| `--expected-m41-package-sha256` | No | Optional: when supplied, must match validated M41 canonical artifact SHA; when omitted, record **`expected_m41_package_sha256_status`:** **`optional_not_supplied`** |

M42 **does not** scan the repository or operator `out/` tree to discover M05 unless a **clean** upstream binding is already carried inside M41 (inheritance path only — no broad discovery).

## Modes

### 1. Fixture CI (`--fixture-ci`)

- Emits schema-only artifacts for merge-gate CI.
- **`package_status`:** `fixture_schema_only_no_operator_package`
- **`evaluation_ready`:** `false`

### 2. Operator package preflight (`--profile operator_preflight`)

- Requires **`--m41-package-json`** plus expected **M39 receipt** digest and **source / final candidate** SHA-256 arguments consistent with the M41 checklist pattern (see emitter CLI).
- Validates M41 canonical seal, M41 readiness posture (from `package_status`), inherited M39 receipt digest vs CLI-expected digest when M41 carries it, and candidate role SHAs.
- Optional M39 files strengthen cross-check fields when their digests match M41 / ledger expectations.
- Optional M05: validate `contract_id == starlab.v15.strong_agent_scorecard.v1` and `protocol_profile_id == starlab.v15.strong_agent_benchmark_protocol.v1` when present; bind by canonical SHA only — **no** benchmark execution.

## Output artifacts

- `v15_m42_two_hour_candidate_checkpoint_evaluation_package.json` (sealed)
- `v15_m42_two_hour_candidate_checkpoint_evaluation_package_report.json`
- `v15_m42_two_hour_candidate_checkpoint_evaluation_package_checklist.md`
- `v15_m42_candidate_evaluation_routing_packet.md`
- `v15_m42_candidate_bindings_index.json`

## Gate pack (P0–P10)

| Gate | Name | Pass condition (summary) |
| --- | --- | --- |
| **P0** | M41 package bound | M41 JSON readable; canonical seal valid |
| **P1** | M41 status ready | M41 `package_status` in readiness set |
| **P2** | M39 receipt inherited | Upstream M39 receipt digest in M41 matches CLI-expected digest when bound |
| **P3** | Source candidate bound | Source lineage SHA consistent |
| **P4** | Final candidate bound | Final candidate SHA consistent |
| **P5** | Candidate role valid | Structural candidate checkpoint roles |
| **P6** | Evidence companions bound | Companion / cross-check posture (when applicable) |
| **P7** | Optional M05 protocol valid | M05 JSON valid when supplied; or optional not supplied |
| **P8** | Public/private boundary | Path-leak heuristics |
| **P9** | Non-claims preserved | Claim flags remain honest |
| **P10** | Evaluation routing only | Package is routing / assembly — not execution |

## Relationship to M41

M41 is the **sole normal authority** for the completed two-hour run package. M42 **builds on** M41; it does **not** re-litigate M39 from raw artifacts alone.

## Relationship to M05

Optional scorecard protocol binding: **`binding_status`** may be **`optional_not_supplied`**, **`bound_by_cli_sha`**, **`inherited_from_m41`**, or blocked on invalid CLI JSON. **No** scorecard **results** and **no** benchmark match execution.

## Non-claims

M42 does **not** claim: benchmark pass, strength evaluation, checkpoint promotion, scorecard **results**, T2/T3, XAI execution, human-panel execution, showcase release, or v2 authorization.

## Status vocabulary (selected)

- `fixture_schema_only_no_operator_package`
- `package_blocked_missing_m41_package`
- `package_blocked_invalid_m41_package`
- `package_blocked_m41_not_ready`
- `package_blocked_m39_receipt_mismatch`
- `package_blocked_source_candidate_mismatch`
- `package_blocked_final_candidate_mismatch`
- `package_ready_for_future_candidate_evaluation`
- `package_ready_with_noncritical_warnings`
- `package_blocked_invalid_m05_protocol` (when operator supplies invalid M05 JSON / contract mismatch)

## Ledger anchors (public record examples)

- **M39 receipt SHA-256:** `675ae631ff2fa8a9f71f2c03a93f3abbffbfe0c45fcb49a59c933920330b010c`
- **Source lineage SHA-256:** `eac6fc1f37aa958279a80209822765ecfa6aa2525ed64a8bee88c0ac2be13d26`
- **Final two-hour candidate SHA-256:** `51cea94ed5324087863b246b7b31a21021eba286924aea4609aa09466430a943`

## Provisional next

- **Success path:** `V15-M43_bounded_evaluation_gate_for_two_hour_candidate`
- **Remediation path:** `V15-M43_2Hour_Candidate_Evaluation_Package_Remediation`
