"""V15-M59 — adapter smoke readout IO (deterministic JSON + report)."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Final

from starlab.runs.json_util import canonical_json_dumps, sha256_hex_of_canonical_json
from starlab.v15.m59_adapter_smoke_readout_models import (
    CANONICAL_M58_ARTIFACT_SHA256,
    CANONICAL_UPSTREAM_MAIN_SHA,
    CONTRACT_ID_REFUSAL_REPORT,
    EVIDENCE_SOURCE_FIXTURE,
    FILENAME_MAIN_JSON,
    LOCK_DEFERRED_M60,
    M58_ACCEPTANCE_REASON_COMPLETED,
    M58_STATUS_ACCEPTED,
    MILESTONE,
    NEXT_DECISION_M60,
    NEXT_MILESTONE_LEDGER,
    NON_CLAIMS,
    READOUT_ADAPTER_SMOKE_ACCEPTED,
    READOUT_BENCHMARK_NOT_EVIDENCE,
    READOUT_NOT_PROMOTED,
    REFUSED_CLAIMS,
    REPORT_FILENAME,
    SCHEMA_VERSION_READOUT,
    STRONGEST_ALLOWED_CLAIM,
    UPSTREAM_MILESTONE,
)

_SHA256_LEN: Final[int] = 64
_GIT_SHA_LEN: Final[int] = 40


def validate_lowercase_sha256_64(value: str) -> str | None:
    s = str(value).strip().lower()
    if len(s) != _SHA256_LEN or any(c not in "0123456789abcdef" for c in s):
        return None
    return s


def validate_git_sha40(value: str) -> str | None:
    s = str(value).strip().lower()
    if len(s) != _GIT_SHA_LEN or any(c not in "0123456789abcdef" for c in s):
        return None
    return s


def build_readout_body(
    *,
    m58_status: str,
    m58_acceptance_reason: str,
    main_sha: str,
    m58_artifact_sha256: str,
    evidence_source: str,
) -> dict[str, Any]:
    return {
        "schema_version": SCHEMA_VERSION_READOUT,
        "milestone": MILESTONE,
        "upstream_milestone": UPSTREAM_MILESTONE,
        "upstream_evidence": {
            "m58_status": m58_status,
            "m58_acceptance_reason": m58_acceptance_reason,
            "main_sha": main_sha,
            "artifact_sha256": m58_artifact_sha256,
            "evidence_source": evidence_source,
        },
        "readout": {
            "adapter_smoke_status": READOUT_ADAPTER_SMOKE_ACCEPTED,
            "benchmark_status": READOUT_BENCHMARK_NOT_EVIDENCE,
            "promotion_status": READOUT_NOT_PROMOTED,
            "lock_decision_status": LOCK_DEFERRED_M60,
            "next_decision": NEXT_DECISION_M60,
        },
        "strongest_allowed_claim": STRONGEST_ALLOWED_CLAIM,
        "refused_claims": dict(REFUSED_CLAIMS),
        "non_claims": list(NON_CLAIMS),
    }


def build_readout_report(main_body: dict[str, Any]) -> dict[str, Any]:
    ue = main_body.get("upstream_evidence")
    ro = main_body.get("readout")
    return {
        "contract_id": CONTRACT_ID_REFUSAL_REPORT,
        "milestone": MILESTONE,
        "upstream_milestone": UPSTREAM_MILESTONE,
        "upstream_evidence_summary": ue if isinstance(ue, dict) else {},
        "readout_summary": ro if isinstance(ro, dict) else {},
        "strongest_allowed_claim": main_body.get("strongest_allowed_claim"),
        "refused_claims": main_body.get("refused_claims"),
        "non_claims": main_body.get("non_claims"),
        "next_decision_milestone": NEXT_MILESTONE_LEDGER,
        "benchmark_overclaim_refusal": "all_listed_overclaims_refused_true",
        "readout_canonical_sha256": sha256_hex_of_canonical_json(main_body),
    }


def write_readout_artifacts(output_dir: Path, *, body: dict[str, Any]) -> tuple[Path, Path]:
    out = output_dir.resolve()
    out.mkdir(parents=True, exist_ok=True)
    main_p = out / FILENAME_MAIN_JSON
    rep_p = out / REPORT_FILENAME
    main_p.write_text(canonical_json_dumps(body), encoding="utf-8")
    report = build_readout_report(body)
    rep_p.write_text(canonical_json_dumps(report), encoding="utf-8")
    return main_p, rep_p


def validate_operator_evidence_inputs(
    *,
    m58_status: str | None,
    m58_acceptance_reason: str | None,
    main_sha: str | None,
    m58_artifact_sha256: str | None,
) -> tuple[bool, str]:
    if m58_status is None or str(m58_status).strip() == "":
        return False, "missing --m58-status"
    if m58_acceptance_reason is None or str(m58_acceptance_reason).strip() == "":
        return False, "missing --m58-acceptance-reason"
    if main_sha is None or str(main_sha).strip() == "":
        return False, "missing --main-sha"
    if m58_artifact_sha256 is None or str(m58_artifact_sha256).strip() == "":
        return False, "missing --m58-artifact-sha256"

    st = str(m58_status).strip().lower()
    if st != M58_STATUS_ACCEPTED:
        return (
            False,
            f"--m58-status must be {M58_STATUS_ACCEPTED!r} for this readout (got {m58_status!r})",
        )
    rs = str(m58_acceptance_reason).strip()
    if rs != M58_ACCEPTANCE_REASON_COMPLETED:
        return (
            False,
            "--m58-acceptance-reason must be "
            f"{M58_ACCEPTANCE_REASON_COMPLETED!r} (got {m58_acceptance_reason!r})",
        )
    if validate_git_sha40(str(main_sha)) is None:
        return False, "--main-sha must be 40 lowercase hex chars"
    if validate_lowercase_sha256_64(str(m58_artifact_sha256)) is None:
        return False, "--m58-artifact-sha256 must be 64 lowercase hex chars"
    return True, ""


def build_fixture_readout_body() -> dict[str, Any]:
    ms = validate_git_sha40(CANONICAL_UPSTREAM_MAIN_SHA)
    art = validate_lowercase_sha256_64(CANONICAL_M58_ARTIFACT_SHA256)
    assert ms is not None and art is not None
    return build_readout_body(
        m58_status=M58_STATUS_ACCEPTED,
        m58_acceptance_reason=M58_ACCEPTANCE_REASON_COMPLETED,
        main_sha=ms,
        m58_artifact_sha256=art,
        evidence_source=EVIDENCE_SOURCE_FIXTURE,
    )
