"""V15-M55 — bounded evaluation package preflight constants."""

from __future__ import annotations

from typing import Final

CONTRACT_ID: Final[str] = "starlab.v15.bounded_evaluation_package_preflight.v1"
REPORT_CONTRACT_ID: Final[str] = "starlab.v15.bounded_evaluation_package_preflight_report.v1"
PROFILE_M55: Final[str] = "starlab.v15.m55.bounded_evaluation_package_preflight.v1"
MILESTONE: Final[str] = "V15-M55"
EMITTER_MODULE: Final[str] = "starlab.v15.emit_v15_m55_bounded_evaluation_package_preflight"

SCHEMA_VERSION: Final[str] = "1.0"
GATE_ARTIFACT_DIGEST_FIELD: Final[str] = "artifact_sha256"

FILENAME_MAIN_JSON: Final[str] = "v15_bounded_evaluation_package_preflight.json"
REPORT_FILENAME: Final[str] = "v15_bounded_evaluation_package_preflight_report.json"

PROFILE_FIXTURE_CI: Final[str] = "fixture_ci"
PROFILE_OPERATOR_PREFLIGHT: Final[str] = "operator_preflight"
PROFILE_OPERATOR_DECLARED: Final[str] = "operator_declared"

SOURCE_KIND_FIXTURE: Final[str] = "fixture_ci"
SOURCE_KIND_OPERATOR: Final[str] = "operator_declared"

STATUS_READY: Final[str] = "ready_for_bounded_readout"
STATUS_BLOCKED_MISSING_INPUT: Final[str] = "blocked_missing_required_input"
STATUS_BLOCKED_IDENTITY_MISMATCH: Final[str] = "blocked_identity_mismatch"
STATUS_BLOCKED_INVALID_SHA256: Final[str] = "blocked_invalid_sha256"
STATUS_BLOCKED_CLAIM_VIOLATION: Final[str] = "blocked_claim_violation"
STATUS_BLOCKED_PRIVATE_BOUNDARY: Final[str] = "blocked_private_boundary_violation"

ALLOWED_NEXT_STEP: Final[str] = "V15-M56_bounded_evaluation_package_readout"

CANONICAL_UPSTREAM_M54_PACKAGE_SHA256: Final[str] = (
    "bbe08673aa85beb0ae7e51a627a68c67fd95a930176d174d2c60bb96e4a278d6"
)
CANONICAL_UPSTREAM_M54_PACKAGE_ID: Final[str] = (
    "starlab.v15.m54.twelve_hour_run_package.sealed.bbe08673aa85beb0ae7e51a627a68c67fd95a930176d174d2c60bb96e4a278d6"
)

PREFLIGHT_ID_FIXTURE: Final[str] = "v15_m55_bounded_evaluation_package_preflight_fixture_ci_v1"

# Deterministic fixture-only auxiliary digests (metadata placeholders; not real operator evidence).
FIXTURE_PACKAGE_ID: Final[str] = "starlab.v15.m55.fixture_ci.evaluation_package.v1"
FIXTURE_EVALUATION_MANIFEST_SHA256: Final[str] = "ab" * 32
FIXTURE_CANDIDATE_IDENTITY_SHA256: Final[str] = "cd" * 32
FIXTURE_SCORECARD_READOUT_PLAN_SHA256: Final[str] = "ef" * 32

CHECK_ID_PACKAGE_IDENTITY: Final[str] = "package_identity_declared"
CHECK_ID_UPSTREAM_CLOSURE: Final[str] = "upstream_m54_closure"
CHECK_ID_MANIFEST_COMPLETE: Final[str] = "manifest_completeness"
CHECK_ID_PATH_HYGIENE: Final[str] = "path_hygiene"
CHECK_ID_CLAIM_HYGIENE: Final[str] = "claim_hygiene"
CHECK_ID_READOUT_READY: Final[str] = "readout_readiness"

REASON_UPSTREAM_MISMATCH: Final[str] = (
    "declared_upstream_m54_sha256_does_not_match_canonical_sealed_package"
)
REASON_INVALID_SHA256_FORMAT: Final[str] = "sha256_must_be_64_lowercase_hex_characters"
REASON_MISSING_OPERATOR_ARG: Final[str] = "missing_required_operator_cli_input"
REASON_MANIFEST_FILE_MISSING: Final[str] = "evaluation_package_manifest_unreadable_or_missing"
REASON_CANDIDATE_FILE_MISSING: Final[str] = "candidate_identity_json_unreadable_or_missing"
REASON_SCORECARD_FILE_MISSING: Final[str] = "scorecard_readout_plan_json_unreadable_or_missing"
REASON_PACKAGE_SHA_MISMATCH: Final[str] = (
    "evaluation_package_sha256_does_not_match_synthesized_binding"
)
REASON_COMPANY_SECRETS_REF: Final[str] = "input_metadata_references_docs_company_secrets"
REASON_OUT_PATH_REF: Final[str] = "input_metadata_references_raw_out_path_as_committed_evidence"
REASON_CLAIM_FLAG_TRUE: Final[str] = "claim_flag_must_remain_false_in_m55"

NON_CLAIMS: Final[tuple[str, ...]] = (
    "No evaluation execution was performed.",
    "No benchmark pass/fail result is claimed.",
    "No checkpoint promotion is claimed.",
    "No strong-agent, human-panel, XAI, ladder, or v2-readiness claim is made.",
)

DEFAULT_CLAIM_FLAGS: Final[dict[str, bool]] = {
    "evaluation_executed": False,
    "benchmark_pass_claimed": False,
    "candidate_promoted": False,
    "strong_agent_claimed": False,
    "human_panel_claimed": False,
    "xai_demo_claimed": False,
    "v2_ready_claimed": False,
}

FORBIDDEN_FLAG_CLAIM_BENCHMARK: Final[str] = "--claim-benchmark-pass"
FORBIDDEN_FLAG_CLAIM_STRENGTH: Final[str] = "--claim-strength"
FORBIDDEN_FLAG_PROMOTE: Final[str] = "--promote-checkpoint"
FORBIDDEN_FLAG_RUN_BENCHMARK: Final[str] = "--run-benchmark"
FORBIDDEN_FLAG_RUN_XAI: Final[str] = "--run-xai"
FORBIDDEN_FLAG_RUN_HUMAN_PANEL: Final[str] = "--run-human-panel"
FORBIDDEN_FLAG_SHOWCASE: Final[str] = "--release-showcase"
FORBIDDEN_FLAG_V2: Final[str] = "--authorize-v2"
FORBIDDEN_FLAG_T2: Final[str] = "--execute-t2"
FORBIDDEN_FLAG_T3: Final[str] = "--execute-t3"
FORBIDDEN_FLAG_T4: Final[str] = "--execute-t4"
FORBIDDEN_FLAG_T5: Final[str] = "--execute-t5"
FORBIDDEN_FLAG_LOAD_CKPT_EVAL: Final[str] = "--load-checkpoint-for-evaluation"
FORBIDDEN_FLAG_TORCH_LOAD: Final[str] = "--torch-load-checkpoint"

FORBIDDEN_CLI_FLAGS: Final[tuple[str, ...]] = (
    FORBIDDEN_FLAG_CLAIM_BENCHMARK,
    FORBIDDEN_FLAG_CLAIM_STRENGTH,
    FORBIDDEN_FLAG_PROMOTE,
    FORBIDDEN_FLAG_RUN_BENCHMARK,
    FORBIDDEN_FLAG_RUN_XAI,
    FORBIDDEN_FLAG_RUN_HUMAN_PANEL,
    FORBIDDEN_FLAG_SHOWCASE,
    FORBIDDEN_FLAG_V2,
    FORBIDDEN_FLAG_T2,
    FORBIDDEN_FLAG_T3,
    FORBIDDEN_FLAG_T4,
    FORBIDDEN_FLAG_T5,
    FORBIDDEN_FLAG_LOAD_CKPT_EVAL,
    FORBIDDEN_FLAG_TORCH_LOAD,
)
