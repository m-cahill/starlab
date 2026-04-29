"""V15-M33 candidate checkpoint model-load / CUDA inference probe constants."""

from __future__ import annotations

from typing import Final

CONTRACT_ID_M33_PROBE: Final[str] = "starlab.v15.candidate_checkpoint_model_load_cuda_probe.v1"
PROFILE_M33_PROBE: Final[str] = "starlab.v15.m33.candidate_checkpoint_model_load_cuda_probe.v1"

MILESTONE_LABEL_M33: Final[str] = "V15-M33"

EMITTER_MODULE_M33: Final[str] = (
    "starlab.v15.emit_v15_m33_candidate_checkpoint_model_load_cuda_probe"
)

FILENAME_MAIN_JSON: Final[str] = "v15_candidate_checkpoint_model_load_cuda_probe.json"
REPORT_FILENAME: Final[str] = "v15_candidate_checkpoint_model_load_cuda_probe_report.json"
CHECKLIST_FILENAME: Final[str] = "v15_candidate_checkpoint_model_load_cuda_probe_checklist.md"

SCHEMA_VERSION: Final[str] = "1.0"
GATE_ARTIFACT_DIGEST_FIELD: Final[str] = "artifact_sha256"

STATUS_PROBE_COMPLETED: Final[str] = "candidate_model_load_cuda_probe_completed"
STATUS_FIXTURE_SCHEMA_ONLY: Final[str] = "fixture_schema_only_no_checkpoint_blob"
STATUS_REFUSED_BLOCKERS: Final[str] = "candidate_model_load_cuda_probe_refused_with_blockers"

M32_EXECUTION_STATUSES_OK: Final[frozenset[str]] = frozenset(
    {
        "candidate_evaluation_execution_fixture_completed",
        "candidate_evaluation_execution_operator_local_metadata_completed",
    },
)

RECOMMENDED_NEXT_SUCCESS: Final[str] = "V15-M35_candidate_checkpoint_smoke_benchmark_readiness"
RECOMMENDED_NEXT_LOADER_REMEDIATION: Final[str] = "V15-M35_candidate_checkpoint_probe_remediation"

NON_CLAIMS_M33: Final[tuple[str, ...]] = (
    "no training",
    "no 72-hour campaign",
    "no live SC2 execution",
    "no benchmark pass",
    "no scorecard execution",
    "no strength evaluation",
    "no checkpoint promotion",
    "no XAI execution",
    "no human-panel execution",
    "no showcase release",
    "no v2 authorization",
    "no T2/T3 claim",
)

EXPECTED_PUBLIC_CANDIDATE_SHA256: Final[str] = (
    "eac6fc1f37aa958279a80209822765ecfa6aa2525ed64a8bee88c0ac2be13d26"
)
