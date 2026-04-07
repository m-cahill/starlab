"""Environment drift evaluation against governed smoke matrix (M06)."""

from __future__ import annotations

from typing import Any, Literal

from starlab.runs.json_util import canonical_json_dumps
from starlab.sc2.models import Sc2RuntimeSpec
from starlab.sc2.runtime_smoke_matrix import (
    CI_PROFILE,
    LATER_MILESTONES,
    LOCAL_PROFILE,
    build_runtime_smoke_matrix,
)

DRIFT_REPORT_SCHEMA_VERSION = "starlab.environment_drift_report.v1"

CheckStatus = Literal["pass", "warn", "fail", "not_evaluated"]
CheckSeverity = Literal["required", "warning"]

CANONICAL_CONTROL = Sc2RuntimeSpec().control_observation_surface
CANONICAL_REPLAY_DECODE = Sc2RuntimeSpec().replay_decode_surface


def validate_m01_probe_surface(probe: dict[str, Any]) -> list[str]:
    """Deterministic structural validation of M01 probe JSON; empty list if valid."""

    errors: list[str] = []
    required_top = (
        "base_build",
        "data_version",
        "interface_modes",
        "notes",
        "paths",
        "present",
        "spec",
    )
    for key in required_top:
        if key not in probe:
            errors.append(f"missing top-level key: {key!r}")

    if errors:
        return errors

    if probe["base_build"] is not None and not isinstance(probe["base_build"], str):
        errors.append("base_build must be string or null")
    if probe["data_version"] is not None and not isinstance(probe["data_version"], str):
        errors.append("data_version must be string or null")

    im = probe["interface_modes"]
    if not isinstance(im, dict):
        errors.append("interface_modes must be an object")
    else:
        for k in ("feature_layer_interface", "raw_interface", "rendered_interface"):
            if k not in im:
                errors.append(f"interface_modes missing key: {k!r}")
            elif not isinstance(im[k], bool):
                errors.append(f"interface_modes[{k!r}] must be boolean")

    notes = probe["notes"]
    if not isinstance(notes, list) or not all(isinstance(x, str) for x in notes):
        errors.append("notes must be a list of strings")

    paths = probe["paths"]
    if not isinstance(paths, dict):
        errors.append("paths must be an object")
    else:
        for k, v in paths.items():
            if not isinstance(k, str):
                errors.append("paths keys must be strings")
                break
            if v is not None and not isinstance(v, str):
                errors.append(f"paths[{k!r}] must be string or null")
                break

    present = probe["present"]
    if not isinstance(present, dict):
        errors.append("present must be an object")
    else:
        for k, v in present.items():
            if not isinstance(k, str):
                errors.append("present keys must be strings")
                break
            if not isinstance(v, bool):
                errors.append(f"present[{k!r}] must be boolean")
                break

    spec = probe["spec"]
    if not isinstance(spec, dict):
        errors.append("spec must be an object")
    else:
        if "control_observation_surface" not in spec:
            errors.append("spec missing control_observation_surface")
        elif not isinstance(spec["control_observation_surface"], str):
            errors.append("spec.control_observation_surface must be a string")
        if "replay_decode_surface" not in spec:
            errors.append("spec missing replay_decode_surface")
        elif not isinstance(spec["replay_decode_surface"], str):
            errors.append("spec.replay_decode_surface must be a string")

    if not errors and isinstance(spec, dict):
        cos = spec["control_observation_surface"]
        rds = spec["replay_decode_surface"]
        if cos != CANONICAL_CONTROL:
            errors.append(
                f"spec.control_observation_surface must be {CANONICAL_CONTROL!r} (M01 boundary)",
            )
        if rds != CANONICAL_REPLAY_DECODE:
            errors.append(
                f"spec.replay_decode_surface must be {CANONICAL_REPLAY_DECODE!r} (M01 boundary)",
            )

    return errors


def derive_runtime_boundary_label(probe: dict[str, Any]) -> str | None:
    """Runtime boundary label from probe (M01/M03-compatible string)."""

    spec = probe.get("spec")
    if not isinstance(spec, dict):
        return None
    cos = spec.get("control_observation_surface")
    if isinstance(cos, str) and cos.strip():
        return cos
    return None


def _check_result(
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


def _is_blank_optional_str(value: Any) -> bool:
    return value is None or (isinstance(value, str) and not value.strip())


def evaluate_environment_drift(
    *,
    probe: dict[str, Any],
    profile: str,
    run_identity: dict[str, Any] | None,
) -> dict[str, Any]:
    """Build deterministic ``environment_drift_report.json`` body."""

    if profile not in (CI_PROFILE, LOCAL_PROFILE):
        msg = f"unknown profile: {profile!r}"
        raise ValueError(msg)

    boundary = derive_runtime_boundary_label(probe)
    matrix_label = boundary if boundary is not None else ""

    validation_errors = validate_m01_probe_surface(probe)
    probe_ok = not validation_errors

    probe_schema_status: CheckStatus = "pass" if probe_ok else "fail"
    probe_schema_observed = "valid M01 probe surface" if probe_ok else "; ".join(validation_errors)
    checks: list[dict[str, Any]] = [
        _check_result(
            check_id="probe_schema_valid",
            expected="structurally valid M01 probe JSON with canonical runtime surfaces",
            observed=probe_schema_observed,
            severity="required",
            status=probe_schema_status,
        ),
    ]

    rbl_ok = boundary == CANONICAL_CONTROL
    rbl_status: CheckStatus = "pass" if rbl_ok else "fail"
    checks.append(
        _check_result(
            check_id="runtime_boundary_label_present",
            expected=f"spec.control_observation_surface == {CANONICAL_CONTROL!r}",
            observed=boundary if boundary is not None else "(missing or invalid spec)",
            severity="required",
            status=rbl_status,
        ),
    )

    fingerprint: dict[str, Any] | None = None
    fingerprint_comparison_performed = run_identity is not None
    environment_fingerprint_used = False
    advisory_notes: list[str] = []

    if run_identity is not None:
        fp_raw = run_identity.get("environment_fingerprint")
        if fp_raw is not None:
            if not isinstance(fp_raw, dict):
                msg = "run_identity.environment_fingerprint must be an object or null"
                raise ValueError(msg)
            fingerprint = fp_raw if fp_raw else None
            environment_fingerprint_used = fingerprint is not None

    if profile == LOCAL_PROFILE:
        # adapter_name_present: fingerprint only; else not_evaluated
        if fingerprint is None or not fingerprint:
            checks.append(
                _check_result(
                    check_id="adapter_name_present",
                    expected="environment_fingerprint.adapter_name present when fingerprint exists",
                    observed="no environment_fingerprint supplied",
                    severity="warning",
                    status="not_evaluated",
                ),
            )
        else:
            an = fingerprint.get("adapter_name")
            if isinstance(an, str) and an.strip():
                checks.append(
                    _check_result(
                        check_id="adapter_name_present",
                        expected="non-empty adapter_name in fingerprint",
                        observed=an,
                        severity="warning",
                        status="pass",
                    ),
                )
            else:
                checks.append(
                    _check_result(
                        check_id="adapter_name_present",
                        expected="non-empty adapter_name in fingerprint",
                        observed="adapter_name missing or empty",
                        severity="warning",
                        status="warn",
                    ),
                )

        bb_cap = not _is_blank_optional_str(probe.get("base_build"))
        checks.append(
            _check_result(
                check_id="base_build_captured",
                expected=(
                    "base_build non-null non-empty (captured) or intentionally null (unknown)"
                ),
                observed=str(probe.get("base_build"))
                if probe.get("base_build") is not None
                else "null",
                severity="warning",
                status="pass" if bb_cap else "warn",
            ),
        )

        dv_cap = not _is_blank_optional_str(probe.get("data_version"))
        checks.append(
            _check_result(
                check_id="data_version_captured",
                expected=(
                    "data_version non-null non-empty (captured) or intentionally null (unknown)"
                ),
                observed=str(probe.get("data_version"))
                if probe.get("data_version") is not None
                else "null",
                severity="warning",
                status="pass" if dv_cap else "warn",
            ),
        )

    if fingerprint:
        # Overlapping drift checks (warning severity)
        fp_boundary = fingerprint.get("runtime_boundary_label")
        if isinstance(fp_boundary, str) and fp_boundary.strip():
            match = fp_boundary == boundary
            checks.append(
                _check_result(
                    check_id="fingerprint_runtime_boundary_match",
                    expected="fingerprint.runtime_boundary_label matches probe-derived boundary",
                    observed=f"probe={boundary!r} fingerprint={fp_boundary!r}",
                    severity="warning",
                    status="pass" if match else "warn",
                ),
            )
        elif fp_boundary is not None:
            checks.append(
                _check_result(
                    check_id="fingerprint_runtime_boundary_match",
                    expected="fingerprint.runtime_boundary_label comparable string",
                    observed="fingerprint.runtime_boundary_label invalid or empty",
                    severity="warning",
                    status="warn",
                ),
            )

        pb = probe.get("base_build")
        fb = fingerprint.get("base_build")
        if fb is not None or pb is not None:
            if pb is None and fb is not None:
                advisory_notes.append(
                    "fingerprint has base_build but probe base_build is null (advisory).",
                )
                checks.append(
                    _check_result(
                        check_id="fingerprint_base_build_match",
                        expected="probe.base_build matches fingerprint when both set",
                        observed=f"probe=null fingerprint={fb!r}",
                        severity="warning",
                        status="warn",
                    ),
                )
            elif fb is None and pb is not None:
                advisory_notes.append(
                    "probe has base_build but fingerprint base_build is null (advisory).",
                )
                checks.append(
                    _check_result(
                        check_id="fingerprint_base_build_match",
                        expected="probe.base_build matches fingerprint when both set",
                        observed=f"probe={pb!r} fingerprint=null",
                        severity="warning",
                        status="warn",
                    ),
                )
            elif isinstance(pb, str) and isinstance(fb, str):
                match = pb == fb
                checks.append(
                    _check_result(
                        check_id="fingerprint_base_build_match",
                        expected="probe.base_build equals fingerprint.base_build",
                        observed=f"probe={pb!r} fingerprint={fb!r}",
                        severity="warning",
                        status="pass" if match else "warn",
                    ),
                )

        pdv = probe.get("data_version")
        fdv = fingerprint.get("data_version")
        if fdv is not None or pdv is not None:
            if pdv is None and fdv is not None:
                advisory_notes.append(
                    "fingerprint has data_version but probe data_version is null (advisory).",
                )
                checks.append(
                    _check_result(
                        check_id="fingerprint_data_version_match",
                        expected="probe.data_version matches fingerprint when both set",
                        observed=f"probe=null fingerprint={fdv!r}",
                        severity="warning",
                        status="warn",
                    ),
                )
            elif fdv is None and pdv is not None:
                advisory_notes.append(
                    "probe has data_version but fingerprint data_version is null (advisory).",
                )
                checks.append(
                    _check_result(
                        check_id="fingerprint_data_version_match",
                        expected="probe.data_version matches fingerprint when both set",
                        observed=f"probe={pdv!r} fingerprint=null",
                        severity="warning",
                        status="warn",
                    ),
                )
            elif isinstance(pdv, str) and isinstance(fdv, str):
                match = pdv == fdv
                checks.append(
                    _check_result(
                        check_id="fingerprint_data_version_match",
                        expected="probe.data_version equals fingerprint.data_version",
                        observed=f"probe={pdv!r} fingerprint={fdv!r}",
                        severity="warning",
                        status="pass" if match else "warn",
                    ),
                )

        # Advisory-only fields (adapter_name uses adapter_name_present when fingerprint exists)
        for label, key in (
            ("platform_string (advisory)", "platform_string"),
            ("probe_digest (advisory)", "probe_digest"),
        ):
            val = fingerprint.get(key)
            if val is not None and val != "":
                advisory_notes.append(
                    f"fingerprint.{key} present ({label}); advisory context in M06.",
                )

    overall = _compute_overall_status(checks)
    return {
        "advisory_notes": sorted(advisory_notes),
        "check_results": checks,
        "environment_fingerprint_used": environment_fingerprint_used,
        "fingerprint_comparison_performed": fingerprint_comparison_performed,
        "later_milestones": list(LATER_MILESTONES),
        "overall_status": overall,
        "profile": profile,
        "runtime_boundary_label": matrix_label,
        "schema_version": DRIFT_REPORT_SCHEMA_VERSION,
    }


def _compute_overall_status(checks: list[dict[str, Any]]) -> CheckStatus:
    if any(c["severity"] == "required" and c["status"] == "fail" for c in checks):
        return "fail"
    if any(c["status"] in ("warn", "fail") for c in checks):
        return "warn"
    return "pass"


def emit_m06_artifacts(
    *,
    probe: dict[str, Any],
    profile: str,
    run_identity: dict[str, Any] | None,
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Return ``(smoke_matrix, drift_report)`` bodies."""

    report = evaluate_environment_drift(
        probe=probe,
        profile=profile,
        run_identity=run_identity,
    )
    matrix = build_runtime_smoke_matrix(
        runtime_boundary_label=str(report["runtime_boundary_label"]),
    )
    return matrix, report


def matrix_to_json(matrix: dict[str, Any]) -> str:
    return canonical_json_dumps(matrix)


def report_to_json(report: dict[str, Any]) -> str:
    return canonical_json_dumps(report)
