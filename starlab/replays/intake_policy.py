"""Deterministic replay intake policy evaluation (M07)."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from starlab.replays.intake_models import (
    CHECK_IDS,
    CheckSeverity,
    CheckStatus,
    IntakeStatus,
    NormalizedReplayIntakeMetadata,
)

EXP_BINDING_HASH_EXPECTED = (
    "replay_binding.replay_content_sha256 matches computed replay hash when binding supplied"
)
EXP_LINKED_ARTIFACTS_CONSISTENT = (
    "optional run_identity/manifest consistent with replay_binding when supplied"
)


@dataclass(frozen=True)
class PolicyOutcome:
    """Result of deterministic policy evaluation."""

    intake_status: IntakeStatus
    local_processing_allowed: bool
    canonical_review_eligible: bool
    public_redistribution_allowed: bool
    reason_codes: tuple[str, ...]
    advisory_notes: tuple[str, ...]
    check_results: tuple[dict[str, Any], ...]


def _check(
    *,
    check_id: str,
    status: CheckStatus,
    severity: CheckSeverity,
    expected: str,
    observed: str,
) -> dict[str, Any]:
    return {
        "check_id": check_id,
        "expected": expected,
        "observed": observed,
        "severity": severity,
        "status": status,
    }


def _run_identity_matches_binding(
    run_identity: dict[str, Any],
    replay_binding: dict[str, Any],
) -> bool:
    return bool(
        run_identity["run_spec_id"] == replay_binding["run_spec_id"]
        and run_identity["execution_id"] == replay_binding["execution_id"]
        and run_identity["proof_artifact_hash"] == replay_binding["proof_artifact_hash"],
    )


def _manifest_matches_binding(
    manifest: dict[str, Any],
    replay_binding: dict[str, Any],
) -> bool:
    keys = (
        "replay_content_sha256",
        "replay_binding_id",
        "run_spec_id",
        "execution_id",
        "proof_artifact_hash",
        "lineage_seed_id",
    )
    return bool(all(manifest[k] == replay_binding[k] for k in keys))


def _manifest_matches_run_identity(
    manifest: dict[str, Any],
    run_identity: dict[str, Any],
) -> bool:
    return bool(
        manifest["run_spec_id"] == run_identity["run_spec_id"]
        and manifest["execution_id"] == run_identity["execution_id"]
        and manifest["proof_artifact_hash"] == run_identity["proof_artifact_hash"],
    )


def _describe_identity_conflicts(
    *,
    replay_binding: dict[str, Any],
    run_identity: dict[str, Any] | None,
    manifest: dict[str, Any] | None,
) -> str:
    conflicts: list[str] = []
    if run_identity is not None and not _run_identity_matches_binding(run_identity, replay_binding):
        conflicts.append("run_identity fields disagree with replay_binding")
    if manifest is not None and not _manifest_matches_binding(manifest, replay_binding):
        conflicts.append("manifest fields disagree with replay_binding")
    if (
        run_identity is not None
        and manifest is not None
        and not _manifest_matches_run_identity(manifest, run_identity)
    ):
        conflicts.append("manifest fields disagree with run_identity")
    return "; ".join(sorted(conflicts))


def evaluate_intake_policy(
    *,
    meta: NormalizedReplayIntakeMetadata | None,
    metadata_error: str | None,
    replay_path: Path,
    replay_sha256: str | None,
    replay_read_error: str | None,
    replay_binding: dict[str, Any] | None,
    replay_binding_error: str | None,
    run_identity: dict[str, Any] | None,
    run_identity_error: str | None,
    manifest: dict[str, Any] | None,
    manifest_error: str | None,
) -> PolicyOutcome:
    """Pure policy evaluation from loaded inputs and loader errors."""

    reason_codes: list[str] = []
    advisory_notes: list[str] = []
    checks: list[dict[str, Any]] = []

    expected_hash_mismatch = bool(
        meta is not None
        and replay_sha256 is not None
        and meta.expected_replay_content_sha256 is not None
        and meta.expected_replay_content_sha256 != replay_sha256,
    )

    binding_hash_mismatch = bool(
        replay_binding is not None
        and replay_sha256 is not None
        and replay_binding["replay_content_sha256"] != replay_sha256,
    )

    loader_rejected = bool(
        meta is None
        or replay_read_error is not None
        or replay_sha256 is None
        or expected_hash_mismatch
        or replay_binding_error is not None
        or binding_hash_mismatch
        or run_identity_error is not None
        or manifest_error is not None
    )

    semantic_identity_conflict = False
    identity_conflict_detail = ""
    if (
        not loader_rejected
        and replay_binding is not None
        and replay_binding_error is None
        and replay_sha256 is not None
        and replay_binding["replay_content_sha256"] == replay_sha256
        and run_identity_error is None
        and manifest_error is None
    ):
        identity_conflict_detail = _describe_identity_conflicts(
            manifest=manifest,
            replay_binding=replay_binding,
            run_identity=run_identity,
        )
        semantic_identity_conflict = bool(identity_conflict_detail)

    # 1. metadata_schema_valid
    if meta is None:
        checks.append(
            _check(
                check_id="metadata_schema_valid",
                status="fail",
                severity="required",
                expected=f"valid {NormalizedReplayIntakeMetadata.__name__}",
                observed=metadata_error or "invalid metadata",
            ),
        )
    else:
        checks.append(
            _check(
                check_id="metadata_schema_valid",
                status="pass",
                severity="required",
                expected="structurally valid replay intake metadata",
                observed="valid",
            ),
        )

    # 2. replay_file_readable
    if replay_read_error is not None:
        checks.append(
            _check(
                check_id="replay_file_readable",
                status="fail",
                severity="required",
                expected="replay file readable as opaque bytes",
                observed=replay_read_error,
            ),
        )
    else:
        checks.append(
            _check(
                check_id="replay_file_readable",
                status="pass",
                severity="required",
                expected="replay file readable as opaque bytes",
                observed=f"read {replay_path.name}",
            ),
        )

    # 3. replay_sha256_computed
    if replay_sha256 is None:
        checks.append(
            _check(
                check_id="replay_sha256_computed",
                status="fail",
                severity="required",
                expected="SHA-256 over replay bytes",
                observed=replay_read_error or "not computed",
            ),
        )
    else:
        checks.append(
            _check(
                check_id="replay_sha256_computed",
                status="pass",
                severity="required",
                expected="SHA-256 over replay bytes",
                observed=replay_sha256,
            ),
        )

    # 4–6
    if meta is None:
        for cid, label in (
            ("origin_class_declared", "declared_origin_class enum"),
            ("provenance_status_declared", "declared_provenance_status enum"),
            ("redistribution_posture_declared", "declared_redistribution_posture enum"),
        ):
            checks.append(
                _check(
                    check_id=cid,
                    status="not_evaluated",
                    severity="required",
                    expected=label,
                    observed="skipped (metadata invalid)",
                ),
            )
    else:
        checks.append(
            _check(
                check_id="origin_class_declared",
                status="pass",
                severity="required",
                expected="declared_origin_class is a governed enum",
                observed=meta.declared_origin_class,
            ),
        )
        checks.append(
            _check(
                check_id="provenance_status_declared",
                status="pass",
                severity="required",
                expected="declared_provenance_status is a governed enum",
                observed=meta.declared_provenance_status,
            ),
        )
        checks.append(
            _check(
                check_id="redistribution_posture_declared",
                status="pass",
                severity="required",
                expected="declared_redistribution_posture is a governed enum",
                observed=meta.declared_redistribution_posture,
            ),
        )

    # 7. expected_hash_match
    if meta is None or replay_sha256 is None:
        checks.append(
            _check(
                check_id="expected_hash_match",
                status="not_evaluated",
                severity="warning",
                expected="expected_replay_content_sha256 matches computed hash when provided",
                observed="not evaluated",
            ),
        )
    elif meta.expected_replay_content_sha256 is None:
        checks.append(
            _check(
                check_id="expected_hash_match",
                status="not_evaluated",
                severity="warning",
                expected="expected_replay_content_sha256 matches computed hash when provided",
                observed="no expected hash declared",
            ),
        )
    elif not expected_hash_mismatch:
        checks.append(
            _check(
                check_id="expected_hash_match",
                status="pass",
                severity="warning",
                expected="expected hash matches computed replay hash",
                observed="match",
            ),
        )
    else:
        checks.append(
            _check(
                check_id="expected_hash_match",
                status="fail",
                severity="warning",
                expected="expected hash matches computed replay hash",
                observed=(
                    f"mismatch: expected {meta.expected_replay_content_sha256} "
                    f"observed {replay_sha256}"
                ),
            ),
        )

    # 8. binding_hash_match
    if replay_binding_error is not None:
        checks.append(
            _check(
                check_id="binding_hash_match",
                status="fail",
                severity="required",
                expected=EXP_BINDING_HASH_EXPECTED,
                observed=replay_binding_error,
            ),
        )
    elif replay_binding is None:
        checks.append(
            _check(
                check_id="binding_hash_match",
                status="not_evaluated",
                severity="required",
                expected=EXP_BINDING_HASH_EXPECTED,
                observed="no replay_binding.json supplied",
            ),
        )
    elif replay_sha256 is None:
        checks.append(
            _check(
                check_id="binding_hash_match",
                status="fail",
                severity="required",
                expected=EXP_BINDING_HASH_EXPECTED,
                observed="no computed replay hash",
            ),
        )
    elif not binding_hash_mismatch:
        checks.append(
            _check(
                check_id="binding_hash_match",
                status="pass",
                severity="required",
                expected="binding replay hash matches computed replay hash",
                observed="match",
            ),
        )
    else:
        checks.append(
            _check(
                check_id="binding_hash_match",
                status="fail",
                severity="required",
                expected="binding replay hash matches computed replay hash",
                observed=(
                    f"mismatch: binding {replay_binding['replay_content_sha256']} "
                    f"observed replay {replay_sha256}"
                ),
            ),
        )

    # 9. binding_identity_consistent
    if replay_binding_error is not None or replay_binding is None:
        checks.append(
            _check(
                check_id="binding_identity_consistent",
                status="not_evaluated",
                severity="required",
                expected=EXP_LINKED_ARTIFACTS_CONSISTENT,
                observed="no valid replay binding loaded",
            ),
        )
    elif run_identity_error is not None:
        checks.append(
            _check(
                check_id="binding_identity_consistent",
                status="fail",
                severity="required",
                expected=EXP_LINKED_ARTIFACTS_CONSISTENT,
                observed=run_identity_error,
            ),
        )
    elif manifest_error is not None:
        checks.append(
            _check(
                check_id="binding_identity_consistent",
                status="fail",
                severity="required",
                expected=EXP_LINKED_ARTIFACTS_CONSISTENT,
                observed=manifest_error,
            ),
        )
    elif semantic_identity_conflict:
        checks.append(
            _check(
                check_id="binding_identity_consistent",
                status="fail",
                severity="required",
                expected="linked STARLAB artifacts agree on shared identity fields",
                observed=identity_conflict_detail,
            ),
        )
    elif run_identity is None and manifest is None:
        checks.append(
            _check(
                check_id="binding_identity_consistent",
                status="not_evaluated",
                severity="required",
                expected=EXP_LINKED_ARTIFACTS_CONSISTENT,
                observed="no run_identity or manifest supplied",
            ),
        )
    else:
        checks.append(
            _check(
                check_id="binding_identity_consistent",
                status="pass",
                severity="required",
                expected="linked STARLAB artifacts agree on shared identity fields",
                observed="consistent",
            ),
        )

    # Reason codes
    if meta is None:
        reason_codes.append("metadata_schema_invalid")
    if replay_read_error is not None:
        reason_codes.append("replay_unreadable")
    if expected_hash_mismatch:
        reason_codes.append("expected_hash_mismatch")
    if replay_binding_error is not None:
        reason_codes.append("replay_binding_malformed")
    if binding_hash_mismatch:
        reason_codes.append("replay_binding_hash_mismatch")
    if run_identity_error is not None:
        reason_codes.append("run_identity_malformed")
    if manifest_error is not None:
        reason_codes.append("run_artifact_manifest_malformed")
    if semantic_identity_conflict:
        reason_codes.append("evidence_conflict")

    quarantine_redist = (
        not loader_rejected
        and meta is not None
        and meta.declared_redistribution_posture == "forbidden"
    )
    if quarantine_redist:
        reason_codes.append("redistribution_forbidden")

    intake_status: IntakeStatus
    if loader_rejected:
        intake_status = "rejected"
    elif quarantine_redist or semantic_identity_conflict:
        intake_status = "quarantined"
    elif meta is not None:
        eligible = _is_eligible_for_canonical_review(
            meta=meta,
            replay_binding_present=replay_binding is not None and replay_binding_error is None,
        )
        if eligible:
            intake_status = "eligible_for_canonical_review"
        else:
            intake_status = "accepted_local_only"
            if meta.declared_origin_class == "starlab_generated" and (
                replay_binding is None or replay_binding_error is not None
            ):
                advisory_notes.append(
                    "starlab_generated without a consistent M04 replay_binding.json; "
                    "canonical review blocked",
                )
            if meta.declared_provenance_status in ("asserted", "unknown"):
                advisory_notes.append(
                    "provenance posture is not verified; canonical review blocked"
                )
            if meta.declared_redistribution_posture == "unknown":
                advisory_notes.append("redistribution posture unknown; canonical review blocked")
    else:
        intake_status = "rejected"
        reason_codes.append("policy_internal_invariant")

    reason_codes_sorted = sorted(set(reason_codes))
    advisory_sorted = sorted(set(advisory_notes))

    # 10. canonical_review_requirements_met
    if intake_status == "eligible_for_canonical_review":
        cr_status: CheckStatus = "pass"
        cr_observed = "eligible_for_canonical_review"
    elif intake_status == "accepted_local_only":
        cr_status = "warn"
        cr_observed = "accepted_local_only"
    elif intake_status == "quarantined":
        cr_status = "fail"
        cr_observed = "quarantined"
    else:
        cr_status = "fail"
        cr_observed = "rejected"

    checks.append(
        _check(
            check_id="canonical_review_requirements_met",
            status=cr_status,
            severity="required",
            expected="policy outcome supports canonical review eligibility per M07 rules",
            observed=cr_observed,
        ),
    )

    assert len(checks) == len(CHECK_IDS), (len(checks), CHECK_IDS)

    local_ok = intake_status in ("eligible_for_canonical_review", "accepted_local_only")
    cr_eligible = intake_status == "eligible_for_canonical_review"
    public_ok = intake_status == "eligible_for_canonical_review" and (
        meta is not None and meta.declared_redistribution_posture == "allowed"
    )

    return PolicyOutcome(
        intake_status=intake_status,
        local_processing_allowed=local_ok,
        canonical_review_eligible=cr_eligible,
        public_redistribution_allowed=public_ok,
        reason_codes=tuple(reason_codes_sorted),
        advisory_notes=tuple(advisory_sorted),
        check_results=tuple(checks),
    )


def _is_eligible_for_canonical_review(
    *,
    meta: NormalizedReplayIntakeMetadata,
    replay_binding_present: bool,
) -> bool:
    """Whether declared posture meets canonical-review bar (before evidence checks)."""

    if meta.declared_provenance_status != "verified":
        return False
    if meta.declared_redistribution_posture != "allowed":
        return False
    if meta.declared_origin_class == "starlab_generated":
        return replay_binding_present
    return True
